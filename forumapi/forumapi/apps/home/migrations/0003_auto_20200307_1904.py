# Generated by Django 2.2.6 on 2020-03-07 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_banner_is_http'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default='2020-03-07 20:00:00', verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='is_show',
            field=models.BooleanField(default=True, verbose_name='是否上架'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='name',
            field=models.CharField(max_length=150, verbose_name='标题'),
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='标题')),
                ('orders', models.IntegerField(verbose_name='显示顺序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_http', models.BooleanField(default=True, help_text='如果是站内地址,则默认勾选', verbose_name='是否站内的链接')),
                ('link', models.CharField(help_text='如果是站外链接,必须加上协议, 格式如: http://www.renran.cn', max_length=500, verbose_name='导航地址')),
                ('option', models.SmallIntegerField(choices=[(1, '头部导航'), (2, '脚部导航')], default=1, verbose_name='导航位置')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='son', to='home.Nav', verbose_name='父亲导航')),
            ],
            options={
                'verbose_name': '导航菜单',
                'verbose_name_plural': '导航菜单',
                'db_table': 'rr_nav',
            },
        ),
    ]
