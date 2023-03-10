import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    tree = write_tree(gitdir, index)
    return commit_tree(gitdir, tree, message, author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    index = read_index(gitdir)
    for f in index:
        if pathlib.Path(f.name).is_file():
            if "/" in f.name:
                shutil.rmtree(f.name[: f.name.find("/")])
            else:
                os.remove(f.name)
    obj_path = gitdir / "objects" / obj_name[:2] / obj_name[2:]
    file = open(obj_path, "rb")
    commit = file.read()
    tree_files = find_tree_files(commit_parse(commit).decode(), gitdir)
    for name, sha in tree_files:
        if "/" in name:
            dir_name = name[: name.find("/")]
            if not pathlib.Path(dir_name).exists():
                pathlib.Path(dir_name).absolute().mkdir()
        with open(name, "w") as file:
            header, content = read_object(sha, gitdir)
            file.write(content.decode())
