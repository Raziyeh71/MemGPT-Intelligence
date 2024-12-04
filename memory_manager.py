from dataclasses import dataclass
from typing import List, Dict, Optional
import time

@dataclass
class Memory:
    content: str
    timestamp: float
    importance: float
    context: str
    memory_type: str  # 'core', 'recent', 'archival'

class MemoryManager:
    def __init__(self, core_memory_size: int = 5, recent_memory_size: int = 10):
        self.core_memories: List[Memory] = []
        self.recent_memories: List[Memory] = []
        self.archival_memories: List[Memory] = []
        self.core_memory_size = core_memory_size
        self.recent_memory_size = recent_memory_size

    def add_memory(self, content: str, importance: float, context: str) -> Memory:
        """Add a new memory to the appropriate storage based on importance."""
        memory = Memory(
            content=content,
            timestamp=time.time(),
            importance=importance,
            context=context,
            memory_type='recent'
        )

        if importance >= 0.8:  # High importance memories go to core
            if len(self.core_memories) >= self.core_memory_size:
                # Move least important core memory to recent
                least_important = min(self.core_memories, key=lambda x: x.importance)
                self.core_memories.remove(least_important)
                least_important.memory_type = 'recent'
                self._add_to_recent(least_important)
            
            memory.memory_type = 'core'
            self.core_memories.append(memory)
        else:
            self._add_to_recent(memory)

        return memory

    def _add_to_recent(self, memory: Memory):
        """Add memory to recent storage, moving older ones to archival if needed."""
        self.recent_memories.append(memory)
        if len(self.recent_memories) > self.recent_memory_size:
            oldest = self.recent_memories.pop(0)
            oldest.memory_type = 'archival'
            self.archival_memories.append(oldest)

    def get_relevant_memories(self, query: str, top_k: int = 3) -> List[Memory]:
        """Simple relevance-based memory retrieval (in a real implementation, this would use embeddings)."""
        all_memories = self.core_memories + self.recent_memories + self.archival_memories
        # Simple keyword matching (in practice, use proper embedding similarity)
        scored_memories = [
            (memory, len(set(query.lower().split()) & set(memory.content.lower().split())))
            for memory in all_memories
        ]
        scored_memories.sort(key=lambda x: (-x[1], -x[0].importance))
        return [memory for memory, _ in scored_memories[:top_k]]

    def summarize_memory_state(self) -> Dict[str, int]:
        """Return a summary of the current memory state."""
        return {
            'core_memories': len(self.core_memories),
            'recent_memories': len(self.recent_memories),
            'archival_memories': len(self.archival_memories)
        }
