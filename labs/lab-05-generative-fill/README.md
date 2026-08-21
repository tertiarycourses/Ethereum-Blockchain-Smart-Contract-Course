# Lab 05 — Generative Fill: Directed Inpainting

**Course:** Generative AI (GenAI) Visuals in Photoshop and Firefly (`TGS-2024045220`)
**Version:** v7 · 21 August 2026

## Scenario

An editorial wildlife visual needs a plausible environmental detail without damaging the original subject.

## Objective

Use a controlled selection and Generative Fill to add, replace and remove content non-destructively.

## Supplied Photoshop/JPEG files

- `elephant-start.psd`

## Detailed procedure

1. Open `elephant-start.psd` and save `lab05-generative-fill.psd`.
2. Duplicate the source group and identify protected subject edges.
3. Draw a selection with enough surrounding context for one added environmental detail.
4. Run Generative Fill with a concise prompt and retain at least three variations.
5. Select the strongest variation by edge, light, scale and narrative fit.
6. Create a second selection and use a blank prompt for a controlled removal.
7. Inspect both edits at Fit and 100%, refining masks without flattening.
8. Export `lab05-final.jpg` and capture the Layers panel as evidence.

## Evidence to retain

Layered PSD, selected variations, final JPEG and zoomed edge/Layers-panel evidence.

## Acceptance criteria

- [ ] Original pixels remain protected.
- [ ] Generated edits are on named generated layers with editable masks.
- [ ] Edges, lighting and scale pass 100% inspection.

## Reflection prompts

- Which decision most improved the message or focal hierarchy?
- How does the Layers panel prove that the workflow remains editable?
- What rights or provenance evidence must accompany the finished image?
