import google.generativeai as genai
import json
from typing import List, Dict, Any
import os

class GeminiAnalyzer:
    """Analyzes logs using Google's Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini analyzer
        
        Args:
            api_key: Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.logs = []
        self.chat = None
        
    def load_logs(self, logs: List[Dict[str, Any]]):
        """
        Load logs for analysis
        
        Args:
            logs: List of log entries
        """
        self.logs = logs
        # Initialize chat with context about the logs
        log_summary = f"I have loaded {len(logs)} log entries. Each log entry contains: timestamp, message, "
        if 'log_stream_name' in logs[0]:
            log_summary += "log stream name, and event ID. "
        else:
            log_summary += "and other metadata. "
        
        self.chat = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": [f"You are a log analysis assistant. {log_summary} I will ask you questions about these logs."]
            },
            {
                "role": "model",
                "parts": ["I understand that I'm analyzing log data. I can help you extract insights, identify patterns, troubleshoot issues, and answer questions about the logs. What would you like to know about the log entries?"]
            }
        ])
    
    def load_logs_from_file(self, file_path: str):
        """
        Load logs from a JSON file
        
        Args:
            file_path: Path to JSON log file
        """
        with open(file_path, 'r') as f:
            logs = [json.loads(line) for line in f]
        self.load_logs(logs)
    
    def ask_sync(self, question: str) -> str:
        """
        Ask a question about the logs
        
        Args:
            question: Question about the logs
            
        Returns:
            Gemini's response
        """
        if not self.chat:
            raise RuntimeError("No logs loaded. Call load_logs() first.")
            
        # Prepare context for the question
        context = f"Based on the loaded logs, please answer this question: {question}\n\n"
        context += "Here are some relevant log entries that might help:\n"
        
        # Add relevant log entries as context
        for log in self.logs[:10]:
            context += json.dumps(log) + "\n"
            
        response = self.chat.send_message(context)
        return response.text 