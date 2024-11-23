from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import spacy
import re
from typing import List, Dict, Tuple
from collections import defaultdict
import pandas as pd
from datetime import datetime
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

class AdvancedLogAnalyzer:
    def __init__(self):
        # Load models
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
        self.zero_shot = pipeline("zero-shot-classification")
        
        # Initialize TF-IDF
        self.tfidf = TfidfVectorizer(max_features=1000)
        
        # Attack patterns
        self.attack_patterns = {
            'sql_injection': r'(?i)(union\s+select|select\s+.*\s+from|drop\s+table)',
            'xss': r'(?i)(<script>|javascript:|onload=|onerror=)',
            'command_injection': r'(?i)(;\s*[\w\d]+\s*;|\|\s*[\w\d]+)',
            'path_traversal': r'(?i)(\.\.\/|\.\.\\|~\/)',
            'buffer_overflow': r'(?i)(A{20,}|\x00{10,})'
        }
        
    def deep_pattern_analysis(self, log_entry: str) -> Dict:
        """Perform deep pattern analysis using BERT"""
        inputs = self.tokenizer(log_entry, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        attention = outputs.attentions[-1].mean(dim=1)  # Get attention weights
        
        # Find important tokens
        important_tokens = []
        for i, weight in enumerate(attention[0]):
            if weight > 0.1:  # Threshold for importance
                token = self.tokenizer.decode([inputs['input_ids'][0][i]])
                important_tokens.append((token, float(weight)))
                
        return {
            'important_tokens': important_tokens,
            'attention_score': float(attention.mean())
        }
        
    def detect_attack_patterns(self, log_entry: str) -> List[str]:
        """Detect known attack patterns in logs"""
        detected_patterns = []
        for attack_type, pattern in self.attack_patterns.items():
            if re.search(pattern, log_entry):
                detected_patterns.append(attack_type)
        return detected_patterns
        
    def build_event_graph(self, logs: List[str]) -> nx.DiGraph:
        """Build a graph of related events"""
        G = nx.DiGraph()
        
        for i, log in enumerate(logs):
            # Add node for current log
            G.add_node(i, text=log)
            
            # Look for relationships with previous logs
            for j in range(max(0, i-5), i):
                similarity = self._calculate_similarity(logs[j], log)
                if similarity > 0.5:
                    G.add_edge(j, i, weight=similarity)
                    
        return G
        
    def _calculate_similarity(self, log1: str, log2: str) -> float:
        """Calculate similarity between two log entries"""
        doc1 = self.nlp(log1)
        doc2 = self.nlp(log2)
        return doc1.similarity(doc2)
        
    def generate_advanced_insights(self, logs: List[str]) -> Dict:
        """Generate advanced insights from log analysis"""
        insights = {
            'attack_patterns': defaultdict(int),
            'temporal_clusters': [],
            'entity_relationships': [],
            'anomaly_sequences': []
        }
        
        # Create event graph
        event_graph = self.build_event_graph(logs)
        
        # Find connected components (related events)
        for component in nx.connected_components(event_graph.to_undirected()):
            events = [event_graph.nodes[n]['text'] for n in component]
            if len(events) > 1:
                insights['temporal_clusters'].append(events)
                
        # Analyze each log entry
        for log in logs:
            # Detect attack patterns
            patterns = self.detect_attack_patterns(log)
            for pattern in patterns:
                insights['attack_patterns'][pattern] += 1
                
            # Extract entities and relationships
            doc = self.nlp(log)
            for ent1 in doc.ents:
                for ent2 in doc.ents:
                    if ent1 != ent2:
                        insights['entity_relationships'].append({
                            'source': ent1.text,
                            'target': ent2.text,
                            'type': f"{ent1.label_}-{ent2.label_}"
                        })
                        
        return insights 