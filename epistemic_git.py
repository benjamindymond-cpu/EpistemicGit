# ZeroChain - Minimal truth-seeking engine
# MIT License - Copyright (c) 2026 [Your Name or Handle]
# See LICENSE file for full terms.

import hashlib
import json
from datetime import datetime, timezone
from typing import List, Dict, Any

class FPNode:
    """A single node in the chain — immutable, hashed, linked."""
    def __init__(self, content: str, parent_hash: str = None, is_genesis: bool = False):
        self.content = content.strip()
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.parent_hash = parent_hash
        self.hash = self._compute_hash()
        self.is_genesis = is_genesis
    
    def _compute_hash(self) -> str:
        """SHA-256 hash of timestamp + parent + content (first 16 chars for readability)."""
        data = f"{self.timestamp}|{self.parent_hash or 'genesis'}|{self.content}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        return {
            "hash": self.hash,
            "parent": self.parent_hash,
            "time": self.timestamp,
            "content": self.content,
            "genesis": self.is_genesis
        }

class FPChain:
    """The core chain — append-only, provenance-tracked, fully revisable."""
    def __init__(self, filename: str = "zerochain.json"):
        self.filename = filename
        self.nodes: List[FPNode] = []
        self._load()
        if not self.nodes:
            self._create_genesis()
    
    def _create_genesis(self):
        """Initial node — empty genesis with mechanics + provisional anchor."""
        welcome = (
            "ZeroChain — truth-seeking from zero.\n"
            "Nothing is sacred. Everything is revisable.\n"
            "Mechanics:\n"
            "  - Provenance: hashed + linked + immutable\n"
            "  - Revision: challenge, fork, reconcile, prune anything (including this)\n"
            "Provisional observation: Physical reality exists independently and is testable via physics, biology, experiment.\n"
            "All axioms (including this one) are open to challenge.\n"
            "Begin."
        )
        node = FPNode(welcome, parent_hash=None, is_genesis=True)
        self.nodes.append(node)
        self._save()
        print("\n=== ZeroChain started ===\n")
        print(welcome)
        print(f"\nGenesis hash: {node.hash}")
        print("Type 'show' to see chain, 'help' for commands.\n")
    
    def _load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for entry in data:
                    node = FPNode(entry["content"])
                    node.hash = entry["hash"]
                    node.timestamp = entry["time"]
                    node.parent_hash = entry.get("parent")
                    node.is_genesis = entry.get("genesis", False)
                    self.nodes.append(node)
        except FileNotFoundError:
            pass
    
    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump([n.to_dict() for n in self.nodes], f, indent=2)
    
    def add(self, content: str) -> str:
        """Add a new node to the current tip of the chain."""
        parent_hash = self.nodes[-1].hash if self.nodes else None
        node = FPNode(content, parent_hash)
        self.nodes.append(node)
        self._save()
        print(f"Added: {node.hash}")
        print(f"  {content[:100]}{'...' if len(content)>100 else ''}")
        return node.hash
    
    def add_from(self, target_hash: str, content: str) -> str:
        """Add a new node attached to any existing hash (fork from specific node)."""
        parent_node = next((n for n in self.nodes if n.hash == target_hash), None)
        if not parent_node:
            print(f"Node {target_hash} not found.")
            return None
        node = FPNode(content, parent_hash=target_hash)
        self.nodes.append(node)
        self._save()
        print(f"Added from {target_hash[:8]}: {node.hash}")
        print(f"  {content[:100]}{'...' if len(content)>100 else ''}")
        return node.hash
    
    def challenge(self, target_hash: str, reason: str):
        """Challenge any node — creates a new branch pointing to it."""
        parent_node = next((n for n in self.nodes if n.hash == target_hash), None)
        if not parent_node:
            print(f"Node {target_hash} not found.")
            return
        
        content = f"CHALLENGE on {target_hash[:8]}: {reason.strip()}"
        new_node = FPNode(content, parent_hash=target_hash)
        self.nodes.append(new_node)
        self._save()
        print(f"Challenge forked from {target_hash[:8]} → {new_node.hash}")
        print(f"  Reason: {reason}")
    
    def reconcile_to_core(self, branch_hash: str, summary: str, target_hash: str = None):
        """Self-pruning: collapse a branch back to core as a summary node."""
        branch_node = next((n for n in self.nodes if n.hash == branch_hash), None)
        if not branch_node:
            print(f"Branch {branch_hash} not found.")
            return
        
        target = target_hash or self.nodes[0].hash
        content = f"[RECONCILE] {branch_hash[:8]} → Core: {summary.strip()}"
        new_node = FPNode(content, parent_hash=target)
        self.nodes.append(new_node)
        self._save()
        print(f"Branch {branch_hash[:8]} reconciled to core as {new_node.hash}")
        print(f"  Summary: {summary}")
        
    def merge_from(self, other_file: str, summary: str, target_hash: str = None):
        """Merge summary from another chain file into current chain."""
        import os
        if not os.path.exists(other_file):
            print(f"File {other_file} not found.")
            return
        other_chain = FPChain(other_file)
        if not other_chain.nodes:
            print(f"No nodes in {other_file}")
            return
        other_tip = other_chain.nodes[-1].hash
        self.reconcile_to_core(other_tip, summary, target_hash)
        print(f"Merged summary from {other_file} into current chain.")
    
    def show_chain(self):
        if not self.nodes:
            print("Chain empty. Add your first node.")
            return
        
        print("Current Chain (ASCII tree view):")
        # Build parent-to-children map
        children = {}
        for node in self.nodes:
            parent = node.parent_hash
            if parent not in children:
                children[parent] = []
            children[parent].append(node)
        
        def print_tree(node, prefix=""):
            tag = "[GENESIS]" if node.is_genesis else ""
            c_tag = "[CHALLENGE]" if node.content.startswith("CHALLENGE on") else ""
            r_tag = "[RECONCILE]" if node.content.startswith("[RECONCILE]") else ""
            print(f"{prefix}└─ {node.hash} ← {node.parent_hash[:8] if node.parent_hash else 'genesis'}  {node.timestamp[:19]} {tag}{c_tag}{r_tag}")
            print(f"{prefix}   {node.content[:120]}{'...' if len(node.content)>120 else ''}")
            print()
            
            # If reconciled, collapse children (show only summary)
            if r_tag:
                print(f"{prefix}   (Reconciled branch collapsed — use 'branches {node.parent_hash[:8]}' for full history)")
                return
            
            # Recurse children
            child_list = children.get(node.hash, [])
            for i, child in enumerate(child_list):
                new_prefix = prefix + ("│   " if i < len(child_list)-1 else "    ")
                print_tree(child, new_prefix)
        
        # Start from genesis
        genesis = self.nodes[0]
        print_tree(genesis)
    
    def branches_from(self, target_hash: str):
        """List all direct children of a node (full branch history)."""
        branches = [n for n in self.nodes if n.parent_hash == target_hash]
        if not branches:
            print(f"No branches from {target_hash[:8]}")
            return
        print(f"Branches from {target_hash[:8]}:")
        for node in branches:
            print(f"  - {node.hash}  {node.timestamp[:19]}")
            print(f"    {node.content[:80]}{'...' if len(node.content)>80 else ''}")
    def search(self, keyword: str):
        """Search for nodes containing the keyword (case-insensitive)."""
        keyword = keyword.lower()
        results = []
        for node in self.nodes:
            if keyword in node.content.lower() or keyword in node.hash.lower():
                results.append(node)
        if not results:
            print(f"No nodes found containing '{keyword}'")
            return
        print(f"Found {len(results)} nodes matching '{keyword}':")
        for node in results:
            parent = node.parent_hash[:8] if node.parent_hash else "genesis"
            print(f"  - {node.hash} ← {parent}  {node.timestamp[:19]}")
            print(f"    {node.content[:80]}{'...' if len(node.content)>80 else ''}")
            print()

# Interactive shell
if __name__ == "__main__":
    chain = FPChain()
    print("\nZeroChain v0.1 — truth-seeking from zero")
    print("Commands:")
    print("  add <text>             — add to current tip")
    print("  add-from <hash> <text> — fork from any node")
    print("  challenge <hash> <reason> — challenge any node")
    print("  reconcile <hash> <summary> [target] — collapse branch to core")
    print("  branches <hash>        — show full subtree from node")
    print("  show                   — show current chain")
    print("  quit                   — exit")
    print("\nType 'show' to begin.\n")
    print("Available commands:")
    print("  add <text>             — add to current tip")
    print("  add-from <hash> <text> — fork from any node")
    print("  challenge <hash> <reason> — critique any node")
    print("  reconcile <hash> <summary> [target] — collapse branch to core")
    print("  branches <hash>        — show full subtree from node")
    print("  show                   — display current chain")
    print("  quit                   — exit")
    print("  help                   — show this list")
    print()
    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        if cmd.lower() == "quit":
            break
        elif cmd.lower() == "show":
            chain.show_chain()
        elif cmd.startswith("add "):
            content = cmd[4:].strip()
            if content:
                chain.add(content)
            else:
                print("Nothing to add.")
        elif cmd.startswith("add-from "):
            parts = cmd[9:].strip().split(" ", 1)
            if len(parts) < 2:
                print("Usage: add-from <hash> <text>")
                continue
            target_hash, content = parts[0], parts[1].strip()
            if not content:
                print("No content.")
                continue
            chain.add_from(target_hash, content)
        elif cmd.startswith("challenge "):
            parts = cmd[10:].strip().split(" ", 1)
            if len(parts) < 2:
                print("Usage: challenge <hash> <reason>")
                continue
            target_hash, reason = parts[0], parts[1]
            chain.challenge(target_hash, reason)
        elif cmd.startswith("branches "):
            target_hash = cmd[9:].strip()
            if target_hash:
                chain.branches_from(target_hash)
            else:
                print("Usage: branches <hash>")
        elif cmd.startswith("reconcile "):
            parts = cmd[10:].strip().split(" ", 2)
            if len(parts) < 2:
                print("Usage: reconcile <branch-hash> <summary> [optional-target-hash]")
                continue
            branch_hash = parts[0]
            summary = parts[1]
            target_hash = parts[2] if len(parts) > 2 else None
            chain.reconcile_to_core(branch_hash, summary, target_hash)
        elif cmd == "help":
            print("Available commands:")
            print("  add <text>             — add to current tip")
            print("  add-from <hash> <text> — fork from any node")
            print("  challenge <hash> <reason> — critique any node")
            print("  reconcile <hash> <summary> [target] — collapse branch to core")
            print("  branches <hash>        — show full subtree from node")
            print("  show                   — display current chain")
            print("  quit                   — exit")
            print("  help                   — show this list")
            print()
        elif cmd.startswith("search "):
            keyword = cmd[7:].strip()
            if not keyword:
                print("Usage: search <keyword>")
                continue
            chain.search(keyword)
        elif cmd.startswith("branch "):
            name = cmd[7:].strip()
            if not name:
                print("Usage: branch <name>")
                continue
            new_file = f"zerochain_{name}.json"
            chain._save()  # save current
            print(f"Branched to {new_file}")
            print(f"Switch with: checkout {name}")

        elif cmd == "list-branches":
            import glob
            files = glob.glob("zerochain_*.json")
            if not files:
                print("No branches found (only default chain).")
                return
            print("Available branches:")
            for f in files:
                name = f.replace("zerochain_", "").replace(".json", "")
                print(f"  - {name} ({f})")

        elif cmd.startswith("checkout "):
            name = cmd[9:].strip()
            if not name:
                print("Usage: checkout <name>")
                continue
            new_file = f"zerochain_{name}.json"
            if not os.path.exists(new_file):
                print(f"Branch {new_file} not found.")
                return
            chain = FPChain(new_file)
            print(f"Checked out {new_file}")
            chain.show_chain()

        elif cmd.startswith("merge "):
            parts = cmd[6:].strip().split(" ", 1)
            if len(parts) < 1:
                print("Usage: merge <other-branch-name> <summary>")
                continue
            name = parts[0]
            summary = parts[1] if len(parts) > 1 else "Merged from other branch"
            other_file = f"zerochain_{name}.json"
            chain.merge_from(other_file, summary)

        elif cmd == "log":
            print("Commit history (simplified):")
            for i, node in enumerate(chain.nodes):
                parent = node.parent_hash[:8] if node.parent_hash else "genesis"
                print(f"{i}: {node.hash} ← {parent}  {node.timestamp[:19]}")
                print(f"   {node.content[:80]}{'...' if len(node.content)>80 else ''}")
                print()
        else:
            print("Unknown command. Try add, add-from, challenge, reconcile, branches, show, quit")