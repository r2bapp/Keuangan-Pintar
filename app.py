import streamlit as st
import pandas as pd
import sqlite3
import datetime
from utils.helpers import init_db, save_transaction, get_transactions
from utils.export import export_to_csv, export_to_pdf
from utils.ai import generate_financial_advice

# ----------------------------
# Inisialisasi DB dan Session
# ----------------------------
init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'kategori_pengguna' not in st.session_state:
    st.session_state.kategori_pengguna = None

# ----------------------------
# UI - LOGIN DAN PILIHAN USER
# ----------------------------
st.set_page_config(page_title="Smart Buku Keuangan", layout="wide")
st.title("📒 Smart Buku Keuangan")

if not st.session_state.logged_in:
    with st.form("login_form"):
        nama = st.text_input("Nama Anda")
        email = st.text_input("Email")
        kategori = st.selectbox("Pilih Jenis Pengguna", ["Keluarga", "Pribadi", "Siswa/Mahasiswa", "Pedagang", "UMKM", "Pengusaha", "Pebisnis"])
        submit = st.form_submit_button("Masuk")

        if submit and nama and email:
            st.session_state.logged_in = True
            st.session_state.nama = nama
            st.session_state.email = email
            st.session_state.kategori_pengguna = kategori
            st.success(f"Selamat datang, {nama}! Anda terdaftar sebagai {kategori}.")
            st.experimental_rerun()
else:
    st.sidebar.success(f"Masuk sebagai: {st.session_state.nama} ({st.session_state.kategori_pengguna})")
    menu = st.sidebar.radio("Navigasi", ["Input Data", "Lihat Catatan", "Grafik & Insight", "AI Assistant", "Export Data"])

    if menu == "Input Data":
        st.header("📝 Input Data Keuangan")
        kategori = st.session_state.kategori_pengguna
        with st.form("form_input"):
            tanggal = st.date_input("Tanggal", datetime.date.today())
            jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran", "Tabungan", "Hutang", "Lainnya"])
            item = st.text_input("Deskripsi Item")
            nilai = st.number_input("Jumlah (Rp)", min_value=0)
            catatan = st.text_area("Catatan Tambahan")
            simpan = st.form_submit_button("Simpan")

            if simpan:
                save_transaction(st.session_state.email, tanggal, kategori, jenis, item, nilai, catatan)
                st.success("✅ Data berhasil disimpan!")

    elif menu == "Lihat Catatan":
        st.header("📄 Riwayat Catatan Keuangan")
        df = get_transactions(st.session_state.email)
        st.dataframe(df)

    elif menu == "Grafik & Insight":
        st.header("📊 Analisis Keuangan")
        df = get_transactions(st.session_state.email)
        if df.empty:
            st.info("Belum ada data keuangan.")
        else:
            df["Tanggal"] = pd.to_datetime(df["Tanggal"])
            pemasukan = df[df["Jenis"] == "Pemasukan"].groupby("Tanggal")["Jumlah"].sum()
            pengeluaran = df[df["Jenis"] == "Pengeluaran"].groupby("Tanggal")["Jumlah"].sum()

            st.line_chart(pd.DataFrame({"Pemasukan": pemasukan, "Pengeluaran": pengeluaran}))

    elif menu == "AI Assistant":
        st.header("🤖 Saran Keuangan Otomatis")
        df = get_transactions(st.session_state.email)
        if df.empty:
            st.info("Masukkan data terlebih dahulu untuk mendapatkan saran.")
        else:
            advice = generate_financial_advice(df, st.session_state.kategori_pengguna)
            st.success(advice)

    elif menu == "Export Data":
        st.header("📤 Export Laporan")
        df = get_transactions(st.session_state.email)
        if df.empty:
            st.info("Tidak ada data untuk diekspor.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download CSV", export_to_csv(df), file_name="laporan_keuangan.csv")
            with col2:
                st.download_button("Download PDF", export_to_pdf(df), file_name="laporan_keuangan.pdf")
