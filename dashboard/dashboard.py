import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit.components.v1 as components
import matplotlib.patches as mpatches

# Suntikkan CSS kustom untuk tombol agar tampak seperti teks biasa
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] .block-container {
        padding-top: 5px !important;
    }

    /* Buat teks tombol rata kiri */
    div.stButton > button {
        text-align: left !important;
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        font-size: 18px;
        padding: 0;
        margin-top: 10px;
        cursor: pointer;
        display: block;
        width: 100%;
    }

    /* Buat teks dalam selectbox juga rata kiri */
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        border: none !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        text-align: left !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Atur style visualisasi
sns.set_style("whitegrid")

st.title("Dashboard Analyst E-Commerce Public Dataset")

@st.cache_data
def load_data():
    data = pd.read_csv("data_gabungan.csv")  # Pastikan file main_data.csv sudah tersedia
    return data

data = load_data()

# --- Inisialisasi Session State ---
if "main_page" not in st.session_state:
    st.session_state["main_page"] = "About Data"

# --- Fungsi untuk Mengubah Halaman Utama ---
def set_main_page(page):
    st.session_state["main_page"] = page

# --- Sidebar Navigation ---
st.sidebar.title("E-Commerce Public Dataset")

# Tombol navigasi utama
if st.sidebar.button("About Data"):
    set_main_page("About Data")
if st.sidebar.button("Data"):
    set_main_page("Data")

# Selectbox untuk memilih sub-bagian visualisasi pada halaman About Data
viz_options = [
    "-- Choose Data Visualization --",
    "Customer Behaviour", 
    "Seller Peformances", 
    "Filter Map"
]
viz_option = st.sidebar.selectbox("Analysis Results", viz_options, index=0)

# --- Halaman Utama ---
if st.session_state["main_page"] == "About Data":
    # Tampilkan konten About Data hanya jika opsi default dipilih
    if viz_option == "-- Choose Data Visualization --":
        st.header("About Data")
        st.markdown("""
        E-Commerce Public Dataset merupakan kumpulan data transaksi e-commerce di Brasil yang mencakup sekitar 100.000 pesanan dari tahun 2016 hingga 2018. Dataset ini menyediakan informasi yang sangat komprehensif mengenai berbagai aspek transaksi, mulai dari status pesanan, harga, metode pembayaran, performa pengiriman, lokasi pelanggan, atribut produk, hingga ulasan pelanggan. Data telah dianonimkan dan referensi perusahaan atau mitra dalam ulasan telah digantikan dengan nama-nama karakter dari serial *Game of Thrones*.
        
        Dataset tersusun dari beberapa tabel yang saling terhubung, seperti data pesanan, detail produk, informasi penjual, pelanggan, metode pembayaran, ulasan, serta data geolokasi berdasarkan kode pos. Dengan adanya informasi geolokasi, pengguna dapat menganalisis hubungan antara lokasi geografis dengan pola pembelian dan pengiriman barang. Selain itu, dataset ini dapat diintegrasikan dengan *Marketing Funnel Dataset* untuk mendapatkan perspektif pemasaran yang lebih mendalam.
        
        Analisis yang dapat dilakukan meliputi penerapan *Natural Language Processing* (NLP) pada ulasan pelanggan, segmentasi atau *clustering* pelanggan berdasarkan perilaku belanja, prediksi penjualan dari pola pembelian, evaluasi performa pengiriman untuk optimasi logistik, serta analisis kualitas produk untuk mengidentifikasi kategori dengan tingkat ketidakpuasan tinggi. Dengan kekayaan informasi yang tersedia, dataset ini sangat berguna untuk eksplorasi data, penerapan machine learning, dan pengembangan strategi bisnis di sektor e-commerce.
        
        Berdasarkan proses **Assessing Data**, struktur dataset ini telah dirancang dengan cermat seperti yang ditunjukkan pada diagram berikut:
        """, unsafe_allow_html=True)
        st.image("../img/relasi_data.png", caption="Struktur Dataset")
        st.markdown("""
        Dataset ini terdiri dari beberapa tabel yang terhubung melalui **relasi kunci utama dan kunci asing**, seperti *order_id*, *customer_id*, *product_id*, dan *seller_id*. Dengan menggabungkan seluruh dataset, kita mendapatkan gambaran yang lebih utuh mengenai keterkaitan antara pesanan, pelanggan, metode pembayaran, kategori produk, serta ulasan pelanggan. Pendekatan ini memungkinkan penemuan pola, tren, dan wawasan bisnis yang lebih mendalam.
        """, unsafe_allow_html=True)

    # --- Tampilkan sub visualisasi jika opsi Customer Behaviour dipilih ---
    elif viz_option == "Customer Behaviour":

        st.header("Customer Behavior Analysis")
        
        # --- 1. Distribusi Customer (Peta Persebaran) ---
        st.subheader("Distribusi Customer")
        st.write("Peta berikut menunjukkan distribusi jumlah customer unik di tiap kota. Circle marker menunjukkan rata-rata koordinat kota dengan ukuran marker yang proporsional terhadap jumlah customer. Kota dengan jumlah customer terbanyak ditandai dengan ikon bintang.")
        
        # Kelompokkan data pelanggan berdasarkan customer_city
        customer_group = data.groupby('customer_city').agg({
            'customer_id': pd.Series.nunique,   # Menghitung jumlah customer unik
            'geolocation_lat': 'mean',
            'geolocation_lng': 'mean'
        }).reset_index().rename(columns={'customer_id': 'customer_count'})

        # Tentukan kota dengan jumlah pelanggan terbanyak
        top_customer = customer_group.sort_values('customer_count', ascending=False).iloc[0]

        # Buat peta dengan Folium
        map_center = [data['geolocation_lat'].mean(), data['geolocation_lng'].mean()]
        m = folium.Map(location=map_center, zoom_start=5)

        # Tambahkan marker untuk setiap kota pelanggan menggunakan CircleMarker
        customer_fg = folium.FeatureGroup(name='Pelanggan')
        for _, row in customer_group.iterrows():
            folium.CircleMarker(
                location=[row['geolocation_lat'], row['geolocation_lng']],
                radius=row['customer_count'] / 100,  # Sesuaikan skala radius jika diperlukan
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"{row['customer_city']}: {row['customer_count']} pelanggan"
            ).add_to(customer_fg)

        customer_fg.add_to(m)
        folium.LayerControl().add_to(m)

        # Tandai kota dengan jumlah pelanggan terbanyak dengan marker khusus
        folium.Marker(
            location=[top_customer['geolocation_lat'], top_customer['geolocation_lng']],
            icon=folium.Icon(color='red', icon='star'),
            popup=f"Top Pelanggan: {top_customer['customer_city']} ({top_customer['customer_count']})"
        ).add_to(m)

        components.html(m._repr_html_(), width=700, height=500)
        
        
        # --- 2. Frekuensi Pembelian per Customer (Histogram) ---
        st.subheader("Frekuensi Pembelian per Customer")
        st.write("Histogram berikut menggambarkan frekuensi pembelian per customer. Sumbu X menunjukkan jumlah pembelian, sedangkan sumbu Y menunjukkan jumlah customer yang memiliki frekuensi tersebut.")
        
        # Hitung jumlah pembelian per customer (misalnya dengan menghitung banyaknya order per customer_unique_id)
        purchase_frequency = data.groupby("customer_unique_id").size()
        fig_hist, ax_hist = plt.subplots(figsize=(8,5))
        # Menggunakan seaborn histplot dengan palette yang terintegrasi
        import seaborn as sns
        sns.histplot(purchase_frequency, bins=30, kde=False, color="steelblue", ax=ax_hist)
        ax_hist.set_xlabel("Jumlah Pembelian")
        ax_hist.set_ylabel("Frekuensi Customer")
        ax_hist.set_title("Distribusi Frekuensi Pembelian per Customer")
        st.pyplot(fig_hist)
        
        
        # --- 3. Distribusi Skor Review (Pie Chart) ---

        st.subheader("Distribusi Skor Review")
        st.write("Pie chart berikut menampilkan persentase masing-masing skor review yang diberikan oleh customer.")

        # Hitung frekuensi setiap skor review, lalu urutkan berdasarkan skor
        review_counts = data["review_score"].value_counts().sort_index()

        # Definisikan warna khusus untuk setiap skor (1 s.d. 5) 
        # (sesuaikan hex code jika Anda ingin warna lain)
        score_colors_map = {
            1: "#2A2E5C",  # Contoh warna (dark purple)
            2: "#1B728C",  # Contoh warna (teal)
            3: "#1B8C5F",  # Contoh warna (green)
            4: "#45BF55",  # Contoh warna (light green)
            5: "#C1FA65"   # Contoh warna (lime-ish)
        }

        # Buat list warna sesuai urutan skor
        review_colors = [score_colors_map[score] for score in review_counts.index]

        # Plot pie chart
        fig_pie1, ax_pie1 = plt.subplots(figsize=(8, 6))
        wedges1, texts1, autotexts1 = ax_pie1.pie(
            review_counts,
            labels=review_counts.index,
            autopct='%1.1f%%',
            colors=review_colors,
            startangle=140,
            shadow=True,
            wedgeprops={'edgecolor': 'black'}
        )

        # Ubah format teks persentase dengan background hitam
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_bbox(dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

        ax_pie1.set_title("Distribusi Skor Review", fontsize=14, fontweight='bold')

        # Tambahkan legenda kustom agar warnanya sesuai dengan skor
        patches = [mpatches.Patch(color=score_colors_map[s], label=f"Score {s}") for s in review_counts.index]
        ax_pie1.legend(handles=patches, loc="upper right", bbox_to_anchor=(1.2, 1))

        st.pyplot(fig_pie1)


        # --- 4. Metode Pembayaran Terpopuler (Pie Chart) ---
        st.subheader("Metode Pembayaran Terpopuler")
        st.write("Pie chart berikut menunjukkan metode pembayaran yang paling sering digunakan dalam transaksi, berdasarkan persentase jumlah transaksi.")

        # Hitung frekuensi metode pembayaran
        payment_counts = data["payment_type"].value_counts()

        # Gunakan palet warna bergradasi (misalnya "viridis")
        colors_payment = sns.color_palette("viridis", len(payment_counts))

        # Atur efek explode untuk menonjolkan metode pembayaran paling populer (frekuensi tertinggi)
        explode = [0.1 if i == 0 else 0 for i in range(len(payment_counts))]

        fig_pie2, ax_pie2 = plt.subplots(figsize=(8, 6))
        wedges2, texts2, autotexts2 = ax_pie2.pie(
            payment_counts,
            labels=payment_counts.index,
            autopct='%1.1f%%',
            colors=colors_payment,
            startangle=140,
            explode=explode,
            shadow=True,
            wedgeprops={'edgecolor': 'black'}
        )

        # Ubah format teks persentase agar memiliki background hitam
        for autotext in autotexts2:
            autotext.set_color('white')
            autotext.set_bbox(dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))

        ax_pie2.set_title("Proporsi Jenis Pembayaran yang Digunakan oleh Pelanggan", fontsize=14, fontweight='bold')

        # Tambahkan legenda di samping
        ax_pie2.legend(payment_counts.index, loc="upper right", bbox_to_anchor=(1.2, 1))

        st.pyplot(fig_pie2)





    elif viz_option == "Seller Peformances":
        # --- Konversi Tipe Data untuk Kolom Tanggal ---
        data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
        data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'], errors='coerce')
        data['order_estimated_delivery_date'] = pd.to_datetime(data['order_estimated_delivery_date'], errors='coerce')

        # --- Hitung Waktu Pengiriman ---
        # Waktu pengiriman aktual (dalam hari) dihitung dari selisih antara tanggal pengiriman ke pelanggan dan tanggal pembelian
        data['delivery_time_actual'] = (data['order_delivered_customer_date'] - data['order_purchase_timestamp']).dt.days
        # Waktu pengiriman estimasi (dalam hari) dihitung dari selisih antara tanggal estimasi pengiriman dan tanggal pembelian
        data['delivery_time_estimated'] = (data['order_estimated_delivery_date'] - data['order_purchase_timestamp']).dt.days

        st.header("Seller Performance Analysis")
        st.write("- **Top 10 Seller dengan Penjualan Tertinggi:** Menampilkan grafik batang dari 10 penjual dengan jumlah transaksi terbanyak.")
        

        # 1. Top 10 Seller dengan Penjualan Tertinggi → Bar chart
        st.subheader("Top 10 Seller dengan Penjualan Tertinggi")
        st.write("- **Distribusi Rata-rata Waktu Pengiriman per Seller:** Menunjukkan distribusi rata-rata waktu pengiriman dalam bentuk boxplot.")
        top_sellers = data.groupby("seller_id").size().reset_index(name="penjualan")
        top_sellers = top_sellers.sort_values("penjualan", ascending=False).head(10)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_sellers, x="penjualan", y="seller_id", palette="viridis", ax=ax1)
        ax1.set_xlabel("Jumlah Penjualan")
        ax1.set_ylabel("Seller ID")
        ax1.set_title("Top 10 Seller dengan Penjualan Tertinggi")
        st.pyplot(fig1)

        # 2. Distribusi Rata-rata Waktu Pengiriman per Seller → Boxplot
        st.subheader("Distribusi Rata-rata Waktu Pengiriman per Seller")
        # Hitung rata-rata waktu pengiriman aktual per seller
        avg_delivery_per_seller = data.groupby("seller_id")["delivery_time_actual"].mean().reset_index()
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.boxplot(x=avg_delivery_per_seller["delivery_time_actual"], color="lightblue", ax=ax2)
        ax2.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
        ax2.set_title("Distribusi Rata-rata Waktu Pengiriman per Seller")
        st.pyplot(fig2)

        st.subheader("Distribusi Seller per Provinsi")
        st.write("- **Distribusi Seller per Provinsi:** Memvisualisasikan jumlah penjual di berbagai kota menggunakan peta interaktif.")
        # --- Kelompokkan data penjual berdasarkan seller_city ---
        seller_group = data.groupby('seller_city').agg({
            'seller_id': pd.Series.nunique,   # Menghitung jumlah seller unik
            'geolocation_lat': 'mean',
            'geolocation_lng': 'mean'
        }).reset_index().rename(columns={'seller_id': 'seller_count'})

        # Tentukan kota dengan jumlah penjual terbanyak
        top_seller = seller_group.sort_values('seller_count', ascending=False).iloc[0]

        # --- Buat peta dengan Folium ---
        # Tentukan titik tengah peta berdasarkan rata-rata seluruh koordinat
        map_center = [data['geolocation_lat'].mean(), data['geolocation_lng'].mean()]
        m = folium.Map(location=map_center, zoom_start=5)

        # Tambahkan marker untuk setiap kota penjual menggunakan CircleMarker
        seller_fg = folium.FeatureGroup(name='Penjual')
        for _, row in seller_group.iterrows():
            folium.CircleMarker(
                location=[row['geolocation_lat'], row['geolocation_lng']],
                radius=row['seller_count'] / 100,  # Sesuaikan skala radius sesuai kebutuhan
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6,
                popup=f"{row['seller_city']}: {row['seller_count']} penjual"
            ).add_to(seller_fg)

        seller_fg.add_to(m)
        folium.LayerControl().add_to(m)

        # Tandai kota dengan penjual terbanyak secara khusus dengan marker bertanda bintang
        folium.Marker(
            location=[top_seller['geolocation_lat'], top_seller['geolocation_lng']],
            icon=folium.Icon(color='blue', icon='star'),
            popup=f"Top Penjual: {top_seller['seller_city']} ({top_seller['seller_count']})"
        ).add_to(m)

        # Tampilkan peta di Streamlit
        components.html(m._repr_html_(), width=700, height=500)

        # 4. Rata-rata Waktu Pengiriman (Actual vs Estimated) → Bar chart
        st.write("Bagian ini menganalisis performa penjual dengan beberapa visualisasi, seperti:")


        st.subheader("Rata-rata Waktu Pengiriman (Actual vs Estimated)")
        st.write("- **Rata-rata Waktu Pengiriman (Actual vs Estimated):** Membandingkan rata-rata waktu pengiriman aktual dengan estimasi pengiriman.")
        
        avg_actual = data["delivery_time_actual"].mean()
        avg_estimated = data["delivery_time_estimated"].mean()
        avg_delivery_df = pd.DataFrame({
            "Tipe": ["Actual", "Estimated"],
            "Waktu Pengiriman": [avg_actual, avg_estimated]
        })
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.barplot(x="Tipe", y="Waktu Pengiriman", data=avg_delivery_df, palette="pastel", ax=ax4)
        ax4.set_title("Rata-rata Waktu Pengiriman (Actual vs Estimated)")
        st.pyplot(fig4)

        # 5. Distribusi Harga Produk → Histogram
        st.subheader("Distribusi Harga Produk")
        st.write("- **Distribusi Harga Produk:** Menampilkan histogram distribusi harga produk yang terjual.")
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.histplot(data["price"], kde=True, ax=ax5, color="coral")
        ax5.set_xlabel("Harga Produk")
        ax5.set_title("Distribusi Harga Produk")
        st.pyplot(fig5)

    elif viz_option == "Filter Map":
        st.header("Map Filter By Geolocation City")
        st.write("Fitur ini memungkinkan pengguna untuk memilih kota berdasarkan geolokasi, kemudian:")
        selected_city = st.selectbox("Pilih Kota (Geolocation):", sorted(data['geolocation_city'].dropna().unique()))
        filtered_city_data = data[data['geolocation_city'] == selected_city]
        

        if not filtered_city_data.empty:
            # Menghitung jumlah penjual dan pembeli di kota yang dipilih
            st.write("- Menampilkan jumlah penjual dan pembeli di kota tersebut.")
            seller_count = filtered_city_data['seller_id'].nunique() if 'seller_id' in filtered_city_data.columns else 0
            customer_count = filtered_city_data['customer_unique_id'].nunique() if 'customer_unique_id' in filtered_city_data.columns else 0
            st.write("- Menampilkan peta dengan marker yang menunjukkan lokasi kota terpilih.")
            st.write(f"Pada kota **{selected_city}** terdapat **{seller_count}** penjual dan **{customer_count}** pembeli.")
            
            # Top 5 kategori produk di kota tersebut
            top5_products = filtered_city_data['product_category_name'].value_counts().head(5)
            st.write("- Menampilkan 5 kategori produk terlaris di kota yang dipilih.")
            st.write("Top 5 kategori produk di kota ini:")
            
            st.dataframe(top5_products.reset_index().rename(columns={'index': 'product_category_name', 'product_category_name': 'Jumlah'}))
            
            # Menentukan titik tengah untuk peta dari data kota tersebut
            avg_lat = filtered_city_data['geolocation_lat'].mean()
            avg_lng = filtered_city_data['geolocation_lng'].mean()
            m = folium.Map(location=[avg_lat, avg_lng], zoom_start=10)
            
            # Menambahkan marker untuk kota terpilih
            folium.Marker(
                location=[avg_lat, avg_lng],
                popup=f"{selected_city}: {seller_count} penjual, {customer_count} pembeli",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)
            
            # Tampilkan peta menggunakan streamlit components
            components.html(m._repr_html_(), width=700, height=500)
        else:
            st.write("Data tidak ditemukan untuk kota yang dipilih.")

    else:
        st.write("Silakan pilih salah satu sub-bab di sidebar (Filter Produk, Analisis Penjualan, atau Map Filter).")


# --- Halaman Data ---
elif st.session_state["main_page"] == "Data":
    st.header("Data")
    st.write("Bagian ini memungkinkan pengguna untuk memfilter dan melihat data berdasarkan beberapa kriteria:")

    st.write("Preview data berdasarkan filter")
    

    # Opsi filter yang tersedia
    filter_options = ["payment_type", "product_category_name", "seller_city", "customer_city", "price"]
    selected_filter = st.selectbox("Pilih Kriteria Filter:", options=filter_options)

    # Menampilkan opsi berdasarkan filter yang dipilih
    if selected_filter != "price":
        unique_values = sorted(data[selected_filter].dropna().unique().tolist())
        selected_value = st.selectbox("Pilih Nilai:", options=["Semua"] + unique_values)
    else:
        selected_value = st.selectbox("Pilih Opsi Harga:", options=["Tertinggi", "Terendah"])

    # Pilihan untuk menampilkan 80 data awal atau terakhir
    opsi_data = st.radio("Tampilkan:", ("80 Data Awal", "80 Data Terakhir"))

    # Terapkan filter berdasarkan pilihan
    filtered_data = data.copy()
    if selected_filter != "price" and selected_value != "Semua":
        filtered_data = filtered_data[filtered_data[selected_filter] == selected_value]
    elif selected_filter == "price":
        if selected_value == "Tertinggi":
            filtered_data = filtered_data.sort_values(by="price", ascending=False)
        else:
            filtered_data = filtered_data.sort_values(by="price", ascending=True)

    # Menampilkan 80 data awal atau terakhir
    if opsi_data == "80 Data Terakhir":
        filtered_data = filtered_data.tail(80)
    else:
        filtered_data = filtered_data.head(80)

    # Tampilkan data dengan container scrollable dan ukuran lebih besar
    st.dataframe(filtered_data, height=600)