from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
	CreateView,
	DeleteView,
	DetailView,
	FormView,
	ListView,
	UpdateView,
)

from .forms import PostForm
from .models import Post


class PostListView(ListView):
	"""Homepage list of posts with search and pagination."""

	model = Post
	paginate_by = 6
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'

	def get_queryset(self):
		queryset = super().get_queryset().select_related('author')
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(
				Q(title__icontains=query) | Q(author__username__icontains=query)
			)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search_query'] = self.request.GET.get('q', '')
		return context


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'
	slug_field = 'slug'
	slug_url_kwarg = 'slug'


class AuthorRequiredMixin(UserPassesTestMixin):
	"""Allow authors or admins to modify a post."""

	raise_exception = True

	def test_func(self):
		post = self.get_object()
		return self.request.user.is_staff or post.author == self.request.user

	def handle_no_permission(self):
		messages.error(self.request, 'You do not have permission to modify this post.')
		return super().handle_no_permission()


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, 'Post created successfully!')
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'
	slug_field = 'slug'
	slug_url_kwarg = 'slug'

	def form_valid(self, form):
		messages.success(self.request, 'Post updated successfully!')
		return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
	model = Post
	template_name = 'blog/post_confirm_delete.html'
	slug_field = 'slug'
	slug_url_kwarg = 'slug'
	success_url = reverse_lazy('blog:post_list')

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, 'Post deleted successfully!')
		return super().delete(request, *args, **kwargs)


class MyPostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/my_posts.html'
	context_object_name = 'posts'
	paginate_by = 6

	def get_queryset(self):
		return (
			Post.objects.filter(author=self.request.user)
			.select_related('author')
			.order_by('-created_at')
		)


class RegisterView(FormView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('blog:post_list')

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		for field in form.fields.values():
			field.widget.attrs.update({'class': 'form-control'})
		return form

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		messages.success(self.request, 'Welcome aboard! Your account has been created.')
		return super().form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Please fix the errors below.')
		return super().form_invalid(form)
