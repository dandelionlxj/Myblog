# coding=utf-8
from django.db import models
from django.contrib.auth.models import  User
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='分类'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural='标签'

    def __str__(self):
        return self.name

class Post(models.Model):

    #文章标题
    title=models.CharField(max_length=70,verbose_name='标题')
    #正文
    body=models.TextField(verbose_name='正文')
    #创建时间
    create_time=models.DateTimeField(verbose_name='创建时间')
    #最后一次修改时间
    modified_time=models.DateTimeField(verbose_name='最近修改时间')
    #文章摘要
    excerpt=models.CharField(max_length=200,blank=True,verbose_name='摘要')
    category=models.ForeignKey(Category,on_delete=True,verbose_name='分类')
    tag=models.ManyToManyField(Tag,blank=True)
    author=models.ForeignKey(User,on_delete=True,verbose_name='作者')

    class Meta:
        verbose_name_plural='文章'
        ordering=['-create_time']
    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})