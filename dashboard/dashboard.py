# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and Introduction
st.title("Dashboard Analisis Data Penyewaan Sepeda")
st.markdown("""
Selamat datang di dashboard proyek analisis data penyewaan sepeda. 
Dashboard ini memvisualisasikan analisis distribusi pengguna dan faktor cuaca berdasarkan dataset.
""")

# Load Dataset
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/day.csv')
    return data

data = load_data()

# Sidebar for Filters
st.sidebar.title("Filter Data")
season = st.sidebar.selectbox("Pilih Musim:", ["All", "Spring", "Summer", "Fall", "Winter"])
day_type = st.sidebar.radio("Pilih Tipe Hari:", ["All", "Weekday", "Weekend"])

# Data Filtering
if season != "All":
    season_map = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
    data = data[data["season"] == season_map[season]]

if day_type != "All":
    if day_type == "Weekend":
        data = data[data["weekday"].isin([0, 6])]
    else:
        data = data[~data["weekday"].isin([0, 6])]

# Data Overview
st.subheader("Preview Data")
st.write(data.head())

# Visualizations
st.subheader("Visualisasi Data")

# Distribusi Pengguna Berdasarkan Musim
st.markdown("### Distribusi Pengguna Kasual dan Terdaftar Berdasarkan Musim")
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
data["season_label"] = data["season"].map(season_map)

casual_by_season = data.groupby("season_label")["casual"].mean()
registered_by_season = data.groupby("season_label")["registered"].mean()

fig, ax = plt.subplots()
casual_by_season.plot(kind="bar", color="skyblue", label="Casual", ax=ax)
registered_by_season.plot(kind="bar", color="orange", label="Registered", ax=ax)
ax.set_ylabel("Rata-rata Pengguna")
ax.set_title("Distribusi Pengguna Berdasarkan Musim")
ax.legend()
st.pyplot(fig)

# Faktor Cuaca Berdasarkan Hari
st.markdown("### Perbedaan Faktor Cuaca Berdasarkan Tipe Hari")
data["day_type"] = data["weekday"].apply(lambda x: "Weekend" if x in [0, 6] else "Weekday")

weather_analysis = data.groupby("day_type")[["temp", "hum", "windspeed", "cnt"]].mean()

st.table(weather_analysis)

# Kesimpulan
st.subheader("Kesimpulan")
st.markdown("""
- **Distribusi Pengguna Berdasarkan Musim**:
  Pengguna kasual lebih banyak pada musim tertentu, sementara pengguna terdaftar lebih stabil sepanjang tahun.
- **Faktor Cuaca Berdasarkan Tipe Hari**:
  Suhu lebih tinggi pada akhir pekan, tetapi rata-rata kelembapan dan kecepatan angin tidak menunjukkan perbedaan signifikan.
""")
