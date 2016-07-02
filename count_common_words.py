import json, itertools, re, os, codecs

import mark_interesting


non_word_regex = re.compile('[0-9\W_]+', re.UNICODE)
def split_words(text):
  return [word.lower() for word in re.split(non_word_regex, text) if word]

word_to_count = {}
word_to_path = {}
extensions = {'py', 'js', 'html', 'txt', 'css'}
for path in itertools.islice(mark_interesting.walk_dir(os.path.expanduser('~/Dropbox')), 1000):
  print 'path:', path
  if path.rsplit('.', 1)[-1] in extensions:
    with codecs.open(path, encoding='utf-8') as f:
      text = f.read()

    for word in split_words(text):
      word_to_count.setdefault(word, 0)
      word_to_count[word] += 1
      word_to_path[word] = path

print '--done--'
json_text = json.dumps(sorted(word_to_count.iteritems(), key=lambda t:-t[1]), indent=2)
with open('stuff/word_to_count.json', 'w') as f:
  f.write(json_text)
