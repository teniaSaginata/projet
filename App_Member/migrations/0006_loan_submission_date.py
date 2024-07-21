
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App_Member', '0005_auto_20240513_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='submission_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
