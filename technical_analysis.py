import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta

class Operation:
    def __init__(self, operation_type, bought_at, timestamp, n_shares, stop_loss, take_profit):
        self.operation_type = operation_type
        self.bought_at = bought_at
        self.timestamp = timestamp
        self.n_shares = n_shares
        self.sold_at = None
        self.stop_loss = stop_loss
        self.take_profit = take_profit

class TradingStrategy:
    
    def __init__(self):
        self.data = None
        self.operations = []
        self.cash = 1_000_000
        self.com = 0.00125
        self.strategy_value = [1_000_000]
        self.n_shares = 10
        self.file_mapping = {
            "5m": "aapl_5m_train.csv",
            "1h": "aapl_1h_train.csv",
            "1d": "aapl_1d_train.csv",
            "1m": "aapl_1m_train.csv"
        }

    def load_data(self, time_frame):
        file_name = self.file_mapping.get(time_frame)
        if not file_name:
            raise ValueError("Unsupported time frame.")
        self.data = pd.read_csv(file_name)
        self.data.dropna(inplace=True)

    def apply_rsi_strategy(self):
        rsi_data = ta.momentum.RSIIndicator(close=self.data.Close, window=14)
        self.data['RSI'] = rsi_data.rsi()

    def apply_sma_strategy(self):
        short_ma = ta.trend.SMAIndicator(self.data.Close, window=5)
        long_ma = ta.trend.SMAIndicator(self.data.Close, window=21)
        self.data["SHORT_SMA"] = short_ma.sma_indicator()
        self.data["LONG_SMA"] = long_ma.sma_indicator()

    def apply_macd_strategy(self):
        macd = ta.trend.MACD(close=self.data['Close'], window_slow=26, window_fast=12, window_sign=9)
        self.data['MACD'] = macd.macd()
        self.data['Signal_Line'] = macd.macd_signal()

    def execute_trades(self):
        for i, row in self.data.iterrows():
            temp_operations = []
            for op in self.operations:
                if op.stop_loss > row.Close or op.take_profit < row.Close:
                    self.cash += row.Close * op.n_shares * (1 - self.com)
                else:
                    temp_operations.append(op)
            self.operations = temp_operations

            if self.cash > row.Close * self.n_shares * (1 + self.com):
                # Implement your strategy logic here, e.g., check for buy/sell signals
                pass

            total_value = len(self.operations) * row.Close * self.n_shares
            self.strategy_value.append(self.cash + total_value)


    def plot_results(self):
        plt.figure(figsize=(12, 8))
        plt.plot(self.strategy_value)
        plt.title('Trading Strategy Performance')
        plt.show()

# Usage example
strategy = TradingStrategy()
strategy.load_data(time_frame='5m')  # Automatically loads "aapl_5m_train.csv"
# Apply strategies and execute trades as needed
strategy.plot_results()