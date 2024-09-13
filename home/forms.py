from django import forms
from .models import feedback, contact_us

class feedback_form(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ['name', 'position', 'description']
    
    def __init__(self, *args, **kwargs):
        super(feedback_form, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['position'].widget.attrs['placeholder'] = 'Enter your position'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter your feedback'

class contact_form(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = ['message']
    
    def __init__(self, *args, **kwargs):
        super(contact_form, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['placeholder'] = 'Enter your message here'