"""
Setup configuration for pip installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8')

setup(
    name="data-text-pipeline",
    version="1.0.0",
    author="Ahmed Yasir",
    author_email="your.email@example.com",
    description="Unified data and text processing pipeline with NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmedyasir779/data-text-pipeline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "nltk>=3.6.0",
        "spacy>=3.0.0",
        "textblob>=0.15.0",
        "rake-nltk>=1.0.6",
        "scikit-learn>=0.24.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
        "pyyaml>=5.4.0",
        "unidecode>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "pytest-mock>=3.6.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "data-text-pipeline=cli:main",
        ],
    },
)