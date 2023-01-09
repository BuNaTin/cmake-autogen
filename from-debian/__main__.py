import sys
import argparse
import pathlib

import deps
import cmake

def main(folder: str, force: bool, type: str):

    if not deps.init(folder, force):
        print("Could not init dependencies files")
        exit(1)

    find_deps = deps.get_all(folder)

    for dep in find_deps:
        deps.create(folder, dep) 

    print(find_deps)

    cmake.gen(folder, type, find_deps, force)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='from-debian', description='From debian folder and sources create cmake with cmake/Find files', epilog="Please don't call me")
    
    parser.add_argument('-f', '--force', action='store_true', help='recreate FindCmake files')
    parser.add_argument('-t', '--type', required=True, choices=cmake.source_types)
    parser.add_argument('dir', type=pathlib.Path, help="directory of a project")
    
    args = parser.parse_args(sys.argv[1:])
    main(str(args.dir), args.force, args.type)
