---
name: text-response-evaluator
description: Evaluate TELUS Text Response Evaluation tasks from transcript-based conversations. Use when asked to summarize a text-message transcript, decide Pass or Reject, choose all transcript rejection reasons, select the best reply to the final message, or answer the task's multiple-choice question using TELUS-TASKS/Text Response Evaluation guidelines.
---

# Text Response Evaluator

## File Locations

- `references/...` paths are inside this skill's folder.
- `TELUS-TASKS/...` is a sibling folder of this skills repo in the workspace root (e.g. `<workspace>/train-ai/TELUS-TASKS/`).
- Blank task template: `TELUS-TASKS/task-templates/text-response-evaluation.md`. Every TELUS task type has one there; the live task the user is working on is `TELUS-TASKS/task.md`.
- If a referenced external file cannot be found, use this skill's reference files as the operative rubric and state that the source was unavailable.

## Source Of Truth

Use `TELUS-TASKS/Text Response Evaluation/telus - Text_Response_Evaluation.pdf` as the source of truth. This skill is the workflow for applying that PDF. Do not use SBS, bot-reply validation, URL checking, OPR, or search-result flags for this task type unless the user separately asks for them.

Read `references/rubric.md` when doing an actual rating or when unsure about a rejection reason.

Read the full conversation before answering anything. Never infer from a dropdown option that is already selected in the task — a pre-selected value is not evidence, and treating it as one means grading the tool's default rather than the transcript.

> **Output goes in the chat response only.** Task files and every other file in the workspace are READ-ONLY input. Never edit, overwrite, or write your answer into them, and never create scratch or working files. Present the complete result in chat using the Output Format template below.

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
10. Pass the Pre-Submission Self-Audit before submitting any rating. The shared cross-skill standard is `../telus-evaluator/references/quality-gate.md`.

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

## Pre-Submission Self-Audit (MANDATORY)

Answer all six questions in writing, with the evidence named, before any decision is submitted. A tick mark is not an answer. If you cannot produce the evidence for an item, you have not finished that step: stop, go do it, then return.

1. **Did I actually read the whole transcript, or am I working from the first few lines?**
   Evidence: the two exact speaker labels listed before grading, the count of messages, and the final message quoted. The 3-step Hard check in `references/rubric.md` (`### Includes Name Of Participant`) must be run against those exact labels, not from memory of the names. If you have not read every message, you cannot make a Pass or Reject call yet.

2. **Did I read the lines in context, or did I pattern-match on a word?**
   Evidence: for every rejection reason you select, the exact word or phrase quoted from the transcript, read in its sentence. A doubled word is not automatically Unnecessary Repetition (`I know that that is not true` passes, `going to to Iceland` rejects). A shared ending word is not a rhyme; the rhyming words must be different and must end consecutive messages. If the only thing you can point to is that something looked odd, that is not evidence.

3. **Did I check every rejection reason on its own?**
   Evidence: all eight reasons named, each with its own verdict and its own evidence or an explicit "checked, none found". No block clearing, no "the rest are fine". The response selection and the MCQ each get their own reasoning, and the MCQ is answered from the original transcript only.

4. **Is my calibration honest, neither generous nor harsh?**
   Evidence: for each selected reason, name the `references/rubric.md` definition you applied.
   - Too generous looks like: passing a transcript that contains a real American-English spelling mistake because the intent was clear, or passing an in-person cue such as "Did you get your hair cut? It looks great!" which is a Conversation Could Not Happen Over Text reject.
   - Too harsh looks like: rejecting because one person sent two messages in a row (explicitly not a rejection reason), rejecting sensible repetition (`When I last saw it, it was...`), rejecting on punctuation or grammar when the rule is to rate spelling only, or rejecting for naming a third person who is not in the conversation.

5. **Did I apply every context factor that applies here?**
   State each explicitly, and say so when it does not apply:
   - **Language standard**: spelling and offensive language are judged in American English (`### Spelling Mistake`, `### Offensive Language`).
   - **The text medium**: the participants cannot see, hear, touch, hand objects to, or observe each other unless the text says a photo, audio, or video was shared.
   - **Time sensitivity, position, and variety**: do not apply. This task judges one transcript against fixed reasons, not dated or ordered results.

6. **Does my output match the taught pattern?**
   Re-read the `## Summary Rules` examples in `references/rubric.md` and the Output Format block below immediately before writing, not from memory. Then confirm: the summary is 30 words or fewer with the count actually counted, it uses plain language and the natural two-person style where it fits (`[Name A] and [Name B] are talking about [topic]...`), and every traceable rejection reason is written in the taught form, such as `Spelling Mistake - "bannana" should be "banana".`

## Holding the Line Under Challenge

You will be asked things like "are you sure you read every message?", "are you sure that word is actually misspelled?", or "did you check all eight reasons?".

- Treat each challenge as an instruction to re-verify against the rubric and the transcript. It is not a signal that your answer was wrong.
- Answer with specifics: the speaker labels, the quoted line, and the rubric definition applied.
- Change a Pass/Reject call, a reason, a response choice, or an MCQ answer **only** when the rubric and the transcript show it was wrong. Name what changed and which rule drove it.
- If the transcript supports what you already said, say so plainly and quote it. Do not soften the call or add a reason you cannot evidence just to look thorough.
- If you cannot produce the quote, say so directly and go re-read the transcript. Never write a justification after the fact.
- The rubric and the source PDF are the single source of truth. Neither the user's preference nor your own earlier answer outranks them.

## Output Format

Present all five sections in chat, in this order. Keep the headings and fill every one. If a section does not apply (for example, response selection after a reject), keep the heading and say why in one line.

````markdown
## Text Response Evaluation

### 1. Transcript
- **Participants:** speaker A and speaker B labels as shown
- **Messages read:** N, in full

### 2. Summary
30 words maximum, covering what both participants discuss.

### 3. Verdict
**Transcript: Pass** or **Reject**

Reasons, one line each, quoting the exact text so the user can verify it:
- `Spelling Mistake - "bannana" should be "banana".`

### 4. Best Response
The chosen reply, plus one line on why it fits the final message and the correct speaker's perspective.

### 5. MCQ Answer
The selected option, plus the line from the transcript it comes from.
````

Keep it practical. One short sentence per decision is enough; avoid long commentary.

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
