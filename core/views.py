from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, OTPForm, RegistrationForm, PostForm
import random
import smtplib  # temporary use (or use Django's send_mail)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment, Profile



def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('register')

            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Store user data in session
            request.session['user_data'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'username': username,
                'email': email,
                'password': form.cleaned_data['password'],
                'otp': otp
            }

            # Send OTP to email (placeholder function)
            print("OTP:", otp)  # replace with actual email logic
            send_mail(
                    subject='Your OTP for SocialBuzz Registration',
                    message=f'Your OTP is: {otp}',
                    from_email='your_gmail@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )

            messages.success(request, "OTP has been sent to your email.")
            return redirect('verify_otp')
    else:
        form = RegistrationForm()

    return render(request, "core/register.html", {"form": form})





def verify_otp_view(request):
    user_data = request.session.get("user_data")

    if not user_data:
        messages.error(request, "Session expired. Please register again.")
        return redirect("register")

    if request.method == "POST":
        if 'resend_otp' in request.POST:
            new_otp = str(random.randint(100000, 999999))
            user_data["otp"] = new_otp  # update OTP inside the session
            request.session["user_data"] = user_data  # save updated dict
            request.session.modified = True  # mark session as changed

            send_mail(
                subject='Your New OTP for SocialBuzz',
                message=f'Your new OTP is: {new_otp}',
                from_email='your_gmail@gmail.com',
                recipient_list=[user_data["email"]],
                fail_silently=False,
            )

            messages.success(request, "New OTP sent to your email.")
            return redirect("verify_otp")

        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]

            if entered_otp == user_data["otp"]:
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    password=user_data["password"]
                )
                del request.session["user_data"]
                messages.success(request, "Account created! Please log in.")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()


    return render(request, "core/verify_otp.html", {"form": form})




def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login_input = form.cleaned_data["login_input"]
        password = form.cleaned_data["password"]

        # Support login via email or username
        user = User.objects.filter(email=login_input).first() or User.objects.filter(username=login_input).first()

        if user:
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
        
        messages.error(request, "Invalid credentials.")
    
    return render(request, "core/login.html", {"form": form})



@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")





def home_view(request):
    posts = Post.objects.all().order_by('-created_at')

    # Check if the request is a comment submission
    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        post_id = request.POST.get('post_id')

        if comment_text and post_id:
            post = get_object_or_404(Post, id=post_id)
            Comment.objects.create(post=post, user=request.user, content=comment_text)
            return redirect('home')

    # Add like status to each post
    for post in posts:
        post.liked_by_user = False
        if request.user.is_authenticated:
            post.liked_by_user = post.likes.filter(user=request.user).exists()

    return render(request, 'core/home.html', {'posts': posts})




@login_required(login_url='/login/')
def create_post_view(request):
    form = PostForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "Post created!")
        return redirect('home')

    return render(request, "core/create_post.html", {"form": form})




from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login/')
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    liked = True
    if not created:
        like.delete()
        liked = False

    # Check if it's an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

    # Fallback: regular browser redirect
    return redirect('home')



def comments_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        if reply_text:
            Comment.objects.create(
                post=post,
                user=request.user,  # assumes user is logged in
                content=reply_text
            )
            return redirect('comments', post_id=post.id)
    comments = post.comments.order_by('-timestamp')
    return render(request, 'core/comments.html', {'post' : post, 'comments' : comments})




def user_profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    # Create a Profile
    profile, created = Profile.objects.get_or_create(user=user_profile)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')
    is_following = request.user in user_profile.profile.followers.all()
    return render(request, 'core/profile.html', {
        'profile_user': user_profile,
        'posts': posts,
        'is_following': is_following,
    })





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EditProfileForm

@login_required(login_url='/login/')
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            # Update user fields separately
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            # Save profile
            form.save()

            return redirect('user-profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile, user=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})




@login_required(login_url='/login/')
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    current_user = request.user

    if current_user in target_profile.followers.all():
        target_profile.followers.remove(current_user)
    else:
        target_profile.followers.add(current_user)

    return redirect('user-profile', username=username)




from django.db.models import Q

def search_users_view(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, 'core/search.html', {
        'query': query,
        'results': results,
    })




from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required(login_url='/login/')
def delete_post(request, post_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            post.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='/login/')
def messages_view(request):
    if request.user.is_authenticated:
        return render(request, 'core/messages.html')
    else:
        return redirect('login/')