import "dotenv/config";
import Together from "together-ai";

const together = new Together();

async function main() {
  const billUrl =
    "https://napkinsdev.s3.us-east-1.amazonaws.com/next-s3-uploads/1627e746-7eda-46d3-8d08-8c8eec0d6c9c/nobu.jpg?x-id=PutObject";

  const response = await together.chat.completions.create({
    model: "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages: [
      {
        role: "system",
        content:
          "You are an expert at extracting information from receipts. Extract all the content from the receipt.",
      },
      {
        role: "user",
        content: [
          { type: "text", text: "Extract receipt information" },
          { type: "image_url", image_url: { url: billUrl } },
        ],
      },
    ],
  });

  if (response?.choices?.[0]?.message?.content) {
    console.log("response:", response.choices[0].message.content);
    return response.choices[0].message.content;
  }

  throw new Error("Failed to extract receipt information");
}

main();
