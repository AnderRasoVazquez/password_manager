"""This module manages a password storage."""
import argparse
import sys

__version__ = 0.1


GPG_ID = None


def check():
    """Initial checks before running the program."""
    # comprobar si tiene GPG instalado, si no avisar y salir con error
    # comprobar si existe la carpeta "$HOME/.password-store/" y que tenga el archivo '.gpg_id'
        # (he puesto esta carpeta para que sea compatible con otro gestor
        # que tambien usa GPG y con una aplicacion de Android llamada "password store")
    # si no los tiene decirle que haga un "yapm init"
    # si los tiene, cargar el id del archivo en la variable GPG_ID (por ejemplo '7D9D16BE')
    pass


# puede ser buena idea separar init, add y rm en archivos diferentes
def init(args):
    """Initialize new password storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
    # crear si no existe la carpeta "$HOME/.password-store/"
    # coger args.gpg_id y meterlo en "$HOME/.password-store/.gpg-id" si no existe


def add(args):
    """Add new password to the storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
    # if args.insert: un prompt usando getpass (importarlo) para insertar el password de forma oculta, si no,
        # se veria en el historial de bash y eso es un buen penco
    # si no args.insert, mirar las demas opciones para crear un pass
        # coger el args.password_dest y mirar si tiene '/'
        # por ejemplo "email/google.gpg", crearia la carpeta email y dentro un archivo "google.gpg" con la contraseña
        # El archivo se cifra usando el "$HOME/.password-store/.gpg-id" que deberiamos tener ya en GPG_ID
        # si tiene mas de un '/' serian multiples carpetas

        # UN EJEMPLO DE IMPLEMENTACION para 'lol/lel/muehehe':
        # "lol/lel/muehehe".split('/') # ['lol', 'lel', 'muehehe']
        # argumentos = "lol/lel/muehehe".split('/')
        # argumentos[0:-1]  # desde el principio hasta el penultimo ['lol', 'lel']
        # "/".join(argumentos[0:-1])  # se pueden juntar de nuevo 'lol/lel' para hacer un 'mkdir -p'
        # nombre = argumentos[-1]  # el ultimo, 'muehehe'


def rm(args):
    """Remove password from the storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
    # podria borrar lo que le dijeras 'lol/lel/muehehe.gpg' borraria el archivo
        # 'lol/lel/' borrar la carpeta


def main():
    """Main function."""
    check()  # TODO sin implementar

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
                            dest='pass_len',
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

    # parser for rm command
    parser_remove = subparsers.add_parser('rm', help='removes a stored password')
    parser_remove.add_argument('password_dest',
                               help='password destination')

    # if no argument was provided append '-h'
    if not sys.argv[1:]:
        sys.argv.extend(['-h'])

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
