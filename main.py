from api import perform_search_query, perform_openai_request
from summarizer import summarize
from embeddings import get_sorted_sentence_embeddings

while True:
    user_query: str = input("\n\nPlease input your query: ")

    # exit mechanism
    if user_query == "exit":
        break

    # perform a search for user query
    search_results = perform_search_query(query=user_query)

    # generate sorted sentence embeddings
    sorted_embeddings = get_sorted_sentence_embeddings(
        user_query=user_query,
        sentences=[rc for r in search_results.results for rc in r.contents],
    )

    # summarize the search results to fit the chatgpt prompt limit
    summarized_content = summarize(sorted_embeddings)

    # call openai with the summary
    response = perform_openai_request(prompt=user_query, knowledge=summarized_content)

    # print the result to the user
    print("\n")
    print(response)
    print("\n")
