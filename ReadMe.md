# Github-Copilot-Agent

This project uses the **GitHub Copilot SDK for Python** to run an automated Copilot session that reads an OpenAPI file (
`resources/petstore.yaml`) and generates Java test/code artifacts into a target Maven project folder.

## What is `github-copilot-cli`?

**GitHub Copilot CLI** is the command-line Copilot experience (interactive terminal assistant). It helps developers run
prompts, edit code, and use tools from a terminal workflow. In this project we need it for login into the Github
account, so we can use the subscirtion.

## What is `github-copilot-sdk`?

GitHub Copilot SDK is a developer toolkit that lets you embed the GitHub Copilot AI agent into your own applications or
services. Instead of building an AI coding agent from scratch, you can use the SDK to access Copilot's capabilities
programmatically. In this project, the SDK is the core integration used by code:

- `src/custom_agent.py` creates a `CopilotClient`, then creates a session with custom tools.
- `src/tool/WriteFileArg.py` defines the custom `write_file` tool exposed to the model.
- `main.py` orchestrates instruction phases and runs the agent end-to-end.

## How they are used together here
1. Use Github sdk to login into your Github account and get the access token.
2. Install the necessary dependencies (see `requirements.txt`).
3. Create a maven project folder (e.g. `target-maven-project`) and add a `pom.xml` file.
4. Specify the target Maven project path in `main.py` (variable `MAVEN_PROJECT_ROOT`).
5. Run `python main.py` to start the agent session. The agent will read the OpenAPI file and generate Java code into the target Maven project folder.
Alternatively, you can run `main_constant_commiunication.py` to use a constant prompt instead of reading the OpenAPI file.
## Quick run

1. Set `MAVEN_PROJECT_ROOT` in `main.py` to your target Java/Maven project path.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run:
   `python main.py`