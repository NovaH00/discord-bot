import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from flaskapp import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


# Message
async def send_message(message: Message, user_msg: str) -> None:
    if not user_msg:
        print("No msg were provided")
        return

    is_private = user_msg[0] == "?"
    if is_private:
        user_msg = user_msg[1:]

    try:
        response = get_response(user_input=user_msg)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


# Handling startup
@client.event
async def on_ready() -> None:
    print(f"{client.user} is running")


# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    # Check if the message starts with '/nsr_bot'
    if not message.content.startswith('/nsr_bot'):
        return  # If it doesn't, do nothing and exit the function

    # Extract the actual message after '/nsr_bot'
    user_message = message.content[len('/nsr_bot'):].strip()

    username = str(message.author)
    channel = str(message.channel)
    print(f"Channel: {channel}, Author: {username}, MSG: {user_message}")

    await send_message(message, user_message)


# Entry point
def main() -> None:
    keep_alive()
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
