from together import Together

client = Together()

prompt = "You are an expert at extracting information from receipts. Extract all the content from the receipt."

imageUrl = "https://napkinsdev.s3.us-east-1.amazonaws.com/next-s3-uploads/1627e746-7eda-46d3-8d08-8c8eec0d6c9c/nobu.jpg?x-id=PutObject"


stream = client.chat.completions.create(
    model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": imageUrl,
                    },
                },
            ],
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "" if chunk.choices else "", end="", flush=True)