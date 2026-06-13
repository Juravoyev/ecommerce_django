from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_expand_catalog_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='categories/',
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='products/',
            ),
        ),
    ]
