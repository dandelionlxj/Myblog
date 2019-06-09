#coding:utf-8
import markdown
from django.shortcuts import render,HttpResponse,get_object_or_404
from . models import Post ,Category
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView

# Create your views here.
# def index(request):
#     '''
#     主页
#     '''
#     post_list=Post.objects.all().order_by('-create_time')
#     return render(request,'blog/index.html',{'post_list':post_list})
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def detail(request,pk):
#     #如果文章不存在，则返回404错误
#     post=get_object_or_404(Post,pk=pk)
#     #阅读量+1
#     post.increase_views()
#     post.body=markdown.markdown(post.body,
#                                 extensions=[
#                                     'markdown.extensions.extra',
#                                     'markdown.extensions.codehilite', #语法高亮拓展
#                                     'markdown.extensions.toc',        #自动生成目录
#                                 ])
#     form=CommentForm()
#     #获取这篇文章下的全部评论
#     comment_list=post.comment_set.all()
#
#     #将文章、表单、以及文章下的评论列表作为模板变量传给detail
#     context={'post':post,
#              'form':form,
#              'comment_list':comment_list
#     }
#     return render(request,'blog/detail.html',context=context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response=super(PostDetailView,self).get(request,*args,**kwargs)

        #将文章量加一，注意self.object的值就是被访问的文章post
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        #覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post=super(PostDetailView,self).get_object(queryset=None)
        post.body=markdown.markdown(post.body,
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite', #语法高亮拓展
                                    'markdown.extensions.toc',        #自动生成目录
                                ])
        return post

    def get_context_data(self, **kwargs):
        #还要把评论表单、post 下的评论列表传递给模板。
        context=super(PostDetailView,self).get_context_data(**kwargs)
        form=CommentForm()
        # 获取这篇文章下的全部评论
        comment_list=self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# def archives(request,year,month):
#     post_list=Post.objects.filter(create_time__year=year,
#                                   create_time__month=month
#                                   ).order_by('-create_time')
#     return render(request,'blog/index.html',{'post_list':post_list})

class ArchivesView(IndexView):
    def get_queryset(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
                                                              create_time__month=month
                                                              )


# def category(request,pk):
#     cate=get_object_or_404(Category,pk=pk)
#     post_list=Post.objects.filter(category=cate).order_by('-create_time')
#     return render(request,'blog/index.html',{'post_list':post_list})

class CategoryView(IndexView):

    #覆写父类的get_queryset方法，因其默认获取全部列表数据
    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)