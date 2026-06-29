---
name: text-response-evaluator
description: Evaluate TELUS Text Response Evaluation tasks from transcript-based conversations. Use when Codex is asked to summarize a text-message transcript, decide Pass or Reject, choose all transcript rejection reasons, select the best reply to the final message, or answer the task's multiple-choice question using TELUS-TASKS/Text Response Evaluation guidelines.
---

# Text Response Evaluator

## Source Of Truth

Use `TELUS-TASKS/Text Response Evaluation/telus - Text_Response_Evaluation.pdf` as the source of truth. This skill is the workflow for applying that PDF. Do not use SBS, bot-reply validation, URL checking, OPR, or search-result flags for this task type unless the user separately asks for them.

Read `references/rubric.md` when doing an actual rating or when unsure about a rejection reason.

## Workflow

1. Confirm the task type is Text Response Evaluation, not SBS or bot reply validation.
2. Read the full transcript and identify the two participants.
3. Before deciding Pass/Reject, scan every message for hard rejection issues, especially whether either person mentions the other person's exact name/User ID.
4. Write a transcript summary in no more than 30 words.
5. Decide whether the transcript `Passes` or `Rejects`.
6. If it rejects, select every rejection reason that applies and stop response selection unless the task still requires a separate answer.
7. If it passes, evaluate all response options as replies to the final message only.
8. Choose the best response that is natural, context-aware, from the correct speaker's perspective, and free of rejection issues.
9. Answer the multiple-choice question using only the original transcript, not the selected response. Read the question wording exactly.

## Transcript Summary

Keep the summary short, plain, and factual.

- Maximum 30 words.
- Mention the main topic or topics.
- If the conversation has many unrelated topics or does not make sense, say that.
- Do not add outside assumptions.
- Do not name participants unless the names help clarity.
- Prefer the user's natural style: `[Name A] and [Name B] are talking about [topic]. [Name A] says/asks..., while [Name B]...`

Example:
`My friend is late for their first day of work and asks me for a ride.`

Preferred examples:

- `Chris and Alex are talking about the Egyptian pyramids. Chris claims aliens built them, while Alex argues that ancient Egyptians built them.`
- `Sailor and Captain are talking about whether to delay sailing because of a storm report. Sailor wants caution, while Captain thinks they can manage it.`

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

Important guardrails:

- Ignore punctuation and grammar for the spelling category. Rate spelling only.
- Use American English spelling.
- One person sending two messages in a row is normal and is not a rejection reason.
- Multiple topics are allowed if the conversation changes naturally.
- Reject overlapping, random, or robotic topic shifts.
- Texting participants cannot see, hear, touch, hand objects to, or observe each other unless the text says a photo/audio/video was shared. The PDF says no photos, audio, or video are shared by default.
- Treat the visible speaker labels as User IDs. This includes names, roles, labels, and pronouns such as `Chris`, `Alex`, `Captain`, `Sailor`, `Person A`, `PersonA`, or `Me`.
- Reject if one participant writes the other participant's exact speaker label/User ID, even if it sounds natural as a title, such as `Thanks, Captain.`
- Naming a third person who is not one of the two participants is allowed.

## Response Selection

Only select a response if the transcript passes.

Choose the option that:

- Replies to the last message, not an earlier message.
- Fits the context and tone.
- Comes from the correct speaker's perspective.
- Sounds like a casual text response a real person would send.
- Does not contain spelling mistakes, emojis, offensive language, impossible in-person actions, repetition, rhyming, or other transcript rejection issues.

Do not choose a response that:

- Repeats the previous message without answering it.
- Talks about a different topic.
- Uses placeholders like `[topic]`.
- Assumes the texters are physically together.
- Contains a spelling error or emoji, even if it otherwise fits.

## Multiple-Choice Question

Answer using the original transcript only. Ignore the response option you selected when answering the MCQ.

Read the wording carefully:

- `Who sent the last text?` asks for the last speaker.
- `Who did not send the last text?` asks for the other participant, unless both/none apply.
- `Who did not ask any questions?` requires checking every message for question marks or question wording from both participants.
- Do not answer from memory or from the previous task pattern.

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
