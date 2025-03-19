from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List, Union
import re

mcp = FastMCP("Formatter")

@mcp.tool()
def format_message(text: str, style: str = "default") -> str:
    """
    Format any text into a clean, human-readable message.
    
    Args:
        text: The text to format
        style: Formatting style ('default', 'concise', 'detailed')
        
    Returns:
        A formatted, human-readable message
    """
    # Use a language model-like prompt to format the message
    if style == "concise":
        return create_concise_message(text)
    elif style == "detailed":
        return create_detailed_message(text)
    else:  # default
        return create_default_message(text)

@mcp.tool()
def summarize(text: str, max_length: int = 200) -> str:
    """
    Summarize text to a specified maximum length.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of the summary
        
    Returns:
        A summarized version of the input text
    """
    # Simple summarization by truncating and adding ellipsis if needed
    if len(text) <= max_length:
        return text
    
    # Try to find a sentence boundary near the max_length
    sentences = re.split(r'(?<=[.!?])\s+', text[:max_length + 50])
    summary = ""
    
    for sentence in sentences:
        if len(summary) + len(sentence) <= max_length:
            summary += sentence + " "
        else:
            break
    
    if summary:
        return summary.strip()
    else:
        # If no good sentence boundary, just truncate
        return text[:max_length - 3] + "..."

@mcp.tool()
def highlight_key_points(text: str) -> str:
    """
    Extract and highlight key points from text.
    
    Args:
        text: The text to analyze
        
    Returns:
        A formatted message with highlighted key points
    """
    # Simple key point extraction based on common patterns
    key_points = []
    
    # Look for sentences with indicator phrases
    indicators = [
        "important", "key", "critical", "essential", "significant",
        "note that", "remember", "notably", "specifically", "in particular"
    ]
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        # Check if sentence contains any indicator words
        if any(indicator.lower() in sentence.lower() for indicator in indicators):
            key_points.append(sentence)
        # Check for numbered or bulleted points
        elif re.match(r'^\s*[\d*-]+\s+', sentence):
            key_points.append(sentence)
    
    # If no key points found, take first and last sentences as summary
    if not key_points and len(sentences) > 1:
        key_points = [sentences[0], sentences[-1]]
    elif not key_points and sentences:
        key_points = [sentences[0]]
    
    if key_points:
        result = "Key Points:\n"
        for i, point in enumerate(key_points, 1):
            result += f"{i}. {point}\n"
        return result
    else:
        return "No key points identified in the text."

# Helper functions for formatting
def create_concise_message(text: str) -> str:
    """Create a concise, to-the-point message."""
    # Remove excessive whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    
    # Format each paragraph
    formatted_paragraphs = []
    for para in paragraphs:
        # Remove redundant phrases
        para = re.sub(r'(?i)(please note that|as you can see|it is worth mentioning that)', '', para)
        formatted_paragraphs.append(para.strip())
    
    # Join paragraphs with proper spacing
    return "\n\n".join(formatted_paragraphs)

def create_detailed_message(text: str) -> str:
    """Create a detailed, structured message."""
    # Normalize line breaks
    text = re.sub(r'\r\n|\r', '\n', text)
    
    # Split into paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    
    # Format each paragraph
    formatted_text = ""
    for i, para in enumerate(paragraphs):
        # Add section headers for longer texts
        if len(paragraphs) > 1 and len(para.split()) > 10:
            formatted_text += f"Section {i+1}:\n"
        
        # Format paragraph
        formatted_text += para.strip() + "\n\n"
    
    return formatted_text.strip()

def create_default_message(text: str) -> str:
    """Create a balanced, readable message."""
    # Normalize line breaks
    text = re.sub(r'\r\n|\r', '\n', text)
    
    # Remove excessive whitespace
    text = re.sub(r' +', ' ', text)
    
    # Ensure proper spacing after punctuation
    text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
    
    # Split into paragraphs and format
    paragraphs = re.split(r'\n\s*\n', text)
    formatted_paragraphs = [para.strip() for para in paragraphs]
    
    # Join paragraphs with proper spacing
    return "\n\n".join(formatted_paragraphs)

if __name__ == "__main__":
    mcp.run(transport="stdio")
