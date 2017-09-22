## Article Summarizer

Project structure:

```
├── README.md
├── main.py
├── promote.sh
└── requirements.txt
```

### Instructions

In a terminal shell run:

```bash
$ pip install requirements.txt

# we need to install the 'punkt' nltk package for the NLP summarization
$ python -c "import nltk; nltk.download('punkt')"

# lastly, deploy the model
$ python main.py
```

### Example input:

```
{"url": "https://new.surfline.com/surf-news/santa-cruz-surf-character-catches-final-wave/10365"}
```

### Result

```
{'summary': 'Never sporting a wetsuit, but always a smile, Marty “The Mechanic” Schreiber was an unmistakable personality amongst the Santa Cruz surf community.\n“I was really blown away,” said longtime Santa Cruz native Ken “Skindog” Collins.\nEven in the dead of winter, he’d brave the brutal Santa Cruz water without a wetsuit.\nBut Marty Mechanic was one of ‘em.\nHe could be seen driving a truck emblazoned by the words, “Marty The Mechanic,” which became a fitting moniker.'}
```