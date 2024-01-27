from transformers import AutoModel, AutoTokenizer
import torch
import time


class MyLLM:
    def __init__(self, checkpoint: str):
        self.checkpoint: str = checkpoint
        self.torch_device: str = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = AutoModel.from_pretrained(checkpoint).to(self.torch_device)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def generate(self, text):
        model_inputs = self.tokenizer(text, return_tensors='pt').to(self.torch_device)
        

def get_model(checkpoint: str) -> MyLLM:
    start = time.time()
    print(f'Starting to load model {checkpoint}')
    model = MyLLM(checkpoint)
    finish = time.time()
    print(f'Finished loading model {checkpoint}, it took {finish - start} seconds')
    return model


llama_quantized_model = get_model("TheBloke/llama-7b.ggmlv3.q2_K.bin")

