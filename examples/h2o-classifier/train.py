import h2o
from h2o.estimators import H2ORandomForestEstimator

import os

# Alteryx recommends limiting the amount of memory that h2o can consume with the `max_mem_size` flag.
# the defualt is 4gb, which is likely more than you need!
h2o.init(max_mem_size='100m')

data = h2o.import_file('iris.csv')

training_columns =  ['C1', 'C2', 'C3', 'C4']
response_column = 'C5'

train, test = data.split_frame(ratios=[0.8])

model = H2ORandomForestEstimator(ntrees=50, max_depth=20, nfolds=10)
model.train(x=training_columns, y=response_column, training_frame=train)

save_path = os.path.realpath('.') + '/objects/'
model_path = h2o.save_model(model=model, path=save_path, force=True)

# h2o uses the model_id (random) to name the model, so we're going to rename it to something else
# so we can access it in the deploy script
os.rename(model_path, os.path.join(save_path, 'h2o_rf_model'))
