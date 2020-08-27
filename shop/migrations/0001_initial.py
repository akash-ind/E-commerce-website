# Generated by Django 3.0.5 on 2020-08-01 14:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shop.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
        ('print', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=32)),
                ('p_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('prices', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('product_image', models.ImageField(upload_to=shop.models.path_and_rename('products/images'))),
            ],
            options={
                'ordering': ['-prices'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('category_image', models.ImageField(upload_to=shop.models.category_path('products/category'))),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductWithCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ProductCategory'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=256, null=True)),
                ('order_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('method', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateTimeField()),
                ('active', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('not_responding', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Address')),
                ('print_order', models.ManyToManyField(blank=True, to='print.PrintDoc')),
                ('shop_order', models.ManyToManyField(blank=True, to='shop.ProductWithCount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=64, null=True)),
                ('category', models.CharField(blank=True, max_length=64, null=True)),
                ('number', models.IntegerField(help_text='Only Number are allowed', validators=[django.core.validators.MinValueValidator(1)])),
                ('expected_price', models.IntegerField(help_text='Only number are allowed', validators=[django.core.validators.MinValueValidator(1)])),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('delivered', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('printing', models.ManyToManyField(blank=True, to='print.PrintDoc')),
                ('products', models.ManyToManyField(blank=True, to='shop.ProductWithCount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
