from pydantic import BaseModel, Field


class WriteFileArgs(BaseModel):
    path: str = Field(
        description="Absolute path, or a path relative to the workspace root, for the file to write."
    )
    content: str = Field(description="The complete UTF-8 file contents to write.")
