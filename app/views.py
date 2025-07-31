from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http import JsonResponse

from .models import (
    UserProfile,  # ✅ Custom user model
    Section,
    Post,
    Community,
    ChatMessage,
    JobOpening,
    Repolink,
    Feedback
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

from .models import Post, JobOpening, Section

def admin_page(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'post':
            section_id = request.POST['section']
            content_name = request.POST['content_name']
            description = request.POST['description']
            url = request.POST['url']
        

            section = Section.objects.get(id=section_id)

            Post.objects.create(
                section=section,
                content_name=content_name,
                description=description,
                url=url,
            
            )
            messages.success(request, 'Post added successfully!')

        elif form_type == 'job_opening':
            section_id = request.POST['section']
            content_name = request.POST['content_name']
            description = request.POST['description']
            url = request.POST['url']

            section = Section.objects.get(id=section_id)

            JobOpening.objects.create(
                section=section,
                content_name=content_name,
                description=description,
                url=url
            )
            messages.success(request, 'Job opening added successfully!')

        elif form_type == 'repo_link':
            section_id = request.POST['section']
            repo_name = request.POST['repo_name']
            description = request.POST['description']
            repo_url = request.POST['repo_url']

            section = Section.objects.get(id=section_id)

            Repolink.objects.create(
                section=section,
                repo_name=repo_name,
                description=description,
                repo_url=repo_url
            )
            messages.success(request, 'Repo link added successfully!')

        return redirect('admin_page')

    posts = Post.objects.select_related('section').all()
    job_openings = JobOpening.objects.select_related('section').all()
    sections = Section.objects.all()
    repositories = Repolink.objects.select_related('section').all()
    feedback= Feedback.objects.all()
    return render(request, 'login/admin.html', {
        'sections': sections,
        'posts': posts,
        'job_openings': job_openings,
        'repositories': repositories,
        'feedbacks': feedback,
    })



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


def filter_jobs(request):
    section_id = request.GET.get('section_id')
    if section_id:
        jobs = JobOpening.objects.filter(section__id=section_id)
    else:
        jobs = JobOpening.objects.all()

    job_data = [
        {
            'content_name': job.content_name,
            'description': job.description,
            'url': job.url
        }
        for job in jobs
    ]

    return JsonResponse({'jobs': job_data})

def repo_filter(request):
    section_id = request.GET.get('section_id')
    if section_id:
        repos = Repolink.objects.filter(section__id=section_id)
    else:
        repos = Repolink.objects.all()

    repo_data = [
        {
            'repo_name': repo.repo_name,
            'description': repo.description,
            'repo_url': repo.repo_url
        }
        for repo in repos
    ]

    return JsonResponse({'repos': repo_data})


def delete_jobopening(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    job.delete()
    messages.success(request, 'Job opening deleted successfully.')
    return redirect('admin_page')


def edit_jobopening(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    if request.method == 'POST':
        job.content_name = request.POST['content_name']
        job.description = request.POST['description']
        job.url = request.POST['url']
        job.save()
        messages.success(request, 'Job opening updated successfully.')
        return redirect('admin_page')
    return render(request, 'login/edit_job.html', {'job': job})

def delete_repo(request, repo_id):
    repo = get_object_or_404(Repolink, id=repo_id)
    repo.delete()
    messages.success(request, 'Repository link deleted successfully.')
    return redirect('admin_page')


def edit_repo(request, repo_id):
    repo = get_object_or_404(Repolink, id=repo_id)
    if request.method == 'POST':
        repo.content_name = request.POST['content_name']
        repo.description = request.POST['description']
        repo.repo_url = request.POST['repo_url']
        repo.save()
        messages.success(request, 'Repository link updated successfully.')
        return redirect('admin_page')
    return render(request, 'login/edit_repo.html', {'repo': repo})


# submit feedback
def submit_feedback(request):
    if request.method == "POST":
        feedback_type = request.POST.get('feedback_type')
        message = request.POST.get('message')
        rating = request.POST.get('rating') or None
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('signin')
        user = UserProfile.objects.get(id=user_id)
        Feedback.objects.create(
            user=user,
            feedback_type=feedback_type,
            message=message,
            rating=rating
        )
        messages.success(request, "Thank you for your feedback!, your feedback is valuable to us, we will review it and take necessary actions.")
        return redirect('dashboard')  # or your current page


def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully.")
    return redirect('admin_page')  # or your admin URL name
