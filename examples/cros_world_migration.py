#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：跨世界迁移（数字生命体从一个世界迁移到另一个世界）
运行：python3 examples/cros_world_migration.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from parser import Identity, Event, CausalChain, DigitalLifeForm


def main():
    # 数字生命体在源世界
    identity = Identity.generate("world_forest_001")
    npc = DigitalLifeForm(
        identity, "精灵王",
        {"kindness": 0.45, "suspicion": 0.60, "coldness": 0.34},
        ["父亲死于与树精的战争", "圣树落叶是和平的象征"],
    )

    # 在源世界积累事件
    e1 = Event("friendly", str(identity), str(identity), {"keywords": ["和平"]})
    npc.chain.append(e1)
    e2 = Event("reconcile", str(identity), str(identity), {"keywords": ["落叶"]})
    npc.chain.append(e2)
    print(f"[源世界] {npc.name} 因果链: {len(npc.chain)} 条事件, 校验 {npc.chain.verify()}")

    # 导出因果链（跨世界迁移的核心：记忆与性格随身份迁移）
    exported = npc.chain.export()
    print(f"[迁移] 导出因果链: {len(exported)} 条事件")

    # 在目标世界重建（身份不变，记忆完整继承）
    new_identity = Identity(identity.puf_fingerprint, "world_city_002")
    migrated = DigitalLifeForm(
        new_identity, npc.name, dict(npc.personality), list(npc.memories)
    )
    for ev_data in exported:
        ev = Event(
            ev_data["event_type"], ev_data["initiator_id"],
            ev_data["receiver_id"], ev_data["params"], ev_data["timestamp"],
        )
        ev.event_id = ev_data["event_id"]
        migrated.chain.append(ev)

    print(f"[目标世界] 新身份: {migrated.identity}")
    print(f"[目标世界] 性格继承: {migrated.personality}")
    print(f"[目标世界] 记忆继承: {migrated.memories}")
    print(f"[目标世界] 因果链: {len(migrated.chain)} 条事件, 校验 {migrated.chain.verify()}")

    # 跨世界一致性验证：PUF 指纹不变
    assert identity.puf_fingerprint == new_identity.puf_fingerprint
    print(f"\n跨世界一致性: PUF 指纹不变 -> {identity.puf_fingerprint}")
    print("结论：数字生命体跨世界迁移成功，记忆与性格完整继承。")


if __name__ == "__main__":
    main()
