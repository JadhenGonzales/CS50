from django import forms


class PostForm(forms.Form):
    post_content= forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )