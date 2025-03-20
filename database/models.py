from django.db import models
from django.core.validators import RegexValidator
from datetime import date

class Member(models.Model):
    SEX_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'انثى')
    ]
    
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='اسم العضو'
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='النوع'
    )
    age = models.PositiveIntegerField(
        default=18,
        verbose_name='العمر'
    )
    address = models.CharField(
        max_length=100,
        default='الارض',
        verbose_name='السكن'
    )
    date_of_join = models.DateField(
        default=date.today,
        verbose_name='تاريخ الانضمام'
    )
    phone_number = models.CharField(
        max_length=17,
        verbose_name='رقم الهاتف'
    )
    telegram_id = models.CharField(
        max_length=30,
        validators=[RegexValidator(regex=r'^@[\w]+$', message='Invalid Telegram ID')],
        verbose_name='معرف التلقرام'
    )
    is_revision = models.BooleanField(
        null=True,
        blank=True,
        verbose_name='مراجعة'
    )
    colleage = models.CharField(
        max_length=200,
        verbose_name='الكلية'
    )
    working_untill = models.DateField(
        verbose_name='يعمل حتى'
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='البريد الإلكتروني'
    )
    telgram_username = models.CharField(
        max_length=200,
        verbose_name='اسم مستخدم التلقرام'
    )

    class Meta:
        verbose_name = 'عضو'
        verbose_name_plural = 'الأع'