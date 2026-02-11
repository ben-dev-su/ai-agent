import argparse
import os

from call_function import available_functions, call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse


def main() -> None:

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="ai-agent", description="Chatbot"
    )
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args: argparse.Namespace = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError()

    client: genai.Client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("api request failed")

    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []
    if response.function_calls is not None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise Exception("Error: Empty parts result")

            if function_call_result.parts[0].function_response is None:
                raise Exception("Error: function_response is None")

            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: function_response.response is None")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
