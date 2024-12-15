import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import tkinter as tk
from tkinter import messagebox

def fetch_page(url):
    try:
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.text
        else:
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    prices = []
    ratings = []

    for product in soup.find_all("div", {"data-component-type": "s-search-result"}):
        name = product.find("span", {"class": "a-text-normal"})
        products.append(name.text.strip() if name else "N/A")

        price = product.find("span", {"class": "a-price-whole"})
        prices.append(price.text.strip() if price else "N/A")

        rating = product.find("span", {"class": "a-icon-alt"})
        ratings.append(rating.text.strip() if rating else "N/A")

    return products, prices, ratings

def save_to_csv(products, prices, ratings, filename="amazon_products.csv"):
    data = {
        "Product Name": products,
        "Price": prices,
        "Rating": ratings
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def start_scraping():
    url = url_entry.get()
    
    status_label.config(text="Fetching the page...")
    root.update()

    html = fetch_page(url)
    if not html:
        messagebox.showerror("Error", "Failed to fetch the page.")
        status_label.config(text="Failed to fetch the page.")
        return

    status_label.config(text="Parsing the page...")
    root.update()
    products, prices, ratings = parse_page(html)

    if products:
        save_to_csv(products, prices, ratings)
        status_label.config(text="Data saved to amazon_products.csv")
        messagebox.showinfo("Success", "Data saved to CSV successfully!")
    else:
        messagebox.showwarning("No Data", "No products found.")
        status_label.config(text="No products found.")

root = tk.Tk()
root.title("Amazon Product Scraper")

url_label = tk.Label(root, text="Enter Amazon Search URL:")
url_label.pack(padx=10, pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10, pady=5)

scrape_button = tk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.pack(pady=10)

status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.pack(pady=10)

root.mainloop()
