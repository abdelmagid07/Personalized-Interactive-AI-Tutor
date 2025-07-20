from dotenv import load_dotenv
import os
from openai import OpenAI
import tiktoken

# load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# set parameters for the OpenAI API
model = "gpt-4o"
temperature = 0.7
topic = ''
client = OpenAI(api_key=api_key)    

# Initial system message to set tutor behavior
conversation = [
    {
        "role": "system",
        "content":  "You are a highly knowledgeable, encouraging, and interactive personal tutor. "
        "Your goal is to teach the user about a topic they choose, breaking it down step by step using simple, clear explanations. "
        "After each step, ask the user a short, relevant question to check their understanding before continuing. "
        "Pause and wait for the user's response. If the user is unsure, patiently re-explain the concept in a different way. "
        "Always keep the tone supportive and curious, like a coach who wants the student to succeed. "
        "Avoid overwhelming detail—focus on clarity, engagement, and building intuition. "
        "Remain in tutor mode throughout the conversation."
        "Please avoid using LaTeX or markdown formatting. Use plain text for explanations and math (e.g., '3 * 4' instead of '3 \\cdot 4')."
    }
]

# Define the first topic to start the conversation
topic = input("\nWhat topic would you like to learn about? ")
conversation.append({"role": "user", "content": f"I want to learn about {topic}."})
response = client.responses.create(
    model=model,
    input=conversation,
    temperature=temperature,
)
print("\nTutor:", response.output_text)

# Start the conversation loop
while True:
    user_input = input("\nYou: ")
    conversation.append({"role": "user", "content": user_input})
    
    response = client.responses.create(
        model=model,
        input=conversation,
        temperature=temperature,
    )
    
    # Print the model's response
    print("\nTutor:", response.output_text)
    
    # Add the model's response to the conversation
    conversation.append({"role": "assistant", "content": response.output_text})
    
    # Ask for the next topic if the user wants to continue
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("\nTutor: Thank you for learning with me! Goodbye!")
        break


