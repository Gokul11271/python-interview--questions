import MetaTrader5 as mt5
import time
from datetime import datetime

# ===== USER SETTINGS =====
SYMBOL = "XAUUSD_"                # Trading symbol
gap = 1.0                         # Distance between orders
PROFIT_UNIT = 3500                # Profit unit for TP calculation
LOSS_TARGET = -2500               # Stop-loss target (negative)
volumes = [0.01, 0.02, 0.03, 0.04, 0.04, 0.04, 0.04]  # Volume sequence

# ===== SOUND SETTINGS =====
sound_profit = "profit.wav"
sound_loss = "loss.wav"
sound_trigger = "trigger.wav"

# ===== LOGGING =====
def printl(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ===== INITIALIZATION =====
def init_mt5():
    if not mt5.initialize():
        print("❌ MT5 Initialize failed!")
        quit()
    printl(f"✅ Connected to MT5 Terminal: {mt5.terminal_info().name}")

# ===== CLOSE ALL =====
def close_all_positions():
    positions = mt5.positions_get(symbol=SYMBOL)
    if positions:
        for pos in positions:
            close_position(pos)
    # Remove pending orders
    orders = mt5.orders_get(symbol=SYMBOL)
    if orders:
        for order in orders:
            mt5.order_delete(order.ticket)
    printl("✅ All positions and pending orders closed.")

# ===== CLOSE POSITION =====
def close_position(pos):
    side = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": pos.volume,
        "type": side,
        "position": pos.ticket,
        "price": mt5.symbol_info_tick(SYMBOL).ask if side == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(SYMBOL).bid,
        "deviation": 20,
        "magic": 123456,
        "comment": "close",
    }
    mt5.order_send(request)

# ===== PLACE PENDING STOP =====
def place_pending_stop(order_type, price, volume):
    if order_type == "BUY":
        otype = mt5.ORDER_TYPE_BUY_STOP
    else:
        otype = mt5.ORDER_TYPE_SELL_STOP

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": SYMBOL,
        "volume": volume,
        "type": otype,
        "price": price,
        "deviation": 20,
        "magic": 123456,
        "comment": "cycle",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        printl(f"⚠️ Order failed: {result.comment}")
    else:
        printl(f"✅ {order_type} STOP placed at {price} vol={volume}")
    return price

# ===== MAIN CYCLIC LOGIC =====
def run_cycle():
    init_mt5()
    digits = mt5.symbol_info(SYMBOL).digits
    tick = mt5.symbol_info_tick(SYMBOL)
    base_price = tick.bid

    # ===== STARTING WITH SELL STOP =====
    print("\n👉 Choose starting SELL STOP price:")
    price_options = [
        round(base_price - gap, digits),
        round(base_price - (2 * gap), digits),
        round(base_price - (3 * gap), digits)
    ]

    print(f"1. {price_options[0]}\n2. {price_options[1]}\n3. {price_options[2]}")
    choice = input("Enter choice (1/2/3 or custom price): ")

    if choice in ["1", "2", "3"]:
        sell_price = price_options[int(choice) - 1]
    else:
        try:
            sell_price = float(choice)
        except:
            print("⚠️ Invalid input! Using default.")
            sell_price = price_options[0]

    active_price = place_pending_stop("SELL", sell_price, volumes[0])
    last_order_type = "SELL"

    equity_base = mt5.account_info().equity
    cumulative_tp = 0
    cumulative_trigger = 0
    current_volume_index = 0

    printl(f"📌 Baseline equity set at {equity_base:.2f}")

    while True:
        time.sleep(2)
        positions = mt5.positions_get(symbol=SYMBOL)
        orders = mt5.orders_get(symbol=SYMBOL)
        equity_now = mt5.account_info().equity
        floating_pl = equity_now - equity_base

        # ===== LOSS CHECK =====
        if floating_pl <= LOSS_TARGET:
            printl(f"❌ LOSS Target Hit ({floating_pl:.2f}) ≤ {LOSS_TARGET}. Closing all!")
            close_all_positions()
            printl("🔔 LOSS sound x2")
            break

        # ===== TP CHECK =====
        if floating_pl >= cumulative_tp and cumulative_tp > 0:
            printl(f"🎯 Cumulative TP reached! Profit={floating_pl:.2f} ≥ Target={cumulative_tp:.2f}")
            close_all_positions()
            printl("💰 Profit Sound x2")
            break

        # ===== NEW TRIGGER CHECK =====
        if positions:
            pos = positions[-1]  # Latest position
            if cumulative_trigger < len(positions):
                cumulative_trigger = len(positions)
                printl(f"🔔 Trigger #{cumulative_trigger} → ticket={pos.ticket}, type={'BUY' if pos.type==0 else 'SELL'}, vol={pos.volume}, open_price={pos.price_open}")

                # Increase TP target
                cumulative_tp += PROFIT_UNIT * pos.volume
                printl(f"💰 New cumulative TP target = {cumulative_tp:.2f}")

                # Next volume
                current_volume_index = min(current_volume_index + 1, len(volumes) - 1)
                next_vol = volumes[current_volume_index]

                # ===== Alternating SELL → BUY → SELL → BUY pattern =====
                if last_order_type == "BUY":
                    next_side = "SELL"
                    next_price = round(pos.price_open - gap, digits)
                else:
                    next_side = "BUY"
                    next_price = round(pos.price_open + gap, digits)

                printl(f"📈 Next {next_side} STOP placed at {next_price} (next vol={next_vol}, new TP target={cumulative_tp:.2f})")
                active_price = place_pending_stop(next_side, next_price, next_vol)
                last_order_type = next_side

        # ===== Show floating P/L =====
        printl(f"💸 Floating P/L: {floating_pl:.2f} | TP Target: {cumulative_tp:.2f} | Open Trades: {len(positions)} | Pending: {len(orders)}")

# ===== RUN =====
if __name__ == "__main__":
    run_cycle()
