from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.forms import *

# Create your views here.
def test(request):
    context = {"test": "testing_django"}
    return render(request, "test.html", context)


def homepage(request):
    return render(request, "homepage.html")


@login_required
def blogpost_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.comment_author = request.user.profile
            comment.save()
            return redirect("blogpost_detail", post_id=post_id)
    else:
        form = CommentForm()
    comments = Comment.objects.filter(blog=post)
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "blog/blogpost_detail.html", context)


##maybe this will work????
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.comment_author.user:
        comment.delete()
    return redirect("blogpost_detail", post_id=comment.blog.id)
