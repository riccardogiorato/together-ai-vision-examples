import "dotenv/config";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";
import Together from "together-ai";

const together = new Together();

async function main() {
  const billUrl =
    "https://napkinsdev.s3.us-east-1.amazonaws.com/next-s3-uploads/1627e746-7eda-46d3-8d08-8c8eec0d6c9c/nobu.jpg?x-id=PutObject";
  // Define the receipt schema using Zod
  const receiptSchema = z.object({
    businessName: z
      .string()
      .optional()
      .describe("Name of the business on the receipt"),
    date: z.string().optional().describe("Date when the receipt was created"),
    total: z.number().optional().describe("Total amount on the receipt"),
    tax: z.number().optional().describe("Tax amount on the receipt"),
  });

  // Convert Zod schema to JSON schema for Together AI
  const jsonSchema = zodToJsonSchema(receiptSchema, { target: "openAi" });

  const response = await together.chat.completions.create({
    model: "meta-llama/Llama-4-Scout-17B-16E-Instruct",
    messages: [
      {
        role: "system",
        content:
          "You are an expert at extracting information from receipts. Extract the relevant information and format it as JSON.",
      },
      {
        role: "user",
        content: [
          { type: "text", text: "Extract receipt information" },
          { type: "image_url", image_url: { url: billUrl } },
        ],
      },
    ],
    response_format: { type: "json_object", schema: jsonSchema },
  });

  if (response?.choices?.[0]?.message?.content) {
    const output = JSON.parse(response.choices[0].message.content);
    console.dir(output);
    return output;
  }

  throw new Error("Failed to extract receipt information");
}

main();
