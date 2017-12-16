"""This module manages a password storage."""
import argparse
import sys
import string
from random import randint
from getpass import getpass
from os import makedirs, remove, listdir, rmdir
from os.path import isfile, isdir, expanduser
from shutil import which
from subprocess import Popen, PIPE
from time import sleep
import signal

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


def signal_handler(signal, frame):
    """KeyboardInterrupt signal handler."""
    sys.exit("\nExecution aborted!")


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


# puede ser buena idea separar init, add y rm en archivos diferentes
def init(args):
    """Initialize new password storage."""
    if args.verbose:
        print("{} command used".format(args.command))
        print(args)
        print()
    mkdir_if_not_exists(PASSWORD_FOLDER, args.verbose)
    gpg_file_path = PASSWORD_FOLDER + GPG_FILE
    write_file(gpg_file_path, args.gpg_id, args.verbose)


def build_pass(args):
    """Build a password based on args."""
    passw = string.ascii_lowercase
    if args.uppercase:
        passw += string.ascii_uppercase
    if args.symbols:
        passw += string.punctuation
    if args.numbers:
        passw += string.digits

    if args.verbose:
        print("Building password with options: {}".format(args))

    return "".join([passw[randint(0, len(passw) - 1)] for _ in range(args.length)])


def encrypt_password(passw):
    """Encrypts a string using GPG."""
    # https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline
    p1 = Popen(["echo", passw], stdout=PIPE)
    p2 = Popen(["gpg", "--encrypt", "--armor", "-r", GPG_ID], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]  # in bytes, we need to decode it
    return output.decode()  # default is "utf-8"


def decrypt_password(encrypted_passw):
    """Decrypts a string using GPG."""
    # https://docs.python.org/3/library/subprocess.html
    p1 = Popen(["echo", encrypted_passw], stdout=PIPE)
    p2 = Popen(["gpg", "--decrypt"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]  # in bytes, we need to decode it
    return output.decode()  # default is "utf-8"


def write_file(file_path, file_content, verbose_mode=False, mode='w'):
    """Write content to a file."""
    with open(file_path, mode) as file:
        file.write(file_content)
        if verbose_mode:
            print("{} written.".format(file_path))


def get_folder(path):
    """Return folder name."""
    path_args = path.split('/')
    return "/".join(path_args[0:-1])


def mkdir_if_not_exists(folder, verbose_mode=False):
    """Creates a folder if not exists."""
    if not isdir(folder):
        makedirs(folder)
        if verbose_mode:
            print("Created {}".format(folder))


def remove_file(path, verbose_mode=False):
    """Deletes a file."""
    if isfile(path) and path.startswith(PASSWORD_FOLDER):
        remove(path)
        if verbose_mode:
            print("Deleted {}".format(path))
    else:
        print("{} is not a file".format(path))


def remove_dir(path, verbose_mode=False):
    """Empties and deletes a directory recursively."""
    if isdir(path) and path.startswith(PASSWORD_FOLDER):
        # como medida de seguridad para asegurar que no se le pasa
        # ningún directorio fuera del area de trabajo (como /, p.e.)
        for entry in listdir(path):
            # para cada entrada en el directorio, se eliminan los archivos
            # y se llama recursivamente a la función en los directorios
            # al terminar, se elimina el directorio (ahora vacío)
            full_entry = "/".join((path, entry))
            if isfile(full_entry):
                remove_file(full_entry, verbose_mode)
            elif isdir(full_entry):
                remove_dir(full_entry, verbose_mode)
        rmdir(path)
        if verbose_mode:
            print("Deleted {}".format(path))
    else:
        print("{} is not a valid directory".format(path))


def build_absolute_path(path, ext=".gpg"):
    """Builds absolute '.gpg' file path."""
    return PASSWORD_FOLDER + path + ext


def get_passw(args):
    """Returns a manual typed or generated password."""
    if args.insert:
        passw = getpass("Insert password: ")
    else:
        passw = build_pass(args)
        print("Generated password:\n{}".format(passw))
    return passw


def parse_path(path):
    """Strip starting or ending '/'."""
    if path.startswith('/'):
        path = path[1:]
    if path.endswith('/'):
        path = path[:-1]
    return path


def add(args):
    """Add new password to the storage."""
    check_config()
    passw = get_passw(args)

    encrypted_passw = encrypt_password(passw)
    path = parse_path(args.password_dest)

    if '/' in path:
        folder = get_folder(path)
        mkdir_if_not_exists(PASSWORD_FOLDER + folder, args.verbose)

    absolute_file_path = build_absolute_path(path)
    write_file(absolute_file_path, encrypted_passw, args.verbose)


def rm(args):
    """Remove password from the storage."""
    check_config()
    path = PASSWORD_FOLDER + parse_path(args.path)
    if isfile(path):
        remove_file(path, args.verbose)
    elif isdir(path):
        if args.recursive:
            remove_dir(path, args.verbose)
        else:
            print("{} is a directory".format(path))


def show(args):
    """Decrypt password and show it."""
    # https: // docs.python.org / 3 / library / functions.html  # print
    check_config()
    path = build_absolute_path(parse_path(args.path))
    if isfile(path):
        with open(path) as pass_file_content:
            encrypted_passw = pass_file_content.read().strip()
        passw = decrypt_password(encrypted_passw).strip()
        text = ""
        for t in range(1, args.time + 1)[::-1]:
            print(" "*text.__len__(), end='\r')
            # string "vacía" (invisible) para borrar el input anterior
            # tiene que haber una forma mas bonita...
            text = "You have {0} second(s) to copy the password: {1}".format(t, passw)
            print(text, end='\r')
            sleep(1)
        print(" " * text.__len__(), end='\r')
        print("Time has expired")

    else:
        print("{} is not a stored password".format(path))


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

    # parser for rm command
    parser_remove = subparsers.add_parser('rm', help='removes a stored password')
    parser_remove.add_argument('path',
                               help='path to the password (or folder if -r is used)')
    parser_remove.add_argument('-r', '--recursive',
                               action='store_true',
                               help='removes a folder recursively')

    # parser for show command
    parser_show = subparsers.add_parser('show', help='shows a stored password')
    parser_show.add_argument('path',
                             help='path to the password')
    parser_show.add_argument('-c', '--clipboard',
                             action='store_true',
                             help='copy password to clipboard instead of printing it')
    parser_show.add_argument('-t', '--time',
                             type=int,
                             default=10,
                             help='time the password is shown on screen')

    return parser


def main():
    """Main function."""
    signal.signal(signal.SIGINT, signal_handler)
    parser = build_parser()

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
