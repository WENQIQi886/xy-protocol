# XY Protocol SDK

XY Protocol 的 Python SDK，实现协议核心逻辑：身份解析、事件解析、因果链校验、数字生命体建模。

## 快速开始

```python
from parser import Identity, Event, CausalChain, DigitalLifeForm

# 1. 创建身份
identity = Identity.generate("world_forest_001")
print(identity)  # xy://a3f2e1d4c5b6789a@world_forest_001

# 2. 创建数字生命体
npc = DigitalLifeForm(
    identity,
    name="精灵王",
    personality={"kindness": 0.3, "suspicion": 0.7, "coldness": 0.4},
    memories=["父亲死于与树精的战争"],
)

# 3. 追加事件
event = Event("friendly", str(identity), str(identity), {"keywords": ["和平"]})
npc.chain.append(event)

# 4. 校验因果链
assert npc.chain.verify() is True
```

## 模块

| 模块 | 说明 |
|------|------|
| `Identity` | 身份标识解析与生成（xy://{puf}@{world}） |
| `Event` | 事件记录（哈希指针链式连接） |
| `CausalChain` | 因果链（append-only + 哈希链校验） |
| `DigitalLifeForm` | 数字生命体（性格 + 记忆 + 因果链） |

## 依赖

零依赖，Python 3.8+。
