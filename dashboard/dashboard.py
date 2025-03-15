import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit.components.v1 as components
import matplotlib.patches as mpatches
import plotly.express as px

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
    data = pd.read_csv("main_data.csv")  # Pastikan file main_data.csv sudah tersedia
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
    "Geolocation Map",
    "RFM Analysis"
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

        # Tambahkan filter untuk memilih rentang jumlah customer
        min_customers = int(customer_group['customer_count'].min())
        max_customers = int(customer_group['customer_count'].max())
        selected_range = st.slider("Pilih Rentang Jumlah Customer:", min_value=min_customers, max_value=max_customers, value=(min_customers, max_customers))

        # Filter data berdasarkan rentang yang dipilih
        filtered_customer_group = customer_group[(customer_group['customer_count'] >= selected_range[0]) & (customer_group['customer_count'] <= selected_range[1])]

        # Tentukan kota dengan jumlah pelanggan terbanyak dari data yang sudah difilter
        if not filtered_customer_group.empty:
            top_customer = filtered_customer_group.sort_values('customer_count', ascending=False).iloc[0]

            # Buat peta dengan Folium
            map_center = [data['geolocation_lat'].mean(), data['geolocation_lng'].mean()]
            m = folium.Map(location=map_center, zoom_start=5)

            # Tambahkan marker untuk setiap kota pelanggan menggunakan CircleMarker
            customer_fg = folium.FeatureGroup(name='Pelanggan')
            for _, row in filtered_customer_group.iterrows():
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
        else:
            st.write("Tidak ada data yang sesuai dengan rentang yang dipilih.")
        
        
        # --- 2. Frekuensi Pembelian per Customer (Histogram) ---
        st.subheader("Frekuensi Pembelian per Customer")
        st.write("Histogram berikut menggambarkan frekuensi pembelian per customer. Sumbu X menunjukkan jumlah pembelian, sedangkan sumbu Y menunjukkan jumlah customer yang memiliki frekuensi tersebut.")

        # Hitung jumlah pembelian per customer
        purchase_frequency = data.groupby("customer_unique_id").size()

        # Tambahkan filter untuk memilih rentang jumlah pembelian
        min_purchase = int(purchase_frequency.min())
        max_purchase = int(purchase_frequency.max())
        selected_range = st.slider("Pilih Rentang Jumlah Pembelian:", min_value=min_purchase, max_value=max_purchase, value=(min_purchase, max_purchase))

        # Filter data berdasarkan rentang yang dipilih
        filtered_data = purchase_frequency[(purchase_frequency >= selected_range[0]) & (purchase_frequency <= selected_range[1])]

        # Plot histogram
        fig_hist, ax_hist = plt.subplots(figsize=(8,5))
        sns.histplot(filtered_data, bins=30, kde=False, color="steelblue", ax=ax_hist)
        ax_hist.set_xlabel("Jumlah Pembelian")
        ax_hist.set_ylabel("Frekuensi Customer")
        ax_hist.set_title("Distribusi Frekuensi Pembelian per Customer")
        st.pyplot(fig_hist)

        
        
        # --- 3. Distribusi Skor Review (Pie Chart) ---
        st.subheader("Distribusi Skor Review")
        st.write("Pie chart berikut menampilkan persentase masing-masing skor review yang diberikan oleh customer.")

        # Tambahkan filter untuk memilih skor review yang ingin ditampilkan
        all_scores = sorted(data["review_score"].unique())
        selected_scores = st.multiselect("Pilih skor review:", options=all_scores, default=all_scores)

        # Filter data berdasarkan skor yang dipilih
        filtered_reviews = data[data["review_score"].isin(selected_scores)]

        if not filtered_reviews.empty:
            # Hitung frekuensi setiap skor review, lalu urutkan berdasarkan skor
            review_counts = filtered_reviews["review_score"].value_counts().sort_index()

            # Definisikan warna khusus untuk setiap skor (1 s.d. 5)
            score_colors_map = {
                1: "#2A2E5C",  # dark purple
                2: "#1B728C",  # teal
                3: "#1B8C5F",  # green
                4: "#45BF55",  # light green
                5: "#C1FA65"   # lime-ish
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
        else:
            st.write("Tidak ada data untuk skor review yang dipilih.")

        # --- 4. Metode Pembayaran Terpopuler (Pie Chart) ---
        st.subheader("Metode Pembayaran Terpopuler")
        st.write("Pie chart berikut menunjukkan metode pembayaran yang paling sering digunakan dalam transaksi, berdasarkan persentase jumlah transaksi.")

        # Tambahkan filter untuk memilih metode pembayaran yang ingin ditampilkan
        all_payment_types = data["payment_type"].unique().tolist()
        selected_payment_types = st.multiselect("Pilih metode pembayaran:", options=all_payment_types, default=all_payment_types)

        # Filter data berdasarkan metode pembayaran yang dipilih
        filtered_payment_data = data[data["payment_type"].isin(selected_payment_types)]

        if not filtered_payment_data.empty:
            # Hitung frekuensi metode pembayaran
            payment_counts = filtered_payment_data["payment_type"].value_counts()

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
        else:
            st.write("Tidak ada data untuk metode pembayaran yang dipilih.")
    




    elif viz_option == "Seller Peformances":

        # --- Konversi Tipe Data untuk Kolom Tanggal ---
        data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
        data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'], errors='coerce')
        data['order_estimated_delivery_date'] = pd.to_datetime(data['order_estimated_delivery_date'], errors='coerce')

        # --- Hitung Waktu Pengiriman ---
        # Waktu pengiriman aktual (dalam hari)
        data['delivery_time_actual'] = (data['order_delivered_customer_date'] - data['order_purchase_timestamp']).dt.days
        # Waktu pengiriman estimasi (dalam hari)
        data['delivery_time_estimated'] = (data['order_estimated_delivery_date'] - data['order_purchase_timestamp']).dt.days

        st.header("Seller Performance Analysis")
        st.write("- **Top 10 Seller dengan Penjualan Tertinggi:** Menampilkan grafik batang dari 10 penjual dengan jumlah transaksi terbanyak.")

        # --------------------------------------------------------
        # 1. Top 10 Seller dengan Penjualan Tertinggi (Bar Chart)
        # --------------------------------------------------------
        st.subheader("Top 10 Seller dengan Penjualan Tertinggi")
        # Hitung jumlah penjualan per seller
        seller_sales = data.groupby("seller_id").size().reset_index(name="penjualan")
        # Filter: pilih rentang jumlah penjualan
        min_penjualan = int(seller_sales["penjualan"].min())
        max_penjualan = int(seller_sales["penjualan"].max())
        penjualan_range = st.slider("Pilih rentang jumlah penjualan:", min_value=min_penjualan, max_value=max_penjualan, value=(min_penjualan, max_penjualan))
        # Filter seller berdasarkan rentang yang dipilih
        filtered_seller_sales = seller_sales[(seller_sales["penjualan"] >= penjualan_range[0]) & (seller_sales["penjualan"] <= penjualan_range[1])]
        # Pilih 10 seller teratas dari data yang sudah difilter
        top_sellers = filtered_seller_sales.sort_values("penjualan", ascending=False).head(10)
        # Plot bar chart
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_sellers, x="penjualan", y="seller_id", palette="viridis", ax=ax1)
        ax1.set_xlabel("Jumlah Penjualan")
        ax1.set_ylabel("Seller ID")
        ax1.set_title("Top 10 Seller dengan Penjualan Tertinggi")
        st.pyplot(fig1)

        # --------------------------------------------------------
        # 2. Distribusi Rata-rata Waktu Pengiriman per Seller (Boxplot)
        # --------------------------------------------------------
        st.subheader("Distribusi Rata-rata Waktu Pengiriman per Seller")
        # Hitung rata-rata waktu pengiriman aktual per seller
        avg_delivery_per_seller = data.groupby("seller_id")["delivery_time_actual"].mean().reset_index()
        # Filter: pilih rentang waktu pengiriman
        min_delivery = int(avg_delivery_per_seller["delivery_time_actual"].min())
        max_delivery = int(avg_delivery_per_seller["delivery_time_actual"].max())
        delivery_range = st.slider("Pilih rentang rata-rata waktu pengiriman (hari):", min_value=min_delivery, max_value=max_delivery, value=(min_delivery, max_delivery))
        filtered_delivery = avg_delivery_per_seller[(avg_delivery_per_seller["delivery_time_actual"] >= delivery_range[0]) &
                                                    (avg_delivery_per_seller["delivery_time_actual"] <= delivery_range[1])]
        # Plot boxplot
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.boxplot(x=filtered_delivery["delivery_time_actual"], color="lightblue", ax=ax2)
        ax2.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
        ax2.set_title("Distribusi Rata-rata Waktu Pengiriman per Seller")
        st.pyplot(fig2)

        # --------------------------------------------------------
        # 3. Distribusi Seller per Provinsi (Peta Interaktif)
        # --------------------------------------------------------
        st.subheader("Distribusi Seller per Provinsi")
        st.write("- **Distribusi Seller per Provinsi:** Memvisualisasikan jumlah penjual di berbagai kota menggunakan peta interaktif.")
        # Kelompokkan data penjual berdasarkan seller_city
        seller_group = data.groupby('seller_city').agg({
            'seller_id': pd.Series.nunique,   # Menghitung jumlah seller unik
            'geolocation_lat': 'mean',
            'geolocation_lng': 'mean'
        }).reset_index().rename(columns={'seller_id': 'seller_count'})
        # Filter: pilih rentang jumlah penjual per kota
        min_seller_count = int(seller_group["seller_count"].min())
        max_seller_count = int(seller_group["seller_count"].max())
        seller_range = st.slider("Pilih rentang jumlah penjual per kota:", min_value=min_seller_count, max_value=max_seller_count, value=(min_seller_count, max_seller_count))
        filtered_seller_group = seller_group[(seller_group["seller_count"] >= seller_range[0]) & (seller_group["seller_count"] <= seller_range[1])]
        if not filtered_seller_group.empty:
            # Tentukan kota dengan jumlah seller terbanyak dari data yang sudah difilter
            top_seller = filtered_seller_group.sort_values('seller_count', ascending=False).iloc[0]
            # Buat peta
            map_center = [data['geolocation_lat'].mean(), data['geolocation_lng'].mean()]
            m = folium.Map(location=map_center, zoom_start=5)
            seller_fg = folium.FeatureGroup(name='Penjual')
            for _, row in filtered_seller_group.iterrows():
                folium.CircleMarker(
                    location=[row['geolocation_lat'], row['geolocation_lng']],
                    radius=row['seller_count'] / 100,  # Sesuaikan skala radius
                    color='red',
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.6,
                    popup=f"{row['seller_city']}: {row['seller_count']} penjual"
                ).add_to(seller_fg)
            seller_fg.add_to(m)
            folium.LayerControl().add_to(m)
            # Tandai kota dengan jumlah seller terbanyak secara khusus
            folium.Marker(
                location=[top_seller['geolocation_lat'], top_seller['geolocation_lng']],
                icon=folium.Icon(color='blue', icon='star'),
                popup=f"Top Penjual: {top_seller['seller_city']} ({top_seller['seller_count']})"
            ).add_to(m)
            components.html(m._repr_html_(), width=700, height=500)
        else:
            st.write("Tidak ada data penjual sesuai dengan filter yang dipilih.")

        # --------------------------------------------------------
        # 4. Rata-rata Waktu Pengiriman (Actual vs Estimated) (Bar Chart)
        # --------------------------------------------------------
        st.subheader("Rata-rata Waktu Pengiriman (Actual vs Estimated)")
        st.write("- **Rata-rata Waktu Pengiriman (Actual vs Estimated):** Membandingkan rata-rata waktu pengiriman aktual dengan estimasi pengiriman.")
        # Tambahkan filter tanggal berdasarkan order_purchase_timestamp
        min_date = data['order_purchase_timestamp'].min().date()
        max_date = data['order_purchase_timestamp'].max().date()
        selected_dates = st.date_input("Pilih rentang tanggal pembelian:", value=(min_date, max_date))
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
        else:
            start_date, end_date = min_date, max_date
        filtered_date_data = data[(data['order_purchase_timestamp'].dt.date >= start_date) & (data['order_purchase_timestamp'].dt.date <= end_date)]
        if not filtered_date_data.empty:
            avg_actual = filtered_date_data["delivery_time_actual"].mean()
            avg_estimated = filtered_date_data["delivery_time_estimated"].mean()
            avg_delivery_df = pd.DataFrame({
                "Tipe": ["Actual", "Estimated"],
                "Waktu Pengiriman": [avg_actual, avg_estimated]
            })
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            sns.barplot(x="Tipe", y="Waktu Pengiriman", data=avg_delivery_df, palette="pastel", ax=ax4)
            ax4.set_title("Rata-rata Waktu Pengiriman (Actual vs Estimated)")
            st.pyplot(fig4)
        else:
            st.write("Tidak ada data untuk rentang tanggal yang dipilih.")

        # --------------------------------------------------------
        # 5. Distribusi Harga Produk (Histogram)
        # --------------------------------------------------------
        st.subheader("Distribusi Harga Produk")
        st.write("- **Distribusi Harga Produk:** Menampilkan histogram distribusi harga produk yang terjual.")
        # Filter: pilih rentang harga produk
        min_price = float(data["price"].min())
        max_price = float(data["price"].max())
        price_range = st.slider("Pilih rentang harga produk:", min_value=min_price, max_value=max_price, value=(min_price, max_price))
        filtered_price_data = data[(data["price"] >= price_range[0]) & (data["price"] <= price_range[1])]
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        sns.histplot(filtered_price_data["price"], kde=True, ax=ax5, color="coral")
        ax5.set_xlabel("Harga Produk")
        ax5.set_title("Distribusi Harga Produk")
        st.pyplot(fig5)

    elif viz_option == "Geolocation Map":
        st.header("Map Filter By Geolocation City")
        st.write("Fitur ini memungkinkan pengguna untuk melihat kota-kota yang memenuhi kriteria minimum jumlah penjual dan pembeli, beserta penandaan area untuk masing-masing kota.")

        # Filter: Masukkan threshold minimum penjual dan pembeli
        min_sellers = st.number_input("Minimum jumlah penjual:", min_value=0, value=0)
        min_customers = st.number_input("Minimum jumlah pembeli:", min_value=0, value=0)

        # Kelompokkan data berdasarkan kota (geolocation_city)
        city_group = data.groupby('geolocation_city').agg({
            'seller_id': pd.Series.nunique,
            'customer_unique_id': pd.Series.nunique,
            'geolocation_lat': 'mean',
            'geolocation_lng': 'mean'
        }).reset_index().rename(columns={
            'seller_id': 'seller_count',
            'customer_unique_id': 'customer_count'
        })

        # Filter kota yang memenuhi threshold
        filtered_city_group = city_group[
            (city_group['seller_count'] >= min_sellers) &
            (city_group['customer_count'] >= min_customers)
        ]

        if not filtered_city_group.empty:
            st.write(f"Terdapat {filtered_city_group.shape[0]} kota yang memenuhi kriteria.")
            st.dataframe(filtered_city_group)

            # Filter tambahan: Tentukan tingkat zoom peta
            map_zoom = st.slider("Tentukan tingkat zoom peta:", min_value=5, max_value=15, value=10)

            # Titik tengah peta dihitung dari rata-rata koordinat kota-kota yang memenuhi kriteria
            avg_lat = filtered_city_group['geolocation_lat'].mean()
            avg_lng = filtered_city_group['geolocation_lng'].mean()
            m = folium.Map(location=[avg_lat, avg_lng], zoom_start=map_zoom)

            # Tambahkan marker dan circle untuk setiap kota yang memenuhi kriteria
            for _, row in filtered_city_group.iterrows():
                # Tambahkan circle untuk menandai area kota
                folium.Circle(
                    location=[row['geolocation_lat'], row['geolocation_lng']],
                    radius=5000,  # radius dalam meter, sesuaikan jika diperlukan
                    color='blue',
                    fill=True,
                    fill_opacity=0.1,
                    popup=f"Area {row['geolocation_city']}"
                ).add_to(m)

                # Tambahkan marker untuk menampilkan info jumlah penjual dan pembeli
                folium.Marker(
                    location=[row['geolocation_lat'], row['geolocation_lng']],
                    popup=f"{row['geolocation_city']}: {row['seller_count']} penjual, {row['customer_count']} pembeli",
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(m)

            # Tampilkan peta menggunakan streamlit components
            components.html(m._repr_html_(), width=700, height=500)
        else:
            st.write("Tidak ada kota yang memenuhi kriteria minimum penjual dan pembeli.")
    
    elif viz_option == "RFM Analysis":
        st.header("Understanding Customer Loyalty")

        data["order_purchase_timestamp"] = pd.to_datetime(data["order_purchase_timestamp"])

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Pilih Tanggal Mulai:", data["order_purchase_timestamp"].min())
        with col2:
            end_date = st.date_input("Pilih Tanggal Akhir:", data["order_purchase_timestamp"].max())

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        data = data[(data["order_purchase_timestamp"] >= start_date) & 
                    (data["order_purchase_timestamp"] <= end_date)]


        # Hitung RFM
        snapshot_date = data['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
        rfm = data.groupby('customer_unique_id').agg({
            'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
            'order_id': 'count',
            'payment_value': 'sum'
        }).reset_index()
        rfm.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']

        # Grouping Manual
        def manual_grouping(freq):
            if freq <= 2:
                return "Low"
            elif freq <= 5:
                return "Medium"
            else:
                return "High"

        rfm['Transaction_Group'] = rfm['Frequency'].apply(manual_grouping)

        # Binning Monetary
        bins = [0, 100, 500, 1000, 5000, rfm['Monetary'].max()]
        labels = ['<100', '100-500', '500-1000', '1000-5000', '>5000']
        rfm['Monetary_bin'] = pd.cut(rfm['Monetary'], bins=bins, labels=labels, include_lowest=True)

        # Pilihan Filter di dalam Halaman
        st.subheader("Filter Tambahan")
        col3, col4 = st.columns(2)

        with col3:
            group_option = st.selectbox("Pilih Kelompok Transaksi:", ["All", "Low", "Medium", "High"])
        with col4:
            monetary_option = st.selectbox("Pilih Kategori Total Pengeluaran:", ["All"] + list(rfm['Monetary_bin'].unique()))

        # Terapkan Filter
        if group_option != "All":
            rfm = rfm[rfm["Transaction_Group"] == group_option]
        if monetary_option != "All":
            rfm = rfm[rfm["Monetary_bin"] == monetary_option]

        # Visualisasi Data
        st.subheader("Visualisasi Data")

        # Distribusi Recency
        fig_recency = px.histogram(rfm, x="Recency", nbins=30, title="Distribusi Recency", color_discrete_sequence=["skyblue"])
        st.plotly_chart(fig_recency)

        # Distribusi Frequency
        fig_frequency = px.histogram(rfm, x="Frequency", nbins=30, title="Distribusi Frequency", color_discrete_sequence=["salmon"])
        st.plotly_chart(fig_frequency)

        # Distribusi Monetary
        fig_monetary = px.histogram(rfm, x="Monetary", nbins=30, title="Distribusi Monetary", color_discrete_sequence=["lightgreen"])
        st.plotly_chart(fig_monetary)

        # Scatter Plot Frequency vs Monetary
        fig_scatter = px.scatter(rfm, x="Frequency", y="Monetary", title="Hubungan antara Frequency dan Monetary", opacity=0.5)
        st.plotly_chart(fig_scatter)

        # Boxplot Transaksi Grouping
        fig_boxplot = px.box(rfm, x="Transaction_Group", y="Monetary", title="Perbandingan Total Pengeluaran berdasarkan Kelompok Transaksi", color="Transaction_Group")
        st.plotly_chart(fig_boxplot)

        # Distribusi Bin Monetary
        fig_bar = px.bar(rfm['Monetary_bin'].value_counts().sort_index(), 
                        title="Distribusi Pelanggan Berdasarkan Total Pengeluaran (Binning)",
                        labels={'index': 'Kategori Total Pengeluaran', 'value': 'Jumlah Pelanggan'})
        st.plotly_chart(fig_bar)



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