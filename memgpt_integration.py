import os
from typing import List, Dict, Optional
import json
from datetime import datetime
from memgpt.client import MemGPTClient
from memgpt.constants import DEFAULT_HUMAN
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Check for API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    print("Please ensure you have a .env file with your API key")
    sys.exit(1)

os.environ["OPENAI_API_KEY"] = api_key

class MemGPTEnhancedAssistant:
    def __init__(self, 
                 model: str = "gpt-4",
                 storage_dir: str = "memgpt_storage"):
        """
        Initialize MemGPT-enhanced assistant
        
        Args:
            model: Model to use (e.g., "gpt-4", "gpt-3.5-turbo")
            storage_dir: Directory for storing persistent data
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize client
        self.client = MemGPTClient()
        
        # Create agent
        self.agent = self.client.create_agent(
            name="assistant",
            model=model,
            human=DEFAULT_HUMAN,
            persona="You are a helpful AI assistant with persistent memory."
        )
        
        # Initialize conversation history
        self.conversation_history = []
        
    def send_message(self, message: str) -> str:
        """
        Send a message to the MemGPT agent and get response
        
        Args:
            message: User message
            
        Returns:
            Agent's response
        """
        # Send message and get response
        response = self.client.user_message(self.agent.id, message)
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": message,
            "assistant": response
        })
        
        return response
    
    def save_conversation(self):
        """Save conversation history"""
        history_file = os.path.join(self.storage_dir, "conversation_history.json")
        with open(history_file, "w") as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def load_conversation(self):
        """Load conversation history"""
        history_file = os.path.join(self.storage_dir, "conversation_history.json")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                self.conversation_history = json.load(f)

def demo_memgpt_assistant():
    """Demonstrate MemGPT-enhanced assistant capabilities"""
    
    # Initialize assistant
    print("Initializing MemGPT-enhanced assistant...")
    assistant = MemGPTEnhancedAssistant(
        model="gpt-4",
        storage_dir="memgpt_demo_storage"
    )
    
    print("\nAssistant is ready! You can start chatting.")
    print("Type 'exit' to end the conversation.")
    print("Type 'save' to save the current state.")
    print("Type 'load' to load the previous state.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("\nSaving conversation...")
                assistant.save_conversation()
                print("Goodbye!")
                break
                
            elif user_input.lower() == 'save':
                assistant.save_conversation()
                print("\nConversation saved successfully!")
                continue
                
            elif user_input.lower() == 'load':
                assistant.load_conversation()
                print("\nPrevious conversation loaded successfully!")
                continue
            
            # Get response from assistant
            response = assistant.send_message(user_input)
            print("\nAssistant:", response)
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit.")

if __name__ == "__main__":
    demo_memgpt_assistant()
