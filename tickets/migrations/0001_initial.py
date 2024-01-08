# Generated by Django 4.2 on 2024-01-07 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=8, null=True)),
                ('adresse', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Objet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Represantant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Recu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marque', models.CharField(max_length=200)),
                ('probleme', models.CharField(max_length=200)),
                ('note', models.TextField(max_length=500)),
                ('prix', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('accompte', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('observation', models.TextField(blank=True, max_length=500, null=True)),
                ('cree_a', models.DateTimeField(auto_now_add=True)),
                ('modifie_a', models.DateTimeField(auto_now=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recus', to='tickets.categorie')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recus', to='tickets.client')),
                ('objet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recus', to='tickets.objet')),
                ('represantant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recus', to='tickets.represantant')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recus', to='tickets.status')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalRecu',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('marque', models.CharField(max_length=200)),
                ('probleme', models.CharField(max_length=200)),
                ('note', models.TextField(max_length=500)),
                ('prix', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('accompte', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('observation', models.TextField(blank=True, max_length=500, null=True)),
                ('cree_a', models.DateTimeField(blank=True, editable=False)),
                ('modifie_a', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('categorie', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tickets.categorie')),
                ('client', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tickets.client')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('objet', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tickets.objet')),
                ('represantant', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tickets.represantant')),
                ('status', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tickets.status')),
            ],
            options={
                'verbose_name': 'historical recu',
                'verbose_name_plural': 'historical recus',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='categorie',
            name='famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='tickets.famille'),
        ),
    ]
