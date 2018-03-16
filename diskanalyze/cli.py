import os
import sys

from diskanalyze.dirtree import Tree, get_tree_size
from diskanalyze.report import reporter
import diskanalyze.utils as utils


def main():
    PATH = sys.argv[1] if len(sys.argv) > 1 else input('> ')
    if not PATH:
        exit()

    path = utils.path_norm(PATH)
    root = Tree(path)
    print(path)

    total_size, total_files = get_tree_size(path, root)

    filename = reporter(PATH, root, total_size, total_files)
    os.system("start " + filename)
