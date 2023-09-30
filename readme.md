# Chat GPT Live

This repo uses metaphor API to search the internet for a query, then summarizes the content
retrieved from the basic internet search using an embedding model. The summarized text
that is now within ChatGPT's prompt length limit, then gets fed into OpenAI to generate a response to the
user query.


## Getting Started

To get started please make sure you have python 3.11 and poetry installed. Then
open `.env` file and put in your OpenAI and metaphor API keys.

Then run this

```
poetry install
```

After installation, run:

```
poetry run python main.py
```

## Tests

The tests are located in `/tests/` directory
