import tkinter as tk
from tkinter import messagebox
from stock import Stock, calculate_gbce_all_share_index
import time


class StockMarketApp:
    def __init__(self, master):
        self.master = master
        master.title("Super Simple Stock Market")
        self.tea = Stock('TEA', 'Common', 0, par_value=100)
        self.pop = Stock('POP', 'Common', 8, par_value=100)
        self.ale = Stock('ALE', 'Common', 23, par_value=60)
        self.gin = Stock('GIN', 'Preferred', 8, par_value=100, fixed_dividend=0.02)
        self.joe = Stock('JOE', 'Common', 13, par_value=250)

        # GUI Elements
        self.label = tk.Label(master, text="Enter Price:")
        self.label.pack()

        self.price_entry = tk.Entry(master)
        self.price_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.results_text = tk.Text(master, height=10, width=50)
        self.results_text.pack()

    def calculate(self):
        try:
            price_input = float(self.price_entry.get())

            # i. Calculate Dividend Yield
            dividend_yield_tea = self.tea.calculate_dividend_yield(price_input)
            dividend_yield_gin = self.gin.calculate_dividend_yield(price_input)

            # ii. Calculate P/E Ratio
            pe_ratio_ale = self.ale.calculate_pe_ratio(price_input)
            pe_ratio_joe = self.joe.calculate_pe_ratio(price_input)

            # iii. Record a trade
            timestamp_input = int(time.time())
            self.tea.record_trade(timestamp_input, 50, 'Buy', 110)
            self.gin.record_trade(timestamp_input, 30, 'Sell', 130)

            # iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
            vws_tea = self.tea.calculate_volume_weighted_stock_price(timestamp_input - (15 * 60))

            # b. Calculate GBCE All Share Index
            all_share_index = calculate_gbce_all_share_index([self.tea, self.pop, self.ale, self.gin, self.joe])

            # Display results in the Text widget, a simple display
            results_message = f"TEA Dividend Yield: {dividend_yield_tea}\n" \
                              f"GIN Dividend Yield: {dividend_yield_gin}\n" \
                              f"ALE P/E Ratio: {pe_ratio_ale}\n" \
                              f"JOE P/E Ratio: {pe_ratio_joe}\n" \
                              f"TEA Volume Weighted Stock Price: {vws_tea}\n" \
                              f"GBCE All Share Index: {all_share_index}"

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results_message)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
