from django import forms
from django.forms import ModelForm, CharField, TextInput, widgets

from .core import var
from .core import hilal


# hilal_app
class InputForm(forms.Form):
    latitude_degree = forms.IntegerField(
        min_value=0,
        max_value=90,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;",
            }
        ),
    )
    latitude_minute = forms.FloatField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;",
                "step": "0.01",
            }
        ),
    )
    latitude_second = forms.FloatField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;",
                "step": "0.01",
            }
        ),
    )

    longitude_degree = forms.IntegerField(
        min_value=0,
        max_value=180,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;",
            }
        ),
    )
    longitude_minute = forms.FloatField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;,",
                "step": "0.01",
            }
        ),
    )
    longitude_second = forms.FloatField(
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control p-1 text-end",
                "style": "min-width: 6ch; max-width: 8ch;",
                "step": "0.01",
            }
        ),
    )

    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
    )

    date_end = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
    )

    latitude_direction = forms.TypedChoiceField(
        choices=(
            ("south", "S"),
            ("north", "N"),
        ),
        widget=widgets.Select(
            attrs={
                "class": "btn btn-primary",
            }
        ),
    )

    longitude_direction = forms.TypedChoiceField(
        choices=(
            ("east", "E"),
            ("west", "W"),
        ),
        widget=widgets.Select(
            attrs={
                "class": "btn btn-primary",
            }
        ),
    )

    def decimal_degree(self, degree, minute, second):
        if degree < 0:
            return -(abs(degree) + (minute / 60) + (second / 3600))
        else:
            return degree + (minute / 60) + (second / 3600)

    def hitung(self):
        # clear data stored in variable
        for i in var.data:
            var.data[i] = []
        for i in var.config:
            var.config[i] = []
        latitude_val = self.decimal_degree(
            self.cleaned_data["latitude_degree"],
            self.cleaned_data["latitude_minute"],
            self.cleaned_data["latitude_second"],
        )
        longitude_val = self.decimal_degree(
            self.cleaned_data["longitude_degree"],
            self.cleaned_data["longitude_minute"],
            self.cleaned_data["longitude_second"],
        )
        if self.cleaned_data['latitude_direction'] == 'south':
            var.config['latitude'] = latitude_val * -1
        else:
            var.config['latitude'] = latitude_val

        if self.cleaned_data['longitude_direction'] == 'west':
            var.config['longitude'] = longitude_val * -1
        else:
            var.config['longitude'] = longitude_val

        var.config["date_start"] = self.cleaned_data["date_start"]
        var.config["date_end"] = self.cleaned_data["date_end"]

        date_start = var.config["date_start"]
        date_end = var.config["date_end"]

        start = (date_start.year, date_start.month, date_start.day)
        end = (date_end.year, date_end.month, date_end.day)
        latitude = var.config["latitude"]
        longitude = var.config["longitude"]

        f = hilal(latitude, longitude, start, end)
        f.compute()