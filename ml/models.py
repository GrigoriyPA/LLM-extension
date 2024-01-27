from transformers import AutoModel, AutoTokenizer
import torch
import time


class MyLLM:
    def __init__(self, checkpoint: str):
        self.checkpoint: str = checkpoint
        self.torch_device: str = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

        start = time.time()
        print(f'Starting to load model {checkpoint}')
        self.model = AutoModel.from_pretrained(checkpoint).to(self.torch_device)
        finish = time.time()
        print(f'Finished loading model {checkpoint}, it took {finish - start} seconds')

    def generate(self, text):
        model_inputs = self.tokenizer(text, return_tensors='pt').to(self.torch_device)


codellama_instruct_model = MyLLM("codellama/CodeLlama-7b-Instruct-hf")

