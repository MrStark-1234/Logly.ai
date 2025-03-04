import argparse
import yaml
from datetime import datetime
import json
from typing import Dict, Any

from .sources.aws_cloudwatch import CloudWatchLogSource
from .sources.apache import ApacheLogSource
from .sources.mock_cloudwatch import MockCloudWatchSource

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_log_source(source_type: str, config: Dict[str, Any]):
    """Get the appropriate log source based on type"""
    sources = {
        'cloudwatch': CloudWatchLogSource,
        'apache': ApacheLogSource,
        'mock-cloudwatch': MockCloudWatchSource
    }
    
    if source_type not in sources:
        raise ValueError(f"Unsupported log source type: {source_type}")
        
    return sources[source_type](config)

def main():
    parser = argparse.ArgumentParser(description='Log ingestion tool')
    parser.add_argument('--config', required=True, help='Path to configuration YAML file')
    parser.add_argument('--source', required=True, 
                      choices=['cloudwatch', 'apache', 'mock-cloudwatch'], 
                      help='Log source type')
    parser.add_argument('--start-time', help='Start time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--end-time', help='End time (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--output', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    # Parse times if provided
    start_time = None
    end_time = None
    if args.start_time:
        start_time = datetime.strptime(args.start_time, '%Y-%m-%d %H:%M:%S')
    if args.end_time:
        end_time = datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S')
    
    # Load configuration
    config = load_config(args.config)
    
    # Get and use log source
    with get_log_source(args.source, config) as source:
        # Open output file if specified
        output_file = open(args.output, 'w') if args.output else None
        try:
            for log in source.read_logs(start_time, end_time):
                # Convert datetime objects to string for JSON serialization
                log['timestamp'] = log['timestamp'].isoformat()
                
                # Write to output
                if output_file:
                    output_file.write(json.dumps(log) + '\n')
                else:
                    print(json.dumps(log))
        finally:
            if output_file:
                output_file.close()

if __name__ == '__main__':
    main() 