# Generated by Django 4.2.2 on 2023-09-26 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artuser', '0002_alter_artentry_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='artentry',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.CreateModel(
            name='ArtEntryRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('art_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artuser.artentry')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'art_entry')},
            },
        ),
    ]
