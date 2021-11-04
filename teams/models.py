from django.db import DefaultConnectionProxy, models
from django.urls import reverse
from django.utils.text import slugify
from cms.fields import OrderField
from pathlib import Path


class Team(models.Model):
    PREMIERLEAGUE = 1
    LALIGA = 2
    INDIANSUPERLEAGUE = 3
    LEAGUES = (
        (PREMIERLEAGUE, 'Premier-League'),
        (LALIGA, 'LaLiga'),
        (INDIANSUPERLEAGUE, 'I.S.L'),
    )
    team = models.CharField(max_length=50, verbose_name='Team')
    establishment_date = models.DateField(null=True, verbose_name='Established on')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Price in €')
    players = models.IntegerField(blank=True, null=True, verbose_name='Players')
    league = models.PositiveSmallIntegerField(choices=LEAGUES, default=INDIANSUPERLEAGUE, verbose_name='League')
    order = OrderField(blank=True, verbose_name='Order #', default=None)

    def __str__(self):
        return self.team

    def get_absolute_url(self):
        return reverse('teams:team-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['order']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Team')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    title = models.CharField(max_length=50, default="#", blank=True)
    username = models.CharField(max_length=90, verbose_name='Username')
    email = models.EmailField(verbose_name='Email')
    position = models.CharField(max_length=100, verbose_name='Position')
    date_bought = models.DateTimeField(blank=True, null=True, verbose_name='Date Bought')
    order = OrderField(blank=True, for_fields=['team'], verbose_name='Order #')

    def __str__(self):
        return str(self.team)

    def save(self, *args, **kwargs):
        self.slug = slugify('{}-{}-{}'.format(self.team, self.team.team, self.team.pk))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('teams:player-update', kwargs={'team': self.team.pk, 'slug': self.slug})

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ('order', '-date_bought')


class Documents(models.Model):
    documents = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Team')
    file = models.FileField(upload_to='files/', null=True, blank=True, max_length=255, verbose_name='Filename')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='File uploaded at')
    order = OrderField(blank=True, for_fields=['team'], verbose_name='Order #')

    @property
    def filename(self):
        return Path(self.documents.name).name

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if self.pk:
            old_documents = Documents.objects.get(pk=self.pk).file
            if not old_documents == self.file:
                storage = old_documents.storage
                if storage.exists(old_documents.name):
                    storage.delete(old_documents.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage = self.file.storage
        if storage.exists(self.file.name):
            storage.delete(self.file.name)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ('order', )
