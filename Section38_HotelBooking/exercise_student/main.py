from fpdf import FPDF
import pandas

df = pandas.read_csv("Resources/articles.csv", dtype={"id": str})


class Article:
    def __init__(self, article_id):
        self.id = article_id
        self.name = df.loc[df['id'] == self.id, 'name'].squeeze()
        self.price = df.loc[df['id'] == self.id, 'price'].squeeze()

    def available(self):
        in_stock = df.loc[df['id'] == self.id, 'in stock'].squeeze()
        return in_stock


class Receipt:
    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Receipt nr. {self.article.id}")
        pdf.ln(10)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Article: {self.article.name}")
        pdf.ln(10)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, text=f"Price: {self.article.price}")
        pdf.ln(10)

        pdf.output("receipt.pdf")


print(df)
article_ID = input("Choose an article to buy: ")
article = Article(article_id=article_ID)
if article.available():
    receipt = Receipt(article)
    receipt.generate()
else:
    print("No such article in stock.")

