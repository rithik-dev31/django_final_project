from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from .models import Section, Post
from django.shortcuts import redirect
from .models import Post
from django.shortcuts import get_object_or_404


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        User.objects.create(username=username, password=password)
        messages.success(request, 'Account created! Please log in.')
        return redirect('signin')
    return render(request, 'login/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin123':
            return redirect('admin_page')

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    return render(request, 'login/signin.html')

def dashboard(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        sections = Section.objects.all()
        return render(request, 'login/dashboard.html', {'user': user, 'sections': sections})
    return redirect('signin')

def section_redirect_view(request):
    if request.method == 'POST':
        section_name = request.POST['section_name']
        return redirect('section_detail', section_name=section_name)

def image_detail(request, section_name):
    posts = Post.objects.filter(section__name__iexact=section_name)
    return render(request, 'login/section_detail.html', {
        'section_name': section_name,
        'posts': posts
    })

def section_detail_view(request, section_name):
    posts = Post.objects.filter(section__name__iexact=section_name)
    previous_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'login/section_detail.html', {
        'section_name': section_name,
        'posts': posts,
        'previous_url': previous_url
    })


def admin_page(request):
    if request.method == 'POST':
        section_id = request.POST['section']
        content_name = request.POST['content_name']
        description = request.POST['description']
        url = request.POST['url']
        image = request.FILES.get('image')

        section = Section.objects.get(id=section_id)

        Post.objects.create(
            section=section,
            content_name=content_name,
            description=description,
            url=url,
        )

        messages.success(request, 'Post added successfully!')
        return redirect('admin_page')  # Redirect to the same admin dashboard

    sections = Section.objects.all()
    return render(request, 'login/admin.html', {'sections': sections})



def add_section(request):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        section_image = request.FILES.get('section_image')  # ✅ handle image upload

        if section_name:
            Section.objects.create(name=section_name,image=section_image)
            messages.success(request, "Section added successfully!")
        else:
            messages.error(request, "Section name cannot be empty.")
    return redirect('admin_page')  # redirect back to admin dashboard

def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('signin')  # Redirect to login/signin page