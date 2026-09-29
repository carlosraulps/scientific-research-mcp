#!/usr/bin/env python3
"""
================================================================================
Liu et al. Procedural Skill Crystallizer
================================================================================
Crystallizes successfully diagnosed workflows, error recoveries, and verified
simulation procedures into persistent, reusable skills that sync directly with
SKILL.md and persist across model migrations.
================================================================================
"""

import os
import sys
import json
import sqlite3
import datetime
from typing import Dict, Any, List, Optional


class SkillCrystallizer:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.memory_dir = os.path.join(self.base_dir, "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = os.path.join(self.memory_dir, "skills_memory.db")
        self.skill_md_path = os.path.join(self.base_dir, "SKILL.md")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crystallized_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                trigger_conditions TEXT NOT NULL,
                procedure_code TEXT NOT NULL,
                validation_criteria TEXT,
                usage_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_procedure(
        self,
        skill_name: str,
        description: str,
        trigger_conditions: str,
        procedure_code: str,
        validation_criteria: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crystallizes an operational procedure into persistent memory and appends to SKILL.md.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO crystallized_skills (skill_name, description, trigger_conditions, procedure_code, validation_criteria, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(skill_name) DO UPDATE SET
                description = excluded.description,
                trigger_conditions = excluded.trigger_conditions,
                procedure_code = excluded.procedure_code,
                validation_criteria = excluded.validation_criteria,
                updated_at = excluded.updated_at
        """, (skill_name, description, trigger_conditions, procedure_code, validation_criteria, now_iso, now_iso))
        conn.commit()
        conn.close()

        # Append to SKILL.md under a dedicated section if not already present
        if os.path.exists(self.skill_md_path):
            with open(self.skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            skill_tag = f"### Learned Skill: `{skill_name}`"
            if skill_tag not in content:
                new_section = f"""

{skill_tag}
- **Description**: {description}
- **Trigger**: {trigger_conditions}
- **Validation**: {validation_criteria or 'Automated schema verification'}
```python
{procedure_code}
```
"""
                with open(self.skill_md_path, "a", encoding="utf-8") as f:
                    f.write(new_section)

        return {
            "status": "CRYSTALLIZED",
            "skill_name": skill_name,
            "updated_at": now_iso,
            "isError": False
        }

    def search_procedures(self, query: str) -> Dict[str, Any]:
        """
        Finds crystallized skills and procedures matching a natural language query or error signature.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, skill_name, description, trigger_conditions, procedure_code, validation_criteria, usage_count
            FROM crystallized_skills
        """)
        rows = cur.fetchall()
        conn.close()

        q_lower = query.lower()
        matches = []
        for r in rows:
            combined = f"{r[1]} {r[2]} {r[3]} {r[5] or ''}".lower()
            if any(term in combined for term in q_lower.split()):
                matches.append({
                    "id": r[0],
                    "skill_name": r[1],
                    "description": r[2],
                    "trigger_conditions": r[3],
                    "procedure_code": r[4],
                    "validation_criteria": r[5],
                    "usage_count": r[6]
                })

        return {
            "query": query,
            "total_matches": len(matches),
            "skills": matches,
            "isError": False
        }
