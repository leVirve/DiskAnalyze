import sys
import time

from diskanalyze.dirtree import Tree, get_tree_size
from diskanalyze.utils import scaler


def traverse(node):
    print('{}"{}" ... {}'.format(
        ' ' * node.level, node.name, scaler(node.folder_size)))
    for e in node.children:
        traverse(e)


THRESHOLD = 1024 * 1024 * 100  # 100 MB
# THRESHOLD = 1024 * 1  # 100 KB

path = sys.argv[1] if len(sys.argv) > 1 else 'C:\\Users\\salas'
root = Tree(path)

s = time.time()
_ = get_tree_size(path, root)
print('Total size of "{}": {} (in {:.3f} sec.)'.format(
    path, scaler(root.folder_size), time.time() - s))

traverse(root)
