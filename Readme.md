# Dashboard E-Commerce Public Dataset

## Gambaran Umum
E-Commerce Public Dataset adalah kumpulan data transaksi e-commerce di Brasil yang mencakup sekitar 100.000 pesanan dari tahun 2016 hingga 2018. Dataset ini menyediakan informasi yang sangat kaya mengenai berbagai aspek pesanan, seperti status pesanan, harga, metode pembayaran, performa pengiriman, lokasi pelanggan, atribut produk, serta ulasan pelanggan. Data telah dianonimkan, dan referensi perusahaan atau mitra dalam ulasan telah diganti dengan nama-nama dari serial *Game of Thrones*. Dengan adanya data geolocation berdasarkan kode pos, analisis mengenai hubungan antara lokasi geografis dengan pola pembelian dan pengiriman dapat dilakukan dengan lebih mendalam. Dataset ini juga dapat digabungkan dengan *Marketing Funnel Dataset* untuk mendapatkan perspektif pemasaran yang lebih komprehensif.

## Struktur Proyek
- **dashboard/**  
  - `dashboard.py` — File utama aplikasi Streamlit untuk dashboard.  
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

3. **Unduh dan Ekstrak Data:**
   Karena ukuran dataset terlalu besar untuk disertakan dalam repositori, file `main_data.csv` perlu diunduh secara manual.
   
   - **Unduh data dari tautan berikut:**  
     [Download Data](https://drive.google.com/file/d/1hXpa3YTI1V1kHsHkA0NTUTmbpDevcTto/view?usp=drive_link)
   
   - **Pindahkan hasil unduhan ke dalam folder `dashboard/`**
   - **Ekstrak file `main_data.csv` ke dalam folder `dashboard/`**

## Menjalankan Dashboard
Setelah data tersedia, ikuti langkah-langkah berikut untuk menjalankan dashboard:

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

