#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XY Protocol Demo — 让 NPC 永远记住你
=====================================
3 个数字生命体（NPC），7 个事件，因果链驱动性格演化。

零依赖：Python 3.8+ 直接运行
    python3 demo.py

核心机制：
  1. 因果链（Causal Chain）：append-only + 哈希指针链式校验
  2. 性格加权决策：记忆检索 -> 性格触发 -> 行为输出
  3. 闭环反馈：事件类型 -> 性格微调 -> 行为变化
  4. 群体异步广播：个体链 -> 群体链 -> 信息不对称涌现
"""

import hashlib
import json
import uuid
from datetime import datetime
import copy


# ============================================================
# 1. 因果链（Causal Chain）
# ============================================================

class Event:
    """单条事件记录，哈希指针链式连接"""

    def __init__(self, event_type, initiator_id, receiver_id, params, timestamp=None):
        self.event_id = uuid.uuid4().hex[:16]
        self.event_type = event_type
        self.initiator_id = initiator_id
        self.receiver_id = receiver_id
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        self.params = params
        self.prev_hash = None
        self.self_hash = None

    def compute_hash(self):
        payload = json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type,
            "initiator_id": self.initiator_id,
            "receiver_id": self.receiver_id,
            "timestamp": self.timestamp,
            "params": self.params,
            "prev_hash": self.prev_hash,
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class CausalChain:
    """只可追加的因果链，任何篡改都会导致哈希链断裂"""

    GENESIS = "0" * 64

    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.events = []
        self.prev_hash = self.GENESIS

    def append(self, event):
        ev = copy.deepcopy(event)
        ev.prev_hash = self.prev_hash
        ev.self_hash = ev.compute_hash()
        self.events.append(ev)
        self.prev_hash = ev.self_hash
        return ev

    def verify(self):
        prev = self.GENESIS
        for e in self.events:
            if e.prev_hash != prev or e.self_hash != e.compute_hash():
                return False
            prev = e.self_hash
        return True

    def __len__(self):
        return len(self.events)


# ============================================================
# 2. 数字生命体（Digital Life Form）
# ============================================================

class DigitalLifeForm:
    """具备独立记忆、唯一身份、时序行为记录的数字生命体"""

    # 事件类型 -> 性格微调权重（闭环反馈）
    PERSONALITY_DELTA = {
        "trespass":  {"suspicion": +0.05, "coldness": +0.02},
        "threat":    {"suspicion": +0.08, "coldness": +0.05, "kindness": -0.05},
        "observe":   {"suspicion": +0.02},
        "friendly":  {"kindness": +0.05, "suspicion": -0.05, "coldness": -0.03},
        "gift":      {"kindness": +0.05, "suspicion": -0.05},
        "reconcile": {"kindness": +0.05, "suspicion": -0.05, "coldness": -0.05},
        "broadcast": {},
    }

    def __init__(self, npc_id, name, personality, memories):
        self.npc_id = npc_id
        self.name = name
        self.personality = personality  # {"kindness":.., "suspicion":.., "coldness":..}
        self.memories = memories        # 初始记忆（历史背景）
        self.chain = CausalChain(npc_id)

    def recall(self, keywords):
        """按关键词检索相关记忆"""
        return [m for m in self.memories if any(k in m for k in keywords)]

    def decide(self, event):
        """性格加权决策：返回 (记忆行, 决策行)"""
        hits = self.recall(event.params.get("keywords", []))
        mem_line = f"检索到记忆：{hits[0]}" if hits else "无相关记忆"
        if self.personality["kindness"] >= self.personality["suspicion"]:
            action = event.params.get("kind_action", "友善回应")
        else:
            action = event.params.get("suspicious_action", "戒备观察")
        return mem_line, action

    def adjust_personality(self, event):
        """闭环反馈：事件类型 -> 性格微调，返回变化字典"""
        delta = self.PERSONALITY_DELTA.get(event.event_type, {})
        changes = {}
        for trait, d in delta.items():
            old = self.personality.get(trait, 0.0)
            new = max(0.0, min(1.0, old + d))
            if abs(new - old) > 1e-9:
                changes[trait] = (old, new)
                self.personality[trait] = new
        return changes

    def __repr__(self):
        return self.name


# ============================================================
# 3. 群体因果链（群体异步广播）
# ============================================================

class GroupChain:
    """群体因果链：统一群体记忆查询接口，信息不对称产生涌现"""

    def __init__(self, group_id):
        self.group_id = group_id
        self.chain = CausalChain(group_id)

    def broadcast(self, event):
        """异步广播：事件追加至群体链"""
        return self.chain.append(event)

    def snapshot(self):
        """当前群体链快照（不同成员在不同时刻看到不同快照）"""
        return [e.event_type for e in self.chain.events]


# ============================================================
# 4. 主流程：3 个 NPC，7 个事件
# ============================================================

def fmt_personality(p):
    return (f"善良 {p['kindness']:.2f} | 多疑 {p['suspicion']:.2f} | "
            f"冷酷 {p['coldness']:.2f}")


def main():
    print("=" * 62)
    print("  XY Protocol Demo — 让 NPC 永远记住你")
    print("  3 个数字生命体 · 7 个事件 · 因果链驱动性格演化")
    print("=" * 62)

    # ---- 创建 3 个数字生命体 ----
    elf_king = DigitalLifeForm(
        "elf_king", "精灵王",
        {"kindness": 0.30, "suspicion": 0.70, "coldness": 0.40},
        ["父亲死于与树精的战争", "精灵领地曾被树精践踏",
         "圣树落叶是树精一族最高规格的和平信物"],
    )
    elder_treant = DigitalLifeForm(
        "elder_treant", "树精长老",
        {"kindness": 0.80, "suspicion": 0.20, "coldness": 0.10},
        ["守护圣树千年，曾有精灵伤害过圣树的根", "圣树落叶是和平的象征"],
    )
    wind_sprite = DigitalLifeForm(
        "wind_sprite", "风之精灵",
        {"kindness": 0.60, "suspicion": 0.30, "coldness": 0.20},
        ["见证过精灵与树精的旧怨", "相信沟通能化解仇恨"],
    )
    npcs = {n.npc_id: n for n in (elf_king, elder_treant, wind_sprite)}
    group = GroupChain("world_forest_001")

    print("\n【初始性格】")
    for n in npcs.values():
        print(f"  {n.name}: {fmt_personality(n.personality)}")

    # ---- 事件 1：树精长老踩到精灵领地苔藓 ----
    print("\n" + "-" * 62)
    print("事件 1/7  [trespass] 树精长老踩到了精灵领地的苔藓")
    e1 = Event("trespass", "elder_treant", "elf_king",
               {"keywords": ["树精", "战争"], "desc": "踩到精灵领地苔藓",
                "suspicious_action": "派遣斥候监视树精长老",
                "kind_action": "派使者询问来意"})
    mem, act = elf_king.decide(e1)
    print(f"  [精灵王] 我从群体因果链得知：树精长老踩到了精灵领地的苔藓。")
    print(f"           {mem} — 多疑性格触发。")
    print(f"           决策：{act}。")
    elf_king.chain.append(e1)
    group.broadcast(e1)

    # ---- 事件 2：精灵斥候误入圣树区 ----
    print("\n" + "-" * 62)
    print("事件 2/7  [observe] 精灵斥候误入圣树区")
    e2 = Event("observe", "elf_king", "elder_treant",
               {"keywords": ["精灵", "圣树"], "desc": "精灵斥候误入圣树区",
                "suspicious_action": "召唤树根卫士戒备",
                "kind_action": "友善引导他离开，还送了一片圣树落叶"})
    mem, act = elder_treant.decide(e2)
    print(f"  [树精长老] 发现精灵斥候误入圣树区。")
    print(f"             {mem}")
    print(f"             但善良值 {elder_treant.personality['kindness']:.1f} 压倒多疑 — 决定{act}。")
    elder_treant.chain.append(e2)
    group.broadcast(e2)

    # ---- 事件 3：树精长老赠送圣树落叶 ----
    print("\n" + "-" * 62)
    print("事件 3/7  [gift] 树精长老赠送圣树落叶")
    e3 = Event("gift", "elder_treant", "elf_king",
               {"keywords": ["和平", "落叶"], "desc": "赠送圣树落叶",
                "suspicious_action": "半信半疑，先收下观察",
                "kind_action": "收下落叶，视为友善证明"})
    mem, act = elf_king.decide(e3)
    print(f"  [精灵王] 收到树精长老的友善证明（圣树落叶）。")
    print(f"           {mem}")
    print(f"           决策：{act}。")
    elf_king.chain.append(e3)
    group.broadcast(e3)

    # ---- 事件 4：风之精灵调解 ----
    print("\n" + "-" * 62)
    print("事件 4/7  [friendly] 风之精灵出面调解")
    e4 = Event("friendly", "wind_sprite", "elf_king",
               {"keywords": ["沟通", "仇恨"], "desc": "风之精灵调解",
                "suspicious_action": "保持距离听其说辞",
                "kind_action": "愿意倾听，放下戒备"})
    mem, act = elf_king.decide(e4)
    print(f"  [风之精灵] 见证过精灵与树精的旧怨，相信沟通能化解仇恨。")
    print(f"  [精灵王] {mem}")
    print(f"           决策：{act}。")
    wind_sprite.chain.append(e4)
    elf_king.chain.append(e4)
    group.broadcast(e4)

    # ---- 事件 5：双方和解 ----
    print("\n" + "-" * 62)
    print("事件 5/7  [reconcile] 精灵王与树精长老和解")
    e5 = Event("reconcile", "elf_king", "elder_treant",
               {"keywords": ["和平", "落叶"], "desc": "双方和解",
                "suspicious_action": "口头和解，暗中戒备",
                "kind_action": "真诚和解，结为盟友"})
    mem, act = elder_treant.decide(e5)
    print(f"  [树精长老] {mem}")
    print(f"             决策：{act}。")
    elf_king.chain.append(e5)
    elder_treant.chain.append(e5)
    group.broadcast(e5)

    # ---- 事件 6：群体广播汇聚 ----
    print("\n" + "-" * 62)
    print("事件 6/7  [broadcast] 群体异步广播汇聚")
    e6 = Event("broadcast", "wind_sprite", "world_forest_001",
               {"keywords": [], "desc": "群体链汇聚"})
    group.broadcast(e6)
    snap = group.snapshot()
    print(f"  [群体链] 当前快照（{len(snap)} 条）：{', '.join(snap)}")
    print(f"           不同成员在不同时刻查询，看到不同快照 — 信息不对称产生涌现。")

    # ---- 事件 7：性格闭环反馈结算 ----
    print("\n" + "-" * 62)
    print("事件 7/7  [feedback] 闭环反馈：事件驱动性格微调")
    for n in npcs.values():
        for ev in n.chain.events:
            n.adjust_personality(ev)
    for n in npcs.values():
        print(f"  {n.name}: {fmt_personality(n.personality)}")

    # ---- 因果链完整性校验 ----
    print("\n" + "=" * 62)
    print("因果链完整性校验（哈希指针链式）")
    all_ok = True
    for n in npcs.values():
        ok = n.chain.verify()
        all_ok = all_ok and ok
        print(f"  {n.name} 个体链: {len(n.chain)} 条事件, 校验 {'通过 ✓' if ok else '失败 ✗'}")
    gok = group.chain.verify()
    all_ok = all_ok and gok
    print(f"  群体链: {len(group.chain)} 条事件, 校验 {'通过 ✓' if gok else '失败 ✗'}")

    print("\n" + "=" * 62)
    print("结论：精灵王的性格因为一次意外的友善行为，永远改变了。")
    print("这就是 XY Protocol — 让 NPC 永远记住你。")
    print("=" * 62)
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
