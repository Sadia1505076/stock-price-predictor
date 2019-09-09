# Generated by Django 2.2.1 on 2019-07-29 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0003_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('trade_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('authorized_capital', models.FloatField(blank=True, null=True)),
                ('paidup_capital', models.FloatField(blank=True, null=True)),
                ('outstanding_share_number', models.BigIntegerField(blank=True, null=True)),
                ('sector', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DseHistory',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('dsex_index', models.FloatField(blank=True, null=True)),
                ('total_trade', models.BigIntegerField(blank=True, null=True)),
                ('total_volume', models.BigIntegerField(blank=True, null=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
                ('total_market_cap', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dse_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DsePrediction',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('future_index', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dse_prediction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=45)),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True)),
                ('email_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShareHistory',
            fields=[
                ('trade_code', models.ForeignKey(db_column='trade_code', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='home.Company')),
                ('date', models.DateField()),
                ('opening_price', models.FloatField(blank=True, null=True)),
                ('max_price', models.FloatField(blank=True, null=True)),
                ('min_price', models.FloatField(blank=True, null=True)),
                ('closing_price', models.FloatField(blank=True, null=True)),
                ('total_volume', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'share_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SharePrediction',
            fields=[
                ('trade_code', models.ForeignKey(db_column='trade_code', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='home.Company')),
                ('date', models.DateField()),
                ('future_price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'share_prediction',
                'managed': False,
            },
        ),
    ]
