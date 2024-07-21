
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0009_alter_author_table'),
        ('App_Member', '0010_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Librarian.book_data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.userdetails')),
            ],
        ),
    ]
