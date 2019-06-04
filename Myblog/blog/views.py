#coding:utf-8
import markdown
from django.shortcuts import render,HttpResponse,get_object_or_404
from . models import Post ,Category
from comments.forms import CommentForm

# Create your views here.
def index(request):
    '''
    主页
    '''
    post_list=Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',{'post_list':post_list})

def detail(request,pk):
    #如果文章不存在，则返回404错误
    post=get_object_or_404(Post,pk=pk)
    #阅读量+1
    post.increase_views()
    post.body=markdown.markdown(post.body,
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite', #语法高亮拓展
                                    'markdown.extensions.toc',        #自动生成目录
                                ])
    form=CommentForm()
    #获取这篇文章下的全部评论
    comment_list=post.comment_set.all()

    #将文章、表单、以及文章下的评论列表作为模板变量传给detail
    context={'post':post,
             'form':form,
             'comment_list':comment_list
    }
    return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
    post_list=Post.objects.filter(create_time__year=year,
                                  create_time__month=month
                                  ).order_by('-create_time')
    return render(request,'blog/index.html',{'post_list':post_list})

def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',{'post_list':post_list})