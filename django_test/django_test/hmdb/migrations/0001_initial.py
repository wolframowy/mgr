# Generated by Django 2.2.6 on 2019-11-10 19:32

from django.db import migrations, models
import djongo.models.fields
import hmdb.submodels.spectra


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spectra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ms_ms', djongo.models.fields.EmbeddedModelField(model_container=hmdb.submodels.spectra.MsMs, null=True)),
            ],
        ),
    ]
