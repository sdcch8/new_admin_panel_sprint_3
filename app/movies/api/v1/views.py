from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import GenericViewSet

from movies.models import Filmwork
from .pagination import Pagination
from .serializers import FilmworkSerializer


class ListRetrieveViewSet(ListAPIView, RetrieveAPIView,
                          GenericViewSet):
    pass


class FilmworkViewSet(ListRetrieveViewSet):
    queryset = Filmwork.objects.all().prefetch_related('genres', 'persons')
    serializer_class = FilmworkSerializer
    pagination_class = Pagination
