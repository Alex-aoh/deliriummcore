from django.urls import path, include
from . import views
from rest_framework import routers


app_name = "api"

router = routers.DefaultRouter()
router.register(r'ticket', views.TicketViewSet)
router.register(r'ticketrequest', views.TicketRequestViewSet)
router.register(r'eventaccount', views.EventAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
