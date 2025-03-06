from django import forms
from .models import Album, Song, BandMember, Comment

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_date', 'cover_image']

    def clean_release_date(self):
        date = self.cleaned_data.get('release_date')
        if date is None:
            raise forms.ValidationError("Release date is required.")
        return date


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'album', 'duration']

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration.total_seconds() <= 0:
            raise forms.ValidationError("Duration must be greater than 0.")
        return duration




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'song']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return text
