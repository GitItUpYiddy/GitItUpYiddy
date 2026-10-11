"""
🌙 Strategy Stress-Test Gate (Research -> BACKTEST GATE -> Incubate)

A strategy must pass every check here before it gets tiny live size.
pandas + numpy only. Real data only: reads the OHLCV CSV, never generates prices.

Checks:
  1. Look-ahead detector   signals must not change when future bars are removed
  2. Out-of-sample         params picked on the first 70%, frozen, judged on the last 30% after fees
  3. Trade count           enough OOS trades to mean anything
  4. Random-entry control  must beat random entries with the same trade count and hold time
  5. Parameter neighbors   nearby settings must also work (not one lucky knob)
  6. Multi-slice           must hold up across timeframes and separate time windows

Execution model: decide on bar t close, fill at bar t+1 open. Fees + slippage charged per side.

Usage:
  python src/scripts/stress_test.py                     # stress test sma_cross on the sample data
  python src/scripts/stress_test.py --strategy rsi_revert
  python src/scripts/stress_test.py --selftest          # prove the gate can fail
"""
import argparse
import itertools
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "rbi", "BTC-USD-15m.csv"))
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "stress_test"))

# Gate settings (all adjustable)
FEE = 0.001             # 0.10% per side (typical taker fee)
SLIPPAGE = 0.0005       # 0.05% per side
IS_FRACTION = 0.70      # in-sample share used to pick params
MIN_OOS_TRADES = 30
RANDOM_SEEDS = 300
RANDOM_PERCENTILE = 95  # must beat this percentile of random-entry results
MIN_NEIGHBOR_PASS = 0.75
MIN_SLICE_PASS = 0.60
TIMEFRAMES = ["15min", "1h", "4h"]
WINDOWS = 4


# ---------- data ----------

def load_ohlcv(path=DATA_PATH):
    df = pd.read_csv(path, skipinitialspace=True)
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df.columns = [c.strip().lower() for c in df.columns]
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.set_index("datetime").sort_index()


def resample(df, rule):
    if rule == "15min":
        return df
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    return df.resample(rule).agg(agg).dropna()


def bars_per_year(df):
    minutes = (df.index[1] - df.index[0]).total_seconds() / 60
    return 365 * 24 * 60 / minutes


# ---------- strategies: return a 0/1 long-flat position decided at each bar's close ----------

def sma_cross(df, fast=20, slow=100):
    c = df["close"]
    return (c.rolling(fast).mean() > c.rolling(slow).mean()).astype(int)


def rsi_revert(df, length=14, entry=30, exit=55):
    delta = df["close"].diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / length, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / length, adjust=False).mean()
    rsi = 100 - 100 / (1 + gain / loss)
    pos = pd.Series(np.nan, index=df.index)
    pos[rsi < entry] = 1
    pos[rsi > exit] = 0
    return pos.ffill().fillna(0).astype(int)


def buy_and_hold(df):
    return pd.Series(1, index=df.index)


def peek_cheater(df):
    """Deliberately uses tomorrow's close. The look-ahead detector must flag this."""
    return (df["close"].shift(-1) > df["close"]).astype(int)


STRATEGIES = {
    "sma_cross": (sma_cross, {"fast": [10, 20, 30, 50], "slow": [100, 150, 200, 300]}),
    "rsi_revert": (rsi_revert, {"length": [7, 14, 21], "entry": [20, 25, 30, 35], "exit": [50, 55, 60]}),
}


# ---------- engine ----------

def backtest(df, pos, fee=FEE, slippage=SLIPPAGE):
    """pos[t] is decided at close t and held from open t+1 to open t+2."""
    held = pos.shift(1).fillna(0)
    open_to_open = df["open"].shift(-1) / df["open"] - 1
    cost = held.diff().abs().fillna(held.iloc[0]) * (fee + slippage)
    rets = (held * open_to_open - cost).fillna(0)
    equity = (1 + rets).cumprod()

    entries = (held.diff() == 1) | ((held.iloc[0] == 1) & (held.index == held.index[0]))
    n_trades = int(entries.sum())
    bars_in = int(held.sum())
    bpy = bars_per_year(df)
    sharpe = rets.mean() / rets.std() * np.sqrt(bpy) if rets.std() > 0 else 0.0
    return {
        "total_return": float(equity.iloc[-1] - 1),
        "sharpe": float(sharpe),
        "max_drawdown": float((equity / equity.cummax() - 1).min()),
        "trades": n_trades,
        "avg_hold_bars": bars_in / n_trades if n_trades else 0.0,
        "exposure": bars_in / len(held),
    }


def random_entry_returns(df, n_trades, hold, seeds=RANDOM_SEEDS):
    """Random long entries: same number of trades and same holding length, no overlap."""
    n, hold = len(df), max(1, int(round(hold)))
    n_trades = min(n_trades, (n - 2) // hold)
    if n_trades == 0:
        return np.array([0.0])
    rng = np.random.default_rng(42)
    slack = n - 1 - n_trades * hold
    out = []
    for _ in range(seeds):
        starts = np.sort(rng.choice(slack + 1, n_trades, replace=True)) + np.arange(n_trades) * hold
        pos = np.zeros(n, dtype=int)
        for s in starts:
            pos[s:s + hold] = 1
        out.append(backtest(df, pd.Series(pos, index=df.index))["total_return"])
    return np.array(out)


# ---------- checks ----------

def lookahead_check(fn, df, params, cutoffs=(0.5, 0.7, 0.9)):
    full = fn(df, **params)
    bad = []
    for f in cutoffs:
        c = int(len(df) * f)
        part = fn(df.iloc[:c], **params)
        if not part.equals(full.iloc[:c]):
            first = part.index[(part != full.iloc[:c]).values][0]
            bad.append(f"signal at {first} changes when later data is removed (cutoff {int(f * 100)}%)")
    return bad


def neighbors(grid, best):
    keys = list(grid)
    out = []
    for k in keys:
        i = grid[k].index(best[k])
        for j in (i - 1, i + 1):
            if 0 <= j < len(grid[k]):
                out.append({**best, k: grid[k][j]})
    return out


def valid(params):
    return not ("fast" in params and params["fast"] >= params["slow"]) and \
           not ("entry" in params and params["entry"] >= params["exit"])


def stress_test(name, fn, grid, df):
    split = int(len(df) * IS_FRACTION)
    is_df, oos_df = df.iloc[:split], df.iloc[split:]
    checks = []

    # pick params on in-sample only
    combos = [dict(zip(grid, v)) for v in itertools.product(*grid.values())]
    combos = [p for p in combos if valid(p)]
    scored = [(backtest(is_df, fn(is_df, **p))["total_return"], p) for p in combos]
    best = max(scored, key=lambda x: x[0])[1]

    # 1. look-ahead
    leaks = lookahead_check(fn, df, best)
    checks.append(("lookahead", not leaks, leaks[0] if leaks else "signals are stable when future bars are removed"))

    # 2. out-of-sample after costs (indicators warm up on in-sample history, then scored on OOS only)
    full_pos = fn(df, **best)
    oos = backtest(oos_df, full_pos.iloc[split:])
    bh = backtest(oos_df, buy_and_hold(oos_df))
    checks.append(("out_of_sample", oos["total_return"] > 0,
                   f"OOS return {oos['total_return']:+.1%} after costs (buy & hold {bh['total_return']:+.1%})"))

    # 3. trade count
    checks.append(("trade_count", oos["trades"] >= MIN_OOS_TRADES,
                   f"{oos['trades']} OOS trades (need {MIN_OOS_TRADES})"))

    # 4. random-entry control
    rand = random_entry_returns(oos_df, oos["trades"], oos["avg_hold_bars"])
    pct = float((rand < oos["total_return"]).mean() * 100)
    checks.append(("random_control", pct >= RANDOM_PERCENTILE,
                   f"beats {pct:.0f}% of {len(rand)} random-entry runs (need {RANDOM_PERCENTILE}%; random median {np.median(rand):+.1%})"))

    # 5. parameter neighbors
    nb = [p for p in neighbors(grid, best) if valid(p)]
    nb_ok = sum(backtest(oos_df, fn(df, **p).iloc[split:])["total_return"] > 0 for p in nb)
    frac = nb_ok / len(nb) if nb else 0.0
    checks.append(("param_neighbors", frac >= MIN_NEIGHBOR_PASS,
                   f"{nb_ok}/{len(nb)} neighboring settings profitable OOS (need {MIN_NEIGHBOR_PASS:.0%})"))

    # 6. timeframes x time windows
    slices = []
    for tf in TIMEFRAMES:
        tdf = resample(df, tf)
        tpos = fn(tdf, **best)
        for w, idx in enumerate(np.array_split(np.arange(len(tdf)), WINDOWS)):
            r = backtest(tdf.iloc[idx], tpos.iloc[idx])
            b = backtest(tdf.iloc[idx], buy_and_hold(tdf.iloc[idx]))
            slices.append({"timeframe": tf, "window": w + 1, "start": str(tdf.index[idx[0]].date()),
                           "return": r["total_return"], "buy_hold": b["total_return"], "trades": r["trades"]})
    s_ok = sum(s["return"] > 0 for s in slices)
    checks.append(("multi_slice", s_ok / len(slices) >= MIN_SLICE_PASS,
                   f"{s_ok}/{len(slices)} timeframe/window slices profitable (need {MIN_SLICE_PASS:.0%})"))

    passed = all(ok for _, ok, _ in checks)
    return {
        "strategy": name, "params": best, "verdict": "PASS" if passed else "FAIL",
        "data": {"file": os.path.basename(DATA_PATH), "start": str(df.index[0]), "end": str(df.index[-1]),
                 "bars": len(df), "buy_hold_full_period": backtest(df, buy_and_hold(df))["total_return"],
                 "note": "one asset over one period, sliced by timeframe and window; not independent datasets"},
        "costs": {"fee_per_side": FEE, "slippage_per_side": SLIPPAGE},
        "oos": oos, "oos_buy_hold": bh,
        "checks": [{"check": c, "pass": bool(ok), "detail": d} for c, ok, d in checks],
        "slices": slices,
    }


def print_report(r):
    print(f"\n🌙 Stress test: {r['strategy']} {r['params']}")
    d = r["data"]
    print(f"   data: {d['file']} {d['start'][:10]} → {d['end'][:10]} ({d['bars']} bars), buy & hold {d['buy_hold_full_period']:+.1%}")
    print(f"   ⚠️  {d['note']}")
    for c in r["checks"]:
        print(f"   {'✅' if c['pass'] else '❌'} {c['check']:<16} {c['detail']}")
    print(f"   VERDICT: {r['verdict']}\n")


def save(r):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{r['strategy']}_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(path, "w") as f:
        json.dump(r, f, indent=2, default=str)
    return path


def selftest(df):
    """The gate is only trustworthy if it can fail. Each of these must hold."""
    results = []

    leaks = lookahead_check(peek_cheater, df, {})
    results.append(("look-ahead detector flags a future-peeking strategy", bool(leaks)))

    clean = lookahead_check(sma_cross, df, {"fast": 20, "slow": 100})
    results.append(("look-ahead detector passes an honest strategy", not clean))

    with_fee = backtest(df, buy_and_hold(df))["total_return"]
    no_fee = backtest(df, buy_and_hold(df), fee=0, slippage=0)["total_return"]
    results.append(("fees reduce buy & hold return", with_fee < no_fee))

    split = int(len(df) * IS_FRACTION)
    oos_df = df.iloc[split:]
    rng = np.random.default_rng(7)
    coin = pd.Series(rng.integers(0, 2, len(oos_df)), index=oos_df.index)
    r = backtest(oos_df, coin)
    rand = random_entry_returns(oos_df, r["trades"], r["avg_hold_bars"])
    pct = (rand < r["total_return"]).mean() * 100
    results.append((f"coin-flip strategy fails random control (beat {pct:.0f}%)", pct < RANDOM_PERCENTILE))

    print("\n🧪 Gate self-test")
    for name, ok in results:
        print(f"   {'✅' if ok else '❌'} {name}")
    ok = all(ok for _, ok in results)
    print(f"   {'GATE CAN FAIL: trustworthy' if ok else 'GATE IS BROKEN: do not trust its PASS results'}\n")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", default="sma_cross", choices=list(STRATEGIES))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    df = load_ohlcv()
    if args.selftest:
        raise SystemExit(0 if selftest(df) else 1)
    fn, grid = STRATEGIES[args.strategy]
    report = stress_test(args.strategy, fn, grid, df)
    print_report(report)
    print(f"   saved: {save(report)}")
