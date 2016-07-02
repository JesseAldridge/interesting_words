import json, itertools, re, os, codecs

from stemming import porter2

import mark_interesting


non_word_regex = re.compile('[0-9\W_]+', re.UNICODE)
def split_words(text):
  return [word.lower() for word in re.split(non_word_regex, text) if word]

def stem_word(word, cache={}):
  if word not in cache:
    cache[word] = porter2.stem(word)
  return cache[word]

stem_to_count = {}
stem_to_path = {}
extensions = {'py', 'js', 'html', 'txt', 'css'}
for path in itertools.islice(mark_interesting.walk_dir(os.path.expanduser('~/Dropbox')), 1000):
  print 'path:', path
  if path.rsplit('.', 1)[-1] in extensions:
    with codecs.open(path, encoding='utf-8') as f:
      text = f.read()

    for word in split_words(text):
      stem = stem_word(word)
      stem_to_count.setdefault(stem, 0)
      stem_to_count[stem] += 1
      stem_to_path[stem] = path

print '--done--'
json_text = json.dumps(sorted(stem_to_count.iteritems(), key=lambda t:-t[1]), indent=2)
with open('stuff/stem_to_count.json', 'w') as f:
  f.write(json_text)
