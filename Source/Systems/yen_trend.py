from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class YenTrendState:
    current_date: Optional[str] = None
    today_open: Optional[float] = None


def update_today_open(state: YenTrendState, latest_price: float) -> None:
    """
    日付が変わったら、その時点の価格を当日の始値として保持する。
    """
    today = datetime.now().strftime("%Y-%m-%d")
    if state.current_date != today:
        state.current_date = today
        state.today_open = latest_price


def judge_yen_trend(
    state: YenTrendState,
    current_price: float,
    neutral_threshold: float = 0.05
) -> str:
    """
    USD/JPY の当日始値と現在価格から円高/円安/中立を判定する。

    neutral_threshold:
        中立とみなす価格差。0.05 なら 5銭以内は中立。
    """
    if state.today_open is None:
        return "不明"

    diff = current_price - state.today_open

    if abs(diff) <= neutral_threshold:
        return "中立"
    if diff > 0:
        return "円安"   # ドル円上昇
    return "円高"       # ドル円下落


def is_reverse_direction(yen_trend: str, signal: str) -> bool:
    """
    円高/円安と売買シグナルが逆行しているか判定する。
    signal は 'BUY' or 'SELL' を想定。
    """
    if yen_trend == "円高" and signal == "BUY":
        return True
    if yen_trend == "円安" and signal == "SELL":
        return True
    return False