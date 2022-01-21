from booking.models import Booking, BookingManager
from django import forms


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["time", "date", "user_mobile", "user_name", "user_email"]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Approve the booking if confirmation_required is False
        b_manager = BookingManager.objects.first()
        if not b_manager.confirmation_required:
            instance.approved = True

        if commit:
            instance.save()
        return instance


class BookingManagerForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            # get current classes from Meta
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
        fields = "__all__"
        exclude = [
            # TODO: Add this fields to admin panel and fix the functions
            "max_appointment_per_time",
            "max_appointment_per_day",
        ]
