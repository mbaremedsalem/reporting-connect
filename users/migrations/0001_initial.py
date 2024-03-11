# Generated by Django 5.0.1 on 2024-02-23 16:04

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(max_length=16, unique=True)),
                ('username', models.CharField(max_length=16, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('post', models.CharField(max_length=200, null=True)),
                ('role', models.CharField(choices=[('Caissier', 'Caissier'), ('ChefAgence', 'ChefAgence')], default='Caissier', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('verified', models.BooleanField(default=False)),
                ('restricted', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('number_attempt', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('AGENCE', models.CharField(max_length=255)),
                ('AGENCELIB', models.CharField(max_length=255)),
                ('TXFRAIS', models.DecimalField(decimal_places=2, max_digits=10)),
                ('TXCOMMV', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CLIMIN', models.IntegerField()),
                ('CLIMAX', models.IntegerField()),
                ('CLIATTR', models.CharField(max_length=255)),
                ('CLIENT', models.CharField(max_length=255)),
                ('ADRNO', models.CharField(max_length=255)),
                ('VILLE', models.CharField(max_length=255)),
                ('CONNECTE', models.CharField(max_length=255)),
                ('AGCPTA', models.CharField(max_length=255)),
                ('AGCOUR', models.CharField(max_length=255)),
                ('IMPRAVIS', models.CharField(max_length=255)),
                ('IMPRETAT', models.CharField(max_length=255)),
                ('IBATAVIS', models.CharField(max_length=255)),
                ('IBATETAT', models.CharField(max_length=255)),
                ('IBATREL', models.CharField(max_length=255)),
                ('IMPRMATR', models.CharField(max_length=255)),
                ('IBATMATR', models.CharField(max_length=255)),
                ('SYS_CREATED_BY', models.CharField(max_length=255)),
                ('SYS_UPDATED_DATE', models.DateTimeField()),
                ('SYS_UPDATED_BY', models.CharField(max_length=255)),
                ('SYS_VERSION_NUMBER', models.IntegerField()),
                ('SYS_CREATED_DATE', models.DateTimeField()),
                ('CLIAGP', models.CharField(max_length=255)),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'AGENCE',
            },
        ),
        migrations.CreateModel(
            name='cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_de_compte', models.CharField(blank=True, max_length=100, null=True)),
                ('code_agence', models.CharField(blank=True, max_length=5, null=True)),
                ('Nbre_carnet', models.CharField(blank=True, max_length=1, null=True)),
                ('Nbre_feuilles', models.CharField(blank=True, max_length=100, null=True)),
                ('code_transaction', models.CharField(blank=True, max_length=2, null=True)),
                ('nom_client', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('Code_Devise', models.CharField(blank=True, max_length=30, null=True)),
                ('code_bank', models.CharField(blank=True, max_length=100, null=True)),
                ('code_pays', models.CharField(blank=True, max_length=10, null=True)),
                ('numero_de_debut', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('CODE_RACINE', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('CODE_AGENCE', models.CharField(max_length=255)),
                ('NOM', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'CLIENT',
            },
        ),
        migrations.CreateModel(
            name='DemChqDtl',
            fields=[
                ('CHECKBK_NOOPER', models.CharField(max_length=255)),
                ('CHECKBKNB', models.CharField(max_length=255)),
                ('REFER1', models.CharField(max_length=255)),
                ('REFER2', models.CharField(max_length=255)),
                ('STATUS', models.CharField(max_length=255)),
                ('STATUSDATE', models.DateField()),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('SYS_VERSION_NUMBER', models.IntegerField()),
                ('SYS_CREATED_DATE', models.DateField()),
                ('SYS_CREATED_BY', models.CharField(max_length=255)),
                ('SYS_UPDATED_DATE', models.DateField()),
                ('SYS_UPDATED_BY', models.CharField(max_length=255)),
                ('STATE', models.CharField(max_length=255)),
                ('VALIDE', models.CharField(max_length=255)),
                ('CIRMAN', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'DEMCHQDTL',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('subj', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.uoload_document)),
            ],
        ),
        migrations.CreateModel(
            name='Caissier',
            fields=[
                ('useraub_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(null=True, upload_to=users.models.image_uoload_profile)),
            ],
            options={
                'abstract': False,
            },
            bases=('users.useraub',),
        ),
        migrations.CreateModel(
            name='ChefAgence',
            fields=[
                ('useraub_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(null=True, upload_to=users.models.image_uoload_profile)),
            ],
            options={
                'abstract': False,
            },
            bases=('users.useraub',),
        ),
        migrations.CreateModel(
            name='DemChq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COMPTE', models.CharField(max_length=255)),
                ('DEVISE', models.CharField(max_length=255)),
                ('RESID', models.CharField(max_length=255)),
                ('NCG', models.CharField(max_length=255)),
                ('LIBELLE', models.CharField(max_length=255)),
                ('NBRCHQ', models.IntegerField()),
                ('TYPCHQ', models.CharField(max_length=255)),
                ('ADRL1', models.CharField(max_length=255)),
                ('ADRNAT', models.CharField(max_length=255)),
                ('ADRL2', models.CharField(max_length=255)),
                ('ADRNO', models.CharField(max_length=255)),
                ('ADRL3', models.CharField(max_length=255)),
                ('ADRL4', models.CharField(max_length=255)),
                ('ADRL5', models.CharField(max_length=255)),
                ('DATDEM', models.DateField()),
                ('DATEDDEM', models.DateField()),
                ('DATREDEM', models.DateField()),
                ('DATREMCL', models.DateField()),
                ('DATMAJ', models.DateField()),
                ('REFER1', models.CharField(max_length=255)),
                ('REFER2', models.CharField(max_length=255)),
                ('NBRSOU', models.IntegerField()),
                ('CLERIB', models.CharField(max_length=255)),
                ('CHQREM', models.CharField(max_length=255)),
                ('CHQRES', models.CharField(max_length=255)),
                ('ADRL6', models.CharField(max_length=255)),
                ('INSTR', models.CharField(max_length=255)),
                ('ANNUL', models.CharField(max_length=255)),
                ('DATDES', models.DateField()),
                ('CHQDET', models.CharField(max_length=255)),
                ('STATE', models.CharField(max_length=255)),
                ('VALIDE', models.CharField(max_length=255)),
                ('EXPL', models.CharField(max_length=255)),
                ('XCIRCUL', models.CharField(max_length=255)),
                ('XEXPED', models.CharField(max_length=255)),
                ('CORCLI', models.CharField(max_length=255)),
                ('CORADRNO', models.CharField(max_length=255)),
                ('NSERLOT', models.CharField(max_length=255)),
                ('DELAI', models.CharField(max_length=255)),
                ('NATDEM', models.CharField(max_length=255)),
                ('CREMDEM', models.CharField(max_length=255)),
                ('CREMEFF', models.CharField(max_length=255)),
                ('XAVIS', models.CharField(max_length=255)),
                ('XPRIOR', models.CharField(max_length=255)),
                ('XRENOUV', models.CharField(max_length=255)),
                ('XTOPE', models.CharField(max_length=255)),
                ('EXPLVALID', models.CharField(max_length=255)),
                ('DATVALID', models.DateField()),
                ('NOOPER', models.CharField(max_length=255)),
                ('DADRNO', models.CharField(max_length=255)),
                ('DADRNAT', models.CharField(max_length=255)),
                ('DADRL1', models.CharField(max_length=255)),
                ('DADRL2', models.CharField(max_length=255)),
                ('DADRL3', models.CharField(max_length=255)),
                ('DADRL4', models.CharField(max_length=255)),
                ('DADRL5', models.CharField(max_length=255)),
                ('DADRL6', models.CharField(max_length=255)),
                ('CIRCULANT', models.CharField(max_length=255)),
                ('RENOUVNBR', models.CharField(max_length=255)),
                ('DATHDEM', models.DateField()),
                ('TYPRUE', models.CharField(max_length=255)),
                ('TYPIMM1', models.CharField(max_length=255)),
                ('TYPIMM2', models.CharField(max_length=255)),
                ('CODPOST', models.CharField(max_length=255)),
                ('DCODPOST', models.CharField(max_length=255)),
                ('DTYPRUE', models.CharField(max_length=255)),
                ('DTYPIMM1', models.CharField(max_length=255)),
                ('DTYPIMM2', models.CharField(max_length=255)),
                ('DNUMRUE', models.CharField(max_length=255)),
                ('NUMRUE', models.CharField(max_length=255)),
                ('CLIENT', models.ForeignKey(db_column='CLIENT', on_delete=django.db.models.deletion.CASCADE, to='users.client')),
            ],
            options={
                'db_table': 'DEMCHQ',
            },
        ),
    ]
