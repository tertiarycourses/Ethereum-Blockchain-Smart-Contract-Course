"""Single source of truth for TGS-2024045220 courseware v8."""

TITLE = "Generative AI (GenAI) Visuals in Photoshop and Firefly"
SHORT_TITLE = "Generative-AI-Visuals-in-Photoshop-and-Firefly"
COURSE_CODE = "TGS-2024045220"
VERSION = "v8"
VERSION_DATE = "13 October 2026"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "201200696W"
TRAINER = "Dr Alfred Ang"
TSC_TITLE = "Visual Communication"
TSC_CODE = "DSN-COM-4005-1.1"
DURATION = "2 days · 16 hours, including 2 hours of assessment"

LEARNING_OUTCOMES = [
    "LO1: Initiate visual communication through generative AI in Photoshop and Firefly.",
    "LO2: Create storyboards in Firefly for visual narratives and task flows.",
    "LO3: Propose enhancements through aesthetic analysis and advanced critique in Photoshop.",
    "LO4: Formulate generative-AI colour strategies in Photoshop.",
]

TSC_KNOWLEDGE = [
    ("K1", "Elements of typography, logos, visual communication design and information design."),
    ("K2", "Best practices for visual communication."),
    ("K3", "Uses of relevant visual-design software packages."),
    ("K4", "Colour fundamentals and forms."),
    ("K5", "Techniques for analysing aesthetics."),
]

TSC_ABILITIES = [
    ("A1", "Initiate visual communication ideas through exploration."),
    ("A2", "Develop outputs by integrating media, materials, processes and environments."),
    ("A3", "Create storyboards and task flows to communicate intentions."),
    ("A4", "Evaluate design work with stakeholders."),
    ("A5", "Propose suggestions to enhance visual formats."),
    ("A6", "Critique own and others' work using explicit criteria."),
    ("A7", "Develop strategies that strengthen the appeal of visual outputs."),
]

ASSESSMENT = {
    "written": "Written Assessment (WA/SAQ): 5 open-ended questions, 60 minutes, K1–K5.",
    "practical": "Practical Performance (PP): 4 tasks, 60 minutes, A1–A7.",
    "note": "Both instruments are individual, open book and competency based; no practice exam is included.",
}

TOPICS = [
    {"num": 1, "title": "GenAI for Visual Communication", "subtitle": "Turn an audience need into an intentional, rights-aware visual direction.", "codes": "LO1 · K1 · K2 · A1 · A2"},
    {"num": 2, "title": "Firefly Storyboards and Reference Control", "subtitle": "Control composition and style, then organise variations into a communicable flow.", "codes": "LO2 · K3 · A3"},
    {"num": 3, "title": "Photoshop Generative Editing and Critique", "subtitle": "Use selections and generative features to build, evaluate and improve editable composites.", "codes": "LO3 · K3 · K5 · A4 · A5 · A6"},
    {"num": 4, "title": "Colour Strategy, Enhancement and Delivery", "subtitle": "Build a coherent palette, preserve editability and verify the delivered visual.", "codes": "LO4 · K4 · K5 · A7"},
]


def _c(topic, title, mechanism, best_for, controls, watch, evidence, source):
    return {"topic": topic, "title": title, "mechanism": mechanism, "best_for": best_for,
            "controls": controls, "watch": watch, "evidence": evidence, "source": source}


CONCEPTS = [
    _c(1, "Human-led GenAI Creative Loop", "A human defines the brief, directs generation, selects evidence and remains accountable for publication.", "Fast exploration where intent and judgement matter more than raw variation count.", "Brief · prompt · variation · critique · edit · verify", "Automating the decision as well as the production.", "A decision log connects the selected visual to audience, purpose and acceptance criteria.", "Adobe Firefly Help"),
    _c(1, "GenAI Image Use Cases and Boundaries", "Generation, insertion, removal, expansion and translation solve different visual problems and carry different risks.", "Choosing an appropriate AI feature before opening a tool.", "Task type · rights · sensitivity · required control · delivery channel", "Using generation where faithful documentation is required.", "The chosen feature and boundary are justified against the brief.", "Adobe Photoshop Help"),
    _c(1, "Prompt Anatomy", "A useful prompt combines subject, action, setting, visual treatment, composition and constraints.", "Creating a clear starting direction without over-prescribing every pixel.", "Subject · action · setting · medium · lighting · camera · exclusions", "Contradictory adjectives, vague subjects and accidental text instructions.", "Prompt components can be traced to visible properties of the result.", "Adobe Firefly Help"),
    _c(1, "Prompt Iteration and Variation", "Changing one prompt factor at a time makes cause and effect observable.", "Converging from a broad direction to a defensible final candidate.", "Baseline · single-variable change · seed/variation · comparison notes", "Changing model, prompt, style and composition simultaneously.", "A contact sheet shows at least three labelled iterations and the selection reason.", "Adobe Firefly Help"),
    _c(1, "Visual Hierarchy and Emphasis", "Scale, contrast, position, isolation and detail establish what viewers notice first.", "Campaign visuals that need a clear focal point and reading order.", "Primary focal point · secondary cue · supporting detail · CTA space", "Competing focal points or an empty area that cannot hold useful copy.", "A squint test and thumbnail view preserve the intended reading order.", "Legacy trainer slides v6"),
    _c(1, "Scale, Balance and Alignment", "Relative size signals importance; visual mass and common edges stabilise the composition.", "Combining generated imagery with typography or brand elements.", "Scale ratio · visual weight · grid · edge alignment · safe area", "Centred-by-default layouts or tangencies that feel accidental.", "Guides and a reduced-size review confirm balance across the frame.", "Legacy trainer slides v6"),
    _c(1, "Contrast, Repetition and Negative Space", "Contrast separates roles, repetition creates coherence and negative space gives the message room to breathe.", "Social tiles, posters and storyboard frames that must scan quickly.", "Value contrast · colour contrast · repeated motif · breathing room", "Decorative repetition that overwhelms the subject.", "Grayscale and thumbnail checks confirm separation and rhythm.", "Legacy trainer slides v6"),
    _c(1, "Audience, Story and Responsible Provenance", "A visual is credible when its message fits the audience and its source, prompts and edits remain explainable.", "Commercial, organisational and public-facing visual communication.", "Audience need · claim risk · asset rights · prompt log · Content Credentials", "Misleading realism, unlicensed references or unsupported claims.", "A provenance note accompanies the editable master and export.", "Adobe Content Credentials"),

    _c(2, "Choosing a Firefly Image Model", "Firefly models offer different balances of speed, realism, prompt interpretation and control.", "Matching generation quality and latency to the storyboard purpose.", "Current model · output intent · speed · detail · available controls", "Assuming the newest model behaves identically to an older one.", "The selected model is recorded with a visible comparison or reason.", "Adobe Firefly Help"),
    _c(2, "Content Type and Visual Intensity", "Content type steers photo/illustration behaviour while visual intensity adjusts how strongly styling affects the result.", "Moving between documentary-looking and illustrative storyboard frames.", "Photo/art · auto mode · visual intensity · effects", "Treating intensity as a substitute for a clear prompt.", "Two controlled variants demonstrate the effect of the setting.", "Adobe Firefly Help"),
    _c(2, "Colour, Lighting and Camera Controls", "Secondary controls guide palette, lighting direction, field of view and depth cues.", "Keeping a sequence visually coherent without copying every frame.", "Colour/tone · lighting · camera angle · lens/depth cues", "A lighting instruction that conflicts with the reference composition.", "Frames share a documented palette and plausible light direction.", "Adobe Firefly Help"),
    _c(2, "Composition Reference", "A composition reference transfers spatial arrangement and structural relationships without duplicating the source pixels.", "Maintaining camera position, pose or layout across storyboard alternatives.", "Reference strength · crop · silhouette · dominant lines · prompt", "Using a reference without rights or expecting identity fidelity.", "Overlay or side-by-side evidence confirms structural similarity.", "Adobe Firefly Composition Reference"),
    _c(2, "Style Reference", "A style reference guides colour, texture, lighting and rendering character while the prompt controls subject matter.", "Unifying multiple scenes under one art direction.", "Reference strength · visual intensity · effects · prompt specificity", "Combining style and composition changes without a baseline.", "A contact sheet shows consistent treatment across different subjects.", "Adobe Firefly Style Reference"),
    _c(2, "Storyboard Architecture", "A storyboard converts a narrative into beats with a purpose, frame, transition and evidence for each beat.", "Explaining an experience, campaign sequence or task journey.", "Opening · context · action · transformation · outcome · CTA", "A gallery of attractive images with no causal sequence.", "Every frame has a caption, purpose and transition note.", "Legacy trainer slides v6"),
    _c(2, "Task Flow for Team Collaboration", "A task flow assigns inputs, decisions, hand-offs and review gates so visual work can be repeated by a team.", "Moving from ideation to approved, editable and channel-ready output.", "Owner · input · action · decision · output · reviewer", "Unowned approval steps or ambiguous version names.", "A flow diagram identifies ownership and acceptance at each gate.", "Legacy trainer slides v6"),
    _c(2, "Generated Texture with Editable Photoshop Type", "Generate a rights-aware texture as imagery. Keep editable type as the base layer, place the generated texture immediately above it, and clip the texture to the type so the letterforms control visibility without rasterising the text.", "Creating expressive display typography while keeping wording, font, colour and fit editable.", "Texture prompt · live type base layer · texture layer above · clipping mask · scale/position · colour overlay · tracking · legibility", "Reversing the clipping stack, treating generated pixels as editable copy, using obsolete Text Effects interfaces, or losing contrast at delivery size.", "The PSD retains a live type base layer, clipped texture layer immediately above it and named colour/fit controls; the reopened export passes a thumbnail legibility check.", "Adobe Photoshop Help — Create type; Create and manage clipping masks"),

    _c(3, "Photoshop Generative AI Feature Map", "Photoshop connects Generative Fill, Expand, Background, Harmonize and reference-based generation to selections and layers.", "Selecting the smallest feature that solves the editing problem.", "Selection · prompt/reference · model · variations · generated layer", "Flattening before review or confusing destructive and generated edits.", "The Layers panel shows the generated content and editable source structure.", "Adobe Photoshop Generative AI Overview"),
    _c(3, "Selection as a Generative Instruction", "Selection geometry defines where change may occur and gives the model contextual pixels at its boundary.", "Precise insertion, replacement and local repair.", "Selection edge · feather · context margin · mask · target layer", "Selections that clip shadows or include protected details.", "Selection/mask evidence and a 100% edge inspection are retained.", "Adobe Photoshop Help"),
    _c(3, "Generative Fill", "Generative Fill creates non-destructive variations on a new generated layer inside the selected region.", "Adding, replacing or removing local content with contextual blending.", "Prompt or blank prompt · model · variation · generated layer", "Anatomy errors, repeated textures and lighting mismatch.", "Before/after, selected variation and layered PSD prove the decision.", "Adobe Photoshop Generative Fill"),
    _c(3, "Generative Expand", "Generative Expand extends the canvas and synthesises contextual pixels beyond the original frame.", "Reframing a master visual for landscape, portrait and square channels.", "Crop ratio · anchor · prompt/blank · safe area · variation", "Extending low-quality edges or moving the focal point unintentionally.", "Three channel crops preserve subject integrity and useful copy space.", "Adobe Photoshop Generative Expand"),
    _c(3, "Generate Background and Harmonize", "Background generation replaces the environment; Harmonize adjusts a placed subject to the surrounding tone, colour and light.", "Fast composites that still require realistic integration.", "Subject isolation · background prompt · scale · contact shadow · Harmonize", "Floating subjects, incorrect perspective or inconsistent light direction.", "Layered before/after and zoomed edge/shadow evidence pass review.", "Adobe Photoshop Generative AI Overview"),
    _c(3, "Reference Image in Generative Fill", "A reference image provides additional visual guidance while the prompt and selection define the requested change.", "Improving consistency of an object, material or visual direction.", "Reference asset · rights · prompt · selection · variation", "Expecting an exact copy or using a reference without permission.", "The reference, selected output and rights record are stored together.", "Adobe Photoshop Reference Image"),
    _c(3, "Inpainting and Outpainting", "Inpainting changes content inside a boundary; outpainting synthesises beyond an existing boundary.", "Choosing between local repair and frame extension.", "Protected area · context overlap · seam location · content continuity", "Visible seams, repeated objects or altered protected content.", "A difference review confirms only the intended region changed.", "Adobe Photoshop Help"),
    _c(3, "Aesthetic Critique and Golden-ratio Heuristics", "Critique separates description, interpretation, evaluation and recommendation; compositional heuristics are prompts for judgement, not guarantees.", "Explaining why a visual works and proposing an actionable revision.", "Hierarchy · balance · rhythm · focal placement · audience fit · technical finish", "Treating a grid or ratio as proof of quality.", "A criterion-based critique identifies evidence, impact and one testable change.", "Legacy trainer slides v6"),

    _c(4, "Hue, Saturation, Brightness and Value", "Hue identifies colour family, saturation its intensity, and value/brightness its light-dark position.", "Diagnosing palette and separation before choosing an adjustment.", "Hue relationship · saturation range · value contrast · skin/brand constraints", "Increasing saturation when the problem is value separation.", "A palette swatch and grayscale review support the colour decision.", "Adobe Photoshop Help"),
    _c(4, "Adjustment Layers and Masks", "Adjustment layers store tonal or colour changes separately; masks control where each adjustment applies.", "Reversible campaign colour work and local corrections.", "Adjustment type · layer order · mask density · blend mode · opacity", "Painting directly on the only copy or leaving masks unnamed.", "Named adjustment layers and masks remain editable in the PSD.", "Adobe Adjustment Layers"),
    _c(4, "Histogram and Levels", "The histogram displays tonal distribution; Levels remaps black point, white point and midtones.", "Correcting global tonal range and identifying clipping.", "Channel · black point · gamma · white point · output levels", "Forcing every image to fill the histogram or clipping detail.", "Before/after histograms and highlight/shadow checks show controlled range.", "Adobe Photoshop Help"),
    _c(4, "Curves", "Curves remaps input to output values with points that target overall tone or individual colour channels.", "Fine contrast shaping and colour-balance correction.", "Anchor points · slope · channel · mask · clipping preview", "Too many points, banding or unwanted colour casts.", "A labelled Curves layer and before/after comparison show the intended change.", "Adobe Curves Help"),
    _c(4, "Colour Balance and Hue/Saturation", "Colour Balance shifts tonal ranges toward complementary colours; Hue/Saturation targets hue families and intensity.", "Harmonising composite elements and establishing a campaign palette.", "Shadows/midtones/highlights · target colour range · saturation · mask", "Global shifts that damage skin tones, neutrals or brand colours.", "Sampled swatches and targeted masks demonstrate controlled application.", "Adobe Photoshop Help"),
    _c(4, "Neural Filters and Restoration", "Neural Filters provide AI-assisted transformations that can output to a new layer for further review.", "Restoration, colourisation and portrait enhancement where source evidence is incomplete.", "Filter model · strength · output method · local cleanup · review", "Invented detail, identity changes or treating an AI result as historical fact.", "Original, AI output and manual corrections remain separately reviewable.", "Adobe Neural Filters"),
    _c(4, "Campaign Colour Consistency", "A campaign palette combines role-based colours, contrast targets and adjustment recipes across assets.", "Keeping storyboard, social and poster outputs recognisably related.", "Primary/secondary/accent roles · value range · accessibility · export profile", "Matching hex values while ignoring surrounding colour and output profile.", "A palette sheet and three channel exports show consistent roles.", "Legacy trainer slides v6"),
    _c(4, "Output Verification and Content Credentials", "Professional delivery includes export settings, reopen checks, provenance and a retained editable master.", "Hand-off to stakeholders, publication and audit-ready delivery.", "Format · dimensions · profile · compression · metadata · Content Credentials", "Assuming an exported file is correct without reopening it.", "PSD, verified JPEG and provenance/read-me record form one evidence package.", "Adobe Content Credentials"),
]


def _lab(num, topic, slug, title, objective, scenario, assets, steps, evidence, acceptance, slide_image):
    return {"num": num, "topic": topic, "slug": slug, "title": title, "objective": objective,
            "scenario": scenario, "assets": assets, "steps": steps, "evidence": evidence,
            "acceptance": acceptance, "slide_image": slide_image}


LABS = [
    _lab(1, 1, "prompt-to-image-visual-brief", "Prompt-to-Image Visual Brief",
         "Translate an audience brief into a controlled Firefly prompt set and selected visual direction.",
         "A reading campaign needs an imaginative hero image with clear copy space for a social tile.",
         [("reference/lab reference 1/02 Turning descriptions into images/02-02-Creating your first prompt/Firefly_a dog reading a book while sitting at a desk by candle light, while wearing glasses,  120801.jpg", "dog-reading-reference.jpg"),
          ("reference/lab reference 1/02 Turning descriptions into images/02-03-Understanding Firefly models/model4.jpg", "firefly-model-reference.jpg")],
         ["Create a folder named `working` and preserve the supplied JPEGs unchanged.", "Write a one-sentence brief naming audience, message, channel, aspect ratio and required copy space.", "Draft a baseline prompt using subject, action, setting, visual treatment, composition and lighting.", "Generate a first set in Firefly and record the model and content type used.", "Change only one prompt factor for iteration two; label the changed factor.", "Change a different single factor for iteration three; retain all three prompt/result records.", "Compare the candidates for hierarchy, copy space, artefacts, audience fit and rights/provenance.", "Export the selected candidate as `lab01-selected.jpg` and save `lab01-decision-log.txt`."],
         "Three prompt/result records, selected JPEG and decision log identifying A1 exploration and A2 integration decisions.",
         ["At least three controlled prompt iterations are retained.", "The selected JPEG has a clear focal point and intentional copy space.", "The log records model, prompt, selection reason and provenance consideration."],
         "reference/lab reference 1/02 Turning descriptions into images/02-02-Creating your first prompt/Firefly_a dog reading a book while sitting at a desk by candle light, while wearing glasses,  120801.jpg"),
    _lab(2, 1, "design-principles-prompt-refinement", "Design Principles and Prompt Refinement",
         "Use Photoshop layout evidence to refine a generated visual against hierarchy, balance and contrast criteria.",
         "A creative studio wants a poster-ready yarn-art visual with one strong headline zone.",
         [("reference/lab reference 1/03 Using advanced settings/03-03-Creating your own Structure reference/reference.psd", "structure-reference.psd"),
          ("reference/lab reference 1/03 Using advanced settings/03-03-Creating your own Structure reference/reference.jpg", "structure-reference.jpg")],
         ["Open `structure-reference.psd` and immediately save `lab02-working.psd`.", "Inspect layer names, canvas ratio, dominant lines and negative-space zones.", "Create guides for a primary focal area, headline zone and safe margins.", "Write a Firefly prompt that preserves the structural intent while changing subject or material.", "Generate at least two candidates and place them as separate Smart Object layers.", "Add editable placeholder type to test hierarchy; do not embed essential copy in generated pixels.", "Compare scale, alignment, value contrast and breathing room at Fit and thumbnail views.", "Retain the stronger candidate, name all layers and export `lab02-poster.jpg`."],
         "Layered PSD, exported JPEG and a short comparison note covering K1/K2 design principles.",
         ["PSD contains guides, editable type and separate candidate layers.", "The final hierarchy remains clear at thumbnail size.", "Comparison note cites at least three explicit design criteria."],
         "reference/lab reference 1/03 Using advanced settings/03-03-Creating your own Structure reference/reference.jpg"),
    _lab(3, 2, "composition-and-style-references", "Composition and Style References",
         "Create a controlled Firefly comparison using composition and style references independently and together.",
         "A wellness campaign needs varied subjects that retain one composition and art direction.",
         [("reference/lab reference 1/03 Using advanced settings/03-03-Creating your own Structure reference/reference.jpg", "composition-reference.jpg"),
          ("reference/lab reference 1/03 Using advanced settings/03-04-Using a Style reference/hummingbird.jpg", "style-reference.jpg")],
         ["Confirm the supplied references are used only for this authorised learning activity.", "Write one subject prompt and generate a baseline without references.", "Add `composition-reference.jpg`, select a moderate strength and generate a second set.", "Remove the composition reference, add `style-reference.jpg` and generate a third set.", "Apply both references and generate a fourth set without changing the core subject prompt.", "Export one candidate from each condition using descriptive filenames.", "Create a four-up comparison canvas in Photoshop with editable labels.", "Record which setting best controlled structure, treatment and campaign consistency."],
         "Four labelled JPEG conditions, comparison PSD and a reference-control decision note.",
         ["Baseline, composition-only, style-only and combined results are present.", "Only the intended reference condition changes between comparisons.", "Decision note distinguishes structural and stylistic influence."],
         "reference/lab reference 1/03 Using advanced settings/03-04-Using a Style reference/hummingbird.jpg"),
    _lab(4, 2, "storyboard-and-task-flow", "Storyboard and Task Flow",
         "Build a five-frame Firefly storyboard and a team task flow that communicates intent and ownership.",
         "A fictional Wellness Week Singapore 2026 campaign needs a short visual journey from stress to restorative action.",
         [("reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.psd", "storyboard-starter.psd"),
          ("reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.jpg", "storyboard-reference.jpg")],
         ["Save the PSD as `lab04-storyboard.psd` and inspect its editable frame structure.", "Write five beats: opening, context, action, transformation and outcome/CTA.", "Define a shared palette, lighting direction, aspect ratio and style reference for the sequence.", "Generate one candidate for each beat, keeping the documented shared controls constant.", "Place each candidate in its own Smart Object frame and add editable captions.", "Create a task-flow panel naming owner, input, action, review gate and output for generation, Photoshop edit and approval.", "Review continuity of subject, palette, lighting and causal sequence with a peer.", "Revise one frame, record the reason and export `lab04-storyboard.jpg`."],
         "Five-frame layered storyboard PSD, exported JPEG, task-flow panel and peer-review note.",
         ["Every frame has a purpose and transition caption.", "Task flow includes ownership and an approval gate.", "At least one revision is traceable to stakeholder or peer feedback."],
         "reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.jpg"),
    _lab(5, 3, "generative-fill", "Generative Fill: Directed Inpainting",
         "Use a controlled selection and Generative Fill to add, replace and remove content non-destructively.",
         "An editorial wildlife visual needs a plausible environmental detail without damaging the original subject.",
         [("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-01-Using generative fill in Photoshop/elephant-start.psd", "elephant-start.psd")],
         ["Open `elephant-start.psd` and save `lab05-generative-fill.psd`.", "Duplicate the source group and identify protected subject edges.", "Draw a selection with enough surrounding context for one added environmental detail.", "Run Generative Fill with a concise prompt and retain at least three variations.", "Select the strongest variation by edge, light, scale and narrative fit.", "Create a second selection and use a blank prompt for a controlled removal.", "Inspect both edits at Fit and 100%, refining masks without flattening.", "Export `lab05-final.jpg` and capture the Layers panel as evidence."],
         "Layered PSD, selected variations, final JPEG and zoomed edge/Layers-panel evidence.",
         ["Original pixels remain protected.", "Generated edits are on named generated layers with editable masks.", "Edges, lighting and scale pass 100% inspection."],
         "reference/lab reference 1/02 Turning descriptions into images/02-06-Using content types and styles/Firefly_a robot dancing at a party 830052.jpg"),
    _lab(6, 3, "background-and-harmonize", "Background Replacement and Harmonize",
         "Generate a new background, integrate a placed element and evaluate lighting, perspective and contact.",
         "A portrait must be adapted into an outdoor campaign visual while remaining editable.",
         [("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/photoshoot-start.psd", "photoshoot-start.psd"),
          ("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/park bench.jpg", "park-bench.jpg")],
         ["Open the starter PSD and save `lab06-harmonize.psd`.", "Inspect subject isolation and refine the mask around hair, clothing and contact edges.", "Generate a background that provides compatible camera height, light direction and copy space.", "Place `park-bench.jpg` as a Smart Object and remove its original background non-destructively.", "Scale and position the bench using perspective and believable subject relationship.", "Use Harmonize where available, outputting to an editable layer; otherwise use clipped adjustment layers.", "Add or refine contact shadow and compare before/after at Fit and 100%.", "Export `lab06-final.jpg` and record the critique criteria used."],
         "Layered PSD, final JPEG, before/after comparison and criterion-based integration note.",
         ["Subject and placed element masks remain editable.", "Light, perspective and contact shadow are visually coherent.", "The note evaluates at least four explicit aesthetic/technical criteria."],
         "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/park bench.jpg"),
    _lab(7, 3, "generative-expand-channel-ratios", "Generative Expand for Channel Ratios",
         "Extend one master visual into square, landscape and portrait variants without losing hierarchy.",
         "A campaign hero must work across social, presentation and mobile-story channels.",
         [("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-04-Generative expand/koala-start.psd", "koala-start.psd"),
          ("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-04-Generative expand/landscape-start.jpeg", "landscape-start.jpeg")],
         ["Open `koala-start.psd`, save `lab07-master.psd` and identify protected subject pixels.", "Create a square 1:1 variant with Generative Expand and intentional copy space.", "Create a 16:9 landscape variant, adjusting the anchor to protect the focal point.", "Create a 9:16 portrait variant with adequate top and bottom safe areas.", "Retain at least two variations for any ratio with repeated objects or seams.", "Inspect edges, repeated textures and subject anatomy at 100%.", "Add non-destructive cleanup layers only where required.", "Export `lab07-square.jpg`, `lab07-landscape.jpg` and `lab07-portrait.jpg`."],
         "Master PSD plus three channel JPEGs and a ratio-by-ratio verification checklist.",
         ["All three aspect ratios are delivered.", "Focal hierarchy and protected subject details remain intact.", "No visible seams or repeated artefacts remain at 100%."],
         "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-04-Generative expand/landscape-start.jpeg"),
    _lab(8, 3, "reference-image-composition", "Reference Image and Multi-Prompt Composition",
         "Use a permitted reference image and staged selections to construct a coherent multi-element composition.",
         "A fashion visual requires an altered garment treatment that follows a supplied material reference.",
         [("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-06-Using reference/coat-start.psd", "coat-start.psd"),
          ("reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-06-Using reference/reference.jpeg", "garment-reference.jpeg")],
         ["Open `coat-start.psd`, save `lab08-reference-image.psd` and inspect existing masks.", "Record the supplied reference filename and authorised learning-use context.", "Select only the garment region, preserving face, hands and background.", "Invoke Generative Fill with `garment-reference.jpeg` as the reference and a concise material/colour prompt.", "Review variations for garment boundary, folds, lighting and identity preservation.", "Create a second isolated selection for one supporting accessory or background detail.", "Critique the result using description, interpretation, evaluation and recommendation; make one traceable revision.", "Export `lab08-final.jpg` and save the critique as `lab08-critique.txt`."],
         "Layered reference-guided PSD, final JPEG, rights note and four-part critique with revision.",
         ["Protected identity and background regions remain unchanged.", "Reference asset and selected variation are retained with the PSD.", "The critique leads to one visible, traceable improvement."],
         "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-06-Using reference/reference.jpeg"),
    _lab(9, 4, "restoration-critique-colour", "Restoration, Critique and Colour Strategy",
         "Restore a damaged image, evaluate invented detail and develop a reversible colour treatment.",
         "An archive image will support a heritage-wellness story but must not imply certainty where AI reconstructs missing detail.",
         [("reference/lab reference 3/Ch 2/02_07_restoration/old-damaged-image-start.psd", "old-damaged-image-start.psd"),
          ("reference/lab reference 1/09 Adobe Firefly for enterprise/09-03-Style kits/model.jpeg", "colour-reference.jpeg")],
         ["Open the damaged PSD and save `lab09-restoration.psd` without altering the original layer.", "Use a Neural Filter or restoration workflow with output set to a new layer.", "Inspect faces, hands, edges and repeating texture; mask or retouch unsupported artefacts.", "Create a Levels or Curves adjustment layer to establish usable tonal range without clipping.", "Develop a restrained palette using Colour Balance or Hue/Saturation adjustment layers and masks.", "Compare the original, AI-only and corrected states at Fit and 100%.", "Write a critique distinguishing observed source detail from AI-inferred detail.", "Export `lab09-final.jpg` and retain a palette swatch layer in the PSD."],
         "Layered restoration PSD, verified JPEG, palette swatches and critique of AI-inferred detail.",
         ["Original, AI output and manual corrections remain separately reviewable.", "Tonal range avoids unintended highlight/shadow clipping.", "The critique discloses uncertainty and proposes a defensible enhancement."],
         "reference/lab reference 1/09 Adobe Firefly for enterprise/09-03-Style kits/model.jpeg"),
    _lab(10, 4, "wellness-campaign-capstone", "Wellness Campaign Capstone",
         "Integrate A1–A7 into an editable campaign visual, storyboard summary, critique and colour-delivery package.",
         "Fictional Wellness Week Singapore 2026 needs a coherent hero visual and three channel exports for a positive, inclusive message.",
         [("reference/tms/PP - Generative AI (GenAI) Visuals in Photoshop and Firefly.psd", "wellness-campaign-start.psd"),
          ("reference/tms/PP - Generative AI (GenAI).jpg", "wellness-campaign-reference.jpg")],
         ["Open the starter PSD, save `lab10-capstone.psd` and write a brief naming audience, message and channels.", "Explore at least two Firefly directions; record prompt, model, references and selection rationale.", "Integrate the selected result with the supplied PSD using named layers, masks and generated layers.", "Create a three-frame storyboard strip showing problem, restorative action and outcome/CTA.", "Ask a peer to evaluate hierarchy, inclusivity, aesthetics, technical finish and message fit; record the feedback.", "Propose and implement at least two traceable enhancements based on the critique.", "Create a role-based colour strategy with primary, secondary and accent swatches plus reversible adjustment layers.", "Export square, landscape and portrait JPEGs; reopen each and record dimensions, colour profile and visual verification."],
         "Layered master PSD, prompt log, storyboard strip, peer critique, enhancement record, palette and three verified JPEGs.",
         ["The package visibly demonstrates A1–A7.", "All adjustments and generated elements remain editable and named.", "Three exports are reopened and pass dimension, colour and visual checks.", "Provenance and asset-permission notes accompany delivery."],
         "reference/tms/PP - Generative AI (GenAI).jpg"),
]

SOURCES = [
    ("Official course page", "https://www.tertiarycourses.com.sg/wsq-generative-ai-genai-visuals-in-photoshop-and-firefly.html"),
    ("Legacy trainer slides v6", "reference/WSQ - Master Trainer Slides - Generative AI (GenAI) Visuals in Photoshop and Firefly - v6.pptx"),
    ("Original practical lab references", "reference/lab reference 1; reference/lab reference 2; reference/lab reference 3"),
    ("Live LMS-TMS assessment papers", "reference/tms/original-WA.docx; reference/tms/original-PP.docx"),
    ("Adobe Firefly Text to Image", "https://helpx.adobe.com/firefly/web/work-with-images/generate-images/generate-images-from-text-descriptions.html"),
    ("Adobe Firefly Style Reference", "https://helpx.adobe.com/firefly/web/work-with-images/generate-images/reference-images-for-styling.html"),
    ("Adobe Firefly Composition Reference", "https://helpx.adobe.com/firefly/web/work-with-images/generate-images/match-image-composition-to-reference-image.html"),
    ("Adobe Photoshop Generative AI Overview", "https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html"),
    ("Adobe Photoshop Reference Image", "https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/use-reference-images-for-consistent-results.html"),
    ("Adobe Photoshop Generative Model Control", "https://helpx.adobe.com/photoshop/desktop/generative-ai/select-an-ai-model-for-generative-control.html"),
    ("Adobe Neural Filters", "https://helpx.adobe.com/photoshop/desktop/effects-filters/neural-filters/use-neural-filters-to-enhance-images.html"),
    ("Adobe Adjustment Layers", "https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html"),
    ("Adobe Curves Help", "https://helpx.adobe.com/photoshop/using/curves-adjustment.html"),
    ("Adobe Content Credentials", "https://helpx.adobe.com/au/firefly/web/get-started/learn-the-basics/content-credentials-overview.html"),
    ("Adobe Firefly Product Terms", "https://helpx.adobe.com/legal/product-descriptions/adobe-firefly.html"),
]
