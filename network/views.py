from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-date").all()

    return render(request, "network/index.html", {
        "posts": posts,
        "likes": 0
    })
   

def profile(request, user):
    # Get user
    user = get_object_or_404(User, username=user)

    # Get user posts
    try:
        posts = Post.objects.filter(user = user)
        posts = posts.order_by("-date").all()
    except:
        posts = False

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

    # Check if profile page is currently loggedin user
    current_user = False
    if user.username == str(request.user):
        current_user = True


    return render(request, "network/profile.html",{
        "user_name": user.username,
        "user_posts": posts,
        "user_follows": user_follows,
        "user_followers": user_followers,
        "current_user": current_user,
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
