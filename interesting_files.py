import os

from ascii_graph import Pyasciigraph

import mark_interesting


def sizeof_fmt(num, suffix='B'):
  for unit in ['','K','M','G','T','P','E','Z']:
      if abs(num) < 1024.0:
          return "%3.1f%s%s" % (num, unit, suffix)
      num /= 1024.0
  return "%.1f%s%s" % (num, 'Yi', suffix)


interesting, not_interesting = mark_interesting.build_categories()

labeled_sizes = []
for category in interesting, not_interesting:
  labeled_sizes += [
    ('{}|{}'.format(category.basename[0], path[-10:]), os.path.getsize(path))
    for path in category.entries]

labeled_sizes.sort(key=lambda t: t[1])
labeled_sizes = labeled_sizes[int(len(labeled_sizes) * .1):int(len(labeled_sizes) * .9)]
labeled_sizes.sort(key=lambda t: t[0])

graph = Pyasciigraph()
for line in graph.graph('test print', labeled_sizes):
    print line
