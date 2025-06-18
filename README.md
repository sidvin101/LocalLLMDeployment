# LocalLLMDeployment

## model downloaded from https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF 
I used llama.cpp to deploy a server with this model. Once llama.cpp is installed, I run

```
./llama-server \
  --model /path/to/model.gguf \
  --port 5000 \
  --ctx-size 512 \
  --n-gpu-layers 20
```
To get a server running. 

Once done, run 
```
app.py
```
For the flask app that will make an API call for the server.

## Project Complexity
This repo showcases a simple web application that wraps a locally deployed LLM via a llama.cpp server through an API call. A Flask front end is used for interaction.

### Components
- app.py: The Flask server, that provides with basic web UI with POST and GET functionality
- api_wrapper.py: handles groups of chat payloads and caching

## Big O aspects
- Cache Hashing: O(n), where n is the length of the serialized input JSON file
- Cache Lookup: Since it is a dictionary, the average case is O(1)
- API Call: O(1) codewise, but is ultimately dependent on LLM server latency
