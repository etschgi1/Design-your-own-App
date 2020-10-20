#!/bin/python3
# https://github.com/SimonLammer/testpythonscript

"""
Attention students: these tests only check some core functionality, they do NOT replace your own testing!

This can be used to test other python scripts.
Other scripts will be imported and tested in a new subprocess each.
"""

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta
from importlib import import_module
import io
import multiprocessing
import os
from pathlib import Path
import re
import sys
import textwrap
import threading
import time
import traceback
from types import FunctionType, ModuleType
from typing import Callable, Dict, List, Optional, Tuple
import unittest

TESTSUITE_DESCRIPTION = "Design your own app - Intermediate assignment (Snake) testsuite - student version" # displayed in help message

LIBRARY = None # This will be set to the imported script

EVALUATION = {i: 0.0 for i in range(1, 8)}

class TestCaseBase(unittest.TestCase):
  def setUp(self):
    global EVALUATION
    reinitialize_library_attributes()
    self.initial_evaluation = EVALUATION.copy()

  def tearDown(self):
    global EVALUATION
    EVALUATION = {i: round(EVALUATION[i], 1) for i in EVALUATION.keys()}
    evaluation_delta = {i: EVALUATION[i] - self.initial_evaluation[i] for i in EVALUATION.keys()}
    print(f"{' ' * (49 - len(self.id()))}evaluation: {evaluation_delta}", end='\t')

  def evaluation(self, category: int, value: int):
    global EVALUATION
    EVALUATION[category] += value

  def set_default_attributes(self):
    LIBRARY.BOARD_HEIGHT = 8
    LIBRARY.BOARD_WIDTH = 8
    LIBRARY.LIVES = 3
    LIBRARY.APPLE_LIVES = 10
    LIBRARY.SCORE = 0
    LIBRARY.APPLE = 'H7'
    LIBRARY.SNAKE = ['B2', 'B3', 'B4', 'C4', 'D4']
    LIBRARY.ORIENTATION = 4

BOARD_HEADER_PATTERN = re.compile(r'^Lives: (-?\d+) - Apple Lives: (-?\d+) - Score: (-?\d+)')
class TestBoard(TestCaseBase):
  def setUp(self):
    super().setUp()
    self.set_default_attributes()

  def test_border(self):
    for width in [8]:
      for height in [8]:
        with self.subTest(BOARD_HEIGHT = height, BOARD_WIDTH = width):
          LIBRARY.BOARD_WIDTH = width
          LIBRARY.BOARD_HEIGHT = height
          with captured_io() as (_, out, _):
            LIBRARY._1_print_game_board()
            output = out.getvalue().split('\n')
          self.assertEqual(height + 5, len(output), "Incorrect number of lines in output")
          self.assertEqual("-" * (width * 3 + 4), output[1], "Incorrect number of '-' above board.")
          for row in range(height):
            rl = rowletter(row)
            self.assertEqual(f'{rl} | ', output[row + 2][:4], f"Row {rl} starts incorrectly")
            self.assertEqual(f' |', output[row + 2][-2:], f"Row {rl} ends incorrectly")
          self.assertEqual("-" * (width * 3 + 4), output[-3], "Incorrect number of '-' below board.")
          self.evaluation(1, 7)

  def test_header_simple(self):
    with captured_io() as (_, out, _):
      LIBRARY._1_print_game_board()
    self.assertEqual(f'Lives: 3 - Apple Lives: 10 - Score: 0', out.getvalue().split('\n')[0])
    self.evaluation(1, 1)

  def test_snake_head(self):
    for orientation_number, orientation in {
      2: ("up", '∧'),
      3: ("left", '<'),
      4: ("down", 'v'),
      5: ("right", '>')
    }.items():
      with self.subTest(orientation=orientation[0]):
        with captured_io() as (_, out, _):
          LIBRARY.APPLE = 'B1'
          LIBRARY.SNAKE = ['A0']
          LIBRARY.ORIENTATION = orientation_number
          LIBRARY._1_print_game_board()

        head = out.getvalue().split('\n')[2][4]
        self.assertEqual(orientation[1], head, f"The snake head should be '{orientation[1]}' when looking {orientation[0]}. Board: \n" + out.getvalue())
        self.evaluation(3, 1.5/4)

  def test_snake_tail_line(self):
    LIBRARY.APPLE = 'B1'
    upper_bound = 5
    lower_bound = 2
    evaluation_score_per_subtest = 1/16
    for length in range(lower_bound, upper_bound + 1):
      with self.subTest("straight up", snake_length=length):
        with captured_io() as (_, out, _):
          LIBRARY.SNAKE = [rowletter(i) + '0' for i in range(length - 1, -1, -1)]
          LIBRARY.ORIENTATION = 2
          LIBRARY._1_print_game_board()

        output = out.getvalue().split('\n')
        for row in range(length - 1):
          self.assertEqual('+', output[3 + row][4], f"Cell {rowletter(row)}0 is part of the snake tail, but not '+' on the following board:\n" + out.getvalue())
        self.evaluation(3, evaluation_score_per_subtest)

      with self.subTest("straight down", snake_length=length):
        with captured_io() as (_, out, _):
          LIBRARY.SNAKE = [rowletter(i) + '0' for i in range(length)]
          LIBRARY.ORIENTATION = 4
          LIBRARY._1_print_game_board()

        output = out.getvalue().split('\n')
        for row in range(length - 1):
          self.assertEqual('+', output[2 + row][4], f"Cell {rowletter(row)}0 is part of the snake tail, but not '+' on the following board:\n" + out.getvalue())
        self.evaluation(3, evaluation_score_per_subtest)

      with self.subTest("straight left", snake_length=length):
        with captured_io() as (_, out, _):
          LIBRARY.SNAKE = ['A' + str(i) for i in range(length - 1, -1, -1)]
          LIBRARY.ORIENTATION = 3
          LIBRARY._1_print_game_board()

        output = out.getvalue().split('\n')
        for col in range(length - 1):
          self.assertEqual('+', output[2][7 + 3 * col], f"Cell A{col} is part of the snake tail, but not '+' on the following board:\n" + out.getvalue())
        self.evaluation(3, evaluation_score_per_subtest)

      with self.subTest("straight right", snake_length=length):
        with captured_io() as (_, out, _):
          LIBRARY.SNAKE = ['A' + str(i) for i in range(length)]
          LIBRARY.ORIENTATION = 5
          LIBRARY._1_print_game_board()

        output = out.getvalue().split('\n')
        for col in range(length - 1):
          self.assertEqual('+', output[2][4 + 3 * col], f"Cell A{col} is part of the snake tail, but not '+' on the following board:\n" + out.getvalue())
        self.evaluation(3, evaluation_score_per_subtest)

class TestGame(TestCaseBase):
  def setUp(self):
    super().setUp()
    self.set_default_attributes()

  def test_exit(self):
    with captured_io('q\n') as (stdin, stdout, _):
      try:
        LIBRARY.main()
      except SystemExit:
        pass
      except:
        self.fail("'q' should quit the game. Output:\n" + stdout.getvalue())
    self.evaluation(4, 2)

  def test_apple_respawn(self):
    for run in range(300):
      with self.subTest():
        self.set_default_attributes()
        LIBRARY.APPLE_LIVES = 2
        lives = LIBRARY.LIVES
        apple = LIBRARY.APPLE
        with captured_io('\n\nq\n') as (_, out, _):
          try:
            LIBRARY.main()
          except:
            pass
        self.assertEqual(lives - 1, LIBRARY.LIVES, "LIVES should have been decremented. Output:\n" + out.getvalue())
        self.assertNotEqual(apple, LIBRARY.APPLE, "The apple should have spawned at a new location. Output:\n" + out.getvalue())
        self.evaluation(6, 11/300)

  def test_game_over(self):
    LIBRARY.APPLE_LIVES = 2
    LIBRARY.LIVES = 1
    with captured_io('\n\ntest_snake.py\n') as (_, out, _):
      try:
        LIBRARY.main()
      except EOFError:
        self.fail(out.getvalue())
    self.assertEqual(2, out.getvalue().count('input [w a s d]'), f"Don\'t prompt for a movement direction after LIVES equals 0. Output:\n" + out.getvalue())
    self.evaluation(6, 5)

  def test_score(self):
    score = LIBRARY.SCORE
    for i in range(1, 5):
      with captured_io('\n') as (_, out, _):
        try:
          LIBRARY.main()
        except EOFError:
          pass
      self.assertEqual(score + i, LIBRARY.SCORE, f"The score should have been {score + i}. Output:\n" + out.getvalue())
      self.evaluation(4, 3/4)

LEADERBOARD_ITEM_PATTERN = re.compile(r'.* - Score: (\d+) - Lives: (\d+) - Snake length: (\d+)')
HISTORY_FILE = 'history.txt'
class TestLeaderboard(TestCaseBase):
  def setUp(self):
    super().setUp()
    self.set_default_attributes()
    with open(HISTORY_FILE, 'r') as file:
      self.original_history = list(file)
    self.clear_history_file()
    with open(HISTORY_FILE, 'r') as file:
      self.assertEqual([], list(file), "The history file should have been cleared.")

  def clear_history_file(self):
    with open(HISTORY_FILE, 'w') as file:
      file.seek(0)
      file.truncate()

  def set_default_attributes(self):
    super().set_default_attributes()
    LIBRARY.SNAKE = ['A3', 'A2', 'A1', 'A0']
    LIBRARY.ORIENTATION = 3
    LIBRARY.LIVES = 1

  def tearDown(self):
    super().tearDown()
    with open(HISTORY_FILE, 'w') as file:
      file.seek(0)
      file.writelines(self.original_history)

def rowletter(index):
  return chr(ord("A") + index)


################################################################################
# Students are not expected to read or understand the rest of the code. (You don't need to understand most code above either.)
################################################################################

INITIAL_LIBRARY_ATTRIBUTES = {} # If you are a student, don't worry about this variable

def reinitialize_library_attributes():
  for key, value in INITIAL_LIBRARY_ATTRIBUTES.items():
    setattr(LIBRARY, key, value)

@contextmanager
def captured_io(initial_in=None) -> Tuple[io.StringIO, io.StringIO, io.StringIO]:
  new_in, new_out, new_err = io.StringIO(initial_in), io.StringIO(), io.StringIO()
  old_in, old_out, old_err = sys.stdin, sys.stdout, sys.stderr
  try:
    sys.stdin, sys.stdout, sys.stderr = new_in, new_out, new_err
    yield sys.stdin, sys.stdout, sys.stderr
  finally:
    sys.stdin, sys.stdout, sys.stderr = old_in, old_out, old_err

def test(lib, filename: Path):
  global LIBRARY
  LIBRARY = lib
  global INITIAL_LIBRARY_ATTRIBUTES
  INITIAL_LIBRARY_ATTRIBUTES = copy_attributes(lib)
  unittest.main(argv=['first-arg-is-ignored'], verbosity=2, exit=False) # https://medium.com/@vladbezden/using-python-unittest-in-ipython-or-jupyter-732448724e31
  LIBRARY = None
  global EVALUATION
  print(f"Completed testing {filename} - evaluation: {', '.join(f'{k}: {v}/{m}' for (k, v), m in zip(EVALUATION.items(), [8, 0, 2.5, 5, 0, 16, 0]))} = {sum(EVALUATION.values())}/31.5")

def copy_attributes(module):
  attributes = {}
  for key in dir(module):
    if key.startswith('__'):
      continue
    attr = getattr(module, key)
    if type(attr) not in [FunctionType, ModuleType]:
      attributes[key] = attr
  return attributes

################################################################################
# The testsuite's internals are below.
# You shouldn't need to edit the rest of the file. (Please submit a pull request
#   to https://github.com/SimonLammer/testpythonscript otherwise)
################################################################################

LOAD_TIMEOUT = None       # cli arg; Terminate the subprocess if importing the library takes longer
COMPLETION_TIMEOUT = None # cli arg; Terminate the subprocess if takes longer to finish gracefully

WAIT_DELAY = timedelta(milliseconds=50)
OUTPUT_REPORT_DELAY = timedelta(milliseconds=5)
TERMINATION_DELAY = OUTPUT_REPORT_DELAY + timedelta(milliseconds=2)

def main():
  args = parse_args()
  scripts: List[Path] = args.script
  max_processes = args.processes
  global LOAD_TIMEOUT
  LOAD_TIMEOUT = args.load_timeout
  global COMPLETION_TIMEOUT
  COMPLETION_TIMEOUT = args.completion_timeout

  queue = multiprocessing.Queue() # for communication with subprocesses

  index_pid = {} # key: index, value: pid

  outputs: Dict[int, str] = {} # key: pid, value: stdout & stderr for each script
  exitcodes: Dict[int, int] = {} # key: pid, value: exitcode

  timeouts: List[Tuple[int, datetime]] = [] # [(pid, datetime), (...), ...]

  ready: List[multiprocessing.Process] = list(map(lambda x: multiprocessing.Process(target=runtest, args=(*x, queue)), enumerate(scripts)))
  running: List[multiprocessing.Process] = []

  while len(ready) > 0 or len(running) > 0:
    for i, p in enumerate(running):
      if not p.is_alive():
        print(f"process {p.pid} finished with exit code {p.exitcode}")
        exitcodes[p.pid] = p.exitcode
        p.join()
        del running[i]

    while 0 < len(ready) and len(running) < max_processes:
      process = ready.pop()
      running.append(process)
      process.start()

    # print("timeouts", timeouts)
    while queue.empty() and (len(timeouts) == 0 or timeouts[0][1] > datetime.now()) and (len(running) > 0 and running[0].is_alive()):
      time.sleep(WAIT_DELAY.total_seconds())

    while not queue.empty():
      pid, item = queue.get_nowait()
      if pid not in index_pid.values(): # item is the process index
        print(f"process {pid} is processing {scripts[item]}")
        index_pid[item] = pid
      elif isinstance(item, str): # process sent its output
        # print(f"process {pid} sent its output")
        outputs[pid] = item
      elif isinstance(item, datetime): # process set timeout
        # print(f"setting timeout of pid {pid} to {item}")
        for i, (p, t) in enumerate(timeouts):
          if p == pid:
            timeouts[i] = (pid, item)
            break
        else:
          timeouts.append((pid, item))
      elif item is None: # process canceled timeout
        for i, (p, t) in enumerate(timeouts):
          if pid == p:
            # print(f"canceling timout of pid {pid} ({t})")
            del timeouts[i]
      else:
        raise RuntimeWarning("Invalid item in queue", item)

    timeouts.sort(key=lambda x: x[1])
    time.sleep(TERMINATION_DELAY.total_seconds()) # give timeouted processes enough time to report their output
    for pid, t in timeouts:
      if t > datetime.now():
        break
      for i, p in enumerate(running):
        if pid == p.pid and p.is_alive():
          print(f"process {pid} exceeded its timeout {t} by {datetime.now() - t}, terminating")
          p.terminate()

  for i in range(len(scripts)):
    pid = index_pid[i]
    print('+' * 80)
    print(f"Output of {scripts[i]} test (exitcode {exitcodes[pid]}):")
    output = outputs[pid]
    if output is not None:
      print(''.join(output))

def parse_args():
  def filetype(filepath):
    path = Path(filepath)
    if not path.is_file():
      raise argparse.ArgumentTypeError(f"{filepath} does not exist!")
    return path

  parser = argparse.ArgumentParser(description=TESTSUITE_DESCRIPTION, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-p', '--processes',
    help="Maximum number of processes to use in parallel.",
    type=int,
    default=os.cpu_count())
  parser.add_argument('-l', '--load-timeout',
    help="A test will be terminated if loading the script takes longer than this many milliseconds.",
    type=lambda x: timedelta(milliseconds=float(x)),
    default="1000")
  parser.add_argument('-c', '--completion-timeout',
    help="A test will be terminated if it takes longer than this many milliseconds.",
    type=lambda x: timedelta(milliseconds=float(x)),
    default="60000")
  parser.add_argument('script',
    help="The script file to test. MUST end in '.py' (without quotes)!",
    nargs='+',
    type=filetype)
  return parser.parse_args()

def runtest(index: int, scriptpath: Path, queue: multiprocessing.Queue):
  output = io.StringIO()
  sys.stdout = output
  sys.stderr = output
  try:
    pid = multiprocessing.current_process().pid
    queue.put((pid, index))

    def reportoutput():
      while True:
        queue.put((pid, output.getvalue()))
        time.sleep(OUTPUT_REPORT_DELAY.total_seconds())
    t = threading.Thread(target=reportoutput, daemon=True)
    t.start()

    def testwrapper(lib, _):
      queue.put((pid, datetime.now() + timedelta(seconds=15)))
      test(lib, scriptpath)
    queue.put((pid, datetime.now() + timedelta(seconds=1)))
    testscript(scriptpath, testwrapper)
  except:
    traceback.print_exception(*sys.exc_info())
  queue.put((pid, output.getvalue()))

# https://stackoverflow.com/a/52328080/2808520
def testscript(scriptpath: Path, test: Callable):
  '''
  Runs some tests with the given script.
  '''
  assert(scriptpath.name.endswith('.py')) # thwart ModuleNotFoundError 
  sys.path.insert(0, str(scriptpath.parent.absolute()))
  imported_library = import_module(scriptpath.name[:-3])
  test(imported_library, scriptpath)
  del imported_library
  sys.path.pop(0)

if __name__ == '__main__':
  main()
