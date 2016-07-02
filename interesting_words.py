import json, re

from stemming import porter2



with open('stuff/stem_to_count.json') as f:
  text = f.read()
stem_to_count = json.loads(text)


stem_to_word = {}
def stem(word, word_to_stem={}):
  if word not in word_to_stem:
    word_to_stem[word] = porter2.stem(word)
  if word_to_stem[word] not in stem_to_word:
    stem_to_word[word_to_stem[word]] = word
  return word_to_stem[word]

with open('stuff/lambda_the_ultimate.txt') as f:
  text = f.read()

words = (word.strip("'") for word in re.findall("([\w']+)", text) if word not in stem_to_word)
tokens = [stem(word.lower()) for word in words]

token_to_count = {}
for token in tokens:
  token_to_count.setdefault(token, 0)
  token_to_count[token] += 1

rare_words = [
  stem_to_word[t[0]] for t in sorted(token_to_count.iteritems(), key=lambda t: t[1])][:100]
print ' '.join(rare_words)
