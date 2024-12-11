from django.shortcuts import render, redirect
from .form import InputForm
from .core import var, hilal
import datetime
from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

# Create your views here.

## test_app
# # Home page view function
# def home_view(request):
#     return render(request, 'test_app/home.html')

# def contact_view(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.send_email()
#             return redirect('contact-success')
#     else:
#         form = ContactForm()
#     context = {'form':form}
#     return render(request, 'test_app/contact.html', context)

# def contact_success_view(request):
#     return render(request, 'test_app/contact_success.html')

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

    # ## peta ketinggian hilal di indonesia
    # date = data['conjunction']
    # latitude_range = np.arange(-15.0, 10.0, 1)
    # longitude_range = np.arange(95.0, 140.0, 1)
    # altitude_data = {
    #     'latitude': [],
    #     'longitude': [],
    #     'altitude': [],
    # }
    # for lat in latitude_range:
    #     for lon in longitude_range:
    #         alt = Find.altitude_map(lat, lon, date)
    #         altitude_data['latitude'].append(lat)
    #         altitude_data['longitude'].append(lon)
    #         altitude_data['altitude'].append(alt.degrees)

    # alt_min = int(min(altitude_data['altitude']))-1
    # alt_max = int(max(altitude_data['altitude']))+1
    # lat_min = int(min(altitude_data['latitude']))
    # lat_max = int(max(altitude_data['latitude']))
    # lon_min = int(min(altitude_data['longitude']))
    # lon_max = int(max(altitude_data['longitude']))

    # ranged = np.arange(alt_min, alt_max, 1)
    # alt_group = {int(key): {'lat': [], 'lon': []} for key in ranged}

    # for i in range(len(altitude_data['latitude'])):
    #     for r in ranged:
    #         if int(altitude_data['altitude'][i]) == r:
    #             alt_group[r]['lat'].append(altitude_data['latitude'][i])
    #             alt_group[r]['lon'].append(altitude_data['longitude'][i])
    #         else:
    #             pass

    # # # Membuat peta menggunakan plotly.graph_objects
    # fig = go.Figure()

    # for i in alt_group.keys():
    #     # Menambahkan data titik ke peta
    #     fig.add_trace(go.Scattermapbox(
    #         lat=alt_group[i]['lat'],  # Latitude
    #         lon=alt_group[i]['lon'],  # Longitude
    #         mode='markers',  # Marker mode
    #         marker=go.scattermapbox.Marker(
    #             size=5,  # Ukuran marker berdasarkan alt
    #             colorscale='Turbo',  # Skema warna
    #         ),
    #         text=f"Ketinggian: {i}",  # Informasi tooltip
    #         name=i
    #     ))

    # # Layout peta
    # fig.update_layout(
    #     width=1080/2,
    #     height=720/2,
    #     mapbox=dict(
    #         style="open-street-map",  # Gaya peta
    #         zoom=2.8,  # Tingkat zoom
    #         center=dict(lat=sum(altitude_data['latitude'])/len(altitude_data['latitude']),
    #                     lon=sum(altitude_data['longitude'])/len(altitude_data['longitude']))  # Pusat peta
    #     ),
    #     hovermode='closest',
    #     title="Peta Ketinggian Hilal",
    #     margin={"r": 0, "t": 50, "l": 0, "b": 0}  # Mengatur margin
    # )
    # alt_group.clear()

    # # Buat plot
    # altitude_chart = plot(fig, output_type='div')
    
    # return render(request, 'hilal_app/detail.html', {'data': data, 'plot_div': plot_div, 'altitude_chart':altitude_chart})
    return render(request, 'hilal_app/detail.html', {'data': data, 'plot_div': plot_div})