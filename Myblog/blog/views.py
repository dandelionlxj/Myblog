#coding:utf-8
import markdown
from django.shortcuts import render,HttpResponse,get_object_or_404
from . models import Post ,Category,Tag
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

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
    #指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 1

    def get_context_data(self,**kwargs):
        #首先获得父类生成的传递给模板的字典
        context =super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page=context.get('page_obj')
        is_paginated = context.get('is_paginated')

        #调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self,paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left=[]
        right=[]
        left_has_more=False
        right_has_more=False

        #如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        first=False
        last=False

        #获得用户当前请求的页码号
        page_number=page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        #获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number==1:
            right=page_range[page_number:page_number+2]

            #如果最右边的页码号比最后一页的页码号减去 1 还要小，说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，
            if right[-1]<total_pages-1:
                right_has_more=True
            if right[-1] < total_pages:
                last = True

        elif page_number ==total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            #是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data




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
        md=markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite', #语法高亮拓展
            TocExtension(slugify=slugify),
        ])
        post.body=md.convert(post.body)
        post.toc=md.toc
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


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=tag)