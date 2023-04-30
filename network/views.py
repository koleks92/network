from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator

import json

from .models import User, Post, Follow


def index(request):
    # Check if logged in
    logged_in = False
    if request.user.is_authenticated:
        logged_in = True

    posts = Post.objects.all()
    posts = posts.order_by("-date").all()

    # Show only 10 post at one page
    paginator = Paginator(posts, 10)

    # Get Page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "logged_in": logged_in, 
    })
   

def profile(request, user):
    # Get user
    user = get_object_or_404(User, username=user)

    # Get user posts
    try:
        posts = Post.objects.filter(user = user)
        posts = posts.order_by("-date").all()

        # Show only 10 post at one page
        paginator = Paginator(posts, 10)

        # Get Page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = False

    # Get number of users that follow this profile
    try:
        user_followers = len(Follow.objects.filter(followed_users = user))
    except:
        user_followers = 0

    # Get number of users that are followed by this profile
    try:
        user_follows = len(Follow.objects.get(user = user).followed_users.all())
    except:
        user_follows = 0

    # Get if current user is watching the page !
    current_user = False
    if user.username == str(request.user):
        current_user = True

    # Check if logged in
    logged_in = False
    if request.user.is_authenticated:
        logged_in = True

    return render(request, "network/profile.html",{
        "user_name": user.username,
        "page_obj": page_obj,
        "user_follows": user_follows,
        "user_followers": user_followers,
        "current_user": current_user,
        "logged_in": logged_in
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@csrf_exempt
@login_required
def create_post(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    # Check post
    data = json.loads(request.body)

    # Get post text
    post_body = data.get("body", "")

    # Create post
    p = Post(body = post_body, user = request.user)
    p.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

@csrf_exempt
@login_required
def follow_unfollow(request, user_name):
    user_2_follow = get_object_or_404(User, username=user_name)

    if request.method == "GET":
        if Follow.objects.filter(user=request.user, followed_users=user_2_follow).exists():
            message = "Followed"
        else:
            message = "Unfollowed"

        return JsonResponse({"message": message}, status=200)
    
    # Check if PUT
    if request.method == "PUT":
        
        if Follow.objects.filter(user=request.user, followed_users=user_2_follow).exists():
            # Unfollow the user
            follow = Follow.objects.get(user=request.user)
            follow.followed_users.remove(user_2_follow)
            message = "Unfollowed"
        else:
            # Follow the user
            follow, created = Follow.objects.get_or_create(user=request.user)
            follow.followed_users.add(user_2_follow)
            message = "Followed"

        return JsonResponse({"message": message}, status=200)
    
@login_required
def following(request):
    # Get user's follows
    try:
        user = Follow.objects.get(user = request.user)
        followed_users = user.followed_users.all()
        posts = Post.objects.filter(user__in=followed_users)
        posts = posts.order_by("-date").all()

        # Show only 10 post at one page
        paginator = Paginator(posts, 10)

        # Get Page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        return render(request, "network/following.html", {
            "page_obj": page_obj,
            "logged_in": True
        })
    except:
        return render(request, "network/error.html", {
            "title": "Following",
            "message": "There's been an error! Please try again!"
        })
    
@csrf_exempt    
@login_required
def edit(request, post_id):
    try:
        if request.method == "POST":
            # Get post
            post = Post.objects.get(id = post_id)

            # Check if post user is actually logges in user
            if post.user != request.user:
                return render(request, "network/error.html", {
                "title": "Edit",
                "message": "You are not allowed to change this post !"
                })

            # Get data
            data = json.loads(request.body)

            # Get post text
            edit_body = data.get("body", "")

            post.body = edit_body
            post.save()
         
            return JsonResponse({"message": "Edit sucessful"}, status=200)

    except:
        return render(request, "network/error.html", {
            "title": "Edit",
            "message": "There's been an error. Please try again !"
        })

@csrf_exempt
def likes(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    try:
        if request.method == "GET":
            num_of_likes = len(post.likes.all())
            liked = False

            if request.user.is_authenticated and post.likes.filter(username = request.user).exists():
                liked = True

            response_data = {"num_of_likes": num_of_likes,
                            "liked": liked}
            
            return JsonResponse(response_data)
                
        if request.method == "PUT" and request.user.is_authenticated:
            if post.likes.filter(username = request.user).exists():
                post.likes.remove(request.user)
                return JsonResponse({"message": "Unliked"})
            else:
                post.likes.add(request.user)
                return JsonResponse({"message": "Liked"})
            
    except:
        return render(request, "network/error.html", {
            "title": "Like",
            "message": "There's been an error. Please try again !"
        })



