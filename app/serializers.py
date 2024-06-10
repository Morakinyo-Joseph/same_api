from rest_framework import serializers
from .models import Player, Team, Match, Coach
from datetime import datetime, timedelta


class JSONArrayOfObjectsField(serializers.Field):
    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Value must be a array of object.")

        for item in data:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item must be a dictionary in the array.")

        return data

    def to_representation(self, value):
        return value



class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"
        read_only_fields = ()

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "name", "team_id", "position",)
        read_only_fields = ()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "sport_type", "fullname", "shortname", "coach_id", "group")
        read_only_fields = ("id", "time_created")

class MatchSerializer(serializers.ModelSerializer):
    # event = JSONArrayOfObjectsField(required=False)
    time_status = serializers.SerializerMethodField()

    def get_time_status(self, obj):
        current_datetime = datetime.now()
        match_datetime = datetime.combine(obj.date, obj.time)
        match_end_datetime = match_datetime + timedelta(minutes=70)
        
        if current_datetime > match_end_datetime:
            return "Ended"
        elif current_datetime >= match_datetime and current_datetime <= match_end_datetime:
            return "Live"
        else:
            return "Upcoming"

    class Meta:
        model = Match
        fields = "__all__"
        read_only_fields = ()