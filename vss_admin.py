# -*- coding:utf-8 -*-
import vss_functions
import argparse


def argument_parsing():
    parser = argparse.ArgumentParser(description=u'vss_admin v0.010 - command-line tool to administer '
                                                 u'Volume Shadow Copy Service',
                                     epilog='made by Alexey Shcherbakov, 2016')
    parser.add_argument('--LS', '-List_shadows',
                        action='store_true',
                        dest='need_list_shadows',
                        default=False,
                        help='Display all shadows copies')

    parser.add_argument('--C', '-Create_shadow',
                        action='store_true',
                        dest='need_to_create_shadow_copy',
                        default=False,
                        help='Create shadow copy, you can specify drive letter with parameter --D')

    parser.add_argument('--DS', '-Delete_shadow',
                        action='store_true',
                        default=False,
                        dest='need_to_delete_shadow',
                        help='Delete shadow copy, you need to specify shadow copy id with parameter --id')

    parser.add_argument('--id',
                        action='store',
                        type=str,
                        dest='shadow_id',
                        help='Specify shadow copy id')

    parser.add_argument('--D',
                        action='store',
                        type=str,
                        dest='drive_letter',
                        help='Specify drive letter')

    return parser.parse_args()


class ShadowIdError(Exception):
    pass


if __name__ == '__main__':
    args = argument_parsing()
    try:
        if args.need_list_shadows:
            vss_functions.List_shadows()

        elif args.need_to_create_shadow_copy:
            if args.drive_letter:
                vss_functions.vss_create(args.drive_letter)
            else:
                vss_functions.vss_create('C')
            print('Success!')

        elif args.need_to_delete_shadow:
            if args.shadow_id:
                vss_functions.vss_delete("{%s}" % args.shadow_id)
                print('Success!')
            else:
                raise ShadowIdError
        else:
            print('Not enough arguments. Use --h key for help.')
    except ShadowIdError:
        print('Please, specify shadow ID with --id parameter, or check shadow id.')
