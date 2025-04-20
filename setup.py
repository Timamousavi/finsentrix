from setuptools import setup, find_packages

setup(
    name="finsentrix",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.5",
        "hazm>=0.7.0",
        "transformers>=4.11.0",
        "torch>=1.9.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=0.24.2",
        "plotly>=5.3.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "finsentrix=finsentrix.cli:main",
        ],
    },
    author="Tima Mousavi",
    author_email="fatemehmousavy@ut.ac.ir",
    description="Global Financial Market Sentiment Analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Timamousavi/finsentrix",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
) 