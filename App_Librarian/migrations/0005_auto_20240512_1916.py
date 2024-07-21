
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0004_auto_20240512_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_data',
            name='cover_image',
            field=models.ImageField(upload_to='media/App_Librarian/coverimages/'),
        ),
        migrations.AlterField(
            model_name='book_data',
            name='pdf_file',
            field=models.FileField(upload_to='media/App_Librarian/pdfs/'),
        ),
    ]
