from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="finsentrix",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "finsentrix=src.api.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A sentiment analysis system for Iranian stock market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iranian-stock-sentiment-analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 