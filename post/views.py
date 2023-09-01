from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Tag, Stream, Follow, Post, Likes
from django.contrib.auth.decorators import login_required
from .forms import NewPostForm
from django.urls import reverse
from userauths.models import Profile
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    all_user = User.objects.all()
    profile = Profile.objects.all()
    gropu_ids = []
    for post in posts:
        gropu_ids.append(post.id)
    post_items = Stream.objects.filter(id__in=gropu_ids).all()
    return render(request, 'index.html', {'post_items': post_items, 'all_user': all_user, 'profile':profile})


def NewPost(request):
    user = request.user.id
    tags_objs = []
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list = list(tag_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
        return render(request, 'newpost.html', {'form': form})


def Postdetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # comments

    comments = Comment.objects.filter(post=post).order_by('-date')
    #print(comments[0].post)

    # comment form
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('postdetail', args=[post_id]))
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post,
        'comments': comments,
    }

    return render(request, 'post-details.html', context)


def PostLikes(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    print(post)
    current_like = post.likes
    liked = Likes.objects.filter(user=user, post=post)
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_like += 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_like -= 1
    post.likes = current_like
    print(post.likes)
    post.save()
    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))


def Favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('postdetail', args=[post_id]))
