import argparse
import sys
from pathlib import Path
from colorama import Fore, Style, init

init()

from unified_pipeline import UnifiedPipeline

def print_success(msg):
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}! {msg}{Style.RESET_ALL}")

def print_header(msg):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{msg}")
    print(f"{'='*60}{Style.RESET_ALL}\n")

def run_pipeline(args):
    print_header("UNIFIED DATA + TEXT PIPELINE")

    try:
        # Initialize pipeline
        pipeline = UnifiedPipeline()
        
        # Step 1: Load structured data
        if args.data_file:
            print_info("Loading structured data...")
            pipeline.load_structured_data(args.data_file)
            print_success(f"Loaded data from {args.data_file}")
        else:
            print_error("No data file provided. Use --data-file")
            sys.exit(1)
        
        # Step 2: Load text data
        if args.text_column:
            print_info(f"Extracting text from column '{args.text_column}'...")
            pipeline.load_text_column(args.text_column)
            print_success(f"Extracted text from '{args.text_column}'")
        elif args.text_file:
            print_info("Loading text from file...")
            pipeline.load_text_file(args.text_file)
            print_success(f"Loaded text from {args.text_file}")
        else:
            print_warning("No text data specified. Analyzing data only.")
        
        # Step 3: Clean data
        if args.clean:
            print_header("CLEANING DATA")
            pipeline.clean_data(strategy=args.clean_strategy)
            
            if pipeline.text_data:
                pipeline.clean_text()
            
            print_success("Data cleaned")
        
        # Step 4: Analyze
        print_header("ANALYZING")
        
        if args.analyze_data or args.all:
            pipeline.analyze_data()
        
        if args.analyze_text or args.all:
            if pipeline.text_data:
                pipeline.analyze_text()
            else:
                print_warning("No text data to analyze")
        
         # Sentiment analysis
        if args.sentiment or args.all:
            if pipeline.text_data:
                print_header("SENTIMENT ANALYSIS")
                pipeline.analyze_sentiment()
                
                # Correlate with data if specified
                if args.correlate:
                    pipeline.correlate_sentiment_with_column(args.correlate)
            else:
                print_warning("No text data for sentiment analysis")
        
        # Create visualizations
        if args.visualize or args.all:
            print_header("CREATING VISUALIZATIONS")
            pipeline.create_visualizations(args.output.replace('.txt', '').replace('unified_report', 'output'))
        
        # Export results
        if args.export:
            print_header(f"EXPORTING TO {args.export.upper()}")
            pipeline.export_results(format=args.export, 
                                   output_dir=args.output.replace('.txt', '').replace('unified_report', 'output'))
            
        # Step 5: Correlation analysis
        if args.correlate:
            if pipeline.text_data:
                print_info(f"Calculating correlation with '{args.correlate}'...")
                pipeline.correlate_data_with_text_length(args.correlate)
            else:
                print_warning("Need text data for correlation analysis")
        
        # Step 6: Generate report
        print_header("GENERATING REPORT")
        report = pipeline.generate_report()
        print(report)
        
        # Step 7: Save output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pipeline.save_report(str(output_path))
            print_success(f"Report saved to {args.output}")
        
        # Summary
        summary = pipeline.get_summary()
        print_header("PIPELINE SUMMARY")
        print(f" Data rows: {summary['data_rows']}")
        print(f" Data columns: {summary['data_columns']}")
        print(f" Text entries: {summary['text_entries']}")
        
        print_header("✓ PIPELINE COMPLETE")
        
    except FileNotFoundError as e:
        print_error(f"File not found: {e}")
        sys.exit(1)
    except ValueError as e:
        print_error(f"Value error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Unified Data + Text Processing Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
                # Full analysis with sentiment
                python cli.py --data-file products.csv --text-column review --all
                
                # Sentiment + correlation with rating
                python cli.py --data-file reviews.csv --text-column text --sentiment --correlate rating
                
                # Create visualizations
                python cli.py --data-file data.csv --text-column feedback --all --visualize
                
                # Export results
                python cli.py --data-file data.csv --text-column text --all --export csv
        """
    )
    
    # Input files
    parser.add_argument('--data-file', '-d', type=str,
                       help='Structured data file (CSV, Excel, JSON)')
    parser.add_argument('--text-column', '-t', type=str,
                       help='Column name containing text data')
    parser.add_argument('--text-file', type=str,
                       help='Separate text file (alternative to text-column)')
    
    # Processing options
    parser.add_argument('--clean', '-c', action='store_true',
                       help='Clean data and text')
    parser.add_argument('--clean-strategy', type=str,
                       choices=['drop', 'fill', 'forward_fill'],
                       default='drop',
                       help='Strategy for handling missing values')
    
    # Analysis options
    parser.add_argument('--analyze-data', action='store_true',
                       help='Analyze structured data')
    parser.add_argument('--analyze-text', action='store_true',
                       help='Analyze text data')
    parser.add_argument('--sentiment', action='store_true',
                       help='Analyze sentiment of text')
    parser.add_argument('--visualize', action='store_true',
                       help='Create visualization dashboard')
    parser.add_argument('--export', type=str,
                       choices=['csv', 'json', 'excel'],
                       help='Export results to file')
    parser.add_argument('--correlate', type=str,
                       help='Correlate specified column with text length')
    
    # Output
    parser.add_argument('--output', '-o', type=str,
                       default='output/unified_report.txt',
                       help='Output file for report')
    
    # Shortcuts
    parser.add_argument('--all', '-a', action='store_true',
                       help='Run complete analysis (data + text + correlation)')
    
    args = parser.parse_args()
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    try:
        run_pipeline(args)
    except KeyboardInterrupt:
        print_warning("\n\nInterrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()