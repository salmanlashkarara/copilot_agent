import asyncio
from pathlib import Path

from src import instructions
from src.custom_agent import CustomAgent

# Set this to your Maven project root to generate files there
# Or leave None to use the default (current project root)
MAVEN_PROJECT_ROOT = r"C:\Users\lashksal\IdeaProjects\Api-Agent"


async def main() -> None:
    api_definition = await get_api_definition_path()
    agent = CustomAgent()

    sequential_instructions = [instructions.MODEL_INSTRUCTION,
                               instructions.RESOURCE_EXTRACTION_INSTRUCTIONS,
                               instructions.REST_ASSURED_REQUESTS_INSTRUCTIONS,
                               instructions.HELPER_METHODS_INSTRUCTIONS,
                               instructions.TEST_INSTRUCTIONS,
                               instructions.CLEAN_CODE_HELPERS_INSTRUCTIONS]

    for instruction in sequential_instructions:
        await agent.run_agent_with_instructions(
            str(api_definition),
            instruction,
            target_directory=MAVEN_PROJECT_ROOT)


async def get_api_definition_path():
    project_root = Path(__file__).resolve().parent
    api_definition = project_root / "resources" / "petstore.yaml"
    return api_definition


if __name__ == "__main__":
    asyncio.run(main())
