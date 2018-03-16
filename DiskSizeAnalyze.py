"""

    Directories Size on Disk Analyzer

    Author: Salas
    Update: 2014/08/20

"""
import os

from diskanalyze.dirtree import Tree, get_tree_size
import diskanalyze.utils as utils


FILENAME = "snapshot.html"
TEMPLATE = "source/res/template.html"
ERR_DUMP = "error_dump.log"

template = open(TEMPLATE, 'r')
snapshot = open(FILENAME, 'w', encoding='utf8')
err_dump = open(ERR_DUMP, 'w', encoding='utf8')

COLORSET = [("#F7464A", "#FF5A5E"),
            ("#46BFBD", "#5AD3D1"),
            ("#43B4DE", "#57C8F2"),
            ("#FDB45C", "#FFC870"),
            ("#E4BF33", "#F8D347"),
            ("#949FB1", "#A8B3C5"),
            ("#4D5360", "#616774")]


def reporter(root, result):
    """ generate the report file,
        using template view defined under ./source/res/
    """
    view = template.read()
    data = 'var data = ['
    entries = ''

    choose = 0
    total_size = 0
    total_files = 0
    for node in result.children:
        choose %= len(COLORSET)
        data += (
            '{'
            f'value: {node.folder_size},'
            f'color: "{COLORSET[choose][0]}",'
            f'highlight: "{COLORSET[choose][1]}",'
            f'label: "{node.name}"'
            '},')
        entries += (
            f'<li class="list-group-item" style="color:{COLORSET[choose][0]}">'
            f'{node.name} - {utils.scaler(node.folder_size)}</li>')
        choose += 1
        total_size += node.folder_size
        total_files += node.num_files
    data += '];'

    res = utils.scaler(total_size).split()
    total_size, suffix = res[0], res[1]
    snapshot.write(view % (
        root, total_size, suffix, total_files, 0, entries, data))

    snapshot.close()
    err_dump.close()

    # Remove err_dump.log file if it's empty
    remove_err_log = False
    with open(ERR_DUMP, 'r', encoding='utf-8') as f:
        if not f.read():
            remove_err_log = True
    if remove_err_log:
        os.remove(ERR_DUMP)


使用方法 = '''
           ** 資料夾容量分布分析 **

        使用方法:
        1. 手動輸入欲分析資料夾路徑
        2. 直接將資料夾拖進視窗

                Author: Salas 2014/08
        '''

if __name__ == '__main__':
    print(使用方法)
    PATH = input('> ')
    if not PATH:
        exit()

    path = utils.path_norm(PATH)
    root = Tree(path)
    print(path)

    _ = get_tree_size(path, root)

    reporter(PATH, root)
    os.system("start " + FILENAME)
