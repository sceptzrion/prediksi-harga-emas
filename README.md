# Prediksi Harga Emas dengan Linear Regression (Streamlit App)

Aplikasi ini merupakan proyek mata kuliah **Machine Learning**, yang dikembangkan oleh **Kelompok 5**. Aplikasi ini memanfaatkan algoritma **Linear Regression** untuk memprediksi harga emas per gram dalam mata uang **Rupiah (IDR)** berdasarkan harga historis dua hari sebelumnya.

---

## 🚀 Fitur Aplikasi

- 📈 **Prediksi harga emas besok** berdasarkan data real-time dari MetalPriceAPI
- 💰 **Konversi otomatis** dari USD per troy ounce ke IDR per gram
- 📉 **Visualisasi harga terkini**: harga emas hari ini & kemarin
- 🧪 **Simulasi input manual**: pengguna dapat menguji prediksi berdasarkan nilai harga sendiri
- 🔄 **Integrasi API**:
  - [MetalPriceAPI](https://metalpriceapi.com) untuk harga emas (XAU/USD)
  - [CurrencyAPI](https://currencyapi.com) untuk kurs USD → IDR

---

## 🧠 Model yang Digunakan

Model yang digunakan adalah algoritma **Linear Regression**, yang telah dilatih menggunakan data historis harga emas dalam satuan USD per troy ounce. Model ini kemudian digunakan untuk memprediksi harga emas satu hari ke depan berdasarkan harga penutupan dua hari sebelumnya (`Lag_1`, `Lag_2`).

---

## 📦 File yang Dibutuhkan

Pastikan file berikut ada di direktori yang sama:
- `app.py` → file utama aplikasi Streamlit
- `model_regresi.pkl` → file model Machine Learning yang sudah dilatih

---
