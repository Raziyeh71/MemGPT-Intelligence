import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional, Tuple
import json
import os
from datetime import datetime
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from dataclasses import dataclass, asdict
import logging
import pandas as pd

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

@dataclass
class IntelligentMemory:
    content: str
    timestamp: float
    importance: float
    context: str
    memory_type: str
    embedding: Optional[List[float]] = None
    access_count: int = 0
    last_accessed: float = 0
    related_memories: List[str] = None
    tags: List[str] = None
    
    def to_dict(self):
        data = asdict(self)
        if self.embedding is not None:
            data['embedding'] = self.embedding.tolist()
        return data
    
    @classmethod
    def from_dict(cls, data):
        if 'embedding' in data and data['embedding'] is not None:
            data['embedding'] = np.array(data['embedding'])
        return cls(**data)

class IntelligentMemoryManager:
    def __init__(self, storage_dir: str = "intelligent_memory_storage"):
        self.storage_dir = storage_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.memories: List[IntelligentMemory] = []
        self.importance_threshold = 0.7  # Dynamic threshold
        self.memory_capacity = 1000  # Maximum number of memories to store
        
        # Create storage directory
        os.makedirs(storage_dir, exist_ok=True)
        self.load_memories()
        
        # Initialize logging
        logging.basicConfig(
            filename=os.path.join(storage_dir, 'memory_operations.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text using sentence transformer."""
        return self.model.encode([text])[0]
    
    def _calculate_importance(self, content: str, context: str, related_memories: List[IntelligentMemory]) -> float:
        """Calculate importance score using multiple factors."""
        base_importance = 0.5
        importance_factors = []
        
        # Length factor (longer content might be more important)
        length_factor = min(len(content.split()) / 100, 1.0) * 0.2
        importance_factors.append(length_factor)
        
        # Context continuity (related to existing memories)
        if related_memories:
            context_factor = min(len(related_memories) / 5, 1.0) * 0.3
            importance_factors.append(context_factor)
        
        # Semantic richness (unique words ratio)
        words = content.lower().split()
        unique_words = len(set(words))
        richness_factor = min(unique_words / len(words), 1.0) * 0.2
        importance_factors.append(richness_factor)
        
        # Named entity factor
        try:
            tokens = nltk.word_tokenize(content)
            pos_tags = nltk.pos_tag(tokens)
            named_entities = [word for word, pos in pos_tags if pos in ['NNP', 'NNPS']]
            entity_factor = min(len(named_entities) / 5, 1.0) * 0.3
            importance_factors.append(entity_factor)
        except Exception as e:
            logging.warning(f"Error in named entity detection: {e}")
        
        return base_importance + sum(importance_factors)
    
    def _find_related_memories(self, content: str, embedding: np.ndarray) -> List[IntelligentMemory]:
        """Find related memories using embedding similarity."""
        if not self.memories:
            return []
        
        similarities = []
        for memory in self.memories:
            if memory.embedding is not None:
                similarity = cosine_similarity([embedding], [memory.embedding])[0][0]
                similarities.append((memory, similarity))
        
        # Sort by similarity and return top related memories
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, sim in similarities[:5] if sim > 0.5]
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract relevant tags from content."""
        tokens = nltk.word_tokenize(content.lower())
        pos_tags = nltk.pos_tag(tokens)
        
        # Extract nouns and named entities as tags
        tags = []
        for word, pos in pos_tags:
            if pos.startswith(('NN', 'JJ')) and word not in stopwords.words('english'):
                tags.append(word)
        
        return list(set(tags))[:5]  # Return up to 5 unique tags
    
    def add_memory(self, content: str, context: str) -> IntelligentMemory:
        """Add a new memory with intelligent processing."""
        # Generate embedding
        embedding = self._generate_embedding(content)
        
        # Find related memories
        related_memories = self._find_related_memories(content, embedding)
        
        # Calculate importance
        importance = self._calculate_importance(content, context, related_memories)
        
        # Extract tags
        tags = self._extract_tags(content)
        
        # Create memory
        memory = IntelligentMemory(
            content=content,
            timestamp=datetime.now().timestamp(),
            importance=importance,
            context=context,
            memory_type='active' if importance > self.importance_threshold else 'archive',
            embedding=embedding,
            related_memories=[m.content for m in related_memories],
            tags=tags
        )
        
        # Add memory and manage capacity
        self.memories.append(memory)
        self._manage_capacity()
        
        # Log operation
        logging.info(f"Added memory: {content[:50]}... | Importance: {importance:.2f}")
        
        # Save memories
        self.save_memories()
        return memory
    
    def _manage_capacity(self):
        """Manage memory capacity using intelligent selection."""
        if len(self.memories) > self.memory_capacity:
            # Calculate retention scores
            retention_scores = []
            current_time = datetime.now().timestamp()
            
            for memory in self.memories:
                # Factors for retention
                recency = 1 / (current_time - memory.timestamp + 1)
                importance = memory.importance
                access_frequency = memory.access_count / (current_time - memory.timestamp + 1)
                
                # Combined retention score
                retention_score = (
                    0.4 * importance +
                    0.3 * recency +
                    0.3 * access_frequency
                )
                retention_scores.append((memory, retention_score))
            
            # Sort by retention score and keep top memories
            retention_scores.sort(key=lambda x: x[1], reverse=True)
            self.memories = [m for m, _ in retention_scores[:self.memory_capacity]]
    
    def get_relevant_memories(self, query: str, top_k: int = 5) -> List[Tuple[IntelligentMemory, float]]:
        """Get relevant memories using semantic search."""
        query_embedding = self._generate_embedding(query)
        
        relevant_memories = []
        current_time = datetime.now().timestamp()
        
        for memory in self.memories:
            if memory.embedding is not None:
                # Calculate semantic similarity
                similarity = cosine_similarity([query_embedding], [memory.embedding])[0][0]
                
                # Calculate recency factor
                recency = 1 / (current_time - memory.timestamp + 1)
                
                # Combined relevance score
                relevance = 0.7 * similarity + 0.3 * recency
                
                relevant_memories.append((memory, relevance))
        
        # Sort by relevance and return top-k
        relevant_memories.sort(key=lambda x: x[1], reverse=True)
        return relevant_memories[:top_k]
    
    def analyze_memory_patterns(self) -> Dict:
        """Analyze patterns in stored memories."""
        if not self.memories:
            return {}
        
        df = pd.DataFrame([{
            'importance': m.importance,
            'context': m.context,
            'memory_type': m.memory_type,
            'access_count': m.access_count,
            'timestamp': m.timestamp,
            'tags': m.tags
        } for m in self.memories])
        
        analysis = {
            'importance_stats': {
                'mean': df['importance'].mean(),
                'std': df['importance'].std(),
                'median': df['importance'].median()
            },
            'context_distribution': df['context'].value_counts().to_dict(),
            'memory_type_distribution': df['memory_type'].value_counts().to_dict(),
            'common_tags': pd.Series([tag for tags in df['tags'] for tag in tags]).value_counts().head().to_dict()
        }
        
        return analysis
    
    def save_memories(self):
        """Save memories to disk."""
        memory_data = [memory.to_dict() for memory in self.memories]
        with open(os.path.join(self.storage_dir, 'memories.json'), 'w') as f:
            json.dump(memory_data, f, indent=2)
    
    def load_memories(self):
        """Load memories from disk."""
        memory_file = os.path.join(self.storage_dir, 'memories.json')
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                memory_data = json.load(f)
            self.memories = [IntelligentMemory.from_dict(m) for m in memory_data]
