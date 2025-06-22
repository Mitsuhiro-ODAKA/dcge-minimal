# model/dcge_model.py

import pandas as pd
import gamspy as gp
from gamspy import (
    Container, Set, Parameter, Variable,
    Equation, Model, Sense, Problem, Sum
)

def build_static_cge(sam_path):
    """
    ベース年 SAM から静的 CGE を解き、
    家計消費シェア (dict) と投資率 (float) を返す。
    """
    # ── SAM 読み込み ──────────────────────────────────────────────
    sam = pd.read_csv(sam_path, index_col=0)

    # ── Container & Sets ─────────────────────────────────────────
    m    = Container()
    comm = Set(m, "comm", records=["Agri", "Manu"])

    # ── 家計消費シェア算出 ────────────────────────────────────────
    hh = sam.loc["Household", comm.records].astype(float)
    total_hh = hh.sum()
    cons_share = { c: hh[c] / total_hh for c in comm.records }

    # ── 総付加価値（VA）と投資率算出 ───────────────────────────────
    va = sam.loc["ValueAdded", comm.records].astype(float)
    total_va = va.sum()
    inv = sam.loc["Investment", comm.records].astype(float).sum()
    inv_share = inv / total_va

    # ── Parameters ────────────────────────────────────────────────
    p_cshare = Parameter(
        m, name="cons_share", domain=[comm],
        records=[(c, cons_share[c]) for c in comm.records]
    )
    p_ishare = Parameter(m, name="inv_share")
    p_ishare[...] = inv_share

    # ── Variables ─────────────────────────────────────────────────
    C = Variable(m, name="C", domain=[comm])  # 各財の消費
    I = Variable(m, name="I")                 # 総投資

    # ── Equations ────────────────────────────────────────────────
    eqs = []

    # 1) 財市場クリア： C[c] = cons_share[c] * (VA_total - I)
    goods_eq = Equation(m, name="goods_eq", domain=[comm])
    for c in comm.records:
        goods_eq[c] = (
            C[c] == p_cshare[c] * (total_va - I[...])
        )
    eqs.append(goods_eq)

    # 2) 投資恒等式： I = inv_share * VA_total
    inv_eq = Equation(m, name="inv_eq")
    inv_eq[...] = (
        I[...] == p_ishare[...] * total_va
    )
    eqs.append(inv_eq)

    # ── モデル solve ──────────────────────────────────────────────
    model = Model(
        m,
        name="static_cge",
        equations=eqs,
        problem=Problem.LP,
        sense=Sense.MAX,
        objective=Sum((comm,), C)
    )
    sol = model.solve()

    # ── 結果取り出し ─────────────────────────────────────────────
    C_res = { c: C.records[(c,)] for c in comm.records }
    I_res = I.records[()]

    return sol, C_res, I_res
