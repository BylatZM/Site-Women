from django.urls import path, register_converter
from . import views
from women.views import page_not_found
from . import converters
from django.views import defaults

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
  path('', views.WomenHome.as_view(), name="home"),
  path('about/', views.about, name="about"),
  path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
  path('addpage/', views.AddPage.as_view(), name='addpage'),
  path('contact/', views.contact, name='contact'),
  path('login/', views.login, name='login'),
  path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name="category"),
  path('tag/<slug:tag_slug>', views.ShowTagPostList.as_view(), name="tag"),
  path('edit/<slug:slug>/', views.UpdatePage.as_view(), name="edit_page"),
  path('delete/<slug:slug>/', views.DeletePage.as_view(), name="delete_page")
]

defaults.page_not_found = page_not_found