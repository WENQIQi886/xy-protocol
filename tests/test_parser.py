#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XY Protocol SDK 单元测试
运行：python3 -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from parser import CausalChain, DigitalLifeForm, Event, GroupChain, Identity


class TestIdentity(unittest.TestCase):

    def test_generate_and_str(self):
        ident = Identity.generate("world_forest_001", seed="fixed-seed")
        self.assertEqual(str(ident), f"xy://{ident.puf_fingerprint}@world_forest_001")

    def test_generate_fingerprint_length(self):
        ident = Identity.generate("world_forest_001")
        self.assertEqual(len(ident.puf_fingerprint), 16)

    def test_generate_deterministic_with_seed(self):
        a = Identity.generate("world_forest_001", seed="seed-a")
        b = Identity.generate("world_forest_001", seed="seed-a")
        c = Identity.generate("world_forest_001", seed="seed-b")
        self.assertEqual(a.puf_fingerprint, b.puf_fingerprint)
        self.assertNotEqual(a.puf_fingerprint, c.puf_fingerprint)

    def test_parse_roundtrip(self):
        ident = Identity.generate("world_forest_001")
        parsed = Identity.parse(str(ident))
        self.assertEqual(parsed.puf_fingerprint, ident.puf_fingerprint)
        self.assertEqual(parsed.world_id, ident.world_id)

    def test_parse_invalid(self):
        with self.assertRaises(ValueError):
            Identity.parse("not-an-identity")


class TestEvent(unittest.TestCase):

    def test_hash_is_deterministic(self):
        e = Event("friendly", "a", "b", {"keywords": ["和平"]})
        self.assertEqual(e.compute_hash(), e.compute_hash())

    def test_hash_changes_with_params(self):
        e1 = Event("friendly", "a", "b", {"keywords": ["和平"]})
        e2 = Event("friendly", "a", "b", {"keywords": ["战争"]})
        self.assertNotEqual(e1.compute_hash(), e2.compute_hash())

    def test_event_id_auto_generated(self):
        e = Event("gift", "a", "b", {})
        self.assertEqual(len(e.event_id), 16)


class TestCausalChain(unittest.TestCase):

    def setUp(self):
        self.chain = CausalChain("owner_1")

    def test_append_sets_hashes(self):
        ev = Event("friendly", "a", "b", {})
        appended = self.chain.append(ev)
        self.assertIsNotNone(appended.self_hash)
        self.assertEqual(appended.prev_hash, CausalChain.GENESIS)

    def test_verify_empty_chain(self):
        self.assertTrue(self.chain.verify())

    def test_verify_valid_chain(self):
        for i in range(3):
            self.chain.append(Event("friendly", "a", "b", {"i": i}))
        self.assertEqual(len(self.chain), 3)
        self.assertTrue(self.chain.verify())

    def test_verify_detects_tampering(self):
        self.chain.append(Event("friendly", "a", "b", {"i": 0}))
        self.chain.append(Event("friendly", "a", "b", {"i": 1}))
        self.chain.events[0].params["i"] = 999
        self.assertFalse(self.chain.verify())

    def test_export_import_roundtrip(self):
        src = CausalChain("owner_1")
        src.append(Event("friendly", "a", "b", {"keywords": ["和平"]}))
        src.append(Event("gift", "b", "a", {"keywords": ["落叶"]}))
        exported = src.export()

        dst = CausalChain("owner_1")
        for data in exported:
            ev = Event(data["event_type"], data["initiator_id"],
                       data["receiver_id"], data["params"], data["timestamp"])
            ev.event_id = data["event_id"]
            ev.prev_hash = data["prev_hash"]
            ev.self_hash = data["self_hash"]
            dst.events.append(ev)
        dst.prev_hash = dst.events[-1].self_hash

        self.assertTrue(dst.verify())


class TestDigitalLifeForm(unittest.TestCase):

    def setUp(self):
        self.identity = Identity.generate("world_forest_001", seed="elf")
        self.npc = DigitalLifeForm(
            self.identity, "精灵王",
            {"kindness": 0.3, "suspicion": 0.7, "coldness": 0.4},
            ["父亲死于与树精的战争", "精灵领地曾被树精践踏"],
        )

    def test_recall_hits(self):
        hits = self.npc.recall(["树精", "战争"])
        self.assertEqual(len(hits), 2)
        self.assertIn("战争", hits[0])

    def test_recall_miss(self):
        hits = self.npc.recall(["不存在"])
        self.assertEqual(hits, [])

    def test_decide_suspicious_when_suspicion_dominant(self):
        ev = Event("trespass", "b", str(self.identity),
                   {"keywords": ["树精"], "suspicious_action": "派遣斥候",
                    "kind_action": "派使者询问"})
        hits, action = self.npc.decide(ev)
        self.assertEqual(action, "派遣斥候")

    def test_decide_kind_when_kindness_dominant(self):
        npc = DigitalLifeForm(
            self.identity, "树精长老",
            {"kindness": 0.8, "suspicion": 0.2, "coldness": 0.1},
            ["守护圣树千年"],
        )
        ev = Event("observe", "a", str(self.identity),
                   {"keywords": ["精灵", "圣树"], "suspicious_action": "戒备",
                    "kind_action": "友善引导"})
        hits, action = npc.decide(ev)
        self.assertEqual(action, "友善引导")

    def test_adjust_personality_friendly(self):
        ev = Event("friendly", "a", str(self.identity),
                   {"keywords": ["和平"]})
        changes = self.npc.adjust_personality(ev)
        self.assertIn("kindness", changes)
        self.assertAlmostEqual(self.npc.personality["kindness"], 0.35)
        self.assertAlmostEqual(self.npc.personality["suspicion"], 0.65)

    def test_adjust_personality_clamps_to_bounds(self):
        npc = DigitalLifeForm(
            self.identity, "极端善良",
            {"kindness": 0.99, "suspicion": 0.1, "coldness": 0.0},
            [],
        )
        npc.adjust_personality(Event("friendly", "a", "b", {}))
        self.assertLessEqual(npc.personality["kindness"], 1.0)

    def test_adjust_personality_unknown_event_noop(self):
        npc = DigitalLifeForm(self.identity, "x", {"kindness": 0.5}, [])
        changes = npc.adjust_personality(Event("unknown_type", "a", "b", {}))
        self.assertEqual(changes, {})

    def test_chain_verify_after_events(self):
        ev = Event("friendly", str(self.identity), str(self.identity),
                   {"keywords": ["和平"]})
        self.npc.chain.append(ev)
        self.assertTrue(self.npc.chain.verify())


class TestGroupChain(unittest.TestCase):

    def test_broadcast_and_snapshot(self):
        group = GroupChain("world_forest_001")
        group.broadcast(Event("trespass", "a", "b", {}))
        group.broadcast(Event("gift", "b", "a", {}))
        self.assertEqual(group.snapshot(), ["trespass", "gift"])

    def test_chain_verify(self):
        group = GroupChain("world_forest_001")
        group.broadcast(Event("observe", "a", "b", {}))
        self.assertTrue(group.chain.verify())


if __name__ == "__main__":
    unittest.main()
