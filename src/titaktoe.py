import random
from .db import get_score, set_score

class TicTacToe:
  def __init__(self):
    self.board = [["⠀" for _ in range(3)] for _ in range(3)]
    self.player_letter = "X"
    self.computer_letter = "O"
    self.player_id = None

  def print_board(self):
    board_string = ""
    for row in self.board:
      board_string += "|".join(row) + "\n"
    return board_string

  def is_winner(self, letter):
    for row in self.board:
      if row == [letter, letter, letter]:
        return True

    for col in range(3):
      if (
        self.board[0][col] == letter
        and self.board[1][col] == letter
        and self.board[2][col] == letter
      ):
        return True
    
    if (
      self.board[0][0] == letter
      and self.board[1][1] == letter
      and self.board[2][2] == letter
    ):
      return True
    if (
      self.board[0][2] == letter
      and self.board[1][1] == letter
      and self.board[2][0] == letter
    ):
      return True

    return False

  def is_full(self):
    for row in self.board:
      for col in row:
        if col == "⠀":
          return False
    return True

  async def play_game(self, message, client):
    self.player_id = message.author.id
    await message.channel.send(self.print_board())
    while not self.is_full():
      await message.channel.send(
        "Enter the row and column of your move (e.g. `1 2` for top-right corner):"
      )
      move = await client.wait_for(
        "message", check=lambda m: m.author.id == self.player_id
      )
      splited = move.content.strip().split()
      if len(splited) != 2:
        await message.channel.send(
          "Invalid input"
        )
        continue

      row, col = splited[0], splited[1]
      if not (row.isdigit() and col.isdigit()):
        await message.channel.send(
          "Enter the row and column in the folowing format `2 2`. Eg. row and column separeted by a space"
        )
        continue

      row, col = int(row), int(col)
      
      if (row >= 3 or row < 0) or (col >= 3 or col < 0):
        await message.channel.send(
          "Both the row and the column can't be smaller than 0 or greater than 3"
        )
        continue
        
      if self.board[row][col] != "⠀":
        await message.channel.send(
          "This slot is alredy taken try another one!"
        )
        continue
      
      self.board[row][col] = self.player_letter
      if self.is_winner(self.player_letter):
        score = get_score(str(message.author))
        set_score(str(message.author), score + 1)
        await message.channel.send(f"Your score: {score + 1}")
        await message.channel.send("Player wins!")
        await message.channel.send(self.print_board())
        return
      if self.is_full():
        await message.channel.send("It's a tie!")
        score = get_score(str(message.author))
        await message.channel.send(f"Your score: {score}")
        return

      empty_spaces = []
      for i in range(3):
        for j in range(3):
          if self.board[i][j] == "⠀":
            empty_spaces.append((i, j))

      computer_choice = random.choice(empty_spaces)
      self.board[computer_choice[0]][computer_choice[1]] = self.computer_letter
      await message.channel.send(self.print_board())
      if self.is_winner(self.computer_letter):
        score = get_score(str(message.author))
        set_score(str(message.author), score - 1)
        await message.channel.send("Computer wins!")
        await message.channel.send(f"Your score: {score - 1}")
        return
