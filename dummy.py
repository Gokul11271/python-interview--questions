import MetaTrader5 as mt5
import time
from datetime import datetime
import math
import pygame

# Reference image (uploaded): /mnt/data/182f41c6-6fac-47e7-ba96-53e8b93b8cad.png

# ------------------- Config ------------------- #
SYMBOL = "XAUUSD_"    # trading symbol (must match your MT5 symbol name)
SLIPPAGE = 500
MAGIC = 12345
LOSS_TARGET = 500.0       # equity loss stop (in $)
PROFIT_UNIT = 60          # profit per volume unit for TP calculation

# ---------------- SELL/GAP configuration ---------------- #
SELL_GAP = 1              # integer gap for SELL (we add sell_step each BUY trigger)
# ------------------------------------------------------------------- #

# ------------------- Globals ------------------- #
order_log = []
base_buy_price = None     # anchor BUY price (float), decimal locked from this
fixed_decimal = None      # fractional part locked
sell_step = 1             # unused in new pattern but kept for compatibility
sell_next_price = None

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

# Volume limits (fallbacks)
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

# ------------------- sound Generator ------------------- #
def play_mp3_repeat(file_path, repeat=2, gap=0.1, label="🔊 Custom Sound"):
    try:
        print(f"{label} (×{repeat})")
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        for _ in range(repeat):
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            time.sleep(gap)
    except Exception as e:
        printl("⚠️ Sound playback failed:", e)

# ------------------- Volume Generator ------------------- #
def volume_pattern_generator():
    pattern = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
    for vol in pattern:
        yield vol
    while True:
        yield 0.10

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
        print("\n📊 Trading Summary (pattern price shown as integer):")
        print(f"{'Order':<6} {'Ticket':<10} {'Type':<6} {'Volume':<8} {'Pattern':<8} {'ActualClose':<12}")
        print("-" * 70)
        for i, entry in enumerate(order_log, 1):
            ticket = entry.get("ticket", "")
            typ = entry.get("type", "")
            vol = entry.get("volume", "")
            patt = entry.get("pattern_price", "")
            actual_close = entry.get("actual_close", "")
            print(f"{i:<6} {ticket:<10} {typ:<6} {vol:<8} {patt:<8} {actual_close:<12}")
        print("-" * 70)
        print(f"✅ Total Orders: {len(order_log)}\n")

def place_pending_stop(order_side: str, base_price: float, volume: float, max_attempts=0, delay=1.0):
    """
    Places a pending BUY_STOP or SELL_STOP at base_price, but enforces broker stop_level
    and retries until success (or until max_attempts > 0 is reached).
    Returns placed price (rounded) or None on failure.
    """
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

# ------------------- Trading Cycle (NEW pattern per your table) ------------------- #
def run_cycle(vol_gen):
    global base_buy_price, fixed_decimal, sell_step, sell_next_price

    tick = mt5.symbol_info_tick(SYMBOL)
    if not tick:
        printl("❌ No tick data available. Cannot run cycle.")
        return "error"

    # 1) Compute & place the anchor BUY STOP candidate (we won't wait for it to trigger first)
    base_ask = tick.ask
    min_buy_stop = base_ask + stop_level + (2 * point)
    candidate_buy = round(min_buy_stop, digits)

    first_vol = next(vol_gen)
    cumulative_tp = first_vol * PROFIT_UNIT

    printl(f"🟢 Candidate base BUY STOP computed at {candidate_buy} (market ask={base_ask})")
    # We do not necessarily place BUY first; we use this as our anchor and lock decimals from it.
    base_buy_price = candidate_buy
    fixed_decimal = base_buy_price - int(base_buy_price)
    base_int = int(base_buy_price)
    printl(f"🔒 base_buy_price anchor set to {base_buy_price} | fixed_decimal = {fixed_decimal}")

    # 2) Place initial SELL STOP at base_int + fixed_decimal (adjust to broker limits)
    init_sell_price_candidate = base_int + fixed_decimal

    # Ensure candidate SELL is <= broker allowed max (tick.bid - stop_level - 2*point)
    tick_now = mt5.symbol_info_tick(SYMBOL)
    if not tick_now:
        printl("❌ No tick available to place initial SELL.")
        return "error"
    max_allowed_sell = tick_now.bid - stop_level - (2 * point)
    if init_sell_price_candidate > max_allowed_sell:
        # preserve decimal if possible by lowering integer
        allowed_max = max_allowed_sell - (1 * point)
        allowed_int = int(math.floor(allowed_max - fixed_decimal))
        init_sell_price_candidate = allowed_int + fixed_decimal

    init_sell_price = round(init_sell_price_candidate, digits)
    first_vol = normalize_volume(first_vol)
    placed = place_pending_stop("SELL", init_sell_price, first_vol)
    if not placed:
        printl("❌ Could not place initial SELL STOP.")
        return "error"

    sell_next_price = placed
    printl(f"🔁 Initial SELL STOP placed at {placed}. Now waiting for triggers...")

    # prepare loop state
    last_positions = mt5.positions_get(symbol=SYMBOL) or []
    last_pos_count = len(last_positions)
    baseline_equity = account_equity_profit()
    triggered_count = 0
    last_trigger_info = None

    printl(f"📌 Baseline equity set at {baseline_equity:.2f}")
    printl(f"💰 Initial cumulative TP target = ${cumulative_tp:.2f}\n")

    # MAIN LOOP
    while True:
        ai = mt5.account_info()
        if ai:
            print(f"\r💵 Balance: {ai.balance:.2f} | 📊 Profit: {ai.profit:+.2f} | 🎯 TP Target: {cumulative_tp:.2f}", end="", flush=True)

        acc_profit = account_equity_profit()
        positions = mt5.positions_get(symbol=SYMBOL) or []

        if not positions:
            time.sleep(0.5)
            continue

        current_count = len(positions)
        if current_count > last_pos_count:
            last_ticket_set = set([lp.ticket for lp in last_positions])
            new_positions = [p for p in positions if p.ticket not in last_ticket_set]
            for pos in new_positions:
                triggered_count += 1

                cur_total_profit = account_equity_profit() - baseline_equity
                pos_type_str = "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL"
                actual_open = getattr(pos, "price_open", "N/A")

                printl(f"\n\n🔔 Trigger #{triggered_count} → ticket={pos.ticket}, type={pos_type_str}, vol={pos.volume}, open_price={actual_open}")

                # If cumulative TP reached, close and exit
                if cur_total_profit >= cumulative_tp:
                    last_trigger_info = {
                        "ticket": pos.ticket,
                        "type": pos_type_str,
                        "volume": pos.volume,
                        "open_price": actual_open,
                        "account_balance": account_balance(),
                        "account_profit": account_equity_profit(),
                        "cumulative_tp_target": cumulative_tp
                    }
                    printl(f"🎯 This position caused TP to be reached! Profit={cur_total_profit:.2f} ≥ Target={cumulative_tp:.2f}")
                    printl(f"📌 Triggering position details: {last_trigger_info}")
                    close_all_positions()
                    return "profit"

                # Log pattern integer for readability
                if pos.type == mt5.POSITION_TYPE_BUY:
                    pattern_price_display = base_int + sell_step
                else:
                    pattern_price_display = base_int

                order_log.append({
                    "ticket": pos.ticket,
                    "type": pos_type_str,
                    "volume": pos.volume,
                    "cumulative_tp": cumulative_tp,
                    "pattern_price": pattern_price_display,
                    "actual_close": getattr(pos, "price_open", "")
                })

                # next volume & TP update
                next_vol = next(vol_gen)
                cumulative_tp += next_vol * PROFIT_UNIT

                # ------------------ NEW PATTERN LOGIC (REQUESTED) ------------------
                # Pattern:
                #   When a SELL triggers -> next is BUY at base_int + triggered_count (4001,4002,...)
                #   When a BUY triggers  -> next is SELL at base_int (always 4000)
                if pos.type == mt5.POSITION_TYPE_SELL:
                    # SELL triggered → next is BUY
                    next_side = "BUY"


                    # BUY integer increases sequentially: base_int + triggered_count
                    buy_int = base_int + triggered_count   # 4001, 4002, ...
                    candidate_price = buy_int + fixed_decimal
                    

                    # ensure bro  ker limits for BUY
                    tickc = mt5.symbol_info_tick(SYMBOL)
                    if not tickc:
                        printl("❌ No tick available while computing BUY price.")
                        return "error"
                    min_allowed_buy = tickc.ask + stop_level + (2 * point)
                    if candidate_price < min_allowed_buy:
                        buy_int = int(math.ceil(min_allowed_buy - fixed_decimal))
                        candidate_price = buy_int + fixed_decimal

                    next_price = round(candidate_price, digits)
                    printl(f"📈 Next BUY STOP at {next_price} | vol={next_vol} | New TP={cumulative_tp:.2f}")

                else:
                    # BUY triggered → next is SELL
                    next_side = "SELL"

                    # SELL always returns to base_int
                    sell_int = base_int
                    candidate_price = sell_int + fixed_decimal

                    tickc = mt5.symbol_info_tick(SYMBOL)
                    if not tickc:
                        printl("❌ No tick available while computing SELL price.")
                        return "error"
                    max_allowed_sell = tickc.bid - stop_level - (2 * point)
                    if candidate_price > max_allowed_sell:
                        sell_int = int(math.floor(max_allowed_sell - fixed_decimal))
                        candidate_price = sell_int + fixed_decimal

                    next_price = round(candidate_price, digits)
                    printl(f"📈 Next SELL STOP at {next_price} | vol={next_vol} | New TP={cumulative_tp:.2f}")
                # ------------------------------------------------------------

                active_price = place_pending_stop(next_side, next_price, next_vol)
                sell_next_price = active_price
                last_order_type = next_side

            last_pos_count = current_count
            last_positions = positions

        # Periodic safety checks
        total_profit = acc_profit - baseline_equity
        if total_profit >= cumulative_tp:
            printl(f"\n🎯 Cumulative TP reached on periodic check! Profit={total_profit:.2f} ≥ Target={cumulative_tp:.2f}")
            if not last_trigger_info:
                last_trigger_info = {
                    "ticket": None,
                    "type": None,
                    "volume": None,
                    "open_price": None,
                    "account_balance": account_balance(),
                    "account_profit": account_equity_profit(),
                    "cumulative_tp_target": cumulative_tp
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
        printl("🚀 Starting automated cycle (NEW pattern) — using base BUY anchor for decimals.")
        run_cycle(vol_gen)
    except KeyboardInterrupt:
        printl("🛑 Script stopped by user.")
    finally:
        mt5.shutdown()
        printl("MT5 connection closed.")

if __name__ == "__main__":
    main()
