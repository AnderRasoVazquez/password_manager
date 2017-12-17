"""This module contains all add command related functions."""

import string
from random import randint
from getpass import getpass
from subprocess import Popen, PIPE
from shutil import which

from .utils import parse_path, mkdir_if_not_exists, write_file,\
                   build_absolute_path, pass_to_clipboard, print_and_erase_passw


def convert_num_to_bin(num):
    """Convert a number to a binary without initial '0b'."""
    return bin(num)[2:].zfill(3)


def build_pass(pass_len, pass_conf, verbose):
    """Build a password."""
    pass_conf = convert_num_to_bin(pass_conf)
    passw = string.ascii_lowercase
    if int(pass_conf[0]):
        passw += string.punctuation
    if int(pass_conf[1]):
        passw += string.ascii_uppercase
    if int(pass_conf[2]):
        passw += string.digits

    if verbose:
        print("Building password with options: length={}, conf={}".format(pass_len, pass_conf))

    return "".join([passw[randint(0, len(passw) - 1)] for _ in range(pass_len)])


def encrypt_password(passw, GPG_ID):
    """Encrypts a string using GPG."""
    # https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline
    p1 = Popen(["echo", passw], stdout=PIPE)
    p2 = Popen(["gpg", "--encrypt", "--armor", "-r", GPG_ID], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]  # in bytes, we need to decode it
    return output.decode()  # default is "utf-8"


def get_folder(path):
    """Return folder name."""
    path_args = path.split('/')
    return "/".join(path_args[0:-1])


def get_passw(manual, pass_len, pass_conf, verbose):
    """Returns a manual typed or generated password."""
    if manual:
        passw = getpass("Insert password: ")
    else:
        passw = build_pass(pass_len, pass_conf, verbose)
    return passw


def handle_passw_output(manual, clipboard, passw):
    """Decide how will know the user his password."""
    if not manual:
        if clipboard:
            if not which("xclip"):
                print("xclip program is needed for copying to clipboard.")
                print_and_erase_passw(passw)
            else:
                pass_to_clipboard(passw)
        else:
            print_and_erase_passw(passw)


def add(manual, pass_len, pass_conf, password_dest, clipboard, PASSWORD_FOLDER, GPG_ID, verbose=False):
    """Add new password to the storage."""
    passw = get_passw(manual, pass_len, pass_conf, verbose)
    encrypted_passw = encrypt_password(passw, GPG_ID)
    path = parse_path(password_dest)

    if '/' in path:
        folder = get_folder(path)
        mkdir_if_not_exists(PASSWORD_FOLDER + folder, verbose)

    absolute_file_path = build_absolute_path(PASSWORD_FOLDER, path)
    write_file(absolute_file_path, encrypted_passw, verbose)

    handle_passw_output(manual, clipboard, passw)
