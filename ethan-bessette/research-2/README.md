# Machine Learning Research Project 2
AI Tools Review
Ethan Bessette

## The Process

### Setup
1. In the root directory:
```
curl -Lf https://github.com/Stability-AI/stable-audio-tools/archive/refs/heads/main.zip | tar -xz
```

2.
```
uv python pin 3.10
uv init
uv add pip hf
uv sync
source .venv/bin/activate
```

3.
```
cd stable-audio-tools-main
uv pip install .
```

The stable audio tools will install all the dependencies you need. If you accidentally enter `uv sync` again, you'll have to reinstall the dependencies. To avoid this, feel free to update `pyproject.toml` with all current packages.


4. Log in to Hugging Face to download the pre-trained weights. If you haven't already, make an account [here](huggingface.co). Then, navigate to the settings page, access tokens, and create a token. Then in the root directory:

