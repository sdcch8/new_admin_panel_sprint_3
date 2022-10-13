import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        ordering = ['id']
        db_table = '"content"."genre"'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

        constraints = [
            models.UniqueConstraint(fields=['id'], name='genre_pkey')
        ]
        indexes = [
            models.Index(fields=['id'], name='genre_pkey'),
        ]

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE,
                                  verbose_name=_('film_work'),
                                  related_name='genre_filmwork')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              verbose_name=_('genre'),
                              related_name='genre_filmwork')
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ['id']
        db_table = '"content"."genre_film_work"'
        verbose_name = _('GenreFilmwork')
        verbose_name_plural = _('GenreFilmworks')

        constraints = [
            models.UniqueConstraint(fields=['id'], name='genre_film_work_pkey')
        ]
        indexes = [
            models.Index(fields=['id'], name='genre_film_work_pkey'),
            UniqueIndex(fields=['film_work_id', 'genre_id'],
                        name='film_work_genre_idx'),
        ]

    def __str__(self):
        return '{film_work} / {genre}'.format(film_work=self.film_work.title,
                                              genre=self.genre.name)


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        ordering = ['id']
        db_table = '"content"."person"'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

        constraints = [
            models.UniqueConstraint(fields=['id'], name='person_pkey')
        ]
        indexes = [
            models.Index(fields=['id'], name='person_pkey'),
        ]

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):

    class Roles(models.TextChoices):
        ACTOR = 'actor'
        DIRECTOR = 'director'
        WRITER = 'writer'

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE,
                                  verbose_name=_('film_work'),
                                  related_name='person_filmwork')
    person = models.ForeignKey('Person', on_delete=models.CASCADE,
                               verbose_name=_('person'),
                               related_name='person_filmwork')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    role = models.TextField(_('role'), choices=Roles.choices, null=True)

    class Meta:
        ordering = ['id']
        db_table = '"content"."person_film_work"'
        verbose_name = _('PersonFilmwork')
        verbose_name_plural = _('PersonFilmworks')

        constraints = [
            models.UniqueConstraint(fields=['id'],
                                    name='person_film_work_pkey')
        ]
        indexes = [
            models.Index(fields=['id'], name='person_film_work_pkey'),
            models.Index(fields=['film_work_id', 'person_id', 'role'],
                         name='film_work_person_role_idx'),
        ]

    def __str__(self):
        return '{title} / {name} / {role}'.format(title=self.film_work.title,
                                                  name=self.person.full_name,
                                                  role=self.role)


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypeChoices(models.TextChoices):
        MOVIE = _('movie')
        TV_SHOW = _('tv_show')

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    type = models.CharField(_('type'), max_length=255,
                            choices=TypeChoices.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class Meta:
        ordering = ['id']
        db_table = '"content"."film_work"'
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

        constraints = [
            models.UniqueConstraint(fields=['id'], name='film_work_pkey')
        ]
        indexes = [
            models.Index(fields=['id'], name='film_work_pkey'),
            models.Index(fields=['title'], name='film_work_title_idx'),
            models.Index(fields=['creation_date'],
                         name='film_work_creation_date_idx'),
        ]

    def __str__(self):
        return self.title
