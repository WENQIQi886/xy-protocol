#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：群体广播（个体链 -> 群体链）
运行：python3 examples/group_broadcast.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from parser import Identity, Event, CausalChain, DigitalLifeForm


def main():
    # 三个数字生命体
    elf = DigitalLifeForm(
        Identity.generate("world_forest_001"), "精灵王",
        {"kindness": 0.3, "suspicion": 0.7, "coldness": 0.4},
        ["父亲死于与树精的战争"],
    )
    treant = DigitalLifeForm(
        Identity.generate("world_forest_001"), "树精长老",
        {"kindness": 0.8, "suspicion": 0.2, "coldness": 0.1},
        ["守护圣树千年"],
    )
    sprite = DigitalLifeForm(
        Identity.generate("world_forest_001"), "风之精灵",
        {"kindness": 0.6, "suspicion": 0.3, "coldness": 0.2},
        ["相信沟通能化解仇恨"],
    )

    # 群体因果链
    group_chain = CausalChain("world_forest_001")

    # 事件 1：树精长老踩到精灵领地苔藓
    e1 = Event("trespass", str(treant.identity), str(elf.identity),
               {"keywords": ["树精", "战争"]})
    elf.chain.append(e1)
    group_chain.append(e1)
    print(f"[事件1] 树精长老踩到精灵领地苔藓 -> 精灵王个体链 + 群体链")

    # 事件 2：精灵斥候误入圣树区
    e2 = Event("observe", str(elf.identity), str(treant.identity),
               {"keywords": ["精灵", "圣树"]})
    treant.chain.append(e2)
    group_chain.append(e2)
    print(f"[事件2] 精灵斥候误入圣树区 -> 树精长老个体链 + 群体链")

    # 事件 3：群体广播汇聚
    e3 = Event("broadcast", str(sprite.identity), "world_forest_001", {})
    group_chain.append(e3)
    print(f"[事件3] 群体广播汇聚")

    # 校验
    print(f"\n个体链校验: 精灵王={elf.chain.verify()}, 树精长老={treant.chain.verify()}")
    print(f"群体链校验: {group_chain.verify()}")
    print(f"群体链快照: {[e.event_type for e in group_chain.events]}")


if __name__ == "__main__":
    main()
