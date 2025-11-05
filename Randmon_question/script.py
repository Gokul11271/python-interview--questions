#!/usr/bin/env python3
"""
Fixed & improved cyclic BUY/SELL STOP script for MetaTrader5.

- Retries failed orders until success
- Prints how many attempts were made
- Profit target is linked to the pending order that triggered
- Keeps a log of all triggered orders and prints summary at the end
"""

import MetaTrader5 as mt5
import time
from datetime import datetime

# ------------------- Config ------------------- #
SYMBOL = "XAUUSD_"    # trading symbol (set to your broker's symbol name)
SLIPPAGE = 500           # allowed deviation in points
MAGIC = 12345            # magic number
LOSS_TARGET = 50.0       # equity loss stop (in $)
POLL_INTERVAL = 0.5      # seconds between main loop polls
DEFAULT_PROFIT_TARGET = 1.0  # default $ profit target

# ------------------- Globals ------------------- #
order_log = []  # stores history of triggered trades

# ------------------- MT5 Init ------------------- #
if not mt5.initialize():
    print("❌ Initialize() failed, error =", mt5.last_error())
    quit()

print("✅ MT5 Initialized")

if not mt5.symbol_select(SYMBOL, True):
    print(f"❌ Failed to select symbol {SYMBOL}")
    mt5.shutdown()
    quit()

symbol_info = mt5.symbol_info(SYMBOL)
if symbol_info is None:
    print(f"❌ symbol_info for {SYMBOL} returned None")
    mt5.shutdown()
    quit()

point = symbol_info.point
stop_level = symbol_info.trade_stops_level * point if symbol_info.trade_stops_level is not None else 0
digits = symbol_info.digits

# Volume limits
vol_min = symbol_info.volume_min or 0.01
vol_step = symbol_info.volume_step or 0.01
vol_max = symbol_info.volume_max or 100.0

# ------------------- Helpers ------------------- #
def now():
    return datetime.now().strftime("%H:%M:%S")

def normalize_volume(vol: float) -> float:
    if vol <= vol_min:
        return vol_min
    steps = round((vol - vol_min) / vol_step)
    normalized = vol_min + steps * vol_step
    normalized = max(vol_min, min(normalized, vol_max))
    return float(round(normalized, 8))

def printl(*args, **kwargs):
    print(f"[{now()}]", *args, **kwargs)

# ------------------- Generators ------------------- #
def formula25_table(vol_min=0.02, vol_step=0.02, rows=14):
    data = []
    target_profit = 0.0
    vol = vol_min
    for _ in range(rows):
        target_profit += vol * 25
        actual = vol * 14.6
        col25 = target_profit / 2
        data.append({
            "Target Profit": round(target_profit, 2),
            "Volume": round(vol, 2),
            "Actual": round(actual, 2),
            "25%": round(col25, 2),
        })
        vol += vol_step
    return data

def formula25_generator(vol_min=0.02, vol_step=0.02):
    target_profit = 0.0
    vol = vol_min
    while True:
        target_profit += vol * 25
        yield (round(vol, 2), round(target_profit, 2))
        vol += vol_step

# ------------------- Order / Position Helpers ------------------- #
def cancel_all_pending():
    orders = mt5.orders_get(symbol=SYMBOL)
    if not orders:
        return 0
    removed = 0
    for o in orders:
        try:
            req = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": int(o.ticket),
                "symbol": o.symbol,
                "magic": o.magic if hasattr(o, "magic") else MAGIC,
                "comment": "Cancel pending by script"
            }
            mt5.order_send(req)
            removed += 1
        except Exception as e:
            printl("Warning cancelling order:", e)
    if removed:
        printl(f"🗑️ Cleared {removed} pending orders.")
    return removed

def close_all_positions(max_attempts=0, delay=1.0):
    positions = mt5.positions_get(symbol=SYMBOL)
    if not positions:
        cancel_all_pending()
        printl("✅ No positions to close.")
    else:
        for pos in positions:
            attempt = 0
            while True:
                attempt += 1
                if pos.type == mt5.POSITION_TYPE_BUY:
                    close_type = mt5.ORDER_TYPE_SELL
                    price = mt5.symbol_info_tick(SYMBOL).bid
                else:
                    close_type = mt5.ORDER_TYPE_BUY
                    price = mt5.symbol_info_tick(SYMBOL).ask

                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": SYMBOL,
                    "volume": pos.volume,
                    "type": close_type,
                    "position": pos.ticket,
                    "price": price,
                    "deviation": SLIPPAGE,
                    "magic": MAGIC,
                    "comment": "Close by script"
                }
                result = mt5.order_send(request)
                if result and getattr(result, "retcode", None) == mt5.TRADE_RETCODE_DONE:
                    printl(f"✅ Closed position {pos.ticket} at {price} (attempts={attempt})")
                    break
                else:
                    err = getattr(result, "retcode", mt5.last_error())
                    printl(f"⚠️ Failed to close position {pos.ticket} (retcode={err}), attempt={attempt}... retrying")
                    time.sleep(delay)
                if max_attempts > 0 and attempt >= max_attempts:
                    printl(f"❌ Max attempts reached while closing {pos.ticket}")
                    break

    cancel_all_pending()
    printl("✅ All positions and pending orders closed.")

    # --- Print summary log --- 
    if order_log:
        print("\n📊 Trading Summary:")
        print(f"{'Ticket':<10} {'Type':<6} {'Volume':<8} {'TP($)':<8}")
        print("-" * 40)
        for entry in order_log:
            print(f"{entry['ticket']:<10} {entry['type']:<6} {entry['volume']:<8} {entry['tp']:<8}")
        print("-" * 40)
        print(f"✅ Total Orders: {len(order_log)}\n")

def account_equity_profit():
    ai = mt5.account_info()
    if ai:
        return ai.profit
    return 0.0

def place_pending_stop(order_side: str, base_price: float, volume: float, max_attempts=0, delay=1.0):
    cancel_all_pending()
    volume = normalize_volume(volume)

    tick = mt5.symbol_info_tick(SYMBOL)
    if not tick:
        printl("❌ No tick available to place order.")
        return None

    if order_side == "BUY":
        mt_type = mt5.ORDER_TYPE_BUY_STOP
        min_price = tick.ask + stop_level + (2 * point)
        price = max(base_price, min_price)
    else:
        mt_type = mt5.ORDER_TYPE_SELL_STOP
        max_price = tick.bid - stop_level - (2 * point)
        price = min(base_price, max_price)

    price = round(price, digits)

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": SYMBOL,
        "volume": volume,
        "type": mt_type,
        "price": price,
        "deviation": SLIPPAGE,
        "type_filling": mt5.ORDER_FILLING_FOK,
        "type_time": mt5.ORDER_TIME_GTC,
        "comment": f"Cyclic {order_side} STOP",
        "magic": MAGIC,
    }

    attempt = 0
    while True:
        attempt += 1
        result = mt5.order_send(request)
        if result is not None and getattr(result, "retcode", None) == mt5.TRADE_RETCODE_DONE:
            printl(f"✅ {order_side} STOP placed at {price} vol={volume} (retcode=10009, attempts={attempt})")
            return price
        else:
            err = getattr(result, "retcode", mt5.last_error())
            printl(f"⚠️ Failed to place {order_side} STOP (retcode={err}), attempt={attempt}... retrying")
            time.sleep(delay)
        if max_attempts > 0 and attempt >= max_attempts:
            printl(f"❌ Max attempts reached ({max_attempts}). Could not place {order_side} STOP.")
            return None

# ------------------- Trading Cycle ------------------- #
def run_cycle(vol_gen, gap):
    tick = mt5.symbol_info_tick(SYMBOL)
    if not tick:
        printl("❌ No tick data available. Cannot run cycle.")
        return "error"

    base_ask = tick.ask
    options = [round(base_ask + i * point * 10, digits) for i in range(1, 4)]

    print("\n👉 Choose starting BUY STOP price:")
    for i, val in enumerate(options, 1):
        print(f"{i}. {val}")
    choice = input("Enter choice (1/2/3 or custom price): ").strip()
    if choice in ["1", "2", "3"]:
        buy_price = options[int(choice) - 1]
    else:
        try:
            buy_price = float(choice)
        except ValueError:
            printl("Invalid price entered. Aborting cycle.")
            return "error"

    vol, expected_profit = next(vol_gen)

    printl(f"Starting vol={vol}, expected TP=${expected_profit}")
    printl(f"🚀 Starting cycle with BUY STOP at {buy_price}, gap={gap}, SL=${LOSS_TARGET}")
    active_price = place_pending_stop("BUY", buy_price, vol)
    if not active_price:
        return "error"

    last_pending_expected = expected_profit
    profit_target = None
    last_order_type = "BUY"
    last_positions = mt5.positions_get(symbol=SYMBOL) or []
    last_pos_count = len(last_positions)

    baseline_equity = None
    triggered_count = 0

    while True:
        acc_profit = account_equity_profit()
        positions = mt5.positions_get(symbol=SYMBOL)

        if not positions:
            print("⏳ Waiting for first trade to trigger...", end="\r")
            time.sleep(POLL_INTERVAL)
            continue

        if baseline_equity is None:
            baseline_equity = acc_profit
            printl(f"📌 Baseline equity set at: {baseline_equity:.2f}")
            time.sleep(POLL_INTERVAL)
            continue

        if profit_target is None and last_pending_expected is not None:
            profit_target = last_pending_expected
            printl(f"📌 Profit target set to: ${profit_target}")

        trade_profit = acc_profit - baseline_equity
        print(f"❤️ Trades={triggered_count} | Profit={trade_profit:.2f} "
              f"(Target=${profit_target if profit_target else 'N/A'} 👾 Total=${acc_profit:.2f})", end="\r")

        if profit_target is not None:
            if trade_profit >= profit_target:
                printl(f"\n🎯 TP hit {trade_profit:.2f} >= {profit_target:.2f}")
                close_all_positions()
                return "profit"
            if trade_profit <= -LOSS_TARGET:
                printl(f"\n❌ SL hit {trade_profit:.2f} <= -{LOSS_TARGET}")
                close_all_positions()
                return "loss"

        current_positions = mt5.positions_get(symbol=SYMBOL) or []
        curr_count = len(current_positions)

        if curr_count > last_pos_count:
            new_positions = [p for p in current_positions if p.ticket not in [lp.ticket for lp in last_positions]]
            for pos in new_positions:
                triggered_count += 1
                profit_target = last_pending_expected
                printl(f"\n🔔 Trigger #{triggered_count} → ticket={pos.ticket}, vol={pos.volume}, TP=${profit_target}")

                # --- Log this trade ---
                order_log.append({
                    "ticket": pos.ticket,
                    "type": "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL",
                    "volume": pos.volume,
                    "tp": profit_target
                })

                next_vol, next_expected_profit = next(vol_gen)

                if pos.type == mt5.POSITION_TYPE_BUY and last_order_type == "BUY":
                    sell_price = round(active_price - gap, digits)
                    printl(f"🔔 BUY triggered → placing SELL STOP {sell_price}, vol={next_vol}, TP=${next_expected_profit}")
                    active_price = place_pending_stop("SELL", sell_price, next_vol)
                    last_order_type = "SELL"
                else:
                    buy_price_next = round(active_price + gap, digits)
                    printl(f"🔔 SELL triggered → placing BUY STOP {buy_price_next}, vol={next_vol}, TP=${next_expected_profit}")
                    active_price = place_pending_stop("BUY", buy_price_next, next_vol)
                    last_order_type = "BUY"

                last_pending_expected = next_expected_profit

            last_pos_count = curr_count
            last_positions = current_positions

        time.sleep(POLL_INTERVAL)

# ------------------- Main ------------------- #
def main():
    try:
        print("📊 25% Formula Table:")
        for row in formula25_table():
            print(row)
        vol_gen = formula25_generator()

        gap = None
        while gap is None:
            try:
                gap = float(input("Enter gap (distance between BUY and SELL in price units): ").strip())
            except ValueError:
                printl("Please input a numeric gap value.")

        run_cycle(vol_gen, gap)

    except KeyboardInterrupt:
        printl("🛑 Script stopped by user.")
    finally:
        mt5.shutdown()
        printl("MT5 connection closed.")

if __name__ == "__main__":
    main()
