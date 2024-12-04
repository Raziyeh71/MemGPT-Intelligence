import json
import os
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class PersistentMemory:
    content: str
    timestamp: float
    importance: float
    context: str
    memory_type: str
    session_id: str
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class PersistentMemoryManager:
    def __init__(self, storage_dir: str = "memory_storage"):
        self.storage_dir = storage_dir
        self.core_memories: List[PersistentMemory] = []
        self.recent_memories: List[PersistentMemory] = []
        self.archival_memories: List[PersistentMemory] = []
        self.current_session_id: str = self._generate_session_id()
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        self.load_memories()
    
    def _generate_session_id(self) -> str:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_memory(self, content: str, importance: float, context: str) -> PersistentMemory:
        memory = PersistentMemory(
            content=content,
            timestamp=datetime.now().timestamp(),
            importance=importance,
            context=context,
            memory_type='recent',
            session_id=self.current_session_id
        )
        
        if importance >= 0.8:
            memory.memory_type = 'core'
            self.core_memories.append(memory)
        else:
            self.recent_memories.append(memory)
            
            # Move older memories to archival
            if len(self.recent_memories) > 10:
                old_memory = self.recent_memories.pop(0)
                old_memory.memory_type = 'archival'
                self.archival_memories.append(old_memory)
        
        # Save after each new memory
        self.save_memories()
        return memory
    
    def get_memories_by_context(self, context: str) -> List[PersistentMemory]:
        all_memories = self.core_memories + self.recent_memories + self.archival_memories
        return [m for m in all_memories if m.context.lower() == context.lower()]
    
    def get_session_memories(self, session_id: Optional[str] = None) -> List[PersistentMemory]:
        all_memories = self.core_memories + self.recent_memories + self.archival_memories
        if session_id:
            return [m for m in all_memories if m.session_id == session_id]
        return all_memories
    
    def get_relevant_memories(self, query: str, top_k: int = 3) -> List[PersistentMemory]:
        all_memories = self.core_memories + self.recent_memories + self.archival_memories
        
        # Simple keyword matching (could be enhanced with embeddings)
        scored_memories = [
            (memory, len(set(query.lower().split()) & set(memory.content.lower().split())))
            for memory in all_memories
        ]
        scored_memories.sort(key=lambda x: (-x[1], -x[0].importance))
        return [memory for memory, _ in scored_memories[:top_k]]
    
    def save_memories(self):
        memory_data = {
            'core': [m.to_dict() for m in self.core_memories],
            'recent': [m.to_dict() for m in self.recent_memories],
            'archival': [m.to_dict() for m in self.archival_memories],
        }
        
        with open(os.path.join(self.storage_dir, 'memories.json'), 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def load_memories(self):
        memory_file = os.path.join(self.storage_dir, 'memories.json')
        if not os.path.exists(memory_file):
            return
        
        with open(memory_file, 'r') as f:
            memory_data = json.load(f)
        
        self.core_memories = [PersistentMemory.from_dict(m) for m in memory_data.get('core', [])]
        self.recent_memories = [PersistentMemory.from_dict(m) for m in memory_data.get('recent', [])]
        self.archival_memories = [PersistentMemory.from_dict(m) for m in memory_data.get('archival', [])]
