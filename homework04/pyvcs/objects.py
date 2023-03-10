import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    root = pathlib.Path(".git")
    head = f"{fmt} {len(data)}\0"
    store = head.encode() + data
    hash = hashlib.sha1(store).hexdigest()
    if not write:
        return hash
    path = root / "objects" / hash[:2]
    path.mkdir(parents=True, exist_ok=True)
    with (path / hash[2:]).open("wb") as f:
        f.write(zlib.compress(store))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if not 4 <= len(obj_name) <= 40:
        raise ValueError(f"Not a valid object name {obj_name}")
    objects_path = gitdir / "objects" / obj_name[:2]
    objects = [
        obj_name[:2] + obj_path.name
        for obj_path in objects_path.iterdir()
        if obj_path.name.find(obj_name[2:]) != -1
    ]
    if not objects:
        raise ValueError(f"Not a valid object name {obj_name}")
    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> tp.Optional[str]:
    parts = gitdir.parts
    if obj_name[2:] in parts[-1]:
        return f"{parts[-2]}{parts[-1]}"
    return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj_path = gitdir / "objects" / sha[:2] / sha[2:]
    with obj_path.open("rb") as f:
        compressed = f.read()
    uncompressed = zlib.decompress(compressed)
    header, content = uncompressed.split(b"\x00", maxsplit=1)
    fmt, size_str = header.decode().split()
    size = int(size_str)
    assert len(content) == size
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    i = 0
    while i < len(data):
        j = data.find(b" ", i)
        mode = int(data[i:j].decode())
        i = j + 1
        j = data.find(b"\x00", i)
        name = data[i:j].decode()
        i = j + 1
        sha = bytes.hex(data[i : i + 20])
        i += 20
        result.append((mode, name, sha))
    return result


def format_tree(files: tp.List[tp.Tuple[int, str, str]]) -> str:
    lines = []
    for f in files:
        obj_type, obj_data = read_object(f[2], pathlib.Path(".git"))
        line = f"{f[0]:06} {obj_type} {f[2]}\t{f[1]}"
        lines.append(line)
    return "\n".join(lines)


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    objects = resolve_object(obj_name, gitdir)
    for obj in objects:
        obj_type, data = read_object(obj, gitdir)
        if pretty:
            if obj_type == "tree":
                files = read_tree(data)
                print(format_tree(files))
            else:
                print(data.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            subtree_files = find_tree_files(f[2], gitdir)
            for name, blob_sha in subtree_files:
                full_path = f"{f[1]}/{name}"
                result.append((full_path, blob_sha))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    i = data.find(b"tree")
    return data[i + 5 : i + 45]
