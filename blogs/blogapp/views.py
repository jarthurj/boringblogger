from django.shortcuts import render,redirect,get_object_or_404
from .models import Post, Comment
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy,reverse

class Dashboard(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blogapp/postlist.html'
    paginate_by = 1
    ordering = ["-created_at"]

    def get_queryset(self):
        return Post.objects.all()

class NewPost(LoginRequiredMixin,View):
    def get(self,request):
        form = PostForm()
        return render(request, "blogapp/newpost.html",{"form":form})
    
    def post(self,request):
        form = PostForm(request.POST)
        messages.success(request, "Post created!")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("dashboard")
        return render(request, "blogapp/newpost.html",{"form":form})

class PostList(ListView):
    model = Post
    template_name = 'blogapp/postlist.html'
    paginate_by = 1
    ordering = ["-created_at"]

class DeletePost(LoginRequiredMixin,DeleteView,UserPassesTestMixin):
    model = Post
    success_url = reverse_lazy('dashboard')
    raise_exception = True

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Post deleted!")
        return super().form_valid(form)

class EditPost(LoginRequiredMixin,View):
    def get(self,request,pk):
        post = get_object_or_404(Post, id=pk, author=request.user)
        form = PostForm(instance=post)
        return render(request, "blogapp/newpost.html",{"form":form})
    
    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk, author=request.user)
        form = PostForm(request.POST,instance=post)
        messages.success(request, "Post created!")
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("dashboard")
        return render(request, "blogapp/newpost.html",{"form":form})
    
class NewComment(LoginRequiredMixin,View):
    def get(self,request,pk):
        form = CommentForm()
        context = {
            "form":form,
            "post":Post.objects.get(id=pk),
            }
        return render(request,"blogapp/newcomment.html",context)

    def post(self,request,pk):
        form = CommentForm(request.POST)
        messages.success(request,"Comment Created!")
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(id=pk)
            comment.save()
            return redirect('dashboard')
