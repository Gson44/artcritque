from django.shortcuts import render, redirect, get_object_or_404
from .forms import Sign_Up_Form, Art_Entry_Form
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ArtUser, ArtEntry, ArtEntryRating
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def can_edit_or_delete(user, art_entry):
    return user == art_entry.art_user.user


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        #print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(username)
            print(password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()    
    return render(request, 'sign_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = Sign_Up_Form(request.POST)
        print(form)
        if form.is_valid():
            user =form.save()
            ArtUser.objects.create(user=user)
            return redirect("sign_in")
    else:
        form = Sign_Up_Form()
   
    return render(request, "sign_up.html", {'form': form})

def dashboard(request):
    data = ArtEntry.objects.all()
    print(data)
    return render(request, 'dashboard.html', {'data': data})

def post_image(request):
    if request.method == 'POST':
        form = Art_Entry_Form(request.POST, request.FILES)
        if form.is_valid():
            art_entry = form.save(commit=False)
            print(request.user)
            try:
                art_user = ArtUser.objects.get(user=request.user)
                print("User exist")
            except ArtUser.DoesNotExist:
                print("User doesnt exist")
                
            art_entry.art_user = art_user
            art_entry.save()
            print("Save Success")
            return redirect('dashboard')
    else:
        form = Art_Entry_Form()
    return render(request, 'post_image.html', {'form': form})
def update_image(request, image_id):
    art_entry = get_object_or_404(ArtEntry, id=image_id)
    
    @user_passes_test(lambda user: can_edit_or_delete(user, art_entry), login_url='sign_in/')
    def protected_view(request):
        if request.method == 'POST':
            form = Art_Entry_Form(request.POST, request.FILES, instance=art_entry)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = Art_Entry_Form(instance=art_entry)
        return render(request, 'update_image.html', {'form': form, 'art_entry': art_entry})
    
    return protected_view(request)
def delete_image(request, image_id):
    art_entry = get_object_or_404(ArtEntry, id=image_id)
    
    @user_passes_test(lambda user: can_edit_or_delete(user, art_entry), login_url='sign_in/')
    def protected_view(request):
        if request.method == 'POST':
            art_entry.delete()
            return redirect('dashboard')
        return render(request, 'delete_image.html', {'art_entry': art_entry})
    
    return protected_view(request)
@login_required
@require_POST
def rate_art_entry(request, art_entry_id):
    art_entry = get_object_or_404(ArtEntry, pk=art_entry_id)
    rating = int(request.POST.get('rating', 0))

    if rating < 1 or rating > 5:
        return JsonResponse({'error': 'Invalid rating'})

    if request.user == art_entry.art_user.user:
        return JsonResponse({'error': 'You cannot rate your own entry'})

    # Check if the user has already rated this ArtEntry
    existing_rating = ArtEntryRating.objects.filter(user=request.user, art_entry=art_entry).first()
    if existing_rating:
        return JsonResponse({'error': 'You have already rated this entry'})

    # Create a new rating
    ArtEntryRating.objects.create(user=request.user, art_entry=art_entry, rating=rating)

    # Recalculate the average rating for the ArtEntry
    ratings = ArtEntryRating.objects.filter(art_entry=art_entry)
    total_ratings = sum([rating.rating for rating in ratings])
    num_ratings = len(ratings)
    art_entry.average_rating = total_ratings / num_ratings
    art_entry.save()

    return JsonResponse({'success': 'Rating submitted successfully'})

def get_user_rating(request, art_entry_id):
    if request.method == 'GET':
        art_entry = get_object_or_404(ArtEntry, pk=art_entry_id)
        rating_obj = ArtEntryRating.objects.filter(user=request.user, art_entry=art_entry).first()
        
        if rating_obj:
            return JsonResponse({'rating': rating_obj.rating})
        else:
            return JsonResponse({'rating': 0})