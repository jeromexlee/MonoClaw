# Conversation Notes — Agent Instructions

## What This Directory Is

Auto-generated meeting/conversation records. Audio sources are typically iPhone Voice Memos (transferred to Mac via AirDrop), transcribed locally via whisper.cpp, then processed by LLM in a single pass to generate structured markdown notes.

**Generation pipeline**: `transcribe-airdrop.sh` → whisper.cpp transcription → `build-meeting-note.py` → LLM single-pass summary → `YYYYMMDD_HHMMSS_<name>.md`

Conversation language is **mixed English and Chinese** (code-switching), with technical terms and product names typically in English and discussion in Chinese.

## Document Structure: Two Regions

Each note has two distinct regions with different editing rules:

**Structured notes** (above `## Original Transcript`): LLM-generated content — TL;DR, Topic breakdown, decisions & consensus, Action Items. This section is editable and most prone to errors requiring manual correction.

**Raw transcript** (below `## Original Transcript`): Verbatim whisper output with timestamps. **Never modify this section** — it is the ground truth for tracing back and re-understanding context.

## Methodology for Correcting Meeting Notes

When users provide corrections, the two most common error types are:

### 1. Transcription Errors (whisper misheard)

Whisper transcribed one word as another with similar pronunciation. Typical example: in mixed English-Chinese context, "revoke" was transcribed as "rework".

Handling: Replace comprehensively in the structured notes section, but **do not change the raw transcript**. After replacement, read through related paragraphs to ensure semantic coherence — cannot just do mechanical keyword replacement.

Post-correction improvement: Add the correct word to `keywords.txt` so future whisper transcriptions are more accurate.

### 2. Semantic Misunderstanding (LLM misunderstood)

Whisper's transcription itself is fine, but LLM misunderstood the speaker's meaning during summarization. These errors are often more subtle and have greater impact.

Typical example: "security won't change" — LLM understood as "won't change security boundaries", but actual meaning is "security team refuses to help with this change, we need to do it ourselves". This is Chinese colloquial shorthand being incorrectly expanded by LLM literally.

Handling: Cannot just fix one or two lines. A semantic error cascades to:
- TL;DR summary
- Topic breakdown (current state, discussion conclusion, actions, risks/dependencies)
- Decisions & consensus
- Action Items

Must track all propagation paths of the erroneous semantics in the document and correct each one, ensuring the corrected narrative remains consistent and coherent across all sections.

### Correction Process

1. First understand the user's correction and its impact on the document's overall narrative
2. List all affected sections (usually far more than one)
3. Starting from TL;DR, proceed through the document in order, confirming semantic coherence for each section independently
4. Keep the raw transcript unchanged
5. After correction, verify: the structured notes should contain no traces of the erroneous semantics

### Common Pitfalls in English-Chinese Code-Switching

- English words with similar pronunciation swapped (rework/revoke, risk/rest, root/route)
- Chinese colloquial shorthand over-interpreted by LLM ("X won't change" = "X team won't help", not "won't change X")
- Unclear pronoun reference — in "it says you do it yourselves", "it" could refer to a team rather than a person
- Speaker attribution confusion — in multi-person conversations, LLM may attribute A's viewpoint to B

## Supporting Files

- `keywords.txt`: Keyword hints for whisper, one per line. When whisper repeatedly misheard a word, add the correct form here.
- `build-meeting-note.py`: LLM summarization script that takes transcribed text and outputs structured markdown.
- `transcribe-airdrop.sh`: End-to-end pipeline script from audio to final markdown.
