from booking.models import Booking, BookingSettings
from django import forms


class ChangeInputsStyle(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            # get current classes from Meta
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-check-input" if input_type == "checkbox" else " form-control  flatpickr-input"
            else:
                classes = " form-check-input" if input_type == "checkbox" else " form-control flatpickr-input"
            self.fields[field].widget.attrs.update({
                'class': classes
            })


class BookingDateForm(ChangeInputsStyle):
    date = forms.DateField(required=True)


class BookingTimeForm(ChangeInputsStyle):
    time = forms.TimeField(widget=forms.HiddenInput())


class BookingCustomerForm(ChangeInputsStyle):
    user_name = forms.CharField(max_length=250)
    user_email = forms.EmailField()
    user_mobile = forms.CharField(required=False, max_length=10)


class BookingSettingsForm(ChangeInputsStyle, forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = BookingSettings
        fields = "__all__"
        exclude = [
            # TODO: Add this fields to admin panel and fix the functions
            "max_appointment_per_time",
            "max_appointment_per_day",
        ]
