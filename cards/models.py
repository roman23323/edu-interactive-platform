from django.conf import settings
from django.db import models


class CardCollection(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='card_collections',
    )

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Card(models.Model):
    collection = models.ForeignKey(
        CardCollection,
        on_delete=models.CASCADE,
        related_name='cards',
    )

    first_page = models.TextField()
    second_page = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Card #{self.id}'