import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    workdir_path = pathlib.Path(workdir).resolve()
    git_dir_name = os.environ.get("GIT_DIR", ".git")
    git_dir_path = workdir_path / git_dir_name

    if git_dir_path.exists() and git_dir_path.is_dir():
        return git_dir_path

    if workdir_path.parent == workdir_path:
        raise Exception("Not a git repository")

    return repo_find(workdir_path.parent)


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    root = os.getenv("GIT_DIR", ".git")
    workdir = pathlib.Path(workdir)
    if workdir.is_file():
        raise ValueError(f"{workdir.name} is not a directory")
    try:
        os.makedirs(workdir / root / "refs" / "heads")
        os.makedirs(workdir / root / "refs" / "tags")
        os.makedirs(workdir / root / "objects")
    except OSError as e:
        raise Exception(f"Failed to create directories: {e}") from e
    try:
        with open(workdir / root / "HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        with open(workdir / root / "config", "w") as f:
            f.write(
                "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
            )
        with open(workdir / root / "description", "w") as f:
            f.write("Unnamed pyvcs repository.\n")
    except OSError as e:
        raise OSError(f"Failed to write files: {e}") from e
    return pathlib.Path(workdir / root)
