# Generated by Django 3.2.4 on 2021-06-22 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='CollegeProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.PositiveSmallIntegerField()),
                ('cutoff', models.PositiveSmallIntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.college')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('batch', models.PositiveSmallIntegerField()),
                ('rank', models.PositiveIntegerField()),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quota', models.CharField(choices=[('RE', 'Regualar'), ('OT', 'Other')], default='RE', max_length=2)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.collegeprogram')),
            ],
        ),
        migrations.AddField(
            model_name='collegeprogram',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.program'),
        ),
        migrations.AddField(
            model_name='college',
            name='programs',
            field=models.ManyToManyField(through='rank.CollegeProgram', to='rank.Program'),
        ),
    ]
