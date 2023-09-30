import pydantic
import typing


class MetaphorSearchResult(pydantic.BaseModel):
    url: str
    contents: typing.Any


class MetaphorSearchResponse(pydantic.BaseModel):
    results: typing.List[MetaphorSearchResult]


class SentenceEmbedding(pydantic.BaseModel):
    content: str
    score: float
    order: int

    @property
    def token_count(self):
        # Calculate the approximate token count
        avg_chars_per_token = 4.5  # An aprx I got from chatgpt itself
        token_count = len(self.content) / avg_chars_per_token
        return int(token_count)  # Convert to an integer for a whole number of tokens


class OpenAiResponse(pydantic.BaseModel):
    content: str
