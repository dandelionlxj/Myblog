# coding=utf-8
from django.db import models
from django.contrib.auth.models import  User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

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
    views=models.PositiveIntegerField(default=0,verbose_name='阅读量')
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name_plural='文章'
        ordering=['-create_time']
    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        #如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md=markdown.Markdown(extensions=[
                'markdown,extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #先将 Markdown 文本渲染成 HTML 文本
            #strip_tags 去掉 HTML 文本的全部 HTML 标签
            #从文本摘取前 54 个字符赋给 excerpt
            self.excerpt=strip_tags(md.convert(self.body))[:54]

        #调用父类的save方法将数据保存到数据库中
        super(Post,self).save(*args,**kwargs)