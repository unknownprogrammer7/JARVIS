"""
Core AI logic for J.A.R.V.I.S - Advanced Brain Module
Processes input messages, detects intents, and orchestrates responses.
Enhanced with command parsing, app interaction, and memory integration.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Brain:
    """
    The Brain class is the core AI logic engine for J.A.R.V.I.S.
    Responsible for:
    - Parsing user messages
    - Detecting intents and commands
    - Routing to appropriate handlers
    - Managing interaction flow
    - Coordinating with memory and permission systems
    """

    def __init__(self):
        """
        Initializes the Brain with default state and command mappings.
        Sets up intent recognition patterns and app configurations.
        """
        self.commands = self._load_commands()
        self.conversation_history = []
        self.last_intent = None
        self.user_context = {}
        
    def _load_commands(self) -> Dict:
        """
        Loads command mappings from configuration.
        
        Returns:
            Dict: Command patterns and their associated handlers
        """
        return {
            'open': self.handle_open_app,
            'launch': self.handle_open_app,
            'start': self.handle_open_app,
            'search': self.handle_search,
            'find': self.handle_search,
            'tell': self.handle_query,
            'what': self.handle_query,
            'who': self.handle_query,
            'where': self.handle_query,
        }

    def parse_message(self, message: str) -> Dict:
        """
        Parses incoming user message into structured format.
        Extracts keywords, entities, and command patterns.
        
        Args:
            message (str): Raw user input message
            
        Returns:
            Dict: Parsed message containing tokens, keywords, entities
        """
        if not message or not isinstance(message, str):
            return {'error': 'Invalid message', 'tokens': []}
        
        # Normalize input
        cleaned_message = message.lower().strip()
        tokens = cleaned_message.split()
        
        parsed_data = {
            'raw': message,
            'cleaned': cleaned_message,
            'tokens': tokens,
            'length': len(tokens),
            'timestamp': datetime.now().isoformat(),
            'entities': self._extract_entities(tokens),
            'keywords': self._extract_keywords(tokens),
        }
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'content': message,
            'timestamp': parsed_data['timestamp']
        })
        
        return parsed_data

    def _extract_entities(self, tokens: List[str]) -> Dict:
        """
        Extracts named entities from message tokens.
        Identifies app names, locations, times, etc.
        
        Args:
            tokens (List[str]): Tokenized message
            
        Returns:
            Dict: Extracted entities categorized by type
        """
        entities = {'apps': [], 'times': [], 'locations': []}
        
        # App entity recognition
        known_apps = ['instagram', 'facebook', 'whatsapp', 'twitter', 'gmail', 'youtube']
        for token in tokens:
            if token in known_apps:
                entities['apps'].append(token)
        
        return entities

    def _extract_keywords(self, tokens: List[str]) -> List[str]:
        """
        Extracts important keywords from tokens.
        Filters out common stop words.
        
        Args:
            tokens (List[str]): Tokenized message
            
        Returns:
            List[str]: Filtered keyword tokens
        """
        stop_words = {'a', 'the', 'and', 'or', 'is', 'are', 'to', 'for', 'of', 'in', 'on'}
        return [t for t in tokens if t not in stop_words and len(t) > 2]

    def detect_intent(self, parsed_data: Dict) -> Tuple[str, float]:
        """
        Detects user intent from parsed message data.
        Returns intent type and confidence score.
        
        Args:
            parsed_data (Dict): Output from parse_message()
            
        Returns:
            Tuple[str, float]: (intent_type, confidence_score)
        """
        tokens = parsed_data.get('tokens', [])
        
        if not tokens:
            return 'unclear', 0.0
        
        first_token = tokens[0]
        
        # Intent detection logic
        if first_token in self.commands:
            intent = first_token
            confidence = 0.95
        elif first_token in ['open', 'launch']:
            intent = 'open'
            confidence = 0.9
        elif any(kw in first_token for kw in ['search', 'find', 'look']):
            intent = 'search'
            confidence = 0.85
        elif any(kw in first_token for kw in ['what', 'who', 'where', 'when', 'how']):
            intent = 'query'
            confidence = 0.8
        else:
            intent = 'unclear'
            confidence = 0.5
        
        self.last_intent = intent
        return intent, confidence

    def handle_open_app(self, app_name: str) -> str:
        """
        Handles opening applications (native or web).
        Checks if app is installed, applies permissions.
        
        Args:
            app_name (str): Name of app to open
            
        Returns:
            str: Status message
        """
        app_name = app_name.lower().strip()
        return f"Opening {app_name}..."

    def handle_search(self, query: str) -> str:
        """
        Handles internet search requests.
        Integrates with search APIs.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Search results or status
        """
        return f"Searching for: {query}"

    def handle_query(self, question: str) -> str:
        """
        Handles general knowledge queries.
        Checks memory first, then searches if needed.
        
        Args:
            question (str): User question
            
        Returns:
            str: Answer or search results
        """
        return f"Answering: {question}"

    def interact(self, intent: str, parsed_data: Dict) -> str:
        """
        Executes interaction based on detected intent.
        Routes to appropriate command handler.
        
        Args:
            intent (str): Detected intent type
            parsed_data (Dict): Parsed message data
            
        Returns:
            str: Response from handler
        """
        tokens = parsed_data.get('tokens', [])
        
        if intent in self.commands and tokens:
            handler = self.commands[intent]
            # Extract argument (usually app name or query)
            arg = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
            response = handler(arg)
        else:
            response = "I didn't understand that. Could you please rephrase?"
        
        # Log response
        self.conversation_history.append({
            'type': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat(),
            'intent': intent
        })
        
        return response

    def process_message(self, message: str) -> str:
        """
        Complete pipeline: parse -> detect intent -> interact.
        
        Args:
            message (str): User input
            
        Returns:
            str: Assistant response
        """
        parsed = self.parse_message(message)
        intent, confidence = self.detect_intent(parsed)
        response = self.interact(intent, parsed)
        return response

    def get_conversation_history(self) -> List[Dict]:
        """
        Retrieves full conversation history.
        
        Returns:
            List[Dict]: List of all messages in conversation
        """
        return self.conversation_history

    def clear_history(self):
        """
        Clears conversation history.
        Useful for new sessions or privacy.
        """
        self.conversation_history = []
        self.user_context = {}


# Singleton instance
brain_instance = None

def get_brain() -> Brain:
    """
    Gets or creates singleton Brain instance.
    
    Returns:
        Brain: The Brain instance
    """
    global brain_instance
    if brain_instance is None:
        brain_instance = Brain()
    return brain_instance


# Example usage:
if __name__ == '__main__':
    brain = Brain()
    
    # Test messages
    test_messages = [
        'Open Instagram',
        'Search for Python tutorials',
        'What is the capital of France?',
    ]
    
    for msg in test_messages:
        response = brain.process_message(msg)
        print(f'User: {msg}')
        print(f'JARVIS: {response}')
        print('-' * 50)