
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Member', '0006_loan_submission_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='extended_loan_period',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='loan',
            name='extended_submission_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_status',
            field=models.CharField(choices=[('requested', 'Requested'), ('issued', 'Issued'), ('returned', 'Returned'), ('extended', 'Extended')], default='requested', max_length=20),
        ),
    ]
