from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import utils
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import models

class WomenHome(utils.DataMixin, ListView):
  template_name = 'women/index.html'
  context_object_name = 'posts'
  title_page = 'Главная страница'
  cat_selected = 0

  def get_queryset(self):
    return models.Women.published.all().select_related('cat')

@login_required
def about(request):
  contact_list = models.Women.published.all()
  paginator = Paginator(contact_list, 3)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  return render(request, 'women/about.html', {'title': 'О сайте', 'page_obj': page_obj})

class ShowPost(utils.DataMixin, DetailView):
  model = models.Women
  template_name = 'women/post.html'
  slug_url_kwarg = 'post_slug'
  context_object_name = 'post'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return self.get_mixin_context(context, title=context['post'].title)
  
  def get_object(self, queryset=None):
    return get_object_or_404(models.Women.published, slug=self.kwargs[self.slug_url_kwarg])

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, utils.DataMixin, CreateView):
  model = models.Women
  fields = '__all__'
  template_name = 'women/add_page.html'
  title_page = 'Добавить статью'
  permission_required = 'women.add_women'
  permission_denied_message = 'У вас нет прав для добавления постов'

class UpdatePage(PermissionRequiredMixin, utils.DataMixin, UpdateView):
  model = models.Women
  fields = ['title', 'content', 'photo', 'is_published', 'cat']
  template_name = 'women/add_page.html'
  title_page = 'Редактирование статьи'
  permission_required = 'women.change_women'
  success_url = reverse_lazy('home')

class DeletePage(PermissionRequiredMixin, utils.DataMixin, DeleteView):
  model = models.Women
  fields = ['title', 'content', 'photo', 'is_published']
  template_name = 'women/add_page.html'
  success_url = reverse_lazy('home')
  permission_required = 'women.delete_women'
  title_page = 'Удалить статью'

@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
  return HttpResponse(f"contact page") 

def login(request):
  return HttpResponse(f"login page") 

def bad_address_one(request):
  return HttpResponseRedirect(reverse('home'))

def bad_address_two(request):
  uri = reverse('cat_id', args=(5, ))
  return redirect(uri)

class WomenCategory(utils.DataMixin, ListView):
  template_name = 'women/index.html'
  context_object_name = 'posts'
  allow_empty = False

  def get_queryset(self):
    return models.Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    cat = context['posts'][0].cat
    return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)

def page_not_found(request, exception):
  return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class ShowTagPostList(utils.DataMixin, ListView):
  model = models.Women
  context_object_name = 'posts'
  template_name = 'women/index.html'
  allow_empty = False

  def get_queryset(self):
    return self.model.published.filter(tags__slug=self.kwargs.get('tag_slug', '')).select_related('cat')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    tag = models.TagPost.objects.get(slug=self.kwargs['tag_slug'])
    return self.get_mixin_context(context, title=f"Тег: {tag.tag}", cat_selected=None)
