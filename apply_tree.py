import os
import time
import shutil

import click

from diskanalyze.dirtree import Tree, apply_tree
from diskanalyze.utils import scaler


@click.command()
@click.argument('fname')
@click.argument('path')
@click.option('--k', default=100)
@click.option('--target', type=click.Path())
def main(fname, path, target, k):
    THRESHOLD = 1024 * k

    root = Tree(path)

    def copy(node, size):
        assert target
        if size > THRESHOLD:
            return
        filepath_target = node.path.replace(path, target)
        os.makedirs(os.path.dirname(filepath_target), exist_ok=Tree)
        shutil.copy(node.path, filepath_target)
        print('Found...' + node.path, scaler(size))

    fn = {
        'cp': copy,
    }[fname]

    s = time.time()
    apply_tree(path, root, fn)
    print('Fin {} (in {:.3f} sec.)'.format(path, time.time() - s))


if __name__ == '__main__':
    main()
