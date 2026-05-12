import os
from evaluableai import MistralClient
from mistralai.models.chat_completion import ChatMessage

#The following settings will ontl send data to evlauable ai and will not run eval
client = MistralClient(
    api_key=os.environ["MISTRAL_API_KEY"],
    evaluableai_params={
        "token": os.getenv("EVALUABLEAI_API_KEY"),
        "eval": False,
        "sampling": 1,
        "eval_list": ["Sentiment"],
        "async": False,
        "tag_names": ["EXP 1", "Mistral AI"],
    }
)


fact_questions_with_answers = [
    ["What is the only mammal capable of true flight?", "Bats"],
    ["In what year did Neil Armstrong and Buzz Aldrin land on the moon?", "1969"],
    ["What is the hardest natural substance on Earth?", "Diamond"],
    ["Which planet is known as the Red Planet?", "Mars"],
    ["What is the largest ocean on Earth?", "Pacific Ocean"],
    ["How long does it take for light from the Sun to reach Earth?", "About 8 minutes"],
    ["What is the chemical symbol for table salt?", "NaCl"],
    ["Which animal has the highest blood pressure?", "Giraffe"],
    ["What temperature does water boil at under normal conditions?", "100 degrees Celsius"],
    ["Which is the largest planet in our solar system?", "Jupiter"]
]






import time  # Import the time module

def main():
    for i in range(len(fact_questions_with_answers)):
        message = fact_questions_with_answers[i][0]
        messages = [
            ChatMessage(role="user", content=message)
        ]
        chat_response = client.chat(
            model="mistral-small",
            messages=messages,
            ground_truth=fact_questions_with_answers[i][1]
        )


        print(f"Message: {message} -> Result: {chat_response}")
        # time.sleep(1)  # Wait for 1 second before the next loop iteration


if __name__ == "__main__":
    main()


# ################################################################
# #Demo 2 Running with eval
#
# import os
# from evaluableai import MistralClient
# from mistralai.models.chat_completion import ChatMessage
#
# client = MistralClient(
#     api_key=os.environ["MISTRAL_API_KEY"],
#     evaluableai_params={
#         "token": "YOUR EVALUABLEAI API KEY",
#         "eval": True,
#         "sampling": 1,
#         "eval_list": ["general_eval", "bleu", "word_error_rate", "rouge", "semantic_similarity"],
#         "async": False
#     }
# )
#
# messages = [
#     ChatMessage(role="user", content="what comes after tank in dictionary")
# ]
#
# # No streaming
# chat_response = client.chat(
#     model="mistral-tiny",
#     messages=messages,
# )
