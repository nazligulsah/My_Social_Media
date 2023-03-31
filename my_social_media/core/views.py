from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .models import Account, Post, Liked, Follow
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from itertools import chain

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Account.objects.get(user=user_object)
    
    user_following_list = []
    feed = []

    user_following = Follow.objects.filter(follower_user=request.user)

    for users in user_following:
        user_following_list.append(users.followed_user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    
    #posts = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list})

@login_required(login_url='signin')
def profile(request,pk):
    #pk is an username 
    user_object = User.objects.get(username=pk)
    user_profile = Account.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object.id)
    
  
    user_post_length = len(user_posts)

    follower = User.objects.get(username = request.user.username) 
    followed = User.objects.get(username = pk) 
    

    if Follow.objects.filter(follower_user=follower, followed_user=followed).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(Follow.objects.filter(followed_user=followed))
    user_following = len(Follow.objects.filter(follower_user=followed))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)
    
@login_required(login_url='signin')    
def follow(request):
    if request.method == 'POST':
        #follower_user = request.user
        follower = request.POST['follower_user']
        followed = request.POST['followed_user']
        follower = User.objects.get(username=follower)
        followed = User.objects.get(username=followed)
        print(follower)
        print(followed)
        if Follow.objects.filter(follower_user=follower, followed_user=followed).first():
            delete_follower = Follow.objects.get(follower_user=follower, followed_user=followed)
            delete_follower.delete()
            return redirect('/profile/'+followed.username)
        else:
            new_follower = Follow.objects.create(follower_user=follower, followed_user=followed)
            new_follower.save()
            return redirect('/profile/'+followed.username)
    else:
        return redirect('/')
    
    
@login_required(login_url = 'sigin')
def settings(request):
    
    user_profile = Account.objects.get(user=request.user)
    if request.method == "POST":
       
        if request.FILES.get('image') == None:
            image = user_profile.profile_picture
            full_name = request.POST['full_name']
            bio = request.POST['bio']
            
            user_profile.profile_picture = image
            user_profile.full_name = full_name
            user_profile.bio = bio
            user_profile.save()
            
        if request.FILES.get('image') != None:
           
            image = request.FILES.get('image')
            full_name = request.POST['full_name']
            bio = request.POST['bio']
            
            user_profile.profile_picture = image
            user_profile.full_name = full_name
            user_profile.bio = bio
            user_profile.save()
        return redirect('settings')
    print("not post rewuest")
    #user = User.objects.get(username= request.user).id
    user_profile = Account.objects.get(user=request.user)
    return render(request, 'setting.html' ,{'user_profile': user_profile})

@login_required(login_url = 'sigin')
def post(request):
    if request.method == 'POST':
        #user = request.user.username
        user= request.user
        image = request.FILES.get('image_post')
        description = request.POST['description']

        new_post = Post.objects.create(user=user, image=image, description=description)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url = 'sigin')  
def like_post(request):
    username = request.user.username
    user_id = request.user.id
    print("user_id", user_id)
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = Liked.objects.filter(post_id=post_id, user=user_id).first()
    
    user = User.objects.get(id = user_id)
    print("user", user)
    if like_filter == None:
        new_like = Liked.objects.create(post_id=post_id, user=user)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

    


def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        #check username 
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()   
            
            #redirect to setting page
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            
            #a user has an account
            user_model = User.objects.get(username=username)
            new_account = Account.objects.create(user=user_model, id=user_model.id)
            new_account.save()
            return redirect('settings')

            
    else:
        return render(request, 'signup.html')
     
    return render(request, 'signup.html')

def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return messages.info("Credentials is not valid")
    
    return render(request, 'signin.html', {messages : 'messages'} )

@login_required(login_url='signin')
def logout(request):
    
    auth.logout(request)
    return render(request, 'signin.html')