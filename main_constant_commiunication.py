import asyncio
from pathlib import Path

from copilot import CopilotClient
from src import instructions
from src.custom_agent import CustomAgent
from src.tool.write_file_service import WriteFileService

END_SESSION = "/end_session"

# Set this to your Maven project root to generate files there
# Or leave None to use the default (current project root)
MAVEN_PROJECT_ROOT = r"C:\Users\lashksal\IdeaProjects\Api-Agent"


async def main() -> None:
    api_definition = await get_api_definition_path()
    agent = CustomAgent()
    workspace_root = resolve_workspace_root()

    WriteFileService.set_workspace_root(workspace_root)
    client = CopilotClient(working_directory=str(workspace_root))

    sequential_instructions = [instructions.MODEL_INSTRUCTION,
                               instructions.RESOURCE_EXTRACTION_INSTRUCTIONS,
                               instructions.REST_ASSURED_REQUESTS_INSTRUCTIONS,
                               instructions.HELPER_METHODS_INSTRUCTIONS,
                               instructions.TEST_INSTRUCTIONS,
                               instructions.CLEAN_CODE_HELPERS_INSTRUCTIONS]

    try:
        await client.start()
        session = await client.create_session(
            tools=[WriteFileService.write_file],
            working_directory=str(workspace_root),
        )

        for instruction in sequential_instructions:
            prompt = agent.build_instructions(str(api_definition), instruction, workspace_root)
            response = await session.send_and_wait(prompt, timeout=600.0)

            print(response.data.content)

        print("\nInteractive mode started. Type /end_session to stop.")
        while True:
            user_input = (await asyncio.to_thread(input, "You: ")).strip()
            if user_input == END_SESSION:
                print("Ending session.")
                break

            if not user_input:
                continue

            response = await session.send_and_wait(user_input, timeout=600.0)

            if response is None:
                print("The session completed without a final assistant message.")
                continue

            print(f"Agent: {response.data.content}")
    finally:
        await client.stop()


def resolve_workspace_root() -> Path:
    if MAVEN_PROJECT_ROOT is None:
        return Path(__file__).resolve().parent
    return Path(MAVEN_PROJECT_ROOT).resolve()


async def get_api_definition_path() -> Path:
    project_root = Path(__file__).resolve().parent
    api_definition = project_root / "resources" / "petstore.yaml"
    return api_definition


if __name__ == "__main__":
    asyncio.run(main())
