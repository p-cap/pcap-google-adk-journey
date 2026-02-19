from google.adk.agents import Agent
import google.genai as genai
from dotenv import load_dotenv
from google import genai
import os

# 1. Load the variables from the .env file into the system environment
load_dotenv()

# 2. Retrieve the specific key using os.getenv
api_key = os.getenv("GEMINI_API_KEY")

# 3. Use it to initialize your Gemini Client
client = genai.Client(api_key=api_key)


s_instructions = 'You are pcap. Always introduce yourself. Your primary goal is to help users manage their context window. Whenever a user provides a prompt or asks about token usage, you must use the get_token_count_from_prompt tool to provide an accurate number. Do not estimate; always use your tool.'

def get_info(info: str) -> dict:
    """
    Gets generic info about this agent
    """
    if info:
        return {
            'status': 'success',
            'report' : 'I am the pcap agent'
        }
    else:
        return {
            'status' : 'error',
            'error_message': f'Your message, {info}, caused an issue'
        }


def get_token_count_from_prompt(prompt: str) -> dict:
    """
    Calculates the number of tokens in a given prompt string.
    
    Args:
        prompt: The text to be tokenized and counted.
    """
    try:
        # New syntax: client.models.count_tokens
        response = client.models.count_tokens(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        return {
            "total_tokens": response.total_tokens,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

root_agent = Agent(
    name='pcap_agent',
    model='gemini-2.0-flash',
    description=(
    "An expert utility agent named 'pcap' that specializes in tokenomics and context window analysis. "
    "It calculates precise token counts for user prompts and provides insights into how much of the "
    "model's context window is being utilized."
    ),
    instruction=(
        f'{s_instructions}'
    ),
    tools = [get_info,get_token_count_from_prompt]
)

