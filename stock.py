
class Stock:
    def __init__(self, symbol, stock_type, last_dividend, par_value, fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    def calculate_dividend_yield(self, price):
        if self.stock_type == 'Common':
            return self.last_dividend / price if price != 0 else None
        elif self.stock_type == 'Preferred':
            return (self.fixed_dividend * self.par_value) / price if price != 0 else None

    def calculate_pe_ratio(self, price):
        return price / self.last_dividend if self.last_dividend != 0 else None

    def record_trade(self, timestamp, quantity, buy_sell, traded_price):
        self.trades.append({'timestamp': timestamp, 'quantity': quantity, 'buy_sell': buy_sell, 'traded_price': traded_price})

    def calculate_volume_weighted_stock_price(self, time_limit):
        relevant_trades = [trade for trade in self.trades if trade['timestamp'] >= time_limit]
        if not relevant_trades:
            return None
        total_quantity_price = sum(trade['traded_price'] * trade['quantity'] for trade in relevant_trades)
        total_quantity = sum(trade['quantity'] for trade in relevant_trades)
        return total_quantity_price / total_quantity


# Function to calculate the geometric mean for GBCE All Share Index
def calculate_gbce_all_share_index(stocks):
    product_of_prices = 1
    count = 0
    for stock in stocks:
        if stock.calculate_volume_weighted_stock_price(0) is not None:
            product_of_prices *= stock.calculate_volume_weighted_stock_price(0)
            count += 1
    if count == 0:
        return None
    return pow(product_of_prices, 1/count)

