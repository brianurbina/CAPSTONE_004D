# Generated by Django 5.1.1 on 2024-10-29 00:17

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0006_alter_conversacion_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reseña',
            fields=[
                ('id_resena', models.UUIDField(primary_key=True, serialize=False)),
                ('estrellas', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('reseña', models.CharField(default='Sin comentarios', max_length=255)),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dueñoreseña', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dueñoperfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
