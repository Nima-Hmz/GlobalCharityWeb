# Generated by Django 5.0.4 on 2024-04-23 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogmodel',
            options={'ordering': ('-updated',), 'verbose_name': 'وبلاگ', 'verbose_name_plural': 'بلاگ ها'},
        ),
        migrations.AddField(
            model_name='blogmodel',
            name='lovely',
            field=models.BooleanField(default=False, verbose_name='محبوب'),
        ),
    ]
