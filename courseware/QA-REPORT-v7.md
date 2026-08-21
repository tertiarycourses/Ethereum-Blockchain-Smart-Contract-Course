# Courseware QA Report — v7

**Course:** Generative AI (GenAI) Visuals in Photoshop and Firefly  
**Course code:** TGS-2024045220  
**Audit date:** 21 August 2026

## Release requirement override

The installed `/courseware-qa` text contains a generic mandatory practice-exam check. The explicit course requirement is **do not add a practice exam**, so that stale generic check is overridden. The PPT, Learner Guide, labs and assessment set were scanned and contain no practice exam.

## A. PPT quality — PASS

- 114-slide v7 deck; course code, provider and UEN are present.
- Separate General Trainer Profile and Dr Alfred Ang profile slides are present.
- Visual LMS-TMS course-material slide and a clickable learner-labs slide are present.
- Assessment Briefing precedes Assessment Design; final flow maps WA to PP and sign-off.
- Five editable native PowerPoint charts render correctly.
- 44 embedded pictures plus the generated cover hero provide visual evidence and examples.
- No click-by-click procedures occur in the PPT; lab slides carry only purpose, high-level actions and evidence.
- Structural scan found no off-slide shapes, overlap or clipped text. All 114 rendered pages were reviewed; the final Thank You slide is white.

## B. Assessment quality — PASS

- Original count preserved: 5 WA questions and 4 PP tasks.
- Original instrument preserved: Written Assessment plus Practical Performance.
- Timing preserved from the live approved papers: 60 minutes WA and 60 minutes PP.
- All questions are open-ended; no multiple-choice items.
- All four v4 DOCX files carry the correct WSQ instrument cover.
- Question-paper page 2 contains trainee information, instructions, grading and the clickable LMS route; assessment content begins on page 3.
- Structural assessment verifier passed all four rendered files.

| Criterion | Assessment item | Course evidence |
|---|---|---|
| K1 | WA Question 1 | Topic 1; Labs 1–2 |
| K2 | WA Question 2 | Topic 1; Labs 1–2 |
| K3 | WA Question 3 | Topics 2–3; Labs 3–8 |
| K4 | WA Question 4 | Topic 4; Labs 9–10 |
| K5 | WA Question 5 | Topics 3–4; Labs 6, 8–10 |
| A1–A2 | PP Task 1 | Labs 1, 5–6 |
| A3–A4 | PP Task 2 | Lab 4 |
| A5–A6 | PP Task 3 | Labs 6, 8–9 |
| A7 | PP Task 4 | Labs 9–10 |

## C. Lesson Plan — PASS

- WSQ cover, v7 version-control record, learning outcomes and two-day schedule are present.
- Slide references match the generated `slide_map.json`: Labs 1–10 map to slides 37, 38, 58, 59, 79, 80, 81, 82, 103 and 104.
- Assessment block is 2 hours total and maps K1–K5/A1–A7.
- Final DOCX rendered cleanly to 6 pages; the current PDF is included.

## D. Learner Guide — PASS

- WSQ cover and v7 version-control record are present.
- `LEARNER-GUIDE.md` and the DOCX contain the same 4 topics, 32 concepts and 10 labs.
- Every lab contains a detailed eight-step procedure, evidence requirements and acceptance criteria.
- Final DOCX rendered cleanly to 29 pages with all embedded images; the current PDF is included.

## E. Labs and alignment — PASS

- Ten individual self-contained folders exist.
- Every folder contains `README.md`, `README.pdf`, and at least one PSD or JPEG source asset.
- Labs, PPT, Learner Guide and PP tasks share the same lab sequence and evidence model.

## F. Files and distribution — PASS

- Current PPTX/PDF, Learner Guide DOCX/PDF and Lesson Plan DOCX/PDF are present in `courseware/`.
- Only v7 trainer-slide outputs are present.
- Assessment material remains in `assessment/` and is excluded from the public GitHub release.
- Candidate papers are designated for learner access on Drive; answer keys are designated trainer-only.

## Overall verdict

**PASS — ready for Drive dry-run and LMS-TMS publication preflight.**
