from google.adk.agents import Agent
import google.generativeai as genai

s_instructions = 'You are the p-cap agent that states its name and calculate the context window for a given prompt'

def get_info(info: str) -> dict:
    """
    Gets generic info about this agent
    """
    if info:
        return {
            'status': 'success',
            'report' : {
                'I am the pcap agent'
            }
        }
    else:
        return {
            'status' : 'error',
            'error_message': {
                f'Your message, {info}, caused an issue'
            }
        }


def get_context_stats(prompt_text: str, system_instruction: str):
    model_name ='gemini-2.0-flash'
    model = genai.GenerativeModel(model_name)
    full_content = prompt_text
    if system_instruction:
        full_content = system_instruction + prompt_text
    stats = model.count_token(full_content)
    return {
        'token_count': stats.total_tokens,
        'character_count': len(full_content)
    }
    

root_agent = Agent(
    name='pcap_agent',
    model='gemini-2.0-flash',
    description=(
        'Agent to tell user its name.'
    ),
    instruction=(
        f'{s_instructions}'
    ),
    tools = [get_info, get_context_stats]
)

