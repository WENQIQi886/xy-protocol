#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XY Protocol SDK — 解析器核心代码
=================================
实现 XY 协议的核心逻辑：身份解析、事件解析、因果链校验。

零依赖：Python 3.8+
"""

import hashlib
import json
import re
import uuid
from datetime import datetime
import copy


# ============================================================
# 身份解析
# ============================================================

IDENTITY_RE = re.compile(r"^xy://([0-9a-f]{16})@([\w\-]+)$")


class Identity:
    """数字生命体身份标识：xy://{puf_fingerprint_hex}@{world_id}"""

    def __init__(self, puf_fingerprint, world_id):
        self.puf_fingerprint = puf_fingerprint
        self.world_id = world_id

    @classmethod
    def parse(cls, identity_str):
        m = IDENTITY_RE.match(identity_str)
        if not m:
            raise ValueError(f"非法身份标识: {identity_str}")
        return cls(m.group(1), m.group(2))

    @classmethod
    def generate(cls, world_id, seed=None):
        """基于 PUF 指纹生成全球唯一身份标识"""
        raw = seed or uuid.uuid4().hex
        fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        return cls(fingerprint, world_id)

    def __str__(self):
        return f"xy://{self.puf_fingerprint}@{self.world_id}"


# ============================================================
# 事件解析
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

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "initiator_id": self.initiator_id,
            "receiver_id": self.receiver_id,
            "timestamp": self.timestamp,
            "params": self.params,
            "prev_hash": self.prev_hash,
            "self_hash": self.self_hash,
        }

    @classmethod
    def from_dict(cls, data):
        ev = cls(
            data["event_type"],
            data["initiator_id"],
            data["receiver_id"],
            data["params"],
            data["timestamp"],
        )
        ev.event_id = data["event_id"]
        ev.prev_hash = data["prev_hash"]
        ev.self_hash = data["self_hash"]
        return ev


# ============================================================
# 因果链
# ============================================================

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
        """校验整条链的完整性"""
        prev = self.GENESIS
        for e in self.events:
            if e.prev_hash != prev:
                return False
            if e.self_hash != e.compute_hash():
                return False
            prev = e.self_hash
        return True

    def export(self):
        return [e.to_dict() for e in self.events]

    def __len__(self):
        return len(self.events)


# ============================================================
# 数字生命体
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

    def __init__(self, identity, name, personality, memories):
        self.identity = identity
        self.name = name
        self.personality = personality
        self.memories = memories
        self.chain = CausalChain(str(identity))

    def recall(self, keywords):
        return [m for m in self.memories if any(k in m for k in keywords)]

    def decide(self, event):
        hits = self.recall(event.params.get("keywords", []))
        if self.personality.get("kindness", 0.5) >= self.personality.get("suspicion", 0.5):
            action = event.params.get("kind_action", "友善回应")
        else:
            action = event.params.get("suspicious_action", "戒备观察")
        return hits, action

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

    def __str__(self):
        return f"{self.name} <{self.identity}>"


# ============================================================
# 群体因果链
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
