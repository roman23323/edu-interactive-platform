from django.urls import path

from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.collection_list, name='collection_list'),

    path(
        'create/',
        views.collection_create,
        name='collection_create',
    ),

    path(
        '<int:collection_id>/',
        views.collection_detail,
        name='collection_detail',
    ),

    path(
        '<int:collection_id>/cards/create/',
        views.card_create,
        name='card_create',
    ),

    path(
        '<int:collection_id>/study/',
        views.study_cards,
        name='study_cards',
    ),
]