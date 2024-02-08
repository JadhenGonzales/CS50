import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Profile, Post
from .forms import PostForm
from .utilities import check_json


def index(request):
    return render(request, "network/index.html", {
        "form": PostForm
    })


@login_required
def create_post(request):
    # Creating a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    #Check form validity and save post
    form = PostForm(request.POST)
    if form.is_valid():
        c_form = form.cleaned_data
        new_post = Post(
            owner=request.user.profile,
            text=c_form["post_content"],
        )
        new_post.save()
        return JsonResponse({"message": "Post sent successfully"}, status=201)
    else:
        return JsonResponse({"error": "Invalid form content"}, status=400)


@login_required
def edit_post(request):
    # Following someone must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check JSON data
    clean_data, message = check_json(request.body)
    if not clean_data:
        return JsonResponse({"error": message}, status=400)

    target_post = clean_data['target']
    new_text = clean_data['text']
    
    # Check if user owns the post
    if target_post.owner != request.user.profile:
        return JsonResponse({"error": "Cannot edit others posts."}, status=400)
    
    target_post.text = new_text
    target_post.save()
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def follow_profile(request):
    # Following someone must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check JSON data
    clean_data, message = check_json(request.body)
    if not clean_data:
        return JsonResponse({"error": message}, status=400)

    target_profile = clean_data['target']
    follow = clean_data['modifier']
    
    # Check if user does not own the profile
    if target_profile == request.user.profile:
        return JsonResponse({"error": "Cannot follow yourself."}, status=400)

    # Follow or Unfollow target_profile
    if follow:
        target_profile.followers.add(request.user.profile)
        message = "Followed."
    elif request.user.profile in target_profile.followers.all():
        target_profile.followers.remove(request.user.profile)
        message = "Unfollowed."
    else:
        message = "No changes."
    
    target_profile.save()
    return JsonResponse({"message": message}, status=200)

@login_required
def like_post(request):
    # Liking a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check JSON data
    clean_data, message = check_json(request.body)
    if not clean_data:
        return JsonResponse({"error": message}, status=400)

    target_post = clean_data['target']
    like = clean_data['modifier']
    
    # Check if user does not own the post
    if target_post.owner == request.user.profile:
        return JsonResponse({"error": "Cannot like own post."}, status=400)
    
    # Like or Unlike post
    if like:
        target_post.likes.add(request.user.profile)
        message = "Like added."
    elif request.user.profile in target_post.likes.all():
        target_post.likes.remove(request.user.profile)
        message = "Like removed."
    else:
        message = "No changes."
    
    target_post.save()
    return JsonResponse({"message": message}, status=200)
    

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
