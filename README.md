# APEC_Chatbot

APEC_Chatbot is an AI-powered chatbot designed to assist users with various queries and automate conversations. It leverages modern natural language processing techniques to provide intelligent, context-aware responses.

---

## 🚀 Features

- Conversational AI for user interaction
- Customizable intents and responses
- Easy integration with messaging platforms
- Modular and extensible codebase

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/KhangNB26/APEC_Chatbot.git
cd APEC_Chatbot
```

### 2. Prepare Data

Run the following scripts to crawl and save datasets to Qdrant:

```bash
python backend/data_scripts.py
python backend/data_embedding.py
```

### 3. Configure Environment

- Edit the `.env` file:
  - Set `HF_CACHE_DIR` to your desired HuggingFace model cache path.
  - If using Mistral or other large models, add `HUGGINGFACE_TOKEN` with your HuggingFace token.
- The project uses **Qdrant Cloud** and **Docker**.

### 4. Build the Service

Start the chatbot web service:

```bash
docker-compose up
```

### 5. Access the Chatbot

Open your browser and go to:  
[http://localhost:8000/ui/index.html](http://localhost:8000/ui/index.html)

---

## ⚠️ Notes

- **Security:** QDRANT_API_KEY and QDRANT_HOST are required for Qdrant Cloud and Docker. Handle these credentials securely.
- **Model Limitations:** The default model is `TinyLlama/TinyLlama-1.1B-Chat-v1.0` due to hardware constraints. For better results, use a more powerful model like Mistral (see below).
- **Using Mistral Model:**  
  Add your HuggingFace token to `.env` as `HUGGINGFACE_TOKEN`, then update `text_2_text.py` as follows:
  ```python
  # Get HuggingFace token from environment variable
  hf_token = os.getenv("HUGGINGFACE_TOKEN")
  # Create pipeline for text generation using HuggingFace token
  tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)
  model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)
  text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)
  ```
- **Demo:**  
  See `Chatbot_Demo_Image.png` for a demonstration screenshot.