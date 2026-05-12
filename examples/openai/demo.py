#!/usr/bin/env -S poetry run python
import random
import os
from evaluableai import OpenAI

import time


# Setup
client = OpenAI(
    evaluableai_params={
        "token": os.getenv("EVALUABLEAI_API_KEY"),
        "eval": False,
        "sampling": 1,
        "eval_list": ["Sentiment"],
        "async": False,
        "tag_names": ["EXP 1", "Open AI"],
    }
)

# Data Generation
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



def main():
    for i in range(len(fact_questions_with_answers)):
        message = fact_questions_with_answers[i][0]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            ground_truth=fact_questions_with_answers[i][1]
        )
        print(f"Message: {message} -> Result: {completion.choices[0].message.content}")
        # time.sleep(1)  # Wait for 1 second before the next loop iteration


if __name__ == "__main__":
    main()
