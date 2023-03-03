import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    path = gitdir / ref
    f = path.open("w")
    f.write(new_value)
    f.close()


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    (gitdir / name).open("w").write(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    refname = get_ref(gitdir) if refname == "HEAD" else refname
    if is_detached(gitdir):
        return refname
    return (gitdir / pathlib.Path(refname)).open("r").read()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    return ref_resolve(gitdir, "HEAD") if (gitdir / get_ref(gitdir)).exists() else None


def is_detached(gitdir: pathlib.Path) -> bool:
    return "ref" not in (gitdir / "HEAD").open("r").read()


def get_ref(gitdir: pathlib.Path) -> str:
    path = gitdir / "HEAD"
    detached = is_detached(gitdir)
    with path.open("r") as f:
        ref = f.read()[5:-1] if not detached else f.read()
    return ref
