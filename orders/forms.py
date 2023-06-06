from django.forms import ModelForm

from .models import Payment


class PaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["client"].widget.attrs["placeholder"] = "Full name"
        self.fields["client_email"].widget.attrs["placeholder"] = "example@gamil.com"
        self.fields["amount"].widget.attrs["placeholder"] = "1000.00"
        # self.fields["comment"].widget.attrs["rows"] = 6
        # self.fields["comment"].widget.attrs[
        #     "placeholder"
        # ] = "I'm very happy for making this donation"

    class Meta:
        model = Payment
        fields = ["client", "client_email", "amount",]