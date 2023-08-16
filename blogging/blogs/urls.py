from django.urls import path, re_path
from . import views

urlpatterns = [
    path('home', views.HomeView.as_view(), name='home'),
    path('first', views.home, name='first'),
    path("blogs/<int:pk>", views.BlogPostDetailView.as_view(), name="blog_post_detail"),  # Use BlogPostDetailView
    path("blogs/newblog", views.NewBlogView.as_view(), name="add_new_blog"),
    path("blogs/categorized_blogs/<str:category>", views.CategorizedBlogsView.as_view(), name="categorized_blogs"),

    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    path('blogs/process_button_click', views.ProcessButtonClickView.as_view(), name='process_button_click'),
    path('like_comment/<int:comment>/<int:blog>/', views.LikeCommentView.as_view(), name='like_comment'),
    path('dislike_comment/<int:comment>/<int:blog>/', views.DislikeCommentView.as_view(), name='dislike_comment'),
    path('', views.RegisterView.as_view(), name='registration_form'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
