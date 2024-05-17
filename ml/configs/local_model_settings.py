import torch


WEIGHT_TYPE = torch.float16

CONTEXT_MAX_LENGTH = 512
MAX_NEW_TOKENS = 1024

NUM_EMBEDDINGS = 32011
EMBEDDING_DIM = 3072

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'mps')
