I want to parse a website for its content and then create a knowledge base of this data.
I would then want to create a llm based chatbot that can answer questions about this knowledge base.

Step 1: Website Parsing (Data Extraction)
    I want to c a website for its main content and store it in a structured format. The website may contain dynamic content (JavaScript). Write a Python script using the `crawl4ai`  (https://docs.crawl4ai.com/)library to:
    1. Crawl a given URL and extract the main content (text, HTML, and metadata).
    2. Handle pagination if the website has multiple pages.
    3. Save the extracted content into a JSON file for further processing.
    4. Include error handling for failed requests and rate limiting to avoid IP bans.

    Provide the code with detailed comments explaining each step.

Step 2: Data Preprocessing
    I have scraped website content stored in a JSON file. Write a Python script to preprocess this data:
    1. Clean the text by removing duplicates, extra whitespace, and non-text elements (e.g., ads, navigation links).
    2. Split the text into smaller chunks of 500-1000 tokens using LangChain's `RecursiveCharacterTextSplitter`, with an overlap of 200 tokens to preserve context.
    3. Add metadata (e.g., source URL, timestamp) to each chunk for traceability.
    4. Save the preprocessed data into a new JSON file.

    Provide the code with detailed comments explaining each step.

Step 3: Embeddings & Knowledge Base Storage
    I have preprocessed text chunks stored in a JSON file. Write a Python script to:
    1. Generate embeddings for each chunk using OpenAI's `text-embedding-3-small` model.
    2. Store the embeddings and associated metadata in a vector database (e.g., Chroma or FAISS).
    3. Optimize the vector database for fast similarity search (e.g., using HNSW indexing in FAISS).
    4. Save the vector database to disk for later use.

    Provide the code with detailed comments explaining each step.

Step 4: Chatbot Development (RAG Pipeline)
    I have a vector database containing text embeddings and metadata. Write a Python script to create a Retrieval-Augmented Generation (RAG) pipeline:
    1. Convert user queries into embeddings using the same model used for the knowledge base.
    2. Perform a similarity search in the vector database to retrieve the top-k most relevant chunks.
    3. Pass the retrieved chunks and the user query to an LLM (e.g., GPT-4) to generate a response.
    4. Add safeguards to handle out-of-scope questions (e.g., "I don't have information on that").
    5. Cache frequent queries to reduce latency and costs.

    Provide the code with detailed comments explaining each step.

Step 5: Testing & Validation
    I have built a RAG-based chatbot. Write a Python script to:
    1. Test the chatbot with a set of sample queries (e.g., 10-20 questions).
    2. Evaluate the responses based on precision (relevance of answers) and recall (coverage of correct information).
    3. Log the queries, responses, and evaluation metrics for analysis.
    4. Provide suggestions for improving the chatbot based on the test results.

    Provide the code with detailed comments explaining each step.

Step 6: Deployment & Scaling
    I have a RAG-based chatbot that works locally. Write a Python script to:
    1. Deploy the chatbot as a REST API using FastAPI or Flask.
    2. Add rate limiting and authentication to the API for security.
    3. Create a simple frontend using Streamlit or Gradio for user interaction.
    4. Monitor API usage, response quality, and system health using logging and Prometheus.

    Provide the code with detailed comments explaining each step.

Step 7: Maintenance
    I have deployed a RAG-based chatbot. Write a Python script to:
    1. Schedule periodic re-crawling of the website to refresh the knowledge base.
    2. Automate the process of updating embeddings and the vector database.
    3. Send alerts for scraping failures, LLM API issues, or other errors.
    4. Log user interactions to improve retrieval and model performance over time.

    Provide the code with detailed comments explaining each step.