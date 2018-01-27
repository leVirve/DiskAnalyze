"""

    Directories Size on Disk Analyzer

    Author: Salas
    Update: 2014/08/20

"""
import os
import sys

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

total_file = 0
total_dirs = 0
total_size = 0


def scaler(size):
    """ transform the size into string scale
    """
    scale = 0
    while size > 1024:
        size /= 1024
        scale += 1
    return '{0:.1f} '.format(size) + ('B', 'KB', 'MB', 'GB')[scale]


def treesize_simple(path):
    """ One line implementation,
        but no exception control """
    return sum(os.path.getsize(os.path.join(dirpath, filename))
               for dirpath, dirnames, filenames in os.walk(path)
               for filename in filenames
               )


def treesize(path):
    """ recursively get the size of
        all files and directories under the path """
    if os.path.isfile(path):
        sum_size = os.path.getsize(path)
    else:
        sum_size = 0

        for dirpath, dirnames, filenames in os.walk(path):
            global total_dirs
            global total_file
            total_dirs += len(dirnames)
            total_file += len(filenames)

            for filename in filenames:
                p = os.path.join(dirpath, filename)
                try:
                    sum_size += os.path.getsize(p)
                except FileNotFoundError as e:
                    # File path too long (> 260), fk Win32API!
                    path = "\\\\?\\" + p
                    sum_size += os.path.getsize(path)
                except Exception as e:
                    print(e, file=err_dump)

    raw_size = sum_size
    str_size = scaler(sum_size)

    return str_size, raw_size


def reporter(root, result):
    """ generate the report file,
        using template view defined under ./source/res/
    """
    global total_size

    view = template.read()
    data = 'var data = ['
    entries = ''

    choose = 0
    for key, value in sorted(result.items(), key=lambda x: x[1][1], reverse=True):
        choose %= len(COLORSET)
        data += (
            '{ value: %s,'
            'color: "%s",'
            'highlight: "%s",'
            'label: "%s" },'
            % (value[1], COLORSET[choose][0], COLORSET[choose][1], key)
        )
        entries += (
            '<li class="list-group-item" style="color:%s">%s - %s</li>'
            % (COLORSET[choose][0], key, value[0])
        )
        total_size += value[1]
        choose += 1
    data += '];'

    res = scaler(total_size).split()
    total_size, suffix = res[0], res[1]
    snapshot.write(view % (root, total_size, suffix, total_file, total_dirs, entries, data))

    snapshot.close()
    err_dump.close()

    # Remove err_dump.log file if it's empty
    remove_err_log = False
    with open(ERR_DUMP, 'r', encoding='utf-8') as f:
        if not f.read():
            remove_err_log = True
    if remove_err_log:
        os.remove(ERR_DUMP)


def path_norm(path):
    path.strip()
    if path[0] == '"':
        path = path[1:-1]
    path = os.path.normpath(path)
    return path

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
        sys.exit(0)

    path = path_norm(PATH)
    print(path)
    result = dict()
    for p in os.listdir(path):
        pp = os.path.join(path, p)
        result[p] = treesize(pp)

    reporter(PATH, result)
    os.system("start " + FILENAME)
