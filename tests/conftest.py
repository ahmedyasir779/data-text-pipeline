import pytest
import pandas as pd
import os
from pathlib import Path


@pytest.fixture
def sample_csv_path(tmp_path):
    """
    Create temporary CSV file for testing
    
    Args:
        tmp_path: pytest's temporary directory fixture
        
    Returns:
        Path to temporary CSV file
    """
    data = pd.DataFrame({
        'product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
        'rating': [4.5, 3.8, 4.2, 4.7, 3.5],
        'price': [1200, 800, 600, 400, 150],
        'review': [
            'Great laptop! Fast performance and excellent build quality.',
            'Good phone but battery life could be better.',
            'Nice tablet for media consumption.',
            'Amazing monitor! Colors are vibrant.',
            'Keyboard is okay but keys feel cheap.'
        ]
    })
    
    csv_path = tmp_path / "test_data.csv"
    data.to_csv(csv_path, index=False)
    
    return str(csv_path)


@pytest.fixture
def sample_dataframe():
    """
    Create sample DataFrame for testing
    
    Returns:
        pandas DataFrame
    """
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['NYC', 'LA', 'Chicago'],
        'score': [85, 90, 78]
    })


@pytest.fixture
def sample_texts():
    """
    Create sample text data for testing
    
    Returns:
        List of text strings
    """
    return [
        'This is a great product! I love it.',
        'Not bad but could be better.',
        'Terrible quality. Do not buy.',
        'Amazing! Best purchase ever.',
        'It works fine. Nothing special.'
    ]


@pytest.fixture
def sample_text_file(tmp_path):
    """
    Create temporary text file
    
    Args:
        tmp_path: pytest's temporary directory fixture
        
    Returns:
        Path to temporary text file
    """
    text_content = """
    Apple Inc. is located in Cupertino, California.
    CEO Tim Cook announced revenue of $394 billion.
    Contact: info@apple.com or call (408) 996-1010.
    Visit https://www.apple.com for more info.
    """
    
    text_path = tmp_path / "test_text.txt"
    text_path.write_text(text_content)
    
    return str(text_path)


@pytest.fixture
def cache_dir(tmp_path):
    """
    Create temporary cache directory
    
    Args:
        tmp_path: pytest's temporary directory fixture
        
    Returns:
        Path to cache directory
    """
    cache_path = tmp_path / ".cache"
    cache_path.mkdir()
    return str(cache_path)