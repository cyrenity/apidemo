from django.urls import include, path
from rest_framework import routers
from napi.views import ProcessQueueActionViewSet

router = routers.DefaultRouter()
router.register(r'processqueue', ProcessQueueActionViewSet, 'pq')

urlpatterns = [
    path('', include(router.urls)),
]