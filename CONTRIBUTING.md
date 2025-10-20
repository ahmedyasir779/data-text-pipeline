# Contributing Guide

Thank you for considering contributing to the Unified Data & Text Processing Pipeline!

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

## Development Setup

### 1. Fork & Clone
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/ahmedyasir779/data-text-pipeline.git
cd data-text-pipeline
```

### 2. Create Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Make Changes

- Write code
- Add tests
- Update documentation

### 5. Run Tests
```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=. --cov-report=html

# Ensure 75%+ coverage
```

### 6. Commit Changes
```bash
git add .
git commit -m "Add: Brief description of changes"
```

**Commit Message Format:**
- `Add: New feature`
- `Fix: Bug description`
- `Update: Documentation/dependency`
- `Refactor: Code improvement`
- `Test: Add test for X`

### 7. Push & Create PR
```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub.

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Document all functions
- Maximum line length: 100 characters

### Example:
```python
def process_data(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    """
    Process dataframe with specified strategy
    
    Args:
        df: Input DataFrame
        strategy: Cleaning strategy ('drop', 'fill', 'forward_fill')
        
    Returns:
        Processed DataFrame
        
    Raises:
        ValueError: If strategy is invalid
    """
    if strategy not in ['drop', 'fill', 'forward_fill']:
        raise ValueError(f"Invalid strategy: {strategy}")
    
    # Implementation
    return df
```

## Testing Requirements

### All PRs must include:

1. **Unit tests** for new features
2. **Coverage** of 75% or higher
3. **All tests passing**

### Test Structure:
```python
class TestNewFeature:
    """Test suite for new feature"""
    
    def test_basic_functionality(self):
        """Test basic use case"""
        # Arrange
        input_data = ...
        
        # Act
        result = function(input_data)
        
        # Assert
        assert result == expected
    
    def test_edge_cases(self):
        """Test edge cases"""
        ...
    
    def test_error_handling(self):
        """Test error conditions"""
        with pytest.raises(ValueError):
            function(invalid_input)
```

## Documentation Requirements

### Update documentation for:

- New features → README.md + docs/
- Bug fixes → CHANGELOG.md
- API changes → docs/API.md

## Pull Request Process

1. **Update CHANGELOG.md** with your changes
2. **Ensure all tests pass**
3. **Update documentation**
4. **Request review** from maintainers
5. **Address feedback**

## Code Review Criteria

PRs are reviewed for:

- ✅ Code quality
- ✅ Test coverage
- ✅ Documentation
- ✅ Performance impact
- ✅ Security implications

## Questions?

Open an issue or discussion on GitHub!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.