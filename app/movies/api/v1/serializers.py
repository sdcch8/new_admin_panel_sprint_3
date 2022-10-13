from rest_framework import serializers

from movies.models import Filmwork, Genre, PersonFilmwork


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', )

    def to_representation(self, obj):
        return obj.name


class PersonsSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return obj['person__full_name']


class FilmworkSerializer(serializers.ModelSerializer):
    genres = GenresSerializer(many=True, read_only=True)
    actors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'title', 'description', 'creation_date', 'rating',
                  'type', 'genres', 'actors', 'writers', 'directors')
        model = Filmwork

    def get_persons(self, obj, role):
        return PersonFilmwork.objects.select_related('person').filter(
            film_work=obj, role=role).values('person__full_name')

    def get_actors(self, obj):
        serializer = PersonsSerializer(
            instance=self.get_persons(obj, 'actor'), many=True)
        return serializer.data

    def get_writers(self, obj):
        serializer = PersonsSerializer(
            instance=self.get_persons(obj, 'writer'), many=True)
        return serializer.data

    def get_directors(self, obj):
        serializer = PersonsSerializer(
            instance=self.get_persons(obj, 'director'), many=True)
        return serializer.data
