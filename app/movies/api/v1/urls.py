from django.urls import include, path
from rest_framework import routers

from movies.api.v1.views import FilmworkViewSet

v1_router = routers.DefaultRouter()

v1_router.register(
    r'movies',
    FilmworkViewSet,
    basename='movies'
)
urlpatterns = [
    path('', include(v1_router.urls)),
]
