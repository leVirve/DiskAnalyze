
def scaler(size):
    """ transform the size into string scale
    """
    scale = 0
    while size > 1024:
        size /= 1024
        scale += 1
    return '{0:.1f} '.format(size) + ('B', 'KB', 'MB', 'GB')[scale]
