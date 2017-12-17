"""This module contains all rm command related functions."""
from os.path import isfile, isdir
from os import remove
from shutil import rmtree
import sys

from .utils import parse_path


def remove_file(path, verbose_mode=False):
    """Deletes a file."""
    if isfile(path):
        remove(path)
        if verbose_mode:
            print("Deleted {}".format(path))
    else:
        print("{} is not a file".format(path))


def remove_dir(path, verbose_mode=False):
    """Delete directory or directory tree."""
    rmtree(path)
    if verbose_mode:
        print("Deleted {}".format(path))


def confirm(path):
    """Confirm an action."""
    result = input("Confirm deletion of {} with [y]: ".format(path))
    return True if result in ['y', 'Y'] else False


def rm(password_folder, path, recursive=False, verbose=False, ext=".gpg"):
    """Remove password from the storage."""
    path = password_folder + parse_path(path)
    if not recursive:
        path += ext
    if isfile(path):
        if confirm(path):
            remove_file(path, verbose)
        else:
            sys.exit("Deletion aborted.")
    elif isdir(path):
        if confirm(path):
            remove_dir(path, verbose)
        else:
            sys.exit("Deletion aborted.")
    else:
        sys.exit("Path doesn't exist.")

