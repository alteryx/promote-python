import promote
from schema import Schema

import newspaper
from newspaper import Article

USERNAME = "colin"
API_KEY = "d580d451-06b9-4c10-a73f-523adca5f48c"
PROMOTE_URL = "http://localhost:3000/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

@promote.validate_json(Schema({'url': str}))
def promoteModel(data):
    # print(weights)
    art = Article(url=data['url'], language='en')
    art.download()
    art.parse()
    art.nlp()
    result = art.summary
    return {"summary": result}


TESTURL = "https://new.surfline.com/surf-news/santa-cruz-surf-character-catches-final-wave/10365"
TESTDATA = {"url": TESTURL}

# test the model locally
print(promoteModel(TESTDATA))

# name and deploy our model
p.deploy("ArticleSummarizer", promoteModel, TESTDATA, True)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("ArticleSummarizer", testdata)

# example result:
# {
#     'summary': 'Never sporting a wetsuit, but always a smile, Marty “The Mechanic”
#     Schreiber was an unmistakable personality amongst the Santa Cruz
#     surf community.\n“I was really blown away,” said longtime Santa Cruz
#     native Ken “Skindog” Collins.\nEven in the dead of winter, he’d brave
#     the brutal Santa Cruz water without a wetsuit.\nBut Marty Mechanic was one
#     of ‘em.\nHe could be seen driving a truck emblazoned by the words, “Marty
#     The Mechanic,” which became a fitting moniker.'
#   }
