import torch


WEIGHT_TYPE = torch.float16

CONTEXT_MAX_LENGTH = 512

DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'mps')

MAX_NEW_TOKENS = 200
