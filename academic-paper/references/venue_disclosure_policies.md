# AI-Usage Disclosure Policy Database — v2

**Snapshot date**: 2026-04-09 (original v1 database build; individual rows carry their own "access date" recording when each was last re-verified)
**Scope**: v1 (2026-04) covered 6 ML/NLP-focused venues (ICLR, NeurIPS, Nature, Science, ACL, EMNLP). v2 (2026-07, #596) adds 7 medical-publishing policy targets: the ICMJE umbrella recommendations, four ICMJE member journals (BMJ, JAMA, The Lancet, NEJM), PLOS, Frontiers. Education/QA journals remain deferred.
**Maintenance**: policies drift. Before submission, the user should verify against the venue's current page. The "source URL" and "access date" below record when ARS last verified each policy.
**Ordering note**: all entries are kept in one global alphabetical order by canonical English label (per step 5 of "Adding a new venue" below).

---

## Evidence-layer contract

This file is the venue track's policy-evidence layer consumed by `disclosure_mode_protocol.md`. It contains source provenance, policy wording, prohibited uses, and placement evidence; it contains no executable renderer directives. Selector aliases, applicability predicates, required/conditional fact mappings, halt outcomes, advisories, and rendering behavior exist only in the protocol. The two surfaces require coordinated maintenance when a target changes. This evidence file is not a standalone disclosure template.

Unknown-venue handling is defined exclusively in `disclosure_mode_protocol.md`;
free policy prose, whether pasted or recorded here, is not an executable
category-to-field mapping.

---

## Venue: ACL (Association for Computational Linguistics)

| Field | Value |
|---|---|
| Source URL | https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics#Guidelines_for_Generative_Assistance_in_Authorship |
| Access date | 2026-06-07 |
| Policy summary | Use of generative AI to create content must be fully disclosed in the **Acknowledgements** section (the policy's own example: "Section 3 was written with inputs from ChatGPT"). Disclosure is graduated by use type: language-only assistance (paraphrasing/polishing) and short-form input assistance (predictive keyboards) do **not** require disclosure; low-novelty text generation and AI-suggested new ideas **do**. AI literature-search tools require no special disclosure but the usual citation-accuracy and thoroughness requirements still apply. Authors are fully responsible for all submitted content. |
| Required phrasing elements | Name the tool and the specific content it produced (the policy example states the section and the tool). For low-novelty generated text, also affirm the output was checked for accuracy and carries appropriate citations for both the source text and the source idea(s). |
| Preferred disclosure location | The **Acknowledgements** section (per the ACL Admin Wiki current guidance). The 2023-era separate "Use of AI Assistance" subsection is no longer the canonical location. |
| Prohibited uses | Listing a generative AI tool as an author. Using automated tools that rephrase existing work as one's own without attribution (treated as plagiarism). Generated text that copies existing work is subject to the plagiarism policy. |
| Authorship rule | AI tools cannot be listed as authors; ACL does not consider a generative model an entity that can fulfill co-authorship requirements |
| Notes | Source is the org-wide ACL Admin Wiki policy (ACL Exec-approved, current through 2025), which ARR / EMNLP 2026 link to for current paper-integrity guidance. Supersedes the 2023 ACL conference blog URL (still live but stale: it pointed disclosure at a dedicated subsection rather than Acknowledgements). |

---

## Venue: BMJ (The BMJ / BMJ Publishing Group)

| Field | Value |
|---|---|
| Source URL | https://authors.bmj.com/policies/ai-use/ |
| Access date | 2026-07-31 |
| Policy summary | BMJ considers content produced with AI; its "approach is one of transparency". The policy applies to all content formats (text, audio, video, images, data) and is explicitly WAME/COPE-aligned. BMJ expects adequate declaration and says authors should declare AI use; inadequate declaration can lead to rejection or, post-publication, to corrective action. |
| Required phrasing elements | Declare what AI technology was used, why it was used, and how it was used. Authors should consider providing a **summary of the input, output, and the way the authors reviewed the AI output** as supplementary files or additional information for editorial review. |
| Preferred disclosure location | **Contributor section** (acknowledgement of AI use); research-related AI use additionally requires a fuller description in **Methods**. |
| Prohibited uses | Listing AI as an author. Inadequate declaration of AI use (grounds for rejection or post-publication action). Peer reviewers putting unpublished manuscripts into publicly available AI tools. |
| Authorship rule | "AI technologies will not be accepted as an author(s) of any content submitted to BMJ for publication." |
| Notes | BMJ is an ICMJE member journal. The ICMJE umbrella recommendations and BMJ's own AI-use page are simultaneously relevant sources; neither source states that it silently replaces the other. |

---


## Venue: EMNLP (Empirical Methods in Natural Language Processing)

| Field | Value |
|---|---|
| Source URL | https://2026.emnlp.org/paper-integrity-policy/ (refers authors to ACL's generative-authorship guidelines; canonical text at the ACL Admin Wiki — see ACL row) |
| Access date | 2026-06-07 |
| Policy summary | For AI-assistance disclosure, EMNLP refers authors to ACL's generative-authorship guidelines. Same requirements apply. See ACL row. |
| Required phrasing elements | Same as ACL |
| Preferred disclosure location | Same as ACL: the **Acknowledgements** section |
| Prohibited uses | Same as ACL |
| Authorship rule | Same as ACL |
| Notes | EMNLP 2026 maintains its own Paper Integrity Policy page that refers authors to ACL's generative-authorship guidelines for this issue (and carries additional EMNLP/ARR-specific integrity policies beyond AI disclosure). The canonical source for the AI-disclosure rules below is the ACL Admin Wiki (see ACL row). |

---

## Venue: Frontiers (Frontiers journals)

| Field | Value |
|---|---|
| Source URL | https://www.frontiersin.org/guidelines/policies-and-publication-ethics |
| Access date | 2026-08-01 |
| Policy summary | Section "Artificial intelligence: fair use and disclosure policy". Generative AI (LLMs; text-to-image generators) may be used in writing/editing and in figure production, subject to disclosure. Authors remain responsible for checking factual accuracy of applicable GenAI-created content, including quotes, citations, and references; checking GenAI-produced or GenAI-edited written and visual content is plagiarism-free; and checking a figure accurately reflects the data when it represents manuscript data. These quality checks are pre-submission actions rather than disclosure-rendering fields. |
| Required phrasing elements | Identify the tool's "name, version, model, and source" for AI-produced or AI-edited content. Prompts and outputs are encouraged as supplementary files. |
| Preferred disclosure location | **Acknowledgments** (AI-generated main text); AI-produced or AI-edited written or visual content → Acknowledgments AND **Methods** if applicable. |
| Prohibited uses | Listing generative AI as author or co-author. Editors/reviewers uploading manuscript content to external generative AI tools. |
| Authorship rule | "Authors should not list a generative AI technology as a co-author or author of any submitted manuscript." |
| Notes | Explicitly permits GenAI-assisted figure production subject to verification and disclosure — broader than most medical venues in this database. The factual-accuracy, plagiarism-free, and conditionally applicable accuracy-to-data checks are carried as a labelled Phase-5 pre-submission checklist. An unknown or false check remains outstanding and must not be rendered as confirmed; it is not a disclosure `UNKNOWN` halt or a categorical prohibition. |

---

## Venue: ICLR (International Conference on Learning Representations)

| Field | Value |
|---|---|
| Source URL | https://iclr.cc/public/AuthorGuide |
| Access date | 2026-04-09 |
| Policy summary | Authors may use LLMs and AI assistants for writing and code. Authors must disclose AI use and are fully responsible for all content. AI cannot be listed as an author. |
| Required phrasing elements | Must state specific tool(s) used and specific tasks assisted. Must include "the authors take full responsibility for the content." |
| Preferred disclosure location | Paper body — a dedicated paragraph in the paper, typically at the end of the Introduction or in Acknowledgements |
| Prohibited uses | None explicitly prohibited, but fabricated citations or results would violate general scientific integrity policies |
| Authorship rule | AI tools cannot be listed as authors |

---

## Venue: ICMJE (International Committee of Medical Journal Editors — umbrella recommendations)

| Field | Value |
|---|---|
| Source URL | https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html (§II.A.4); https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html (Section V.A) |
| Access date | 2026-08-01 |
| Policy summary | ICMJE Recommendations §II.A.4 "Artificial Intelligence (AI)-Assisted Technology" plus the standalone chapter Section V "Use of Artificial Intelligence in Publishing" (V.A Use of AI by Authors; V.B Use of AI by Reviewers; V.C Editors' Role in Ensuring Responsible Use of AI) — the umbrella policy layer used alongside the instructions of participating journals, including NEJM, The Lancet, JAMA, and BMJ. Authors should disclose AI-assisted technology use at submission; AI cannot be an author or be cited as an author; humans remain responsible for all submitted material. Section V.A advises authors to carefully review and edit AI-generated content and requires appropriate attribution and full citations for quoted material; "Referencing AI-generated material as the primary source is not acceptable"; nondisclosure of AI use "may require corrective action and may be construed as misconduct in some circumstances". |
| Required phrasing elements | Disclose whether and how AI-assisted technologies were used, both in the cover letter and in the submitted work itself. |
| Preferred disclosure location | **Cover letter AND in the work**: writing assistance → **Acknowledgments**; AI use in data collection / analysis / figure generation → **Methods**. |
| Prohibited uses | Listing AI as author or co-author; citing AI as an author; referencing AI-generated material as the primary source. The recommendation that authors carefully review and edit AI output is recorded in the summary as advice, not converted here into a separate prohibited-use condition. |
| Authorship rule | "Chatbots (such as ChatGPT) should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work, and these responsibilities are required for authorship" |
| Notes | Umbrella recommendations, not a journal: the source says authors should use these recommendations **alongside** the target journal's instructions. The NEJM / The Lancet / JAMA / BMJ rows record both the ICMJE relationship and each journal's own clauses. The standalone Section V spans the full publishing workflow — AI use by authors (V.A), by peer reviewers (V.B), and the editors' role in ensuring responsible AI use (V.C); only the author-side clauses are summarized in this row. The #108 anchor track separately carries an `icmje` policy anchor (16-field matrix). |

---


## Venue: JAMA (JAMA Network)

| Field | Value |
|---|---|
| Source URL | Official: https://jamanetwork.com/journals/jama/pages/instructions-for-authors ; exact stable snapshot: https://web.archive.org/web/20260701223416/https://jamanetwork.com/journals/jama/pages/instructions-for-authors |
| Access date | 2026-08-01 (live official page verified in a browser; the cited exact official-URL snapshot is from 2026-07-01 and is not a complete capture of the current manuscript-class prohibitions) |
| Policy summary | "Instructions for Authors", AI sections ("Use of AI in Publication and Research" plus the authorship clauses). The policy is restrictive-by-default: submission and publication of AI-created content "is discouraged, unless part of formal research design or methods, and is not permitted without clear description of the content that was created" plus identification of the model or tool (name, version and extension numbers, manufacturer). Authors must review and confirm the accuracy of AI-generated content and remain accountable for it. Where AI assisted with content creation, revision, or formatting, the use must be reported in the Acknowledgment section. For any AI used in a scientific study, authors must address AI-specific rights conditions and describe the specific research use; only studies using LLMs trigger the platform/tool/version/manufacturer/date and prompt-sequence/revision details. The guidance does not apply to basic tools for checking grammar or spelling. It says AI should not be used to generate or format references and recommends standard reference managers; this is retained as guidance rather than restated as an explicit "not permitted" rule. |
| Required phrasing elements | For manuscript-preparation AI: platform/program/tool name, model or tool version **and extension number(s) when applicable**, manufacturer, date(s) of use, a description of how AI was used and on which portions of the manuscript/content, confirmation that the authors reviewed and confirmed the accuracy of generated content, and confirmation that they take responsibility for its integrity. For any scientific-study AI use, describe the specific research use. The policy separately addresses two conditional rights cases. If copyright-protected content was entered into the model/tool, **include a copy** of the copyright-holder permission/license with the submission **and separately describe** that permission/license in Methods. If AI-generated text, images, or multimedia are included in the submitted work, state the rights or permission to publish **as determined by the AI service or owner** in Methods or the relevant legend. Only for a study using an LLM: also report platform/program/tool name, version, manufacturer, date(s), prompt(s), their sequence, and any prompt revisions made in response to initial outputs. |
| Preferred disclosure location | **Acknowledgment section** (manuscript-preparation AI); **Methods** (research AI and the description of any triggered copyright-input permission/license); publication-rights information for included AI-generated content → **Methods or the relevant figure legend**, as applicable. The required permission/license copy is a separate submission-package item; the policy does not designate it as text to paste into Methods. |
| Prohibited uses | Using AI/LLMs/chatbots to draft **Opinion manuscripts, Letters to the Editor, Online Comments, A Piece of My Mind, or Poetry**; submitting AI-created content without a clear description and identification of the model/tool; submitting clinical images or clinical illustrations created or manipulated by these technologies unless they are part of a formal research design or method that is fully disclosed. |
| Authorship rule | "Nonhuman artificial intelligence, language models, machine learning, or similar technologies do not qualify for authorship." |
| Notes | JAMA is an ICMJE member journal; the ICMJE umbrella recommendations and JAMA's Instructions for Authors are simultaneously relevant sources. These AI-specific clauses are not a complete JAMA Methods/reporting checklist; current study-design, reporting-guideline, ethics, data-sharing, and other applicable rights/licensing instructions remain separately applicable. The reference sentence uses “should not” for AI/LLM/chatbot generation or formatting of references, rather than JAMA's stronger “not permitted” wording for the manuscript classes and clinical-image cases listed above. A Piece of My Mind and Poetry drafting clauses were verified on the live official page on 2026-08-01 and are absent from the cited 2026-07-01 snapshot. No later exact official-URL snapshot was available when checked, so the runtime prohibition is retained with this evidence gap stated explicitly. |

---

## Venue: Nature (Nature Publishing Group)

**Policy-source dedup pointer:** Nature's substantive AI policy text is co-cited by the #108 policy-anchor renderer (`policy_anchor_table.md` Nature section, verbatim quotes per 16 fields). Both consumers reference the canonical source pointer `shared/policy_data/nature_policy.md` so a future single-source-of-truth refactor can extract Nature's policy text without breaking either consumer's substantive content. Dedup invariant lint: `verify_nature_dedup_with_venue` in `scripts/check_policy_anchor_table.py`.

**Derivation note (#108 scope limitation):** the venue-track summary fields below (Policy summary / Required phrasing elements / Preferred disclosure location / Prohibited uses / Authorship rule) **are derived** from `shared/policy_data/nature_policy.md` but are **not auto-generated from it** — the v3.2 venue path predates the canonical source and continues to drive runtime rendering off these summary rows. If Nature's source policy drifts, **the canonical source file MUST be updated first** (per the G4 invariant) and these summary rows **MUST be reviewed and updated in the same change**. A future refactor (out of #108 scope) can replace these summary rows with an extract from the canonical source so the dedup contract is auto-enforced; until then this section is a derived view that requires manual sync.

| Field | Value |
|---|---|
| Source URL | https://www.nature.com/nature/editorial-policies/ai |
| Access date | 2026-04-09 |
| Policy summary | Authors who use AI tools — including LLMs — in the writing of a manuscript, production of images, or other elements of the research must document this use transparently in the Methods or Acknowledgements section. LLMs cannot be listed as authors. Authors are responsible for the accuracy of AI-generated content. |
| Required phrasing elements | Must name the tool and describe how it was used. Must state authors verified and take responsibility for all content. Nature encourages detailed descriptions. |
| Preferred disclosure location | **Methods section** (recommended by Nature) or Acknowledgements. Also mention in the cover letter. |
| Prohibited uses | AI-generated text or images cannot be presented as original human work without disclosure. Fabrication of references or data is prohibited under general integrity policy. |
| Authorship rule | AI tools cannot meet authorship criteria (accountability requirement) and must not be listed as authors |
| Notes | Lu et al. (2026, Nature 651:914-919) provides a worked example: their AI Scientist paper includes full disclosure in Methods and Ethics Statement, with explicit IRB-style approval for the human reviewer participation. |

---

## Venue: NEJM (The New England Journal of Medicine)

| Field | Value |
|---|---|
| Source URL | Official: https://www.nejm.org/about-nejm/editorial-policies ; exact current snapshot: https://web.archive.org/web/20260731132825/https://www.nejm.org/about-nejm/editorial-policies |
| Access date | 2026-07-31 (live official URL is bot-walled to non-browser clients; the exact official-URL snapshot above was captured and re-verified against the current page) |
| Policy summary | "Editorial Policies", section "Author Use of AI-Assisted Technologies". Authors must disclose at submission whether AI-assisted technologies were used (ICMJE-aligned). The current policy says authors **must carefully review and edit all materials produced with AI**; they must be able to assert that AI-produced text/images contain no plagiarism and must properly attribute quoted material with full citations. These are current obligations, not advice inherited from the older 2025 snapshot. |
| Required phrasing elements | Describe at submission which AI-assisted technologies were used and what the technology produced; confirm that the authors carefully reviewed and edited the AI-produced material and can assert that it contains no plagiarism; include attribution and full citations for quoted material. |
| Preferred disclosure location | At submission, in **both the cover letter and the submitted work**. |
| Prohibited uses | Listing AI as an author; plagiarism in AI-produced text or images; "Citation of AI-generated material as a primary source is not acceptable." |
| Authorship rule | "Because the authors of a manuscript are responsible for the accuracy, integrity, and originality of the work, chatbots or other AI-assisted technologies cannot be listed as authors." |
| Notes | NEJM is an ICMJE member journal. The ICMJE umbrella recommendations and NEJM's own Editorial Policies are simultaneously relevant sources; neither source states that it silently replaces the other. |

---

## Venue: NeurIPS (Conference on Neural Information Processing Systems)

| Field | Value |
|---|---|
| Source URL | https://neurips.cc/public/EthicsGuidelines |
| Access date | 2026-04-09 |
| Policy summary | Authors must disclose any use of generative AI or LLMs during manuscript preparation, including writing, coding, and data analysis. Full responsibility lies with the human authors. |
| Required phrasing elements | Must specify tool name, version if known, and specific tasks. Must state authors reviewed all AI-generated content. |
| Preferred disclosure location | Acknowledgements section or a separate "Use of AI Tools" subsection before References |
| Prohibited uses | Cannot use AI to fabricate or falsify data. Cannot list AI as author. |
| Authorship rule | AI tools cannot be listed as authors |

---

## Venue: PLOS (PLOS journals)

| Field | Value |
|---|---|
| Source URL | https://journals.plos.org/plosone/s/ethical-publishing-practice |
| Access date | 2026-08-01 |
| Policy summary | "Ethical Publishing Practice", section "Artificial Intelligence Tools and Technologies". Contributions by AI tools / LLMs to a submission must be clearly reported; authors must ensure the accuracy and validity of AI-assisted content, cite original sources, and ensure that hypotheses, interpretations, and conclusions remain the authors' own. |
| Required phrasing elements | Tool name(s), how the tool was used, how its outputs were validated, and which parts of the work were AI-affected. |
| Preferred disclosure location | A dedicated part of **Methods** (or Acknowledgements if the article type has no Methods section). |
| Prohibited uses | Using AI to fabricate or misrepresent primary research data — "The use of AI tools and technologies to fabricate or otherwise misrepresent primary research data is unacceptable." Reviewers/editors uploading submissions to generative AI platforms. Noncompliance leads to rejection, retraction, or a published notice. |
| Authorship rule | No explicit AI-authorship prohibition on this policy page as of 2026-08-01. The policy expects that articles "report the listed authors' own work and ideas" and that "Contributions by artificial intelligence (AI) tools and technologies to a study or to an article's contents must be clearly reported" — AI contributions are handled via disclosure, not authorship. |

---

## Venue: Science (AAAS)

| Field | Value |
|---|---|
| Source URL | https://www.science.org/content/page/science-journals-editorial-policies |
| Access date | 2026-04-09 |
| Policy summary | Authors must disclose any use of AI-generated text, figures, or data in the manuscript. The use of AI writing tools must be documented in the Acknowledgements section or in Materials and Methods. AI tools are not authors. |
| Required phrasing elements | Must identify the AI tool by name. Must indicate which parts of the manuscript were aided by the tool. Must affirm that authors verified the accuracy of all AI-generated content. |
| Preferred disclosure location | **Acknowledgements** (preferred) or **Materials and Methods** |
| Prohibited uses | AI-generated text submitted without disclosure violates editorial policy. Fabricated figures or data are prohibited. |
| Authorship rule | AI tools cannot be listed as authors; all listed authors must meet ICMJE criteria |

---

## Venue: The Lancet

| Field | Value |
|---|---|
| Source URL | The Lancet Information for Authors: https://www.thelancet.com/pb/assets/raw/Lancet//authors/lancet-information-for-authors.pdf ; exact official-URL snapshot of that original URL: https://web.archive.org/web/20250713081908/https://www.thelancet.com/pb/assets/raw/Lancet//authors/lancet-information-for-authors.pdf ; current Elsevier journal policy: https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals |
| Access date | 2026-08-01 (the exact Lancet PDF capture is reproducible; Elsevier's policy was live-verified) |
| Policy summary | The Lancet author-information PDF served at its current official URL identifies the journal as an ICMJE signatory; its publisher's current journal policy governs generative-AI use. For manuscript preparation, authors should disclose AI-tool use in a separate declaration; basic spelling, grammar, and punctuation checks do not require declaration, while substantive changes do. Specialist assistive technology used solely for accessibility is also outside the declaration requirement. AI used in the research process must be described in detail in Methods. Elsevier now distinguishes explanatory images, data visualizations, primary research images, research-method images, graphical abstracts, and cover art instead of applying the superseded blanket image rule. General-purpose generative-AI image tools must not create graphical abstracts; dedicated scientific illustration or other professional illustration tools are the permitted path, with the tool named in the image caption and with publication rights checked. AI-generated cover art is conditionally permitted only after prior permission from both the journal editor and publisher. Authors remain responsible for image accuracy, originality, rights, and attribution. |
| Required phrasing elements | Manuscript-preparation declaration: tool/service name, purpose/reason, extent of human oversight, confirmation that authors reviewed and edited the content as needed, and confirmation of full author responsibility. Research-process use: reproducible Methods detail. For every otherwise permitted submitted visual, verify accuracy and originality and, when based on existing artwork/graphics, record attribution and rights-holder permission. Explanatory-image use: disclose the tool, version, and how it was used in each image caption and in the general declaration. Data-visualization use: model/tool name, version, and developer/manufacturer in Methods. Research-method-image use: name, version, and developer/manufacturer when applicable. Permitted AI-assisted graphical-abstract use: name the dedicated scientific or professional illustration tool in the graphical-abstract image caption and confirm that its terms provide the necessary publication rights. AI-generated cover art: prior editor and publisher permission, permissions for any third-party material used, and appropriate content attribution. |
| Preferred disclosure location | Manuscript preparation → a separate **"Declaration of generative AI and AI-assisted technologies in the manuscript preparation process" immediately before the references**. Research-process use, AI-generated data visualizations, and permitted research-method-image use → **Methods**. Explanatory images → **each image caption AND the general declaration**. Permitted AI-assisted graphical-abstract illustration-tool use → **the graphical-abstract image caption**. Cover-art approval and rights evidence are pre-submission permission actions, not a manuscript disclosure location. |
| Prohibited uses | Listing or citing an AI tool as an author; fabricating or altering research data, results, or references; using AI to create or alter primary research images representing observed/experimental data that were not directly obtained in the research (formal AI-assisted research-design/method use remains the reproducibly disclosed exception); using general-purpose generative AI for graphical abstracts; generating images that duplicate or refer to existing copyrighted images, real people, others' identifiable products/brands, or any likeness of an individual's voice. AI use may not replace the authors' intellectual contribution. |
| Authorship rule | AI tools must not be listed as authors or co-authors, nor cited as authors; accountable human authors approve and take responsibility for the final work. |
| Notes | The superseded February-2025 `tl-info-for-authors.pdf` is deliberately not used. The reproducible Lancet author-information PDF identifies the journal's ICMJE relationship but is dated May 2019 and contains no generative-AI clause; it is not presented as the source of the current AI rules. Those rules come from Elsevier's current journal policy. The ICMJE recommendations and Lancet/Elsevier instructions are simultaneously relevant sources; neither source states that it silently overrides the other. |

---

## Adding a new venue (v2 and beyond)

To add a venue to this database:

1. Find the venue's current AI-usage policy page (not a third-party summary).
2. Copy the structured fields above.
3. Fill in each field with verbatim or closely-paraphrased policy text.
4. Record the source URL and date accessed.
5. Add the venue entry to this file in alphabetical order.
6. Add explicit selector aliases, applicability predicates, and required/conditional facts to `disclosure_mode_protocol.md`; do not rely on the policy prose to create a second implicit mapping.
7. Update the "Scope" line and the user-facing selector/count surfaces.

For venues without a published AI policy: record "No explicit AI-usage policy found as of {date}" for database maintenance, but do not add the target to the runnable selector set. Runtime behavior for unknown/no-policy targets is defined only in `disclosure_mode_protocol.md`.

**Education/QA journals** still targeted for a future revision (deferred at v2, which added medical venues instead): Higher Education, Quality in Higher Education, Studies in Higher Education, Assessment & Evaluation in Higher Education, Journal of Higher Education Policy and Management. These will require separate research as their policies are less standardized than ML/NLP venues.
