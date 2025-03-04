# Logly - Log Ingestion Tool

A Python-based tool for ingesting logs from various sources including AWS CloudWatch and Apache logs, with AI-powered analysis using Google's Gemini API.

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setting up Gemini API

Before using the log analysis features, you need to set up your Gemini API key:

```bash
# Set the API key in your terminal
export GEMINI_API_KEY=your_actual_api_key_here

# Verify the API key is set
echo $GEMINI_API_KEY
```

To make the API key persistent, add it to your shell configuration file:
- For bash users: Add to `~/.bashrc`
- For zsh users: Add to `~/.zshrc`

## Usage

The tool can be used via command line interface:

```bash
python -m logly.cli --config <config_file> --source <source_type> [--start-time "YYYY-MM-DD HH:MM:SS"] [--end-time "YYYY-MM-DD HH:MM:SS"] [--output output.json]
```

### Arguments:
- `--config`: Path to YAML configuration file
- `--source`: Log source type (cloudwatch, apache, or mock-cloudwatch)
- `--start-time`: Optional start time for log retrieval
- `--end-time`: Optional end time for log retrieval
- `--output`: Optional output file path (default: stdout)

## Configuration

### Mock CloudWatch Configuration (for testing)
```yaml
# mock_cloudwatch_config.yml
num_events: 50  # Number of mock events to generate
```

### AWS CloudWatch Configuration
```yaml
# cloudwatch_config.yml
aws_access_key_id: YOUR_ACCESS_KEY
aws_secret_access_key: YOUR_SECRET_KEY
region_name: us-west-2
log_group_name: /aws/lambda/my-function
log_stream_name: 2023/04/01/[$LATEST]12345678  # Optional
```

### Apache Logs Configuration
```yaml
# apache_config.yml
log_path: /var/log/apache2/access.log
log_format: combined  # or 'common'
```

## Examples

1. Using mock CloudWatch logs (for testing without AWS credentials):
```bash
# Generate mock logs
python -m logly.cli --config mock_cloudwatch_config.yml --source mock-cloudwatch --output sample_logs.json

# Analyze the mock logs using Gemini AI
python -m logly.analyze_cli --logs sample_logs.json
```

2. Reading AWS CloudWatch logs:
```bash
python -m logly.cli --config cloudwatch_config.yml --source cloudwatch --start-time "2023-04-01 00:00:00" --output cloudwatch_logs.json
```

3. Reading Apache logs:
```bash
python -m logly.cli --config apache_config.yml --source apache --start-time "2023-04-01 00:00:00" --end-time "2023-04-02 00:00:00"
```

## AI-Powered Log Analysis

After generating logs, you can analyze them using the Gemini-powered analysis tool:

```bash
# Make sure your Gemini API key is set
export GEMINI_API_KEY=your_actual_api_key_here

# Start the analysis session
python -m logly.analyze_cli --logs your_logs.json
```

Example questions you can ask:
- "What are the most common types of events?"
- "Are there any error patterns?"
- "What happened between 2:00 PM and 3:00 PM?"
- "Show me all authentication-related events"
- "Analyze the distribution of event types"

## Output Format

Logs are output in JSON format, one log entry per line. Each log entry contains:

### CloudWatch Logs:
```json
{
    "timestamp": "2023-04-01T00:00:00+00:00",
    "message": "Log message content",
    "log_stream_name": "stream_name",
    "event_id": "event_id"
}
```

### Apache Logs:
```json
{
    "timestamp": "2023-04-01T00:00:00",
    "remote_host": "192.168.1.1",
    "request_method": "GET",
    "request_url": "/path",
    "status": 200,
    "response_bytes": "1234",
    "user_agent": "Mozilla/5.0...",
    "referer": "http://example.com"
}
```

### Mock CloudWatch Logs:
```json
{
    "timestamp": "2024-03-02T04:29:06.289095+00:00",
    "message": "Sample log message",
    "log_stream_name": "mock-stream-1",
    "event_id": "mock-event-0"
}
```

## Extending

To add support for new log sources:

1. Create a new class in the `logly/sources` directory
2. Inherit from `LogSource` base class
3. Implement the required methods: `connect()`, `read_logs()`, and `close()`
4. Add the new source type to the `get_log_source()` function in `cli.py`
