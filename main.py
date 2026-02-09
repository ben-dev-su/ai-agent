import os
from dotenv import load_dotenv
from google import genai
from google.genai.chats import GenerateContentResponse


def main():
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError()

    client: genai.Client = genai.Client(api_key=api_key)

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello World, Gemini",
    )

    print(response.text)


if __name__ == "__main__":
    main()
