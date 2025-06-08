# CiteSight 🔍

CiteSight is an automated research assistant that helps you gather, analyze, and cross-validate information from multiple web sources. It provides well-cited summaries and insights for your research questions.

## Features

- 🌐 Automated web research across multiple sources
- 📝 Smart content extraction and summarization
- ✓ Cross-validation of information across sources
- 📊 Confidence assessment for findings
- 💾 Export reports in JSON and TXT formats
- 🎨 Clean, modern web interface

## Quick Start

1. Clone the repository
2. Create a conda environment:
```bash
conda create -n cite_sight python=3.9
conda activate cite_sight
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```
OPENROUTER_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run src/app.py
```

## Tech Stack

- **Frontend**: Streamlit
- **LLM Integration**: OpenRouter API (using Deepseek model)
- **Web Search**: DuckDuckGo
- **Content Extraction**: Trafilatura
- **Language**: Python 3.9+

