import openai
import numpy as np

class OpenaiClassifier():
    def __init__(self, api_keys):
        openai.api_key = api_keys['Openai']

    # rate: $0.0200 / 1K tokens
    def get_ratings_from_davinci(self, review):
        prompt = f"Rate the following review as an integer from 1 to 5, where 1 is the worst and 5 is the best: \"{review}\""
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            n=1,
            max_tokens=5,
            temperature=0.5,
            top_p=1
        )

        try:
            rating = int(response.choices[0].text.strip())
            return rating
        except ValueError:
            return None
    
    # rate: $0.002 / 1K tokens
    def get_ratings_from_gpt35(self, review):
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature = 0.2,
        messages=[
            # {"role": "system", "content": "You are a professional financial analyst."},
            {"role": "user", 
             "content": f"Rate the following review as an integer from 1 to 5, where 1 is the worst and 5 is the best: \"{review}\""}
        ]
        )

        print(completion.choices[0].message)




