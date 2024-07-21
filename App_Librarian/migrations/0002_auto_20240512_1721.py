
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='book',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='user',
        ),
        migrations.DeleteModel(
            name='Book_Data',
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
