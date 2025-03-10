# Generated by Django 5.1.4 on 2024-12-26 19:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('approved', 'Подтверждено'), ('rejected', 'Отклонено')], default='pending', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('object_id', models.PositiveIntegerField(verbose_name='ID актива')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Тип актива')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests_sent', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests_received', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Запрос на передачу',
                'verbose_name_plural': 'Запросы на передачу',
                'unique_together': {('from_user', 'to_user', 'content_type', 'object_id')},
            },
        ),
    ]
