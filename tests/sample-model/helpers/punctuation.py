import re
import string

regex = re.compile('[%s]' % re.escape(string.punctuation))

def cleanName(name):
    return regex.sub('', name)