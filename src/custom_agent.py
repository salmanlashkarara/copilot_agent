from pathlib import Path

from copilot import CopilotClient

from src.tool.write_file_service import WriteFileService


class CustomAgent:
    async def run_agent_with_instructions(
            self,
            openapi_file_path: str,
            instruction: str,
            target_directory: str | None = None,
    ) -> None:
        if target_directory is None:
            workspace_root = Path(__file__).resolve().parent
        else:
            workspace_root = Path(target_directory).resolve()

        WriteFileService.set_workspace_root(workspace_root)
        prompt = self.build_instructions(openapi_file_path, instruction, workspace_root)

        client = CopilotClient(working_directory=str(workspace_root))

        try:
            await client.start()
            session = await client.create_session(
                tools=[WriteFileService.write_file],
                working_directory=str(workspace_root),
            )

            response = await session.send_and_wait(prompt, timeout=600.0)

            if response is None:
                print("The session completed without a final assistant message.")
                return

            print(response.data.content)

        finally:
            await client.stop()

    def build_instructions(
            self,
            openapi_file_path: str,
            instruction: str,
            workspace_root: Path,
    ) -> str:
        openapi_path = Path(openapi_file_path).resolve()

        if not openapi_path.exists():
            raise FileNotFoundError(f"OpenAPI file not found: {openapi_file_path}")

        openapi_content = openapi_path.read_text(encoding="utf-8")

        return (
                instruction.strip()
                + "\n\nExecution rules:\n"
                + "- Create files on disk by calling the write_file tool.\n"
                + "- Do not only paste generated code in the chat response.\n"
                + f"- Workspace root: {workspace_root.as_posix()}\n"
                + "- Write files only under that workspace root.\n"
                + "- You may pass file paths relative to the workspace root, for example: src/main/java/org/example/models/Pet.java\n"
                + "- Each write_file call must contain the full contents of the file to create.\n"
                + "\n\nOpenAPI specification:\n```yaml\n"
                + openapi_content
                + "\n```"
        )
