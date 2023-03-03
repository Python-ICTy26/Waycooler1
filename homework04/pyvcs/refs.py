import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    # PUT YOUR CODE HERE
    return {}


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    # PUT YOUR CODE HERE
    return {}


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    # PUT YOUR CODE HERE
    return {}


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    # PUT YOUR CODE HERE
    return {}


def is_detached(gitdir: pathlib.Path) -> bool:
    # PUT YOUR CODE HERE
    return {}


def get_ref(gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    return {}
