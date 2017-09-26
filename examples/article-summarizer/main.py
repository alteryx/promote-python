import promote
from schema import Schema

import newspaper
from newspaper import Article

p = promote.Promote("colin", "789asdf879h789a79f79sf79s",
                    "https://sandbox.c.yhat.com/")

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
# p.deploy("ArticleSummarizer", promoteModel, TESTDATA,
        #  confirm=True, dry_run=True, verbose=0)

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
