from src.titaktoe import TicTacToe
from src.hangman import Hangman
from src.db import get_score, get_top_10_players_string
import discord

if __name__ == "__main__":
  intents = discord.Intents.all()
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print("Bot is ready.")


  @client.event
  async def on_message(message):
    
    if message.content == "!say hi":
      await message.channel.send("Hello there!")
    elif message.content == "!help":
      return_message = """!help - show this message
!say hi - greetings from me
!my score - shows you your total score
!best - list of the best players
!ttt - play tiktaktoe
!hm - play hangman
!bj - play blackjack"""
      await message.channel.send(return_message)
    elif message.content == "!my score":
      score = get_score(str(message.author))
      await message.channel.send(f"Your score is: {score}")
    elif message.content == "!best":
      await message.channel.send(get_top_10_players_string())
    elif message.content.startswith("!ttt"):
      game = TicTacToe()
      await game.play_game(message, client)
    elif message.content.startswith("!hm"):
      game = Hangman()
      await game.play_game(message, client)
  
  client.run("MTA2NzgyNTgxOTk0NDIyNjg1Ng.GixJxR.317RCnJpq7tEz1wDisTerMJNpQ-KSSKM6OyuC0")