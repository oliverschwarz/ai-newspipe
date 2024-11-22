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