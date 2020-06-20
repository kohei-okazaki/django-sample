# -*- coding: utf-8 -*-
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db import models
import re


# Create your models here.
def number_only(value):
    if (re.match(r'^[0-9]*$', value) == None):
        raise ValidationError("%(value)s is not Number", params={"value":value})


class Friend(models.Model):
    """
    FRIENDテーブルのEntityクラス(主)
    """

    # name = models.CharField(max_length=100, validators=[number_only])
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=200, validators=[EmailValidator()])
    gender = models.BooleanField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    birthday = models.DateField()

    def __str__(self):
        return "Friend: id=" + str(self.id) + \
            ", name=" + str(self.name) + \
            ", age=" + str(self.age) + \
            ", mail=" + str(self.mail)


class Message(models.Model):
    """
    MESSAGEテーブルのEntityクラス(従)
    """

    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Message: id=" + str(self.id) + \
            ", title=" + str(self.title) + \
            ", content=" + str(self.content) + \
            ", pub_date=" + str(self.pub_date)

    class Meta:
        ordering = ('pub_date',)
