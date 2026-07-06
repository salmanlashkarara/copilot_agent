from pathlib import Path

from copilot.tools import define_tool
from src.tool.WriteFileArgs import WriteFileArgs


class WriteFileArg:
    # Global workspace root that can be configured before session creation
    _WORKSPACE_ROOT: Path | None = None

    @classmethod
    def set_workspace_root(cls, path: str | Path) -> None:
        cls._WORKSPACE_ROOT = Path(path).resolve()

    @classmethod
    def get_workspace_root(cls) -> Path:
        if cls._WORKSPACE_ROOT is None:
            raise ValueError("Workspace root must be set before using write_file.")
        return cls._WORKSPACE_ROOT

    @classmethod
    def resolve_workspace_path(cls, raw_path: str) -> Path:
        # Parse the user-provided path and expand "~" to the user's home directory.
        path = Path(raw_path).expanduser()

        # If the path is relative, anchor it under the configured workspace root.
        if not path.is_absolute():
            path = cls.get_workspace_root() / path

        # Normalize the path (resolve "..", ".", and symlinks where possible).
        resolved_path = path.resolve()

        try:
            # Ensure the final path is inside the workspace root; this raises ValueError if not.
            resolved_path.relative_to(cls.get_workspace_root())
        except ValueError as exc:
            # Reject path traversal or absolute paths that escape the workspace boundary.
            raise PermissionError(
                f"Refusing to write outside the workspace root: {cls.get_workspace_root()}"
            ) from exc

        # Return the validated, absolute workspace-safe path.
        return resolved_path

    @staticmethod
    @define_tool(
        description="Write a UTF-8 text file under the workspace root. Use this to create generated source files.",
        skip_permission=True,
    )
    async def write_file(args: WriteFileArgs):
        path = WriteFileArg.resolve_workspace_path(args.path)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args.content, encoding="utf-8")

        return f"Wrote file: {path}"
