---
name: text-response-evaluator
description: Evaluate TELUS Text Response Evaluation tasks from transcript-based conversations. Use when asked to summarize a text-message transcript, decide Pass or Reject, choose all transcript rejection reasons, select the best reply to the final message, or answer the task's multiple-choice question using TELUS-TASKS/Text Response Evaluation guidelines.
---

# Text Response Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Source Of Truth

Use `TELUS-TASKS/Text Response Evaluation/telus - Text_Response_Evaluation.pdf` as the source of truth. This skill is the workflow for applying that PDF. Do not use SBS, bot-reply validation, URL checking, OPR, or search-result flags for this task type unless the user separately asks for them.

Read `references/rubric.md` when doing an actual rating or when unsure about a rejection reason.

## Workflow

1. Confirm the task type is Text Response Evaluation, not SBS or bot reply validation.
2. Read the full transcript and identify the two participants.
3. Before deciding Pass/Reject, scan every message for hard rejection issues. Run the 3-step Hard check in `references/rubric.md` (`### Includes Name Of Participant`) for the participant-name rule; it is the authoritative version.
4. Write a transcript summary in no more than 30 words.
5. Decide whether the transcript `Passes` or `Rejects`.
6. If it rejects, select every rejection reason that applies and stop response selection unless the task still requires a separate answer.
7. If it passes, evaluate all response options as replies to the final message only.
8. Choose the best response that is natural, context-aware, from the correct speaker's perspective, and free of rejection issues.
9. Answer the multiple-choice question using only the original transcript, not the selected response. Read the question wording exactly.

## Transcript Summary

Maximum 30 words, plain and factual, covering the main topic or topics. Full rules, style pattern, and examples: `references/rubric.md` (`## Summary Rules`).

## Pass Or Reject

Pass only if the transcript sounds like a natural text conversation between two humans and has none of the rejection issues.

Reject if any rejection reason applies. Select all that apply:

- `Spelling Mistake`
- `Unnecessary Repetition`
- `Contains Emojis`
- `Offensive Language`
- `Includes Name of Participant`
- `Incoherent/Not Human`
- `Conversation Could Not Happen Over Text`
- `Conversation Rhymes`

Hard gates that decide the call:

- One person sending two messages in a row is normal and is not a rejection reason.
- Texting participants cannot see, hear, touch, hand objects to, or observe each other unless the text says a photo/audio/video was shared.
- Treat the visible speaker labels as User IDs, including roles and pronouns such as `Captain`, `Sailor`, `PersonA`, or `Me`.

Per-reason definitions, evidence requirements, and pass/reject examples: `references/rubric.md` (`## Rejection Reasons`).

## Response Selection

Only select a response if the transcript passes. Pick the option that replies to the final message, fits context and speaker, sounds like a real casual text, and carries no rejection issue. Full good/bad criteria: `references/rubric.md` (`## Response Selection Rules`).

## Multiple-Choice Question

Answer from the original transcript only, never from the response you selected, and read the question wording literally. Question-by-question handling and the `Both` / `None of them` cases: `references/rubric.md` (`## Multiple-Choice Rule`).

## Output Format

Keep answers compact and practical:

```markdown
Summary: ...

Transcript: Pass/Reject
Reasons: ...

Best response: ...

MCQ answer: ...
```

If the user asks for reasoning, add one short sentence per decision. Avoid long commentary.

When a rejection reason is traceable, include the exact word or phrase so the user can verify it:

- `Spelling Mistake - "bannana" should be "banana".`
- `Unnecessary Repetition - "a a" in "for a a walk".`
- `Includes Name of Participant - "Thanks, Captain" mentions the other speaker label.`
- `Contains Emojis - emoji appears in "...".`
- `Conversation Rhymes - consecutive messages end with "today" and "away".`

## Final Checklist

Before finalizing:

- Summary is 30 words or fewer.
- Summary uses a natural human style where possible.
- Pass/Reject is based on the PDF reasons, not vibes.
- All rejection reasons were checked.
- Any traceable rejection reason includes the exact word or phrase.
- The other-participant name/User ID rule was checked against the exact speaker labels.
- Response selection only replies to the final message.
- The selected response has no rejection issue.
- MCQ answer ignores the selected response, uses only the original transcript, and follows the exact wording of the question.
