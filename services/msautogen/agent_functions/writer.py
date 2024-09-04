from agent_functions.agents import agent_write_readme
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_readme(file_path, repo_name, openai_api_key, openai_model):
    output_file_name = "readme.md"
    readme_template = f"""
# {repo_name} 

## Description

*This is what the code is*

## Setup

*Code to setup*

## Usage

*How to use the code*
"""
    if not os.path.isfile(output_file_name):
        with open(output_file_name, 'w') as file:
            file.write(readme_template)

    with open(file_path, "r", encoding="utf-8") as notes_file:
        notes_content = notes_file.read()

    # Create the prompt with all the notes content included
    prompt = f"Update the provided README.md template using only markdown and the detailed notes. Fill in the 'Description', 'Setup', and 'Usage' sections appropriately based on the notes. It is crucial for setup that you follow the setup.py and look into its entrypoints and details. Use headers, bullet points, and code blocks for clear formatting. Provide all necessary information succinctly. Here is the README.md template to update:\n\n{readme_template}\n--------------\nNotes:\n{notes_content}"

    agent_write_readme(prompt, output_file_name, openai_api_key, openai_model)

    with open(output_file_name, 'r', encoding='utf-8') as file:
        text = file.read()

    # Locate the position of the final occurrence of repo_name in the text
    repo_name_pos = text.rfind(f"# {repo_name}")

    if repo_name_pos == -1:
        return text.strip()

    # Extract content starting from the final occurrence of repo_name
    content = text[repo_name_pos:].strip()

    # Remove the admin part at the bottom if it exists
    admin_pattern = re.compile(
        r"--------------------------------------------------------------------------------\s*"
        r"Admin \(to chat_manager\):\s*"
        r"--------------------------------------------------------------------------------",
        re.DOTALL
    )

    admin_match = admin_pattern.search(content)

    if admin_match:
        content = content[:admin_match.start()].strip()

    lines = content.splitlines()

    # Remove the last line
    content = "\n".join(lines[:-1])

    return content
