# Migración inicial independiente de Agenda Simple V1.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Cliente', fields=[
            ('id', models.AutoField(primary_key=True, serialize=False)),
            ('nombre', models.CharField(max_length=100)),
            ('apellido', models.CharField(max_length=100)),
            ('correo', models.EmailField(max_length=150)),
            ('dni', models.CharField(max_length=20, unique=True)),
            ('telefono', models.CharField(blank=True, max_length=30)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
        ], options={'db_table': 'clientes'}),
        migrations.CreateModel(name='Cita', fields=[
            ('id', models.AutoField(primary_key=True, serialize=False)),
            ('asunto', models.CharField(max_length=200)),
            ('fecha', models.DateField()),
            ('hora', models.TimeField()),
            ('direccion', models.CharField(max_length=255)),
            ('referencia', models.CharField(blank=True, max_length=255)),
            ('notas', models.TextField(blank=True)),
            ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')], default='Pendiente', max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('cliente', models.ForeignKey(db_column='client_id', on_delete=django.db.models.deletion.PROTECT, related_name='citas', to='apps.cliente')),
        ], options={'db_table': 'citas', 'ordering': ['fecha', 'hora']}),
    ]
