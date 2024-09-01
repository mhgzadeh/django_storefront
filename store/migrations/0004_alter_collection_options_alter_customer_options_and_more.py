# Generated by Django 5.1 on 2024-09-01 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('store', '0003_alter_order_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ('title',)},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('last_name', 'first_name')},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-placed_at', 'customer')},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('title',)},
        ),
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products',
                                    to='store.collection'),
        ),
    ]
