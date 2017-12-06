import h2o
from h2o.estimators import H2ORandomForestEstimator

import os

h2o.init()
data = h2o.import_file('iris.csv')

training_columns =  ['C1', 'C2', 'C3', 'C4']
response_column = 'C5'

train, test = data.split_frame(ratios=[0.8])

model = H2ORandomForestEstimator(ntrees=50, max_depth=20, nfolds=10)
model.train(x=training_columns, y=response_column, training_frame=train)

save_path = os.path.realpath('.') + '/objects/'
h2o.save_model(model=model, path=save_path)