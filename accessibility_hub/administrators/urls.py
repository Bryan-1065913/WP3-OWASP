from django.urls import path
from . import views

app_name = 'administrators'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('get_deskundige_in_behandeling_ajax/', views.get_deskundige_in_behandeling_ajax, name='get_deskundige_in_behandeling_ajax'),
    path('get_alle_deskundige_ajax/', views.get_alle_deskundige_ajax, name='get_alle_deskundige_ajax'),
    path('portal/', views.portal, name='portal'),
    path('goedkeuren_deskundige/<int:deskundige_id>/', views.goedkeuren_deskundige, name='goedkeuren_deskundige'),
    path('afkeuren_deskundige/<int:deskundige_id>/', views.afkeuren_deskundige, name='afkeuren_deskundige'),
    path('ervaringsdeskundige/<int:deskundige_id>/', views.ervaringsdeskundige, name='ervaringsdeskundige'),
    path('medewerker/<int:medewerker_id>/', views.medewerker, name='medewerker'),
    path('verwijder_medewerker/<int:medewerker_id>/', views.verwijder_medewerker, name='verwijder_medewerker'),
    path('organisatie/<int:id>/', views.organisatie, name='organisatie'),
    path('verwijder_organisatie/<int:id>/', views.verwijder_organisatie, name='verwijder_organisatie'),
    path('accepteer_organisatie/<int:id>/', views.accepteer_organisatie, name='accepteer_organisatie'),
    path('updates_organisatie/', views.check_updates_organisaties, name='updates_organisatie'),
    path('mail/', views.mail, name='mail'),
    path('onderzoek/<int:onderzoek_id>/', views.onderzoek, name='onderzoek'),
    path('verwijder_onderzoek/<int:onderzoek_id>/', views.verwijder_onderzoek, name='verwijder_onderzoek'),
    path('accepteer_onderzoek/<int:onderzoek_id>/', views.accepteer_onderzoek, name='accepteer_onderzoek'),
    path('updates_onderzoek/', views.check_updates_onderzoek, name='updates_onderzoek'),
]
