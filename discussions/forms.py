from django import forms 

class CommentForm(forms.Form):
    comment_text = forms.CharField(label="comment", widget=forms.Textarea
                    (attrs={'class':'form-control', 'name':'comment', 'placeholder':'Your Comment*'}))
