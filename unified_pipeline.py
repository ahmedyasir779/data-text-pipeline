import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
from pathlib import Path
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

from advanced_nlp import AdvancedNLP
from cache_manager import CacheManager
from progress_tracker import ProgressTracker
from tqdm import tqdm

class UnifiedPipeline:
    def __init__(self, use_cache: bool = True):
        """
        Initialize the unified pipeline
        
        Args:
            use_cache: Whether to use caching (default: True)
        """
        self.data_df = None
        self.text_data = []
        self.results = {}
        self.advanced_nlp = AdvancedNLP()
        
        # Caching
        self.use_cache = use_cache
        if use_cache:
            self.cache = CacheManager()
        else:
            self.cache = None
        
        print("✓ Unified Pipeline initialized")
        if use_cache:
            print("  Cache enabled")
    
    # ===============================
    # DATA LOADING
    # ===============================
    def load_structured_data(self, file_path: str) -> 'UnifiedPipeline':
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
         # Check cache
        cache_key = None
        if self.cache:
            cache_key = self.cache._generate_key(file_path)
            cached_data = self.cache.get(cache_key, category='data')
            
            if cached_data is not None:
                self.data_df = cached_data
                print(f"✓ Loaded from cache: {len(self.data_df)} rows, {len(self.data_df.columns)} columns")
                return self
        
        # Load from file
        print(f" Loading {path.suffix} file...")

        if path.suffix == '.csv':
            self.data_df = pd.read_csv(file_path)
        elif path.suffix in ['.xls', '.xlsx']:
            self.data_df = pd.read_excel(file_path)
        elif path.suffix == '.json':
            self.data_df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Cache the result
        if self.cache and cache_key:
            self.cache.set(cache_key, self.data_df, category='data')

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
    
    def analyze_sentiment(self) -> 'UnifiedPipeline':
        """
        Analyze sentiment of text data
        
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print("⚠ No text data to analyze sentiment")
            return self
        
        # Check cache
        cache_key = None
        if self.cache:
            cache_key = self.cache._generate_key(str(self.text_data))
            cached_sentiment = self.cache.get(cache_key, category='nlp')
            
            if cached_sentiment is not None:
                self.results['sentiment'] = cached_sentiment
                print("✓ Loaded sentiment analysis from cache")
                return self
        
        print("Analyzing sentiment...")
        
        sentiments = []
        for text in self.text_data:
            blob = TextBlob(text)
            sentiment = {
                'polarity': blob.sentiment.polarity,  # -1 (negative) to +1 (positive)
                'subjectivity': blob.sentiment.subjectivity,  # 0 (objective) to 1 (subjective)
            }
            sentiments.append(sentiment)
        
        # Calculate averages
        avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
        avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
        
        # Categorize sentiments
        positive = sum(1 for s in sentiments if s['polarity'] > 0.1)
        neutral = sum(1 for s in sentiments if -0.1 <= s['polarity'] <= 0.1)
        negative = sum(1 for s in sentiments if s['polarity'] < -0.1)
        
        sentiment_results = {
            'sentiments': sentiments,
            'avg_polarity': avg_polarity,
            'avg_subjectivity': avg_subjectivity,
            'positive_count': positive,
            'neutral_count': neutral,
            'negative_count': negative,
            'total': len(sentiments)
        }
        
        self.results['sentiment'] = sentiment_results
        

        # Cache the result
        if self.cache and cache_key:
            self.cache.set(cache_key, sentiment_results, category='nlp')

        print(f"✓ Sentiment analysis complete")
        print(f"  Positive: {positive} ({positive/len(sentiments)*100:.1f}%)")
        print(f"  Neutral: {neutral} ({neutral/len(sentiments)*100:.1f}%)")
        print(f"  Negative: {negative} ({negative/len(sentiments)*100:.1f}%)")
        print(f"  Avg polarity: {avg_polarity:.3f}")
        
        return self

    def extract_entities(self) -> 'UnifiedPipeline':
        """Extract named entities from text with progress"""
        if not self.text_data:
            print("⚠ No text data for entity extraction")
            return self
        
        # Check cache
        cache_key = None
        if self.cache:
            cache_key = self.cache._generate_key(str(self.text_data) + '_entities')
            cached_entities = self.cache.get(cache_key, category='nlp')
            
            if cached_entities is not None:
                self.results['entities'] = cached_entities
                print("✓ Loaded entity extraction from cache")
                return self
        
        print("Extracting named entities...")
        entities = self.advanced_nlp.extract_entities(self.text_data)
        
        self.results['entities'] = entities
        
        # Cache the result
        if self.cache and cache_key:
            self.cache.set(cache_key, entities, category='nlp')
        
        print(f"✓ Entity extraction complete")
        for entity_type, data in entities.items():
            print(f"  {entity_type}: {data['total']} mentions ({data['unique']} unique)")
        
        return self
    
    def extract_keywords(self, method: str = 'tfidf', top_n: int = 10) -> 'UnifiedPipeline':
        """
        Extract keywords from text
        
        Args:
            method: 'rake' or 'tfidf'
            top_n: Number of keywords to extract
            
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print("⚠ No text data for keyword extraction")
            return self
        
        print(f"Extracting keywords using {method.upper()}...")
        
        if method == 'rake':
            keywords = self.advanced_nlp.extract_keywords(self.text_data, top_n=top_n)
        else:  # tfidf
            keywords = self.advanced_nlp.extract_keywords_tfidf(self.text_data, top_n=top_n)
        
        self.results['keywords'] = {
            'method': method,
            'keywords': keywords
        }
        
        print(f"✓ Extracted {len(keywords)} keywords")
        print("  Top 5:")
        for keyword, score in keywords[:5]:
            print(f"    {keyword}: {score:.3f}")
        
        return self
    
    def detect_topics(self) -> 'UnifiedPipeline':
        """
        Detect topics in text
        
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print("⚠ No text data for topic detection")
            return self
        
        print("Detecting topics...")
        topics = self.advanced_nlp.detect_topics(self.text_data)
        
        self.results['topics'] = topics
        
        print(f"✓ Detected {len(topics)} topics")
        for topic in topics.keys():
            print(f"  • {topic}")
        
        return self
    
    def analyze_complexity(self) -> 'UnifiedPipeline':
        """
        Analyze text complexity and readability
        
        Returns:
            Self for method chaining
        """
        if not self.text_data:
            print("⚠ No text data for complexity analysis")
            return self
        
        print("Analyzing text complexity...")
        complexity = self.advanced_nlp.analyze_text_complexity(self.text_data)
        
        self.results['complexity'] = complexity
        
        print(f"✓ Complexity analysis complete")
        print(f"  Reading level: {complexity['interpretation']}")
        print(f"  Flesch score: {complexity['avg_flesch_reading_ease']}")
        print(f"  Grade level: {complexity['avg_flesch_kincaid_grade']}")
        
        return self
    
    def correlate_sentiment_with_column(self, column_name: str) -> 'UnifiedPipeline':
        """
        Correlate sentiment with a numeric column
        
        Example: Does positive sentiment correlate with higher ratings?
        
        Args:
            column_name: Name of numeric column to correlate
            
        Returns:
            Self for method chaining
        """
        if 'sentiment' not in self.results:
            print("⚠ Run analyze_sentiment() first")
            return self
        
        if self.data_df is None or column_name not in self.data_df.columns:
            print(f"⚠ Column '{column_name}' not found")
            return self
        
        sentiments = self.results['sentiment']['sentiments']
        polarities = [s['polarity'] for s in sentiments]
        
        # Make sure lengths match
        if len(polarities) != len(self.data_df):
            print("⚠ Sentiment and data lengths don't match")
            return self
        
        # Calculate correlation
        column_values = self.data_df[column_name].values
        correlation = np.corrcoef(column_values, polarities)[0, 1]
        
        if 'correlations' not in self.results:
            self.results['correlations'] = {}
        
        self.results['correlations']['sentiment_' + column_name] = {
            'column': column_name,
            'correlation': correlation,
            'type': 'sentiment_polarity'
        }
        
        print(f"✓ Correlation between {column_name} and sentiment: {correlation:.3f}")
        
        # Interpretation
        if correlation > 0.7:
            print("  → Strong positive correlation")
        elif correlation > 0.4:
            print("  → Moderate positive correlation")
        elif correlation > 0.2:
            print("  → Weak positive correlation")
        elif correlation > -0.2:
            print("  → Very weak/no correlation")
        elif correlation > -0.4:
            print("  → Weak negative correlation")
        elif correlation > -0.7:
            print("  → Moderate negative correlation")
        else:
            print("  → Strong negative correlation")
        
        return self
    
    def create_visualizations(self, output_dir: str = 'output') -> 'UnifiedPipeline':
        """
        Create visualizations of the analysis
        
        Args:
            output_dir: Directory to save visualizations
            
        Returns:
            Self for method chaining
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(16, 10))
        
        plot_count = 0
        
        # Plot 1: Data distribution (if numeric columns exist)
        if self.data_df is not None:
            numeric_cols = self.data_df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                plot_count += 1
                ax1 = plt.subplot(2, 3, 1)
                
                # Show distribution of first numeric column
                col = numeric_cols[0]
                self.data_df[col].hist(bins=20, ax=ax1, color='skyblue', edgecolor='black')
                ax1.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
                ax1.set_xlabel(col)
                ax1.set_ylabel('Frequency')
        
        # Plot 2: Sentiment distribution
        if 'sentiment' in self.results:
            plot_count += 1
            ax2 = plt.subplot(2, 3, 2)
            
            sentiment = self.results['sentiment']
            categories = ['Positive', 'Neutral', 'Negative']
            counts = [sentiment['positive_count'], 
                     sentiment['neutral_count'], 
                     sentiment['negative_count']]
            colors = ['green', 'gray', 'red']
            
            ax2.bar(categories, counts, color=colors, alpha=0.7, edgecolor='black')
            ax2.set_title('Sentiment Distribution', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Count')
            
            # Add percentage labels
            total = sum(counts)
            for i, (cat, count) in enumerate(zip(categories, counts)):
                percentage = count / total * 100
                ax2.text(i, count + 0.5, f'{percentage:.1f}%', 
                        ha='center', va='bottom', fontweight='bold')
        
        # Plot 3: Sentiment polarity histogram
        if 'sentiment' in self.results:
            plot_count += 1
            ax3 = plt.subplot(2, 3, 3)
            
            polarities = [s['polarity'] for s in self.results['sentiment']['sentiments']]
            ax3.hist(polarities, bins=20, color='purple', alpha=0.7, edgecolor='black')
            ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral')
            ax3.set_title('Sentiment Polarity Distribution', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Polarity (-1=Negative, +1=Positive)')
            ax3.set_ylabel('Frequency')
            ax3.legend()
        
        # Plot 4: Text length distribution
        if self.text_data:
            plot_count += 1
            ax4 = plt.subplot(2, 3, 4)
            
            lengths = [len(text.split()) for text in self.text_data]
            ax4.hist(lengths, bins=20, color='orange', alpha=0.7, edgecolor='black')
            ax4.set_title('Text Length Distribution', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Word Count')
            ax4.set_ylabel('Frequency')
        
        # Plot 5: Correlation scatter (if exists)
        if 'correlations' in self.results and self.data_df is not None:
            for corr_name, corr_data in self.results['correlations'].items():
                plot_count += 1
                ax5 = plt.subplot(2, 3, 5)
                
                if corr_data['type'] == 'sentiment_polarity':
                    column = corr_data['column']
                    polarities = [s['polarity'] for s in self.results['sentiment']['sentiments']]
                    
                    ax5.scatter(self.data_df[column], polarities, 
                              alpha=0.6, color='teal', edgecolor='black')
                    ax5.set_title(f'{column} vs Sentiment\n(r={corr_data["correlation"]:.3f})', 
                                fontsize=12, fontweight='bold')
                    ax5.set_xlabel(column)
                    ax5.set_ylabel('Sentiment Polarity')
                    
                    # Add trend line
                    z = np.polyfit(self.data_df[column], polarities, 1)
                    p = np.poly1d(z)
                    ax5.plot(self.data_df[column], p(self.data_df[column]), 
                           "r--", alpha=0.8, linewidth=2)
                
                break  # Only show first correlation
        
        # Plot 6: Top words (if text statistics exist)
        if 'text_statistics' in self.results:
            plot_count += 1
            ax6 = plt.subplot(2, 3, 6)
            
            top_words = self.results['text_statistics']['top_10_words']
            words = [w[0] for w in top_words[:8]]  # Top 8 for readability
            counts = [w[1] for w in top_words[:8]]
            
            ax6.barh(words, counts, color='steelblue', edgecolor='black')
            ax6.set_title('Top 8 Most Common Words', fontsize=12, fontweight='bold')
            ax6.set_xlabel('Frequency')
            ax6.invert_yaxis()
        
        plt.tight_layout()
        
        # raise SystemExit(output_dir)
        # Save
        output_path = Path(output_dir) / 'analysis_dashboard.png'
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Visualizations saved to {output_path}")
        
        return self
    
    def process_batch(self, file_paths: List[str], text_column: str) -> Dict:
        """
        Process multiple files in batch
        
        Args:
            file_paths: List of file paths to process
            text_column: Column containing text data
            
        Returns:
            Dictionary with aggregated results
        """
        print(f"🔄 Batch processing {len(file_paths)} files...")
        
        all_results = []
        
        for file_path in ProgressTracker.track(file_paths, "Processing files", "file"):
            try:
                # Reset pipeline
                self.data_df = None
                self.text_data = []
                self.results = {}
                
                # Process file
                self.load_structured_data(file_path)
                self.load_text_column(text_column)
                self.analyze_data()
                self.analyze_text()
                self.analyze_sentiment()
                
                # Store results
                all_results.append({
                    'file': file_path,
                    'results': self.results.copy()
                })
                
            except Exception as e:
                print(f"⚠ Error processing {file_path}: {e}")
                all_results.append({
                    'file': file_path,
                    'error': str(e)
                })
        
        print(f"✓ Batch processing complete: {len(all_results)} files processed")
        
        return {
            'total_files': len(file_paths),
            'successful': sum(1 for r in all_results if 'error' not in r),
            'failed': sum(1 for r in all_results if 'error' in r),
            'results': all_results
        }
    
    def export_results(self, format: str = 'csv', output_dir: str = 'output') -> 'UnifiedPipeline':
        """
        Export results to various formats
        
        Args:
            format: 'csv', 'json', or 'excel'
            output_dir: Directory to save exports
            
        Returns:
            Self for method chaining
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Create results DataFrame
        if self.data_df is not None:
            results_df = self.data_df.copy()
            
            # Add sentiment if available
            if 'sentiment' in self.results:
                sentiments = self.results['sentiment']['sentiments']
                results_df['sentiment_polarity'] = [s['polarity'] for s in sentiments]
                results_df['sentiment_subjectivity'] = [s['subjectivity'] for s in sentiments]
                
                # Add sentiment category
                def categorize_sentiment(polarity):
                    if polarity > 0.1:
                        return 'Positive'
                    elif polarity < -0.1:
                        return 'Negative'
                    else:
                        return 'Neutral'
                
                results_df['sentiment_category'] = results_df['sentiment_polarity'].apply(categorize_sentiment)
            
            # Add text length if text data exists
            if self.text_data:
                results_df['text_word_count'] = [len(text.split()) for text in self.text_data]
            
            # Export based on format
            if format == 'csv':
                output_path = Path(output_dir) / 'results.csv'
                results_df.to_csv(output_path, index=False)
            elif format == 'json':
                output_path = Path(output_dir) / 'results.json'
                results_df.to_json(output_path, orient='records', indent=2)
            elif format == 'excel':
                output_path = Path(output_dir) / 'results.xlsx'
                results_df.to_excel(output_path, index=False)
            else:
                print(f"⚠ Unknown format: {format}")
                return self
            
            print(f"✓ Results exported to {output_path}")
        
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
        
        # Sentiment analysis
        if 'sentiment' in self.results:
            report.append("\n\n SENTIMENT ANALYSIS")
            report.append("-" * 60)
            
            sentiment = self.results['sentiment']
            report.append(f"Average polarity: {sentiment['avg_polarity']:.3f}")
            report.append(f"Average subjectivity: {sentiment['avg_subjectivity']:.3f}")
            report.append(f"\nSentiment breakdown:")
            report.append(f"  Positive: {sentiment['positive_count']} ({sentiment['positive_count']/sentiment['total']*100:.1f}%)")
            report.append(f"  Neutral: {sentiment['neutral_count']} ({sentiment['neutral_count']/sentiment['total']*100:.1f}%)")
            report.append(f"  Negative: {sentiment['negative_count']} ({sentiment['negative_count']/sentiment['total']*100:.1f}%)")

        if 'entities' in self.results:
            report.append("\n\n NAMED ENTITIES")
            report.append("-" * 60)
            
            entities = self.results['entities']
            for entity_type, data in entities.items():
                report.append(f"\n{entity_type}:")
                report.append(f"  Total mentions: {data['total']}")
                report.append(f"  Unique entities: {data['unique']}")
                report.append("  Top mentions:")
                for entity, count in data['top_5']:
                    report.append(f"    • {entity}: {count}")
        
        # Keywords
        if 'keywords' in self.results:
            report.append("\n\n KEYWORDS")
            report.append("-" * 60)
            
            kw = self.results['keywords']
            report.append(f"Method: {kw['method'].upper()}")
            report.append("\nTop keywords:")
            for keyword, score in kw['keywords'][:10]:
                report.append(f"  • {keyword}: {score:.3f}")
        
        # Topics
        if 'topics' in self.results:
            report.append("\n\n TOPICS")
            report.append("-" * 60)
            
            topics = self.results['topics']
            for topic, keywords in topics.items():
                report.append(f"\n{topic.upper()}:")
                for keyword, score in keywords[:5]:
                    report.append(f"  • {keyword}: {score:.3f}")
        
        # Complexity
        if 'complexity' in self.results:
            report.append("\n\n TEXT COMPLEXITY")
            report.append("-" * 60)
            
            comp = self.results['complexity']
            report.append(f"Flesch Reading Ease: {comp['avg_flesch_reading_ease']}")
            report.append(f"Grade Level: {comp['avg_flesch_kincaid_grade']}")
            report.append(f"Interpretation: {comp['interpretation']}")
            report.append(f"Avg words/sentence: {comp['avg_words_per_sentence']}")

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