from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(GenreFilmwork)
class GenreFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'genre')
    search_fields = ('film_work', 'genre')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


@admin.register(PersonFilmwork)
class PersonFilmworkAdmin(admin.ModelAdmin):
    list_display = ('film_work', 'person', 'role')
    search_fields = ('film_work', 'person')
    list_filter = ('role',)


class GenreFilmworkInline(admin.TabularInline):
    search_fields = ('genre', )
    autocomplete_fields = ('genre',)
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    search_fields = ('film_work', )
    autocomplete_fields = ('film_work',)
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline, )
    list_display = ('title', 'type', 'get_genres', 'creation_date', 'rating', 'created',
                    'modified')
    list_filter = ('type',)
    list_prefetch_related = ('genres',) 
    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])
