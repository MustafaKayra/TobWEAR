from django.db import models
from django.utils.text import slugify

class ProductFeatures(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    feature = models.CharField(max_length=50,null=False,blank=False)

    def __str__(self):
        return f"{self.name} | {self.feature}"


class ProductColor(models.Model):
    COLOR_CHOICES = [
        ('color1', 'Yeşil'),
        ('color2', 'Kırmızı'),
        ('color3', 'Mavi'),
        ('color4', 'Siyah'),
        ('color5', 'Pembe')
    ]

    color = models.CharField(max_length=100,choices=COLOR_CHOICES)
    code = models.CharField(max_length=7,null=False,blank=False)
    code2 = models.CharField(max_length=7,null=False,blank=False)

    def __str__(self):
        return self.get_color_display()


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ('size1', 'S'),
        ('size2', 'M'),
        ('size3', 'XL'),
        ('size4', '2XL')
    ]

    size = models.CharField(max_length=100,choices=SIZE_CHOICES)

    def __str__(self):
        return self.get_size_display()


class ProductImage(models.Model):
    images = models.ImageField(upload_to='images/')


class ProductCategory(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="Kategori İsmi")

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name="Ürün İsmi")
    price = models.IntegerField(null=False,blank=False,verbose_name="Fiyat")
    discounted = models.IntegerField(null=False,blank=False,verbose_name="İndirimli Fiyat")
    features = models.ManyToManyField(ProductFeatures,null=True,blank=True,verbose_name="Ürün Özellikleri")
    colors = models.ManyToManyField(ProductColor,null=True,blank=True,verbose_name="Ürün Renkleri")
    sizes = models.ManyToManyField(ProductSize,null=False,blank=False,verbose_name="Ürün Bedenleri")
    images = models.ManyToManyField(ProductImage,null=False,blank=False,verbose_name="Resimler")
    description = models.TextField(null=True,blank=True)
    category = models.ForeignKey(ProductCategory,null=False,blank=False,verbose_name="Kategori",on_delete=models.CASCADE)
    slug = models.SlugField(null=False,blank=True,unique=True,db_index=True,verbose_name="URL")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}"


