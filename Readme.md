# Dashboard E-Commerce Public Dataset

## Gambaran Umum
E-Commerce Public Dataset adalah kumpulan data transaksi e-commerce di Brasil yang mencakup sekitar 100.000 pesanan dari tahun 2016 hingga 2018. Dataset ini menyediakan informasi yang sangat kaya mengenai berbagai aspek pesanan, seperti status pesanan, harga, metode pembayaran, performa pengiriman, lokasi pelanggan, atribut produk, serta ulasan pelanggan. Data telah dianonimkan, dan referensi perusahaan atau mitra dalam ulasan telah diganti dengan nama-nama dari serial *Game of Thrones*. Dengan adanya data geolocation berdasarkan kode pos, analisis mengenai hubungan antara lokasi geografis dengan pola pembelian dan pengiriman dapat dilakukan dengan lebih mendalam. Dataset ini juga dapat digabungkan dengan *Marketing Funnel Dataset* untuk mendapatkan perspektif pemasaran yang lebih komprehensif.

## Struktur Proyek
- **dashboard/**  
  - `main.py` — File utama aplikasi Streamlit untuk dashboard.  
  - `data_gabungan.csv` — File CSV hasil penggabungan data dari berbagai dataset.
- **notebooks/**  
  - Notebook Jupyter yang mendokumentasikan proses pembersihan, penggabungan, dan analisis data secara detail.
- **requirements.txt**  
  - Daftar paket Python yang diperlukan untuk menjalankan proyek ini.

## Persiapan & Instalasi
1. **Clone Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Instal Dependencies:**
   Pastikan semua paket yang diperlukan telah terinstal dengan menjalankan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Export Data Gabungan:**
   Sebelum memasuki tahap visualisasi, data gabungan diekspor ke dalam file CSV (`data_gabungan.csv`) dan disimpan di folder **dashboard**. Hal ini dilakukan agar data lebih mudah diakses dan digunakan dalam pembuatan dashboard menggunakan Streamlit Cloud.

## Menjalankan Dashboard
Untuk menjalankan dashboard, ikuti langkah-langkah berikut:
1. Masuk ke folder **dashboard**:
   ```bash
   cd dashboard
   ```
2. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run dashboard.py
   ```

## Proses Analisis
Untuk mengetahui proses olah analisis secara mendalam, silakan buka notebook yang terdapat di folder **notebooks**. Notebook tersebut menjelaskan secara rinci langkah-langkah penggabungan data, pembersihan, eksplorasi, hingga visualisasi data.

## Kesimpulan
Dashboard ini memberikan insight mendalam dari E-Commerce Public Dataset by Olist, antara lain:
- **Review Score dan Penjualan:** Menganalisis berapa persentase produk dengan skor tinggi (4-5) dibandingkan dengan skor rendah (1-2) untuk memahami pengaruh review terhadap penjualan.
- **Analisis Geografis:** Mengidentifikasi kota atau wilayah dengan jumlah penjual terbanyak serta jumlah pelanggan terbanyak, yang membantu memahami pusat perdagangan online dan tren geografis.
- **Tren Produk dan Pembayaran:** Mengeksplorasi kategori produk yang diminati serta jenis pembayaran yang paling digemari oleh pelanggan.

Selamat mencoba dan semoga dashboard ini dapat membantu dalam memahami dinamika e-commerce di Brasil!
```
