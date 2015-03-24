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

    ''' Shot Types '''
    Serve = 'Serve'
    Forehand = 'Forehand'
    Backhand = 'Backhand'
    Return = 'Return'
    Missed = 'Missed'

    ''' Serve Types '''
    FirstServe = 'First Serve'
    SecondServe = 'Second Serve'
    ServeTypes = [FirstServe, SecondServe]

    ''' Return Types '''
    FirstReturn = 'First Return'
    SecondReturn = 'Second Return'

    ''' Return / Key Stroke Stroke Types '''
    Drive = 'Drive'
    Slice = 'Slice'
    Volley = 'Volley'
    Overhead = 'Overhead'
    Lob = 'Lob'
    DropShot = 'Drop Shot'
    Other = 'Other'

    ReturnStrokeTypes = ['First Return', 'Second Return']
    KeyStrokeTypes = [Drive, Slice, Volley, Overhead, Lob, DropShot, Other]

    ''' Service Outcomes '''
    ServeIn = 'In'
    ServeWinner = 'Serve Winner'
    Ace = 'Ace'
    Let = 'Let'
    FootFault = 'Foot Fault'

    ''' Return Outcomes '''
    ReturnIn = 'In'
    Volleyed = 'Volleyed'
    ReturnWinner = 'Winner'
    PassingShot = 'Passing Shot'
    ForcingError = 'Forcing Error'
    ForcingVolleyError = 'Forcing Volley Error'
    NetCord = 'Net Cord'
    InOffNet = 'In Off-Net'

    ''' Key Shot Outcomes '''
    Winner = 'Winner'
    PassingShot = 'Passing Shot'
    ForcingError = 'Forcing Error'
    NetCord = 'Net Cord'
    PutAway = 'Put-Away'

    Out = 'Out'
    OutPassingShot = 'Out Passing Shot'
    OutOffNet = 'Out Off-Net'

    NettedPassingShot = 'Netted Passing Shot'
    Netted = 'Netted'

    InServiceOutcomes = [ServeIn, ServeWinner, Ace]
    WinningServiceOutcomes = [Ace, ServeWinner]
    FaultServiceOutcomes = [Out, OutOffNet, FootFault]
    OutServiceOutcomes = [Out, OutOffNet]
    ServiceErrors = [Netted, Out, OutOffNet]
    ServiceOutcomes = InServiceOutcomes + FaultServiceOutcomes
    InReturnOutcomes = [ReturnIn, Volleyed, ReturnWinner, PassingShot, ForcingError, ForcingVolleyError, NetCord, InOffNet]
    InPlayOutcomes = [ServeIn, ReturnIn, Volleyed, NetCord, InOffNet]
    OutReturnOutcomes = [Out, OutPassingShot, OutOffNet]
    WinningKeyShotOutcomes = WinningReturnOutcomes = [Winner, PassingShot, ForcingError, NetCord, PutAway]
    Winners = [Winner, PassingShot, PutAway]
    OutKeyShotOutcomes = [Out, OutPassingShot, OutOffNet]
    NettedKeyShotOutcomes = [NettedPassingShot, Netted]
    ErrorOpponentAtNet = [NettedPassingShot, OutPassingShot]
    InOpponentAtNet = [PassingShot]
    WinningOutcomes = WinningServiceOutcomes + WinningKeyShotOutcomes
    ForcingErrors = [ForcingError, ForcingVolleyError]
    Errors = NotIn = OutReturnOutcomes + NettedKeyShotOutcomes + [FootFault]
    NotOut = InReturnOutcomes + WinningKeyShotOutcomes + InServiceOutcomes

    WinningShots = 'Winning Shots'
    ForcingShots = 'Forcing Shots'

    ''' Shot Trajectory '''
    Crosscourt = 'Crosscourt'
    ShortAngle = 'Short Angle'
    Center = 'Center'
    Line = 'Line'

    ''' Locations '''
    DoublesAlley = 'Doubles Alley'
    VolleyZone = 'Volley Zone'
    LtSvcBox = 'Left Service Box'
    RtSvcBox = 'Right Service Box'
    ServiceLine = 'Service Line'
    NoMans = "No Man's"
    Baseline = 'Baseline'
    Net = 'Net'
    Long = 'Long'
    Deep = 'Deep'

    ''' Courts '''
    FarCourt = 'Far'
    NearCourt = 'Near'

    ''' Placement '''
    Wide = 'Wide'
    Body = 'Body'
    T = 'T'

    Fifteen = '15'
    Thirty = '30'
    Forty = '40'
    Deuce = 'D'
    GameWon = 'G'
    Advantage = 'A'

    All = 'All'

    [centerline_x, net_y] = [120, 160]
    doubles_wide_x = [18, 230]
    singles_wide_x = [singles_min_x, singles_max_x] = [37, 203]
    out_long_y = [out_long_far_y, out_long_near_y] = [16, 303]
    service_line_y = [service_line_near_y, service_line_far_y] = [90, 230]
    svc_left_x = [singles_min_x, centerline_x + 3]
    svc_right_x = [centerline_x - 3, singles_max_x]
    baseline_zone_y = [baseline_zone_far_y, baseline_zone_near_y] = [out_long_far_y + 20, out_long_near_y - 20]
    no_mans_zone_y = [no_mans_zone_far_y, no_mans_zone_near_y] = [baseline_zone_far_y + 30, baseline_zone_near_y - 30]
    approach_y = [service_line_near_y, service_line_far_y]


class Comment:

   def __init__(self, player, comment):
      self.player = player
      self.comment = comment

   def __repr__(self):
      return repr((self.player, self.comment))


class Coordinate:

   def __init__(self, x, y, c_type):
      [self.court, self.in_doubles, self.in_singles] = [None, None, None]
      [self.right_service_box, self.left_service_box, self.service_boxes, self.service_line] = [None, None, None, None]
      [self.no_mans_land, self.baseline, self.court, self.location, self.x, self.y] = [None, None, None, None, None, None]

      if not (x or y):
          return

      self.x = float(x)
      self.y = float(y)

      self.court = (Constants.Net if self.y == Constants.net_y else (Constants.FarCourt if self.y < Constants.net_y else Constants.NearCourt))
      self.in_doubles = (self.between(Constants.doubles_wide_x, self.x) and self.between(Constants.out_long_y, self.y) and not (self.y == Constants.net_y))
      self.in_singles = (self.between(Constants.singles_wide_x, self.x) and self.between(Constants.out_long_y, self.y) and not (self.y == Constants.net_y))
      self.volley_zone = self.between(Constants.service_line_y, self.y and not self.court == Constants.Net)
      self.right_service_box = (self.between(Constants.service_line_y, self.y) and
                                ((self.between(Constants.svc_left_x, self.x) and self.court == Constants.FarCourt)
                                or (self.between(Constants.svc_right_x, self.x) and self.court == Constants.NearCourt)))
      self.left_service_box = (self.between(Constants.service_line_y, self.y) and
                               ((self.between(Constants.svc_right_x, self.x) and self.court == Constants.FarCourt)
                               or (self.between(Constants.svc_left_x, self.x) and self.court == Constants.NearCourt)))
      self.service_boxes = (self.left_service_box or self.right_service_box)
      self.service_line = (self.between(Constants.no_mans_zone_y, self.y) and not self.service_boxes and not self.court == Constants.Net)
      self.no_mans_land = (self.between(Constants.baseline_zone_y, self.y) and not (self.service_boxes or self.service_line) and not self.court == Constants.Net)
      self.baseline = (self.between(Constants.out_long_y, self.y) and not (self.service_boxes or self.service_line or self.no_mans_land) and not self.court == Constants.Net)
      self.doubles_alley = (self.in_doubles and not self.in_singles)

      self.location = (Constants.LtSvcBox if self.left_service_box else
                       (Constants.RtSvcBox if self.right_service_box else
                        (Constants.ServiceLine if self.service_line else
                         (Constants.VolleyZone if self.volley_zone else
                          (Constants.NoMans if self.no_mans_land else
                           (Constants.Baseline if self.baseline else
                            (Constants.Net if self.court == Constants.Net else
                             (Constants.Long if c_type == 'mark' else Constants.Deep))))))))

   def between(self, coordinate_pair, z):
       return (True if z >= coordinate_pair[0] and z <= coordinate_pair[1] else False)

   def __repr__(self):
      return repr((self.court, self.location))


class Path:

   def __init__(self, impact, mark):
       [self.trajectory] = [None]

       self.impact = impact
       self.mark = mark
       if not (self.impact.x or self.impact.y or mark.x or mark.y):
           return

       if ((self.impact.x <= Constants.centerline_x and self.mark.x > Constants.centerline_x)
          or (self.impact.x > Constants.centerline_x and self.mark.x <= Constants.centerline_x)):
           if self.mark.y > Constants.service_line_near_y and self.mark.y < Constants.service_line_far_y:
               self.trajectory = Constants.ShortAngle
           else:
               self.trajectory = Constants.Crosscourt
       elif self.mark.x > Constants.centerline_x - 40 and self.mark.x < Constants.centerline_x + 40:
           self.trajectory = Constants.Center
       else:
           self.trajectory = Constants.Line

       delta_x = self.impact.x - self.mark.x
       delta_y = self.impact.y - self.mark.y
       ''' angle can be used to calculate inside-out forehands/backhands or Wide-Body-T Serves'''
       self.angle = math.degrees(math.atan2(delta_y, delta_x))
       self.distance = math.sqrt((delta_x) ** 2 + (delta_y) ** 2)

   def __repr__(self):
      return repr((self.impact, self.mark, self.trajectory))


class Shot:

   def __init__(self, players, player, stroke, stroke_type, stroke_x, stroke_y, result, result_x, result_y, r_misc, s_time):
      self.placement = ''
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


class Point:

   def __init__(self, players, winner, T_score, O_score, p_time, rally_length, shots):
      self.players = players
      player_index = Constants.singles_competitors.index(winner)
      self.winner = (None if player_index < 0 else players[player_index])
      self.score = {players[0]: T_score, players[1]: O_score}
      self.p_time = p_time
      self.rally_length = rally_length
      self.shots = shots
      self.strokes = [shot.stroke for shot in self.shots]
      self.stroke_types = [shot.stroke_type for shot in self.shots]
      self.service_winner_1st = (True if len([True for shot in self.shots
                                              if shot.stroke == Constants.Serve
                                              and shot.stroke_type == Constants.FirstServe
                                              and shot.result in Constants.WinningServiceOutcomes]) else False)
      self.service_winner_2nd = (True if len([True for shot in self.shots
                                              if shot.stroke == Constants.Serve
                                              and shot.stroke_type == Constants.SecondServe
                                              and shot.result in Constants.WinningServiceOutcomes]) else False)
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
      self.breakpoints = [point for point in self.points
                          if (point.score[self.receiver] == Constants.Advantage
                              or (point.score[self.receiver] == Constants.Forty and point.score[self.server] != Constants.Forty))]

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
      [self.sides, self.players, self.match_date] = [sides, players, match_date]
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

      self.side_one = self.sides[0]
      self.side_two = self.sides[1]
      self.side_one_stats = PlayerStats(self.side_one, self)
      self.side_two_stats = PlayerStats(self.side_two, self)

   def display_stats(self, width=30, dataset='match', grouping='Basic', view='Table'):
      if dataset == 'match':
          p1s = self.side_one_stats.match_stats
          p2s = self.side_two_stats.match_stats
      elif dataset in list(range(len(self.sets))):
          p1s = self.side_one_stats.sets[dataset]
          p2s = self.side_two_stats.sets[dataset]
      p1fs = [stat for stat in p1s.stats if grouping in stat.groupings]
      p2fs = [stat for stat in p2s.stats if grouping in stat.groupings]
      title = '--' + grouping + '--'

      if view == 'Compare':
          print(self.side_one.center(width), title.center(width), self.side_two.center(width))
      else:
          print(title.ljust(width), self.side_one.ljust(width), self.side_two.ljust(width))

      for i, stat in enumerate(p1fs):
          if view == 'Compare':
              print(p1fs[i].formatted.center(width), p1fs[i].title.center(width), p2fs[i].formatted.center(width))
          else:
              print(p1fs[i].title.ljust(width), p1fs[i].formatted.ljust(width), p2fs[i].formatted.ljust(width))

   def __repr__(self):
      return repr((self.players, self.match_date, self.set_score))


class PlayerStats:

    def __init__(self, name, match):
        self.sets = {}
        [self.name, self.match] = [name, match]
        self.match_stats = Stats(name, match.games)
        for s, Set in enumerate(match.sets):
            self.sets[s] = Stats(name, match.sets[s].games)

    def __repr__(self):
        return repr((self.name))


class Stats:

    def __init__(self, player, games):
        self.player = player
        self.games = games
        self.base_stats()
        self.stroke_stats()
        self.point_stats()
        self.stats()

    def base_stats(self):
        self.games_won = [game for game in self.games if self.player == game.winner]
        self.service_games = [game for game in self.games if game.server in self.player]
        self.receiving_games = [game for game in self.games if game not in self.service_games]
        self.breaks = [game for game in self.games if game.server != self.player and game.winner == self.player]
        self.break_opportunities = [game for game in self.receiving_games if len(game.breakpoints) > 0]
        self.breakgames_pct = (None if not len(self.break_opportunities) else round(len(self.breaks) * 100 / len(self.break_opportunities)))
        self.opponent = (None if not len(self.service_games) else self.service_games[0].receiver)

        self.all_points = [point for game in self.games for point in game.points]
        self.service_points = [point for game in self.service_games for point in game.points]
        self.receiving_points = [point for game in self.receiving_games for point in game.points]

    def stroke_stats(self):
        self.all_player_shots = [shot for point in self.all_points for shot in point.shots if shot.player == self.player]
        self.all_opponent_shots = [shot for point in self.all_points for shot in point.shots if shot.player != self.player]

        self.forehand = KeyShot(*[StrokeType(Constants.Forehand, stroke_type, self.all_player_shots) for stroke_type in Constants.KeyStrokeTypes])
        self.backhand = KeyShot(*[StrokeType(Constants.Backhand, stroke_type, self.all_player_shots) for stroke_type in Constants.KeyStrokeTypes])
        self.serve = Serve(*[StrokeType(Constants.Serve, serve_type, self.all_player_shots) for serve_type in Constants.ServeTypes])
        self.service_return = Return(*[StrokeType(Constants.Return, return_type, self.all_player_shots) for return_type in Constants.ReturnStrokeTypes])

        self.winners = self.forehand.winners[Constants.All] + self.backhand.winners[Constants.All] + self.service_return.winners[Constants.All]
        self.unforced_errors = self.forehand.errors[Constants.All] + self.backhand.errors[Constants.All] + self.service_return.errors[Constants.All]
        self.forced_errors = [shot for shot in self.all_opponent_shots if shot.result in Constants.ForcingErrors]

        self.winning_shots = self.forehand.winners[Constants.WinningShots] + self.backhand.winners[Constants.WinningShots] + self.service_return.winners[Constants.WinningShots]
        self.forcing_errors = self.forehand.winners[Constants.ForcingShots] + self.backhand.winners[Constants.ForcingShots] + self.service_return.winners[Constants.ForcingShots]

        self.aces = self.serve.winners[Constants.Ace]
        self.serve_winners = self.serve.winners[Constants.ServeWinner]
        self.double_faults = self.serve.double_faults
        self.lets = self.serve.first.lets + self.serve.second.lets

        self.approach_shots = [shot for shot in self.all_player_shots if self.between(Constants.approach_y, shot.path.impact.y)]
        self.opponent_failed_passing = [shot for shot in self.all_opponent_shots if shot.player != self.player and shot.result in Constants.ErrorOpponentAtNet]
        self.opponent_passing_winners = [shot for shot in self.all_opponent_shots if shot.player != self.player and shot.result in Constants.InOpponentAtNet]
        self.approach_shot_winners = [shot for shot in self.approach_shots if shot.result in Constants.WinningKeyShotOutcomes]
        self.approach_attempts = self.approach_shots + self.opponent_failed_passing + self.opponent_passing_winners
        self.points_won_at_net = self.approach_shot_winners + self.opponent_failed_passing
        self.approach_attempts_pct = (None if not len(self.approach_attempts) else math.ceil(len(self.points_won_at_net) * 100 / len(self.approach_attempts)))
        return

    def between(self, coordinate_pair, z):
        if not z:
            return None
        return (True if z >= coordinate_pair[0] and z <= coordinate_pair[1] else False)

    def point_stats(self):
        self.points_won = [point for game in self.games for point in game.points if self.player == point.winner]
        self.points_missing_stat = [point for point in self.points_won if Constants.Missed in point.strokes]
        self.points_won_serving = [point for game in self.service_games for point in game.points if self.player == point.winner]
        self.points_won_receiving = [point for game in self.receiving_games for point in game.points if self.player == point.winner]
        self.points_won_at_net_pct = (None if not len(self.points_won_at_net) else round(len(self.points_won_at_net) * 100 / len(self.points_won)))

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

        self.breakpoints = [point for point in self.all_points if point.server == self.opponent
                            and (point.score[self.player] == Constants.Advantage
                                 or (point.score[self.player] == Constants.Forty and point.score[self.opponent] != Constants.Forty))]
        self.breakpoints_pct = (None if not len(self.breakpoints) else round(len(self.breaks) * 100 / len(self.breakpoints)))

        self.first_serves = [shot for game in self.service_games for point in game.points for shot in point.shots if shot.stroke_type == Constants.FirstServe]
        self.first_serves_in = [serve for serve in self.first_serves if serve.result in Constants.NotOut and serve.result != Constants.Let]

        self.points_pct = (None if not len(self.all_points) else round(len(self.points_won) * 100 / len(self.all_points)))
        self.points_won_1st_serve = [point for point in self.points_won
                                     if point.server == self.player == point.winner
                                     and Constants.Missed not in point.strokes
                                     and Constants.SecondServe not in point.stroke_types]
        self.points_pct_1st_serve = (None if not len(self.first_serves_in) else round(len(self.points_won_1st_serve) * 100 / len(self.first_serves_in)))
        self.points_won_2nd_serve = [point for point in self.points_won if point.server == self.player and Constants.SecondServe in point.stroke_types]
        self.points_pct_2nd_serve = (None if not len(self.serve.second.shots) else round(len(self.points_won_2nd_serve) * 100 / len(self.serve.second.shots)))

        self.points_won_receiving = [point for point in self.points_won if point.receiver == self.player]
        self.points_pct_receiving = (None if not len(self.receiving_points) else round(len(self.points_won_receiving) * 100 / len(self.receiving_points)))

        self.aggressive_margin = len(self.aces + self.serve_winners + self.winning_shots + self.forcing_errors) - len(self.double_faults + self.unforced_errors)
        self.aggressive_margin_pct = round(self.aggressive_margin * 100 / len(self.all_points))

        self.returns_1st_serve = [point for point in self.receiving_points if Constants.FirstReturn in point.stroke_types or point.service_winner_1st]
        self.returns_1st_in_play = [shot for point in self.returns_1st_serve for shot in point.shots if shot.stroke_type == Constants.FirstReturn and shot.result in Constants.NotOut]
        self.returns_1st_pct = (None if not len(self.returns_1st_serve) else round(len(self.returns_1st_in_play) * 100 / len(self.returns_1st_serve)))

        self.returns_2nd_serve = [point for point in self.receiving_points if Constants.SecondReturn in point.stroke_types or point.service_winner_2nd]
        self.returns_2nd_in_play = [shot for point in self.returns_2nd_serve for shot in point.shots if shot.stroke_type == Constants.SecondReturn and shot.result in Constants.NotOut]
        self.returns_2nd_pct = (None if not len(self.returns_2nd_serve) else round(len(self.returns_2nd_in_play) * 100 / len(self.returns_2nd_serve)))

        self.returns = self.returns_1st_serve + self.returns_2nd_serve
        self.returns_in_play = self.returns_1st_in_play + self.returns_2nd_in_play
        self.returns_in_play_pct = (None if not len(self.returns) else round(len(self.returns_in_play) * 100 / len(self.returns)))

    def stats(self):
        self.stats = []
        format_p = "{0:.0f}%"
        format_n = "{0:.0f}"
        format_nn = "{0:.0f} / {1:.0f}"
        format_fs_p = "{0} of {1} ({2:.0f}%)"
        format_n_p = "{0:.0f} ({1:.0f}%)"
        self.stats.append(Stat("First Serve Percentage", ['Basic'], self.serve.first.percentage,
                               ("" if not self.serve.first.percentage else format_p.format(self.serve.first.percentage))))
        self.stats.append(Stat("Aces/Service Winners", ['Basic'], len(self.serve.winners[Constants.Ace] + self.serve.winners[Constants.ServeWinner]),
                               format_nn.format(len(self.serve.winners[Constants.Ace]), len(self.serve.winners[Constants.ServeWinner]))))
        self.stats.append(Stat("Second Serve Percentage", ['Basic'], self.serve.second.percentage,
                               ("" if not self.serve.second.percentage else format_p.format(self.serve.second.percentage))))
        self.stats.append(Stat("Double Faults", ['Basic'], self.serve.double_faults, format_n.format(len(self.serve.double_faults))))
        self.stats.append(Stat("Lets", ['Basic'], self.lets, "{0:.0f}".format(len(self.lets))))
        self.stats.append(Stat("Unforced Errors", ['Basic'], self.unforced_errors, format_n.format(len(self.unforced_errors))))
        self.stats.append(Stat("Winners/Forcing Errors", ['Basic'], len(self.winning_shots + self.forcing_errors),
                               format_nn.format(len(self.winning_shots), len(self.forcing_errors))))
        self.stats.append(Stat("Winning Returns", ['Basic'], self.service_return.winners[Constants.All], format_n.format(len(self.service_return.winners[Constants.All]))))
        self.stats.append(Stat("Total Points Won", ['Basic'], self.points_won, format_n_p.format(len(self.points_won), self.points_pct)))
        self.stats.append(Stat("Points Won 1st Serve", ['Basic'], self.points_won_1st_serve,
                               ("" if not (len(self.points_won_1st_serve) and len(self.first_serves_in) and self.points_pct_1st_serve) else
                                format_fs_p.format(len(self.points_won_1st_serve), len(self.first_serves_in), self.points_pct_1st_serve))))
        self.stats.append(Stat("Points Won 2nd Serve", ['Basic'], self.points_won_2nd_serve,
                               ("" if not (len(self.points_won_2nd_serve) and len(self.serve.second.shots) and self.points_pct_2nd_serve) else
                                format_fs_p.format(len(self.points_won_2nd_serve), len(self.serve.second.shots), self.points_pct_2nd_serve))))
        self.stats.append(Stat("Points Won Receiving", ['Basic'], self.points_won_receiving,
                               ("" if not (len(self.points_won_receiving) and len(self.receiving_points) and self.points_pct_receiving) else
                                format_fs_p.format(len(self.points_won_receiving), len(self.receiving_points), self.points_pct_receiving))))
        self.stats.append(Stat("Break Points Converted", ['Basic'], self.breaks,
                               ("" if not (len(self.breaks) and len(self.breakpoints) and self.breakpoints_pct) else
                                format_fs_p.format(len(self.breaks), len(self.breakpoints), self.breakpoints_pct))))
        self.stats.append(Stat("Break Games Converted", ['Basic'], self.breaks,
                               ("" if not (len(self.breaks) and len(self.break_opportunities) and self.breakgames_pct) else
                                format_fs_p.format(len(self.breaks), len(self.break_opportunities), self.breakgames_pct))))
        self.stats.append(Stat("Successful Net Approaches", ['Basic'], self.points_won_at_net,
                               ("" if not (len(self.points_won_at_net) and len(self.approach_attempts) and self.approach_attempts_pct) else
                                format_fs_p.format(len(self.points_won_at_net), len(self.approach_attempts), self.approach_attempts_pct))))
        self.stats.append(Stat("% of Points Won at Net", ['Basic'], self.points_won_at_net_pct,
                               ("" if not (len(self.points_won_at_net) and len(self.points_won) and self.points_won_at_net_pct) else
                                format_fs_p.format(len(self.points_won_at_net), len(self.points_won), self.points_won_at_net_pct))))
        self.stats.append(Stat("% Returns in Play", ['Basic'], self.returns_in_play,
                               ("" if not (self.returns_in_play_pct and self.returns_1st_pct and self.returns_2nd_pct) else
                                "{0:.0f}% ({1:.0f}% / {2:.0f}%)".format(self.returns_in_play_pct, self.returns_1st_pct, self.returns_2nd_pct))))
        self.stats.append(Stat("Aggressive Margin", ['Basic'], self.aggressive_margin,
                               format_n_p.format(self.aggressive_margin, self.aggressive_margin_pct)))

        format_wbt = "{0:3}% Wide, {1:3}% Body, {2:3}% T"
        placement = 'Placement'
        for result in ['In', 'Ace', 'Netted', 'Out']:
            total = sum(self.serve.first.placement[result].values())
            self.stats.append(Stat("1st Serves " + result, [placement], total,
                              format_wbt.format((0 if not total else round(self.serve.first.placement[result][Constants.Wide] * 100 / total)),
                                                (0 if not total else round(self.serve.first.placement[result][Constants.Body] * 100 / total)),
                                                (0 if not total else round(self.serve.first.placement[result][Constants.T] * 100 / total)))))
            total = sum(self.serve.second.placement[result].values())
            self.stats.append(Stat("2nd Serves " + result, [placement], total,
                              format_wbt.format((0 if not total else round(self.serve.second.placement[result][Constants.Wide] * 100 / total)),
                                                (0 if not total else round(self.serve.second.placement[result][Constants.Body] * 100 / total)),
                                                (0 if not total else round(self.serve.second.placement[result][Constants.T] * 100 / total)))))

        total_winners = len(self.winning_shots)
        format_pct = "{0:3}% ({1} of {2})"
        points_won_at_net = [shot for shot in self.winning_shots if shot.path.impact.location in ["Volley Zone", "Left Service Box", "Right Service Box"]]
        winners_at_net_pct = (0 if not total_winners else round(len(points_won_at_net) * 100 / total_winners))
        self.stats.append(Stat("% Winners at Net", [placement], winners_at_net_pct,
                               format_pct.format(winners_at_net_pct, len(points_won_at_net), total_winners)))
        points_won_in_nomans = [shot for shot in self.winning_shots if shot.path.impact.location in ["No Man's", "Service Line"]]
        winners_from_nomans_pct = (0 if not total_winners else round(len(points_won_in_nomans) * 100 / total_winners))
        self.stats.append(Stat("% Winners from No Man's", [placement], winners_from_nomans_pct,
                               format_pct.format(winners_from_nomans_pct, len(points_won_in_nomans), total_winners)))
        points_won_baseline = [shot for shot in self.winning_shots if shot.path.impact.location in ["Baseline", "Out"]]
        winners_from_baseline_pct = (0 if not total_winners else round(len(points_won_baseline) * 100 / total_winners))
        self.stats.append(Stat("% Winners from Baseline", [placement], winners_from_baseline_pct,
                               format_pct.format(winners_from_baseline_pct, len(points_won_baseline), total_winners)))

        total_forced_errors = len(self.forced_errors)
        forced_errors_at_net = [shot for shot in self.forced_errors if shot.path.mark.location in ["Volley Zone", "Left Service Box", "Right Service Box"]]
        forced_errors_net_pct = (0 if not total_forced_errors else round(len(forced_errors_at_net) * 100 / total_forced_errors))
        self.stats.append(Stat("% Forced Errors at Net", [placement], forced_errors_net_pct,
                               format_pct.format(forced_errors_net_pct, len(forced_errors_at_net), total_forced_errors)))
        forced_errors_in_nomans = [shot for shot in self.forced_errors if shot.path.mark.location in ["No Man's", "Service Line"]]
        forced_errors_nomans_pct = (0 if not total_forced_errors else round(len(forced_errors_in_nomans) * 100 / total_forced_errors))
        self.stats.append(Stat("% Forced Errors from No Man's", [placement], forced_errors_nomans_pct,
                               format_pct.format(forced_errors_nomans_pct, len(forced_errors_in_nomans), total_forced_errors)))
        forced_errors_baseline = [shot for shot in self.forced_errors if shot.path.mark.location in ["Baseline", "Out"]]
        forced_errors_baseline_pct = (0 if not total_forced_errors else round(len(forced_errors_baseline) * 100 / total_forced_errors))
        self.stats.append(Stat("% Forced Errors from Baseline", [placement], forced_errors_baseline_pct,
                               format_pct.format(forced_errors_baseline_pct, len(forced_errors_baseline), total_forced_errors)))

        total_unforced_errors = len(self.unforced_errors)
        unforced_errors_at_net = [shot for shot in self.unforced_errors if shot.path.impact.location in ["Volley Zone", "Left Service Box", "Right Service Box"]]
        unforced_errors_net_pct = (0 if not total_unforced_errors else round(len(unforced_errors_at_net) * 100 / total_unforced_errors))
        self.stats.append(Stat("% Unforced Errors at Net", [placement], unforced_errors_net_pct,
                               format_pct.format(unforced_errors_net_pct, len(unforced_errors_at_net), total_unforced_errors)))
        unforced_errors_in_nomans = [shot for shot in self.unforced_errors if shot.path.impact.location in ["No Man's", "Service Line"]]
        unforced_errors_nomans_pct = (0 if not total_unforced_errors else round(len(unforced_errors_in_nomans) * 100 / total_unforced_errors))
        self.stats.append(Stat("% Unforced Errors from No Man's", [placement], unforced_errors_nomans_pct,
                               format_pct.format(unforced_errors_nomans_pct, len(unforced_errors_in_nomans), total_unforced_errors)))
        unforced_errors_baseline = [shot for shot in self.unforced_errors if shot.path.impact.location in ["Baseline", "Out"]]
        unforced_errors_baseline_pct = (0 if not total_unforced_errors else round(len(unforced_errors_baseline) * 100 / total_unforced_errors))
        self.stats.append(Stat("% Unforced Errors from Baseline", [placement], unforced_errors_baseline_pct,
                               format_pct.format(unforced_errors_baseline_pct, len(unforced_errors_baseline), total_unforced_errors)))

        format_errors = "{0}: {1} {2} {3} {4} {5} {6}"
        top_unforced_errors = Counter([(u.path.impact.location, u.path.trajectory, u.stroke, u.stroke_type, u.result, u.path.mark.location) for u in self.unforced_errors])
        sorted_errors = sorted([[top_unforced_errors[key], key] for key in top_unforced_errors], key=lambda x: x[0], reverse=True)
        top_errors = [error for error in sorted_errors if error[0] > 1]
        for count in range(0, 3):
            if count < len(top_errors):
                error_type = list(top_errors[count][1])
                self.stats.append(Stat("#" + str(count + 1) + " Unforced Error", [placement], top_errors[count][0],
                                       format_errors.format(top_errors[count][0], *error_type)))
            else:
                self.stats.append(Stat("#" + str(count + 1) + " Unforced Error", [placement], '',
                                       format_errors.format(0, '', '', '', '', '', '')))

        # top_forced_errors = Counter([(u.path.impact.location, u.path.trajectory, u.stroke, u.result, u.path.mark.location) for u in self.forced_errors])
        # top_error_types = [key for key in top_forced_errors.keys() if top_forced_errors[key] > 2]
        # for count in range(1, 4):
        #     if count <= len(top_error_types):
        #         error_type = list(top_error_types[count - 1])
        #         self.stats.append(Stat("#" + str(count) + " Forced Error", [placement], top_error_types[count - 1],
        #                                format_errors.format(top_unforced_errors[top_error_types[count - 1]], *error_type)))
        #     else:
        #         self.stats.append(Stat("#" + str(count) + " Forced Error", [placement], '',
        #                                format_errors.format(0, '', '', '', '', '')))

        format_fb = "{0:2}: Fhd {1:2} / Bhd {2:2}"
        format_fs = "{0:2}: 1st {1:2} / 2nd {2:2}"
        unforced = 'Unforced Errors'
        errors_drive = self.forehand.drives.error_number + self.backhand.drives.error_number
        self.stats.append(Stat(Constants.Drive, [unforced], errors_drive,
                               format_fb.format(errors_drive, self.forehand.drives.error_number, self.backhand.drives.error_number)))
        errors_slice = self.forehand.slices.error_number + self.backhand.slices.error_number
        self.stats.append(Stat(Constants.Slice, [unforced], errors_slice,
                               format_fb.format(errors_slice, self.forehand.slices.error_number, self.backhand.slices.error_number)))
        errors_volley = self.forehand.volleys.error_number + self.backhand.volleys.error_number
        self.stats.append(Stat(Constants.Volley, [unforced], errors_volley,
                               format_fb.format(errors_volley, self.forehand.volleys.error_number, self.backhand.volleys.error_number)))
        errors_overhead = self.forehand.overheads.error_number + self.backhand.overheads.error_number
        self.stats.append(Stat(Constants.Overhead, [unforced], errors_overhead,
                               format_fb.format(errors_overhead, self.forehand.overheads.error_number, self.backhand.overheads.error_number)))
        errors_lob = self.forehand.lobs.error_number + self.backhand.lobs.error_number
        self.stats.append(Stat(Constants.Lob, [unforced], errors_lob,
                               format_fb.format(errors_lob, self.forehand.lobs.error_number, self.backhand.lobs.error_number)))
        errors_drop_shot = self.forehand.drop_shots.error_number + self.backhand.drop_shots.error_number
        self.stats.append(Stat(Constants.DropShot, [unforced], errors_drop_shot,
                               format_fb.format(errors_drop_shot, self.forehand.drop_shots.error_number, self.backhand.drop_shots.error_number)))
        errors_other = self.forehand.other.error_number + self.backhand.other.error_number
        self.stats.append(Stat(Constants.Other, [unforced], errors_other,
                               format_fb.format(errors_other, self.forehand.other.error_number, self.backhand.other.error_number)))
        self.stats.append(Stat(Constants.Return, [unforced], self.service_return.error_number,
                               format_fs.format(self.service_return.error_number, self.service_return.first.error_number, self.service_return.second.error_number)))
        return

    def __repr__(self):
        return repr((self.serve.first.percentage, self.serve.second.percentage))


class Stat:

    def __init__(self, title, groupings, value, formatted):
        [self.title, self.groupings, self.value, self.formatted] = [title, groupings, value, formatted]

    def __repr__(self):
        return repr((self.title, self.formatted))


class Serve:

    def __init__(self, first, second):
        [self.first, self.second] = [first, second]
        fl = lambda somelist: [item for innerlist in somelist for item in innerlist]
        self.shots = self.first.shots + self.second.shots
        self.number = len(self.shots)
        self.winners = {k: fl([getattr(e, 'winners').get(k, 0) for e in [first, second]]) for k in Constants.WinningServiceOutcomes + [Constants.All]}
        self.errors = {k: fl([getattr(e, 'errors').get(k, 0) for e in [first, second]]) for k in Constants.Errors + [Constants.All]}
        self.double_faults = self.second.all_errors
        self.calc_placement()
        self.first.placement[Constants.Ace] = Counter([shot.placement for shot in first.all_winners])
        self.second.placement[Constants.Ace] = Counter([shot.placement for shot in second.all_winners])
        self.first.placement[Constants.ServeIn] = Counter([shot.placement for shot in first.all_shots_in])
        self.second.placement[Constants.ServeIn] = Counter([shot.placement for shot in second.all_shots_in])
        self.first.placement[Constants.Out] = Counter([shot.placement for shot in first.errors[Constants.Out] + first.errors[Constants.OutOffNet]])
        self.second.placement[Constants.Out] = Counter([shot.placement for shot in second.errors[Constants.Out] + first.errors[Constants.OutOffNet]])
        self.first.placement[Constants.Netted] = Counter([shot.placement for shot in first.errors[Constants.Netted]])
        self.second.placement[Constants.Netted] = Counter([shot.placement for shot in first.errors[Constants.Netted]])

    def calc_placement(self):
        service_locations = {'Near Deuce': {'court': Constants.NearCourt, 'x': [120, 180],
                                            'placements': {Constants.Wide: [45, 65], Constants.Body: [65, 78], Constants.T: [78, 90], 'O': [90, 180]}},
                             'Near Ad': {'court': Constants.NearCourt, 'x': [60, 120],
                                         'placements': {Constants.Wide: [115, 135], Constants.Body: [102, 115], Constants.T: [90, 102], 'O': [45, 90]}},
                             'Far Deuce': {'court': Constants.FarCourt, 'x': [60, 120],
                                           'placements': {Constants.Wide: [115, 135], Constants.Body: [102, 115], Constants.T: [90, 102], 'O': [45, 90]}},
                             'Far Ad': {'court': Constants.FarCourt, 'x': [120, 180],
                                        'placements': {Constants.Wide: [45, 65], Constants.Body: [65, 78], Constants.T: [78, 90], 'O': [90, 180]}}}
        for shot in self.shots:
            for key in service_locations.keys():
                location = service_locations[key]
                if location['court'] == shot.path.impact.court and location['x'][0] < shot.path.impact.x < location['x'][1]:
                    for place in location['placements'].keys():
                        coordinates = location['placements'][place]
                        if coordinates[0] < abs(shot.path.angle) <= coordinates[1]:
                            shot.placement = place

    def __repr__(self):
        return repr((self.shots))


class Return:

    def __init__(self, first, second):
        [self.first, self.second] = [first, second]
        fl = lambda somelist: [item for innerlist in somelist for item in innerlist]
        self.shots = self.first.shots + self.second.shots
        self.number = len(self.shots)
        self.winners = {k: fl([getattr(e, 'winners').get(k, 0) for e in [first, second]]) for k in Constants.WinningReturnOutcomes + [Constants.All]}
        self.winners[Constants.WinningShots] = fl([self.winners[outcome] for outcome in Constants.Winners])
        self.winners[Constants.ForcingShots] = fl([self.winners[outcome] for outcome in Constants.ForcingErrors if outcome in self.winners.keys()])
        self.errors = {k: fl([getattr(e, 'errors').get(k, 0) for e in [first, second]]) for k in Constants.Errors + [Constants.All]}
        self.error_number = len(self.errors[Constants.All])
        self.shots_in = {k: fl([getattr(e, 'shots_in').get(k, 0) for e in [first, second]]) for k in Constants.InPlayOutcomes + [Constants.All]}
        self.double_faults = self.second.all_errors

    def __repr__(self):
        return repr((self.shots))


class KeyShot:

    def __init__(self, drives, slices, volleys, overheads, lobs, drop_shots, other):
        [self.drives, self.slices, self.volleys, self.overheads, self.lobs, self.drop_shots,
         self.other] = [drives, slices, volleys, overheads, lobs, drop_shots, other]
        fl = lambda somelist: [item for innerlist in somelist for item in innerlist]
        self.shots = drives.shots + slices.shots + volleys.shots + overheads.shots + lobs.shots + drop_shots.shots + other.shots
        self.number = len(self.shots)
        self.winners = {k: fl([getattr(e, 'winners').get(k, 0) for e in [drives, slices, volleys, overheads, lobs, drop_shots, other]])
                        for k in Constants.WinningOutcomes + [Constants.All]}
        self.winners[Constants.WinningShots] = fl([self.winners[outcome] for outcome in Constants.Winners])
        self.winners[Constants.ForcingShots] = fl([self.winners[outcome] for outcome in Constants.ForcingErrors if outcome in self.winners.keys()])
        self.errors = {k: fl([getattr(e, 'errors').get(k, 0) for e in [drives, slices, volleys, overheads, lobs, drop_shots, other]])
                       for k in Constants.Errors + [Constants.All]}
        self.shots_in = {k: fl([getattr(e, 'shots_in').get(k, 0) for e in [drives, slices, volleys, overheads, lobs, drop_shots, other]])
                         for k in Constants.InPlayOutcomes + [Constants.All]}

    def __repr__(self):
        return repr((self.shots))


class StrokeType:

    def __init__(self, stroke, stroke_type, all_player_shots):
        [self.winners, self.errors, self.shots_in, self.placement] = [{}, {}, {}, {}]
        fl = lambda somelist: [item for innerlist in somelist for item in innerlist]
        self.shots = [shot for shot in all_player_shots if shot.stroke == stroke and shot.stroke_type == stroke_type]
        self.number = len(self.shots)
        self.all_errors = [shot for shot in self.shots if shot.result in Constants.Errors]
        self.error_number = len(self.all_errors)
        self.all_winners = [shot for shot in self.shots if shot.result in Constants.WinningOutcomes]
        self.all_shots_in = [shot for shot in self.shots if shot.result in Constants.InPlayOutcomes]
        self.lets = [shot for shot in self.shots if shot.result == Constants.Let]
        self.percentage = (None if not (len(self.shots) - len(self.lets)) else
                           round(float((len(self.all_shots_in) + len(self.all_winners)) * 100)
                                 / (len(self.shots) - len(self.lets))))
        self.percentage_winners = (None if not (len(self.shots) - len(self.lets)) else
                                   round(float((len(self.all_winners) * 100)
                                         / (len(self.shots) - len(self.lets)))))
        for outcome in Constants.WinningOutcomes:
            self.winners[outcome] = [shot for shot in self.all_winners if shot.result == outcome]
        self.winners[Constants.All] = fl(self.winners.values())
        for outcome in Constants.Errors:
            self.errors[outcome] = [shot for shot in self.all_errors if shot.result == outcome]
        self.errors[Constants.All] = fl(self.errors.values())
        for outcome in Constants.InPlayOutcomes:
            self.shots_in[outcome] = [shot for shot in self.all_shots_in if shot.result == outcome]
        self.shots_in[Constants.All] = fl(self.shots_in.values())

    def __repr__(self):
        return repr((self.shots))


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
         [number_of_sets, match_games, format_description, advantage, lets] = data[1:6]
      elif data[0] == Constants.StartTime:
         start_time = finish_time = data[1]
      elif data[0] == Constants.Server:
         first_server = data[1]
      elif data[0] == Constants.PlayerEnds:
         player_ends = data[1]
      elif data[0] == Constants.Match:
         winner = data[1]
         finish_time = data[2]
      elif data[0] == Constants.Shot:
         if len(data) == 11:
            [r_misc, s_time] = data[9:11]
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


def process(filename):
   match = parse(filename)
   match.display_stats(grouping='Basic')
   match.display_stats(grouping='Unforced Errors', width=30)
   match.display_stats(grouping='Placement', width=50)

# p1s = match.side_one_stats.match_stats
# p2s = match.side_two_stats.match_stats
