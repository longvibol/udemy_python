import pandas as pandas
from fpdf import FPDF

df = pandas.read_csv("Resources/articles.csv")


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

    def receipt_pdf_print(self):
        # Get article name
        article_series = df.loc[df["id"] == self.item_id, "name"]
        if article_series.empty:
            raise ValueError(f"Item id {self.item_id} not found in CSV.")
        article = str(article_series.squeeze()).title()

        # Get price
        price_series = df.loc[df["id"] == self.item_id, "price"]
        price = price_series.squeeze()

        # Create PDF
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font("Times", size=16, style="B")
        pdf.cell(0, 8, text=f"Receipt nr. {self.item_id}")
        pdf.ln(10)

        pdf.set_font("Times", size=14)
        pdf.cell(0, 8, text=f"Article: {article}")
        pdf.ln(10)

        pdf.cell(0, 8, text=f"Price: {price}")
        pdf.ln(10)

        pdf.output("receipt.pdf")


item1 = Item(100)
item1.receipt_pdf_print()
