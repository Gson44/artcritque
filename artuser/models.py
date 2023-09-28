from django.db import models
from datetime import date 
from django.contrib.auth.models import User 
from django.db import models


# Create your models here.
class ArtUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

class ArtEntry(models.Model):
    art_user = models.ForeignKey(ArtUser, on_delete=models.CASCADE)
    art_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='uploads/')
    likes = models.IntegerField(default=0)
    pub_date = models.DateField(default=date.today)
    average_rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)  # New field for average rating
    
class ArtEntryRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_entry = models.ForeignKey('ArtEntry', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    # You can add additional fields like timestamp, if needed

    class Meta:
        unique_together = ('user', 'art_entry')  # Ensures a user can only rate an ArtEntry once
