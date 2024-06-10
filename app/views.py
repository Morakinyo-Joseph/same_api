from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from .models import Coach, Player, Team, Match, Event
from .serializers import PlayerSerializer, TeamSerializer, MatchSerializer, CoachSerializer
from rest_framework.decorators import api_view
import datetime
from django.shortcuts import get_object_or_404


@api_view(["GET"])
def home(request):
    return Response({"code": HTTP_200_OK, "message": "Chance-cup api version1"})


""" Coach """

@api_view(["POST"])
def coach_create(request):
    serializer = CoachSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        coaches = Coach.objects.filter(name=request.data["name"])
        if coaches.exists():
            coach = coaches.first()
            second_serializer = CoachSerializer(instance=coach)
            return Response({"code": HTTP_200_OK, "message": "Coach created successfully.", "data": second_serializer.data})
        else:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": "No coach found with the given name."})


        # return Response({"code": HTTP_200_OK, "message": "Coach created successfully.", "data": second_serializer.data})
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": serializer.errors})
    
def coach_delete(request, id):
    if Coach.objects.filter(id=id).exists():
        coach = Coach.objects.get(id=id)
        coach.delete()
        return Response({"code": HTTP_200_OK, "message": "Coach deleted successfully."})
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Coach not found."})


""" Player """

@api_view(["POST"])
def player_create(request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        players = Player.objects.filter(name=request.data["name"])
        if players.exists():
            player = players.first()
            second_serializer = PlayerSerializer(instance=player)
            return Response({"code": HTTP_200_OK, "message": "Player created successfully.", "data": second_serializer.data})
        else:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": serializer.errors})


@api_view(["PUT"])
def player_edit(request, id):

    if Player.objects.filter(id=id).exists():
        player = Player.objects.get(id=id)
        serializer = PlayerSerializer(instance=player, data=request.data, partial=True)
        if serializer.is_Valid():
            serializer.save()
        else:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": serializer.errors}) 
    else:
        return Response({"code": HTTP_404_NOT_FOUND, "message": "Player does not exists."})


@api_view(["DELETE"])
def player_delete(request, id):

    if Player.objects.filter(id=id).exists():
        player = Player.objects.get(id=id)
        player.delete()
        return Response({"code": HTTP_200_OK, "message": "Player deleted successfully."})
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Player does not exists."})


@api_view(["GET"])
def player_view(request):   
    players = Player.objects.all()

    event = request.GET.get('event')
    team = request.GET.get('team')

    if event not in ['goal', 'assist']:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Invalid event type", "data": {}})

    if event == "goal":
        goals = list(Event.objects.filter(name='goals').values_list('event__goaler', flat=True))

        def get_all_elements(goal):
            player_names = {}

            for item in goal:
                # get player name
                player = get_object_or_404(Player, id=item)
                team = Team.objects.get(id=player.team_id.id)

                player_info = {}
                player_info["team"] = team.fullname
                player_info["goal"] = goal.count(item)
                player_names[player.name] = player_info
            return player_names

        all_goals = get_all_elements(goal=goals)
        return Response({"code": HTTP_200_OK, "message": "Found all Players", "data": all_goals})

    
    if event == "assist":
        assists = list(Event.objects.filter(name='goals').values_list('event__assist', flat=True))
        
        def get_all_elements(assist):
            player_names = {}

            for item in assist:
                # get player name
                try:
                    player = get_object_or_404(Player, id=item)
                    team = Team.objects.get(id=player.team_id.id)
                except Exception:
                    continue  

                player_info = {}
                player_info["team"] = team.fullname
                player_info["assist"] = assist.count(item)
                player_names[player.name] = player_info
            
            return player_names
                
        all_assists = get_all_elements(assist=assists)
        return Response({"code": HTTP_200_OK, "message": "Found all Players", "data": all_assists})


    if team:
        team_instance = get_object_or_404(Team, id=team)
        players = Player.objects.filter(team_id=team_instance.id)
        serializer = PlayerSerializer()

    
    serializer = PlayerSerializer(instance=players, many=True)

    # data_length = len(serializer.data)

    # for player in range(0, data_length):
    #     # get team name
    #     player_id = serializer.data[player]["id"]
    #     team_id = serializer.data[player]["team_id"]

    #     player_team = get_object_or_404(Team, id=team_id)
    #     team_name = player_team.shortname
    #     serializer.data[player]["team_name"] = team_name # append team_name to serailzer

    #     # get player goals
    #     player_goal_count = 0 # counting the amount of goals the player has

    #     matches = Match.objects.all()
    #     for match in matches:
    #         teams = match.teams

    #         def remove_hyphens(input_str):
    #             return input_str.replace("-", "")

    #         player_team_id = remove_hyphens(str(player_team.id))
    #         player_id = remove_hyphens(str(player_id))

    #         if player_team_id not in teams:
    #             pass
    #         else:
    #             events = Event.objects.filter(match_id=match.id).values() # getting all events for each match

    #             for event in events:
    #                 if event["name"] == "goals":
    #                     if event["event"]["goaler"] == player_id:
    #                         player_goal_count += 1


    #     serializer.data[player]["goal"] = player_goal_count

    

    return Response({"code": HTTP_200_OK, "message": "Found all Players", "data": serializer.data})



""" Team """

@api_view(["POST"])
def team_create(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        teams = Team.objects.filter(fullname=request.data["fullname"])
        if teams.exists():
            team = teams.first()
            second_serializer = TeamSerializer(instance=team)
            return Response({"code": HTTP_200_OK, "message": "Team created successfully.", "data": second_serializer.data})
        else:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": serializer.errors})


@api_view(["PUT"])
def team_edit(request, id):

    if Team.objects.filter(id=id).exists():
        team = Team.objects.get(id=id)
        serializer = TeamSerializer(instance=team, data=request.data, partial=True)
        if serializer.is_Valid():
            serializer.save()
        else:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": serializer.errors}) 
    else:
        return Response({"code": HTTP_404_NOT_FOUND, "message": "Team does not exists."})


@api_view(["DELETE"])
def team_delete(request, id):

    if Team.objects.filter(id=id).exists():
        team = Team.objects.get(id=id)
        team.delete()
        return Response({"code": HTTP_200_OK, "message": "Team deleted successfully."})
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Team does not exists."})


@api_view(["GET"])
def team_view(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    
    length = len(serializer.data)
    for team in range(0, length):
        team_id = str(serializer.data[team]["id"])
        team_name = serializer.data[team]['fullname']

        coach_name = get_object_or_404(Coach, id=serializer.data[team]['coach_id'])
        serializer.data[team]["coach"] = coach_name.name
        serializer.data[team].pop('coach_id') # remove the key 'coach_id' from the serializer.data
        
        # stats
        matches_play_count = 0
        win_count = 0
        loss_count = 0
        draw_count = 0
        goal_forward = 0
        goal_against = 0
        goal_diff = 0
        points = 0

        matches = Match.objects.all()
        for match in matches:
            if match.completed:
                teams = match.teams
                
                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_id = remove_hyphens(str(team_id))
                if team_id not in teams:
                    pass
                else:
                    if Event.objects.filter(match_id=match.id).exists():
                        matches_play_count += 1

                    events = Event.objects.filter(match_id=match.id).values() # getting all events for each match

                    team_win = 0
                    team_loss = 0

                    for event in events:
                        if event["name"] == "goals":
                            if event["event"]["goal_team"] == team_id:
                                team_win += 1
                                goal_forward += 1
                            else:  # this means the team lost
                                team_loss += 1
                                goal_against += 1

                    if team_win > team_loss:
                        win_count += 1
                        points += 3
                    elif team_win < team_loss:
                        loss_count += 1
                    elif team_win == team_loss:
                        draw_count += 1
                        points += 1

        if goal_against != 0:
            goal_diff = goal_forward - goal_against

        players = Player.objects.filter(team_id=team_id).values()
        forwards = []
        midfielders = []
        defenders = []
        goalkeepers = []

        for player in players:
            if player["position"] == "forward":
               forwards.append(player["name"])
            elif player["position"] == "midfielder":
                midfielders.append(player["name"])
            elif player["position"] == 'defender':
                defenders.append(player["name"])
            elif player["position"] == "keeper":
                goalkeepers.append(player["name"])


        serializer.data[team]["players"] = {}
        serializer.data[team]["players"]["forwards"] = forwards
        serializer.data[team]["players"]["midfielders"] = midfielders
        serializer.data[team]["players"]["defender"] = defenders
        serializer.data[team]["players"]["goalkeepers"] = goalkeepers

        serializer.data[team]["match_played"] = matches_play_count
        serializer.data[team]["win"] = win_count
        serializer.data[team]["loss"] = loss_count
        serializer.data[team]["draw"] = draw_count

        serializer.data[team]["goal_forward"] = goal_forward
        serializer.data[team]["goal_against"] = goal_against
        serializer.data[team]["goal_diff"] = goal_diff
        serializer.data[team]["point"] = points

    return Response({"code": HTTP_200_OK, "message": "Found all Teams", "data": serializer.data})


@api_view(["GET"])
def team_detail(request, id):
    if Team.objects.filter(id=id).exists():
        team = Team.objects.get(id=id)

        serializer = TeamSerializer(instance=team)
        players = Player.objects.filter(team_id=team)
        serializer.data["players"] = players

        return Response({"code": HTTP_200_OK, "message": "Found Team", "data": serializer.data})

    else:
        return Response({"code": HTTP_404_NOT_FOUND, "message": "Team not found."})


""" Match """

@api_view(["POST"])
def match_create(request):
    sports = ["football", "basketball", "volleyball", "fiveaside"]

    try:
        request.data["type"]
        request.data["teams"]
        request.data["date"]
        request.data["time"]
        request.data["venue"]
    except KeyError:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Key error noticed for missing or invalid key in data."})
    
    valid = False

    sport_type = request.data["type"]

    for sport in sports:
        if sport.lower() == sport_type:
            valid = True
            break

    if not valid:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Invalid sport in type."})
    
    teams = request.data.get("teams", [])

    if len(teams) != 2:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Number of allowed teams exceeded."})

    for index, team in enumerate(teams):
        if not Team.objects.filter(id=team).exists():
            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id at position [{index}] not found."})

    team_a = teams[0]   
    team_b = teams[1]

    if Team.objects.filter(id=team_a).exists():
        team_a = Team.objects.get(id=team_a)
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "First team not Found."})
    
    if Team.objects.filter(id=team_b).exists():
        team_b = Team.objects.get(id=team_b)
        if team_a == team_b:
            return Response({"code": HTTP_400_BAD_REQUEST, "message": "Both teams can't be thesame."})
    else:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Second team not Found."})


    try:
        request.data["date"] = datetime.date.fromisoformat(request.data.get("date"))
    except Exception as e:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Invalid date format. YYYY-MM-DD."})
    
    try:
        request.data["time"] = datetime.time.fromisoformat(request.data.get("time"))
    except Exception as e:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Invalid time format. HH-MM-SS"})

    serializer = MatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"code": HTTP_200_OK, "message": "Match created successfully"})
    else:
        return Response({"code": HTTP_200_OK, "message": serializer.errors})



@api_view(["PUT"])
def match_update(request, id):
    try:
        match_instance = Match.objects.get(id=id)
    except Match.DoesNotExist:
        return Response({"code": HTTP_400_BAD_REQUEST, "message": "Match not found."}, status=404)

    sport_types = {
        "football": ["goals", "offsides", "corners", "shots", "cards", "passes", "fouls"],
        "basketball": [],
        "volleyball": [],  
        "fiveaside": []   
    }

    event_data = request.data["event"]

    if match_instance.type == "football":

        for item in sport_types["football"]:

            if item in event_data:

                if item == "goals":

                    # count = 0
                    
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_goal_params = ['goal_team', 'goaler', 'assist', 'minute', 'conceded_team', 'keeper', 'time']

                        # confirm if the goal request data has the expected fields in goal_params
                        for goal_param in expected_goal_params:
                            if goal_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{goal_param}' field is missing in goals '{event_data_id}'."})

                        goal_team = event_data_item['goal_team']
                        goaler = event_data_item['goaler']
                        assist = event_data_item['assist']
                        minute = event_data_item['minute']
                        conceded_team = event_data_item['conceded_team']
                        keeper = event_data_item['keeper']
                        time = event_data_item['time']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=goal_team).exists():
                                goal_team = Team.objects.get(id=goal_team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                goal_team_id = remove_hyphens(str(goal_team.id))

                                if goal_team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goal team not playing in this match. Check goals '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check goals '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{goal_team}' in goals '{event_data_id}'."})
                        
                        # confirm if goaler exists and belongs to team
                        try:
                            if Player.objects.filter(id=goaler).exists():
                                goaler = Player.objects.get(id=goaler)
                                if goaler.team_id != goal_team:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goaler does not belong to team in goals '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goaler player id not found. Check goals '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid goaler player ID '{goaler}' in goals '{event_data_id}'."})
                        
                        # confirm if assist exists and belongs to team
                        if assist == None:
                            pass
                        else:
                            try:
                                if Player.objects.filter(id=assist).exists():
                                    assist = Player.objects.get(id=assist)
                                    if assist.team_id != goal_team:
                                        return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Assist does not belong to team in goals '{event_data_id}'."})
                                else:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Assist player id not found. Check goals '{event_data_id}'."})
                            except ValueError:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid assist player ID '{assist}' in goals '{event_data_id}'."})
                            
                        # confirm if the minute is within expected range
                        if minute == None:
                            pass
                        else:
                            try:
                                if int(minute) not in range(0, 70):
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Minute not in the expected range of 0 - 70 in goals '{event_data_id}'."})
                            except ValueError as e:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Minute not in expected range of 0 - 70 in goals '{event_data_id}'."})
                            
                        # confirm if conceded team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=conceded_team).exists():
                                conceded_team = Team.objects.get(id=conceded_team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                conceded_team_id = remove_hyphens(str(conceded_team.id))

                                if conceded_team_id not in match_instance.teams: 
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Conceded team not playing in this match. Check goals '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Conceded team id not found. Check goals '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid conceded team ID '{conceded_team}'.  goals '{event_data_id}'."}) 

                        # confirm if keeper exists and belongs to conceded team
                        if keeper == None: # putting this logic here just incase the keeper was not given in the request.
                            pass
                        else:
                            try:
                                if Player.objects.filter(id=keeper).exists():
                                    keeper = Player.objects.get(id=keeper)

                                    if keeper.team_id != conceded_team: 
                                        return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Keeper not in conceded team playing in this match. Check goals '{event_data_id}'."})
                                else:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Keeper player id not. Check goals '{event_data_id}'."})
                            except ValueError:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid keeper player ID '{keeper}' in goals '{event_data_id}'."})   
                        
                        # verify and convert time to isoformat
                        if time == None: # incase the time was none
                            pass
                        else:
                            try:
                                time = datetime.time.fromisoformat(time)
                            except Exception as e:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid time format. Use HH:MM:SS. Check goals '{event_data_id}'"})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()

                        # count += 1
                    # return Response({"code": HTTP_200_OK, "message": "Match goal(s) updated sucessfully."})
                        

                elif item == "offsides":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_offside_params = ['team', 'amount']

                        for offside_param in expected_offside_params:
                            if offside_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{offside_param}' field is missing in offside '{event_data_id}'."})


                        team = event_data_item['team']
                        # player = event_data_item['player']
                        amount = event_data_item['amount']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check offsides '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check offsides '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in offsides '{event_data_id}'."})
                        
                        # confirm if player exists and belongs to team
                        # if player == None:
                        #     pass
                        # else:
                        #     try:
                        #         if Player.objects.filter(id=player).exists():
                        #             player = Player.objects.get(id=player)
                        #             if player.team_id != team:
                        #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team in offsides '{event_data_id}'."})
                        #         else:
                        #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check offsides '{event_data_id}'."})
                        #     except ValueError:
                        #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}' in offsides '{event_data_id}'."})
                        
                        try:
                            int(amount)
                        except ValueError as e:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Total fouls amount '{amount}' must be an integer. Check passes '{event_data_id}'."})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match offside(s) updated sucessfully."})


                elif item == "corners":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_corners_params = ['team', 'amount']

                        for corner_param in expected_corners_params:
                            if corner_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{corner_param}' field is missing in corner '{event_data_id}'."})


                        team = event_data_item['team']
                        amount = event_data_item['amount']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))
                                

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check corners '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check corners '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in corners '{event_data_id}'."})
                        
                        # confirm if player exists and belongs to team
                        # try:
                        #     if Player.objects.filter(id=player).exists():
                        #         player = Player.objects.get(id=player)
                        #         if player.team_id != team:
                        #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team in corners '{event_data_id}'."})
                        #     else:
                        #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check corners '{event_data_id}'."})
                        # except ValueError:
                        #     return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}' in corners '{event_data_id}'."})
                        
                        try:
                            int(amount)
                        except ValueError as e:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Total fouls amount '{amount}' must be an integer. Check passes '{event_data_id}'."})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match corner(s) updated sucessfully."})


                elif item == "shots":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_shots_params = ['team', 'player', 'on_target']

                        for shots_param in expected_shots_params:
                            if shots_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{shots_param}' field is missing in shot '{event_data_id}'."})


                        team = event_data_item['team']
                        player = event_data_item['player']
                        # amount = event_data_item['amount']
                        on_target = event_data_item['on_target']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check shots '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check shots '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in shots '{event_data_id}'."})
                        
                        # confirm if player exists and belongs to team
                        if player == None:
                            pass
                        else:
                            try:
                                if Player.objects.filter(id=player).exists():
                                    player = Player.objects.get(id=player)
                                    if player.team_id != team:
                                        return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team in shots '{event_data_id}'."})
                                else:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check shots '{event_data_id}'."})
                            except ValueError:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}' in shots '{event_data_id}'."})
                        
                        if type(on_target) != bool:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"On target '{on_target}' is not a valid boolean value. Check shots '{event_data_id}'."})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match shot(s) updated sucessfully."})


                elif item == "cards":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_cards_params = ['team', 'card_type', 'player']

                        for cards_param in expected_cards_params:
                            if cards_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{cards_param}' field is missing in shot '{event_data_id}'."})


                        team = event_data_item['team']
                        card_type = event_data_item['card_type']

                        # print("card type", card_type, type(card_type))

                        player = event_data_item['player']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check cards '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check cards '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in cards '{event_data_id}'."})
                        
                        # confirm if player exists and belongs to team
                        if player == None:
                            pass
                        else:
                            try:
                                if Player.objects.filter(id=player).exists():
                                    player = Player.objects.get(id=player)
                                    if player.team_id != team:
                                        return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team in cards '{event_data_id}'."})
                                else:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check cards '{event_data_id}'."})
                            except ValueError:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}' in cards '{event_data_id}'."})
                        
                        if card_type not in ["yellow", "red"]:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Card Type '{card_type}' is not a valid. Must be yellow or red. Check cards '{event_data_id}'."})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match card(s) updated sucessfully."})
                

                elif item == "passes":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_passes_params = ['team', "total_pass"]

                        for passes_param in expected_passes_params:
                            if passes_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{passes_param}' field is missing in passes '{event_data_id}'."})


                        team = event_data_item['team']
                        total_pass = event_data_item['total_pass']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check passes '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check passes '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in passes '{event_data_id}'."})
                        

                        try:
                            int(total_pass)
                        except ValueError as e:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Total pass value '{total_pass}' must be an integer. Check passes '{event_data_id}'."})

                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match pass(s) updated sucessfully."})
                

                elif item == "fouls":
                    for event_data_id, event_data_item in enumerate(event_data[item]):
                        expected_fouls_params = ['team', "amount"]

                        for fouls_param in expected_fouls_params:
                            if fouls_param not in event_data_item:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{fouls_param}' field is missing in fouls '{event_data_id}'."})


                        team = event_data_item['team']
                        # player = event_data_item['player']
                        amount = event_data_item['amount']

                        # confirm if team exists and belongs to match instance
                        try:
                            if Team.objects.filter(id=team).exists():
                                team = Team.objects.get(id=team)

                                def remove_hyphens(input_str):
                                    return input_str.replace("-", "")

                                team_id = remove_hyphens(str(team.id))

                                if team_id not in match_instance.teams:
                                    return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check fouls '{event_data_id}'."})
                            else:
                                return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check fouls '{event_data_id}'."})
                        except ValueError:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}'. Check fouls '{event_data_id}'."})
                        

                        try:
                            int(amount)
                        except ValueError as e:
                            return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Total fouls amount '{amount}' must be an integer. Check passes '{event_data_id}'."})


                        # # confirm if player exists and belongs to team
                        # try:
                        #     if Player.objects.filter(id=player).exists():
                        #         player = Player.objects.get(id=player)
                        #         if player.team_id != team:
                        #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team. Check fouls '{event_data_id}'."})
                        #     else:
                        #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check fouls '{event_data_id}'."})
                        # except ValueError:
                        #     return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}'. Check fouls '{event_data_id}'."})
                        
                        new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                        new_match_event.save()
                        
                    # return Response({"code": HTTP_200_OK, "message": "Match foul(s) updated sucessfully."})
                
            
            else:
                # return Response({"code": HTTP_400_BAD_REQUEST, "message": "No allowed events were given"})
                pass
        return Response({"code": HTTP_200_OK, "message": "Match event uploaded successfully"})



@api_view(["GET"])
def match_view(request):
    matches = Match.objects.all()
    serializer = MatchSerializer(instance=matches, many=True)

    data_length = len(serializer.data)
    for match in range(0, data_length):

        match_instance = serializer.data[match]

        team_a = match_instance["teams"][0]
        team_b = match_instance["teams"][1]

        team_a_instance = get_object_or_404(Team, id=team_a)
        team_b_instance = get_object_or_404(Team, id=team_b)

        if match_instance["completed"] == True:
            team_a_goals = 0
            team_b_goals = 0

            events = Event.objects.filter(match_id=match_instance["id"]).values()
            for event in events:
                if event["name"] == "goals":

                    def remove_hyphens(input_str):
                        return input_str.replace("-", "")

                    team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                    team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                    if event["event"]["goal_team"] == team_a_instance_id:
                        team_a_goals += 1
                    elif event["event"]["goal_team"] == team_b_instance_id:
                        team_b_goals += 1
            
        else:
            team_a_goals = "-"
            team_b_goals = "-"

        match_instance.pop('teams')
        match_instance["home"] = team_a_instance.shortname
        match_instance["away"] = team_b_instance.shortname
        match_instance["home_score"] = team_a_goals
        match_instance["away_score"] = team_b_goals

        # print(f"{team_a_instance.shortname}: ", team_a_goals, "\n",
        #         f"{team_b_instance.shortname}: ", team_b_goals, "\n--------------\n\n")

    return Response({"code": HTTP_200_OK, 'message': "Found all matches", "data": serializer.data})



@api_view(["DELETE"])
def match_delete(request):  
    return None


@api_view(["GET"])
def match_detail(request, id):
    if not Match.objects.filter(id=id).exists():
        return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Match with ID '{id}' not found."})

    match_instance = Match.objects.get(id=id)
    serializer = MatchSerializer(instance=match_instance)

    team_a = serializer.data["teams"][0]
    team_b = serializer.data["teams"][1]

    team_a_instance = get_object_or_404(Team, id=team_a)
    team_b_instance = get_object_or_404(Team, id=team_b)

    # stats
    team_a_goals = 0
    team_b_goals = 0

    team_a_goal_scorers = []
    team_b_goal_scorers = []

    team_a_offsides = None
    team_b_offsides = None

    team_a_corners = None
    team_b_corners = None

    ''' shots / on target'''
    # the introduction of flag is meant to change the datatype of the shots from none to int
    global team_a_shots_flag
    team_a_shots_flag = False

    global team_b_shots_flag
    team_b_shots_flag = False

    team_a_shots = None
    team_b_shots = None
    
    team_a_shots_on_target = None
    team_b_shots_on_target = None
    ''''''

    team_a_passes = None
    team_b_passes = None

    team_a_fouls = None
    team_b_fouls = None


    """ yellow / red cards"""
    global team_a_cards
    team_a_cards = False

    global team_b_cards
    team_b_cards = False

    team_a_yellow_cards = None
    team_a_red_cards = None

    team_b_yellow_cards = None
    team_b_red_cards = None
    ''''''

    if serializer.data["completed"] == True:

        events = Event.objects.filter(match_id=serializer.data["id"]).values()
        for event in events:

            if event["name"] == "goals":
                
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["goal_team"] == team_a_instance_id:
                    team_a_goals += 1

                    goaler = event["goaler"] # trying to get the goaler for each goal and append them to the 
                    goaler = get_object_or_404(Player, id=goaler)

                    team_a_goal_scorers.append({"name": goaler.name, "minute": event["minute"]})

                elif event["goal_team"] == team_b_instance_id:
                    team_b_goals += 1

                    goaler = event["goaler"]
                    goaler = get_object_or_404(Player, id=goaler)

                    team_b_goal_scorers.append({"name": goaler.name, "minute": event["minute"]})
            
            
            elif event["name"] == "offsides":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:
                    team_a_offsides = event["amount"]
                elif event["team"] == team_b_instance_id:
                    team_b_offsides = event["amount"]


            elif event["name"] == "corners":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:
                    team_a_corners = event["amount"]
                elif event["team"] == team_b_instance_id:
                    team_b_corners = event["amount"]


            elif event["name"] == "shots":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:

                    if team_a_shots_flag  == False:   
                        team_a_shots = 0
                        team_a_shots_on_target = 0
                        team_a_shots_flag = True

                    team_a_shots += 1
                    if event["on_target"] == True:
                        team_a_shots_on_target += 1

                elif event["team"] == team_b_instance_id:
                    
                    if team_b_shots_flag == False:
                        team_b_shots = 0
                        team_b_shots_on_target = 0
                        team_b_shots_flag = True

                    team_b_shots += 1
                    if event["on_target"] == True:
                        team_b_shots_on_target += 1

            
            elif event["name"] == "passes":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:
                    team_a_passes = event["total_pass"]
                    
                elif event["team"] == team_b_instance_id:
                    team_b_passes = event["total_pass"]


            elif event["name"] == "fouls":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:
                    team_a_fouls = event["amount"]
                    
                elif event["team"] == team_b_instance_id:
                    team_b_fouls = event["amount"]


            elif event["name"] == "cards":
                event = event["event"]

                def remove_hyphens(input_str):
                    return input_str.replace("-", "")

                team_a_instance_id = remove_hyphens(str(team_a_instance.id))
                team_b_instance_id = remove_hyphens(str(team_b_instance.id))

                if event["team"] == team_a_instance_id:
                    if team_a_cards  == False:   
                        team_a_yellow_cards = 0
                        team_a_red_cards = 0
                        team_a_cards = True

                    if event["card_type"] == "yellow":
                        team_a_yellow_cards += 1
                    elif event["card_type"] == "red":
                        team_a_red_cards += 1

                    
                elif event["team"] == team_b_instance_id:
                    if team_b_cards  == False:   
                        team_b_yellow_cards = 0
                        team_b_red_cards = 0
                        team_b_cards = True

                    if event["card_type"] == "yellow":
                        team_b_yellow_cards += 1
                    elif event["card_type"] == "red":
                        team_b_red_cards += 1
    else:
        team_a_goals = "-"
        team_b_goals = "-"

    data = serializer.data.copy()
    data.pop('teams')
    data["home"] = team_a_instance.shortname
    data["away"] = team_b_instance.shortname
    data["home_score"] = team_a_goals
    data["away_score"] = team_b_goals
    data["home_goal_scorers"] = team_a_goal_scorers
    data["away_goal_scorers"] = team_b_goal_scorers
    data["home_offsides"] = team_a_offsides
    data["away_offsides"] = team_b_offsides
    data["away_shots"] = team_a_shots
    data["home_shots"] = team_b_shots
    data["away_shots_on_target"] = team_a_shots_on_target
    data["home_shots_on_target"] = team_b_shots_on_target

    data["home_passes"] = team_a_passes
    data["away_passes"] = team_b_passes

    data["home_fouls"] = team_a_fouls
    data["away_fouls"] = team_b_fouls

    data["home_yellow_cards"] = team_a_yellow_cards
    data["home_red_cards"] = team_a_red_cards

    data["away_yellow_cards"] = team_b_yellow_cards
    data["away_red_cards"] = team_b_red_cards

    return Response({"code": HTTP_200_OK, "message": "Found Match", "data": data})




# if event == "offsides":
#                     pass
#                 if event == "corners":
#                     pass
#                 if event == "freekicks":
#                     pass
#                 if event == "shots":
#                     pass
#                 if event == "shots_on_target":
#                     pass
#                 if event == "yellow_cards":
#                     pass
#                 if event == "red_cards":
#                     pass
#                 if event == "ball_possessions":
#                     pass
#                 if event == "passes":
#                     pass
#                 if event == "pass_accuracy":
#                     pass
#                 if event == "fouls":
#                     pass




                    # for event_data_id, event_data_item in enumerate(event_data[event]):
                    #     expected_goal_params = ['goal_team', 'goaler', 'assist', 'minute', 'conceded_team', 'keeper', 'time']

                    #     # confirm if the goal request data has the expected fields in goal_params
                    #     for goal_param in expected_goal_params:
                    #         if goal_param not in event_data_item:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{goal_param}' field is missing in goals '{event_data_id}'."})


                    #     goal_team = event_data_item['goal_team']
                    #     goaler = event_data_item['goaler']
                    #     assist = event_data_item['assist']
                    #     minute = event_data_item['minute']
                    #     conceded_team = event_data_item['conceded_team']
                    #     keeper = event_data_item['keeper']
                    #     time = event_data_item['time']

                    #     # confirm if team exists and belongs to match instance
                    #     try:
                    #         if Team.objects.filter(id=goal_team).exists():
                    #             goal_team = Team.objects.get(id=goal_team)

                    #             if goal_team.id not in match_instance.teams:
                    #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goal team not playing in this match. Check goals '{event_data_id}'."})
                    #         else:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check goals '{event_data_id}'."})
                    #     except ValueError:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{goal_team}' in goals '{event_data_id}'."})
                        
                    #     # confirm if goaler exists and belongs to team
                    #     try:
                    #         if Player.objects.filter(id=goaler).exists():
                    #             goaler = Player.objects.get(id=goaler)
                    #             if goaler.team_id != goal_team:
                    #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goaler does not belong to team in goals '{event_data_id}'."})
                    #         else:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Goaler player id not found. Check goals '{event_data_id}'."})
                    #     except ValueError:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid goaler player ID '{goaler}' in goals '{event_data_id}'."})
                        
                    #     # confirm if assist exists and belongs to team
                    #     try:
                    #         if Player.objects.filter(id=assist).exists():
                    #             assist = Player.objects.get(id=assist)
                    #             if assist.team_id != goal_team:
                    #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Assist does not belong to team in goals '{event_data_id}'."})
                    #         else:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Assist player id not found. Check goals '{event_data_id}'."})
                    #     except ValueError:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid assist player ID '{assist}' in goals '{event_data_id}'."})
                        
                    #     # confirm if the minute is within expected range
                    #     try:
                    #         if int(minute) not in range(0, 70):
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Minute not in the expected range of 0 - 70 in goals '{event_data_id}'."})
                    #     except ValueError as e:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Minute not in expected range of 0 - 70 in goals '{event_data_id}'."})
                        
                    #     # confirm if conceded team exists and belongs to match instance
                    #     try:
                    #         if Team.objects.filter(id=conceded_team).exists():
                    #             conceded_team = Team.objects.get(id=conceded_team)
                    #             print(match_instance.teams, type(match_instance.teams))

                    #             if conceded_team.id not in match_instance.teams: 
                    #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Conceded team not playing in this match. Check goals '{event_data_id}'."})
                    #         else:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Conceded team id not found. Check goals '{event_data_id}'."})
                    #     except ValueError:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid conceded team ID '{conceded_team}'.  goals '{event_data_id}'."}) 

                    #     # confirm if keeper exists and belongs to conceded team
                    #     try:
                    #         if Player.objects.filter(id=keeper).exists():
                    #             keeper = Player.objects.get(id=keeper)

                    #             if keeper.team_id != conceded_team: 
                    #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Keeper not in conceded team playing in this match. Check goals '{event_data_id}'."})
                    #         else:
                    #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Keeper player id not. Check goals '{event_data_id}'."})
                    #     except ValueError:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid keeper player ID '{keeper}' in goals '{event_data_id}'."})   
                        
                    #     # verify and convert time to isoformat
                    #     try:
                    #         time = datetime.time.fromisoformat(time)
                    #     except Exception as e:
                    #         return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid time format. Use HH:MM:SS. Check goals '{event_data_id}'"})                        #     print(time)








                # elif item == "freekicks":
                #     for event_data_id, event_data_item in enumerate(event_data[item]):
                #         expected_freekicks_params = ['team', 'player']

                #         for freekicks_param in expected_freekicks_params:
                #             if freekicks_param not in event_data_item:
                #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"'{freekicks_param}' field is missing in freekick '{event_data_id}'."})


                #         team = event_data_item['team']
                #         player = event_data_item['player']

                #         # confirm if team exists and belongs to match instance
                #         try:
                #             if Team.objects.filter(id=team).exists():
                #                 team = Team.objects.get(id=team)

                #                 if team.id not in match_instance.teams:
                #                     return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team not playing in this match. Check freekicks '{event_data_id}'."})
                #             else:
                #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Team id not found. Check freekicks '{event_data_id}'."})
                #         except ValueError:
                #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid team ID '{team}' in freekicks '{event_data_id}'."})
                        
                #         # confirm if player exists and belongs to team
                #         try:
                #             if Player.objects.filter(id=player).exists():
                #                 player = Player.objects.get(id=player)
                #                 if player.team_id != team:
                #                     return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Player does not belong to team in freekicks '{event_data_id}'."})
                #             else:
                #                 return Response({"code": HTTP_400_BAD_REQUEST, "message": f"player id not found. Check freekicks '{event_data_id}'."})
                #         except ValueError:
                #             return Response({"code": HTTP_400_BAD_REQUEST, "message": f"Invalid player ID '{player}' in freekicks '{event_data_id}'."})
                        
                #         new_match_event = Event.objects.create(match_id=match_instance, name=item, event=event_data_item)
                #         new_match_event.save()
                        
                #     return Response({"code": HTTP_200_OK, "message": "Match freekick(s) updated sucessfully."})