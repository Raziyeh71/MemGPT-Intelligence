from persistent_memory import PersistentMemoryManager
from datetime import datetime
from typing import List, Optional, Dict
import os

class PersistentAIAssistant:
    def __init__(self, name: str = "AI Assistant"):
        self.name = name
        self.memory_manager = PersistentMemoryManager()
        self.current_context: Optional[str] = None
        
    def start_session(self, context: Optional[str] = None):
        """Start a new session with optional context."""
        self.current_context = context
        session_start = f"Started new session at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if context:
            session_start += f" with context: {context}"
        
        self.memory_manager.add_memory(
            content=session_start,
            importance=0.7,
            context="session_management"
        )
        
        return self._generate_greeting()
    
    def _generate_greeting(self) -> str:
        """Generate a contextual greeting based on previous interactions."""
        recent_sessions = self.memory_manager.get_memories_by_context("session_management")
        
        if len(recent_sessions) > 1:
            last_session = recent_sessions[-2]  # -1 would be current session
            return f"Welcome back! I remember our last session on {datetime.fromtimestamp(last_session.timestamp).strftime('%Y-%m-%d')}. How can I assist you today?"
        
        return "Hello! I'm your AI assistant. I'll remember our conversation for future sessions. How can I help you?"
    
    def _extract_user_preferences(self, user_input: str):
        """Extract and store user preferences from input."""
        preference_indicators = ["i like", "i prefer", "i want", "i need", "i'm interested in"]
        
        for indicator in preference_indicators:
            if indicator in user_input.lower():
                self.memory_manager.add_memory(
                    content=user_input,
                    importance=0.85,
                    context="user_preference"
                )
                break
    
    def _handle_context_switch(self, user_input: str) -> Optional[str]:
        """Detect and handle context switches in conversation."""
        context_keywords = {
            "project": ["project", "work", "task"],
            "learning": ["learn", "study", "understand"],
            "technical": ["code", "programming", "development"],
            "personal": ["personal", "life", "hobby"]
        }
        
        for context, keywords in context_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                if self.current_context != context:
                    self.current_context = context
                    return f"I notice we're talking about {context} now. I'll keep that in mind."
        return None
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a contextual response."""
        # Extract preferences
        self._extract_user_preferences(user_input)
        
        # Check for context switch
        context_switch_msg = self._handle_context_switch(user_input)
        
        # Handle special commands
        if user_input.lower() == "show memory":
            return self._format_memory_summary()
        
        if user_input.lower() == "show preferences":
            return self._format_preferences()
        
        if user_input.lower() == "show context":
            return self._format_context_info()
        
        # Generate response based on context and memories
        response = self._generate_response(user_input)
        
        # Add conversation to memory
        self.memory_manager.add_memory(
            content=f"User: {user_input} | Assistant: {response}",
            importance=0.6,
            context=self.current_context or "general"
        )
        
        if context_switch_msg:
            response = f"{context_switch_msg}\n\n{response}"
        
        return response
    
    def _generate_response(self, user_input: str) -> str:
        """Generate a response based on context and relevant memories."""
        # Handle specific queries
        if user_input.lower() in ['show context', 'what is the context']:
            return self._format_context_info()
            
        if any(word in user_input.lower() for word in ['memory', 'remember', 'memories']):
            return self._format_memory_summary()
            
        if any(word in user_input.lower() for word in ['preference', 'like', 'prefer']):
            return self._format_preferences()

        if "help" in user_input.lower():
            return (
                "I can assist you with:\n"
                "1. Task Context: I keep track of what we're working on\n"
                "2. Memory Management: I remember our past conversations\n"
                "3. Preference Learning: I learn and remember your preferences\n"
                "\nUseful commands:\n"
                "- Ask about context: 'what is the context?'\n"
                "- Check memories: 'what do you remember?'\n"
                "- View preferences: 'what are my preferences?'\n"
                "- Start new context: 'let's talk about [topic]'"
            )

        # Check for context-specific queries
        if self.current_context:
            context_memories = self.memory_manager.get_memories_by_context(self.current_context)
            if context_memories:
                relevant_memory = context_memories[-1]  # Most recent memory in current context
                return f"In our current {self.current_context} context, we were discussing: {relevant_memory.content}"

        # Get relevant memories for general queries
        relevant_memories = self.memory_manager.get_relevant_memories(user_input)
        if relevant_memories:
            memory = relevant_memories[0]
            if 'User:' in memory.content:
                # Extract just the user's part from the memory
                user_part = memory.content.split('|')[0].replace('User:', '').strip()
                return f"I remember you mentioned {user_part}. Would you like to discuss that further?"
            return f"Based on our previous discussion about {memory.content}, how can I help you now?"

        return "I'm ready to help! Feel free to ask about specific topics or tell me what you'd like to work on."

    def _format_context_info(self) -> str:
        """Format information about current context."""
        if not self.current_context:
            return (
                "We're in a general conversation.\n"
                "You can start a specific context by saying something like:\n"
                "- 'Let's work on a project'\n"
                "- 'I want to learn about [topic]'\n"
                "- 'Let's discuss [technical/personal] matters'"
            )
        
        context_memories = self.memory_manager.get_memories_by_context(self.current_context)
        summary = f"Current Context: {self.current_context.upper()}\n\n"
        
        if context_memories:
            summary += "Recent discussion points:\n"
            for memory in context_memories[-3:]:  # Last 3 memories in this context
                if 'User:' in memory.content:
                    # Clean up the memory content for display
                    content = memory.content.split('|')[0].replace('User:', '').strip()
                    summary += f"- {content}\n"
                else:
                    summary += f"- {memory.content}\n"
        else:
            summary += f"We just started discussing {self.current_context}. What specific aspect would you like to explore?"
        
        return summary

    def _format_memory_summary(self) -> str:
        """Format a summary of stored memories."""
        recent_memories = self.memory_manager.get_session_memories()[-5:]  # Last 5 memories
        
        if not recent_memories:
            return "I don't have any memories stored yet. Let's create some by having a conversation!"
            
        summary = "Here are my recent memories of our interaction:\n\n"
        for memory in recent_memories:
            if 'User:' in memory.content:
                # Clean up the memory content for display
                content = memory.content.split('|')[0].replace('User:', '').strip()
                summary += f"- You told me: {content}\n"
            else:
                summary += f"- {memory.content}\n"
        
        return summary
    
    def _format_preferences(self) -> str:
        """Format stored user preferences."""
        preferences = self.memory_manager.get_memories_by_context("user_preference")
        
        if not preferences:
            return "I haven't stored any specific preferences yet. Feel free to tell me what you like or prefer!"
        
        summary = "Here are your stored preferences:\n\n"
        for pref in preferences:
            summary += f"- {pref.content}\n"
        
        return summary

def main():
    assistant = PersistentAIAssistant()
    print(assistant.start_session())
    print("\nCommands:")
    print("- 'show memory': See what I remember")
    print("- 'show preferences': See stored preferences")
    print("- 'show context': See current context")
    print("- 'exit': End the session")
    print("\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                print("\nAssistant: Goodbye! I'll remember our conversation for next time!")
                break
            
            response = assistant.process_input(user_input)
            print(f"\nAssistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\nAssistant: Session ended. I'll remember our conversation!")
            break
        except Exception as e:
            print(f"\nAssistant: I encountered an error: {str(e)}")
            print("Let's continue our conversation!")

if __name__ == "__main__":
    main()
