import sys
import time

from diskanalyze.dirtree import Tree, get_tree_size
from diskanalyze.utils import scaler


def traverse(node):
    print('{}"{}" ... {}'.format(
        ' ' * node.level, node.name, scaler(node.size)))
    for e in node.children:
        traverse(e)


THRESHOLD = 1024 * 1024 * 100  # 100 MB
# THRESHOLD = 1024 * 1  # 100 KB

path = sys.argv[1] if len(sys.argv) > 1 else 'C:\\Users\\salas'
root = Tree(path)

s = time.time()
root.size = get_tree_size(path, root, THRESHOLD)
print('Total size of "{}": {} (in {:.3f} sec.)'.format(
    path, scaler(root.size), time.time() - s))

traverse(root)
