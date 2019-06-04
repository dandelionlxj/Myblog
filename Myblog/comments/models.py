#coding=utf-8
from django.db import models

# Create your models here.
class Comment(models.Model):
    name=models.CharField(max_length=100,verbose_name='名称')
    email=models.EmailField(max_length=255,verbose_name='邮箱')
    url=models.URLField(blank=True)
    text=models.TextField(verbose_name='评论')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    post=models.ForeignKey('blog.Post',on_delete=True,verbose_name='评论文章')

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name_plural='评论表'