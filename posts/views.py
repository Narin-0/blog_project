from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Post

# Смеситель (Mixin) для проверки прав автора или админа
class OwnerOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_staff

# 1. Список и Детализация (Доступно всем)
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

# 2. Создание (Только авторизованные)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 3. Редактирование и Удаление (Автор или Админ)
class PostUpdateView(LoginRequiredMixin, OwnerOrAdminRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(LoginRequiredMixin, OwnerOrAdminRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})