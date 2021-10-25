import numpy as np
import tensorflow as tf
import promote
import base64
from io import BytesIO
from PIL import Image, ImageChops
from time import time
import operator

USERNAME = 'username'
API_KEY = 'your_api_key'
PROMOTE_URL = 'http://www.promote_url.com'
p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""
    # Input Layer
    input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    # Convolutional Layer #1
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,
        kernel_size=[5, 5],
        padding="same",
    activation=tf.nn.relu)

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(
        inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=10)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probs": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

mnist_classifier = tf.estimator.Estimator(
    model_fn=cnn_model_fn, model_dir="./objects/mnist_convnet_model")

STANDARD_SIZE = (28,28)
def tensorflow_model(data):
    image_string = data["image_string"]
    b = base64.decodebytes(bytes(image_string,'utf-8'))
    f = BytesIO(b)
    img = Image.open(f)
    img = img.convert('1')

    # crop whitespace
    bg = Image.new(img.mode, img.size, 255)
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        bbox = tuple(map(operator.add, bbox, (-15,-15,15,15)))
        bbox = tuple(np.minimum(np.maximum(bbox,0),img.size[0]))
        img = img.crop(bbox)

    img_data = img.getdata()
    img_wide = (255-np.float32(np.array(list(img_data.resize(STANDARD_SIZE)))))/255
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": np.array([img_wide])},
        num_epochs=1,
        shuffle=False)
    predict_results = list(mnist_classifier.predict(predict_input_fn,yield_single_examples=True))[0]

    buffered = BytesIO()
    img.resize(STANDARD_SIZE).save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    predict_results['classes'] = int(predict_results['classes'])
    predict_results['img'] = img_str.decode()
    predict_results['ts'] = data["request_timestamp"]
    return predict_results

with open("./objects/image.png", "rb") as image_file:
    image_string = base64.b64encode(image_file.read()).decode()
TESTDATA = {"image_string":image_string,"request_timestamp":time()}
print(tensorflow_model(TESTDATA))

p.deploy("TensorFlowClassifier", tensorflow_model, TESTDATA, confirm=False, dry_run=False)
