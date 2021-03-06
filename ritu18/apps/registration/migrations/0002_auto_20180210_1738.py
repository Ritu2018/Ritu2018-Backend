# Generated by Django 2.0.2 on 2018-02-10 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_code', models.CharField(max_length=10)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='transactionmodel',
            name='payment_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transactionmodel',
            name='status',
            field=models.CharField(default='p', max_length=1),
        ),
        migrations.AddField(
            model_name='registrationmodel',
            name='transaction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.TransactionModel'),
        ),
        migrations.AlterUniqueTogether(
            name='registrationmodel',
            unique_together={('profile', 'event_code')},
        ),
    ]
