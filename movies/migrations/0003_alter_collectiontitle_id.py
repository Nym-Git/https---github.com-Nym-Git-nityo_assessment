# Generated by Django 4.0.3 on 2023-12-04 13:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_moviecollection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectiontitle',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
