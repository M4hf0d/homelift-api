from django.forms import ModelForm

from .models import Payment


class PaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        full_name = kwargs.pop("full_name", None)
        email = kwargs.pop("email", None)
        amount = kwargs.pop("amount", None)
        
        super(PaymentForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["client"].widget.attrs["placeholder"] = "Full name"
        self.fields["client_email"].widget.attrs["placeholder"] = "example@gamil.com"
        self.fields["amount"].widget.attrs["placeholder"] = "1000.00"

        if full_name:
            self.fields["client"].initial = full_name
        if email:
            self.fields["client_email"].initial = email
        if amount:
            self.fields["amount"].initial = amount

    class Meta:
        model = Payment
        fields = ["client", "client_email", "amount"]
