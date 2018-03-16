import os


def scaler(size):
    """ transform the size into string scale
    """
    scale = 0
    while size > 1024:
        size /= 1024
        scale += 1
    return '{0:.1f} '.format(size) + ('B', 'KB', 'MB', 'GB')[scale]


def path_norm(path):
    path.strip()
    if path[0] == '"':
        path = path[1:-1]
    path = os.path.normpath(path)
    return path


def treesize_simple(path):
    """ One line implementation,
        but no exception control """
    return sum(os.path.getsize(os.path.join(dirpath, filename))
               for dirpath, dirnames, filenames in os.walk(path)
               for filename in filenames
               )


total_file = 0
total_dirs = 0


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
                    # print(e, file=err_dump)
                    pass

    raw_size = sum_size
    str_size = scaler(sum_size)

    return str_size, raw_size
