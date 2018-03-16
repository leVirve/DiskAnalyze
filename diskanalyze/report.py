import os
import pkg_resources

import diskanalyze.utils as utils


def reporter(path, root, total_size, total_files):
    """ generate the report file,
        using template view defined under ./source/res/
    """

    COLORSET = [("#F7464A", "#FF5A5E"),
                ("#46BFBD", "#5AD3D1"),
                ("#43B4DE", "#57C8F2"),
                ("#FDB45C", "#FFC870"),
                ("#E4BF33", "#F8D347"),
                ("#949FB1", "#A8B3C5"),
                ("#4D5360", "#616774")]

    FILENAME = "snapshot.html"
    ERR_DUMP = "error_dump.log"

    snapshot = open(FILENAME, 'w', encoding='utf8')
    err_dump = open(ERR_DUMP, 'w', encoding='utf8')
    template = open(pkg_resources.resource_filename(
        __name__, 'resource/template.html'), 'r').read()
    chartjs = pkg_resources.resource_filename(__name__, 'resource/Chart.js')

    data = 'var data = ['
    entries = ''

    choose = 0
    for node in root.children:
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
    data += '];'

    res = utils.scaler(total_size).split()
    total_size, suffix = res[0], res[1]
    snapshot.write(template % (
        chartjs,
        path, total_size, suffix, total_files, entries, data))

    snapshot.close()
    err_dump.close()

    # Remove err_dump.log file if it's empty
    remove_err_log = False
    with open(ERR_DUMP, 'r', encoding='utf-8') as f:
        if not f.read():
            remove_err_log = True
    if remove_err_log:
        os.remove(ERR_DUMP)

    return FILENAME
