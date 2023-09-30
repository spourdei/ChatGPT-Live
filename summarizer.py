import typing
from api_types import SentenceEmbedding


def summarize(embeddings: typing.List[SentenceEmbedding], max_tokens=2500) -> str:
    used_tokens: int = 0
    embeddings_index: int = 0
    included_embeddings: typing.List[SentenceEmbedding] = []

    while used_tokens < max_tokens and embeddings_index < len(embeddings):
        embedding = embeddings[embeddings_index]

        # We don't want to go over the token limit so have to terminate early if current embedding is too long
        if used_tokens + embedding.token_count > max_tokens:
            break

        # Add the current embedding to the included embeddings
        included_embeddings.append(embedding)

        # Increment the used tokens and index
        used_tokens += embedding.token_count
        embeddings_index += 1

    # Sort the included embeddings based on their original order and return their content
    return "\n".join(
        [
            e.content
            for e in sorted(
                included_embeddings,
                key=lambda x: x.order,
            )
        ]
    )
