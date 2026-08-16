#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：创建数字生命体（NPC）
运行：python3 examples/npc_creation.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from parser import Identity, DigitalLifeForm


def main():
    # 生成全球唯一身份标识
    identity = Identity.generate("world_forest_001")
    print(f"身份标识: {identity}")

    # 创建数字生命体
    npc = DigitalLifeForm(
        identity,
        name="精灵王",
        personality={"kindness": 0.3, "suspicion": 0.7, "coldness": 0.4},
        memories=["父亲死于与树精的战争", "精灵领地曾被树精践踏"],
    )
    print(f"数字生命体: {npc}")
    print(f"性格: {npc.personality}")
    print(f"记忆: {npc.memories}")
    print(f"因果链: {len(npc.chain)} 条事件")


if __name__ == "__main__":
    main()
