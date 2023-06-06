from django.forms import ModelForm

from .models import Payment


class PaymentForm(ModelForm):
    def __init__(self, full_name, email, amount,  *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["client"].widget.attrs["placeholder"] = full_name
        self.fields["client_email"].widget.attrs["placeholder"] = email
        self.fields["amount"].widget.attrs["placeholder"] = amount
        # self.fields["comment"].widget.attrs["rows"] = 6
        # self.fields["comment"].widget.attrs[
        #     "placeholder"
        # ] = "I'm very happy for making this donation"

    class Meta:
        model = Payment
        fields = ["client", "client_email", "amount",]