import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64

# Function to set background
def set_background(image_file):
    with open(image_file, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/jpeg;base64,{base64_image});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stSidebar {{
            background-color: rgba(0, 0, 0, 0.5); /* Transparan hitam */
            backdrop-filter: blur(8px); /* Efek blur untuk tampilan elegan */
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }}
        .stSidebar .inner-layer {{
            background-color: rgba(255, 255, 255, 0.1); /* Transparan putih */
            border-radius: 10px;
        }}
        .title-box {{
            background-color: rgba(0, 0, 0, 0.6); /* Transparan hitam untuk judul */
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-align: center;
        }}
        .title-box h1 {{
            color: #00FFFF;
            font-size: 36px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Path to the uploaded image
uploaded_image_path = r"C:\Users\Loaf\Documents\VSCode\DA\4k mountain.jpg"  # Replace with the correct path
set_background(uploaded_image_path)

# Custom CSS styling for improved UI
st.markdown("""
<style>
    body {
        font-family: 'Georgia', serif;
        background-color: #1e1e1e;
        color: white;
    }
    .outer-layer {
        background-color: rgba(255, 255, 255, 0.1); /* Transparan putih keabuan */
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }
    .inner-layer {
        background-color: rgba(255, 255, 255, 0.15); /* Transparan putih keabuan */
        padding: 20px;
        border-radius: 10px;
    }
    .section-title {
        font-size: 24px;
        color: #00FFFF;
        margin: 15px 0;
    }
    .content {
        padding: 20px;
        background-color: rgba(50, 50, 50, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .card {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    }
    .card h3 {
        font-size: 22px;
        color: #00FFFF;
        margin-bottom: 10px;
    }
    .card h2 {
        font-size: 28px;
        color: white;
    }
    .sidebar-metric {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: rgba(255, 255, 255, 0.2); /* Transparan putih keabuan */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .sidebar-metric-icon {
        font-size: 24px;
        color: #00FFFF;
        margin-right: 10px;
    }
    .sidebar-metric-text {
        font-size: 18px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for overview and metrics
with st.sidebar:
    st.markdown("""
    <div class="outer-layer">
        <div class="inner-layer">
            <div class="title" style="text-align:center; margin: 10px 0; color:cyan;">Sidebar Widgets</div>
            <h3>Biar apa? Biar radiant</h3>
            <p><strong>Data Statistik</strong></p>
            <div class="sidebar-metric">
                <div class="sidebar-metric-icon">📉</div>
                <div class="sidebar-metric-text">Penurunan Bulanan: 3%</div>
            </div>
            <div class="sidebar-metric">
                <div class="sidebar-metric-icon">📈</div>
                <div class="sidebar-metric-text">Pertumbuhan: 5%</div>
            </div>
            <div class="sidebar-metric">
                <div class="sidebar-metric-icon">💬</div>
                <div class="sidebar-metric-text">Tingkat Keterlibatan: 13%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Title section with box
st.markdown("""
<div class="title-box">
    <h1>Prediktor Harga Mobil Bekas</h1>
</div>
""", unsafe_allow_html=True)

# Input form section
st.markdown("<div class='section-title'>Masukkan Spesifikasi Mobil yang Anda Inginkan</div>", unsafe_allow_html=True)
st.markdown("Isi informasi berikut untuk memprediksi harga jual mobil bekas Anda dalam Rupiah (IDR).", unsafe_allow_html=True)

# Inputs
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("Tahun Rilis", min_value=1980, max_value=2024, step=1, value=2015)
        km_driven = st.number_input("Total Odometer (KM)", min_value=0, step=1000, value=50000)
        fuel = st.selectbox("Jenis BBM", ['Diesel', 'Petrol', 'CNG'])
    with col2:
        seller_type = st.selectbox("Jenis Penjual", ['Individual', 'Dealer'])
        transmission = st.selectbox("Tipe Transmisi", ['Manual', 'Automatic'])
        owner = st.selectbox("Status Pemilik", ['First', 'Second', 'Third'])

    col3, col4 = st.columns(2)
    with col3:
        mileage = st.number_input("Jarak Tempuh (km/ltr or km/kg)", min_value=0.0, step=0.1, value=18.0)
        engine = st.number_input("Kapasitas Mesin (CC)", min_value=500.0, step=100.0, value=1200.0)
    with col4:
        max_power = st.number_input("Torsi Maksimal (BHP)", min_value=20.0, step=1.0, value=85.0)
        seats = st.number_input("Jumlah Kursi", min_value=2, max_value=10, step=1, value=5)

    submit = st.form_submit_button("Cek Prediksi Harga")

# Prediction logic
if submit:
    predicted_price_idr = 1200000000  # Example price for demonstration

    # Display prediction result
    st.markdown(f"""
    <div class="card">
        <h3>Prediksi Harga Mobil Bekas Anda:</h3>
        <h2>Rp {predicted_price_idr:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Prediction trend graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[predicted_price_idr * 0.9, predicted_price_idr],
        mode="lines+text+markers",
        line=dict(color='cyan', width=4),
        text=["", f"Rp {predicted_price_idr:,.2f}"],
        textposition='top right'
    ))
    fig.update_layout(
        title="Grafik Tren Harga Mobil Bekas",
        title_x=0.5,
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font=dict(color='white'),
        yaxis=dict(title="Harga (IDR)", tickprefix="Rp "),
        xaxis=dict(title="Tahun", showgrid=False)
    )
    st.plotly_chart(fig)

st.markdown('</div>', unsafe_allow_html=True)
