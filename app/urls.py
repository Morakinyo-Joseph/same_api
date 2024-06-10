from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('api/v1', views.home),

    path('api/v1/coach/create', views.coach_create),
    path('api/v1/coach/delete/<str:id>', views.coach_delete),

    path('api/v1/player/create', views.player_create),
    path('api/v1/player/edit/<str:id>', views.player_edit),
    path('api/v1/player/delete/<str:id>', views.player_delete),
    path('api/v1/player/list/', views.player_view),

    path('api/v1/team/create', views.team_create),
    path('api/v1/team/edit/<str:id>', views.team_edit),
    path('api/v1/team/delete/<str:id>', views.team_delete),
    path('api/v1/team/list', views.team_view),
    path('api/v1/team/detail/<str:id>', views.team_detail),

    path('api/v1/match/create', views.match_create),
    path('api/v1/match/update/<str:id>', views.match_update),
    path('api/v1/match/delete', views.match_delete),
    path('api/v1/match/list', views.match_view),
    path('api/v1/match/detail/<str:id>', views.match_detail)
]
