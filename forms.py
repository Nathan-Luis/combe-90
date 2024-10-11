from django import forms
from .models import MailingList, Contact, Product, Service, SurveyRequest, SurveyImage

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'phone', 'email', 'message']


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['email']


class ProductStockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock_quantity']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'image']


class SurveyRequestForm(forms.ModelForm):
    # Adding a simple FileField for uploading multiple files
    images = forms.FileField(
        required=False,
        help_text='You can upload up to 10 images.',
    )

    class Meta:
        model = SurveyRequest
        fields = ['name', 'email', 'phone', 'survey_address', 'survey_type', 'geo_location', 'additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 4}),
            'geo_location': forms.TextInput(attrs={'placeholder': 'Latitude, Longitude (optional)'}),
        }
        help_texts = {
            'geo_location': 'Leave blank if you do not wish to use your current location.',
        }

    def __init__(self, *args, **kwargs):
        super(SurveyRequestForm, self).__init__(*args, **kwargs)
        # Mark `geo_location` as optional by setting required to False
        self.fields['geo_location'].required = False

    def clean_images(self):
        images = self.files.getlist('images')
        if len(images) > 10:
            raise forms.ValidationError("You can upload a maximum of 10 images.")
        return images

    def save(self, commit=True):
        instance = super(SurveyRequestForm, self).save(commit=False)
        if commit:
            instance.save()
            # Saving uploaded images
            for image in self.cleaned_data.get('images', []):
                SurveyImage.objects.create(survey_request=instance, image=image)
        return instance
