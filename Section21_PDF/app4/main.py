from fpdf import FPDF
import pandas as pd

pdf = FPDF(orientation='P',unit='mm',format='A4')
pdf.set_auto_page_break(auto=False, margin=0)

df = pd.read_csv('topics.csv')

def add_topic_page(pdf, topic):
    """Add a single page with the given topic header."""
    pdf.add_page()
    pdf.set_font('Arial', 'B', size=24)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=12, txt=topic, align='L', ln=1)
    for y in range(20, 298, 10):
        pdf.line(10, y, 200, y)

    # Set the footer
    pdf.ln(260)
    pdf.set_font('Arial', 'B', size=12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=10, txt=topic, align='R', ln=1)

for index, row in df.iterrows():
    pages= int(row["Pages"])
    topic = row["Topic"]
    add_topic_page(pdf, topic)
    if pages > 1:
        for p in range(pages):
            add_topic_page(pdf, topic)
    else:
        add_topic_page(pdf, topic)

pdf.output('output.pdf')