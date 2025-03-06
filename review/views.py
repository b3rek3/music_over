
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Song, Comment
from .forms import AlbumForm, SongForm, CommentForm
# Create your views here.
def index(request):
    return render(request, "base.html")


def song_search(request):
    search_text = request.GET.get("search", "")
    return render(request, "search-result.html", {"search_text": search_text})


def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after adding
    else:
        form = AlbumForm()
    return render(request, 'add_album.html', {'form': form})

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm()
    return render(request, 'add_song.html', {'form': form})



def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


def update_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'update_album.html', {'form': form, 'album': album})


def update_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SongForm(instance=song)
    return render(request, 'update_song.html', {'form': form, 'song': song})





def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'update_comment.html', {'form': form, 'comment': comment})


