from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from post.models import Post, Follow, Stream
from django.core.paginator import Paginator
from django.db import transaction
from .forms import EditProfileForm, UserRegisterationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.

def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()

    post_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts_paginator': posts_paginator,
        'profile': profile,
        'posts': posts,
        'url_name': url_name,
        'post_count': post_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status,
    }

    return render(request, 'profile.html', context)


def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.filter(user=following)
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, following=following, date=post.posted)
                    stream.save()

        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


def editProfile(request):
    user = request.user

    profile = Profile.objects.get(user=user)
    # print(profile.first_name)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.image = form.cleaned_data.get('image')
            profile.save()
            return redirect('profile', profile.user)
    else:
        form = EditProfileForm()
        return render(request, 'edit-profile.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hurray! {username} your account has been created')

            # automatically log in the user

            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('editprofile')
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterationForm()
        context = {
                'form': form,
            }
        return render(request, 'sign-up.html', context)
