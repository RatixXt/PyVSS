import vss_functions
import os
from re import search
import argparse


def argument_parsing():
    parser = argparse.ArgumentParser(description=u'Great Description To Be Here')

    parser.add_argument(
                        action='store',
                        type=str,
                        dest='drive_letter',
                        help='Specify drive letter')

    return parser.parse_args()

def parse_command(input_arg):
    parsed = input_arg.split(' ', 1)
    if len(parsed) == 1:
        return parsed[0], False
    else:
        return parsed[0], parsed[1]


def get_parent_directory():
    parent_dir = '{}\\'.format(os.path.dirname(os.getcwd()))
    if search('VolumeShadowCopy',parent_dir):
        os.chdir(parent_dir)


def print_list_dir(drive_letter):
    unshadow_wd = vss_functions.unshadow_path(drive_letter, os.getcwd())
    print(unshadow_wd)
    indent = len(unshadow_wd) * ' '
    [print('{0}{1}'.format(indent, file)) for file in os.listdir()]


if __name__ == '__main__':

    args = argument_parsing()
    drive_letter = '{}:\\'.format(args.drive_letter)
    shadow_paths = vss_functions.get_shadow_paths(drive_letter)
    if shadow_paths is None:
        print('You don\'t have shadow copies of this drive')
        exit(1)
    else:
        new_wd = vss_functions.get_last_shadow_path(shadow_paths)
    os.chdir(new_wd)
    print_list_dir(drive_letter)
    command, arg = parse_command(input('>'))

    while True:
        if command == 'cd':
            if arg == '..':
                get_parent_directory()
            else:
                os.chdir(arg)

        elif command == 'ls':
            unshadow_wd = vss_functions.unshadow_path(drive_letter, os.getcwd())
            print(unshadow_wd)
            indent = len(unshadow_wd)*' '
            [print('{0}{1}'.format(indent, file)) for file in os.listdir()]

        elif command == 'copy':
            shadow_file, output = arg.split(' ', 1)
            vss_functions.copy_shadow_as_file(shadow_file, output)
            print('File copied.')

        elif command == 'stat':
            print(os.lstat(arg))

        elif command =='open':
            print(vss_functions.open_shadow(arg))

        elif command == 'quit' or command == 'q':
            print('Goodbye!')
            break

        else:
            print('No such command {}, try again'.format(command))

        command, arg = parse_command(input('>'))



