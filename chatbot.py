from memory_manager import MemoryManager
import time
from typing import List, Tuple

class MemoryEnabledChatbot:
    def __init__(self):
        self.memory_manager = MemoryManager(core_memory_size=5, recent_memory_size=10)
        self.conversation_history: List[Tuple[str, str]] = []
        
    def _extract_preferences(self, user_input: str) -> None:
        """Extract potential user preferences from input."""
        # Simple preference detection based on keywords
        if "i like" in user_input.lower() or "i prefer" in user_input.lower():
            self.memory_manager.add_memory(
                content=user_input,
                importance=0.85,
                context="user_preference"
            )
        
        # Detect technical interests
        tech_keywords = ["python", "javascript", "programming", "coding", "AI", "machine learning"]
        for keyword in tech_keywords:
            if keyword.lower() in user_input.lower():
                self.memory_manager.add_memory(
                    content=f"User showed interest in {keyword}",
                    importance=0.75,
                    context="technical_interests"
                )

    def _store_interaction(self, user_input: str, bot_response: str) -> None:
        """Store the interaction in recent memory."""
        self.conversation_history.append((user_input, bot_response))
        self.memory_manager.add_memory(
            content=f"User: {user_input} | Bot: {bot_response}",
            importance=0.6,
            context="conversation_history"
        )

    def _generate_response(self, user_input: str) -> str:
        """Generate a response based on user input and memories."""
        # Get relevant memories
        relevant_memories = self.memory_manager.get_relevant_memories(user_input)
        
        # Basic response generation logic
        if "hello" in user_input.lower() or "hi" in user_input.lower():
            return "Hello! How can I help you today?"
        
        elif "bye" in user_input.lower():
            return "Goodbye! It was nice talking to you!"
        
        elif "what do you remember" in user_input.lower():
            if relevant_memories:
                response = "Here's what I remember that's relevant:\n"
                for memory in relevant_memories:
                    response += f"- {memory.content}\n"
                return response
            return "I don't have any specific memories related to that yet."
        
        elif "preference" in user_input.lower() or "what do i like" in user_input.lower():
            preferences = [m for m in self.memory_manager.core_memories 
                         if m.context == "user_preference"]
            if preferences:
                response = "Based on our conversations, here are your preferences:\n"
                for pref in preferences:
                    response += f"- {pref.content}\n"
                return response
            return "I haven't learned any specific preferences from you yet."
        
        else:
            # Use relevant memories to enhance response
            if relevant_memories:
                memory_content = relevant_memories[0].content
                return f"Based on our previous interaction where {memory_content.lower()}, how can I help you with that?"
            
            return "I'm listening. Feel free to tell me more about your preferences or ask questions!"

    def chat(self):
        """Main chat loop."""
        print("Chatbot: Hello! I'm a memory-enabled chatbot. I can remember our conversations and your preferences.")
        print("         You can say 'bye' to end the conversation.")
        print("         Try asking 'what do you remember?' or telling me about your preferences!")
        print("\n")

        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'bye':
                print("Chatbot: Goodbye! I'll remember our conversation!")
                break

            # Extract and store preferences
            self._extract_preferences(user_input)
            
            # Generate response
            response = self._generate_response(user_input)
            
            # Store the interaction
            self._store_interaction(user_input, response)
            
            print("Chatbot:", response)
            print()

if __name__ == "__main__":
    chatbot = MemoryEnabledChatbot()
    chatbot.chat()
