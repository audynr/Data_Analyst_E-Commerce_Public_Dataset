import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# --- Fungsi Memuat Data Gabungan dari CSV (Data Sudah Dibersihkan) ---
@st.cache_data
def load_merged_data():
    # Langsung load data gabungan dari file CSV
    data = pd.read_csv("data_gabungan.csv")
    return data

data = load_merged_data()

# --- Visualisasi 1: Review Sales ---
sales_by_review = data.groupby("review_score")["order_item_id"].sum().reset_index()
high_score_sales = sales_by_review[sales_by_review["review_score"].isin([4, 5])]["order_item_id"].sum()
low_score_sales = sales_by_review[sales_by_review["review_score"].isin([1, 2])]["order_item_id"].sum()

if high_score_sales > low_score_sales:
    colors_review = ['limegreen', 'lightgreen']
else:
    colors_review = ['lightgreen', 'limegreen']

fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.barplot(x=['Skor Tinggi (4-5)', 'Skor Rendah (1-2)'],
            y=[high_score_sales, low_score_sales],
            palette=colors_review, ax=ax1)
ax1.set_title("Jumlah Barang Terjual Berdasarkan Skor Review")
ax1.set_ylabel("Jumlah Barang Terjual")
plt.tight_layout()

# --- Visualisasi 2: Top Categories ---
top_categories = data['product_category_name'].value_counts().head(10)
colors_categories = sns.color_palette("Blues", n_colors=len(top_categories))[::-1]

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_categories.values, y=top_categories.index, palette=colors_categories, ax=ax2)
ax2.set_title("Kategori Produk Paling Diminati oleh Pelanggan", fontsize=14)
ax2.set_xlabel("Jumlah Pesanan")
ax2.set_ylabel("Kategori Produk")
plt.tight_layout()

# --- Visualisasi 3: Payment Types ---
payment_counts = data['payment_type'].value_counts()
colors_payment = sns.color_palette("viridis", len(payment_counts))
explode = [0.1 if i == 0 else 0 for i in range(len(payment_counts))]

fig3, ax3 = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax3.pie(
    payment_counts, labels=payment_counts.index, autopct='%1.1f%%',
    colors=colors_payment, startangle=140, explode=explode, shadow=True, wedgeprops={'edgecolor': 'black'}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_bbox(dict(facecolor='black', edgecolor='black', boxstyle='round,pad=0.3'))
ax3.set_title("Proporsi Jenis Pembayaran yang Digunakan oleh Pelanggan", fontsize=14, fontweight='bold')
ax3.legend(payment_counts.index, loc="upper right", bbox_to_anchor=(1.2, 1))
plt.tight_layout()

# --- Visualisasi 4: Geospatial Map ---
seller_group = data.groupby('seller_city').agg({
    'seller_id': pd.Series.nunique,
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean'
}).reset_index().rename(columns={'seller_id': 'seller_count'})
top_seller = seller_group.sort_values('seller_count', ascending=False).iloc[0]

customer_group = data.groupby('customer_city').agg({
    'customer_unique_id': pd.Series.nunique,
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean'
}).reset_index().rename(columns={'customer_unique_id': 'customer_count'})
top_customer = customer_group.sort_values('customer_count', ascending=False).iloc[0]

map_center = [data['geolocation_lat'].mean(), data['geolocation_lng'].mean()]
m = folium.Map(location=map_center, zoom_start=5)

seller_fg = folium.FeatureGroup(name='Penjual')
for _, row in seller_group.iterrows():
    folium.CircleMarker(
        location=[row['geolocation_lat'], row['geolocation_lng']],
        radius=row['seller_count'] / 100,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"{row['seller_city']}: {row['seller_count']} penjual"
    ).add_to(seller_fg)

customer_fg = folium.FeatureGroup(name='Pembeli')
for _, row in customer_group.iterrows():
    folium.CircleMarker(
        location=[row['geolocation_lat'], row['geolocation_lng']],
        radius=row['customer_count'] / 100,
        color='red',
        fill=True,
        fill_color='red',
        popup=f"{row['customer_city']}: {row['customer_count']} pembeli"
    ).add_to(customer_fg)

seller_fg.add_to(m)
customer_fg.add_to(m)
folium.LayerControl().add_to(m)

folium.Marker(
    location=[top_seller['geolocation_lat'], top_seller['geolocation_lng']],
    icon=folium.Icon(color='blue', icon='star'),
    popup=f"Top Penjual: {top_seller['seller_city']} ({top_seller['seller_count']})"
).add_to(m)
folium.Marker(
    location=[top_customer['geolocation_lat'], top_customer['geolocation_lng']],
    icon=folium.Icon(color='red', icon='star'),
    popup=f"Top Pembeli: {top_customer['customer_city']} ({top_customer['customer_count']})"
).add_to(m)

# --- Layout Dashboard dengan Tab Utama dan Sub-Tab ---
st.title("Dashboard Analisis E-Commerce Public Dataset")

# Tab utama: Overview dan Result Analyst
main_tabs = st.tabs(["Overview", "Result Analyst"])

with main_tabs[0]:
    st.header("Overview")
    st.markdown("""
    **Penjelasan Singkat tentang E-Commerce Public Dataset**

    E-Commerce Public Dataset adalah kumpulan data transaksi e-commerce di Brasil yang mencakup sekitar 100.000 pesanan dari tahun 2016 hingga 2018. Dataset ini menyediakan informasi yang kaya mengenai status pesanan, harga, metode pembayaran, performa pengiriman, lokasi pelanggan, atribut produk, serta ulasan pelanggan. Data telah dianonimkan dan referensi perusahaan dalam ulasan diganti dengan nama-nama dari serial *Game of Thrones*.

    Dataset ini tersusun dari beberapa tabel yang saling berhubungan melalui **relasi kunci utama dan kunci asing** (misalnya *order_id*, *customer_id*, *product_id*, dan *seller_id*). Proses **Assessing Data** menunjukkan bahwa struktur dataset yang digunakan sesuai dengan diagram di bawah ini:
    """)
    st.image("../img/relasi_data.png", caption="Struktur Dataset", use_container_width=True)

    st.markdown("""
    Penggabungan (merge) semua dataset memungkinkan kita memperoleh informasi yang lebih komprehensif mengenai hubungan antara pesanan, pelanggan, metode pembayaran, kategori produk, dan ulasan pelanggan. Dengan demikian, analisis lanjutan seperti prediksi penjualan, segmentasi pelanggan, hingga pengoptimalan logistik dapat dilakukan dengan lebih akurat.

    Berikut adalah sample data gabungan sebagai referensi:
    """)
    st.dataframe(data.head(50))

with main_tabs[1]:
    # Sub-tab untuk Result Analyst
    sub_tabs = st.tabs([
        "Review Rating Impact", 
        "Top Ten Category Products", 
        "Preferred Payment Type", 
        "Sellers & Buyers Distribution"
    ])
    
    with sub_tabs[0]:
        st.header("Chart 1: Jumlah Barang Terjual Berdasarkan Skor Review")
        st.pyplot(fig1)
        st.markdown("""
        Dari hasil analisis yang ditampilkan dalam grafik, dapat dilihat bahwa **jumlah barang yang terjual dengan skor review tinggi (4-5) jauh lebih banyak dibandingkan dengan barang yang memiliki skor review rendah (1-2)**. Total barang yang terjual dengan skor tinggi mencapai **10.659.278 unit**, sedangkan barang dengan skor rendah hanya **2.854.572 unit**.  

        Temuan ini menunjukkan bahwa **produk dengan review yang lebih baik cenderung lebih diminati oleh pelanggan**, yang mengindikasikan bahwa **review score berperan penting dalam keputusan pembelian**. Dengan kata lain, semakin baik ulasan yang diberikan oleh pelanggan sebelumnya, semakin tinggi kemungkinan produk tersebut akan dibeli oleh pelanggan baru.  

        Hal ini menjadi penting bagi penjual karena **mengetahui distribusi skor dapat membantu memahami kepuasan pelanggan terhadap produk**. Jika mayoritas produk memiliki skor tinggi, berarti kualitas produk dan layanan yang diberikan sudah sesuai dengan harapan pelanggan. Sebaliknya, jika banyak produk memiliki skor rendah, maka ada **peluang perbaikan** baik dari segi kualitas produk, layanan pelanggan, maupun pengiriman.  

        Selain itu, dari sudut pandang bisnis, pemahaman ini bisa digunakan untuk **strategi pemasaran**, seperti menonjolkan produk dengan skor tinggi dalam promosi atau memberikan insentif bagi pelanggan untuk memberikan review positif. Hal ini juga bisa menjadi indikator bagi penjual untuk melakukan perbaikan terhadap produk dengan skor rendah guna meningkatkan daya tariknya di pasar. 🚀
        """)

    with sub_tabs[1]:
        st.header("Chart 2: Kategori Produk Paling Diminati oleh Pelanggan")
        st.pyplot(fig2)
        st.markdown("""
        ### **Kategori Produk yang Paling Diminati oleh Pelanggan**  

        Pada saat itu, kategori produk yang paling diminati oleh pelanggan adalah **cama_mesa_banho** (produk perlengkapan tempat tidur, meja, dan kamar mandi), yang memiliki jumlah pesanan tertinggi dibandingkan dengan kategori lainnya. Selain itu, kategori **beleza_saude** (produk kecantikan dan kesehatan) serta **moveis_decoracao** (perabot dan dekorasi rumah) juga termasuk dalam daftar produk yang banyak diminati. Kategori lainnya yang cukup populer adalah **esporte_lazer** (olahraga dan rekreasi), **informatica_acessorios** (aksesori komputer), serta **utilidades_domesticas** (peralatan rumah tangga).  

        Karena kategori produk dalam dataset sangat banyak, saya hanya mengambil **10 kategori teratas** berdasarkan jumlah pesanan untuk mendapatkan gambaran yang lebih jelas mengenai tren belanja pelanggan. Dari hasil analisis ini, terlihat bahwa pelanggan cenderung melakukan pembelian untuk kebutuhan rumah tangga, kecantikan, serta teknologi dan hiburan.  

        Informasi ini dapat membantu bisnis dalam merancang strategi pemasaran dan mengelola stok barang dengan lebih efektif, terutama untuk produk-produk yang paling sering dibeli pelanggan.
        """)

    with sub_tabs[2]:
        st.header("Chart 3: Jenis Pembayaran yang Paling Digemari oleh Pelanggan")
        st.pyplot(fig3)
        st.markdown("""
        ### **Jenis Pembayaran yang Paling Digemari oleh Pelanggan**  
        Dari hasil analisis metode pembayaran, ditemukan bahwa **kartu kredit** adalah metode pembayaran yang paling banyak digunakan oleh pelanggan, dengan persentase sebesar **73.6%**. Metode pembayaran **boleto** (invoice pembayaran di Brasil) menempati posisi kedua dengan **19.6%**, sedangkan **voucher** digunakan oleh **5.4%** pelanggan, dan **debit card** hanya digunakan oleh **1.4%** pelanggan.  

        Dominasi pembayaran menggunakan kartu kredit menunjukkan bahwa pelanggan lebih memilih transaksi yang memungkinkan pembayaran secara fleksibel, seperti cicilan atau transaksi tanpa perlu saldo langsung. Hal ini bisa menjadi peluang bagi bisnis untuk menawarkan **program cicilan tanpa bunga atau diskon khusus bagi pengguna kartu kredit** guna meningkatkan transaksi.
        """)

    with sub_tabs[3]:
        st.header("Map: Peta Geospatial Penjual dan Pembeli")
        st_folium(m, width=700, height=500)
        st.markdown("""
        Berdasarkan hasil analisis, **kota dengan jumlah penjual terbanyak** adalah **São Paulo**, dengan total **694 penjual**. Sementara itu, **kota dengan jumlah pelanggan terbanyak** juga adalah **São Paulo**, dengan total **14.757 pelanggan**.  

        Hasil ini diperoleh dengan melakukan **pengelompokan data berdasarkan kota**, di mana jumlah **penjual unik** dan **pelanggan unik** dihitung untuk setiap kota. Selain itu, rata-rata **koordinat geografis** dari setiap kota juga diperhitungkan untuk membantu dalam **visualisasi peta interaktif**.  

        Dari hasil ini, terlihat bahwa **São Paulo merupakan pusat utama perdagangan online**, baik dari sisi penjual maupun pelanggan. Hal ini menunjukkan bahwa kota ini memiliki **ekosistem e-commerce yang sangat aktif**, dengan banyaknya pelaku usaha serta pelanggan yang bertransaksi secara online.  

        Mengapa informasi ini penting?  
        1. **Bagi Penjual**  
           - Memahami bahwa São Paulo memiliki banyak pelanggan dapat membantu dalam **menentukan strategi pemasaran dan distribusi produk**.  
           - Penjual bisa lebih fokus **menargetkan iklan dan promosi** di wilayah ini karena tingginya permintaan.  
           - Mempermudah dalam **pengelolaan stok dan logistik**, karena banyaknya penjual dan pelanggan dalam satu wilayah bisa meningkatkan efisiensi pengiriman.  

        2. **Bagi Pelanggan**  
           - Lebih banyak penjual di satu wilayah berarti **lebih banyak pilihan produk**, sehingga pelanggan dapat **membandingkan harga dan kualitas lebih mudah**.  
           - Dengan jumlah penjual yang tinggi, kemungkinan besar **waktu pengiriman akan lebih cepat**, karena barang dikirim dari lokasi yang lebih dekat.  

        Dengan memahami tren geografis ini, pelaku bisnis dapat lebih **mengoptimalkan strategi pemasaran dan distribusi**, sehingga dapat meningkatkan efisiensi operasional dan kepuasan pelanggan. 🚀
        """)
