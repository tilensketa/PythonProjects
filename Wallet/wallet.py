import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.font import Font
import yfinance as yf

from ttkbootstrap.tableview import Tableview
import json
from operator import itemgetter
from tkinter.font import nametofont

screen_width, screen_heigth = 1000, 750
root = ttk.Window(title="Wallet", themename="superhero", size=(screen_width, screen_heigth), position=(500, 140), resizable=(False, False))
root.iconbitmap("icon.ico")
main_page = ttk.Frame(root, width=screen_width, height=screen_heigth)
main_page.place(relx=0.5, rely=0.5, anchor="center")

def switch_page(page):
    page.tkraise()
"""
stock_names = ["GME", "AMC", "MSFT", "BBBY", "TSLA", "AMZN", "BABA", "AAPL", "GOOG", "NFLX", "KO"]
stock_owned_number = [100, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
stock_owned_price = [30, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
stock_data = {}
stock_data["GME"] = {"amount" : 100, "price" : 30}
stock_data["AMC"] = {"amount" : 2, "price" : 3}
stock_data["TSLA"] = {"amount" : 0, "price" : 0}
stock_data["GOOG"] = {"amount" : 0, "price" : 0}
stock_data["BBBY"] = {"amount" : 3, "price" : 3}
stock_data["KO"] = {"amount" : 0, "price" : 0}
stock_data["AAPL"] = {"amount" : 0, "price" : 0}
stock_data["NFLX"] = {"amount" : 0, "price" : 0}
stock_data["AMZN"] = {"amount" : 0, "price" : 0}
stock_data["BABA"] = {"amount" : 0, "price" : 0}
stock_data["NIO"] = {"amount" : 0, "price" : 0}
#stock_data["AML.L"] = {"amount" : 0, "price" : 0}
"""
with open('data.json', 'w') as f:
    json.dump(stock_data, f, indent=2)
"""

class Stock():
    def __init__(self, symbol, amount, buy_price):
        self.symbol = symbol
        self.amount = amount
        self.buy_price = buy_price

    def get_data1(self):
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

def add_stock():
    stocks = []
    f = open('data.json')
    stocks = json.load(f)
    f.close()
    stocks[stock_ticker_entry.get()] = {"amount" : float(stock_amount_entry.get()), "price" : yf.Ticker(stock_ticker_entry.get()).info["regularMarketPrice"]}
    with open('data.json', 'w') as f:
        json.dump(stocks, f, indent=2)

def remove_stock():
    stocks = []
    f = open('data.json')
    stocks = json.load(f)
    f.close()
    del stocks[stock_remove_ticker_entry.get()]
    with open('data.json', 'w') as f:
        json.dump(stocks, f, indent=2)

main_font = Font(family="Cooper Black", size=30)
main_label = ttk.Label(main_page, text="Tilen's Wallet", font=main_font)
main_label.place(relx = 0.5, rely = 0.3, anchor = 'center')

stock_button = ttk.Button(main_page, text="Stocks", width=10, command=lambda: [switch_page(stocks_page), update_table()])
stock_button.place(relx = 0.5, rely = 0.4, anchor = "center")

crypto_button = ttk.Button(main_page, text="Crypto", width=10, command=lambda: switch_page(crypto_page))
crypto_button.place(relx = 0.5, rely = 0.5, anchor = "center")

############################################### ADD ###################################################

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

add_button = ttk.Button(add_stock_page, text="Add", width=10, command=lambda: add_stock())
add_button.place(relx = 0.5, rely = 0.6, anchor = "center")

add_back_button = ttk.Button(add_stock_page, text="Back", width=10, bootstyle="WARNING", command=lambda: [switch_page(stocks_page), update_table()])
add_back_button.place(relx = 0.5, rely = 1, anchor = "s")

############################################## REMOVE ################################################

remove_stock_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
remove_stock_page.place(relx = 0.5, rely = 0.5, anchor = "c")

stock_remove_ticker_label = ttk.Label(remove_stock_page, text="Ticker")
stock_remove_ticker_label.place(relx = 0.5, rely = 0.3, anchor = "c")
stock_remove_ticker_entry = ttk.Entry(remove_stock_page, text="Ticker", width=10)
stock_remove_ticker_entry.place(relx = 0.5, rely = 0.4, anchor = "c")

remove_button = ttk.Button(remove_stock_page, text="Remove", width=10, command=lambda: remove_stock())
remove_button.place(relx = 0.5, rely = 0.6, anchor = "center")

remove_back_button = ttk.Button(remove_stock_page, text="Back", width=10, bootstyle="WARNING", command=lambda: [switch_page(stocks_page), update_table()])
remove_back_button.place(relx = 0.5, rely = 1, anchor = "s")

############################################# STOCKS ###################################################
stocks_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
stocks_page.place(relx = 0.5, rely = 0.5, anchor="center")

title_font = Font(family="Arial", size=20, weight="bold")
stocks_label = ttk.Label(stocks_page, text="Stocks", font=title_font)
stocks_label.place(relx = 0.5, rely = 0.1, anchor = "center")

stocks_add_page_button = ttk.Button(stocks_page, text="Add Stock", width=15, command=lambda: switch_page(add_stock_page))
stocks_add_page_button.place(relx = 0.4, rely = 0.9, anchor = "c")
stocks_remove_page_button = ttk.Button(stocks_page, text="Remove Stock", width=15, command=lambda: switch_page(remove_stock_page))
stocks_remove_page_button.place(relx = 0.6, rely = 0.9, anchor = "c")

stocks_back_button = ttk.Button(stocks_page, text="Back", width=10, bootstyle="WARNING", command=lambda: switch_page(main_page))
stocks_back_button.place(relx = 0.5, rely = 1, anchor = "s")

stocks_refresh_button = ttk.Button(stocks_page, text="Refresh", width=10, command=lambda: update_table())
stocks_refresh_button.place(relx = 0.5, rely = 0.8, anchor = "center")

headers = [
        {"text":"Symbol"},
        {"text":"Price [$]"},
        {"text":"Amount"},
        {"text":"Change [$]"},
        {"text":"Change [%]"},
        {"text":"Profit [$]"},
        {"text":"Profit [%]"}
    ]

def update_table():
    
    stocks_info = []
    f = open('data.json')
    stocks = json.load(f)
    f.close()

    for stock in stocks.keys(): 
        print(stock)
        stock_data = Stock(stock, stocks[stock]["amount"], stocks[stock]["price"])
        rounded_data = []
        for elem in stock_data.get_data1():
            if type(elem) != str:
                rounded_data.append(round(elem, 2))
            else:
                rounded_data.append(elem)
        stocks_info.append(rounded_data)

    dv = ttk.tableview.Tableview(
        master=stocks_page,
        paginated=True,
        coldata=headers,
        rowdata=stocks_info,
        autoalign = False,
        searchable=True,
        bootstyle="SUCCESS",
        pagesize=10,
        height=10,
        #stripecolor=(colors.light, None),
    )
    dv.place(relx = 0.5, rely = 0.5, anchor = "center")
    dv.autofit_columns()






"""
def update_table1():
    stocks = []
    for stock in stock_names:
        stocks.append(yf.Ticker(stock))

    l1 = [
        {"text":"Symbol"},
        {"text":"Price"},
        {"text":"Change [$]"},
        {"text":"Change [%]"},
        {"text":"Profit [$]"},
        {"text":"Profit [%]"}
    ]  # Columns with Names and style 

    stocks_info = []
    i = 0
    for stock in stocks:
        stock_info = []
        ticker_name = stock.info["symbol"]
        market_price = stock.info["regularMarketPrice"]
        market_change_value = stock.info["regularMarketChange"]
        market_change_percent = stock.info["regularMarketChangePercent"]
        if(stock_owned_number[i] != 0):
            profit = stock.info["regularMarketPrice"] - stock_owned_price[i]
            percent = (profit / stock_owned_price[i]) * 100
        else:
            profit = 0
            percent = 0
        stock_info.append(ticker_name)
        stock_info.append(market_price)
        stock_info.append("%.2f" % market_change_value)
        stock_info.append("%.2f" % market_change_percent)
        stock_info.append("%.2f" % profit)
        stock_info.append("%.2f" % percent)
        
        stock_info = tuple(stock_info)
        stocks_info.append(stock_info)
        i += 1

    dv = ttk.tableview.Tableview(
        master=stocks_page,
        paginated=True,
        coldata=l1,
        rowdata=stocks_info,
        searchable=False,
        bootstyle="WARNING",
        pagesize=10,
        height=10,
        #stripecolor=(colors.light, None),
    )
    dv.place(relx = 0.5, rely = 0.5, anchor = "center")
    dv.autofit_columns()
"""
#update_table()

############################################# CRYPTO ###################################################
crypto_page = ttk.Frame(root, height=screen_heigth, width=screen_width)
crypto_page.place(relx = 0.5, rely = 0.5, anchor="center")

crypto_label = ttk.Label(crypto_page, text="Crypto")
crypto_label.place(relx = 0.5, rely = 0.1, anchor = "center")

crypto_back_button = ttk.Button(crypto_page, text="Back", width=10, command=lambda: switch_page(main_page))
crypto_back_button.place(relx = 0.5, rely = 0.9, anchor = "center")


main_page.tkraise()
root.mainloop()