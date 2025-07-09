# APEC_Chatbot

APEC_Chatbot is an AI-powered chatbot designed to assist users with various queries and automate conversations. This project leverages modern natural language processing techniques to provide intelligent and context-aware responses.

## Features

- Conversational AI for user interaction
- Customizable intents and responses
- Easy integration with messaging platforms
- Modular and extensible codebase

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KhangNB26/APEC_Chatbot.git
    cd APEC_Chatbot
    ```

2. Data Scripts
    To prepare the necessary data, run the provided scripts:
    ```bash
    python backend/data_scripts.py
    python backend/data_embedding.py
    ```

    These scripts will crawl and save the datasets to Qdrant for retrieving.

3. Modify .env
    In .env file, there is a variable called HF_CACHE_DIR, this is where your HuggingFace model will be installed, so change it to your own path.

    In addition, I'm using Qdrant Cloud and Docker for chatbot.

4. Building service
    To build the chatbot web, run the following script:
    ```bash
    docker-compose up
    ```

5. Using chatbot 
    Your chatbot address will be: http://localhost:8000/ui/index.html
    Follow this link to experience the Chatbot.

Note:
    - Since I'm using Qdrant Cloud and Docker for service, I have to use the QDRANT_API_KEY and QDRANT_HOST so this can be a problem in security.
    - My laptop is not strong enough to use models like Mistral, or other powerful models. As a result, I'm using "TinyLlama/TinyLlama-1.1B-Chat-v1.0" which is not a great model, so the answer you see in Chatbot might be not that correct.
    - If you want to use model like Mistral, please add to .env a variable called HUGGINGFACE_TOKEN, then paste your token into it. After that, add these lines into text_2_text.py:
    ```
    # Get HuggingFace token from environment variable
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    # Create pipeline for text generation using HuggingFace token
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)
    text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
    ```

    - There is a Demo Image for Chatbot called Chatbot_Demo_Image.png.
