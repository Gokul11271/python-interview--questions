import MetaTrader5 as mt5
import time
from datetime import datetime
import pygame

# ------------------- Config ------------------- #
SYMBOL = "XAUUSD_"    # trading symbol
SLIPPAGE = 500
MAGIC = 12345
LOSS_TARGET = 500.0       # equity loss stop (in $)
PROFIT_UNIT = 50          # profit per volume unit for TP calculation

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

# ------------------- sound Generator (hardcoded) ------------------- #
def play_mp3_repeat(file_path, repeat=2, gap=0.1, label="🔊 Custom Sound"):
    print(f"{label} (×{repeat})")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        for _ in range(repeat):
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(gap)
    except Exception as e:
        printl("⚠️ Sound play failed:", e)

# ------------------- Volume Generator (hardcoded) ------------------- #
def volume_pattern_generator():
    pattern = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
    for vol in pattern:
        yield vol
    while True:
        yield 0.06  # continue with 0.06 for all remaining orders

def account_balance():
    ai = mt5.account_info()
    return ai.balance if ai else 0.0

def account_equity_profit():
    ai = mt5.account_info()
    if ai:
        return ai.profit
    return 0.0

# ------------------- Order Helpers ------------------- #
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
    if positions:
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
    play_mp3_repeat(r"C:\Users\hp\Downloads\cash-register-purchase-87313.mp3", repeat=2, label="💰 Profit Sound")

    if order_log:
        print("\n📊 Trading Summary:")
        print(f"{'Ticket':<10} {'Type':<6} {'Volume':<8} {'Cumulative TP':<12}")
        print("-" * 50)
        for entry in order_log:
            print(f"{entry['ticket']:<10} {entry['type']:<6} {entry['volume']:<8} {entry['cumulative_tp']:<12}")
        print("-" * 50)
        print(f"✅ Total Orders: {len(order_log)}\n")

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
            printl(f"✅ {order_side} STOP placed at {price} vol={volume} (attempts={attempt})")
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

    # first pending volume (used to place first pending)
    first_vol = next(vol_gen)

    # triggered_cum_tp tracks only **triggered** positions (starts at 0)
    triggered_cum_tp = 0.0
    # projected shows what TP would be after placing the next pending (informational)
    projected_cum_tp = first_vol * PROFIT_UNIT

    active_price = place_pending_stop("BUY", buy_price, first_vol)
    if not active_price:
        return "error"

    last_buy_price = buy_price
    last_order_type = "BUY"
    last_positions = mt5.positions_get(symbol=SYMBOL) or []
    last_pos_count = len(last_positions)
    baseline_equity = account_equity_profit()
    triggered_count = 0
    last_trigger_info = None

    printl(f"📌 Baseline equity set at {baseline_equity:.2f}")
    printl(f"💰 Initial projected TP target (pending) = ${projected_cum_tp:.2f}\n")

    # ---------------- MAIN LOOP ----------------
    while True:
        time.sleep(1)  # refresh every second
        ai = mt5.account_info()
        if ai:
            # Show both triggered (actual) and projected (informational)
            print(f"\r💵 Balance: {ai.balance:.2f} | 📊 Profit: {ai.profit:+.2f} | 🎯 Triggered TP: {triggered_cum_tp:.2f} | ⏳ Projected TP: {projected_cum_tp:.2f}", end="", flush=True)

        acc_profit = account_equity_profit()
        positions = mt5.positions_get(symbol=SYMBOL) or []

        # Wait for first trigger
        if not positions:
            continue

        current_count = len(positions)
        if current_count > last_pos_count:
            # identify new positions compared to last snapshot
            last_ticket_set = set([lp.ticket for lp in last_positions])
            new_positions = [p for p in positions if p.ticket not in last_ticket_set]
            for pos in new_positions:
                triggered_count += 1

                pos_type_str = "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL"

                # IMPORTANT: when a new position triggers, add its contribution to triggered_cum_tp
                added_tp = (pos.volume or 0.0) * PROFIT_UNIT
                triggered_cum_tp += added_tp

                cur_total_profit = account_equity_profit() - baseline_equity

                printl(f"\n\n🔔 Trigger #{triggered_count} → ticket={pos.ticket}, AFTER adding this trigger TP contribution = ${triggered_cum_tp:.2f}"
                       f" type={pos_type_str}, vol={pos.volume}, open_price={getattr(pos, 'price_open', 'N/A')}")

                # If profit already meets or exceeds the triggered_cum_tp, mark this pos as the trigger and close.
                if cur_total_profit >= triggered_cum_tp:
                    last_trigger_info = {
                        "ticket": pos.ticket,
                        "type": pos_type_str,
                        "volume": pos.volume,
                        "open_price": getattr(pos, "price_open", None),
                        "account_balance": account_balance(),
                        "account_profit": account_equity_profit(),
                        "cumulative_tp_target": triggered_cum_tp
                    }
                    printl(f"🎯 This position caused TP to be reached! Profit={cur_total_profit:.2f} ≥ Target={triggered_cum_tp:.2f}")
                    printl(f"📌 Triggering position details: {last_trigger_info}")
                    # Close all positions and exit reporting 'profit'
                    close_all_positions()
                    return "profit"

                # log this triggered order with the triggered cumulative TP at that moment
                order_log.append({
                    "ticket": pos.ticket,
                    "type": pos_type_str,
                    "volume": pos.volume,
                    "cumulative_tp": triggered_cum_tp
                })

                # compute next pending volume and projected TP (projected = triggered_cum_tp + next_vol*PROFIT_UNIT)
                next_vol = next(vol_gen)
                projected_cum_tp = triggered_cum_tp + next_vol * PROFIT_UNIT

                # Alternating GAP logic to decide next side/price
                if pos.type == mt5.POSITION_TYPE_BUY:
                    last_buy_price = pos.price_open
                    next_side = "SELL"
                    next_price = round(last_buy_price - gap, digits)
                else:
                    next_side = "BUY"
                    last_buy_price = round(last_buy_price + gap, digits)
                    next_price = last_buy_price

                printl(f"📈 Next {next_side} STOP placed at {next_price} (next vol={next_vol}, projected TP target={projected_cum_tp:.2f})")
                active_price = place_pending_stop(next_side, next_price, next_vol)
                last_order_type = next_side

            last_pos_count = current_count
            last_positions = positions

        # Periodic full TP/SL safety checks (in case TP achieved outside a trigger loop)
        total_profit = acc_profit - baseline_equity
        if total_profit >= triggered_cum_tp and triggered_cum_tp > 0.0:
            printl(f"\n🎯 Cumulative (triggered) TP reached on periodic check! Profit={total_profit:.2f} ≥ Target={triggered_cum_tp:.2f}")
            if not last_trigger_info:
                last_trigger_info = {
                    "ticket": None,
                    "type": None,
                    "volume": None,
                    "open_price": None,
                    "account_balance": account_balance(),
                    "account_profit": account_equity_profit(),
                    "cumulative_tp_target": triggered_cum_tp
                }
                printl("📌 TP hit but trigger position not identified in loop (maybe was closed externally).")
                printl(f"📌 Account state: {last_trigger_info}")
            close_all_positions()
            return "profit"
        if total_profit <= -LOSS_TARGET:
            printl(f"\n❌ SL hit! Profit={total_profit:.2f} ≤ -{LOSS_TARGET}")
            close_all_positions()
            return "loss"

# ------------------- Main ------------------- #
def main():
    try:
        vol_gen = volume_pattern_generator()
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
