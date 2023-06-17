from django.db import models


class Number(models.Model):
    number = models.CharField(unique=True, max_length=255)
    date_added = models.DateTimeField()
    is_active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        managed = False
        db_table = 'number'
        verbose_name = 'Номер телефону'
        verbose_name_plural = 'Номери телефонів'


class NumberActivity(models.Model):
    id_number = models.IntegerField(primary_key=True)
    # id_number = models.ForeignKey('Number', models.DO_NOTHING,  db_column='id_number')
    last_view_date = models.DateTimeField()
    views = models.IntegerField()

    def __str__(self):
        return self.id_number

    class Meta:
        managed = False
        db_table = 'number_activity'
        verbose_name = 'Активність номеру телефону'
        verbose_name_plural = 'Активність номерів телефонів'


class Comment(models.Model):
    id_number = models.ForeignKey('Number', models.DO_NOTHING, db_column='id_number')
    content = models.CharField(max_length=255)
    date_create = models.DateTimeField()
    level = models.ForeignKey('Levels', models.DO_NOTHING, db_column='level')

    def __str__(self):
        return f"{self.id_number} - {self.content}"

    class Meta:
        managed = False
        db_table = 'comment'
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'


class CommentActivity(models.Model):
    id_comment = models.IntegerField(primary_key=True)
    good = models.IntegerField()
    bad = models.IntegerField()

    def __str__(self):
        return self.id_comment

    class Meta:
        managed = False
        db_table = 'comment_activity'
        verbose_name = 'Активність коментаря'
        verbose_name_plural = 'Активність коментарів'


class Levels(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        managed = False
        db_table = 'levels'
        verbose_name = 'Рівень коментаря'
        verbose_name_plural = 'Рівні коментарів'


class DateView(models.Model):
    id_number = models.ForeignKey('Number', models.DO_NOTHING, db_column='id_number')
    date = models.DateField()
    views = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'date_view'


class Contacts(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    create_at = models.DateTimeField()
    answered = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'contacts'


class Questions(models.Model):
    index = models.IntegerField()
    question = models.CharField(max_length=255)
    answer = models.TextField()

    class Meta:
        managed = False
        db_table = 'questions'

