import openai
import os

# API KEY bisa dari environment variable atau langsung ditulis (tidak disarankan langsung untuk produksi)
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

def generate_financial_advice(df, kategori_pengguna):
    pemasukan_total = df[df['Jenis'] == 'Pemasukan']['Jumlah'].sum()
    pengeluaran_total = df[df['Jenis'] == 'Pengeluaran']['Jumlah'].sum()
    tabungan_total = df[df['Jenis'] == 'Tabungan']['Jumlah'].sum()

    prompt = f"""
Saya adalah pengguna kategori: {kategori_pengguna}.
Berikut adalah data keuangan saya bulan ini:
- Total pemasukan: Rp{pemasukan_total:,.0f}
- Total pengeluaran: Rp{pengeluaran_total:,.0f}
- Total tabungan: Rp{tabungan_total:,.0f}

Berikan saya saran keuangan singkat dalam 2-3 poin yang relevan dengan kondisi ini.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        advice = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        advice = "Gagal mendapatkan saran. Silakan cek koneksi atau API key Anda."

    return advice
