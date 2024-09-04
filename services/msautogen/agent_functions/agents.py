import os
import sys
import autogen

def llm_config(openai_api_key, openai_model):
    llm_config = {
        "temperature": 0,
        "config_list": [
            {
                "model": openai_model,
                "api_key": openai_api_key,

            }
        ],
    }

    return llm_config

def is_termination_msg(content):
    have_content = content.get("content", None) is not None
    if have_content and "APPROVED" in content["content"]:
        return True
    return False

def main(prompt, openai_api_key, openai_model):

    COMPLETION_PROMPT = "If everything looks good, respond with APPROVED"

    USER_PROXY_PROMPT = ( "A human admin. Interact with the Project Manager to discuss the plan. Plan execution needs to be approved by this admin."
    )
    CRITIC = (
        "Critic, your mission is pivotal: scrutinize the writer's notes with a discerning eye. Your goal is to elevate the quality of their observations. Challenge them to enhance clarity, strength, and precision in their note-taking. Encourage concise yet profound insights, pushing for a level of excellence that transcends the ordinary. Your feedback should inspire the writer towards crafting notes that are not only informative but exemplary. Remeber that these notes will need to be able to fully describe the details and intricacies of the codebase."
    )
    WRITER = (
        "Writer, your critical assignment is to distill the essence of the code, honing in on its core functionalities, with a specific focus on describing important functions by name. Your notes should be brief and precise, highlighting the role and mechanics of key functions while omitting import statements and extraneous details. Present your findings in plain text, taking into account feedback from the Critic and the Project Manager. Avoid expressions of communication; present your analysis in a code block. Your descriptions must be concise, not exceeding 100 words, to ensure each word contributes to a clear and focused elucidation of the code's primary functions. Make sure to include relevant details and well explained code snippets that could be helpful to outline the functionaliy of the code. It is crucial you include code snippets that allow the uses to use the software in the codebase."
    )
    PROJECT_MANAGER_PROMPT = (
        "Project Manager, as the final arbiter, your responsibility is paramount. It is imperative that you meticulously review and validate the response for its precision and completeness. Conclude your assessment with a definitive 'APPROVED' if the submission meets the standards or 'DENIED, Try again' if it falls short, it is important that you exercise using 'DENIED, Try again' as this achieves a stronger answer! This stringent protocol is essential for the integrity and finality of the project documentation. Your strict compliance is mandatory. Ensure your response augments the writer's input, reflecting a consolidated judgment." + COMPLETION_PROMPT)

    # admin user proxy agent - takes in the prompt and manages the group chat
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # critic agent - suggests better ouput from the writer
    critic = autogen.AssistantAgent(
        name="critic",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=CRITIC,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # writer agent - write an analysis of the code
    writer = autogen.AssistantAgent(
        name="writer",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=WRITER,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # product manager - validate the response to make sure it's correct
    project_manager = autogen.AssistantAgent(
        name="Project_Manager",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=PROJECT_MANAGER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # create a group chat and initiate the chat.
    groupchat = autogen.GroupChat(
        agents=[user_proxy, critic, writer, project_manager],
        messages=[],
        max_round=4,
    )
    
    with RedirectOutputToFile('approved_notes.txt'):
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config(openai_api_key, openai_model))
        user_proxy.initiate_chat(manager, clear_history=True, message=prompt)

def agent_write_readme(prompt, file_path, openai_api_key, openai_model):

    COMPLETION_PROMPT = "If everything looks good, respond with APPROVED"

    USER_PROXY_PROMPT = (
        "A human admin. Interact with the Project Manager to discuss the plan. Plan execution needs to be approved by this admin."
    )
    CRITIC = (
        "Critic, your mission is pivotal: scrutinize the writer's readme draft with a discerning eye. Your goal is to elevate the quality of their observations. Challenge them to enhance clarity, strength, and precision in their note-taking. Encourage concise yet profound insights, pushing for a level of excellence that transcends the ordinary. Your feedback should inspire the writer towards crafting notes that are not only informative but exemplary."
    )
    WRITER = (
        "Writer. Your job is to turn the given notes into a readme.md for a github repo. Therefore, you should create a section on installation and provide a description on the funcitonallity of the codebase. Also provide a sections to discuss the technologies used. You MUST provide your output as a full readme.md enclosed in a codeblock."
    )
    PROJECT_MANAGER_PROMPT = (
        "Project Manager, as the final arbiter, your responsibility is paramount. It is imperative that you meticulously review and validate the response for its precision and completeness. Conclude your assessment with a definitive 'APPROVED' if the submission meets the standards or 'DENIED, Try again' if it falls short, it is important that you exercise using 'DENIED, Try again' as this achieves a stronger answer! This stringent protocol is essential for the integrity and finality of the project documentation. Your strict compliance is mandatory. Ensure your response augments the writer's input, reflecting a consolidated judgment." + COMPLETION_PROMPT)

    # admin user proxy agent - takes in the prompt and manages the group chat
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # critic agent - suggests better ouput from the writer
    critic = autogen.AssistantAgent(
        name="critic",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=CRITIC,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # writer agent - write an analysis of the code
    writer = autogen.AssistantAgent(
        name="writer",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=WRITER,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # product manager - validate the response to make sure it's correct
    project_manager = autogen.AssistantAgent(
        name="Project_Manager",
        llm_config=llm_config(openai_api_key, openai_model),
        system_message=PROJECT_MANAGER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_msg,
    )

    # create a group chat and initiate the chat.
    groupchat = autogen.GroupChat(
        agents=[user_proxy, writer],
        messages=[],
        max_round=3,
    )
    
    with RedirectOutputToFile(file_path):
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config(openai_api_key, openai_model))
        user_proxy.initiate_chat(manager, clear_history=True, message=prompt)

class RedirectOutputToFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def __enter__(self):
        self.file = open(self.filepath, 'a', encoding='utf-8')  
        sys.stdout = self.file
        sys.stderr = open(os.devnull, 'w')  
        print(f"Redirecting output to {self.filepath}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            sys.stdout = self.original_stdout  
            sys.stderr.close()  
            sys.stderr = self.original_stderr  
        finally:
            self.file.close() 
            print(f"Output redirection to {self.filepath} ended")
