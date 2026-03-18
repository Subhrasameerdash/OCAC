import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import PostForm
from .models import Comment, Like, Post


# ── Feed ──────────────────────────────────────────────────────────────
class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 20


# ── Create Post ───────────────────────────────────────────────────────
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Auto-detect post type
        if form.cleaned_data.get('media'):
            form.instance.post_type = 'media'
        else:
            form.instance.post_type = 'thought'
        return super().form_valid(form)


# ── Post Detail ───────────────────────────────────────────────────────
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


# ── Delete Post ───────────────────────────────────────────────────────
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('feed')

    def get_queryset(self):
        # Only allow the author to delete their own posts
        return super().get_queryset().filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        # Skip confirmation template — delete immediately on GET too
        return self.delete(request, *args, **kwargs)


# ── Toggle Like (AJAX) ───────────────────────────────────────────────
@login_required
def toggle_like(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.like_count(),
    })


# ── Add Comment (AJAX) ───────────────────────────────────────────────
@login_required
def add_comment(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    post = get_object_or_404(Post, pk=pk)

    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
    except json.JSONDecodeError:
        text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

    comment = Comment.objects.create(author=request.user, post=post, text=text)

    return JsonResponse({
        'id': comment.pk,
        'author': comment.author.username,
        'author_pic': comment.author.profile_pic.url if comment.author.profile_pic else '',
        'text': comment.text,
        'created_at': comment.created_at.strftime('%b %d, %Y'),
        'comment_count': post.comment_count(),
    })
