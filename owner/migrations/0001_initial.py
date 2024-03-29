# Generated by Django 4.2.6 on 2024-03-03 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Deadstock_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('item_image', models.ImageField(blank=True, null=True, upload_to='item_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.CharField(max_length=255)),
                ('stock', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('manufacturer', models.CharField(max_length=255)),
                ('item_image', models.ImageField(blank=True, null=True, upload_to='item_images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='owner.category')),
            ],
        ),
    ]
