score_board = {}

def get_top_10_players_string():
  global score_board
  sorted_dict = dict(sorted(score_board.items(), key=lambda item: item[1]))
  res = ""
  for key in list(sorted_dict.keys())[:10]:
    res += f"Person: {key}, score: {sorted_dict[key]}\n"
  return res

def get_score(_id):
  global score_board
  return score_board.get(_id, 0)

def set_score(_id, new_score):
  global score_board
  score_board[_id] = new_score
