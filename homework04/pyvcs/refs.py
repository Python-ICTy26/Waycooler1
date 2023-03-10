import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    if isinstance(ref, pathlib.Path):
        ref_path = ref
    elif ref.startswith("refs/"):
        ref_path = gitdir / ref
    else:
        ref_path = gitdir / "refs" / "heads" / ref
    ref_path.write_text(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    (gitdir / name).open("w").write(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    if refname == "HEAD":
        refname = get_ref(gitdir)
    if is_detached(gitdir):
        return refname
    with (gitdir / refname).open("r") as f:
        return f.read().strip()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    head_ref = get_ref(gitdir)
    if (gitdir / head_ref).exists():
        return ref_resolve(gitdir, "HEAD")
    else:
        return None


def is_detached(gitdir: pathlib.Path) -> bool:
    with (gitdir / "HEAD").open("r") as f:
        return "ref" not in f.read()


def get_ref(gitdir: pathlib.Path) -> str:
    path = gitdir / "HEAD"
    detached = is_detached(gitdir)
    with path.open("r") as f:
        ref = f.read()
        return ref.strip() if detached else ref[5:-1]
