
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Member', '0003_auto_20240513_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Name',
            field=models.CharField(default=None, max_length=300),
        ),
    ]
