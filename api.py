import openai
from metaphor_python import Metaphor
from constants import OPENAPI_KEY, METAPHOR_KEY
from api_types import MetaphorSearchResult, MetaphorSearchResponse, OpenAiResponse
from parse import parse_search_response_contents

# Configure the API clients
openai.api_key = OPENAPI_KEY
metaphor_client = Metaphor(METAPHOR_KEY)


def perform_search_query(query: str) -> MetaphorSearchResponse:
    search_response = metaphor_client.search(query, use_autoprompt=True)

    return MetaphorSearchResponse(
        results=[
            MetaphorSearchResult(url=result.url, contents=contents)
            for result, contents in zip(
                search_response.results,
                [
                    parse_search_response_contents(c.extract)
                    for c in search_response.get_contents().contents
                ],
            )
        ]
    )


def perform_openai_request(prompt: str, knowledge: str) -> OpenAiResponse:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"You are a helpful assistant. Answer {prompt}."
                f" Use your own knowledge and the following: {knowledge}."
                " Override your own knowledge with the provided prompt if there is a clash",
            },
        ],
    )

    return completion.choices[0].message.content
