from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email alanı gereklidir")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30,null=False,blank=False,verbose_name="İsim")
    last_name = models.CharField(max_length=30,null=False,blank=False,verbose_name="Soyisim")
    email = models.EmailField(null=False,blank=False,verbose_name="Email",unique=True)
    adress = models.CharField(max_length=200,null=True,blank=True,verbose_name="Adres")
    city = models.CharField(max_length=100,null=True,blank=True,verbose_name="Şehir")
    country = models.CharField(max_length=100,null=True,blank=True,verbose_name="Ülke")
    zipcode = models.CharField(max_length=5,null=True,blank=True,verbose_name="Posta Kodu")
    gsmnumber = models.CharField(max_length=11,null=True,blank=True,verbose_name="Telefon Numarası")
    cardnumber = models.CharField(max_length=16,null=True,blank=True,verbose_name="Kart Numarası")
    cardexpire = models.CharField(max_length=5,null=True,blank=True,verbose_name="Kart Son Kullanma Tarihi")
    cvc = models.CharField(max_length=3,null=True,blank=True,verbose_name="CVC")
    is_active = models.BooleanField(default=True,verbose_name="Kullanıcı Aktiflik Durumu")
    is_staff = models.BooleanField(default=False,verbose_name="Kullanıcı Yönetici Paneline Giriş Yetkisi")
    is_superuser = models.BooleanField(default=False,verbose_name="Yönetici Yetkisi")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Kullanıcı Kayıt Olma Tarihi")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def clean(self):
        if self.zipcode and not self.zipcode.isdigit():
            raise ValidationError("Posta Kodu Sadece Rakamlardan Oluşmalıdır")
        
        if self.zipcode and len(self.zipcode) != 5:
            raise ValidationError("Geçerli Bir Posta Kodu Giriniz")
        
        if self.gsmnumber and not self.gsmnumber.isdigit():
            raise ValidationError("Telefon Numarası Sadece Rakamlardan Oluşmalıdır")
        
        if self.gsmnumber and len(self.gsmnumber) != 11:
            raise ValidationError("Geçerli Bir Telefon Numarası Giriniz")
        
        if self.cardnumber and not self.cardnumber.isdigit():
            raise ValidationError("Kart Numarası Sadece Rakamlardan Oluşmalıdır")
        
        if self.cardnumber and len(self.cardnumber) != 16:
            raise ValidationError("Geçerli Bir Kart Numarası Giriniz")
        
        if self.cardexpire and not self.cardexpire.isdigit():
            raise ValidationError("Kart Son Kullanma Tarihi Sadece Rakamlardan Oluşmalıdır")
        
        if self.cvc and not self.cvc.isdigit():
            raise ValidationError("Kart Güvenlik Kodu Sadece Rakamlardan Oluşmalıdır")
        
        if self.cvc and len(self.cvc) != 3:
            raise ValidationError("Geçerli Bir Kart Güvenlik Kodu Giriniz")
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

