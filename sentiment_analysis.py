import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SentimentAnalysis:

    @staticmethod
    def analyse_reviews(texts):
        if not texts:
            return {
                'total_reviews': 0
            }

        # Join reviews (limit size to avoid token explosion)
        content = "\n".join(texts[:10])

        prompt = f"""
Analyze the sentiment of the following movie reviews.

Return ONLY JSON in this format:
{{
  "positive": number,
  "neutral": number,
  "negative": number
}}

Reviews:
{content}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )

            result_text = response.choices[0].message.content.strip()

            import json
            result = json.loads(result_text)

            total = result["positive"] + result["neutral"] + result["negative"]

            return {
                'total_reviews': total,
                'pos_score': round((result["positive"] / total) * 100, 1) if total else 0,
                'neutral_score': round((result["neutral"] / total) * 100, 1) if total else 0,
                'neg_score': round((result["negative"] / total) * 100, 1) if total else 0,
            }

        except Exception as e:
            print("OpenAI error:", e)
            return {
                'total_reviews': 0
            }