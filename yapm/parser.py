"""Parsing related functions."""
import argparse


def build_parser():
    """Build parser."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command')

    # main parser
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose flag')
    parser.add_argument('-V', '--version',
                        action='store_true',
                        help='show version')

    # parser for init command
    parser_init = subparsers.add_parser('init', help='initialize new password storage')
    parser_init.add_argument('gpg_id',
                             help='password id')

    # parser for add command
    parser_add = subparsers.add_parser('add', help='adds a new password')
    parser_add.add_argument('password_dest',
                            help='password destination')
    parser_add.add_argument('-i', '--insert',
                            action='store_true',
                            help='insert custom password')
    parser_add.add_argument('-l', '--length',
                            type=int,
                            default=21,
                            help='password length')
    parser_add.add_argument('-s', '--symbols',
                            action='store_true',
                            help='symbols enabled')
    parser_add.add_argument('-u', '--uppercase',
                            action='store_true',
                            help='uppercase characters enabled')
    parser_add.add_argument('-n', '--numbers',
                            action='store_true',
                            help='numbers enabled')
    parser_add.add_argument('-c', '--clipboard',
                            action='store_true',
                            help='copy to clipboard')

    # parser for rm command
    parser_remove = subparsers.add_parser('rm', help='removes a stored password')
    parser_remove.add_argument('path',
                               help='path to the password (or folder if -r is used)')
    parser_remove.add_argument('-r', '--recursive',
                               action='store_true',
                               help='remove folder')

    # parser for show command
    parser_show = subparsers.add_parser('show', help='shows password')
    parser_show.add_argument('path',
                             help='password destination')
    parser_show.add_argument('-c', '--clipboard',
                             action='store_true',
                             help='copy password to clipboard instead of printing it')
    parser_show.add_argument('-t', '--time',
                             type=int,
                             default=10,
                             help='time the password is shown on screen')

    return parser
