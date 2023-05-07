import pandas as pd
import json
from cohere_classifier.cohere_classifier import *
from openai_classifier.openai_classifier import *

if __name__ == "__main__":
    with open("../api-keys.json", "r") as f:
        api_keys = json.load(f)
        print(f"Found keys for {', '.join(api_keys.keys())}")


    #-----------------------------------Cohere Classifier------------------------------------------

    # CH_Classifier = CohereClassifier(api_keys)
    # input = ["""the economic gets better, people buy the stocks"""]
    # rate = CH_Classifier.get_ratings(input)
    # print(rate)

    #-----------------------------Openai davinci Classifier----------------------------------------
    # text_reviews = [
    #     "The product was amazing! Absolutely loved it.",
    #     "It's just okay, not great, but not terrible either.",
    #     "The worst experience I've ever had with a product. Terrible!"
    # ]
    # Openai_classifier = OpenaiClassifier(api_keys)

    # ratings = [Openai_classifier.get_ratings_from_davinci(review) for review in text_reviews]
    # print(ratings)

    #-----------------------------Openai gpt 3.5 turbo Classifier----------------------------------
    benzinga = pd.read_csv("../data/Benzinga.csv")
    benzinga_title = benzinga["body"][:1]

    Openai_classifier = OpenaiClassifier(api_keys)

    reponse = [Openai_classifier.get_ratings_from_gpt35(news) for news in benzinga_title]
    print(reponse)
