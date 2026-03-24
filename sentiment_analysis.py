import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SentimentAnalysis:

    @staticmethod
    def analyse_reviews(texts):
        if not texts:
            return {'total_reviews': 0}

        content = "\n".join(texts[:5])

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict JSON generator. Only output valid JSON."
                    },
                    {
                        "role": "user",
                        "content": f"""
Classify these movie reviews into sentiment.

Return ONLY JSON like:
{{"positive": number, "neutral": number, "negative": number}}

Reviews:
{content}
"""
                    }
                ],
                temperature=0,
            )

            result_text = response.choices[0].message.content.strip()

            start = result_text.find("{")
            end = result_text.rfind("}") + 1

            if start == -1 or end == -1:
                raise ValueError("No JSON found")

            clean_json = result_text[start:end]

            result = json.loads(clean_json)

            total = result["positive"] + result["neutral"] + result["negative"]

            return {
                'total_reviews': total,
                'pos_score': round((result["positive"] / total) * 100, 1) if total else 0,
                'neutral_score': round((result["neutral"] / total) * 100, 1) if total else 0,
                'neg_score': round((result["negative"] / total) * 100, 1) if total else 0,
            }

        except Exception as e:
            print("OpenAI error:", e)

            # fallback (so UI doesn't break)
            return {
                'total_reviews': 0,
                'pos_score': 0,
                'neutral_score': 0,
                'neg_score': 0,
            }