import boto3
import json

# Initialize Bedrock client
brt = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

# Ask user for the essay topic
topic = input("What topic would you like me to write an essay about? ")

# Optional: let user choose length (short, medium, long)
length = input("How long? (short / medium / long) [default: medium]: ").strip().lower()
if length == "short":
    max_tokens = 400
    words = "about 200-250 words"
elif length == "long":
    max_tokens = 1000
    words = "about 500-600 words"
else:
    max_tokens = 600
    words = "about 350-400 words"

print(f"\nGenerating a {length or 'medium'} essay on: {topic}")
print("-" * 60)

# Build the Messages API request
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": max_tokens,
    "temperature": 0.7,
    "top_p": 0.9,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You are an excellent 8th-grade science teacher. "
                            f"Write a clear, engaging essay (around {words}) explaining the topic: {topic}. "
                            f"Use simple language, fun analogies, and keep it exciting for 13-14 year olds. "
                            f"Structure it with an introduction, 3-4 main paragraphs, and a conclusion."
                }
            ]
        }
    ]
})

model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

try:
    response = brt.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response['body'].read())
    essay = response_body['content'][0]['text']

    print("\nHere's your essay:\n")
    print(essay)

except Exception as e:
    print("Error:", str(e))


    # Example usage:python .\essay_writer.py
    # What topic would you like me to write an essay about? The water cycle
    # How long? (short / medium / long) [default: medium]: short
    