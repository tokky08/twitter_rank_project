from django import forms

class HelloForm(forms.Form):
    screen_name = forms.CharField(label="スクリーンネーム")