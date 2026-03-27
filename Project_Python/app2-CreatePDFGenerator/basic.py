from fpdf import FPDF

pdf = FPDF(orientation='P',unit='mm',format='A4')


pdf.add_page()
pdf.set_font('Arial','B',size=12)
pdf.cell(w=0,h=12,txt="Hello There!",align='L',ln=1)
pdf.cell(w=0,h=12,txt="Hi There!",align='L',ln=1)


pdf.add_page()
pdf.set_font('Times','B',size=12)
pdf.cell(w=0,h=12,txt="Next There!",align='L',ln=1)
pdf.cell(w=0,h=12,txt="Previous There!",align='L',ln=1)


pdf.output('output.pdf')