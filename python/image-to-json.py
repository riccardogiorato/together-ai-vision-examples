import json
import together
from pydantic import BaseModel, Field
from typing import Optional

# Initialize Together AI client
client = together.Together()

# Define the schema for receipt data matching the Next.js example
class Receipt(BaseModel):
    businessName: Optional[str] = Field(None, description="Name of the business on the receipt")
    date: Optional[str] = Field(None, description="Date when the receipt was created")
    total: Optional[float] = Field(None, description="Total amount on the receipt")
    tax: Optional[float] = Field(None, description="Tax amount on the receipt")

def extract_receipt_info(image_url: str) -> dict:
    """
    Extract receipt information from an image using Together AI's vision capabilities.
    
    Args:
        image_url: URL of the receipt image to process
        
    Returns:
        A dictionary containing the extracted receipt information
    """
    # Call the Together AI API with the image URL and schema
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting information from receipts. Extract the relevant information and format it as JSON."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract receipt information"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        response_format={
            "type": "json_object",
            "schema": Receipt.model_json_schema()
        }
    )
    
    # Parse and return the response
    if response and response.choices and response.choices[0].message.content:
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response as JSON"}
    
    return {"error": "Failed to extract receipt information"}

# Example usage
def main():
    receipt_url = "https://napkinsdev.s3.us-east-1.amazonaws.com/next-s3-uploads/1627e746-7eda-46d3-8d08-8c8eec0d6c9c/nobu.jpg?x-id=PutObject"
    result = extract_receipt_info(receipt_url)
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()