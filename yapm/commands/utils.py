"""Common functions for commands."""

from os import makedirs
from os.path import isdir
from subprocess import Popen, PIPE
from time import sleep


def build_absolute_path(password_folder, path, ext=".gpg"):
    """Builds absolute '.gpg' file path."""
    return password_folder + path + ext


def pass_to_clipboard(text):
    """Pass text to clipboard."""
    sleep(0.5)  # wait for all printed text of GPG
    p = Popen(['xclip', '-selection', 'c'], stdin=PIPE)
    print("Password copied to clipboard, press [Control-C] to erase the clipboard and exit...")
    p.communicate(input=text.encode('utf-8'))


def parse_path(path):
    """Strip starting or ending '/'."""
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    return path


def write_file(file_path, file_content, verbose_mode=False, mode='w'):
    """Write content to a file."""
    with open(file_path, mode) as file:
        file.write(file_content)
        if verbose_mode:
            print("{} written.".format(file_path))


def mkdir_if_not_exists(folder, verbose_mode=False):
    """Creates a folder if not exists."""
    if not isdir(folder):
        makedirs(folder)
        if verbose_mode:
            print("Created {}".format(folder))


def print_and_erase_passw(passw, delete_time=10):
    """Print password and erase it."""
    for t in reversed(range(delete_time + 1)):
        text = "You have {} second(s) to copy the password: {}".format(str(t).zfill(2), passw)
        print(text, end='\r')
        sleep(1)
        print(" " * len(text), end='\r')  # erase output
    print("Time has expired")

