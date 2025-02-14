import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

class TextPreprocessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Split into chunks of 1000 characters
            chunk_overlap=200,  # 200 character overlap between chunks
            length_function=len,
            is_separator_regex=False,
        )

    def load_data(self):
        """Load data from the input JSON file."""
        with open(self.input_file, 'r') as f:
            data = json.load(f)
        return data.get('markdown', '')

    def clean_text(self, text):
        """Clean the text by removing extra whitespace, URLs, and non-text elements."""
        import re

        # Remove markdown links and images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
        text = re.sub(r'\[.*?\]\(.*?\)', '', text)    # Remove links
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Remove navigation elements
        text = re.sub(r'\[.*?\]', '', text)  # Remove remaining markdown-style brackets
        text = re.sub(r'\{.*?\}', '', text)  # Remove curly braces content
        
        # Remove unicode emojis
        text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)
        
        # Remove extra whitespace and newlines
        text = ' '.join(text.split())
        
        # Remove any remaining special characters
        text = re.sub(r'[^a-zA-Z0-9\s.,;:?!-]', '', text)
        
        return text.strip()

    def process(self):
        """Process the text data: clean, split into chunks, and add metadata."""
        try:
            # Load and clean the text
            text = self.load_data()
            cleaned_text = self.clean_text(text)

            # Split the text into chunks
            chunks = self.text_splitter.split_text(cleaned_text)

            # Add metadata to each chunk
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    'content': chunk,
                    'metadata': {
                        'chunk_id': i,
                        'source': self.input_file,
                        'timestamp': datetime.now().isoformat(),
                        'chunk_size': len(chunk),
                    }
                }
                processed_chunks.append(chunk_data)

            # Save the processed chunks
            with open(self.output_file, 'w') as f:
                json.dump(processed_chunks, f, indent=4)

            print(f"Successfully processed {len(processed_chunks)} chunks")
            print(f"Saved processed data to {self.output_file}")

        except Exception as e:
            print(f"Error processing text: {e}")

if __name__ == "__main__":
    # Process the crawled data
    preprocessor = TextPreprocessor('crawled_data.json', 'processed_data.json')
    preprocessor.process()
