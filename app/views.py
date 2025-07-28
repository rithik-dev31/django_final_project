from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

from .models import (
    UserProfile,  # ✅ Custom user model
    Section,
    Post,
    Community,
    ChatMessage,
)

from .forms import UserProfileForm


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        UserProfile.objects.create(username=username, email=email, password=password)
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
            user = UserProfile.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    return render(request, 'login/signin.html')


def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('signin')

    sections = Section.objects.all()
    communities = Community.objects.select_related('section').prefetch_related('members')

    context = {
        'user': user,
        'sections': sections,
        'communities': communities,
    }
    return render(request, 'user_module/dashboard.html', context)


def section_redirect_view(request):
    if request.method == 'POST':
        section_name = request.POST['section_name']
        return redirect('section_detail', section_name=section_name)


def image_detail(request, section_name):
    posts = Post.objects.filter(section__name__iexact=section_name)
    return render(request, 'user_module/section_detail.html', {
        'section_name': section_name,
        'posts': posts
    })


def section_detail_view(request, section_name):
    posts = Post.objects.filter(section__name__iexact=section_name)
    previous_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'user_module/section_detail.html', {
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
        return redirect('admin_page')

    posts = Post.objects.select_related('section').all()
    sections = Section.objects.all()
    return render(request, 'login/admin.html', {'sections': sections, 'posts': posts})


def add_section(request):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        section_image = request.FILES.get('section_image')

        if section_name:
            Section.objects.create(name=section_name, image=section_image)
            messages.success(request, "Section added successfully!")
        else:
            messages.error(request, "Section name cannot be empty.")
    return redirect('admin_page')


def logout_view(request):
    request.session.flush()
    return redirect('signin')


def profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('signin')

    edit_mode = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')
        bio = request.POST.get('bio')
        name = request.POST.get('name')

        user.name = name
        user.username = username
        user.email = email
        user.bio = bio
        if profile_image:
            user.profile_image = profile_image
        user.save()

        return redirect('profile')

    return render(request, 'user_module/profile.html', {
        'user': user,
        'edit_mode': edit_mode,
    })


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('admin_page')


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.content_name = request.POST['content_name']
        post.description = request.POST['description']
        post.url = request.POST['url']
        post.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('admin_page')
    return render(request, 'login/edit_post.html', {'post': post})


def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        section_image = request.FILES.get('section_image')

        if section_name:
            section.name = section_name
        if section_image:
            section.image = section_image

        section.save()
        messages.success(request, "Section updated successfully!")
        return redirect('admin_page')

    return render(request, 'login/edit_section.html', {'section': section})


def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    section.delete()
    messages.success(request, "Section and its related posts deleted successfully.")
    return redirect('admin_page')


def join_community(request, section_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')
    user = UserProfile.objects.get(id=user_id)

    section = Section.objects.get(id=section_id)
    community, created = Community.objects.get_or_create(section=section)

    community.members.add(user)
    community.save()

    return redirect('dashboard')


def leave_community(request, section_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in to leave a community.")
        return redirect('signin')

    user = get_object_or_404(UserProfile, id=user_id)
    section = get_object_or_404(Section, id=section_id)
    community = get_object_or_404(Community, section=section)

    community.members.remove(user)
    messages.success(request, f"You have left the community for {section.name}.")

    return redirect('dashboard')


def community_chat(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    community = get_object_or_404(Community, section=section)

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signin')

    user = get_object_or_404(UserProfile, id=user_id)

    messages = ChatMessage.objects.filter(section=section).order_by('timestamp')

    context = {
        'section': section,
        'community': community,
        'user': user,
        'messages': messages,
    }
    return render(request, 'user_module/community_chat.html', context)
