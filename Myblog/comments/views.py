#coding=utf-8
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_comment(request,post_pk):
    #获取被评论的文章
    post=get_object_or_404(Post,pk=post_pk)

    if request.method=='POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form=CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment=form.save(commit=False)

            #将评论和文章关联
            comment.post=post
            comment.save()

            #重定向到post的详情页
            return redirect(post)

        else:
            '''
            数据不合法，重新渲染详情页，并且渲染表单的错误，
            post.comment_set.all() 方法，等价于 Comment.objects.filter(post=post)
            反向查询全部评论,获取这篇 post 下的的全部评论，
            '''
            comment_list=post.comment_set.all()
            context={'post':post,
                     'form':form,
                     'comment_list':comment_list
                     }
            return render(request,'blog/detail.html',context=context)

    #不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)


