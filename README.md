# AirsoftAssistant

AirsoftAssistant is a Python application that searches the web for a given term, scrapes content from the top 5 unique URLs, summarizes the findings, and generates a description using OpenAI's GPT-3 API. The summarized content and generated description are saved to text files for further use.

## Prerequisites

To run the script, you need to have Python 3 installed on your system. Additionally, the following Python packages are required:

- `google-api-python-client`
- `beautifulsoup4`
- `nltk`
- `openai`
- `requests`

You can install these packages using `pip`:

```bash
pip install google-api-python-client beautifulsoup4 nltk openai requests
```

## Configuration

You need to have API keys for both OpenAI and Google APIs. To obtain the API keys, follow these guides:

- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- [Google API Key and CSE ID](https://developers.google.com/custom-search/v1/introduction)

After obtaining the API keys, create a `config.ini` file in the project directory with the following format:

```
[openai]
api_key = your_openai_api_key
engine = gpt-3.5-turbo

[google]
api_key = your_google_api_key
cse_id = your_google_cse_id
```

Replace `your_openai_api_key`, `your_google_api_key`, and `your_google_cse_id` with the respective API keys and ID.

## Usage

Run the script using Python 3:

```bash
python main.py
```

The script will ask you to choose between two modes:

1. **Search and scrape**: The script will search the web for a given term, scrape content from the top 5 unique URLs, summarize the findings, and generate a description using OpenAI's GPT-3 API.
2. **Read from summary.txt**: The script will only read the content from `summary.txt` and generate a description using OpenAI's GPT-3 API.

**It is possible, that the results of web searches due to unrecognized formatting won't give meaningful output, however the links provided usually appear valid. On this occasion, copy and paste manually relevant descriptions found on the web (it should not be longer than 300-400 words) and paste into summary.txt, then run the script again choosing option 2.**

The generated description, along with the URLs used (if any), will be saved in the `description.txt` file.

## Adjusting Parameters

Some key parameters you might want to adjust include the number of search results to scrape (`num` parameter in `search_web()` function) and the number of sentences to include in the summary (`top_n_sentences` parameter in `summarize_findings()` function). You can adjust these parameters directly in the script.

## License

This project is licensed under the [GPL 3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Contributing

Your comments, suggestions, and contributions are welcomed! Please feel free to open an issue or submit a pull request with your improvements or ideas.
