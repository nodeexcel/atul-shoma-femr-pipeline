from django import forms
from django.conf import settings


class UploadForm(forms.Form):
    input_file = forms.FileField(
        label='FEMR Funds Excel File',
        help_text='Upload the FEMR Funds .xlsx workbook.',
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx'}),
    )

    def clean_input_file(self):
        file = self.cleaned_data['input_file']

        if not file.name.lower().endswith('.xlsx'):
            raise forms.ValidationError('Only .xlsx files are accepted.')

        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 50 * 1024 * 1024)
        if file.size > max_size:
            limit_mb = max_size // (1024 * 1024)
            raise forms.ValidationError(f'File size must be under {limit_mb} MB.')

        return file
