from django.db import models
import uuid


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    team_id = models.ForeignKey("Team", on_delete=models.DO_NOTHING)
    position = models.CharField(max_length=50)
    time_created = models.DateTimeField(auto_now=True)

class Coach(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    time_created = models.DateTimeField(auto_now=True)


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sport_type = models.CharField(max_length=250)
    fullname = models.CharField(max_length=250)
    shortname = models.CharField(max_length=250)
    coach_id = models.ForeignKey(Coach, on_delete=models.DO_NOTHING)
    group = models.CharField(max_length=3)
    time_created = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.fullname


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=250)
    teams = models.JSONField() # [team_id, team_id]
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now=True)
    

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    event = models.JSONField()


