import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import yfinance as yf
from ttkbootstrap.scrolled import ScrolledFrame

import json
from operator import itemgetter

screen_width, screen_heigth = 1000, 750
root = ttk.Window(title="Better Wallet", themename="superhero", size=(screen_width, screen_heigth), position=(500, 140), resizable=(False, False))

main_page = ttk.Frame(root, width=screen_width, height=screen_heigth)
main_page.place(relx=0.5, rely=0.5, anchor="center")


stock_data = {}
stock_data["GME"] = {"quantity" : [100], "price" : [30]}
with open('better_data.json', 'w') as f:
    json.dump(stock_data, f, indent=2)


def switch_page(page):
    page.tkraise()

class Stock():
    def __init__(self, symbol, amount, buy_price):
        self.symbol = symbol
        self.amount = amount
        self.buy_price = buy_price

    def get_data(self):
        stock_data = yf.Ticker(self.symbol).info
        regular_market_price, regular_market_change, regular_market_change_percent = itemgetter("regularMarketPrice", "regularMarketChange", "regularMarketChangePercent")(stock_data)
        profit = (regular_market_price - self.buy_price) * self.amount
        profit_percent = 0
        if profit != 0:
            profit_percent = (profit / (self.buy_price * self.amount)) * 100
        return (self.symbol,
                regular_market_price,
                self.amount,
                regular_market_change,
                regular_market_change_percent,
                profit,
                profit_percent)

########################################################################################

def load_data() -> list:
    with open("better_data.json", "r") as file:
        return json.load(file)
def dump_data(data):
    with open("better_data.json", "w") as file:
        json.dump(data, file, indent=2)

def display_stocks_info():
    stocks_data = load_data()
    print(stocks_data)
    sf.children.clear()
    for symbol in stocks_data:
        ttk.Label(sf, text=symbol).pack(anchor=W)

def error_check(symbol: str, quantity: int, price: float):
    if type(symbol) != str:
        raise ValueError("Invalid symbol")
    elif type(quantity) != int:
        raise ValueError("Invalid quantity")
    elif type(price) != float:
        raise ValueError("Invalid price")

def add_stock(symbol: str, quantity: int, price: float):
    stocks_data = load_data()
    if symbol not in stocks_data:
        stocks_data[symbol] = {"quantity" : [], "price" : []}
    stocks_data[symbol]["quantity"].append(quantity)
    stocks_data[symbol]["price"].append(price)
    dump_data(stocks_data)

def get_stock_price(symbol: str) -> float:
    stock_data = yf.Ticker(symbol).info
    return stock_data["currentPrice"]

########################################################################################

main_label = ttk.Label(main_page, text="Tilen's Wallet")
main_label.place(relx = 0.5, rely = 0.3, anchor = 'center')

stock_button = ttk.Button(main_page, text="Stocks", width=10, command=lambda: switch_page(stocks_page))
stock_button.place(relx = 0.5, rely = 0.4, anchor = "center")

########################################################################################

stocks_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
stocks_page.place(relx = 0.5, rely = 0.5, anchor="center")

stocks_label = ttk.Label(stocks_page, text="Stocks")
stocks_label.place(relx = 0.5, rely = 0.1, anchor = "center")

sf = ScrolledFrame(stocks_page, autohide=True)
sf.pack(fill=BOTH, expand=YES, padx=200, pady=200)

# add a large number of checkbuttons into the scrolled frame
#for x in range(20):
#    ttk.Checkbutton(sf, text=f"Checkbutton {x}").pack(anchor=W)


stocks_add_page_button = ttk.Button(stocks_page, text="Add Stock", width=15, command=lambda: switch_page(add_stock_page))
stocks_add_page_button.place(relx = 0.4, rely = 0.9, anchor = "c")
stocks_remove_page_button = ttk.Button(stocks_page, text="Remove Stock", width=15, command=lambda: switch_page(remove_stock_page))
stocks_remove_page_button.place(relx = 0.6, rely = 0.9, anchor = "c")

stocks_back_button = ttk.Button(stocks_page, text="Back", width=10, bootstyle="WARNING", command=lambda: switch_page(main_page))
stocks_back_button.place(relx = 0.5, rely = 1, anchor = "s")

stocks_refresh_button = ttk.Button(stocks_page, text="Refresh", width=10, command=lambda: display_stocks_info())
stocks_refresh_button.place(relx = 0.5, rely = 0.8, anchor = "center")

########################################################################################

add_stock_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
add_stock_page.place(relx = 0.5, rely = 0.5, anchor = "c")

stock_ticker_label = ttk.Label(add_stock_page, text="Ticker")
stock_ticker_label.place(relx = 0.4, rely = 0.3, anchor = "c")
stock_ticker_entry = ttk.Entry(add_stock_page, text="Ticker", width=10)
stock_ticker_entry.place(relx = 0.4, rely = 0.4, anchor = "c")

stock_amount_label = ttk.Label(add_stock_page, text="Amount")
stock_amount_label.place(relx = 0.6, rely = 0.3, anchor = "c")
stock_amount_entry = ttk.Entry(add_stock_page, text="Amount", width=10)
stock_amount_entry.place(relx = 0.6, rely = 0.4, anchor = "c")

add_button = ttk.Button(add_stock_page, text="Add", width=10, command=lambda: add_stock(str(stock_ticker_entry.get()), 
                                                                                        int(stock_amount_entry.get()), 
                                                                                        get_stock_price(str(stock_ticker_entry.get()))))
add_button.place(relx = 0.5, rely = 0.6, anchor = "center")

add_back_button = ttk.Button(add_stock_page, text="Back", width=10, bootstyle="WARNING", command=lambda: switch_page(stocks_page))
add_back_button.place(relx = 0.5, rely = 1, anchor = "s")

########################################################################################

remove_stock_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
remove_stock_page.place(relx = 0.5, rely = 0.5, anchor = "c")

stock_remove_ticker_label = ttk.Label(remove_stock_page, text="Ticker")
stock_remove_ticker_label.place(relx = 0.5, rely = 0.3, anchor = "c")
stock_remove_ticker_entry = ttk.Entry(remove_stock_page, text="Ticker", width=10)
stock_remove_ticker_entry.place(relx = 0.5, rely = 0.4, anchor = "c")

remove_button = ttk.Button(remove_stock_page, text="Remove", width=10)#, command=lambda: remove_stock())
remove_button.place(relx = 0.5, rely = 0.6, anchor = "center")

remove_back_button = ttk.Button(remove_stock_page, text="Back", width=10, bootstyle="WARNING", command=lambda: switch_page(stocks_page))
remove_back_button.place(relx = 0.5, rely = 1, anchor = "s")

########################################################################################



########################################################################################

main_page.tkraise()
root.mainloop()