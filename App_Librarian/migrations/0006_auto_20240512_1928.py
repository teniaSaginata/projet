
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0005_auto_20240512_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_data',
            name='cover_image',
            field=models.ImageField(upload_to='coverimages/'),
        ),
        migrations.AlterField(
            model_name='book_data',
            name='pdf_file',
            field=models.FileField(upload_to='pdfs/'),
        ),
    ]
