import torch
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from bs4 import BeautifulSoup
import os
import re


class ArticleSummarizer:
    def __init__(self):
        # Load model and tokenizer
        self.model_name = "facebook/bart-large-cnn"
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name)

        # Set device (use GPU if available)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)

    def clean_text(self, text):
        """Clean the text by removing extra whitespaces, special characters, etc."""
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()

        # Add more cleaning as needed

        return text

    def extract_text_from_url(self, url):
        """Extract article text from a given URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            # Get text
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])

            return self.clean_text(article_text)

        except Exception as e:
            return f"Error extracting text from URL: {str(e)}"

    def summarize(self, text, max_length=150, min_length=50):
        """Generate a summary of the given text."""
        # Clean the text
        text = self.clean_text(text)

        # Tokenize and prepare for model
        inputs = self.tokenizer.encode("summarize: " + text,
                                       return_tensors="pt",
                                       max_length=1024,
                                       truncation=True).to(self.device)

        # Generate summary
        summary_ids = self.model.generate(inputs,
                                          max_length=max_length,
                                          min_length=min_length,
                                          length_penalty=2.0,
                                          num_beams=4,
                                          early_stopping=True)

        # Decode the summary
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

    def chunk_long_text(self, text, chunk_size=900):
        """Split text into chunks for long articles."""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def summarize_long_text(self, text, max_length=150, min_length=50):
        """Handle long texts by chunking and summarizing separately."""
        if len(text.split()) <= 1000:
            return self.summarize(text, max_length, min_length)

        # Split text into chunks
        chunks = self.chunk_long_text(text)

        # Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            summary = self.summarize(chunk, max_length=100, min_length=30)
            chunk_summaries.append(summary)

        # Combine chunk summaries and create a final summary
        combined_summary = ' '.join(chunk_summaries)

        # Final summary of the combined summaries
        if len(combined_summary.split()) > 500:
            final_summary = self.summarize(combined_summary, max_length, min_length)
            return final_summary

        return combined_summary