# ZeroChain

Minimal truth-seeking chain from zero.

~240 lines of Python. No LLM. No server. Starts empty.  
Only hard rules: provenance (hashed + linked + immutable) and revision (challenge, fork, reconcile, prune anything).

Everything else (axioms, anchors, gravity, meaning) is proposed, challenged, reconciled or neglected into existence.

Friction (attention cost, neglect) is the selector — not code, not god.

### Quick start

	At > prompt:
		show — see chain
		add <text> — add to tip
		add-from <hash> <text> — fork from any node
		challenge <hash> <reason> — critique any node
		reconcile <hash> <summary> [target] — collapse branch to core
		branches <hash> — view subtree
		quit — exit

Philosophy:
	Branching creates friction instantly.
	Low-value branches wither through neglect (emergent gravity).
	Reason reduces friction only when anchored to external reality.
	Duality survives as the non-dodge resolution.
	The only friction-independent level is the unobserved genesis.

Fork it. Break it. See what survives.

MIT License - do whatever you want. 

### How to update README
1. In your main repo folder (`C:\Users\benja\Documents\FPGame`):
   - Open (or create) `README.md` in Notepad/VS Code.
   - Paste the block above (replace if needed).
   - Save.

2. Commit & push:

	git add README.md
   	git commit -m "Update README: add epistemic version control section + updated commands"
   	git push

3. Refresh repo page: https://github.com/benjamindymond-cpu/ZeroChain  
- README should render with headings, code blocks, etc.

This keeps the identity as "ZeroChain" (the kernel) while clearly explaining the git-inspired layer as a built-in enhancement.  
No need for a separate repo yet — this is still the same project, just more capable.

If you prefer a separate repo for the git features (e.g., "EpistemicGit"), say so — we can fork it out.

Otherwise, this README update is the next small, valuable step.

Run the add/commit/push when ready, then paste any output or the repo page link if you want feedback.

We're moving forward.  
What's after README?  
(Theory test, agent loop, UI, or something else?) 😈🌱

```bash
git clone https://github.com/benjamindymond-cpu/ZeroChain.git
cd ZeroChain
python ZeroChain.py