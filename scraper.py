import requests
from bs4 import BeautifulSoup

def scrape_and_process_text(link):
    # Send a GET request to the provided link
    response = requests.get(link)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all relevant elements (headings and paragraphs)
    elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
    
    processed_text = ""
    for element in elements:
        # Extract text from each element, stripping extra whitespace
        text = element.get_text(strip=True)
        if text:
            # Append the text to the processed_text variable with double newlines
            processed_text += f"{text}\n\n"

    # Return the processed text, removing any trailing newlines
    return processed_text.strip()

def save_scraped_text(filepath, text):
    # Open a file at the specified filepath and write the scraped text to it
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)