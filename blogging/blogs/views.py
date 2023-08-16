from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, permissions

from . import serializers
from .models import BlogPost, UserProfile, Comment, CommentReaction
from .forms import CommentForm, RegistrationForm
from .serializers import BlogPostSerializer


class NewBlogView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_superuser:
            # return redirect('HomeView')
            return Response(template_name='addblog.html')

        else:

            # context = {}
            return Response(template_name='addblog.html')

    def post(self, request):
        if request.user.is_superuser:
            return redirect('HomeView')
        else:
            try:
                serializer = serializers.StudentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    messages.add_message(request, messages.INFO, f'blog added successfully')
                    return redirect('HomeView')
            except:
                messages.add_message(request, messages.WARNING, f"An error occurred. Please try again.")
                return redirect('HomeView')


class UserLoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_superuser:
            # return redirect('HomeView')
            return Response(template_name='login.html')
        else:
            # context = {}
            return Response(template_name='login.html')

    def post(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, "You are already logged in.")
            return redirect('first')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Welcome! You have logged in successfully.")
            return redirect('first')
        else:
            pass
        return Response(template_name='login.html')


class LikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get_comment_and_blog(self, comment_id, blog_id):
        return get_object_or_404(BlogPost, pk=blog_id).comments.filter(pk=comment_id).first()

    def post(self, request, comment, blog):
        comment_obj = self.get_comment_and_blog(comment, blog)

        if not CommentReaction.objects.filter(user=request.user, comment=comment_obj).exists():
            CommentReaction.objects.create(user=request.user, comment=comment_obj, reaction=True)
            comment_obj.likes += 1
            comment_obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DislikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_comment_and_blog(self, comment_id, blog_id):
        return get_object_or_404(BlogPost, pk=blog_id).comments.filter(pk=comment_id).first()

    def post(self, request, comment, blog):
        comment_obj = self.get_comment_and_blog(comment, blog)

        if not CommentReaction.objects.filter(user=request.user, comment=comment_obj, reaction=False).exists():
            CommentReaction.objects.create(user=request.user, comment=comment_obj, reaction=False)
            comment_obj.dislikes += 1
            comment_obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    # renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "You have logged out successfully.")
        return redirect('login')


class RegisterView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_superuser:
            print('hello world')
            form = RegistrationForm()
            print(form)
            # return redirect('HomeView')
            return Response({"form": form}, template_name='register.html')

        else:
            print('hello world')
            form = RegistrationForm()
            print(form)
            # context = {}
            return Response({"form": form}, template_name='register.html')

    def post(self, request):
        form = RegistrationForm(request.data)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            fname = form.cleaned_data["fname"]
            lname = form.cleaned_data["lname"]
            user_exists = UserProfile.objects.filter(email=email).exists()

            if not user_exists:
                new_user = User.objects.create_user(
                    first_name=fname, last_name=lname, username=email, email=email,
                    password=password, is_active=True
                )
                UserProfile.objects.create(fname=fname, lname=lname, password=password, email=email)

                messages.add_message(request, messages.SUCCESS, "Congratulations! Your account has been created.")
                return Response(template_name='login.html', status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User with this email already exists."}, template_name='login.html',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": form.errors}, template_name='login.html', status=status.HTTP_400_BAD_REQUEST)


class BlogPostDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        form = CommentForm()
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        user_id = user
        user = get_object_or_404(UserProfile, email=user_id)
        username = user.fname
        comments = blog_post.comments.all()
        serializer = BlogPostSerializer(blog_post)
        # return render(request, 'blog.html', )
        context = {'blog': blog_post, 'form': form, 'comments': comments, "username": username}
        return Response(context, serializer.data, template_name='blog.html')

    def post(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)
        form = CommentForm(request.data)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.author = request.user.userprofile.fname
            comment.save()
            messages.add_message(request, messages.SUCCESS, "You have added a new comment.")
            # return Response(status=status.HTTP_201_CREATED)
            return redirect('home')
        else:
            return Response({"error": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class HomeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, email=request.user)
        blogs = BlogPost.objects.all()
        return render(request, 'home.html', {'blogs': blogs, "username": user_profile.fname})


@login_required(login_url='login')
def home(request):
    if request.user.is_superuser:
        return redirect('first')
    else:
        print('hello')
        user_id = request.user
        print(user_id)
        user = get_object_or_404(UserProfile, email=user_id)
        username = user.fname
        blogs = BlogPost.objects.all()
        return render(request, 'home.html', {'blogs': blogs, "username": username})


class CategorizedBlogsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category):
        user_profile = get_object_or_404(UserProfile, email=request.user)
        blogs = BlogPost.objects.filter(blog_category=category)
        return render(request, 'home.html', {'blogs': blogs, "username": user_profile.fname, "category": category})


class ProcessButtonClickView(APIView):
    def post(self, request):
        blog = request.data.get('blog', '')
        comment = request.data.get('comment', '')

        if 'like' in request.data:
            return redirect('like_comment', comment=comment, blog=blog)
        elif 'dislike' in request.data:
            return redirect('dislike_comment', comment=comment, blog=blog)
        else:
            return redirect('login')
