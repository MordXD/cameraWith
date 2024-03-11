from dotenv import load_dotenv
from openai import *

load_dotenv()
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'
CYAN = '\033[96m'


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    def generate_text(self, prompt):
        stream_completion = self.client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": "You're an helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        full_response = ""
        line_buffer = ""

        for chunk in stream_completion:
            delta_content = chunk.choices[0].delta.content

            if delta_content is not None:
                line_buffer += delta_content

                if '\n' in line_buffer:
                    lines = line_buffer.split('\n')
                    for line in lines[:-1]:
                        print(NEON_GREEN + line + RESET_COLOR)
                        full_response += line + '\n'
                    line_buffer = lines[-1]
        if line_buffer:
            print(NEON_GREEN + line_buffer + RESET_COLOR)
            full_response += line_buffer
        return full_response
