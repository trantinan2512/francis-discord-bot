# Generated by Django 2.1.7 on 2019-05-06 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HonkaiImpactDaily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(help_text='Must be a Unicode character', max_length=1)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
    ]