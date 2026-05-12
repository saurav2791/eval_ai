#!/usr/bin/env -S poetry run python
from evaluableai import OpenAI


from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings


index_name="test"
your_query = "what is money by venkat"
embeddings=OpenAIEmbeddings(api_key='OPENAI_API_KEY')


docsearch = Pinecone(embedding=embeddings, index_name=index_name)

def retrieve_query(query,k):
    matching_results=docsearch.similarity_search(query,k=k)
    return matching_results

def retrieve_context(query):
    doc_search=retrieve_query(query,2)
    context = ""
    for i in range(len(doc_search)):
        context =  context + doc_search[i].page_content
        context = context + "\n\n\n"
    return context

context = retrieve_context(your_query)



client = OpenAI(
    evaluableai_params={
        "token": "evaluableai-4_6yMnxBE-5Gz8OF4JjcNQEZRtiRNw2z",  # Replace with your actual token
        "tag_names": ["rag_demo"],
    }
)


completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
                    "role": "system",
                    "content": context,
        },
        {
                    "role": "user",
                    "content": your_query,
        }
        ],
)

print(f"Result: {completion.choices[0].message.content}")
