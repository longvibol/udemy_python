import pandas as pandas
from fpdf import FPDF

df = pandas.read_csv("Resources/articles.csv", dtype={"id": str})


class Article:
    def __init__(self, article_id, article_buy):
        self.id = article_id
        self.article_buy = int(article_buy)

        self.name = df.loc[df['id'] == self.id, 'name'].squeeze()
        self.price = float(df.loc[df['id'] == self.id, 'price'].squeeze())
        self.in_stock = int(df.loc[df['id'] == self.id, 'in stock'].squeeze())

    def stock_update(self):
        remain = self.in_stock - self.article_buy
        return remain

    def save_updated_stock(self):
        new_stock = self.stock_update()

        if new_stock < 0:
            print("❌ Not enough stock!")
            return

        # Update dataframe
        df.loc[df['id'] == self.id, 'in stock'] = new_stock

        # Save back to CSV
        df.to_csv("Resources/articles.csv", index=False)
        print(f"✅ Stock updated! Remaining stock: {new_stock}")

print(df)
article_ID = input("Choose an article ID: ")
buy_article = int(input("How many you want to buy: "))

article = Article(article_ID, buy_article)

print(article.stock_update())
article.save_updated_stock()
