"""

    Directories Size on Disk Analyzer

    Author: Salas
    Update: 2014/08/20

"""
import os

from diskanalyze.dirtree import Tree, get_tree_size
from diskanalyze.report import reporter
import diskanalyze.utils as utils


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

    filename = reporter(PATH, root)
    os.system("start " + filename)
