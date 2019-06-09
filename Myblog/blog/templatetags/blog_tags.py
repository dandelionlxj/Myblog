#coding:utf-8
from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
from blog.models import Category

register=template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    '''
    获取最近的五篇文章
    '''
    return Post.objects.all().order_by('create_time')[:num]

@register.simple_tag
def archives():
    '''
    按月排序
    '''
    return Post.objects.dates('create_time','month',order='DESC')

@register.simple_tag
def get_categories():
    '''
    返回文章分类
    '''
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    '''
    返回标签
    '''
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)