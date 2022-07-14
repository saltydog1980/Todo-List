from django.urls import path
from . import views

#namespace so I can use todos:name in my pages and views, example 'todos:signup'
app_name = 'todos'
urlpatterns = [
    path('', views.redir, name='redir'),
    path('todos', views.index, name='todos'),
    path('todos/new', views.new, name='new'),
    path('todos/<int:id>', views.see_item, name='see_item'),
    path('todos/<int:id>/edit', views.edit, name='edit'),
    path('todos/<int:id>/delete', views.delete, name='delete'),
    path('todos/signup', views.sign_up, name='signup'),
    path('todos/signout', views.sign_out, name='signout'),
    path('todos/login', views.log_in, name='login'),
]
