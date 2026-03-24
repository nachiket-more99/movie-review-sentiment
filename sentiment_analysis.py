from google.cloud import language_v1

class SentimentAnalysis:
    # analyze sentiment model
    def analyze_sentiment(content):
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(
            content=content, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})

        return response

    # analyzing reviews
    def analyse_reviews(texts):
        if not texts:
            return {
                'total_reviews': 0
            }

        # Initialize variables
        total_texts = 0
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # writting reviews to text file
        with open('reviews.txt', 'w', encoding='utf-8') as file:
            for item in texts:
                file.write(item + '\n')

        # reading contents from this saved file to pass it to the analyzer 
        with open('reviews.txt', 'r', encoding='utf-8') as file: 
            contents = file.read()

        sentiment = SentimentAnalysis.analyze_sentiment(contents)

        for index, sentence in enumerate(sentiment.sentences):
            sentence_sentiment = sentence.sentiment.score
            total_texts += 1

            # Classify sentiment as positive, negative, or neutral
            if sentence_sentiment > 0:
                positive_count += 1
            elif sentence_sentiment < 0:
                negative_count += 1
            else:
                neutral_count += 1

        
        # Calculate percentage of positive, negative, and neutral sentiment
        positive_percentage = (positive_count / total_texts) * 100
        negative_percentage = (negative_count / total_texts) * 100
        neutral_percentage = (neutral_count / total_texts) * 100
        
        return {
            'total_reviews': total_texts,
            'pos_score': round(positive_percentage, 1),
            'neg_score': round(negative_percentage, 1),
            'neutral_score': round(neutral_percentage, 1), 
        }
