from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Post
from .forms import PostForm, CommentForm

# Create your views here.


def index(request):
    post = Post.objects.filter(published_date__isnull=False)
    context = {'post': post}
    return render(request, 'blogpost/post.html', context)


@login_required(login_url='login')
def draft_post(request):
    if request.user.is_authenticated:
        user = request.user
        post = Post.objects.filter(author__user=user).filter(
            published_date__isnull=True)
        context = {'post': post}
        return render(request, 'blogpost/post.html', context)


def detail_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user != post.author.user:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.author = request.user
                    comment.save()
                    messages.success(request, 'Comment posted')
                    return redirect('detail_post', pk=pk)
            else:
                messages.error(request, "You can't comment on your post")
    context = {'post': post, 'form': form}
    return render(request, 'blogpost/post_detail.html', context)


@login_required(login_url='login')
def create_post(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        form = PostForm()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = profile
                post.save()
                messages.success(request, 'Post Created')
                return redirect('index')
        context = {'form': form}
        return render(request, 'blogpost/create_post.html', context)


@login_required(login_url='login')
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=post)
    if request.method == "POST":
        if request.user == post.author.user:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post updated')
                return redirect('detail_post', pk=pk)
        else:
            messages.error(request, "you can't edit others post")
    context = {'form': form}
    return render(request, 'blogpost/create_post.html', context)


@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author.user:
        post.delete()
        messages.success(request, 'Post deleted')
    else:
        messages.error(request, "you can't delete others post")
    return redirect('index')


@login_required(login_url='login')
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author.user:
        post.publish()
        messages.success(request, 'Post Published')
    else:
        messages.error(request, "you can't publish others post")
    return redirect('index')


@login_required(login_url='login')
def comment_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.user != post.author.user:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment posted')
                return redirect('detail_post', pk=pk)
    else:
        messages.error(request, "You can't comment on your post")
    context = {'form': form}
    return render(request, 'blogpost/comment_form.html', context)


@login_required(login_url='login')
def comment_approve(request, pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=pk)
    if user == comment.post.author.user:
        comment.approve()
        messages.success(request, 'Comment approved')
    else:
        messages.error(request, "you can't approve other's comment")
    return redirect('detail_post', comment.post.id)


@login_required(login_url='login')
def comment_delete(request, pk):
    if request.user.is_authenticated:
        user = request.user
        comment = get_object_or_404(Comment, pk=pk)
        post_id = comment.post.id
        print(user, comment.author)
        if user == comment.post.author.user:
            comment.delete()
            messages.success(request, 'Comment deleted')
        else:
            messages.error(request, "you can't delete other's comment")
    return redirect('detail_post', pk=post_id)
