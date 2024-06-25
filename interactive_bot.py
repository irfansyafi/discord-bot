import discord
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the Discord client
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Load the pre-trained model and tokenizer from Hugging Face
model_name = "microsoft/DialoGPT-medium"  # You can choose small, medium, or large
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event handler for when a message is received
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Check if the message is addressed to the bot using a command prefix or mention
    if message.content.startswith('$chat'):
        user_message = message.content[len('$chat '):].strip()  # Remove the command prefix
        if not user_message:
            await message.channel.send("Please type something for me to respond to!")
            return
        
        # Tokenize and encode the input message
        inputs = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

        # Generate a response using the model
        response_ids = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)

        # Send the response to the channel
        await message.channel.send(response)

# Run the bot with your token
# Ensure you replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(BOT_TOKEN)
