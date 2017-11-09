'''Main entry for the static site generator tool'''

# Link the cli.py from cray/ to this top-level directory just for test
# using `ln -s` on Linux and `mklink` on Windows Since Windows Vista
import argparse
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
    Usage:
    cray [subcommand] [behavior] [params...] 

    Subcommand could be one of "init", "post", "page", "generate", "preview", all subcommands 
    should be executed under the root of a site except for "init"

    for each subcommand, there are some allowed behaviors to use.
    currently, only behaviors for subcommand "post" are implemented, they are:
    
    cray post list
    cray post read <file>
    cray post create <file>
    cray post delete <file>

    The file is the real name of the post file, it could be retrived from "cray post list"

    other subcommands available now are:
    cray init
    cray generate
    cray preview

    More stuff will be added here along with the implemtation to more subcommands and behaviors.
    ''')
    print(usage_msg)

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def get_argparse():
    parser = DefaultHelpParser(prog='cray', description='homebrew static site generator')

    modules_parser = parser.add_subparsers(dest='module_name', title='subcommand list')

    module_init = modules_parser.add_parser('init', description='create a site', \
    help='create a site')
    module_init.add_argument('site_name', help='The site name')

    module_post = modules_parser.add_parser('post', help='subcommand post manager help')
    post_command_parser = module_post.add_subparsers(dest='command_name', \
    help='post module commands')

    post_list_command = post_command_parser.add_parser('list', \
    help='list all entries in post directory')
    post_list_command.add_argument('-v', '--verbose', action='store_true', \
    help='increase verbosity of output')

    post_read_command = post_command_parser.add_parser('read', help='read specified post content')
    post_read_command.add_argument('file_name', help='file name of the post which to be read')
    post_read_command.add_argument('--meta', action='store_true', \
    help='check only meta information of specified post')
    post_read_command.add_argument('--content', action='store_true', \
    help='check only content of specified post')

    post_create_command = post_command_parser.add_parser('create', help='create a post')
    post_create_command.add_argument('file_name', help='file name of the post which to be created')
    post_create_command.add_argument('--public', \
    help='decide if the newly created post is public', action='store_true')

    post_delete_command = post_command_parser.add_parser('delete', help='delete a post')
    post_delete_command.add_argument('file_name', help='file name of the post which to be deleted')

    module_page = modules_parser.add_parser('page', help='subcommand page manager help')
    module_generate = modules_parser.add_parser('generate', \
    description='generate site with current configuration', \
    help='generate site with current configuration')
    module_preview = modules_parser.add_parser('preview', \
    description='start a simple server to preivew generated site', \
    help='start a simple server to preivew generated site')

    parser.add_argument('-v', '--verbose', help='increate output verbosity', action='store_true')

    return parser


def main(args=None):
    '''Entry for cray'''

    if not args:
        args = sys.argv
        
    cray_parser = get_argparse()
    if len(args[1:]) == 0:
        cray_parser.print_help()
    # parser.print_usage() # for just the usage line
        cray_parser.exit()
    args = cray_parser.parse_args()
    #print(vars(args))

    if args.module_name == 'init':
        create_manager = CreateManager(os.getcwd(), args.site_name)
        if create_manager.create():
            print('Successfully create static site %s!' % args.site_name)

        sys.exit(0)

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
    if args.module_name == 'post':

        post_dir = os.path.join(os.getcwd(), '_post')
        post_manager = PostManager(post_dir)
        post_manager.parse_arg(args)

    elif args.module_name == 'page':
        pass
    elif args.module_name == 'generate':
        generate_manager = GenerateManager(os.getcwd())
        generate_manager.read_config(conf_loader)
        generate_manager.generate_site()
    elif args.module_name == 'preview':
        # call HTTP module to start a server on the site directory
        # python -m http.server 8000

        start_server(full_generate_path(os.getcwd(), conf_loader.get_config()))

    elif args.module_name == 'deploy':
        pass



if __name__ == '__main__':
    main(sys.argv)
