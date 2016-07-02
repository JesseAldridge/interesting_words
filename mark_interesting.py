import curses, shutil, os

categories_path = os.path.join('stuff/categories')

def main(stdscr):
  # Wipe categories and read list of paths.

  if os.path.exists(categories_path):
    assert os.path.basename(categories_path) == 'categories'
    shutil.rmtree(categories_path)
  os.mkdir(categories_path)
  with open('stuff/paths.txt') as f:
    text = f.read()

  # Use arrow keys to classify paths and write them to interesting or not files.

  h, w, y, x = 0, 0, 2, 0
  text_win = stdscr.subwin(h, w, y, x)
  for curr_path in text.splitlines():
    with open(curr_path) as f:
      text = f.read()
    stdscr.clear()
    stdscr.addstr(0, 0, curr_path)
    stdscr.addstr(1, 0, '<- no          yes ->')
    try:
      text_win.addstr(1, 0, '\n'.join(text.splitlines()[:10]))
    except TypeError:
      pass
    except Exception as e:
      text_win.clear()
      text_win.addstr(1, 0, str(e), curses.A_REVERSE)
    c = stdscr.getch()
    if c == curses.KEY_LEFT:
      append('interesting', curr_path)
    elif c == curses.KEY_RIGHT:
      append('not-interesting', curr_path)
    elif c == ord('q'):
        break

def append(basename, path):
  with open(os.path.join(categories_path, '{}.txt'.format(basename)), 'a') as f:
    f.write(path)

if __name__ == '__main__':
  curses.wrapper(main)
