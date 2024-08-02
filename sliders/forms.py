from django import forms 


class RequestForm(forms.Form):
    book_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'name':'book', 'placeholder':'Book Name*'}))
