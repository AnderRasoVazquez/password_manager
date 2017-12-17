"""This module manages a password storage."""
import sys
import signal
from .parser import build_parser
from .controller import control


def signal_handler(signal, frame):
    """KeyboardInterrupt signal handler."""
    sys.exit("\nExecution aborted!")


def main():
    """Main function."""
    signal.signal(signal.SIGINT, signal_handler)
    parser = build_parser()

    # if no argument was provided append '-h'
    if not sys.argv[1:]:
        sys.argv.extend(['-h'])

    args = parser.parse_args()

    control(args)


if __name__ == '__main__':
    main()
