# LocalLLMDeployment

## model downloaded from https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF

## Deployment Procss
- Install llama.cpp
- Clone this repo
- Install requirements from requirements.txt
- Download the model from the url link (you may have to request access first)
- Once the model is downloaded, rename it to model.gguf, and keep track of the path to the model
- Run the below code to get the server running:
```
./llama-server \
  --model /path/to/model.gguf \
  --port 5000 \
  --ctx-size 512 \
  --n-gpu-layers 20
```
- In a separate terminal, run app.py. This will be your main method of making API calls

## Application Process
- The user asks a question to the chatbot
- The message will be cached
- If the message is already cached (i.e. if the user has already answered that question before), return the previous answer
- Otherwise, compile the message into an API Wrapper payload
- Using the payload, it will make an API call to the server and return the generated message. 

## Architecture
```
|- /templates
|  - index.html: The main flask UI
|- app.py: The main flask app
|- api_wrapper.py: handles the payload and caching logic
```

## Big O
- Cache Hashing: O(n), where n is the length of the serialized input JSON file
- Cache Lookup: Since it is a dictionary, the average case is O(1)
- API Call: O(1) codewise, but is ultimately dependent on LLM server latency
