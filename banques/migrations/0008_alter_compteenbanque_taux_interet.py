# Generated by Django 4.2.5 on 2024-10-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banques', '0007_remove_compteenbanque_banque_delete_banque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compteenbanque',
            name='taux_interet',
            field=models.FloatField(default=10),
        ),
    ]