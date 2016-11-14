# -*- coding:utf-8 -*-
import vss_functions
from console_argparse import argument_parsing
from os import path

class ShadowIdError(Exception):
    pass


class InputPathError(Exception):
    pass


if __name__ == '__main__':
    args = argument_parsing()
    try:
        if args.need_list_shadows:
            vss_functions.List_shadows()

        elif args.need_to_get_shadow_path:
            if args.input_path:
                print(vss_functions.get_shadow_paths(args.input_path))
            else:
                raise InputPathError
        elif args.need_to_save_hash:
            if args.output_path:
                output_path = args.output_path
            else:
                output_path = ''
            vss_functions.copy_shadow_as_file(
                shadow_path=vss_functions.get_last_shadow_path(
                    vss_functions.get_shadow_paths(r'С:\Windows\System32\config\SAM')),
                output='{}\{}'.format(output_path, 'sam')
            )
            vss_functions.copy_shadow_as_file(
                shadow_path=vss_functions.get_last_shadow_path(
                    vss_functions.get_shadow_paths(r'С:\Windows\System32\config\SYSTEM')),
                output='{}\{}'.format(output_path, 'system')
            )
            print('Success!')
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
    except InputPathError:
        print('Please, specify input path with --I parameter.')
    except ShadowIdError:
        print('Please, specify shadow ID with --id parameter, or check shadow id.')


