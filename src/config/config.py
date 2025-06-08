import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Search Settings
MAX_SEARCH_RESULTS = 5
MAX_RETRIES = 3
TIMEOUT = 30

# LLM Settings
MODEL_NAME = "deepseek/deepseek-r1-0528:free"  # OpenRouter's free Deepseek model
TEMPERATURE = 0.7
MAX_TOKENS = 1000

# OpenRouter Settings
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
SITE_URL = "https://cite-sight.com"  # Replace with your actual site URL
SITE_NAME = "CiteSight"

# Web Scraping Settings
USER_AGENT = "CiteSight Research Agent/1.0" 