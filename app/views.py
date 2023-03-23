from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def test(request):
    context = {"test": "testing_django"}
    return render(request, "test.html", context)


def homepage(request):
    return render(request, "homepage.html")


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
                    return redirect("superuser")
                else:
                    return redirect("user")

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
