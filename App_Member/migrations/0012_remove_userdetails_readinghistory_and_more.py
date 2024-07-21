
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("App_Member", "0011_wishlist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userdetails",
            name="ReadingHistory",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="Bio",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="LoanedBooks",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="MemberSince",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="NotificationPreferences",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="Occupation",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="ProfilePicture",
        ),
        migrations.RemoveField(
            model_name="userdetails",
            name="ReservedBooks",
        ),
        migrations.DeleteModel(
            name="ReadingHistoryEntry",
        ),
    ]
