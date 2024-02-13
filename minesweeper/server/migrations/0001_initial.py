# Generated by Django 5.0.2 on 2024-02-13 15:00

import django.core.validators
import django.db.models.deletion
import server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('width', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Ширина')),
                ('height', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='Высота')),
                ('mines_count', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), server.models.validate_mines_count], verbose_name='Количество мин')),
                ('completed', models.BooleanField(default=False, verbose_name='Завершена ли игра')),
                ('field', models.JSONField(default=list, verbose_name='Поле для игры')),
                ('field_mines', models.JSONField(null=True, verbose_name='Поле с минами')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
        migrations.CreateModel(
            name='Mine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_width', models.PositiveIntegerField()),
                ('y_height', models.PositiveIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mines', to='server.game')),
            ],
        ),
    ]