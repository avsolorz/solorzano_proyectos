from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('especialidad', models.CharField(blank=True, max_length=150)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('correo', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name': 'Diseñador',
                'verbose_name_plural': 'Diseñadores',
                'db_table': 'disenadores',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='RedSocial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_red', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Red Social',
                'verbose_name_plural': 'Redes Sociales',
                'db_table': 'redes_sociales',
                'ordering': ['nombre_red'],
            },
        ),
    ]
