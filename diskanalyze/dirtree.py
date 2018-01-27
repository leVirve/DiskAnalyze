import os
import sys


class Tree:

    def __init__(self, path, level=0):
        self.name = path
        self.children = []
        self.size = 0
        self.level = level

    def add(self, node):
        self.children.append(node)

    def __str__(self):
        return 'Tree(%s @lv%d)' % (self.name, self.level)


def get_tree_size(path, tree, THRESHOLD):
    """
    Return total size of files in path and subdirs. If
    is_dir() or stat() fails, print an error message to stderr
    and assume zero size (for example, file has been deleted).
    """
    total = 0
    try:
        for entry in os.scandir(path):
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError as error:
                print('Error calling is_dir():', error, file=sys.stderr)
                continue
            if is_dir:
                node = Tree(entry.name, tree.level + 1)
                sz = get_tree_size(entry.path, node, THRESHOLD)
                if sz > THRESHOLD:
                    node.size = sz
                    tree.add(node)
                total += sz
            else:
                try:
                    total += entry.stat(follow_symlinks=False).st_size
                except OSError as error:
                    print('Error calling stat():', error, file=sys.stderr)
    except PermissionError as error:
        print('Permission denied os.scandir():', error, file=sys.stderr)
    except FileNotFoundError as error:
        print('FileNotFoundError os.scandir():', path, file=sys.stderr)
    return total


def apply_tree(path, tree, func):
    try:
        for entry in os.scandir(path):
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError as error:
                print('Error calling is_dir():', error, file=sys.stderr)
                continue
            if is_dir:
                node = Tree(entry.name, tree.level + 1)
                apply_tree(entry.path, node, func)
            else:
                try:
                    sz = entry.stat(follow_symlinks=False).st_size
                    func(entry, sz)
                except OSError as error:
                    print('Error calling stat():', error, file=sys.stderr)
    except PermissionError as error:
        print('Permission denied os.scandir():', error, file=sys.stderr)
    except FileNotFoundError as error:
        print('FileNotFoundError os.scandir():', path, file=sys.stderr)
