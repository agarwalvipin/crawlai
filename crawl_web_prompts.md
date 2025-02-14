Step 1: Recursive Crawling with crawl4ai
    Write a Python script using the `crawl4ai` library (/home/vipin/projects/crawlai/venv/lib/python3.12/site-packages/crawl4ai) to recursively crawl a website and extract the main content from all its pages. The script should:
    1. use most features from crawl4ai to make the process as easy as possible. I think you should go through all python files in /home/vipin/projects/crawlai/venv/lib/python3.12/site-packages/crawl4ai to have more context of this library.
    2. Start from a given URL and crawl all pages within the same domain.
    3. Use `crawl4ai`'s auto-detection feature to extract the main content (text, HTML, and metadata) from each page.
    4. Avoid revisiting the same page by maintaining a list of visited URLs.
    5. Respect the website's `robots.txt` and add a delay between requests to avoid overloading the server.
    6. Save the extracted content (URL, text, and metadata) into a JSON file for further processing.

    Provide the code with detailed comments explaining each step.

Step 2: Handling Pagination and Dynamic Content
    Some websites use pagination (e.g., "Next Page" buttons) or dynamic content loading (e.g., infinite scroll). Write a Python script using `crawl4ai` to:
    1. Detect and follow pagination links to crawl all pages in a sequence.
    2. Handle dynamic content loading by simulating user interactions (e.g., scrolling, clicking buttons).
    3. Save the extracted content into a structured format (e.g., JSON).

    Provide the code with detailed comments explaining each step.

Step 3: Filtering Irrelevant Pages
    During recursive crawling, some pages (e.g., "Contact Us", "Privacy Policy") may not contain useful content. Write a Python script to:
    1. Use an LLM (e.g., GPT-4) to classify pages as "relevant" or "irrelevant" based on their content.
    2. Filter out irrelevant pages and save only the relevant ones.
    3. Add metadata (e.g., page title, category) to the relevant pages.

    Provide the code with detailed comments explaining each step.

Step 4: Saving and Organizing Data
    Write a Python script to organize and save the crawled data:
    1. Group pages by category (e.g., blog posts, product pages).
    2. Save the content into a structured format (e.g., JSON or CSV) with the following fields:
    - URL
    - Title
    - Main Content
    - Metadata (e.g., timestamp, category)
    3. Compress the data into a single file (e.g., `.zip`) for easy storage and sharing.

    Provide the code with detailed comments explaining each step.