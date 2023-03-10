import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    content = []
    for entry in index:
        if entry.name.startswith(dirname):
            if entry.name[len(dirname) :].count("/") == 0:
                content.append((entry.mode, entry.name[len(dirname) :], entry.sha1))
            else:
                new_dirname = dirname + entry.name[len(dirname) :].split("/")[0] + "/"
                tree_sha = bytes.fromhex(write_tree(gitdir, index, new_dirname))
                content.append((stat.S_IFDIR, entry.name[len(dirname) :].split("/")[0], tree_sha))
    content_binary = b"".join(
        f"{mode:o} {name}".encode() + b"\0" + sha1 for mode, name, sha1 in content
    )
    return hash_object(content_binary, "tree", write=True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    commit_message = f"tree {tree}\n"
    if parent is not None:
        commit_message += f"parent {parent}\n"
    unix_timestamp = int(time.mktime(time.localtime()))
    time_zone = time.timezone
    if time_zone > 0:
        author_time = f"{unix_timestamp} -0{time_zone // 3600}{(time_zone // 60) % 60}0"
    else:
        author_time = f"{unix_timestamp} +0{abs(time_zone) // 3600}{(abs(time_zone) // 60) % 60}0"
    commit_message += "\n".join(
        (
            f"author {author} {author_time}",
            f"committer {author} {author_time}",
            f"\n{message}\n"
        )
    )
    commit_hash = hash_object(commit_message.encode(), "commit", True)
    return commit_hash
