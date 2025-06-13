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


