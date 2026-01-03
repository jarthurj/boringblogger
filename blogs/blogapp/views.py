from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    context={
        'posts':posts
    }
    return render(request, "blogapp/dashboard.html", context)

@login_required
def newpost(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("dashboard")
    else:
        form = PostForm()
    return render(request, "blogapp/newpost.html",{"form":form})



# def viewpost(request,pk):
#     return render(request,"blogapp/viewpost.html",{"post":Post.objects.get(id=pk)})


def postlist(request):
    posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'blogapp/postlist.html',{'page_obj':page_obj})


def home(request):
    return render(request, "blogapp/home.html", {"posts":Post.objects.all()})