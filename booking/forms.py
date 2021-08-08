from booking.models import Booking, BookingManager
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields  = ["time", "date", "user_name", "user_email"]

        
class BookingManagerForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            #get current classes from Meta
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-check-input" if input_type == "checkbox" else " form-control"
            else:
                classes = " form-check-input" if input_type == "checkbox" else " form-control"
            self.fields[field].widget.attrs.update({
                'class': classes
            })
    class Meta:
        model = BookingManager
        fields  = "__all__"
