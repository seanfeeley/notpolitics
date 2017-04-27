from textblob import TextBlob
import pprint, json, random

text = 'Indo-British APPG familiarisation visit to develop understanding of. Indian policy aims and meet key decision makers in government and business.'
text = 'Brother, James Atkins, is Managing Director of Strategy, Business Development and Digital for Europe, the Middle East and Africa, and Deputy Chairman of Public Affairs for Europe, the Middle East and Africa at Burson-Marsteller.'

blob = TextBlob(text)

# print dir(blob)
# print '\n\n'

# print help(blob)
# j = blob.to_json()

# pprint.pprint(json.loads(blob.json))
# print ''
# print blob.words
# print''
# print blob.noun_phrases
# print ''
# pprint.pprint(json.loads(j))
# print j
# for sentence in blob.sentences:
# 	print sentence


nouns = list()
for word, tag in blob.tags:
	print tag
	if tag == 'NN':
		nouns.append(word.lemmatize())
print nouns
print "This text is about..."
# for item in random.sample(nouns, 5):
# 	word = Word(item)
# 	print word.pluralize()