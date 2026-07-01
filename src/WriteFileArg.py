from pathlib import Path

from copilot.tools import define_tool
from pydantic import BaseModel, Field


# Global workspace root that can be configured before session creation
_WORKSPACE_ROOT: Path | None = None


def set_workspace_root(path: str | Path) -> None:
    """Set the workspace root for file writes."""
    global _WORKSPACE_ROOT
    _WORKSPACE_ROOT = Path(path).resolve()


def get_workspace_root() -> Path:
    """Get the current workspace root, defaulting to the project directory."""
    global _WORKSPACE_ROOT
    if _WORKSPACE_ROOT is None:
        _WORKSPACE_ROOT = Path(__file__).resolve().parent
    return _WORKSPACE_ROOT


class WriteFileArgs(BaseModel):
    path: str = Field(
        description="Absolute path, or a path relative to the workspace root, for the file to write."
    )
    content: str = Field(description="The complete UTF-8 file contents to write.")


def resolve_workspace_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser()

    if not path.is_absolute():
        path = get_workspace_root() / path

    resolved_path = path.resolve()

    try:
        resolved_path.relative_to(get_workspace_root())
    except ValueError as exc:
        raise PermissionError(
            f"Refusing to write outside the workspace root: {get_workspace_root()}"
        ) from exc

    return resolved_path


@define_tool(
    description="Write a UTF-8 text file under the workspace root. Use this to create generated source files.",
    skip_permission=True,
)
async def write_file(args: WriteFileArgs):
    path = resolve_workspace_path(args.path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(args.content, encoding="utf-8")

    return f"Wrote file: {path}"
