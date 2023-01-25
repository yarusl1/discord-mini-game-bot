from .db import get_score, set_score
import random

word_list = ["python", "javascript", "programming", "computer", "science"]

class Hangman():
  def __init__(self):
    self.word = random.choice(word_list)
  
  async def play_game(self, message, client):
      self.player_id = message.author.id
      wrong = 0
      stages = ["",
                "__________⠀⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀⠀|⠀⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀⠀|⠀⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀⠀0⠀⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀/|\⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀/⠀\⠀⠀⠀⠀",
                "|⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
              ]
      rletters = list(self.word)
      board = ["⠀"] * len(self.word)
      win = False
      await message.channel.send("Welcome to Hangman")
      while wrong < len(stages) - 1:
          print(1)
          await message.channel.send("".join(board))
          await message.channel.send("Guess a letter")
          message = await client.wait_for(
            "message", check=lambda m: m.author.id == self.player_id
          )

          char = message.content.lower()
          if len(char) > 1:
              await message.channel.send("It should be a letter")
              continue

          if char in rletters:
              cind = rletters.index(char)
              board[cind] = char
              rletters[cind] = '$'
          else:
              wrong += 1
          
          e = wrong + 1
          if "⠀" not in board:
              score = get_score(str(message.author))
              set_score(str(message.author), score + 1)
              await message.channel.send(f"You win!\nYour score is: {score + 1}")
              await message.channel.send("".join(board))
              win = True
              break
      if not win:
          score = get_score(str(message.author))
          set_score(str(message.author), score - 1)
          await message.channel.send("\n".join(stages[0: wrong]))
          await message.channel.send(f"You lose! It was {self.word}.\nYour score is: {score - 1}")
