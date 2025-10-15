import matplotlib.pyplot as plt

# Sample formula table simulation
formula = [
    {"row": 1, "volume": 0.02, "entry": 3880, "tp": 3880.25, "sl": 3580},
    {"row": 2, "volume": 0.04, "entry": 3880.3, "tp": 3880.75, "sl": 3580.3},
    {"row": 3, "volume": 0.06, "entry": 3880.6, "tp": 3881.5, "sl": 3580.6},
]

# Simulated market price path
market_prices = [3879.5, 3880, 3880.3, 3880.5, 3880.7, 3881, 3881.2, 3881.5]

plt.figure(figsize=(12, 6))

# Plot market price
plt.plot(market_prices, label="Market Price", color="black", linewidth=2, marker="o")

# Plot each order's Entry, TP, and SL
for order in formula:
    plt.hlines(order["entry"], 0, len(market_prices)-1, colors="blue", linestyles="--", label="Entry" if order["row"]==1 else "")
    plt.hlines(order["tp"], 0, len(market_prices)-1, colors="green", linestyles="--", label="TP" if order["row"]==1 else "")
    plt.hlines(order["sl"], 0, len(market_prices)-1, colors="red", linestyles="--", label="SL" if order["row"]==1 else "")

plt.xlabel("Time Step")
plt.ylabel("Price")
plt.title("25% Formula Script: Orders Visualization")
plt.legend()
plt.grid(True)
plt.show()
