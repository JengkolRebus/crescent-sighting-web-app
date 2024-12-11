from django.shortcuts import render, redirect
from .form import InputForm
from .core import var, hilal
import datetime
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

# Create your views here.
# tHilal
# Home page view function
def home_view(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            form.hitung()
            config = var.config
            data = var.data.copy()
            del data['moon_astrometric']
            del data['sun_astrometric']
            del data['moon_app_diameter']
            del data['sun_app_diameter']
            table_data = []
            DataLable= [
                "Conjunction",
                "Sunset",
                "Moonset",
                "Moon Altitude",
                "Moon Azimuth",
                "Sun Altitude",
                "Sun Azimuth",
                "Elongation",
                "Moon Age",
                "Illumination",
                "Lag Time",
            ]
            # Transpose data untuk tabel
            headers = list(data.keys())
            # Tambahkan baris header ke data tabel
            table_data.append(headers)
            for row in zip(*data.values()): table_data.append(list(row))
            return render(request, 'hilal_app/result.html', {'table_data': table_data, 'config':config, 'DataLable': DataLable})
    else:
        form = InputForm()
    context = {'form':form}
    return render(request, 'hilal_app/hilal.html', context)

def result_view(request, context):
    return render(request, 'hilal_app/result.html', context)

def detail_view(request, index):
    # Menggunakan dictionary comprehension (lebih ringkas)
    data = {key: value[index-1] for key, value in var.data.items()}
    data = {**data, **var.config}

    # Data
    x1 = [data['moon_azimuth']]
    x2 = [data['sun_azimuth']]
    y1 = [data['moon_altitude']]
    y2 = [data['sun_altitude']]

    # PLOTLY: grafik posisi hilal
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', name='Bulan', marker=dict(size=14, color='black')))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='markers', name='Matahari', marker=dict(size=14, color='yellow')))
    fig.update_layout(

        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=4
        ),
        showlegend=False,
    )
    fig.update_xaxes(
        scaleanchor='y',
        scaleratio=1,  # Nilai 1 berarti lebar dan tinggi sama
        tick0=1,
        dtick=1,
    )
    fig.update_yaxes(
        range=[-2, 13],
        tick0=1,
        dtick=1,
        zeroline=True, zerolinewidth=2, zerolinecolor='LightPink'
    )
    # Buat plot
    plot_div = plot(fig, output_type='div')
    return render(request, 'hilal_app/detail.html', {'data': data, 'plot_div': plot_div})