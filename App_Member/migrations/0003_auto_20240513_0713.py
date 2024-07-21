
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Member', '0002_auto_20240512_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='City',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='Country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='DateOfBirth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='Gender',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='MemberSince',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='user',
            name='Occupation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='State',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
