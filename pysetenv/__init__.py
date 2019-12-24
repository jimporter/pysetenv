import argparse
import os
import subprocess

from .version import version


def main():
    parser = argparse.ArgumentParser(
        prog='pysetenv',
        usage='%(prog)s [OPTION]... [NAME=VALUE]... [COMMAND [ARG]...]',
        description=('Set each NAME to VALUE in the environment and run ' +
                     'COMMAND. If COMMAND is not specified, print the ' +
                     'resulting environment instead.')
    )

    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)
    parser.add_argument('-i', action='store_true', dest='ignore_environment',
                        help='ignore inherited environment variables')
    parser.add_argument('-u', dest='undef', metavar='NAME', action='append',
                        default=[], help='remove NAME from the environment')
    parser.add_argument('args', metavar='ARGS', nargs=argparse.REMAINDER,
                        help='environment variable or command argument')

    args = parser.parse_args()

    if args.ignore_environment:
        os.environ.clear()
    for undef in args.undef:
        os.environ.pop(undef, None)

    for i, val in enumerate(args.args):
        if i == 0 and val == '--':
            continue
        name, sep, value = val.partition('=')
        if sep:
            os.environ[name] = value
        else:
            break
    else:
        for i in os.environ:
            print('{}={}'.format(i, os.environ[i]))
        return 0

    return subprocess.call(args.args[i:])
