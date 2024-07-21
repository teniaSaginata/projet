
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_period', models.PositiveIntegerField()),
                ('pickup_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingHistoryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_read', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Phone', models.CharField(default=None, max_length=100)),
                ('Email', models.CharField(default=None, max_length=100)),
                ('Username', models.CharField(default=None, max_length=100)),
                ('Password', models.CharField(default=None, max_length=100)),
                ('Address', models.CharField(default=None, max_length=100)),
                ('NotificationPreferences', models.BooleanField(default=True)),
                ('ProfilePicture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
            ],
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='title',
        ),
        migrations.DeleteModel(
            name='LoanRequest',
        ),
        migrations.DeleteModel(
            name='Recommendation',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='user',
            name='LoanedBooks',
            field=models.ManyToManyField(blank=True, related_name='borrowers', through='App_Member.Loan', to='App_Member.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='ReadingHistory',
            field=models.ManyToManyField(blank=True, related_name='readers', through='App_Member.ReadingHistoryEntry', to='App_Member.Book'),
        ),
        migrations.AddField(
            model_name='user',
            name='ReservedBooks',
            field=models.ManyToManyField(blank=True, related_name='reservers', to='App_Member.Book'),
        ),
        migrations.AddField(
            model_name='readinghistoryentry',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.book'),
        ),
        migrations.AddField(
            model_name='readinghistoryentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.user'),
        ),
        migrations.AddField(
            model_name='loan',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.book'),
        ),
        migrations.AddField(
            model_name='loan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Member.user'),
        ),
    ]
