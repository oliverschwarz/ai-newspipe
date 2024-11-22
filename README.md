# A.I. Newspipe

This is a simple news pipeline from RSS to AI to Markdown. I will mainly use this for myself to gather and store interesting news on topics around LLM, machine learning, A.I. and the like.

## System requirements

I am working on a Mac so I don't know whether everything will work on a Windows computer my default. I have left the Windows world many years ago so unfortunately I will not be able to give much support. Additionally I am learning python so I may miss some details here - but I will document them as I learn them.

* Python 3.12+ (it may run with older versions)
* ChatGPT API key and subscription (you will need a different subscription than your ChatGPT Pro subscription)

## AI usage

I will extensively use A.I. assistants in this project. I will try to mark the different ones as I use them and I will try to document all prompts I use. This is mainly because I do not know python (yet), but I will also try to validate and check out the work they do (and how good they are doing it). So far I plan to use the following assistants:

* ChatGPT
* claude.ai
* Github Copilot
* LLama (running locally with a smaller model)

I will mention each A.I. I will use as contributor in the file-level documentation header. If necessary, I will add them to inline comments as well.

## Rough requirements for version 1 (out of my head)

The general idea is to fetch RSS feeds from various sources, put them into a lightweight format without losing the information about the source, push them to the ChatGPT API with a custom prompt to ask for filtering and summarizing. Then taking the response, transfer it into Markdown format and store them in a local file (with more options to publish it later). I want to run this with `cron` every morning. I want to develop test-driven and will start KISS but will move into more object orientation and modularization soon. Different maturity states are marked within the versions of the code.

* Using pytest
* Versioning uses semver
* RSS URLs are stored in a seperate file
* Extensive error handling to help finding problems
* As lightweight as possible

## What I learn

In this section I will document what I come across and what I have to look up. I will note this here for later so that I do not lose focus.

* What is docstring? (Probably some documentation generator)

## Installation

I document everything around the installation from what I know & learn. However, I can probably only document from a macOS view. I recommend to run the script from within a virtual environment to now interfere with local python installations from macOS. You can do so by:

    $ python -m venv venv
    $ source venv/bin/activate

Then you install all the necessary libraries (residing in _requirements.txt_):

    $ pip install -r requirements.txt

You will need an OpenAI API Key that you can get on their [API dashboard](https://platform.openai.com/). Remember, that you need a separate subscription for using the API. **Keep your API key secret.** In this library we will use a `.env` file to store your secret key.

    touch .env
    echo "OPENAI_API_KEY=your-key-here" >> .env

Then open the file and put your OpenAI API key there. We will need it later to ask OpenAI to optimize your news.

## Running the script

### Verbose output

You can activate verbose output of the script, especially the feedreader (for validating the run):

    urls = ["https://example.com/feed"]
    reader = FeedReader(urls, verbose=True)
    entries = reader.fetch_feeds()

It will give you an output like:

    2024-11-22 10:15:30 - src.feed_reader - INFO - Validating 1 URLs
    2024-11-22 10:15:30 - src.feed_reader - INFO - Valid URL added: https://example.com/feed
    2024-11-22 10:15:30 - src.feed_reader - INFO - Starting to fetch 1 feeds
    2024-11-22 10:15:31 - src.feed_reader - INFO - Fetching feed: https://example.com/feed
    2024-11-22 10:15:31 - src.feed_reader - INFO - Successfully fetched feed: Tech News (https://example.com/feed)
    2024-11-22 10:15:31 - src.feed_reader - INFO - Found 15 entries
    2024-11-22 10:15:31 - src.feed_reader - INFO - Completed fetching all feeds. Total entries: 15