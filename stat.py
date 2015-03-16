import datetime
import math
from collections import Counter


class Constants:
    date_format = '%d-%b-%Y'
    time_format = '%H:%M:%S'

    singles_competitors = ['T', 'O']
    doubles_competitors = ['T1', 'T2', 'O1', 'O2']

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
    winner = [Winner, PassingShot, PutAway]
    forcing_error = [ForcingError, ForcingVolleyError]

    Approach = ['Left Service Box', 'Right Service Box']

    fifteen = '15'
    thirty = '30'
    forty = '40'
    deuce = 'D'
    game = 'G'
    advantage = 'A'

    net_y = 160
    doubles_wide_x = [17, 231]
    singles_wide_x = [37, 203]
    svc_left_x = [37, 124]
    svc_right_x = [119, 203]
    out_long_y = [17, 301]
    baseline_y = [37, 281]
    no_mans_y = [67, 251]
    service_line_y = [91, 229]
    box_divider_x = [124, 119]


class Comment:

   def __init__(self, player, comment):
      self.player = player
      self.comment = comment

   def __repr__(self):
      return repr((self.player, self.comment))


class Coordinate:

   def __init__(self, x, y, kind):
      [self.kind, self.net, self.court_far, self.court_near, self.in_doubles, self.in_singles] = [None, None, None, None, None, None]
      [self.right_service_box, self.left_service_box, self.volley_zone, self.service_line] = [None, None, None, None]
      [self.no_mans_land, self.baseline, self.court, self.location, self.x, self.y] = [None, None, None, None, None, None]

      if not (x or y):
          return

      self.x = float(x)
      self.y = float(y)
      self.kind = kind

      self.net = (self.y == Constants.net_y)
      self.court_far = (self.y < Constants.net_y)
      self.court_near = (self.y > Constants.net_y)
      self.in_doubles = (self.between(Constants.doubles_wide_x, self.x) and self.between(Constants.out_long_y, self.y) and not (self.y == Constants.net_y))
      self.in_singles = (self.between(Constants.singles_wide_x, self.x) and self.between(Constants.out_long_y, self.y) and not (self.y == Constants.net_y))
      self.right_service_box = (self.between(Constants.service_line_y, self.y) and
                                ((self.between(Constants.svc_left_x, self.x) and self.court_far)
                                or (self.between(Constants.svc_right_x, self.x) and self.court_near)))
      self.left_service_box = (self.between(Constants.service_line_y, self.y) and
                               ((self.between(Constants.svc_right_x, self.x) and self.court_far)
                               or (self.between(Constants.svc_left_x, self.x) and self.court_near)))
      self.volley_zone = (self.left_service_box or self.right_service_box)
      self.service_line = (self.between(Constants.no_mans_y, self.y) and not self.volley_zone)
      self.no_mans_land = (self.between(Constants.baseline_y, self.y) and not (self.volley_zone or self.service_line))
      self.baseline = (self.between(Constants.out_long_y, self.y) and not (self.volley_zone or self.service_line or self.no_mans_land))

      self.court = ('Far' if self.court_far else ('Near' if self.court_near else 'Net'))
      self.location = ('Doubles Alley' if (self.in_doubles and not self.in_singles) else
                       ('Left Service Box' if self.left_service_box else
                        ('Right Service Box' if self.right_service_box else
                         ('Service Line' if self.service_line else
                          ("No Man's" if self.no_mans_land else
                           ('Baseline' if self.baseline else
                            ('Net' if self.net else 'Out')))))))

   def between(self, coordinate_pair, z):
       return (True if z > coordinate_pair[0] and z < coordinate_pair[1] else False)

   def __repr__(self):
      return repr((self.court, self.location))


class Path:

   def __init__(self, impact, mark):
       [self.trajectory] = [None]

       self.impact = impact
       self.mark = mark
       if not (self.impact.x or self.impact.y or mark.x or mark.y):
           return

       if ((self.impact.x <= 122 and self.mark.x > 122)
          or (self.impact.x > 122 and self.mark.x <= 122)):
           if self.mark.y > 90 and self.mark.y < 230:
               self.trajectory = 'Short Angle'
           else:
               self.trajectory = 'Crosscourt'
       elif self.mark.x > 80 and self.mark.x < 160:
           self.trajectory = 'Middle'
       else:
           self.trajectory = 'Line'

   def __repr__(self):
      return repr((self.impact, self.mark, self.trajectory))


class Shot:

   def __init__(self, players, player, stroke, stroke_type, stroke_x, stroke_y, result, result_x, result_y, r_misc, s_time):
      competitors = (Constants.singles_competitors if len(players) == 2 else Constants.doubles_competitors)
      self.player = players[competitors.index(player)]
      self.stroke = stroke
      self.stroke_type = stroke_type
      self.path = Path(Coordinate(stroke_x, stroke_y, 'impact'), Coordinate(result_x, result_y, 'mark'))
      self.result = result
      self.r_misc = r_misc
      self.s_time = s_time

   def __repr__(self):
      return repr((self.player, self.stroke, self.stroke_type, self.result, self.path))


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
      player_index = Constants.singles_competitors.index(winner)
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
      player_index = (None if winner not in Constants.singles_competitors else Constants.singles_competitors.index(winner))
      self.winner = (None if player_index is None else players[player_index])
      self.score = {players[0]: player_1_score, players[1]: player_2_score}
      self.points = points
      self.g_time = g_time

   def __repr__(self):
      return repr((self.winner, self.score, self.points[-1].score))


class Set:

   def __init__(self, players, winner, player_1, player_2, games):
      player_index = (None if winner not in Constants.singles_competitors else Constants.singles_competitors.index(winner))
      self.winner = (None if player_index is None else players[player_index])
      self.games = games
      self.breaks = [game for game in games if game.server != game.winner]
      self.score = Counter([game.winner for game in self.games])

   def __repr__(self):
      return repr((self.score))


class Match:

   def __init__(self, sides, players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                start_time, finish_time, first_server, player_ends, winner, sets):
      self.sides = sides
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
      player_index = (None if winner not in Constants.singles_competitors else Constants.singles_competitors.index(winner))
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
        self.service_games = [game for game in self.games if game.server in self.name]
        self.receiving_games = [game for game in self.games if game not in self.service_games]
        self.opponent = (None if not len(self.service_games) else self.service_games[0].receiver)

        self.all_points = [point for game in self.games for point in game.points]
        self.service_points = [point for game in self.service_games for point in game.points]
        self.receiving_points = [point for game in self.receiving_games for point in game.points]

        self.all_shots = [shot for point in self.all_points for shot in point.shots if shot.player == self.name]
        self.approach_shots = [shot for shot in self.all_shots if shot.path.impact.location in Constants.Approach]
        self.approach_shots_won = [shot for shot in self.approach_shots if shot.result in Constants.point_won]
        self.approach_shots_pct = (None if not len(self.approach_shots) else math.ceil(len(self.approach_shots_won) * 100 / len(self.approach_shots)))

        self.points_won = [point for game in self.games for point in game.points if self.name == point.winner]
        self.points_won_serving = [point for game in self.service_games for point in game.points if self.name == point.winner]
        self.points_won_receiving = [point for game in self.receiving_games for point in game.points if self.name == point.winner]

        self.avg_rally_length = (None if not len(self.all_points) else math.ceil(sum([int(point.rally_length) for point in self.all_points]) / len(self.all_points)))
        self.avg_rally_length_serving = (None if not len(self.service_points) else
                                         math.ceil(sum([int(point.rally_length) for point in self.service_points]) / len(self.service_points)))
        self.avg_rally_length_receiving = (None if not len(self.receiving_points) else
                                           math.ceil(sum([int(point.rally_length) for point in self.receiving_points]) / len(self.receiving_points)))
        self.avg_rally_length_points_won = (None if not len(self.points_won) else
                                            math.ceil(sum([int(point.rally_length) for point in self.points_won]) / len(self.points_won)))
        self.avg_rally_length_points_won_serving = (None if not len(self.points_won_serving) else
                                                    math.ceil(sum([int(point.rally_length) for point in self.points_won_serving]) / len(self.points_won_serving)))
        self.avg_rally_length_points_won_receiving = (None if not len(self.points_won_receiving) else
                                                      math.ceil(sum([int(point.rally_length) for point in self.points_won_receiving]) / len(self.points_won_receiving)))

        self.breaks = [game for game in self.games if game.server != self.name and game.winner == self.name]
        self.breakpoints = [point for point in self.all_points if point.server == self.opponent
                            and (point.score[self.name] == Constants.advantage
                                 or (point.score[self.name] == Constants.forty and point.score[self.opponent] != Constants.forty))]
        self.breakpoints_pct = (None if not len(self.breakpoints) else round(len(self.breaks) * 100 / len(self.breakpoints)))

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
        self.winners = [point for point in self.points_won if point.shots[-1].player == self.name and point.shots[-1].result in Constants.winner]
        self.forcing_errors = [point for point in self.points_won if point.shots[-1].player == self.name and point.shots[-1].result in Constants.forcing_error]

        self.points_pct = (None if not len(self.all_points) else round(len(self.points_won) * 100 / len(self.all_points)))
        self.points_won_1st_serve = [point for point in self.points_won if point.server == self.name and Constants.second_serve not in point.stroke_types]
        self.points_pct_1st_serve = (None if not len(self.first_serves_in) else round(len(self.points_won_1st_serve) * 100 / len(self.first_serves_in)))
        self.points_won_2nd_serve = [point for point in self.points_won if point.server == self.name and Constants.second_serve in point.stroke_types]
        self.points_pct_2nd_serve = (None if not len(self.second_serves) else round(len(self.points_won_2nd_serve) * 100 / len(self.second_serves)))

        self.points_won_receiving = [point for point in self.points_won if point.receiver == self.name]
        self.points_pct_receiving = (None if not len(self.receiving_points) else round(len(self.points_won_receiving) * 100 / len(self.receiving_points)))

        self.aggressive_margin = len(self.aces + self.serve_winners + self.winners + self.forcing_errors) - len(self.double_faults + self.unforced_errors)
        self.aggressive_margin_pct = round(self.aggressive_margin * 100 / len(self.all_points))

        self.returns_1st_serve = [point for point in self.receiving_points if Constants.first_return in point.stroke_types]
        self.returns_1st_in_play = [shot for point in self.returns_1st_serve for shot in point.shots if shot.stroke_type == Constants.first_return and shot.result in Constants.not_out]
        self.returns_1st_pct = (None if not len(self.returns_1st_serve) else round(len(self.returns_1st_in_play) * 100 / len(self.returns_1st_serve)))

        self.returns_2nd_serve = [point for point in self.receiving_points if Constants.second_return in point.stroke_types]
        self.returns_2nd_in_play = [shot for point in self.returns_2nd_serve for shot in point.shots if shot.stroke_type == Constants.second_return and shot.result in Constants.not_out]
        self.returns_2nd_pct = (None if not len(self.returns_2nd_serve) else round(len(self.returns_2nd_in_play) * 100 / len(self.returns_2nd_serve)))

        self.returns = self.returns_1st_serve + self.returns_2nd_serve
        self.returns_in_play = self.returns_1st_in_play + self.returns_2nd_in_play
        self.returns_in_play_pct = (None if not len(self.returns) else round(len(self.returns_in_play) * 100 / len(self.returns)))

    def __repr__(self):
        return repr((self.first_serves_pct, self.second_serves_pct))


class FormatStats:

    def __init__(self, stats):
        self.first_serve_pct = ("" if not stats.first_serve_pct else "{0:.0f}%".format(stats.first_serve_pct))
        self.aces_service_winners = "{0:.0f} / {1:.0f}".format(len(stats.aces), len(stats.serve_winners))
        self.double_faults = "{0:.0f}".format(len(stats.double_faults))
        self.unforced_errors = "{0:.0f}".format(len(stats.unforced_errors))
        self.winners_forcing_errors = "{0:.0f} / {1:.0f}".format(len(stats.winners), len(stats.forcing_errors))
        self.points_won = "{0} ({1:.0f}%)".format(len(stats.points_won), stats.points_pct)
        self.points_won_1st_serve = ("" if not (len(stats.points_won_1st_serve) and len(stats.first_serves_in) and stats.points_pct_1st_serve) else
                                     "{0} of {1} ({2:.0f}%)".format(len(stats.points_won_1st_serve), len(stats.first_serves_in), stats.points_pct_1st_serve))
        self.points_won_2nd_serve = ("" if not (len(stats.points_won_2nd_serve) and len(stats.second_serves) and stats.points_pct_2nd_serve) else
                                     "{0} of {1} ({2:.0f}%)".format(len(stats.points_won_2nd_serve), len(stats.second_serves), stats.points_pct_2nd_serve))
        self.points_won_receiving = ("" if not (len(stats.points_won_receiving) and len(stats.receiving_points) and stats.points_pct_receiving) else
                                     "{0} of {1} ({2:.0f}%)".format(len(stats.points_won_receiving), len(stats.receiving_points), stats.points_pct_receiving))
        self.break_points_converted = ("" if not (len(stats.breaks) and len(stats.breakpoints) and stats.breakpoints_pct) else
                                       "{0} of {1} ({2:.0f}%)".format(len(stats.breaks), len(stats.breakpoints), stats.breakpoints_pct))
        self.successful_net_approaches = ("" if not (len(stats.approach_shots_won) and len(stats.approach_shots) and stats.approach_shots_pct) else
                                          "{0} of {1} ({2:.0f}%)".format(len(stats.approach_shots_won), len(stats.approach_shots), stats.approach_shots_pct))
        self.returns_in_play = ("" if not (stats.returns_in_play_pct and stats.returns_1st_pct and stats.returns_2nd_pct) else
                                "{0:.0f}% ({1:.0f}% / {2:.0f}%)".format(stats.returns_in_play_pct, stats.returns_1st_pct, stats.returns_2nd_pct))
        self.aggressive_margin = "{0:.0f} ({1:.0f}%)".format(stats.aggressive_margin, stats.aggressive_margin_pct)


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
      data += ['' for x in range(10)]
      if data[0] == Constants.MatchDetails:
         sides = data[1:3]
         if '+' in sides[0] or '&' in sides[0]:
             side_1_separator = ('+' if sides[0].find('+') > -1 else '&')
             side_2_separator = ('+' if sides[1].find('+') > -1 else '&')
             players = sides[0].split(side_1_separator) + sides[0].split(side_2_separator)
             players = [player.strip() for player in players]
         else:
             players = sides
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

   return Match(sides, players, match_date, in_out, number_of_sets, match_games, format_description, advantage, lets,
                start_time, finish_time, first_server, player_ends, winner, sets)


def match_stats(match):
    side_one = match.sides[0]
    side_two = match.sides[1]
    side_one_stats = PlayerStats(side_one, match)
    side_two_stats = PlayerStats(side_two, match)
    p1fs = FormatStats(side_one_stats.match_stats)
    p2fs = FormatStats(side_two_stats.match_stats)

    width = 25
    print (side_one.center(width), "--PLAYER--".center(width), side_two.center(width))
    print (p1fs.first_serve_pct.center(width), "First Serve Percentage".center(width), p2fs.first_serve_pct.center(width))
    print (p1fs.aces_service_winners.center(width), "Aces/Service Winners".center(width), p2fs.aces_service_winners.center(width))
    print (p1fs.double_faults.center(width), "Double Faults".center(width), p2fs.double_faults.center(width))
    print (p1fs.unforced_errors.center(width), "Unforced Errors".center(width), p2fs.unforced_errors.center(width))
    print (p1fs.winners_forcing_errors.center(width), "Winners/Forcing Errors".center(width), p2fs.winners_forcing_errors.center(width))
    print (p1fs.points_won.center(width), "Total Points Won".center(width), p2fs.points_won.center(width))
    print (p1fs.points_won_1st_serve.center(width), "Points Won 1st Serve".center(width), p2fs.points_won_1st_serve.center(width))
    print (p1fs.points_won_2nd_serve.center(width), "Points Won 2nd Serve".center(width), p2fs.points_won_2nd_serve.center(width))
    print (p1fs.points_won_receiving.center(width), "Points Won Receiving".center(width), p2fs.points_won_receiving.center(width))
    print (p1fs.break_points_converted.center(width), "Break Points Converted".center(width), p2fs.break_points_converted.center(width))
    print (p1fs.successful_net_approaches.center(width), "Successful Net Approaches".center(width), p2fs.successful_net_approaches.center(width))
    print (p1fs.returns_in_play.center(width), "% Returns in Play".center(width), p2fs.returns_in_play.center(width))
    print (p1fs.aggressive_margin.center(width), "Aggressive Margin".center(width), p2fs.aggressive_margin.center(width))


match = parse('abcd.ptf')
match_stats(match)
