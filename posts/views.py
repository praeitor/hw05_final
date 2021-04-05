from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse


from posts.models import Post, Group, Follow
from posts.forms import PostForm, CommentForm
from yatube.settings import POSTS_ON_PAGE


User = get_user_model()


def index(request):
    latest = Post.objects.all()[:10]
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'posts': latest, 'page': page}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'posts': posts, 'page': page}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'newpost.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user,
            author__username=username,
        ).exists()
    else:
        following = False
    following_count = Follow.objects.filter(user=request.user).count()
    followers_count = Follow.objects.filter(author=request.user).count()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'posts': posts,
        'page': page,
        'following': following,
        'following_count': following_count,
        'followers_count': followers_count
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    profile = get_object_or_404(User, username=username)
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'profile': profile,
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'post.html', context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        form.save()
    return redirect(
        'post',
        username=username,
        post_id=post_id
    )


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != post.author:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse(
                'post',
                kwargs={'username': username, 'post_id': post_id})
            )
    return render(
        request,
        'newpost.html',
        {'form': form, 'post': post, 'is_edit': True}
    )


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'follow.html', context)


@login_required
def profile_follow(request, username):
    follow_user = get_object_or_404(User, username=username)
    if request.user != follow_user:
        Follow.objects.get_or_create(user=request.user, author=follow_user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    get_object_or_404(
        Follow,
        user=request.user,
        author=unfollow_user
    ).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
