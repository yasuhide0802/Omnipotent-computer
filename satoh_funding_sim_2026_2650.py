# -*- coding: utf-8 -*-
"""
Satoh Funding Simulator (2026 -> 2650)
資金が“自然に”流れて来る仕組みを、信頼(YSD)・実績(Impact)・
コミュニティ(Quadratic)・公共財(RetroFunding)・事業収益(Revenue)の
合成で年次シミュレーションする原型。

実行:
    python satoh_funding_sim_2026_2650.py

出力:
    - 主要年のダイジェスト
    - 年次CSV: funding_timeseries.csv
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple
import math, csv, random

# ---------------- 基本ユーティリティ ----------------

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

RNG = random.Random(42)  # 再現性

# ---------------- モデル構造 ----------------

@dataclass
class Streams:
    grants: float = 0.0          # 公的助成・財団
    donations: float = 0.0       # 個人/企業寄付
    matching: float = 0.0        # 二次資金(Quadratic Funding等)のマッチング
    revenue: float = 0.0         # 事業収益(採用→収益化)
    retro: float = 0.0           # レトロアクティブ公共財ファンディング
    cosmic: float = 0.0          # 宇宙交流由来の資金（2100以降の象徴レイヤ）

    def total(self) -> float:
        return self.grants + self.donations + self.matching + self.revenue + self.retro + self.cosmic

@dataclass
class State:
    year: int
    ysd_trust: float           # 信頼残高（YSDスコア）
    impact: float              # 社会/科学/霊性インパクト（滑らかに蓄積）
    adoption: float            # 採用率（0-1）
    debt_penalty: float        # 失敗や負債による罰則(>=0) 小さいほど良い
    liquidity: float           # 現金同等物
    streams: Streams = field(default_factory=Streams)

# ---------------- パラメータ（直感的に調整可能） ----------------

P = {
    # 信頼(YSD)→資金化の弾力性
    "trust_to_donation_k": 0.10,
    "trust_to_grant_k":    0.08,
    "trust_to_matching_k": 0.06,

    # 影響(Impact)→レトロ資金化の弾力性
    "impact_to_retro_k":   0.12,

    # 採用(Adoption)→収益
    "adopt_to_rev_base":   0.50,  # 基準収益係数
    "adopt_growth_bias":   0.02,  # 毎年の自然成長バイアス（採用側）

    # 信頼と影響の更新
    "ysd_inertia":         0.92,  # 信頼慣性（過去をどれだけ残すか）
    "impact_decay":        0.97,  # 影響の自然減衰
    "impact_gain_k":       0.15,  # 流入資金→影響増加の変換係数

    # 罰則
    "penalty_decay":       0.85,  # 罰則の自然解消
    "penalty_shock_prob":  0.06,  # 毎年の突発リスク確率
    "penalty_shock_max":   0.30,  # 突発罰則の最大

    # 二次資金（Quadratic）の強度（コミュニティ寄与が強くなる年には↑）
    "quadratic_base":      1.0,

    # レトロ資金の遅延（本年の影響ではなく、数年前の影響に後払い）
    "retro_delay":         3,

    # 宇宙レイヤ（2100〜）/ 象徴レイヤ（2650で通貨を超越）
    "cosmic_start":        2100,
    "cosmic_k":            0.05,
    "symbolic_2650_boost": 3.0,  # 2650年の象徴的増幅
}

# 過去影響のリングバッファ（レトロ資金用）
class ImpactMemory:
    def __init__(self, delay: int):
        self.delay = max(1, delay)
        self.buf = [0.0]*self.delay
        self.idx = 0
    def push(self, value: float):
        self.buf[self.idx] = value
        self.idx = (self.idx + 1) % self.delay
    def delayed(self) -> float:
        return self.buf[self.idx]  # ちょうどdelay年前

# ---------------- 資金生成ロジック ----------------

def compute_streams(s: State, t0: int) -> Streams:
    """
    現在の状態から、今年の各ストリームを計算。
    「自然流入」を設計意図として、信頼/影響/採用/罰則から内生的に決める。
    """
    # 有効信頼（罰則で減衰）
    eff_trust = clamp(s.ysd_trust * math.exp(-s.debt_penalty), 0.0, 1e12)

    # 助成・寄付・マッチング（YSDベース）
    grants    = eff_trust * P["trust_to_grant_k"]
    donations = eff_trust * P["trust_to_donation_k"]
    matching  = math.sqrt(donations) * math.sqrt(eff_trust) * P["trust_to_matching_k"] * P["quadratic_base"]

    # 収益（採用→収益）
    revenue   = s.adoption * P["adopt_to_rev_base"] * (1.0 + 0.2 * sigmoid(s.impact))

    # レトロ資金（外部で遅延管理）
    retro     = 0.0  # 外で後付け

    # 宇宙/象徴レイヤ（2100〜）
    cosmic = 0.0
    if s.year >= P["cosmic_start"]:
        cosmic = (eff_trust + s.impact) ** 0.5 * P["cosmic_k"]
        # 2650は象徴的に増幅（貨幣を超える：ここでは数値的ブーストとして表現）
        if s.year >= 2650:
            cosmic *= P["symbolic_2650_boost"]

    return Streams(
        grants=grants,
        donations=donations,
        matching=matching,
        revenue=revenue,
        retro=retro,
        cosmic=cosmic
    )

def update_dynamics(prev: State, streams: Streams, impact_mem: ImpactMemory) -> State:
    year = prev.year + 1

    # 罰則ショック（小さな事故や失敗を表現）
    debt_penalty = prev.debt_penalty * P["penalty_decay"]
    if RNG.random() < P["penalty_shock_prob"]:
        debt_penalty += RNG.uniform(0.0, P["penalty_shock_max"])

    # レトロ資金は delay 年前の impact から
    retro_base = impact_mem.delayed()
    retro = max(0.0, retro_base) * P["impact_to_retro_k"]

    # adoption は信頼・影響・収益から内生的に増える（上限1.0）
    adopt_growth = P["adopt_growth_bias"] + 0.04*sigmoid(prev.ysd_trust/100.0) + 0.08*sigmoid(prev.impact)
    adoption = clamp(prev.adoption + adopt_growth*(1.0 - prev.adoption), 0.0, 1.0)

    # 信頼は慣性＋今年の“善循環”（寄付・収益・レトロ）で増加、罰則で抑制
    trust_influx = 0.35*streams.donations + 0.25*streams.revenue + 0.40*retro
    ysd_trust = P["ysd_inertia"]*prev.ysd_trust + trust_influx
    ysd_trust = ysd_trust * math.exp(-0.3*debt_penalty)

    # 影響は自然減衰 + 投資で成長（収益/レトロ/助成に反応）
    invest = streams.grants + streams.revenue + retro + streams.matching
    impact = prev.impact*P["impact_decay"] + P["impact_gain_k"]*math.log1p(invest)

    # 流動性は各ストリーム合計＋（レトロ）を追加
    liquidity = prev.liquidity + streams.total() + retro

    # レトロ値を今年のimpactで更新（来年以降に効く）
    impact_mem.push(impact)

    # 今年のストリームに retro を反映（後付け）
    streams.retro = retro

    return State(
        year=year,
        ysd_trust=ysd_trust,
        impact=impact,
        adoption=adoption,
        debt_penalty=debt_penalty,
        liquidity=liquidity,
        streams=streams
    )

# ---------------- 初期条件とラン --------------------------------

def init_state(start_year: int = 2026) -> Tuple[State, ImpactMemory]:
    s0 = State(
        year=start_year,
        ysd_trust=8.0,       # 学術・地域貢献で芽生えた初期信頼
        impact=1.0,          # 初期の社会/学術インパクト
        adoption=0.02,       # まだ初期採用
        debt_penalty=0.0,    # 罰則なし
        liquidity=0.6        # 数百万円〜程度の換算（任意単位）
    )
    mem = ImpactMemory(P["retro_delay"])
    mem.push(s0.impact)
    return s0, mem

def simulate(start: int = 2026, end: int = 2650) -> List[State]:
    st, mem = init_state(start)
    out = [st]
    # 初年のストリームを先に計算してから進める
    for y in range(start, end):
        streams = compute_streams(out[-1], start)
        nxt = update_dynamics(out[-1], streams, mem)
        out.append(nxt)
    return out

# ---------------- 実行と結果出力 ----------------

def dump_csv(series: List[State], path: str = "funding_timeseries.csv"):
    keys = ["year","ysd_trust","impact","adoption","debt_penalty","liquidity",
            "grants","donations","matching","revenue","retro","cosmic","total_inflow"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(keys)
        for s in series:
            row = [
                s.year, round(s.ysd_trust,4), round(s.impact,4), round(s.adoption,4),
                round(s.debt_penalty,4), round(s.liquidity,4),
                round(s.streams.grants,4), round(s.streams.donations,4),
                round(s.streams.matching,4), round(s.streams.revenue,4),
                round(s.streams.retro,4), round(s.streams.cosmic,4),
                round(s.streams.total() + s.streams.retro,4)
            ]
            w.writerow(row)

def snapshot(series: List[State], years: List[int]) -> Dict[int, State]:
    idx = {s.year: s for s in series}
    return {y: idx.get(y) for y in years if y in idx}

def human_readable_money(x: float) -> str:
    """
    単位は“抽象値”だが、ざっくり人間可読に。
    初期0.6 ≒ 数百万円、1.0 ≒ 約1000万円イメージ。
    時代が進むと指数的に大きくなるので桁区切り表示だけ整える。
    """
    return f"{x:,.2f} units"

if __name__ == "__main__":
    series = simulate(2026, 2650)
    dump_csv(series)

    snaps = snapshot(series, [2026, 2030, 2050, 2100, 2200, 2500, 2650])
    print("=== Satoh Funding Simulator — Key Milestones ===")
    for y, s in snaps.items():
        tot = s.streams.total() + s.streams.retro
        print(f"\n[{y}]")
        print(f"  Trust(YSD):     {s.ysd_trust:.2f}")
        print(f"  Impact:         {s.impact:.2f}")
        print(f"  Adoption:       {s.adoption:.2%}")
        print(f"  DebtPenalty:    {s.debt_penalty:.2f}")
        print(f"  Liquidity:      {human_readable_money(s.liquidity)}")
        print(f"  Inflow (yr):    {tot:.2f} (grants {s.streams.grants:.2f}, donations {s.streams.donations:.2f}, "
              f"match {s.streams.matching:.2f}, revenue {s.streams.revenue:.2f}, retro {s.streams.retro:.2f}, cosmic {s.streams.cosmic:.2f})")

    print("\nCSV exported -> funding_timeseries.csv")
