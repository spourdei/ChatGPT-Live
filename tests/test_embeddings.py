import pytest
from sentence_transformers import SentenceTransformer, util
from embeddings import get_sorted_sentence_embeddings
from api_types import SentenceEmbedding
import numpy as np
import torch

# Load the pre-trained model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


# Test case 1: Encoding single sentence
@pytest.mark.parametrize(
    "sentence", ["This is a test sentence.", "Another sentence for testing."]
)
def test_encode_single_sentence(sentence):
    encoded_sentence = model.encode(sentence)
    assert isinstance(encoded_sentence, np.ndarray)
    assert encoded_sentence.shape == (
        768,
    )  # Ensure the output has the expected dimension


# Test case 2: Encoding multiple sentences
@pytest.mark.parametrize(
    "sentences",
    [["Sentence 1", "Sentence 2", "Sentence 3"], ["Different 1", "Different 2"]],
)
def test_encode_multiple_sentences(sentences):
    encoded_sentences = model.encode(sentences)
    assert isinstance(encoded_sentences, np.ndarray)
    assert encoded_sentences.shape == (
        len(sentences),
        768,
    )  # Ensure the output has the expected dimension


# Test case 3: Similarity measurement between two sentences
def test_similarity_measurement():
    sentence1 = "This is a test sentence."
    sentence2 = "This is another test sentence."
    similarity_score = util.pytorch_cos_sim(
        model.encode(sentence1), model.encode(sentence2)
    )
    assert isinstance(similarity_score, torch.Tensor)
    assert 0.0 <= similarity_score <= 1.0


# Test case 4: Finding most similar sentence in a list
def test_most_similar_sentence():
    sentence1 = "This is a test sentence."
    sentences_to_compare = [
        "A similar sentence",
        "Another similar sentence",
        "A different sentence",
    ]
    most_similar_idx = (
        util.pytorch_cos_sim(
            model.encode(sentence1), model.encode(sentences_to_compare)
        )
        .argmax()
        .item()
    )
    most_similar_sentence = sentences_to_compare[most_similar_idx]
    assert most_similar_sentence in sentences_to_compare


# Test the get_sorted_sentence_embeddings function
def test_get_sorted_sentence_embeddings():
    # Define some sample input data
    user_query = ["Query"]
    sentences = [
        "SQL database query",
        "some unrelated nonsense but can have query in it",
        "Siavash",
    ]

    # Call the function
    sorted_embeddings = get_sorted_sentence_embeddings(user_query, sentences)

    # Check if the result is a list of SentenceEmbedding objects
    assert isinstance(sorted_embeddings, list)
    for embedding in sorted_embeddings:
        assert isinstance(embedding, SentenceEmbedding)

    # Check if the number of results is less than or equal to 1000
    assert len(sorted_embeddings) <= 1000

    # Check if the list is sorted in descending order of scores
    for i in range(1, len(sorted_embeddings)):
        assert sorted_embeddings[i].score <= sorted_embeddings[i - 1].score

    # Check if the content of the SentenceEmbedding objects matches the original sentences
    for i, embedding in enumerate(sorted_embeddings):
        assert embedding.content == sentences[i]


if __name__ == "__main__":
    pytest.main()
