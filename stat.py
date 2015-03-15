import datetime
from collections import Counter


class Constants:
    date_format = '%d-%b-%Y'
    time_format = '%H:%M:%S'

    competitors = ['T', 'O']

    MatchDetails = 'Match Details'
    Format = 'Format'
    StartTime = 'Start Time'
    Server = 'Server'
    PlayerEnds = 'Player Ends'
    Comment = 'Comment'
    Shot = 'Shot'
    Point = 'Point'
    Game = 'Game'
    Set = 'Set'
    Match = 'Match'

    Serve = 'Serve'
    Forehand = 'Forehand'
    Backhand = 'Backhand'
    Return = 'Return'

    Ace = 'Ace'
    Let = 'Let'
    ServeWinner = 'Serve Winner'

    Drive = 'Drive'
    Slice = 'Slice'
    Overhead = 'Overhead'
    Volleyed = 'Volleyed'
    Lob = 'Lob'
    DropShot = 'Drop Shot'
    Other = 'Other'

    In = 'In'
    InOffNet = 'In Off-Net'
    Winner = 'Winner'
    NetCord = 'Net Cord'
    PutAway = 'Put-Away'
    PassingShot = 'Passing Shot'
    ForcingError = 'Forcing Error'
    ForcingVolleyError = 'Forcing Volley Error'

    Out = 'Out'
    OutOffNet = 'Out Off-Net'
    OutPassingShot = 'Out Passing Shot'
    NettedPassingShot = 'Netted Passing Shot'
    Netted = 'Netted'

    first_serve = 'First Serve'
    second_serve = 'Second Serve'
    first_return = 'First Return'
    second_return = 'Second Return'
    not_in = [Out, OutOffNet, Netted, OutPassingShot, NettedPassingShot]
    errors = [Out, Netted, OutOffNet, OutPassingShot, NettedPassingShot]
    not_out = [Ace, ServeWinner, In, Let, Winner, NetCord, PassingShot, PutAway]
    point_won = [Ace, ServeWinner, In, Winner, NetCord, PassingShot, PutAway, ForcingError, ForcingVolleyError]

    fifteen = '15'
    thirty = '30'
    forty = '40'
    deuce = 'D'
    game = 'G'
    advantage = 'A'


class Comment:

   def __init__(self, player, comment):
      self.player = player
      self.comment = comment

   def __repr__(self):
      return repr((self.player, self.comment))


class Shot:

   def __init__(self, players, player, stroke, stroke_type, stroke_x, stroke_y, result, result_x, result_y, r_misc, s_time):
      self.player = players[Constants.competitors.index(player)]
      self.stroke = stroke
      self.stroke_type = stroke_type
      self.stroke_location = [stroke_x, stroke_y]
      self.stroke_result = [result_x, result_y]
      self.result = result
      self.r_misc = r_misc
      self.s_time = s_time

   def __repr__(self):
      return repr((self.player, self.stroke, self.stroke_type, self.result, self.stroke_location, self.stroke_result))


class Serve:

   def __init__(self, sequence, description, angle, result):
      self.sequence = sequence
      self.description = description
      self.angle = angle
      self.result = result

   def __repr__(self):
      return repr((self.sequence, self.description, self.angle, self.result))


class Point:

   def __init__(self, players, winner, T_score, O_score, p_time, rally_length, shots):
      self.players = players
      player_index = Constants.competitors.index(winner)
      self.winner = (None if player_index < 0 else players[player_index])
      self.score = {players[0]: T_score, players[1]: O_score}
      self.p_time = p_time
      self.rally_length = rally_length
      self.shots = shots
      self.stroke_types = [shot.stroke_type for shot in self.shots]
      self.shot_stats()

   def shot_stats(self):
      self.server = self.shots[0].player
      self.serves = [shot for shot in self.shots if shot.stroke == Constants.Serve]
      self.receiver = [player for player in self.players if player != self.server][0]
      self.key_shot = self.shots[-1]

   def __repr__(self):
      return repr((self.winner, self.score, self.rally_length, self.p_time, self.shots))


class Game:

   def __init__(self, players, winner, player_1_score, player_2_score, g_time, points):
      self.players = players
      self.server = points[0].server
      self.receiver = points[0].receiver
      player_index = (None if winner not in Constants.competitors else Constants.competitors.index(winner))
      self.winner = (None if player_index is None else players[player_index])
      self.score = {players[0]: player_1_score, players[1]: player_2_score}
      self.points = points
      self.g_time = g_time

   def __repr__(self):
      return repr((self.winner, self.score, self.points[-1].score))


class Set:

   def __init__(self, players, winner, player_1, player_2, games):
      player_index = (None if winner not in Constants.competitors else Constants.competitors.index(winner))
      self.winner = (None if player_index is None else players[player_index])
      self.games = games
      self.breaks = [game for game in games if game.server != game.winner]
      self.score = Counter([game.winner for game in self.games])

   def __repr__(self):
      return repr((self.score))


class Match:

   def __init__(self, players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                start_time, finish_time, first_server, player_ends, winner, sets):
      self.players = players
      self.match_date = match_date
      self.date_timestamp = datetime.datetime.strptime(match_date, Constants.date_format)
      self.start_timestamp = datetime.datetime.strptime(start_time, Constants.time_format)
      self.finish_timestamp = datetime.datetime.strptime(finish_time, Constants.time_format)
      self.duration = self.finish_timestamp - self.start_timestamp
      self.in_out = in_out
      self.number_of_sets = number_of_sets
      self.match_games = match_games
      self.format_description = format_description
      self.advantage = advantage
      self.lets = lets
      self.first_server = first_server
      self.player_ends = player_ends
      player_index = (None if winner not in Constants.competitors else Constants.competitors.index(winner))
      self.winner = (None if player_index is None else players[player_index])
      self.sets = sets
      self.games = [game for m_set in self.sets for game in m_set.games]
      self.breaks = [game for game in self.games if game.server != game.winner]
      self.set_score = Counter([m_set.winner for m_set in self.sets])

   def __repr__(self):
      return repr((self.players, self.match_date, self.set_score))


class PlayerStats:

    def __init__(self, name, match):
        self.sets = {}
        self.name = name
        self.match = match
        self.match_stats = Stats(name, match.games)
        for s, Set in enumerate(match.sets):
            self.sets[s] = Stats(name, match.sets[s].games)

    def __repr__(self):
        return repr((self.name))


class Stats:

    def __init__(self, name, games):
        self.name = name
        self.games = games
        self.games_won = [game for game in self.games if self.name == game.winner]
        self.service_games = [game for game in self.games if self.name == game.server]
        self.receiving_games = [game for game in self.games if game not in self.service_games]
        self.opponent = self.service_games[0].receiver

        self.all_points = [point for game in self.games for point in game.points]
        self.service_points = [point for game in self.service_games for point in game.points]
        self.receiving_points = [point for game in self.receiving_games for point in game.points]

        self.points_won = [point for game in self.games for point in game.points if self.name == point.winner]
        self.points_won_serving = [point for game in self.service_games for point in game.points if self.name == point.winner]
        self.points_won_receiving = [point for game in self.receiving_games for point in game.points if self.name == point.winner]

        self.avg_rally_length = round(sum([int(point.rally_length) for point in self.all_points]) / len(self.all_points))
        self.avg_rally_length_serving = round(sum([int(point.rally_length) for point in self.service_points]) / len(self.service_points))
        self.avg_rally_length_receiving = round(sum([int(point.rally_length) for point in self.receiving_points]) / len(self.receiving_points))
        self.avg_rally_length_points_won = round(sum([int(point.rally_length) for point in self.points_won]) / len(self.points_won))
        self.avg_rally_length_points_won_serving = round(sum([int(point.rally_length) for point in self.points_won_serving]) / len(self.points_won_serving))
        self.avg_rally_length_points_won_receiving = round(sum([int(point.rally_length) for point in self.points_won_receiving]) / len(self.points_won_receiving))

        self.breaks = [game for game in self.games if game.server != self.name and game.winner == self.name]
        self.breakpoints = [point for point in self.all_points if point.server == self.opponent
                            and (point.score[self.name] == Constants.advantage
                                 or (point.score[self.name] == Constants.forty and point.score[self.opponent] != Constants.forty))]
        self.breakpoints_pct = round(len(self.breaks) * 100 / len(self.breakpoints))

        self.first_serves = [shot for game in self.service_games for point in game.points for shot in point.shots if shot.stroke_type == Constants.first_serve]
        self.first_serves_in = [serve for serve in self.first_serves if serve.result in Constants.not_out and serve.result != Constants.Let]
        self.first_serve_lets = [serve for serve in self.first_serves if serve.result == Constants.Let]
        self.first_serves_out = [serve for serve in self.first_serves if serve.result not in Constants.not_out]
        self.first_serve_pct = (None if not len(self.first_serves) else
                                round(float(len(self.first_serves) - len(self.first_serves_out) - len(self.first_serve_lets)) * 100
                                      / (len(self.first_serves) - len(self.first_serve_lets))))

        self.second_serves = [shot for game in self.service_games for point in game.points for shot in point.shots if shot.stroke_type == Constants.second_serve]
        self.second_serves_in = [serve for serve in self.second_serves if serve.result in Constants.not_out and serve.result != Constants.Let]
        self.second_serve_lets = [serve for serve in self.second_serves if serve.result == Constants.Let]
        self.second_serves_out = [serve for serve in self.second_serves if serve.result not in Constants.not_out]
        self.second_serve_pct = (None if not len(self.second_serves) else
                                 round(float(len(self.second_serves) - len(self.second_serves_out) - len(self.second_serve_lets)) * 100
                                       / (len(self.second_serves) - len(self.second_serve_lets))))

        self.aces = [serve for serve in self.first_serves if serve.result == Constants.Ace]
        self.serve_winners = [serve for serve in self.first_serves if serve.result == Constants.ServeWinner]
        self.double_faults = [serve for serve in self.second_serves if serve.result in Constants.not_in]
        self.unforced_errors = [point for point in self.all_points
                                if self.name != point.winner
                                and point.shots[-1].stroke != Constants.Serve
                                and point.shots[-1].player == self.name]
        self.winners = [point for point in self.points_won if point.shots[-1].player == self.name and point.shots[-1].result == Constants.Winner]
        self.forcing_errors = [point for point in self.points_won if point.shots[-1].player == self.name and point.shots[-1].result == Constants.ForcingError]

        self.points_pct = round(len(self.points_won) * 100 / len(self.all_points))
        self.points_won_1st_serve = [point for point in self.points_won if point.server == self.name and Constants.second_serve not in point.stroke_types]
        self.points_pct_1st_serve = round(len(self.points_won_1st_serve) * 100 / len(self.first_serves_in))
        self.points_won_2nd_serve = [point for point in self.points_won if point.server == self.name and Constants.second_serve in point.stroke_types]
        self.points_pct_2nd_serve = round(len(self.points_won_2nd_serve) * 100 / len(self.second_serves))
        self.points_won_receiving = [point for point in self.points_won if point.receiver == self.name]
        self.points_pct_receiving = round(len(self.points_won_receiving) * 100 / len(self.receiving_points))

        self.aggressive_margin = len(self.aces + self.serve_winners + self.winners + self.forcing_errors) - len(self.double_faults + self.unforced_errors)
        self.aggressive_margin_pct = round(self.aggressive_margin * 100 / len(self.all_points))

        self.returns_1st_serve = [point for point in self.receiving_points if Constants.first_return in point.stroke_types]
        self.returns_1st_in_play = [shot for point in self.returns_1st_serve for shot in point.shots if shot.stroke_type == Constants.first_return and shot.result in Constants.not_out]
        self.returns_1st_pct = round(len(self.returns_1st_in_play) * 100 / len(self.returns_1st_serve))
        self.returns_2nd_serve = [point for point in self.receiving_points if Constants.second_return in point.stroke_types]
        self.returns_2nd_in_play = [shot for point in self.returns_2nd_serve for shot in point.shots if shot.stroke_type == Constants.second_return and shot.result in Constants.not_out]
        self.returns_2nd_pct = round(len(self.returns_2nd_in_play) * 100 / len(self.returns_2nd_serve))
        self.returns = self.returns_1st_serve + self.returns_2nd_serve
        self.returns_in_play = self.returns_1st_in_play + self.returns_2nd_in_play
        self.returns_in_play_pct = round(len(self.returns_in_play) * 100 / len(self.returns))

    def __repr__(self):
        return repr((self.first_serves_pct, self.second_serves_pct))


class PTN:

    def parse(filename):
       [winner] = ['']
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
          if data[0] == Constants.MatchDetails:
             players = data[1:3]
             match_date = data[3]
             in_out = data[6]
          elif data[0] == Constants.Format:
             number_of_sets = data[1]
             match_games = data[2]
             format_description = data[3]
             advantage = data[4]
             lets = data[5]
          elif data[0] == Constants.StartTime:
             start_time = data[1]
             finish_time = data[1]
          elif data[0] == Constants.Server:
             first_server = data[1]
          elif data[0] == Constants.PlayerEnds:
             player_ends = data[1]
          elif data[0] == Constants.Match:
             winner = data[1]
             finish_time = data[2]
          elif data[0] == Constants.Shot:
             if len(data) == 11:
                r_misc = data[9]
                s_time = data[10]
             shots.append(Shot(players, *data[1:9], r_misc=r_misc, s_time=s_time))
          elif data[0] == Constants.Point:
             points.append(Point(players, *data[1:6], shots=shots))
             shots = []
          elif data[0] == Constants.Comment:
             comments.append(Comment(data[1], data[2]))
          elif data[0] == Constants.Game:
             games.append(Game(players, *data[1:5], points=points))
             [shots, points, comments] = [[], [], []]
          elif data[0] == Constants.Set:
             sets.append(Set(players, *data[1:4], games=games))
             [shots, points, games, comments] = [[], [], [], []]

       if sets == [] and games != []:
           sets.append(Set(players, '', '', '', games=games))

       return Match(players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                    start_time, finish_time, first_server, player_ends, winner, sets)

    def player_stats(player_stats):
        print ("Name                     :", player_stats.name)
        print ("First Serve %            :", player_stats.match_stats.first_serve_pct)
        print ("Aces / Service Winners   :", len(player_stats.match_stats.aces), "/", len(player_stats.match_stats.serve_winners))
        print ("Double Faults            :", len(player_stats.match_stats.double_faults))
        print ("Unforced Errors          :", len(player_stats.match_stats.unforced_errors))
        print ("Winners / Forcing Errors :", len(player_stats.match_stats.winners), "/", len(player_stats.match_stats.forcing_errors))
        print ("Total Points Won         :", len(player_stats.match_stats.points_won), "(", player_stats.match_stats.points_pct, ")")
        print ("First Serve Points Won   :", len(player_stats.match_stats.points_won_1st_serve), "of", len(player_stats.match_stats.first_serves_in),
               "(", player_stats.match_stats.points_pct_1st_serve, ")")
        print ("Second Serve Points Won  :", len(player_stats.match_stats.points_won_2nd_serve), "of", len(player_stats.match_stats.second_serves),
               "(", player_stats.match_stats.points_pct_2nd_serve, ")")
        print ("Receiving Points Won     :", len(player_stats.match_stats.points_won_receiving), "of", len(player_stats.match_stats.receiving_points),
               "(", player_stats.match_stats.points_pct_receiving, ")")
        print ("Break Points Converted   :", len(player_stats.match_stats.breaks), "of", len(player_stats.match_stats.breakpoints),
               "(", player_stats.match_stats.breakpoints_pct, ")")
        print ("Returns in Play          :", player_stats.match_stats.returns_in_play_pct,
               "(", player_stats.match_stats.returns_1st_pct, "/", player_stats.match_stats.returns_2nd_pct, ")")
        print ("Aggressive Margin        :", player_stats.match_stats.aggressive_margin, "(", player_stats.match_stats.aggressive_margin_pct, ")")
