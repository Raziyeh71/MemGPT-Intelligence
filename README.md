# Intelligent Memory Management System

A sophisticated implementation inspired by the MemGPT paper, featuring intelligent memory management, context awareness, and semantic understanding.

## Features

### 1. Intelligent Memory Management
- Smart importance calculation using multiple factors
- Semantic memory processing with embeddings
- Dynamic memory retention and prioritization
- Automatic tag extraction and named entity recognition
- Pattern analysis and insights generation

### 2. Context-Aware Assistant
- Maintains conversation context across sessions
- Remembers user preferences and past interactions
- Provides relevant information based on context
- Supports multiple conversation contexts

### 3. Persistent Memory System
- Disk-based storage for long-term memory retention
- Memory organization into core, recent, and archival categories
- Efficient memory retrieval using semantic search
- Automatic memory cleanup and optimization

## Project Structure

```
memgpt_simple/
├── requirements.txt          # Project dependencies
├── intelligent_memory.py     # Core memory management system
├── persistent_assistant.py   # Context-aware assistant implementation
├── chatbot.py               # Simple chatbot implementation
├── demo_intelligent_system.py# Demonstration of the system
└── memory_storage/          # Directory for persistent storage
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/memgpt_simple.git
cd memgpt_simple
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Intelligent Memory System Demo
```bash
python demo_intelligent_system.py
```
This demonstrates:
- Smart memory storage and retrieval
- Pattern analysis
- Semantic search capabilities

### 2. Context-Aware Assistant
```bash
python persistent_assistant.py
```
Features:
- Cross-session memory
- Context awareness
- User preference learning

### 3. Simple Chatbot
```bash
python chatbot.py
```
Basic features:
- Memory-enabled conversations
- Basic context tracking
- User interaction demo

## Implementation Details

### Intelligent Memory System
- Uses sentence transformers for semantic understanding
- Implements sophisticated importance calculation
- Features dynamic memory retention
- Provides pattern analysis and insights

### Memory Types
1. Core Memories
   - High importance information
   - Critical context and preferences
   - Permanent storage

2. Active Memories
   - Current context and recent interactions
   - Temporary but important information
   - Medium-term retention

3. Archival Memories
   - Historical information
   - Lower priority but maintained
   - Long-term storage with cleanup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the MemGPT paper
- Uses Hugging Face's transformers library
- Built with Python and modern NLP techniques

## Future Improvements

1. Enhanced Semantic Processing
   - Better embedding models
   - More sophisticated similarity metrics
   - Improved context understanding

2. Advanced Memory Management
   - More efficient storage systems
   - Better cleanup strategies
   - Enhanced importance calculations

3. UI/UX Improvements
   - Web interface
   - Visualization of memory patterns
   - Interactive memory exploration

## Contact

Razy Shafiee - r.shafiee93@gmail.com
Project Link: [https://github.com/Raziyeh71/MemGPT-Intelligence.git](https://github.com/Raziyeh71/MemGPT-Intelligence.git)