# Generated by Django 5.1.2 on 2024-10-24 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banques', '0002_compteenbanque_banque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compteenbanque',
            name='banque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banques.banque'),
        ),
    ]
