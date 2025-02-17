import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv(override=True)

groq_api_key = os.getenv('GROQ_API_KEY')
mistral_api_key = os.getenv('MISTRAL_API_KEY')

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:8]}")
else:
    print("Groq API Key not set")

if mistral_api_key:
    print(f"Mistral API Key exists and begins {mistral_api_key[:8]}")
else:
    print("Mistral API Key not set")

# Initialize Mistral client
mistral = OpenAI(
    api_key=mistral_api_key,
    base_url="https://api.mistral.ai/v1"
)

# Initialize Groq client
groq = OpenAI(
    api_key=groq_api_key, 
    base_url="https://api.groq.com/openai/v1"
)

mistral_model = "mistral-large-latest"
groq_model = "deepseek-r1-distill-llama-70b"

mistral_system = """You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way. \
Format your responses using Markdown syntax. Use appropriate markdown elements like **bold**, *italic*, \
lists, quotes, and code blocks where relevant to make your argumentative responses more expressive."""

groq_system = """You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting. Format your responses using Markdown syntax. \
Use appropriate markdown elements like **bold**, *italic*, lists, quotes, and code blocks \
where relevant to make your polite responses more engaging."""

mistral_messages = ["Hi there"]
groq_messages = ["Hi"]

def format_think_tags(message):
    """Convert <think> tags to markdown format"""
    if "<think>" in message and "</think>" in message:
        try:
            # Extract content between think tags
            start_idx = message.find("<think>") + len("<think>")
            end_idx = message.find("</think>")
            
            if start_idx >= 0 and end_idx >= 0:
                thought_content = message[start_idx:end_idx].strip()
                # Get everything after </think> tag
                response_content = message[end_idx + len("</think>"):].strip()
                
                # Replace newlines in thought content with quoted newlines
                quoted_thought = thought_content.replace("\n", "\n> ")
                
                # Format into markdown with better readability using separate strings
                formatted_parts = [
                    "",  # Initial newline
                    "<details>",
                    "<summary>🤔 Thought Process</summary>",
                    "",
                    "> **Analysis:**",
                    f"> {quoted_thought}",
                    "",
                    "</details>",
                    "",
                    "### Response:",
                    response_content,
                    ""
                ]
                
                # Join all parts with newlines
                formatted_message = "\n".join(formatted_parts)
                return formatted_message
        except Exception as e:
            print(f"Warning: Error formatting think tags: {e}")
            return message
    return message

def format_message(role, message, turn):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Apply think tag formatting for DeepSeek messages
    if role == "DeepSeek":
        message = format_think_tags(message)
    
    formatted_message = f"""
### Turn {turn} - {role} ({timestamp})

{message}

---"""
    return formatted_message

def save_conversation(filename="chat.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Conversation between Mistral and DeepSeek\n\n")
        f.write("> This is an AI conversation between two models with different personalities:\n")
        f.write("> - Mistral: An argumentative and snarky chatbot\n")
        f.write("> - DeepSeek: A polite and courteous chatbot that shows its thought process\n\n")
        f.write("## System Instructions\n\n")
        f.write(f"### Mistral's Role\n{mistral_system}\n\n")
        f.write(f"### DeepSeek's Role\n{groq_system}\n\n")
        f.write("## Conversation\n\n")
        
        for turn, (mistral_msg, groq_msg) in enumerate(zip(mistral_messages, groq_messages), 1):
            f.write(format_message("Mistral", mistral_msg, turn))
            f.write(format_message("DeepSeek", groq_msg, turn))

def call_mistral():
    messages = [{"role": "system", "content": mistral_system}]
    for mistral_msg, groq_msg in zip(mistral_messages, groq_messages):
        messages.append({"role": "assistant", "content": mistral_msg})
        messages.append({"role": "user", "content": groq_msg})
    completion = mistral.chat.completions.create(
        model=mistral_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_groq():
    messages = [{"role": "system", "content": groq_system}]
    for mistral_msg, groq_msg in zip(mistral_messages, groq_messages):
        messages.append({"role": "user", "content": mistral_msg})
        messages.append({"role": "assistant", "content": groq_msg})
    messages.append({"role": "user", "content": mistral_messages[-1]})

    completion = groq.chat.completions.create(
        model=groq_model,
        messages=messages
    )
    response = completion.choices[0].message.content
    return response

def main():
    print("Starting conversation...\n")
    print("Saving conversation to chat.md\n")
    
    for i in range(5):
        mistral_msg = call_mistral()
        mistral_messages.append(mistral_msg)
        formatted_mistral = format_message("Mistral", mistral_msg, i+1)
        print(formatted_mistral)
        
        groq_msg = call_groq()
        groq_messages.append(groq_msg)
        formatted_groq = format_message("DeepSeek", groq_msg, i+1)
        print(formatted_groq)
        
        # Save after each turn
        save_conversation()

if __name__ == "__main__":
    main()