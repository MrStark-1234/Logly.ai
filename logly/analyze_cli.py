import argparse
import os
from .analysis.gemini_analyzer import GeminiAnalyzer

def main():
    parser = argparse.ArgumentParser(description='Interactive log analysis using Gemini API')
    parser.add_argument('--logs', required=True, help='Path to log file')
    parser.add_argument('--api-key', help='Gemini API key (can also be set via GEMINI_API_KEY env variable)')
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Gemini API key must be provided via --api-key or GEMINI_API_KEY environment variable")
    
    # Initialize analyzer and load logs
    analyzer = GeminiAnalyzer(api_key)
    analyzer.load_logs_from_file(args.logs)
    
    print("Log analysis session started. Type 'exit' to quit.")
    print("You can ask questions about your logs, for example:")
    print("- What are the most common types of events?")
    print("- Are there any error patterns?")
    print("- What happened between 2:00 PM and 3:00 PM?")
    print()
    
    while True:
        try:
            question = input("\nWhat would you like to know about your logs? > ")
            if question.lower() in ['exit', 'quit']:
                break
                
            response = analyzer.ask_sync(question)
            print("\nAnalysis:", response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            
    print("\nLog analysis session ended.")

if __name__ == '__main__':
    main() 