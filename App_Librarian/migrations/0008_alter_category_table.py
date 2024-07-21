
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0007_delete_loan'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='Category',
        ),
    ]
