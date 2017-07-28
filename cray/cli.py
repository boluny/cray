'''Main entry for the static site generator tool'''

# Link the cli.py from cray/ to this top-level directory just for test
# using `ln -s` on Linux and `mklink` on Windows Since Windows Vista
import os
import sys
import textwrap

from cray.craylib.post_manager import PostManager
from cray.craylib.generate_manager import GenerateManager
from cray.craylib.create_manager import CreateManager
from cray.craylib.config_loader import ConfigLoader
from cray.craylib.utility import start_server, is_valid_site, full_generate_path


def usage():
    '''Print usage message'''
    usage_msg = textwrap.dedent(r'''
    usage:
    cray [class] [behavior] [params...] 
    ''')
    print(usage_msg)

def main(args=None):
    '''Entry for cray'''

    if args is None:
        args = sys.argv

    if len(args) < 2:
        print("Arguments are not sufficient for directory", os.getcwd())
        usage()
        exit(-1)

    if args[1] == 'init':
        if not len(args) == 3:
            print("Invalid params for command 'cray init'")
            exit(-1)

        create_manager = CreateManager(os.getcwd(), args[2])
        if create_manager.create():
            print('Successfully create static site %s!' % args[2])

        return

    # operations other than 'create' should under the site prototype root directory
    if not is_valid_site(os.getcwd()):
        print("Not a valid site structure, please check if this directory contains", \
        "required folders and files.")
        exit(-1)

    conf_loader = ConfigLoader(os.getcwd())
    if not conf_loader.parse_config():
        print("Invalid configuration file, please check.")
        exit(-1)

    # handle post related command logic
    if args[1] == 'post':

        post_dir = os.path.join(os.getcwd(), '_post')
        post_manager = PostManager(post_dir)
        post_manager.parse_arg(args[2:])

    elif args[1] == 'page':
        pass
    elif len(args) == 2 and args[1] == 'generate':
        generate_manager = GenerateManager(os.getcwd())
        generate_manager.read_config(conf_loader)
        generate_manager.generate_site()
    elif args[1] == 'preview':
        # call HTTP module to start a server on the site directory
        # python -m http.server 8000

        start_server(full_generate_path(os.getcwd(), conf_loader.get_config()))

    elif args[1] == 'deploy':
        pass

    else:
        print("Unimplemented option, exit!")
        exit(-1)


if __name__ == '__main__':
    main(sys.argv)
