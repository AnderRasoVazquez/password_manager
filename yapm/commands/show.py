"""This module contains all show command related functions."""

from subprocess import Popen, PIPE
from os.path import isfile

from .utils import parse_path, build_absolute_path, pass_to_clipboard, print_and_erase_passw


def decrypt_password(encrypted_passw):
    """Decrypts a string using GPG."""
    # https://docs.python.org/3/library/subprocess.html
    p1 = Popen(["echo", encrypted_passw], stdout=PIPE)
    p2 = Popen(["gpg", "--decrypt"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]  # in bytes, we need to decode it
    return output.decode()  # default is "utf-8"


def show(password_folder, path, clipboard, the_time):
    """Decrypt password and show it."""
    # https: // docs.python.org / 3 / library / functions.html  # print
    path = build_absolute_path(password_folder, parse_path(path))

    if isfile(path):
        with open(path) as pass_file_content:
            encrypted_passw = pass_file_content.read().strip()
        passw = decrypt_password(encrypted_passw).strip()

        if clipboard:
            pass_to_clipboard(passw)
        else:
            print_and_erase_passw(passw, the_time)

    else:
        print("{} is not a stored password".format(path))


