from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transformjob',
            name='output_format',
            field=models.CharField(
                choices=[('excel', 'Excel (.xlsx)'), ('csv', 'CSV (.csv)')],
                default='excel',
                max_length=10,
            ),
        ),
    ]
