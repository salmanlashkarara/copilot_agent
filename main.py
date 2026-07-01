import asyncio
from pathlib import Path

from src.custom_agent import CustomAgent
from src import instructions

# Set this to your Maven project root to generate files there
# Or leave None to use the default (current project root)
MAVEN_PROJECT_ROOT = r"C:\Users\lashksal\IdeaProjects\Api-Agent"


def collect_instruction_constants() -> list[tuple[str, str]]:
	instruction_items: list[tuple[str, str]] = []

	execution_order = [
		"MODEL_INSTRUCTION",
		"RESOURCE_EXTRACTION_INSTRUCTIONS",
		"REST_ASSURED_REQUESTS_INSTRUCTIONS",
		"HELPER_METHODS_INSTRUCTIONS",
		"TEST_INSTRUCTIONS",
		"CLEAN_CODE_HELPERS_INSTRUCTIONS",
	]

	order_index = {name: index for index, name in enumerate(execution_order)}

	for name, value in vars(instructions).items():
		if not name.isupper():
			continue
		if not isinstance(value, str):
			continue
		if not (name.endswith("_INSTRUCTION") or name.endswith("_INSTRUCTIONS")):
			continue

		instruction_items.append((name, value))

	def sort_key(item: tuple[str, str]) -> tuple[int, str]:
		name, _ = item
		return (order_index.get(name, len(execution_order)), name)

	return sorted(instruction_items, key=sort_key)


async def main() -> None:
	project_root = Path(__file__).resolve().parent
	api_definition = project_root / "resources" / "petstore.yaml"
	agent = CustomAgent()

	for instruction_name, instruction_text in collect_instruction_constants():
		print(f"\n===== Running {instruction_name} =====")
		await agent.run_agent_with_instructions(
			str(api_definition),
			instruction_text,
			target_directory=MAVEN_PROJECT_ROOT,
		)


if __name__ == "__main__":
	asyncio.run(main())
