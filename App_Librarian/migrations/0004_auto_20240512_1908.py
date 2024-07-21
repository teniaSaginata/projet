
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0003_book_data_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_data',
            name='cover_image',
            field=models.ImageField(upload_to='App_Librarian/coverimages/'),
        ),
        migrations.AlterField(
            model_name='book_data',
            name='pdf_file',
            field=models.FileField(upload_to='App_Librarian/pdfs/'),
        ),
    ]
