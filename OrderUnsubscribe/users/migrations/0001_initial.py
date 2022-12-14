# Generated by Django 4.0.6 on 2022-07-16 09:55

from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUnsubscribeInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('TraceId', models.CharField(default='', max_length=32)),
                ('ActionTime', models.TimeField()),
                ('MsgType_x', models.CharField(default='', max_length=32)),
                ('MsgType_y', models.CharField(default='', max_length=32)),
                ('Version_x', models.CharField(default='', max_length=32)),
                ('Version_y', models.CharField(default='', max_length=32)),
                ('OrderID', models.CharField(default='', max_length=32)),
                ('UserPseudoCode_x', models.CharField(default='', max_length=32)),
                ('UserPseudoCode_y', models.CharField(default='', max_length=32)),
                ('ActionID', models.CharField(default='', max_length=32)),
                ('EffectiveRealTime', models.DateTimeField()),
                ('ExpireRealTime', models.CharField(default='', max_length=64)),
                ('ChannelId', models.CharField(default='', max_length=32)),
                ('ProductId_x', models.CharField(default='', max_length=32)),
                ('ProductId_y', models.CharField(default='', max_length=32)),
                ('OrderType', models.CharField(default='', max_length=32)),
                ('sign', models.CharField(default='', max_length=64)),
                ('ProvCode', models.CharField(default='', max_length=32)),
                ('hRet', models.CharField(default='', max_length=32)),
                ('desc', models.CharField(default='', max_length=32)),
                ('url', models.CharField(default='', max_length=128)),
            ],
            options={
                'db_table': 'if2_message',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='?????????')),
                ('password', models.CharField(max_length=128, verbose_name='????????????')),
                ('nickname', models.CharField(blank=True, max_length=13, null=True, verbose_name='??????')),
                ('is_active', models.BooleanField(default=True, verbose_name='????????????')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True, verbose_name='???????????????')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '??????',
                'verbose_name_plural': '??????',
                'db_table': 'user',
            },
        ),
    ]
