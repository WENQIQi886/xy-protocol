# XY Protocol API 参考手册

> 版本：v0.1（Draft）

## 1. 身份 API

### 1.1 创建数字生命体

```
POST /lifeforms
```

请求体：

```json
{
  "name": "精灵王",
  "personality": {"kindness": 0.3, "suspicion": 0.7, "coldness": 0.4},
  "memories": ["父亲死于与树精的战争"]
}
```

响应：

```json
{
  "lifeform_id": "xy://a3f2e1d4c5b6789a@world_forest_001",
  "status": "created"
}
```

### 1.2 查询数字生命体

```
GET /lifeforms/{lifeform_id}
```

## 2. 事件 API

### 2.1 追加事件

```
POST /lifeforms/{lifeform_id}/events
```

请求体：

```json
{
  "event_type": "friendly",
  "initiator_id": "xy://...@world_forest_001",
  "receiver_id": "xy://...@world_forest_001",
  "description_params": {"keywords": ["和平", "落叶"]}
}
```

响应：

```json
{
  "event_id": "a1b2c3d4e5f60718",
  "prev_hash": "0a1b...",
  "self_hash": "9f8e..."
}
```

### 2.2 校验因果链

```
GET /lifeforms/{lifeform_id}/chain/verify
```

响应：

```json
{
  "valid": true,
  "event_count": 4
}
```

## 3. 群体广播 API

### 3.1 广播事件

```
POST /groups/{group_id}/broadcast
```

### 3.2 查询群体快照

```
GET /groups/{group_id}/snapshot
```

## 4. 协同演化 API

### 4.1 建立加密通道

```
POST /lifeforms/{lifeform_id}/secure-channel
```

### 4.2 交换演化数据

```
POST /lifeforms/{lifeform_id}/evolve
```

数据类型：`emotion_vector`（情感向量）、`genetic`（遗传进化）、`self_heal`（自愈修复）、`notarize`（信任公证）。

## 5. 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 参数错误 |
| 401 | 身份验证失败 |
| 404 | 资源不存在 |
| 409 | 因果链校验失败 |
| 500 | 服务器内部错误 |
