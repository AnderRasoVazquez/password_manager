"""This module manages a password storage."""
import argparse
import sys
import string
from random import randint
from getpass import getpass
from os import makedirs
from os.path import isfile, isdir, expanduser
from shutil import which

__version__ = 0.1


GPG_ID = None
PASSWORD_FOLDER = expanduser("~/.password-store/")
GPG_FILE = ".gpg-id"

#################################################################
# EJEMPLO DE USO
#
# `yapm`
# sin argumentos por defecto hace `yapm -h`, muestra la ayuda
#
# INIT
# `yapm init 7D9D16BE`
# crea la carpeta del programa "$HOME/.password-store" y crea un archivo
# "$HOME/.password-store/.gpg.id" donde guarda el id de GPG, el que ves es el mío.
# He pensado en esos nombres para que sea compatible con otros password managers
# que también usan gpg (hay hasta para Android).
# De esta manera se puede sincronizar con otros pc o el movil
#
# ADD
# `yapm add prueba`
# crea un archivo "$HOME/.password-store/prueba.gpg" con una clave random de solo
# minusculas y de 21 caracteres por defecto (21 he sacado de otro password manager)
# `yapm add prueba -sun -l 15`
# -s -> symbols
# -u -> uppercase
# -n -> numbers
# -l 15-> longitud 15
# `yapm add prueba -i`
# te sale un input para que pongas tu el password que ya tengas
#
# RM
# `yamp rm prueba`
# elimina el password, sin mas
#
# SHOW
# `yapm show prueba`
# Descifra "$HOME/.password-store/prueba.gpg" y lo muestra por la terminal
# GPG te pedira el password de tu clave para hacerlo
# `yapm show -c prueba`
# Descifra el password y lo copia a tu clipboard
# Estaria bien que lo borrase des clipboard despues de 45 segundos por ejemplo,
# eso seguro que le mola a Mikel
#
##################################################################


def check():
    """Initial checks before running the program."""
    if not which("gpg"):
        sys.exit("GPG binary not found. ¿Is it installed?")
    gpg_file_path = expanduser(PASSWORD_FOLDER + GPG_FILE)
    if not isfile(gpg_file_path):
        sys.exit("WARNING: password store not configured, please execute:\nyapm init")
    with open(gpg_file_path) as gpg_file_content:
        global GPG_ID
        GPG_ID = gpg_file_content.read().strip()


# puede ser buena idea separar init, add y rm en archivos diferentes
def init(args):
    """Initialize new password storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
        print()
    if not isdir(PASSWORD_FOLDER):
        # crear si no existe la carpeta "$HOME/.password-store/"
        makedirs(PASSWORD_FOLDER, exist_ok=True)
        if args.verbose:
            print("Created directory " + PASSWORD_FOLDER)
    # coger args.gpg_id y meterlo en "$HOME/.password-store/.gpg-id"
    gpg_file_path = PASSWORD_FOLDER + GPG_FILE
    f = open(gpg_file_path, 'w')
    f.write(args.gpg_id)
    f.close()
    if args.verbose:
        print("Created file " + gpg_file_path)


def build_pass(args):
    """Build a password based on args."""
    passw = string.ascii_lowercase
    if args.uppercase:
        passw += string.ascii_uppercase
    if args.symbols:
        passw += string.punctuation
    if args.numbers:
        passw += string.digits

    return "".join([passw[randint(0, len(passw) - 1)] for x in range(args.length)])


def add(args):
    """Add new password to the storage."""
    check()
    if args.insert:
        passw = getpass("Insert password: ")
    else:
        passw = build_pass(args)
    print(passw)
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


def show(args):
    """Decrypt password and show it."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
    # descifraria el password dado
        # si tiene la opcion -c podria copiarlo al clipboard
        # si no, lo mostraria por la terminal


def main():
    """Main function."""
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

    # parser for rm command
    parser_remove = subparsers.add_parser('rm', help='removes a stored password')
    parser_remove.add_argument('password_dest',
                               help='password destination')

    # parser for init command
    parser_show = subparsers.add_parser('show', help='shows password')
    parser_show.add_argument('password_dest',
                             help='password destination')
    parser_show.add_argument('-c', '--clipboard',
                             action='store_true',
                             help='copy password to clipboard instead of printing it')

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
    elif args.command == 'show':
        show(args)


if __name__ == '__main__':
    main()
