import curses, shutil, os


class Category:
  categories_path = os.path.join('stuff/categories')
  seen = set()

  def __init__(self, basename):
    self.basename = basename
    self.path = os.path.join(self.categories_path, '{}.txt'.format(basename))
    self.entries = set()
    if os.path.exists(self.path):
      with open(self.path) as f:
        text = f.read()
      self.entries = set(text.splitlines())
      self.seen |= self.entries

  def append(self, path):
    self.entries.add(path)
    with open(os.path.join(self.categories_path, '{}.txt'.format(self.basename)), 'a') as f:
      f.write(path + '\n')

def walk_dir(root_path):
  # Walk through the root, yielding each path.

  for filename in os.listdir(root_path):
    child_path = os.path.join(root_path, filename)
    if filename.startswith('.'):
      continue
    if os.path.isdir(child_path) and not os.path.islink(root_path):
      for grandchild_path in walk_dir(child_path):
        yield grandchild_path
    else:
      yield child_path

def build_categories():
  if not os.path.exists(Category.categories_path):
    os.mkdir(Category.categories_path)
  return (Category(name) for name in ('interesting', 'not-interesting'))


def main(stdscr):
  def debugger():
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()

  interesting, not_interesting = build_categories()

  # Use arrow keys to classify paths and write them to interesting or not files.

  h, w, y, x = 0, 0, 2, 0
  text_win = stdscr.subwin(h, w, y, x)
  for curr_path in walk_dir(os.path.join(os.path.expanduser('~/Dropbox'))):
    if curr_path in Category.seen:
      continue
    with open(curr_path) as f:
      text = f.read()
    stdscr.clear()
    stdscr.addstr(0, 0, curr_path)
    stdscr.addstr(1, 0, '<- no          yes ->')
    lines = text.splitlines()
    cropped_text = '\n'.join(line[:50] for line in lines[:20])
    try:
      text_win.addstr(1, 0, cropped_text)
    except TypeError:
      pass
    except Exception as e:
      text_win.clear()
      text_win.addstr(1, 0, str(e), curses.A_REVERSE)
    c = stdscr.getch()
    if c == curses.KEY_LEFT:
      not_interesting.append(curr_path)
    elif c == curses.KEY_RIGHT:
      interesting.append(curr_path)
    elif c == ord('q'):
        break


if __name__ == '__main__':
  curses.wrapper(main)
