"""This module manages a password storage."""
import argparse

__version__ = 0.1


# separar init, add y rm en archivos diferentes
def init(args):
    """Initialize new password storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)


def add(args):
    """Add new password to the storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)


def rm(args):
    """Remove password from the storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose flag')
    parser.add_argument('-V', '--version',
                        action='store_true',
                        help='show version')

    parser_init = subparsers.add_parser('init', help='initialize new password storage')
    parser_init.add_argument('gpg_id',
                             help='password id')

    # TODO implementar argumentos para: longitud, mayúsculas y minúsculas, números, caracteres extraños
    parser_add = subparsers.add_parser('add', help='adds a new password')
    parser_add.add_argument('password_dest',
                            help='password destination')
    # TODO implementar argumentos para 2 opciones: que genere el pass o poder escribir tu la contraseña que ya tengas
    parser_add.add_argument('-l', '--length',
                            dest='pass_len',
                            type=int,
                            default=21,
                            help='password length')

    parser_remove = subparsers.add_parser('rm', help='removes a stored password')
    parser_remove.add_argument('password_dest',
                               help='password destination')

    args = parser.parse_args()

    if args.version:
        print("Version: {}".format(__version__))

    if args.command == 'init':
        init(args)
    elif args.command == 'add':
        add(args)
    elif args.command == 'rm':
        rm(args)


if __name__ == '__main__':
    main()
