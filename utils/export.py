import io
import pandas as pd
from fpdf import FPDF

def export_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def export_to_pdf(df):
    buffer = io.BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Judul
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Laporan Keuangan", ln=True, align='C')
    pdf.ln(5)

    # Header
    pdf.set_font("Arial", style='B', size=10)
    col_widths = [30, 30, 40, 30, 60]
    headers = df.columns.tolist()
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, border=1)
    pdf.ln()

    # Rows
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 10, str(item), border=1)
        pdf.ln()

    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()
