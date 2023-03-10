# Generated by Django 4.1.4 on 2022-12-15 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(unique=True, verbose_name='Номер телефона')),
                ('time_zone', models.IntegerField(default=0, verbose_name='Часовой пояс')),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(unique=True, verbose_name='Код оператора')),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.code', verbose_name='Код оператора')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(verbose_name='Дата и время запуска рассылки')),
                ('message_text', models.CharField(max_length=200, verbose_name='Текст сообщения для доставки клиенту')),
                ('time_end', models.DateTimeField(verbose_name='Дата и время окончания рассылки')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.filter', verbose_name='Фильтр свойств клиентов')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, unique=True, verbose_name='Тег')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время создания (отправки)')),
                ('status', models.CharField(choices=[('cr', 'Create'), ('sn', 'Send')], default='cr', max_length=2, verbose_name='Статус отправки')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.mailing', verbose_name='Рассылка')),
            ],
        ),
        migrations.AddField(
            model_name='filter',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='client',
            name='phone_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.code', verbose_name='Код мобильного оператора'),
        ),
        migrations.AddField(
            model_name='client',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tag', verbose_name='Тег'),
        ),
    ]
