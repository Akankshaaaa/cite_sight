from setuptools import setup, find_packages

setup(
    name="cite_sight",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "trafilatura",
        "newspaper3k",
    ],
) 