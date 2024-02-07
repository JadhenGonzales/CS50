import json

from django.contrib.auth import authenticate, decorators, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post
from .forms import PostForm


def index(request):
    return render(request, "network/index.html", {
        "form": PostForm
    })


@decorators.login_required
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


@decorators.login_required
def like_post(request):
    # Liking a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check for post ID and like status
    data = json.loads(request.body)
    post_id = data.get("post_id")
    like_status = data.get("like_status")
    if post_id is None or like_status is None:
        return JsonResponse({"error": "Incomplete submission"}, status=400)
    
    # Check if target post exists
    try:
        target_post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist."}, status=400)
    
    # Check if user does not own the post
    if target_post.owner == request.user.profile:
        return JsonResponse({"error": "Cannot like own post."}, status=400)
    
    # Like or Unlike post
    if like_status:
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
