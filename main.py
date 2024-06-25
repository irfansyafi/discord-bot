import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the Discord client
intents = discord.Intents.default()
intents.messages = True  # Enable message intents
client = discord.Client(intents=intents)


# Define a function to get an inspirational quote
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = response.json()
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

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
    
    # Check if the message starts with $inspire
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

# Run the bot with your token
# Ensure you replace 'YOUR_BOT_TOKEN' with your actual bot token
client.run(BOT_TOKEN)
