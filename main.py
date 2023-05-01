import configparser
from collections import Counter

import nltk.data
import openai
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from nltk import sent_tokenize

# Check if the 'punkt' resource is already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load the API keys and CSE ID from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

openai_api_key = config.get('openai', 'api_key')
engine = config.get('openai', 'engine')
google_api_key = config.get('google', 'api_key')
google_cse_id = config.get('google', 'cse_id')


# Function to search the web for the given query and return the first 5 unique URLs
def search_web(query):
    urls = set()
    try:
        service = build("customsearch", "v1", developerKey=google_api_key)
        response = service.cse().list(q=query, cx=google_cse_id, num=5).execute()
        for item in response['items']:
            urls.add(item['link'])
    except Exception as e:
        print(f"Error searching the web: {e}")
    return list(urls)


# Function to scrape the content of the URLs and save it to summary.txt
def scrape_and_save(urls):
    content = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'}

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            content += soup.get_text() + "\n\n"
        except Exception as e:
            print(f"Error scraping URL {url}: {e}")

    with open('summary.txt', 'w') as f:
        f.write(content)


# Function to summarize findings from summary.txt
def summarize_findings(text, top_n_sentences=5):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Count the occurrences of each sentence
    counter = Counter(sentences)

    # Get the top_n_sentences most common sentences
    most_common_sentences = counter.most_common(top_n_sentences)
    summary = ' '.join([sentence[0] for sentence in most_common_sentences])

    return summary


# Function to generate a response from OpenAI API
def generate_description(prompt):
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            n=1,
            stop=None,
            temperature=0.6
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating description from OpenAI API: {e}")
        return ""


# Main function
def main():
    mode = input("Choose the mode: (1) Search and scrape, (2) Read from summary.txt: ")

    urls = []

    if mode == '1':
        query = input("Enter your search term: ")
        urls = search_web(query)
        print("Searching...", urls)
        scrape_and_save(urls)

        with open('summary.txt', 'r') as f:
            summary_content = f.read()

        # Summarize the content of summary.txt
        print("Summarising findings...")
        summary_content = summarize_findings(summary_content)

        # Save the summarized content back to summary.txt
        with open('summary.txt', 'w') as f:
            f.write(summary_content)

    elif mode == '2':
        with open('summary.txt', 'r') as f:
            summary_content = f.read()

    else:
        print("Invalid mode selected. Exiting.")
        return

    with open('prompt.txt', 'r') as f:
        prompt_content = f.read()

    # Create a variable consisting of the content of prompt.txt and summary.txt, connected with \n\n
    prompt = f"{prompt_content}\n\n{summary_content}"
    print("Sending the query to OpenAI...")

    # Pass the prompt to OpenAI API
    description = generate_description(prompt)

    # Include the URLs in the description
    if urls:
        urls_string = "\n".join(urls)
        description_with_urls = f"{description}\n\nURLs found from the search:\n{urls_string}"
    else:
        description_with_urls = f"{description}\n\nNo URLs were used."

    # Save the whole response with URLs to description.txt
    with open('description.txt', 'w') as f:
        f.write(description_with_urls)
    print("Please find the response in description.txt.\nThank you!")


if __name__ == "__main__":
    main()
