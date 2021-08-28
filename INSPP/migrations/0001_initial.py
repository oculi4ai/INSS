# Generated by Django 3.2.5 on 2021-07-29 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='INSPP_logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(default='[]', max_length=200000000)),
                ('table', models.CharField(default='[]', max_length=200000000)),
                ('values', models.CharField(default='[]', max_length=200000000)),
                ('date_and_time', models.CharField(default='[]', max_length=200000000)),
                ('distribution', models.CharField(default='[]', max_length=200000000)),
            ],
        ),
        migrations.CreateModel(
            name='PackedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('unpacked_product_quantity_in_one', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('Solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], default=('Solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PackingMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('Piece', 'Piece'), ('Kilogram', 'Kilogram'), ('Metre', 'Metre')], max_length=200)),
                ('loq_warning', models.BooleanField(default=0)),
                ('loq_quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('m_type', models.CharField(choices=[('Solid', 'Solid'), ('Liquid', 'Liquid'), ('Gas', 'Gas')], max_length=200)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], max_length=200)),
                ('density', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('loq_warning', models.BooleanField(default=0)),
                ('loq_quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('loq_unit', models.CharField(choices=[('solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UnpackedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('material_type', models.CharField(choices=[('Solid', 'Solid'), ('Liquid', 'Liquid'), ('Gas', 'Gas')], max_length=200)),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('Solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], default=('Solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UnpackedProductRawMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.rawmaterial')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.unpackedproduct')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialsOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], max_length=200)),
                ('date', models.DateField()),
                ('note', models.TextField()),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialsInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('unit', models.CharField(choices=[('solid', (('MG', 'MG'), ('CG', 'CG'), ('DG', 'DG'), ('G', 'G'), ('DAG', 'DAG'), ('HG', 'HG'), ('KG', 'KG'), ('T', 'T'))), ('Liquid / Gas', (('ML', 'ML'), ('CL', 'CL'), ('DL', 'DL'), ('L', 'L'), ('DAL', 'DAL'), ('HL', 'HL'), ('KL', 'KL')))], max_length=200)),
                ('date', models.DateField()),
                ('note', models.TextField()),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='PackingMaterialOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('date', models.DateField()),
                ('note', models.TextField()),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.packingmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='PackingMaterialInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('date', models.DateField()),
                ('note', models.TextField()),
                ('material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.packingmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='PackedProductPackingMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_in_one', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('packed_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.packedproduct')),
                ('packing_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.packingmaterial')),
            ],
        ),
        migrations.AddField(
            model_name='packedproduct',
            name='unpacked_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.unpackedproduct'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.DecimalField(decimal_places=1, default=0, max_digits=100)),
                ('starting_date', models.DateField()),
                ('planned_finishing_date', models.DateField()),
                ('actual_finishing_date', models.DateField(blank=True, null=True)),
                ('done', models.BooleanField(default=0)),
                ('packed_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INSPP.packedproduct')),
            ],
        ),
    ]