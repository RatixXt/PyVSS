import argparse


def argument_parsing():
    parser = argparse.ArgumentParser(description=u'Great Description To Be Here')
    parser.add_argument('--LS', '-List_shadows',
                        action='store_true',
                        # type=bool,
                        dest='need_list_shadows',
                        default=False,
                        help='Display all shadows copies')

    parser.add_argument('--GS', '-Get_shadow_path',
                        action='store_true',
                        # type=bool,
                        default=False,
                        dest='need_to_get_shadow_path',
                        help='Get shadow path from normal path, you need to specify normal path with --I parameter')

    parser.add_argument('--GH', '-Get_hash',
                        action='store_true',
                        # type=bool,
                        default=False,
                        dest='need_to_save_hash',
                        help='Saving SAM and SYSTEM file from \\System32\\config\\ with hash of passwords, '
                             'you can specify path where this files will be saved in --O parameter')

    parser.add_argument('--C', '-Create_shadow_copy',
                        action='store_true',
                        # type=bool,
                        dest='need_to_create_shadow_copy',
                        default=False,
                        help='Create shadow copy, you can specify drive letter with parameter --D')

    parser.add_argument('--DS', '-Delete_shadow',
                        action='store_true',
                        # type=bool,
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

    parser.add_argument('--I',
                        action='store',
                        type=str,
                        dest='input_path',
                        help='Specify input path')

    parser.add_argument('--O',
                        action='store',
                        type=str,
                        dest='output_path',
                        help='Specify output path')

    return parser.parse_args()