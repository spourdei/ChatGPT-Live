import typing
import torch
from api_types import SentenceEmbedding
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def get_embeddings(sentence: [str]):
    return model.encode(sentence, convert_to_tensor=True)


def get_sorted_sentence_embeddings(
    user_query: [str], sentences: [str]
) -> typing.List[SentenceEmbedding]:
    sentence_embeddings = [get_embeddings(sentence) for sentence in sentences]
    query_embedding = get_embeddings(user_query)

    #  use cosine-similarity and torch to find the highest scores
    cos_scores = [
        util.cos_sim(query_embedding, embedding).item()
        for embedding in sentence_embeddings
    ]

    # return the sorted list of sentences according to their score
    return sorted(
        [
            SentenceEmbedding(content=sentence, score=score, order=index)
            for sentence, score, index in zip(
                sentences, cos_scores, range(len(sentences))
            )
        ],
        key=lambda x: x.score,
        reverse=True,
    )
