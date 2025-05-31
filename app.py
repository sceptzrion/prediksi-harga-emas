import streamlit as st
import joblib
import numpy as np
import requests
from datetime import datetime, timedelta

# MENGAMBIL TANGGAL HARI SEBELUMNYA
def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(2)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

YESTERDAY_DATE = yesterday()

# KONFIGURASI API
METAL_API_KEY = st.secrets["METAL_API_KEY"]
CURRENCY_API_KEY = st.secrets["CURRENCY_API_KEY"]

URL_LATEST = f"https://api.metalpriceapi.com/v1/latest?api_key={METAL_API_KEY}&base=USD&currencies=XAU"
URL_YESTERDAY = f"https://api.metalpriceapi.com/v1/{YESTERDAY_DATE}?api_key={METAL_API_KEY}&base=USD&currencies=XAU"
URL_KURS = f"https://api.currencyapi.com/v3/latest?apikey={CURRENCY_API_KEY}&currencies=IDR"

# KONVERSI EMAS & KURS
TROY_OUNCE_TO_GRAM = 31.1035

def usd_ounce_to_idr_gram(usd_ounce, kurs):
    return (usd_ounce * kurs) / TROY_OUNCE_TO_GRAM

def idr_gram_to_usd_ounce(idr_gram, kurs):
    return (idr_gram / kurs) * TROY_OUNCE_TO_GRAM

# AMBIL DATA KURS & EMAS
def ambil_kurs_usd_idr():
    try:
        response = requests.get(URL_KURS)
        data = response.json()
        return data['data']['IDR']['value']
    except:
        st.error("Gagal mengambil kurs USD ke IDR.")
        return None

def ambil_data_emas():
    try:
        r1 = requests.get(URL_LATEST).json()
        r2 = requests.get(URL_YESTERDAY).json()
        lag_1 = r1['rates']['USDXAU']     # Hari ini (lag 1)
        lag_2 = r2['rates']['USDXAU']     # Kemarin (lag 2)
        return lag_1, lag_2
    except:
        st.error("Gagal mengambil data harga emas.")
        return None, None

# LOAD MODEL
model = joblib.load("model_regresi.pkl")

# ===========================
#         DASHBOARD
# ===========================
st.title("Dashboard Prediksi Harga Emas")

st.subheader("Informasi Harga Emas")
lag_1_usd, lag_2_usd = ambil_data_emas()
kurs_usd_idr = ambil_kurs_usd_idr()

if lag_1_usd and lag_2_usd and kurs_usd_idr:
    # Konversi ke IDR/gram
    lag_1_idr_gram = usd_ounce_to_idr_gram(lag_1_usd, kurs_usd_idr)
    lag_2_idr_gram = usd_ounce_to_idr_gram(lag_2_usd, kurs_usd_idr)

    st.metric("Harga Emas Kemarin", f"Rp{lag_2_idr_gram:,.0f} / gram")
    st.metric("Harga Emas Hari Ini", f"Rp{lag_1_idr_gram:,.0f} / gram")
    st.caption(f"*dalam kurs 1 USD → IDR per hari ini: Rp{kurs_usd_idr:,.0f}")

    # Prediksi dalam USD
    pred_usd = model.predict(np.array([[lag_1_usd, lag_2_usd]]))[0]
    pred_idr_gram = usd_ounce_to_idr_gram(pred_usd, kurs_usd_idr)

    selisih = pred_idr_gram - lag_1_idr_gram
    status = "NAIK" if selisih > 0 else "TURUN" if selisih < 0 else "STABIL"
    persentase = (selisih / lag_1_idr_gram) * 100
    if status == "TURUN":
        symbol = "-"
    else:
        symbol = "+"

    st.subheader("Prediksi Harga Emas Besok")
    st.write(f"Prediksi: **Rp{pred_idr_gram:,.0f} / gram**")
    st.write(f"Diperkirakan harga emas besok akan **{status}** sebesar Rp{abs(selisih):,.0f} / gram ({symbol}{abs(persentase):.2f}%)")
else:
    st.warning("Gagal memuat dashboard. Pastikan koneksi API tersedia.")

# ===========================
#    FORM SIMULASI MANUAL
# ===========================
st.markdown("---")
st.subheader("Simulasi Prediksi Manual")

st.write("Masukkan harga H-1 dan H+0 (hari H) dalam Rupiah per gram.")

sim_lag1_idr_gram = st.number_input("Harga H-1 [IDR/gram]", value=0.00, step=10000.00)
sim_lag2_idr_gram = st.number_input("Harga H+0 [IDR/gram]", value=0.00, step=10000.00)

if st.button("Prediksi"):
    if kurs_usd_idr:
        # Konversi ke USD/ounce
        sim_lag1_usd = idr_gram_to_usd_ounce(sim_lag1_idr_gram, kurs_usd_idr)
        sim_lag2_usd = idr_gram_to_usd_ounce(sim_lag2_idr_gram, kurs_usd_idr)

        pred_usd_sim = model.predict(np.array([[sim_lag1_usd, sim_lag2_usd]]))[0]
        pred_idr_gram_sim = usd_ounce_to_idr_gram(pred_usd_sim, kurs_usd_idr)

        selisih_sim = pred_idr_gram_sim - sim_lag2_idr_gram
        status_sim = "NAIK" if selisih_sim > 0 else "TURUN" if selisih_sim < 0 else "STABIL"
        persentase_sim = (selisih_sim / sim_lag2_idr_gram) * 100
        if status_sim == "TURUN":
            symbol_sim = "-"
        else:
            symbol_sim = "+"

        st.success(f"Hasil prediksi harga emas H+1 (besok): **Rp{pred_idr_gram_sim:,.0f} / gram** ({status_sim} sebesar Rp{abs(selisih_sim):,.0f} / gram ({symbol_sim}{abs(persentase_sim):.2f}%))")
    else:
        st.warning("Kurs tidak tersedia, prediksi tidak dapat dilakukan.")

# ===========================
#          TENTANG
# ===========================
st.markdown("---")
st.caption("*Aplikasi ini menampilkan prediksi harga emas untuk hari berikutnya menggunakan algoritma **Linear Regression** berdasarkan data harga penutupan dua hari sebelumnya.")
st.caption("Proyek ini dikembangkan oleh **Kelompok 5** dalam mata kuliah **Machine Learning**.")