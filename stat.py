import datetime
from collections import Counter


class Comment:

   def __init__(self, player, comment):
      self.player = player
      self.comment = comment

   def __repr__(self):
      return repr((self.player, self.comment))


class Shot:
   competitors = ['T', 'O']

   def __init__(self, players, player, stroke, stroke_type, stroke_x, stroke_y, result, result_x, result_y, r_misc, s_time):
      self.player = players[self.competitors.index(player)]
      self.stroke = stroke
      self.stroke_type = stroke_type
      self.stroke_x = stroke_x
      self.stroke_y = stroke_y
      self.result = result
      self.result_x = result_x
      self.result_y = result_y
      self.r_misc = r_misc
      self.s_time = s_time

   def __repr__(self):
      return repr((self.player, self.stroke, self.stroke_type, self.result))


class Serve:

   def __init__(self, sequence, description, angle, result):
      self.sequence = sequence
      self.description = description
      self.angle = angle
      self.result = result

   def __repr__(self):
      return repr((self.sequence, self.description, self.angle, self.result))


class Point:
   competitors = ['T', 'O']
   score = {}

   def __init__(self, players, winner, T_score, O_score, p_time, rally_length, shots):
      self.players = players
      self.winner = self.players[self.competitors.index(winner)]
      self.score[players[0]] = T_score
      self.score[players[1]] = O_score
      self.p_time = p_time
      self.rally_length = rally_length
      self.shots = shots
      self.shot_stats()

   def shot_stats(self):
      self.server = self.shots[0].player
      self.serves = [shot for shot in self.shots if shot.stroke == 'Serve']
      self.receiver = [player for player in self.players if player != self.server][0]
      self.key_shot = self.shots[-1]

   def __repr__(self):
      return repr((self.winner, self.score, self.rally_length, self.p_time, self.shots))


class Game:
   competitors = ['T', 'O']

   def __init__(self, players, winner, player_1_score, player_2_score, g_time, points):
      self.players = players
      self.server = points[0].server
      self.receiver = points[0].receiver
      self.winner = players[self.competitors.index(winner)]
      self.player_1_score = player_1_score
      self.player_2_score = player_2_score
      self.points = points
      self.g_time = g_time
      self.breakpoints = [point for point in points
                          if point.score[point.receiver] == 'A'
                          or (point.score[point.receiver] == '40' and point.score[point.server] != '40')]
      self.first_serves = [shot for point in self.points for shot in point.shots if shot.stroke_type == 'First Serve']
      self.first_serves_out = [serve for serve in self.first_serves if serve.result not in ['Ace', 'Serve Winner', 'In', 'Let']]
      self.first_serves_pct = (None if not len(self.first_serves) else
                               float(len(self.first_serves) - len(self.first_serves_out)) / len(self.first_serves))
      self.second_serves = [shot for point in self.points for shot in point.shots if shot.stroke_type == 'Second Serve']
      self.second_serves_out = [serve for serve in self.second_serves if serve.result not in ['Ace', 'Serve Winner', 'In', 'Let']]
      self.second_serves_pct = (None if not len(self.second_serves) else
                                float(len(self.second_serves) - len(self.second_serves_out)) / len(self.second_serves))

   def __repr__(self):
      return repr((self.winner, self.players[0], self.player_1_score, self.players[1], self.player_2_score))


class Set:
   competitors = ['T', 'O']

   def __init__(self, players, winner, player_1, player_2, games):
      self.winner = players[self.competitors.index(winner)]
      self.player_1 = player_1
      self.player_2 = player_2
      self.games = games
      self.breaks = [game for game in games if game.server != game.winner]
      self.breakpoints = [breakpoint for game in self.games for breakpoint in game.breakpoints]
      self.converted_breakpoints = Counter([game.winner for game in self.games if game.winner != game.server])
      self.score = Counter([game.winner for game in self.games])

   def __repr__(self):
      return repr((self.score))


class Match:
   competitors = ['T', 'O']

   def __init__(self, players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                start_time, finish_time, first_server, player_ends, winner, sets):
      self.players = players
      self.match_date = match_date
      self.date_timestamp = datetime.datetime.strptime(match_date, '%d-%b-%Y')
      self.start_timestamp = datetime.datetime.strptime(start_time, '%H:%M:%S')
      self.finish_timestamp = datetime.datetime.strptime(finish_time, '%H:%M:%S')
      self.duration = self.finish_timestamp - self.start_timestamp
      self.in_out = in_out
      self.number_of_sets = number_of_sets
      self.match_games = match_games
      self.format_description = format_description
      self.advantage = advantage
      self.lets = lets
      self.first_server = first_server
      self.player_ends = player_ends
      self.winner = players[self.competitors.index(winner)]
      self.sets = sets
      self.games = [game for m_set in self.sets for game in m_set.games]
      self.breaks = [game for game in self.games if game.server != game.winner]
      self.set_score = Counter([m_set.winner for m_set in self.sets])

   def __repr__(self):
      return repr((self.players, self.match_date, self.set_score))


class PlayerStats:

    def __init__(self, name, games):
        self.name = name
        self.games = games
        self.service_games = [game for game in self.games if self.name == game.server]
        self.games_won = [game for game in self.games if self.name == game.winner]
        self.all_points = [point for game in self.games for point in game.points]
        self.points_won = [point for game in self.games for point in game.points if self.name == point.winner]
        self.breaks = [game for game in self.games if game.server != self.name and game.winner == self.name]
        self.breakpoints = [point for point in self.all_points if point.score[name] == 'A' or (point.score[name] == '40' and True)]
        self.breakpoint_pct = (None if not len(self.breakpoints) else float(len(self.breaks)) * 100 / len(self.breakpoints))

        # self.first_serves = [shot for point in game.points for game in self.service_games for shot in point.shots if shot.stroke_type == 'First Serve']
        # self.first_serves_out = [serve for serve in self.first_serves if serve.result not in ['Ace', 'Serve Winner', 'In']]
        # self.first_serves_pct = (None if not len(self.first_serves) else
        #                          float(len(self.first_serves) - len(self.first_serves_out)) / len(self.first_serves))

    def __repr__(self):
        return repr((self.name))


def pf(filename):
   try:
      with open(filename, 'r', encoding='utf16') as csvfile:
         lines = csvfile.readlines()
   except:
      with open(filename, 'r') as csvfile:
         lines = csvfile.readlines()

   [shots, points, games, sets, comments] = [[], [], [], [], []]
   for l, line in enumerate(lines):
      line = line.replace('"', '')
      [r_misc, s_time] = ['', '']
      data = line.strip().split(',')
      if data[0] == 'Match Details':
         players = data[1:3]
         match_date = data[3]
         in_out = data[6]
      elif data[0] == 'Format':
         number_of_sets = data[1]
         match_games = data[2]
         format_description = data[3]
         advantage = data[4]
         lets = data[5]
      elif data[0] == 'Start Time':
         start_time = data[1]
      elif data[0] == 'Server':
         first_server = data[1]
      elif data[0] == 'Player Ends':
         player_ends = data[1]
      elif data[0] == 'Match':
         winner = data[1]
         finish_time = data[2]
      elif data[0] == 'Shot':
         if len(data) == 11:
            r_misc = data[9]
            s_time = data[10]
         shots.append(Shot(players, *data[1:9], r_misc=r_misc, s_time=s_time))
      elif data[0] == 'Point':
         points.append(Point(players, *data[1:6], shots=shots))
         shots = []
      elif data[0] == 'Comment':
         comments.append(Comment(data[1], data[2]))
      elif data[0] == 'Game':
         games.append(Game(players, *data[1:5], points=points))
         [shots, points, comments] = [[], [], []]
      elif data[0] == 'Set':
         sets.append(Set(players, *data[1:4], games=games))
         [shots, points, games, comments] = [[], [], [], []]

   return Match(players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                start_time, finish_time, first_server, player_ends, winner, sets)


def refresh():
   print ('exec(open("stat.py").read())')
