import pathlib
import argparse
import shutil
import tempfile
import os
from typing import List, Union


def get_files_from_dir(directory: pathlib.Path):
    extensions = ('png', 'jpg', 'jpeg')
    suffixes = (f'.{ext}' for ext in extensions)
    for suffix in suffixes:
        glob = list(directory.glob(f'*{suffix}'))
        if glob:
            return glob
    raise FileNotFoundError(f'No image was found inside {directory}! Supported extensions: {extensions}')


def order_files(files: List[pathlib.Path]):
    # DEBUG
    # files = [i for i, _ in enumerate(files)]
    ordered_files = files.copy()

    if len(files) < 3:
        return ordered_files

    j = 1
    for i in range(1, len(files) // 2):
        ordered_files.insert(j, ordered_files[-1])
        del ordered_files[-1]
        j += 2

    return ordered_files


def rename_files(files: List[pathlib.Path], dst: Union[None, str, pathlib.Path] = None):
    tdir = pathlib.Path(tempfile.mkdtemp())
    tfiles = []
    if not dst:
        dst = files[0].parent

    for i, file in enumerate(files):
        tfile = tdir / f'{str(i).zfill(3)}{file.suffix}'
        shutil.copy(file, tfile)
        tfiles.append(tfile)

    for file in tfiles:
        shutil.move(file, dst / file.name)

    shutil.rmtree(tdir, ignore_errors=True)

    return files


def main():
    parser = argparse.ArgumentParser('PostScan')
    parser.add_argument('directory')
    args = parser.parse_args()

    d = pathlib.Path(args.directory)
    if not d.is_dir():
        raise ValueError('Must provide a valid directory!')
    files = get_files_from_dir(d)

    # work on found files
    ordered = order_files(files)

    out = pathlib.Path('output')
    os.makedirs(out, exist_ok=True)
    rename_files(ordered, out)
    print('Renamed files!')


if __name__ == '__main__':
    main()
