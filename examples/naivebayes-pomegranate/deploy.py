import promote
from schema import Schema
from pomegranate import NaiveBayes, NormalDistribution
import json

WEIGHTS = json.load(open('./objects/naive_weights.pomo'))

model = NaiveBayes.from_json(WEIGHTS)

def NaiveBayes(data):
    r = model.predict(data).tolist()
    return r

USERNAME = "ross"
API_KEY = "2dcf2d39-0d4a-4d4b-b79d"
PROMOTE_URL = "http://promote.x.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

TESTDATA = [19.08025296, -2.94031655, 9.06747934, 3.30080305, 1.62963848]
print(NaiveBayes(TESTDATA))

# name and deploy our model
p.deploy("NaiveBayes", NaiveBayes, TESTDATA)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("actionProbState", TESTDATA)
