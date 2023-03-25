from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

# Create your views here.
def test(request):
    context = {"test": "testing_django"}
    return render(request, "test.html", context)


@login_required(login_url="login")
def homepage(request):
    profile = request.user.profile
    blogs = BlogPost.objects.filter(author=profile.id)
    context = {"profile": profile, "blogs": blogs}
    return render(request, "homepage.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("login")
                else:
                    return redirect("homepage")

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def blogcomment_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.comment_author = request.user.profile
            comment.save()
            return redirect("blog/blogcomment.html", post_id=post_id)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(blog=post)
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "blog/blogcomment.html", context)


##maybe this will work????
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.comment_author.user:
        comment.delete()
    return redirect("blog/blogcomment.html", post_id=comment.blog.id)


@login_required
def view_post(request):
    foods = BlogPost.objects.all()
    return render(request, "blog/blogcomment.html", {"foods": foods})


def register_view(request):
    form = CustomUserCreatingForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            group = Group.objects.get(name="members")
            user.groups.add(group)
            Profile.objects.create(
                user=user,
                name=name,
                last_name=last_name,
                email=email,
            )
            messages.success(request, "Account successfully created for " + username)
            return redirect("login")
        else:
            messages.info(request, "Passwords did not match")
    context = {"form": form}
    return render(request, "register.html", context)


def filter_results(request):
    category = request.GET.get("category")
    posts = BlogPost.objects.filter(category=category)
    context = {"posts": posts, "category": category}
    return render(request, "filterresults.html", context)


@login_required
def search_posts(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            posts = BlogPost.objects.filter(Title__icontains=query)
            context = {"posts": posts, "form": form}
            return render(request, "search_results.html", context)
    else:
        form = SearchForm()
    context = {"form": form}
    return render(request, "search.html", context)


@login_required
def myblogposts(request):
    user = request.user
    my_posts = BlogPost.objects.filter(author=user.profile)
    context = {"my_posts": my_posts}
    return render(request, "blog/my_blog_posts.html", context)
