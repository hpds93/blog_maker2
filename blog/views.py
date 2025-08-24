from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Blog
from .forms import PostForm, BlogForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    """The home page for Blog Maker."""
    return render(request, 'blog/index.html')


@login_required
def my_blogs(request):
    """Show all user's blogs."""
    blogs = Blog.objects.filter(user=request.user).order_by('date_added')
    context = {'blogs':blogs}
    return render(request, 'blog/my_blogs.html', context)


@login_required
def new_blog(request):
    """Makes a new blog."""
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect("blog:my_blogs")
        
    context = {"form": form}
    return render(request, "blog/new_blog.html", context)


@login_required
def edit_blog(request, blog_id):
    """Edit an existing blog."""

    blog = get_object_or_404(Blog, id=blog_id)

    if request.user != blog.user:
        raise Http404

    if request.method != 'POST':
        form = BlogForm(instance=blog)
    else:        
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:my_blogs')
        
    context = {'form': form,
               'blog_id': blog_id}

    return render(request, 'blog/edit_blog.html', context)


@login_required
def posts(request, blog_id): # o q acontece se usuário tentar POST? # testar! #
    """Show all blog's posts."""

    blog = get_object_or_404(Blog, id=blog_id)

    if request.user != blog.user:
        raise Http404
    
    context = {'posts': blog.post_set.all().order_by('date_added'),
               'blog': blog}
    
    return render(request, 'blog/posts.html', context)


@login_required
def new_post(request, blog_id):
    """Create a new post."""
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user != blog.user:
        raise Http404
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            post.save()
            return redirect("blog:posts", blog_id=blog_id)
        
    context = {"form": form,
               "blog_id": blog_id}  
    
    return render(request, "blog/new_post.html", context)


@login_required
def edit_post(request, post_id):
    """Edit an existing post."""

    post = get_object_or_404(Post, id=post_id)

    if request.user != post.blog.user:
        raise Http404
    
    blog_id = post.blog.id

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        # Test if user owns the post's blog.
        if request.user != post.blog.user: # NOT TESTED YET [need lear to make post requests with test client]
            raise Http404
        
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:posts', blog_id=blog_id) # order by last activity?    
        
    context = {'form': form, 'post_id': post_id}

    return render(request, 'blog/edit_post.html', context)
