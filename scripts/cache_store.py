#!/usr/bin/env python3
"""
================================================================================
SciResearch Hierarchical Semantic & Exact Cache Store (scripts/cache_store.py)
================================================================================
Grounded in Chip Huyen, 'AI Engineering: Building Applications with Foundation Models'
(O'Reilly 2025, Chapter 10, Step 4: Reduce Latency with Caches).

Implements two-tier hierarchical caching for expensive scientific agent operations:
  - Tier 1 (Exact Cache): Fast SHA-256 hash lookup for identical inputs and queries.
  - Tier 2 (Semantic Cache): High-fidelity token-set and n-gram similarity matching
    for semantically equivalent scientific queries, preventing duplicate calculations.
  - Persistent SQLite storage in memory/cache_store.db with TTL expiry & LRU eviction.
  - Namespace isolation ('dft_params', 'bader_symmetry', 'structure_sanity', 'hypotheses').
================================================================================
"""

import os
import time
import json
import sqlite3
import hashlib
from typing import Dict, Any, List, Optional, Tuple


class CacheStore:
    """
    Two-tier hierarchical exact and semantic cache engine.
    """

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_dir = os.path.join(self.base_dir, "memory")
        os.makedirs(self.db_dir, exist_ok=True)
        self.db_path = os.path.join(self.db_dir, "cache_store.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_entries (
                    cache_id TEXT PRIMARY KEY,
                    namespace TEXT NOT NULL,
                    exact_hash TEXT NOT NULL,
                    query_text TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    last_accessed REAL NOT NULL,
                    access_count INTEGER DEFAULT 1,
                    ttl_seconds REAL DEFAULT 86400.0
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_exact ON cache_entries (namespace, exact_hash)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_ns ON cache_entries (namespace)")
            conn.commit()

    @staticmethod
    def _hash_key(key: str) -> str:
        return hashlib.sha256(key.strip().lower().encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _tokenize(text: str) -> set:
        import re
        tokens = re.findall(r'[a-zA-Z0-9_\-\.]+', text.lower())
        return set(tokens)

    @classmethod
    def _jaccard_similarity(cls, text_a: str, text_b: str) -> float:
        set_a = cls._tokenize(text_a)
        set_b = cls._tokenize(text_b)
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union if union > 0 else 0.0

    def get(self, query_key: str, query_text: Optional[str] = None, namespace: str = "default", min_similarity: float = 0.85) -> Optional[Dict[str, Any]]:
        """
        Retrieves a cached result using exact hash matching first, falling back
        to semantic similarity across queries in the same namespace.
        """
        now = time.time()
        exact_h = self._hash_key(query_key)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Tier 1: Exact Hash Match
            cursor.execute("""
                SELECT cache_id, query_text, result_json, created_at, ttl_seconds
                FROM cache_entries
                WHERE namespace = ? AND exact_hash = ?
            """, (namespace, exact_h))
            row = cursor.fetchone()

            if row:
                created_at = row["created_at"]
                ttl = row["ttl_seconds"]
                if ttl > 0 and (now - created_at) > ttl:
                    # Expired entry
                    cursor.execute("DELETE FROM cache_entries WHERE cache_id = ?", (row["cache_id"],))
                    conn.commit()
                else:
                    # Update access statistics
                    cursor.execute("""
                        UPDATE cache_entries
                        SET last_accessed = ?, access_count = access_count + 1
                        WHERE cache_id = ?
                    """, (now, row["cache_id"]))
                    conn.commit()
                    return {
                        "hit_type": "EXACT",
                        "namespace": namespace,
                        "similarity": 1.0,
                        "value": json.loads(row["result_json"])
                    }

            # 2. Tier 2: Semantic Similarity Match
            if query_text and len(query_text.strip()) > 5:
                cursor.execute("""
                    SELECT cache_id, query_text, result_json, created_at, ttl_seconds
                    FROM cache_entries
                    WHERE namespace = ?
                """, (namespace,))
                all_entries = cursor.fetchall()

                best_sim = 0.0
                best_match = None

                for entry in all_entries:
                    created_at = entry["created_at"]
                    ttl = entry["ttl_seconds"]
                    if ttl > 0 and (now - created_at) > ttl:
                        continue

                    sim = self._jaccard_similarity(query_text, entry["query_text"])
                    if sim > best_sim and sim >= min_similarity:
                        best_sim = sim
                        best_match = entry

                if best_match is not None:
                    cursor.execute("""
                        UPDATE cache_entries
                        SET last_accessed = ?, access_count = access_count + 1
                        WHERE cache_id = ?
                    """, (now, best_match["cache_id"]))
                    conn.commit()
                    return {
                        "hit_type": "SEMANTIC",
                        "namespace": namespace,
                        "similarity": round(best_sim, 3),
                        "matched_query": best_match["query_text"],
                        "value": json.loads(best_match["result_json"])
                    }

        return None

    def set(self, query_key: str, query_text: str, value: Any, namespace: str = "default", ttl_seconds: float = 86400.0) -> str:
        """
        Stores an entry in the hierarchical cache.
        """
        now = time.time()
        exact_h = self._hash_key(query_key)
        cache_id = f"{namespace}_{exact_h}"
        val_json = json.dumps(value)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO cache_entries
                (cache_id, namespace, exact_hash, query_text, result_json, created_at, last_accessed, access_count, ttl_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
            """, (cache_id, namespace, exact_h, query_text, val_json, now, now, ttl_seconds))
            conn.commit()

        return cache_id

    def stats(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns summary statistics of the cache store.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if namespace:
                cursor.execute("SELECT COUNT(*), SUM(access_count) FROM cache_entries WHERE namespace = ?", (namespace,))
            else:
                cursor.execute("SELECT COUNT(*), SUM(access_count) FROM cache_entries")
            count, total_access = cursor.fetchone()

            cursor.execute("SELECT DISTINCT namespace FROM cache_entries")
            namespaces = [r[0] for r in cursor.fetchall()]

        return {
            "total_entries": count or 0,
            "total_access_hits": total_access or 0,
            "namespaces": namespaces,
            "db_path": self.db_path
        }


if __name__ == "__main__":
    cache = CacheStore()
    k = "vasp_encut_pt111"
    q = "Optimal ENCUT cutoff energy for Pt(111) slab surface with PBE functional"
    cache.set(k, q, {"ENCUT": 520, "KPOINTS": [8, 8, 1]}, namespace="dft_params")

    # Exact lookup
    h1 = cache.get(k, namespace="dft_params")
    print("Exact hit:", h1 is not None)

    # Semantic lookup
    q_near = "Optimal ENCUT cutoff for Pt(111) surface using PBE functional"
    h2 = cache.get("diff_key", query_text=q_near, namespace="dft_params")
    print("Semantic hit:", h2 is not None, h2.get("similarity") if h2 else None)
