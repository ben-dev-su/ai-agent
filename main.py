import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse


def main() -> None:

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="ai-agent", description="Chatbot"
    )
    parser.add_argument("prompt", type=str, help="User prompt.")
    args: argparse.Namespace = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError()

    client: genai.Client = genai.Client(api_key=api_key)

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.prompt,
    )

    if response.usage_metadata is None:
        raise RuntimeError("api request failed")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
