
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0006_auto_20240512_1928'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
