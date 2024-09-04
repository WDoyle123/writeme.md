import os, subprocess
from os.path import exists

from autogen.code_utils import subprocess
from agent_functions.agents import main

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_code_files(starting_directory, file_extensions=None):
    if file_extensions is None:
        file_extensions = ['.py']
    for root, _, files in os.walk(starting_directory):
        for file in files:
            # Skip __init__.py files
            if file == "__init__.py" or not any(file.endswith(ext) for ext in file_extensions):
                continue
            yield os.path.join(root, file)

def read_file_in_chunks(file_path, chunk_size=4096):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

def analyse_code_chunk(file_path, chunk, openai_api_key, openai_model, max_retries=3):
    # Check if the filename is 'setup.py'
    if "setup.py" in file_path:
        prompt = (
            f"Filename: {file_path}\n\n"
            f"Analyse the following setup.py code segment. Focus specifically on gathering details about the codebase, "
            f"entry points, author information, package names, dependencies, and other configuration settings. "
            f"Provide concise notes on how each part contributes to the overall package setup. Here is the code chunk: \n{chunk}"
        )
    else:
        prompt = (
            f"Filename: {file_path}\n\n"
            f"Analyse the following code segment and provide concise notes on how it works and what it does. "
            f"Make sure to include the file name at the top! Here is the code chunk: \n{chunk}"
        )
    
    attempt = 0
    while attempt < max_retries:
        try:
            main(prompt, openai_api_key, openai_model)
            return  # If processing is successful, exit the function
        except Exception:
            if attempt < max_retries - 1:
                attempt += 1
            else:
                break

def extract_approved_notes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    delimiter = '----------------------------------------------------------------\n'
    blocks = content.split(delimiter)

    previous_block = None

    for block in blocks:
        if previous_block is not None and 'Project_Manager' in block and 'APPROVED' in block:
            if 'writer' in previous_block:
                note = previous_block + delimiter
                with open("groupchat.txt", 'a', encoding='utf-8') as file:
                    file.write(note + "\n\n")
                    logger.info(f"Approved notes written to groupchat.txt")
        
        previous_block = block 

def read_code(repo_path, openai_api_key, openai_model):
    code_files = list(list_code_files(repo_path))
    for file_path in code_files:
        logger.info(f"Reading file: {file_path}")
        try:
            for chunk in read_file_in_chunks(file_path):
                analyse_code_chunk(file_path, chunk, openai_api_key, openai_model)
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    file_output_name = "approved_notes.txt"
    file_output_path = os.path.join(os.getcwd(), file_output_name)

    extract_approved_notes(file_output_name)

def download_repo(repo_name):
    work_dir = 'work_dir'
    os.makedirs(work_dir, exist_ok=True)

    repo_path = os.path.join(work_dir, repo_name.split('/')[-1])
    repo_url = f'https://github.com/{repo_name}.git'

    try:
        result = subprocess.run(['git', 'clone', repo_url, repo_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(f"Repository '{repo_name}' has been cloned to '{repo_path}'.")
        
        if os.path.isdir(os.path.join(repo_path, '.git')):
            logger.info(f"Verification successful: '{repo_path}' contains a .git directory.")
            return repo_path

        else:
            logger.error(f"Verification failed: '{repo_path}' does not contain a .git directory.")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository '{repo_name}'. Error: {e.stderr}")


    return repo_path

