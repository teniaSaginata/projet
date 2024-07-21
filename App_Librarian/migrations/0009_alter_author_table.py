
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0008_alter_category_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='author',
            table='Author',
        ),
    ]
