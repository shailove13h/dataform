from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Post, Category, PostLike
from django.http import JsonResponse
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ip_address = get_client_ip(request)
    if not PostLike.objects.filter(post=post, ip_address=ip_address).exists():
        post.likes += 1
        post.save()
        PostLike.objects.create(post=post, ip_address=ip_address)
    return JsonResponse({'likes': post.likes})



def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug,category_slug=category_slug )
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'blog/category.html', {'category': category, 'posts': posts})

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts': posts, 'query': query})