from memory_manager import MemoryManager

def main():
    # Initialize the memory manager
    memory_manager = MemoryManager(core_memory_size=3, recent_memory_size=5)

    # Add some test memories
    print("Adding memories...")
    
    # Core memories (high importance)
    memory_manager.add_memory(
        "User prefers Python for data science projects",
        importance=0.9,
        context="project preferences"
    )
    memory_manager.add_memory(
        "User is working on a machine learning research paper",
        importance=0.85,
        context="current projects"
    )

    # Recent memories (medium importance)
    memory_manager.add_memory(
        "User asked about TensorFlow installation yesterday",
        importance=0.6,
        context="technical support"
    )
    memory_manager.add_memory(
        "Discussion about GPU optimization techniques",
        importance=0.7,
        context="performance"
    )

    # Print current memory state
    print("\nMemory State:")
    print(memory_manager.summarize_memory_state())

    # Demonstrate memory retrieval
    query = "python machine learning"
    relevant_memories = memory_manager.get_relevant_memories(query)
    
    print("\nRelevant memories for query:", query)
    for memory in relevant_memories:
        print(f"- [{memory.memory_type}] {memory.content} (importance: {memory.importance})")

if __name__ == "__main__":
    main()
