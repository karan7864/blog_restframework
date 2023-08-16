# Generated by Django 4.2.3 on 2023-08-02 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_alter_commentreaction_reaction'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='commentreaction',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='commentreaction',
            name='reaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='commentreaction',
            name='user',
        ),
    ]
