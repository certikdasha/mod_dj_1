# Generated by Django 3.1.7 on 2021-03-20 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210320_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='refund',
            name='ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.order'),
        ),
    ]