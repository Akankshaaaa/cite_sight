# CiteSight: Comprehensive Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Details](#component-details)
- [Implementation Details](#implementation-details)
- [User Interface](#user-interface)
- [Data Flow](#data-flow)
- [API Integration](#api-integration)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)

## Overview

CiteSight is an automated research assistant designed to streamline the process of gathering, analyzing, and synthesizing information from multiple web sources. It employs a combination of web scraping, natural language processing, and machine learning techniques to provide comprehensive, well-cited research summaries.

### Key Features
- Automated multi-source research
- Content extraction and cleaning
- AI-powered summarization
- Cross-validation analysis
- Confidence assessment
- Exportable reports (JSON/TXT)
- Modern web interface

## System Architecture

### Project Structure
```
cite_sight/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   └── research_agent.py    # Main orchestrator
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_tool.py       # Web search implementation
│   │   ├── content_retriever.py # Content extraction
│   │   └── summarizer.py        # AI summarization
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration management
│   └── app.py                  # Streamlit interface
├── .env                        # Environment variables
├── README.md
└── DETAILED_DOCUMENTATION.md
```

## Component Details

### 1. Research Agent (research_agent.py)
The central orchestrator that manages the research workflow:
- Breaks down research questions
- Coordinates between different tools
- Maintains research logs
- Handles error recovery
- Manages state and results

Key methods:
```python
def research(self, question: str) -> Dict:
    # Main research workflow
    # Returns structured research results

def break_down_question(self, question: str) -> List[str]:
    # Splits complex questions into sub-questions

def log_step(self, step: str, details: Dict):
    # Logs research progress
```

### 2. Search Tool (search_tool.py)
Handles web searches using DuckDuckGo:
- Non-API based web search
- Result filtering and ranking
- URL validation and cleaning
- Rate limiting and retry logic

Key features:
- Uses DuckDuckGo's HTML search
- Handles pagination
- Extracts structured results
- Manages request headers and user agents

### 3. Content Retriever (content_retriever.py)
Extracts and cleans web content:
- Uses Trafilatura for content extraction
- Handles different HTML structures
- Cleans and normalizes text
- Extracts metadata (title, date, etc.)

### 4. Summarizer (summarizer.py)
AI-powered content analysis:
- Uses OpenRouter's Deepseek model
- Generates structured summaries
- Extracts key points and quotes
- Assesses confidence levels
- Cross-validates information

### 5. Web Interface (app.py)
Streamlit-based UI with:
- Research input
- Progress tracking
- Results display
- Export options
- Error handling
- Responsive design

## Implementation Details

### Search Implementation
```python
# DuckDuckGo search with retries and error handling
def search(self, query: str) -> List[Dict]:
    for attempt in range(MAX_RETRIES):
        try:
            encoded_query = quote_plus(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            response = requests.get(url, headers=self.headers)
            # Process results...
        except Exception:
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Content Extraction
```python
# Clean content extraction with metadata
def fetch_content(self, url: str) -> Optional[Dict[str, str]]:
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    metadata = trafilatura.extract_metadata(downloaded)
    return {
        "title": metadata.title,
        "content": text,
        "url": url
    }
```

### AI Summarization
```python
# Structured summary generation
def summarize(self, content: str, context: str = "") -> Dict[str, str]:
    prompt = """
    Please analyze and summarize the following content:
    {
        "summary": "...",
        "key_points": [...],
        "quotes": [...],
        "confidence_level": "high/medium/low"
    }
    """
    # Process with OpenRouter API...
```

## Data Flow

1. **Input Processing**
   - User submits research question
   - Question analysis and breakdown
   - Search query formulation

2. **Data Collection**
   - Web search execution
   - URL validation and filtering
   - Content extraction and cleaning

3. **Analysis**
   - Content summarization
   - Key point extraction
   - Quote identification
   - Confidence assessment

4. **Cross-Validation**
   - Information comparison
   - Agreement identification
   - Contradiction detection
   - Unique point extraction

5. **Report Generation**
   - Summary compilation
   - Citation organization
   - Format conversion (JSON/TXT)
   - Export preparation

## API Integration

### OpenRouter API
- Model: deepseek/deepseek-r1-0528:free
- Temperature: 0.7
- Max tokens: 1000
- Response format: JSON
- Error handling and retry logic

Configuration:
```python
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-0528:free"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
```

## Error Handling

1. **Search Errors**
   - Network failures
   - Rate limiting
   - Invalid responses
   - Retry with exponential backoff

2. **Content Extraction**
   - Invalid URLs
   - Access denied
   - Parsing failures
   - Timeout handling

3. **API Errors**
   - Authentication issues
   - Rate limits
   - Model errors
   - Response validation

4. **UI Error Display**
   - User-friendly messages
   - Error logging
   - Recovery options
   - Progress preservation

## Future Enhancements

1. **Research Capabilities**
   - Advanced question breakdown
   - Source credibility scoring
   - Citation format options
   - Research history

2. **UI Improvements**
   - Dark mode
   - Mobile optimization
   - Progress indicators
   - Interactive visualizations

3. **Integration Options**
   - API endpoints
   - Browser extension
   - Document upload
   - Export formats

4. **Performance**
   - Parallel processing
   - Caching
   - Result ranking
   - Resource optimization

## Security Considerations

1. **API Keys**
   - Environment variables
   - Key rotation
   - Access logging
   - Usage monitoring

2. **Web Requests**
   - URL validation
   - Rate limiting
   - Header management
   - Response validation

3. **User Data**
   - Session management
   - Data encryption
   - Privacy controls
   - Access logging

## Best Practices

1. **Code Organization**
   - Modular design
   - Clear separation of concerns
   - Comprehensive documentation
   - Type hints

2. **Error Management**
   - Graceful degradation
   - User feedback
   - Logging
   - Recovery strategies

3. **Testing**
   - Unit tests
   - Integration tests
   - Error scenarios
   - Performance testing

4. **Maintenance**
   - Version control
   - Dependency management
   - Configuration management
   - Deployment procedures 