"""This module contains all init command related functions."""

from .utils import mkdir_if_not_exists, write_file


def init(GPG_FILE, PASSWORD_FOLDER, gpg_id, verbose=False):
    """Initialize new password storage."""
    mkdir_if_not_exists(PASSWORD_FOLDER, verbose)
    gpg_file_path = PASSWORD_FOLDER + GPG_FILE
    write_file(gpg_file_path, gpg_id, verbose)
