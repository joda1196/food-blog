from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from app.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import *
from .filters import *

# Create your views here.


@login_required(login_url="login")
def homepage(request):
    profile = request.user.profile
    blogs = BlogPost.objects.filter(author=profile.id)
    context = {"profile": profile, "blogs": blogs}
    return render(request, "homepage.html", context)


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                messages.info(request, "Username or Password is incorrect")

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


@admin_only
def deleteMember(request, pk):
    member = Profile.objects.get(id=pk)
    user = User.objects.get(id=member.user.id)
    if request.method == "POST":
        user.delete()
        return redirect("login")
    context = {"member": member}
    return render(request, "delete.html", context)


def filter_results(request):
    category = request.GET.get("category")
    posts = BlogPost.objects.filter(category=category)
    context = {"posts": posts, "category": category}
    return render(request, "filterresults.html", context)


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


@login_required
def create_my_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user.profile
            blog_post.save()

            return redirect("detail", pk=blog_post.pk)
    else:
        form = BlogPostForm()
    return render(request, "blog/createblog.html", {"form": form})


##once the function above passes and saves it should redirect to this function where it will display what you created
##sending in pk as the argument manually from the code
##fingers crossed


def blog_detail(request, pk):
    blog_post = BlogPost.objects.get(id=pk)
    return render(request, "blog/blogdetail.html", {"blog_post": blog_post})


@admin_only
def view_members(request):
    members = Profile.objects.all()
    total_members = Profile.objects.count()
    mem_filter = MemberFilter(request.GET, queryset=members)
    members = mem_filter.qs
    context = {
        "members": members,
        "total_members": total_members,
        "mem_filter": mem_filter,
    }
    return render(request, "members/members.html", context)


@login_required
def blog_detail(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    return render(request, "blog/blogdetail.html", {"blog_post": blog_post})


@login_required
def my_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, "blog/myProfile.html", {"user_profile": user_profile})


@login_required
def updateprofile(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("my profile")
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, "blog/updateProfile.html", {"form": form})
