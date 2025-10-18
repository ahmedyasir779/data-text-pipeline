import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
from pathlib import Path

class UnifiedPipeline:
    def __init__(self):
        self.data_df = None
        self.text_data = []
        self.results = {}

        print("UnifiedPipeline initialized.")

    
    # ===============================
    # DATA LOADING
    # ===============================
    def load_structured_data(self, file_path: str) -> 'UnifiedPipeline':
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix == '.csv':
            self.data_df = pd.read_csv(file_path)
        elif path.suffix in ['.xls', '.xlsx']:
            self.data_df = pd.read_excel(file_path)
        elif path.suffix == '.json':
            self.data_df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        print(f"Loaded structured data : {len(self.data_df)} rows, {len(self.data_df.columns)} columns.")

        return self
    
    def load_text_column(self, column_name: str) -> 'UnifiedPipeline':
        """
        Extract text data from a column in the structured data
        
        Args:
            column_name: Name of column containing text
            
        Returns:
            Self for method chaining
        """
        if self.data_df is None:
            raise ValueError("No structured data loaded. Call load_structured_data() first.")
        
        if column_name not in self.data_df.columns:
            raise ValueError(f"Column '{column_name}' not found in data")
        
        self.text_data = self.data_df[column_name].dropna().tolist()
        
        print(f" Extracted {len(self.text_data)} text entries from column '{column_name}'")
        
        return self
    
    def load_text_file(self, file_path: str) -> 'UnifiedPipeline':
        """
        Load text from a file
        
        Args:
            file_path: Path to text file
            
        Returns:
            Self for method chaining
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by lines or paragraphs
        self.text_data = [line.strip() for line in content.split('\n') if line.strip()]
        
        print(f" Loaded text file: {len(self.text_data)} entries")
        
        return self
    
    # ============================================
    # DATA CLEANING
    # ============================================
    
    def clean_data(self, strategy: str = 'drop') -> 'UnifiedPipeline':
        """
        Clean structured data
        
        Args:
            strategy: How to handle missing values ('drop', 'fill', 'forward_fill')
            
        Returns:
            Self for method chaining
        """
        if self.data_df is None:
            print(" No structured data to clean")
            return self
        
        original_rows = len(self.data_df)
        
        # Handle missing values
        if strategy == 'drop':
            self.data_df = self.data_df.dropna()
        elif strategy == 'fill':
            self.data_df = self.data_df.fillna(0)
        elif strategy == 'forward_fill':
            self.data_df = self.data_df.fillna(method='ffill')
        
        # Remove duplicates
        self.data_df = self.data_df.drop_duplicates()
        
        final_rows = len(self.data_df)
        removed = original_rows - final_rows
        
        print(f" Cleaned data: {original_rows} → {final_rows} rows (removed {removed})")
        
        return self
    
    def clean_text(self) -> 'UnifiedPipeline':
        """
        Clean text data (basic cleaning)
        
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print(" No text data to clean")
            return self
        
        import re
        
        cleaned = []
        for text in self.text_data:
            # Remove URLs
            text = re.sub(r'https?://\S+', '', text)
            # Remove emails
            text = re.sub(r'\S+@\S+', '', text)
            # Remove special characters
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            # Normalize whitespace
            text = ' '.join(text.split())
            
            if text:  # Only keep non-empty
                cleaned.append(text)
        
        original_count = len(self.text_data)
        self.text_data = cleaned
        
        print(f" Cleaned text: {original_count} → {len(self.text_data)} entries")
        
        return self
    
    # ============================================
    # ANALYSIS
    # ============================================
    
    def analyze_data(self) -> 'UnifiedPipeline':
        """
        Analyze structured data
        
        Returns:
            Self for method chaining
        """
        if self.data_df is None:
            print(" No structured data to analyze")
            return self
        
        # Get numeric columns
        numeric_cols = self.data_df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print(" No numeric columns found")
            return self
        
        # Calculate statistics
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                'mean': self.data_df[col].mean(),
                'median': self.data_df[col].median(),
                'std': self.data_df[col].std(),
                'min': self.data_df[col].min(),
                'max': self.data_df[col].max()
            }
        
        self.results['data_statistics'] = stats
        
        print(f" Analyzed {len(numeric_cols)} numeric columns")
        
        return self
    
    def analyze_text(self) -> 'UnifiedPipeline':
        """
        Analyze text data
        
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print(" No text data to analyze")
            return self
        
        # Basic text analysis
        from collections import Counter
        
        # Combine all text
        all_text = ' '.join(self.text_data)
        words = all_text.lower().split()
        
        # Word frequency
        word_freq = Counter(words)
        
        # Statistics
        text_stats = {
            'total_entries': len(self.text_data),
            'total_words': len(words),
            'unique_words': len(set(words)),
            'avg_words_per_entry': len(words) / len(self.text_data) if self.text_data else 0,
            'top_10_words': word_freq.most_common(10)
        }
        
        self.results['text_statistics'] = text_stats
        
        print(f"  Analyzed {len(self.text_data)} text entries")
        print(f"  Total words: {text_stats['total_words']}")
        print(f"  Unique words: {text_stats['unique_words']}")
        
        return self
    
    def correlate_data_with_text_length(self, data_column: str) -> 'UnifiedPipeline':
        """
        Correlate numeric data with text length
        
        Example: Does review length correlate with rating?
        
        Args:
            data_column: Name of numeric column to correlate
            
        Returns:
            Self for method chaining
        """
        if self.data_df is None or not self.text_data:
            print(" Need both data and text loaded")
            return self
        
        if data_column not in self.data_df.columns:
            print(f" Column '{data_column}' not found")
            return self
        
        # Calculate text lengths
        text_lengths = [len(text.split()) for text in self.text_data]
        
        # Make sure lengths match
        if len(text_lengths) != len(self.data_df):
            print(" Text and data lengths don't match")
            return self
        
        # Calculate correlation
        correlation = np.corrcoef(self.data_df[data_column], text_lengths)[0, 1]
        
        self.results['correlation'] = {
            'column': data_column,
            'correlation_with_text_length': correlation
        }
        
        print(f" Correlation between {data_column} and text length: {correlation:.3f}")
        
        return self
    
    # ============================================
    # REPORTING
    # ============================================
    
    def generate_report(self) -> str:
        """
        Generate comprehensive report
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("UNIFIED PIPELINE ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Data statistics
        if 'data_statistics' in self.results:
            report.append("\n STRUCTURED DATA STATISTICS")
            report.append("-" * 60)
            
            for col, stats in self.results['data_statistics'].items():
                report.append(f"\n{col}:")
                report.append(f"  Mean: {stats['mean']:.2f}")
                report.append(f"  Median: {stats['median']:.2f}")
                report.append(f"  Std Dev: {stats['std']:.2f}")
                report.append(f"  Range: {stats['min']:.2f} - {stats['max']:.2f}")
        
        # Text statistics
        if 'text_statistics' in self.results:
            report.append("\n\n TEXT ANALYSIS")
            report.append("-" * 60)
            
            stats = self.results['text_statistics']
            report.append(f"Total entries: {stats['total_entries']}")
            report.append(f"Total words: {stats['total_words']}")
            report.append(f"Unique words: {stats['unique_words']}")
            report.append(f"Avg words/entry: {stats['avg_words_per_entry']:.1f}")
            
            report.append("\nTop 10 words:")
            for word, count in stats['top_10_words']:
                report.append(f"  {word}: {count}")
        
        # Correlation
        if 'correlation' in self.results:
            report.append("\n\n CORRELATION ANALYSIS")
            report.append("-" * 60)
            
            corr = self.results['correlation']
            report.append(f"Column: {corr['column']}")
            report.append(f"Correlation with text length: {corr['correlation_with_text_length']:.3f}")
            
            # Interpretation
            corr_value = abs(corr['correlation_with_text_length'])
            if corr_value > 0.7:
                strength = "strong"
            elif corr_value > 0.4:
                strength = "moderate"
            elif corr_value > 0.2:
                strength = "weak"
            else:
                strength = "very weak"
            
            report.append(f"Interpretation: {strength} correlation")
        
        report.append("\n" + "=" * 60)
        report.append(" REPORT COMPLETE")
        report.append("=" * 60)
        
        return '\n'.join(report)
    
    def save_report(self, filepath: str = 'output/unified_report.txt'):
        """
        Save report to file
        
        Args:
            filepath: Where to save report
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f" Report saved to {filepath}")
    
    def get_summary(self) -> Dict:
        """
        Get summary of pipeline results
        
        Returns:
            Dictionary with summary
        """
        return {
            'data_rows': len(self.data_df) if self.data_df is not None else 0,
            'data_columns': len(self.data_df.columns) if self.data_df is not None else 0,
            'text_entries': len(self.text_data),
            'results': self.results
        }

# ============================================
# TESTING CODE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("UNIFIED PIPELINE - TEST")
    print("=" * 60)
    
    # Create sample data for testing
    print("\n Creating sample data...")
    
    # Sample CSV with reviews and ratings
    sample_data = pd.DataFrame({
        'product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
        'rating': [4.5, 3.8, 4.2, 4.7, 3.5],
        'price': [1200, 800, 600, 400, 150],
        'review': [
            'Great laptop! Fast performance and excellent build quality.',
            'Good phone but battery life could be better.',
            'Nice tablet for media consumption. Screen is beautiful.',
            'Amazing monitor! Colors are vibrant and sharp.',
            'Keyboard is okay but keys feel cheap.'
        ]
    })
    
    # Save sample data
    Path('data').mkdir(exist_ok=True)
    sample_data.to_csv('data/products.csv', index=False)
    print(" Sample data created: data/products.csv")
    
    # Test the pipeline
    print("\n Running unified pipeline...")
    
    pipeline = UnifiedPipeline()
    
    # Load and process
    pipeline.load_structured_data('data/products.csv')
    pipeline.load_text_column('review')
    
    # Clean
    pipeline.clean_data()
    pipeline.clean_text()
    
    # Analyze
    pipeline.analyze_data()
    pipeline.analyze_text()
    pipeline.correlate_data_with_text_length('rating')
    
    # Generate report
    print("\n" + "=" * 60)
    print(pipeline.generate_report())
    
    # Save report
    pipeline.save_report()
    
    print("\n" + "=" * 60)
    print(" TEST COMPLETE!")
    print("=" * 60)