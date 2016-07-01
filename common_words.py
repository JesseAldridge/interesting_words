import os, itertools, re


dir_path = os.path.join(os.path.expanduser('~/Dropbox'))

def walk_dir(root_path):
    # Walk through the root, yielding each path.

    for filename in os.listdir(root_path):
        child_path = os.path.join(root_path, filename)
        if filename.startswith('.'):
            continue
        if os.path.isdir(child_path) and not os.path.islink(root_path):
            for grandchild_path in walk_dir(child_path):
                yield grandchild_path
        yield child_path

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

for path in itertools.islice(walk_dir(dir_path), 100):
  print '{:<7} {}'.format(sizeof_fmt(os.path.getsize(path))[:7], path)
  # with open(path) as f:
  #   text = f.read()
  # [word.lower() for word in re.split(non_word_regex, text) if word]
