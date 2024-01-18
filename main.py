from discord import Client, Intents
from google.generativeai import configure, GenerativeModel
from os import environ
from dotenv import load_dotenv
from keep_alive import keep_alive

keep_alive()
load_dotenv()

class GEMINIModelConfig:
    model_name = "models/gemini-pro"
    generation_config = {"temperature": 1,
                         "top_p": 1,
                         "top_k": 1,
                         "max_output_tokens": 2048}

    safety_settings = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                       {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                       {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                       {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}]

async def text_to_text(prompt):
    configure(api_key = environ.get("PaLM_API_Key"))
    model = GenerativeModel(model_name = GEMINIModelConfig.model_name,
                            generation_config = GEMINIModelConfig.generation_config, #type: ignore
                            safety_settings = GEMINIModelConfig.safety_settings)

    prompt_parts = [prompt]
    answer = model.generate_content(contents = prompt_parts)
    return answer.text

class MyClient(Client):
    async def on_ready(self):
        print(f"Logged In as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("<@1153053230377488456>"):
            user_message = message.content.replace("<@1153053230377488456>", "").strip()
            bot_response = await text_to_text(prompt = user_message)

            # Handle potentially long responses with pagination
            chunks = [bot_response[i:i + 1900] for i in range(0, len(bot_response), 1900)]
            page = 1
            await message.channel.send(f"{message.author.mention}")
            for chunk in chunks:
                await message.channel.send(f"|| {message.author.mention} || (Page {page}): {chunk}")
                page += 1

intents = Intents.default()
intents.message_content = True
client = MyClient(intents = intents)

if __name__ == "__main__":
    client.run(token = str(environ.get("BardAI01_TOKEN")))
