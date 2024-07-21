
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0009_alter_author_table'),
        ('App_Member', '0008_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('review_text', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Librarian.book_data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.userdetails')),
            ],
        ),
    ]
