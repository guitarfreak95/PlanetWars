#!usr/bin/env python
"""
@author Arthur de Fluiter
@author Jur van den Berg
@version 3.14

This program is meant to make running the bots a whole lot easier.

For all the options run
python play.py -h
or
python play.py --help
"""
from argparse import ArgumentParser
from subprocess import Popen, PIPE
import sys
import os.path

# these paths are crawled for programs by default, you can add paths here (more permanent)
# or run -e <path> as described in help
default_paths = ["src/python", "out/", "out/artifacts"]


def execution_path(program, paths):
    """
    Given a vague program description, tries to figure out what the hell it's supposed to point to and how to
    execute it.

    example input with expected output:
    "RandomBot.py"             -> "python src/RandomBot.py"
    "RandomBot.jar"            -> "java -jar out/artifacts/RandomBot.jar"
    "RandomBot.java"           -> "java -cp out/classes RandomBot" OR
                                  "java -cp out RandomBot"         (Depending on where it finds it)
    "java out/RandomBot"       -> "java out/RandomBot"
    "shadyCExecutable.exe"     -> Exception
    "java"                     -> Exception

    @type program : string
    @type paths: list[string]
    """
    command = program.strip().split()  # remove trailing whitespace and split into chunks

    # an argument like 'python src/RandomBot.jar'
    if len(command) > 1 and (command[0][:6] == "python" or command[0] == "java"):
        # assume the person knows what they're doing
        return program

    # I assume the last var will be the variable it is trying to execute
    file_name = command[-1]

    if file_name.endswith(".py"):
        exec_path = resolve_path(file_name, paths)
        return "%s %s" % (options.python_exec, exec_path)
    elif file_name.endswith(".class"):
        # remove the ".class" from the base name
        base_name = file_name[:-6]

        # e.g. resolve path for file.class
        try:
            exec_path = resolve_path(file_name, paths, include_file=False)
        except:
            print("Make sure you didn't make a typo and compiled your java first (see gradle)")
            raise

        return "java -cp %s %s" % (exec_path, base_name)
    elif file_name.endswith(".java"):
        # remove the ".java"
        base_name = file_name[:-5]

        # e.g. resolve path for file.class (instead of .java)
        try:
            exec_path = resolve_path("%s.class" % base_name, paths, include_file=False)
        except:
            print("Make sure you didn't make a typo and compiled your java first (see gradle)")
            raise

        return "java -cp %s %s" % (exec_path, base_name)
    elif file_name.endswith(".jar"):
        exec_path = resolve_path(file_name, paths)
        return "java -jar %s" % exec_path
    else:
        raise LookupError("Unsupported language or incomplete name '%s'\nPlease find one of the TA's" % program)


def wizard():
    """The python snake wisperer, yer a wizzerd larry."""
    # check for python
    if sys.version_info[0] != 2:
        print("You're running python3, please use python2")
        exit(-1)

    # check for java
    if not in_path("java"):
        print("You need a version of JRE available (installed, and linked to in PATH)")
        exit(-1)
    if not in_path("javac"):
        print("CS students: You wont be able to compile java (JDK not in path)")

    # By Merlins beard, everything works!


def resolve_path(file_name, paths, include_file=True):
    """Checks the currently selected paths for whether it can find the file"""
    for path in paths:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            if include_file:
                return file_path
            else:
                return path
    err_message = """Could not resolve '%s'\nLooked in paths: %s\nPlease talk to one of the TA's""" % (file_name, paths)
    raise LookupError(err_message)


def in_path(program):
    """Checks whether a program, like java, is in path (automatically checks for program and program.exe)"""
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path.strip('"'), program)
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
        exe_file = os.path.join(path.strip('"'), program + ".exe")
        if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
            return True
    return False


parser = ArgumentParser()

# map option (relative paths)
parser.add_argument("-m", "--map", dest="map",
                    help="the map to play on",
                    default="simplemaps/3planets/map1.txt")

# player 1 & 2, I want only the bare minimum to be mentioned here (EmptyBot.py for instance)
parser.add_argument("-1", "--p1", "--player1", dest="player1",
                    help="the program to run for player 1 (default: RandomBot.py)",
                    default="RandomBot.py")
parser.add_argument("-2", "--p2", "--player2", dest="player2",
                    help="the program to run for player 2 (default: RandomBot.py)",
                    default="RandomBot.py")

# parallel mode (see the playgame engine)
parser.add_argument("-p", "--parrallel", dest="parallel",
                    help="different game mode  (default: serial)",
                    action="store_true")

parser.add_argument("-t", "--max-time", dest="max_time",
                    help="maximum amount of time allowed per turn in msec (default: 1000)",
                    type=int, default=1000)

parser.add_argument("-x", "--max-turns", dest="max_turns",
                    help="maximum amount of turns in a game  (default: 100)",
                    type=int, default=100)

# Visualisation (with the visualisation tools, if this is easier, we could put the code right here)
parser.add_argument("-s", "--show", dest="show",
                    help="whether the game should be visualised  (default: False)",
                    action="store_true")

parser.add_argument("-v", "--verbose", dest="verbose",
                    help="whether to output extra logging information  (default: False)",
                    action="store_true")

parser.add_argument("-e", "--exec-path", dest="exec_path",
                    help="This resolves the path to the executable, if you place the executable in a different place, "
                         "add the string to this list (default included: 'src/python', 'out/', 'out/artifacts')",
                    action="append", default=[])
parser.add_argument("-y", "--python", dest="python_exec",
                    help="This defines the python executable used. Should you get issues with python3/python2 "
                    "mismatches, it might be a good idea to set this to 'python2'. (default 'python')",
                    default="python")

options = parser.parse_args()
wizard()

game_map = options.map
mode = 'parallel' if options.parallel else 'serial'
max_turns = str(options.max_turns)
max_turn_time = str(options.max_time)

player1, player2 = "", ""
paths = options.exec_path + default_paths

try:
    player1 = execution_path(options.player1, paths)
    player2 = execution_path(options.player2, paths)
except LookupError as inst:
    print("Error: %s" % inst)
    exit(-1)

command = ['java', '-jar', 'tools/PlayGame.jar', game_map, player1, player2, mode, max_turns, max_turn_time]

if options.verbose:
    print("Play.py configurations")
    print("---------------------")
    print("Map location: '%s'" % game_map)
    print("Player 1: '%s'" % player1)
    print("Player 2: '%s'" % player2)
    print("Game mode: '%s'" % mode)
    print("Maximum amount of turns: %s" % max_turns)
    print("Time per turn: %s" % max_turn_time)
    print("Visualization: %s" % str(options.show))
    print("---------------------\n")

engine_process = Popen(command, stdout=PIPE, stderr=PIPE)
engine_out, engine_err = engine_process.communicate()  # blocks

if options.verbose:
    print("For a full overview of the game state at all times, please check 'log.txt'")
    print("Errors/Messages picked up by engine")
    print("----------------------------")
    print(engine_err)
else:
    # find out who won and display
    import re

    m = re.findall("(Draw!\s*$|Player \d Wins!\s*$)", engine_err)
    if len(m) is 0:
        print("Something went wrong, engine output dump:")
        print("-------------------------")
        print(engine_err)
        exit()
    else:
        sys.stdout.write(m[0])

# visualiser
if options.show:
    visualizer = [options.python_exec, "tools/visualizer/visualize.py"]
    visualizer_process = Popen(visualizer, stdin=PIPE)
    visualizer_process.communicate(input=engine_out)
    print(engine_out)
