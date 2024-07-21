
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_Librarian', '0007_delete_loan'),
        ('App_Member', '0004_user_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserDetails',
        ),
        migrations.AlterField(
            model_name='loan',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Librarian.book_data'),
        ),
        migrations.AlterField(
            model_name='readinghistoryentry',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Librarian.book_data'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='LoanedBooks',
            field=models.ManyToManyField(blank=True, related_name='borrowers', through='App_Member.Loan', to='App_Librarian.Book_Data'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='ReadingHistory',
            field=models.ManyToManyField(blank=True, related_name='readers', through='App_Member.ReadingHistoryEntry', to='App_Librarian.Book_Data'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='ReservedBooks',
            field=models.ManyToManyField(blank=True, related_name='reservers', to='App_Librarian.Book_Data'),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
