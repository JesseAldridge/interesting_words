import curses, shutil, os


def main(stdscr):
  # Wipe categories and read list of paths.

  if os.path.exists('categories'):
    shutil.rmtree('categories')
  os.mkdir('categories')
  with open('paths.txt') as f:
    text = f.read()

  h, w, y, x = 0, 0, 1, 0
  text_win = stdscr.subwin(h, w, y, x)

  # Use arrow keys to classify paths and write them to interesting or not files.

  for curr_path in text.splitlines():
    with open(curr_path) as f:
      text = f.read()
    stdscr.clear()
    stdscr.addstr(0, 0, curr_path)
    try:
      text_win.addstr(1, 0, text)
    except TypeError:
      pass
    except Exception as e:
      text_win.clear()
      text_win.addstr(1, 0, str(e), curses.A_REVERSE)
    c = stdscr.getch()
    if c == curses.KEY_LEFT:
      with open(os.path.join('categories', 'interesting.txt'), 'a') as f:
        f.write(curr_path)
    elif c == curses.KEY_RIGHT:
      with open(os.path.join('categories', 'not-interesting.txt'), 'a') as f:
        f.write(curr_path)
    elif c == ord('q'):
        break

if __name__ == '__main__':
  curses.wrapper(main)
