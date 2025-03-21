## Installation

1) Configure your .env by copying example.env to .env and setting the variables how you like
2) Install `uv` on your system (if you already have python then just pip install it globally, like this `pip install uv`)
3) Inside the folder type `uv venv`, then activate your venv

   > Windows: .venv\scripts\activate
   >

   > Linux: source .venv/bin/activate
   >
4) Inside of the folder type `uv run pip install -e .`

## Running Membot

With your venv activated run `python main.py` and follow the instructions.

## Commands

`/save` saves the chat history, you can optionally give the file a name

`/quit` quits, it will ask you if you want to save

`/load` will show you available chat history files and load them into your session

`/clear` will clear the chat history in the session. If you loaded the chat history from file, the file remains.

## Prompts

Membot only has one prompt and its in `.env` and its `LLM_ROLE`, feel free to customize this how you like.
