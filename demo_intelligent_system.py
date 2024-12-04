from intelligent_memory import IntelligentMemoryManager
from datetime import datetime
import time

def demo_intelligent_system():
    # Initialize the system
    memory_manager = IntelligentMemoryManager()
    
    print("Demonstrating Intelligent Memory System\n")
    
    # Example 1: Adding technical information
    print("1. Adding technical information...")
    memory_manager.add_memory(
        "The project requires Python 3.8 and uses TensorFlow for deep learning models. "
        "GPU acceleration is recommended for better performance.",
        context="technical_requirements"
    )
    
    # Example 2: Adding user preference
    print("2. Adding user preference...")
    memory_manager.add_memory(
        "User prefers dark mode in IDE and uses VS Code as their primary development environment.",
        context="user_preferences"
    )
    
    # Example 3: Adding project deadline
    print("3. Adding critical project information...")
    memory_manager.add_memory(
        "Critical: Project deadline is March 15th, 2024. All features must be tested and documented by March 10th.",
        context="project_timeline"
    )
    
    # Example 4: Adding related technical information
    print("4. Adding related technical context...")
    memory_manager.add_memory(
        "The deep learning model should be optimized for GPU usage. Consider using TensorFlow's mixed precision training.",
        context="technical_requirements"
    )
    
    # Example 5: Adding less important information
    print("5. Adding background information...")
    memory_manager.add_memory(
        "Team usually has stand-up meetings at 10 AM PST.",
        context="team_practices"
    )
    
    # Demonstrate memory retrieval
    print("\nRetrieving relevant memories for 'GPU optimization'...")
    relevant_memories = memory_manager.get_relevant_memories("GPU optimization")
    print("\nRelevant memories:")
    for memory, relevance in relevant_memories:
        print(f"- [{relevance:.2f}] {memory.content}")
    
    # Analyze patterns
    print("\nAnalyzing memory patterns...")
    analysis = memory_manager.analyze_memory_patterns()
    
    print("\nMemory Analysis:")
    print("1. Importance Statistics:")
    for metric, value in analysis['importance_stats'].items():
        print(f"   - {metric}: {value:.2f}")
    
    print("\n2. Context Distribution:")
    for context, count in analysis['context_distribution'].items():
        print(f"   - {context}: {count}")
    
    print("\n3. Common Tags:")
    for tag, count in analysis['common_tags'].items():
        print(f"   - {tag}: {count}")

if __name__ == "__main__":
    demo_intelligent_system()
