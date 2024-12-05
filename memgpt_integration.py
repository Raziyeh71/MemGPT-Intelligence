import os
from typing import List, Dict, Optional
import json
from datetime import datetime
import openai
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

openai.api_key = api_key

class MemoryEnhancedAssistant:
    def __init__(self, 
                 model: str = "gpt-4",
                 storage_dir: str = "memory_storage",
                 memory_window: int = 10):
        """
        Initialize memory-enhanced assistant
        
        Args:
            model: Model to use (e.g., "gpt-4", "gpt-3.5-turbo")
            storage_dir: Directory for storing persistent data
            memory_window: Number of recent conversations to keep in context
        """
        self.model = model
        self.storage_dir = storage_dir
        self.memory_window = memory_window
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize conversation history
        self.conversation_history = []
        
        # System message that includes memory management capabilities
        self.system_message = """You are a helpful AI assistant with memory capabilities. You can:
1. Remember previous conversations within your context window
2. Reference past interactions when relevant
3. Build upon previous context to provide more personalized responses
4. Maintain conversation continuity

When appropriate, refer back to previous interactions to provide more context-aware responses."""
        
    def _format_messages(self, new_message: str) -> List[Dict[str, str]]:
        """Format messages for the API call"""
        messages = [{"role": "system", "content": self.system_message}]
        
        # Add recent conversation history
        start_idx = max(0, len(self.conversation_history) - self.memory_window)
        for entry in self.conversation_history[start_idx:]:
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["assistant"]})
        
        # Add new message
        messages.append({"role": "user", "content": new_message})
        return messages
        
    def send_message(self, message: str) -> str:
        """
        Send a message to the assistant and get response
        
        Args:
            message: User message
            
        Returns:
            Assistant's response
        """
        # Prepare messages with context
        messages = self._format_messages(message)
        
        # Get response from OpenAI
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        # Extract response text
        response_text = response.choices[0].message.content
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": message,
            "assistant": response_text
        })
        
        return response_text
    
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

def demo_assistant():
    """Demonstrate memory-enhanced assistant capabilities"""
    
    # Initialize assistant
    print("Initializing memory-enhanced assistant...")
    assistant = MemoryEnhancedAssistant(
        model="gpt-4",
        storage_dir="memory_demo_storage",
        memory_window=10
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
    demo_assistant()
