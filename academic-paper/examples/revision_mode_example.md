---
scenario: Revising a paper after receiving peer review comments
mode: revision
agents_used:
  - formatter_agent
  - citation_compliance_agent
  - peer_reviewer_agent
input: Original peer review comments (3 major + 4 minor)
output: Revision comparison table + Response to Reviewers letter
---

# Revision Mode Example: Responding to Peer Review Comments

## Scenario

The user has a completed paper titled "The Impact of Micro-Credential Certification on Employability of Vocational Education Students in Taiwan," which has received peer review comments from a journal (3 major + 4 minor). The user employs academic-paper's revision mode for systematic revision. This example demonstrates the complete workflow from comment parsing, citation correction, review verification, to the Response to Reviewers letter.

---

## Original Peer Review Comments

### Reviewer 1

**Major Comments:**

**M1.** There are serious concerns about the research methodology. The paper uses questionnaire surveys to collect students' self-assessed employability but does not employ any objective indicators (such as actual employment rates, starting salaries, or employer satisfaction) for triangulation. Relying solely on self-assessment to measure "employability" has insufficient validity. It is recommended to supplement with at least one objective indicator or explicitly discuss this methodological limitation.

**M2.** The literature review lacks systematicity. Of the 23 references cited in Chapter 2, more than half are publications from before 2018, and the review does not cover important recent international studies on micro-credentials from the past two years (2024-2025), particularly the latest reports from UNESCO (2024) and the European Commission (2024). It is recommended to supplement with literature from the past three years and update the literature matrix.

**M3.** The statistical analysis is incomplete. The regression model in Table 4 reports only R-squared and beta coefficients, lacking collinearity diagnostics (VIF), residual analysis, and effect sizes. Additionally, the rationale for selecting control variables is unclear — why was "family income" controlled but not "prior work experience"?

**Minor Comments:**

**m1.** The third sentence of the abstract — "This study found that micro-credential certification has a significant positive impact on student employability" — is too vague and does not mention the magnitude of the effect size.

**m2.** Reference formatting is inconsistent: parenthesis style varies across entries. Citation #15 is missing its DOI.

**m3.** The axis labels in Figure 2 have font sizes that are too small; it is recommended to enlarge them to 10pt or above. Figure 3 is missing a caption.

**m4.** The last paragraph on page 47 contains "as shown in Table X," which appears to be a typesetting omission.

---

### Reviewer 2

**Major Comments:**

(No additional major comments, but the reviewer agrees with Reviewer 1's M1 and M2.)

**Minor Comments:**

(Agrees with Reviewer 1's minor comments, and adds:)

**m5 (R2).** It is recommended to add a clearer research gap statement in the Introduction. The transition from problem description to research purpose is currently too abrupt.

**m6 (R2).** The "policy recommendations" paragraph in the Discussion chapter is too brief — it lists only three recommendations without supporting arguments. It is recommended to expand or downgrade this section to "future research directions."

**m7 (R2).** It is recommended to add a research ethics statement explaining the IRB review status and informed consent procedures.

---

## formatter_agent Parses Revision Comments

### Revision Comment Classification

**Parsing Result:** 3 Major + 7 Minor, totaling 10 revision items.

| No. | Type | Affected Section | Revision Scope | Estimated Workload |
|-----|------|-----------------|----------------|-------------------|
| M1 | Major | Methodology, Discussion | Methodological limitation discussion + possible data supplement | High |
| M2 | Major | Literature Review | Supplement literature + update literature matrix | Medium-High |
| M3 | Major | Results | Add statistical diagnostics + effect sizes | Medium |
| m1 | Minor | Abstract | Revise abstract wording | Low |
| m2 | Minor | References | Unify formatting + add DOI | Low |
| m3 | Minor | Figures | Fix figures and tables | Low |
| m4 | Minor | Body text | Fix typesetting | Low |
| m5 | Minor | Introduction | Add research gap statement | Low-Medium |
| m6 | Minor | Discussion | Expand policy recommendations discussion | Medium |
| m7 | Minor | Methodology | Add ethics statement | Low |

### Recommended Revision Strategy

The formatter_agent recommends the following revision order:

1. Address M1 (methodology) first, as it affects the revision direction of Discussion and Limitations
2. Then address M3 (statistical analysis), as the supplementary statistical results may affect the limitation discussion in M1
3. Then address M2 (literature review), as supplemented literature may require cascading updates to the Discussion
4. Finally, batch-process all minor comments

---

## citation_compliance_agent Corrects Citation Issues

### Citation Audit Report

**Audit Scope:** Full-text citation formatting (APA 7.0)

**Issues Found:**

| Issue | Count | Severity |
|-------|-------|----------|
| Inconsistent parenthesis format (full-width/half-width) | 7 instances | Medium |
| Missing DOI | 3 instances | High |
| Inconsistent year format | 2 instances | Low |
| In-text citation / reference list mismatch | 1 instance | High |

### Specific Corrections

**Correction 1: Unify parenthesis format (addressing m2)**

Before correction:
```
(Wang & Chen, 2023) noted in their study...
Lin, M.-D. (2022)'s survey showed...
According to UNESCO (2024) report...
```

After correction:
```
Wang and Chen (2023) noted in their study...
Lin (2022)'s survey showed...
According to the UNESCO (2024) report...
```


**Correction 2: Add missing DOIs (addressing m2)**

Before correction:
```
Huang, C.-W. (2021). Implications of micro-credit systems for technical and vocational
    education. Journal of Technical and Vocational Education, 15(2), 45-68.
```

After correction:
```
Huang, C.-W. (2021). Implications of micro-credit systems for technical and vocational
    education. Journal of Technical and Vocational Education, 15(2), 45-68.
    https://doi.org/10.6235/TVE.202106_15(2).0003
```

**Correction 3: In-text citation / reference list mismatch**

Found that the in-text citation on page 23 reads "Chen et al.2023" but the reference list entry is "Chen, Y.-L., & Wang, S.-T.2023" which has only two authors and should not use "et al."

Before correction:
```
Chen et al.2023found that micro-credential certification helps...
```

After correction:
```
Chen and Wang2023found that micro-credential certification helps...
```

