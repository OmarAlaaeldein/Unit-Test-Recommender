import torch
from torch import nn, FloatTensor
from sentence_transformers import CrossEncoder, SentenceTransformer, util
from transformers import pipeline

# Set the device to use (GPU or CPU)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Model:
    def __init__(self):
        # Move the models to the specified device
        self.bi_encoder = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-dot-v1").to(device)
        #self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', num_labels=1).to(device)
        self.code_summarizer = pipeline("text2text-generation", model="Salesforce/codet5-base-multi-sum",device=0)

    def encode_paragraph(self, paragraph: str):
        return self.bi_encoder.encode(paragraph)

    def summarize_unittests(self, text: str):
        return self.code_summarizer(text)[0]['generated_text']

    #def score_text(self, text: str, text2: str):
    #    return self.cross_encoder.predict([(text,text2 )], activation_fct=nn.Sigmoid())[0]

    #def score_paragraphs(self, text: str, paragraphs: list):
    #    return self.cross_encoder.predict([(text, paragraph) for paragraph in paragraphs], activation_fct=nn.Sigmoid())

    def semantic_search(self, query_embedding: list, paragraph_embeddings: list, top_k: int = 10):
        # Move the tensors to the specified device
        query_embedding = FloatTensor(query_embedding).to(device)
        paragraph_embeddings = FloatTensor(paragraph_embeddings).to(device)
        hits = util.semantic_search(query_embedding, paragraph_embeddings, top_k=top_k)[0]
        return hits