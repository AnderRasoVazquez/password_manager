"""This module contains all cotroller related functions."""
import sys
from os.path import expanduser, isfile
from shutil import which

from .commands.add import add
from .commands.init import init
from .commands.rm import rm
from .commands.show import show

__version__ = '1.0'
GPG_ID = None
PASSWORD_FOLDER = expanduser("~/.password-store/")
GPG_FILE = ".gpg-id"
MAX_TIME = 30


def check_config():
    """Initial checks before running the program."""
    if not which("gpg"):
        sys.exit("GPG binary not found. ¿Is it installed?")
    gpg_file_path = PASSWORD_FOLDER + GPG_FILE
    if not isfile(gpg_file_path):
        sys.exit("WARNING: password store not configured, please execute:\nyapm init")
    with open(gpg_file_path) as gpg_file_content:
        global GPG_ID
        GPG_ID = gpg_file_content.read().strip()


def build_pass_conf(args):
    """Build a binary that represents a password configuration."""
    result = 0b000
    if args.symbols:
        result = result | 0b100
    if args.uppercase:
        result = result | 0b010
    if args.numbers:
        result = result | 0b001
    return result


def control(args):
    """Execute command based on args."""
    if args.version:
        print("Version: {}".format(__version__))

    if args.command == 'init':
        init(GPG_FILE, PASSWORD_FOLDER, args.gpg_id, args.verbose)
    elif args.command == 'add':
        check_config()
        pass_conf = build_pass_conf(args)
        add(args.insert, args.length, pass_conf, args.password_dest,
            args.clipboard, PASSWORD_FOLDER, GPG_ID, args.verbose)
    elif args.command == 'rm':
        check_config()
        rm(PASSWORD_FOLDER, args.path, args.verbose)
    elif args.command == 'show':
        if args.time > MAX_TIME:
            args.time = MAX_TIME
        check_config()
        show(PASSWORD_FOLDER, args.path, args.clipboard, args.time)
