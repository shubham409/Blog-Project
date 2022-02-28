# Generated by Django 4.0.2 on 2022-02-28 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0013_article_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.CharField(db_column='column1', max_length=40)),
                ('column2', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TempUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'temp_user',
            },
        ),
    ]
