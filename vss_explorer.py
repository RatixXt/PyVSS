import vss_functions
import os
from re import search
import argparse
from shutil import copy


class OutputPathError(Exception):
    pass


def argument_parsing():
    parser = argparse.ArgumentParser(description=u'vss_explorer v0.010 - command-line tool to browse shadow copies '
                                                 u'or to create symlinks to shadow copies',
                                     epilog='made by Alexey Shcherbakov, 2016')
    parser.add_argument('--E', '-Explorer',
                        action='store_true',
                        dest='need_explorer',
                        default=False,
                        help='Enter in shadow explorer mode')
    parser.add_argument('--CL', '--Create Link',
                        action='store_true',
                        dest='need_create_symlink',
                        default=False,
                        help='Create symlink for shadow copies, use argument --O to specify path '
                             'where symlink will create.'
                        )
    parser.add_argument(
                        action='store',
                        type=str,
                        dest='drive_letter',
                        help='Specify drive letter')
    parser.add_argument(
                        '--O',
                        action='store',
                        type=str,
                        dest='output_path',
                        help='Specify output path')

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
    if args.need_explorer:
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
                print_list_dir(drive_letter)

            elif command == 'copy':
                shadow_file, output = arg.split(' ', 1)
                # Надо исправить разделение двух аргументов
                # vss_functions.copy_shadow_as_file(shadow_file, output)
                copy(shadow_file, output)
                print('File copied.')

            elif command == 'stat':
                print(os.lstat(arg))

            elif command == 'open':
                print(vss_functions.open_shadow(arg))

            elif command == 'quit' or command == 'q':
                print('Goodbye!')
                break

            elif command == 'help':
                print('You can use next commands:', 'help - show this help message',
                      'cd DIRECTORY - for changing work directory on DIRECTORY, or use cd .. to browse parent dircetory',
                       'ls - output current working directory',
                       'copy FILE_NAME OUTPUT_PATH - сopy FILE_NAME to OUTPUT_PATH',
                       'stat FILE_NAME - output stat of the FILE_NAME',
                       'open FILE_NAME - open file in binary mode (don\'t use this with big files)',
                       'quit, q - quit the program',
                      sep='\n')

            else:
                print('No such command {}, try again'.format(command))

            command, arg = parse_command(input('>'))

    elif args.need_create_symlink:

        if args.output_path:
            for path in shadow_paths:
                symlink_name = search('HarddiskVolumeShadowCopy\d+', path).group(0)
                os.symlink(path, '{}/{}'.format(args.output_path, symlink_name), True)
            print('Success!')
        else:
            print('Please, specify output path for symlinks with --O parameter.')

    else:
        print('Not enough arguments. Use --h key for help.')

