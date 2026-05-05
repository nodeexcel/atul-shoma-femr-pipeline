---
name: Session management and context preservation
description: User wants full project context preserved across sessions — save notes, docs, memories proactively without being asked
type: feedback
originSessionId: 03ce2e1b-d66e-4c61-9283-53647745d1bc
---
User explicitly asked: "these things shouldn't be lost on new session, you should have full context of what is going on in the project." And: "I'm not tracking, you create your docs on whatever you require, and memory in this repo, you have full access."

**Why:** The user manages multiple conversations and doesn't want to re-explain project state each time. They expect Claude to proactively maintain project notes.

**How to apply:**
- At end of every session, save/update project status memory with what changed
- When receiving client emails/transcripts, extract key decisions and save to memory
- When making technical decisions, document them in memory (not just in code comments)
- Keep `docs/` folder updated with handoff docs, meeting summaries, run commands
- Check memory files at session start to load full context before acting
