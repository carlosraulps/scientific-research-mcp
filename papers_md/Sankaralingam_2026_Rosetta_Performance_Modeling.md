| Rosetta:             |           |            | Automating   |            |             |               | First-Principles |             |        |     | Performance |     |     |     |
| -------------------- | --------- | ---------- | ------------ | ---------- | ----------- | ------------- | ---------------- | ----------- | ------ | --- | ----------- | --- | --- | --- |
|                      |           | Modeling   |              |            |             | Using         |                  | Multi-Agent |        |     | LLMs        |     |     |     |
|                      |           |            |              |            | Karthikeyan |               | Sankaralingam,   |             | NVIDIA |     |             |     |     |     |
| Abstract—Analytical  |           |            | performance  |            | models      | — derivations |                  | of          |        |     |             |     |     |     |
| throughput           | or        | speedup    | from         | hardware   | parameters  |               | — make           |             |        |     |             |     |     |     |
| claims independently |           | verifiable |              | and expose | binding     |               | constraints,     |             |        |     |             |     |     |     |
| yet rarely           | accompany |            | architecture | papers     | because     |               | building one     |             |        |     |             |     |     |     |
byhandtakesweeksofexperteffort.WepresentRosetta,amulti-
| agent LLM  | pipeline | that | automatically |       | generates | first-principles |         |     |     |     |     |     |     |     |
| ---------- | -------- | ---- | ------------- | ----- | --------- | ---------------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| analytical | models   | from | research      | paper | PDFs.     | Given            | a paper | as  |     |     |     |     |     |     |
6202 peS 61  ]FP.sc[  1v67391.9062:viXra
| sole input,       | Rosetta | produces   |             | a mathematical  |               | specification, | an          |     |     |     |     |     |     |     |
| ----------------- | ------- | ---------- | ----------- | --------------- | ------------- | -------------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| executable        | Python  | model,     | and         | a plain-English |               | interpretation | —           |     |     |     |     |     |     |     |
| all autonomously, |         | with       | zero        | human           | intervention. |                | The formal- |     |     |     |     |     |     |     |
| ization process   |         | itself is  | the primary |                 | value:        | it surfaces    | implicit    |     |     |     |     |     |     |     |
| assumptions       | and     | identifies | missing     |                 | parameters.   |                | Four design |     |     |     |     |     |     |     |
decisionsaddressfailuremodesofnaïveLLM-basedgeneration:
| a scientific | constitution |             | that prohibits |        | circular       | reasoning, | verify-      |     |     |     |     |     |     |     |
| ------------ | ------------ | ----------- | -------------- | ------ | -------------- | ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
| repair loops | with         | independent |                | critic | agents,        | dual       | verification |     |     |     |     |     |     |     |
| separating   | functional   | correctness |                | from   | scientific     | validity,  | and          | a   |     |     |     |     |     |     |
| best-of-N    | ensemble     | that        | exploits       | LLM    | stochasticity. |            |              |     |     |     |     |     |     |     |
We evaluate Rosetta across three complementary tracks: Fig. 1: Rosetta and Paper Overview
| expert evaluation |     | of  | 12 landmark |     | papers | (CS1), | automated |     |     |     |     |     |     |     |
| ----------------- | --- | --- | ----------- | --- | ------ | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
scoring of 97 unfiltered ISCA 2025 and HPCA 2026 papers the value of analytical models but overwhelmingly relies on
(CS2), and author self-evaluation by six active research groups simulation or measurement results instead.
| (CS3). Across | CS1,   | specification |                 | quality   | scores   | 4–5/5      | on 10 of 12 |      |           |                  |               |             |       |            |
| ------------- | ------ | ------------- | --------------- | --------- | -------- | ---------- | ----------- | ---- | --------- | ---------------- | ------------- | ----------- | ----- | ---------- |
|               |        |               |                 |           |          |            |             | We   | present   | Rosetta,         | a closed-loop | multi-agent |       | pipeline   |
| papers with   | zero   | significant   | hallucinations; |           | across   | CS2,       | 56%         | of   |           |                  |               |             |       |            |
|               |        |               |                 |           |          |            |             | that | automates | first-principles |               | analytical  | model | generation |
| fit-screened  | papers | reach         | Tier            | A insight | quality. | The        | strongest   |      |           |                  |               |             |       |            |
|               |        |               |                 |           |          |            |             | from | research  | paper PDFs       | (Figure       | 1). Given   | a PDF | as its     |
| finding comes | from   | CS3:          | Rosetta’s       | output    | led      | to revised | claims      |      |           |                  |               |             |       |            |
andnewexperimentsinactivesubmissions,andfiveofsixauthor- sole input, Rosetta produces three artifacts: (i) SPEC.md, a
evaluators said they would use it again. mathematical specification of hardware parameters and cost
functions;(ii)model.py,aself-containedexecutablePython
I. INTRODUCTION model; and (iii) INTERPRETATION.md, a plain-English
|     |     |     |     |     |     |     |     | explanation |     | of the model’s | insights. | A central | concept | is to |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------------- | --------- | --------- | ------- | ----- |
An analytical performance model — a closed-form or quantify any discrepancy between what the paper’s described
small-program derivation that predicts a system’s throughput, mechanism can achieve from first principles and its reported
| latency, | energy, | or speedup |     | from | hardware | parameters | and |          |              |        |          |              |         |     |
| -------- | ------- | ---------- | --- | ---- | -------- | ---------- | --- | -------- | ------------ | ------ | -------- | ------------ | ------- | --- |
|          |         |            |     |      |          |            |     | results, | highlighting | either | unstated | assumptions, | omitted | op- |
workload characteristics — is one of the most useful artifacts timizations, or conservative claims. Just as code and data
a computer architecture paper can provide. It makes trans- releases became standard practice, Rosetta-generated artifacts
parent questions that cycle-level simulators can also address can make performance claims independently verifiable by any
but require significant instrumentation and infrastructure to reader,withoutaccesstotheauthors’simulationinfrastructure.
| answer: | why performance |     | bounds | exist, | which | parameters | are |     |     |     |     |     |     |     |
| ------- | --------------- | --- | ------ | ------ | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
WeevaluateRosettainfullyautonomousmodeonpublished
the binding constraints, and how results would change under research papers—a deliberate stress test. A common miscon-
different conditions. Such models are invaluable across the ception is that a camera-ready PDF is a perfectly precise and
research lifecycle. They serve readers by verifying claims in- completeartifact,renderingautomatedmodelingredundant.In
dependently,helpauthorsdebugdesignsalongsidesimulation, reality, published papers are highly compressed and routinely
| provide | self-contained |     | reproducible |     | artifacts, | allow | industry |     |     |     |     |     |     |     |
| ------- | -------------- | --- | ------------ | --- | ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
elideimplicitassumptionsorobscurehardwareparameters.By
practitioners to share architectural insights without exposing succeeding on these sparse documents, we establish a lower
proprietary simulation infrastructure or IP (e.g., Anton [69], a bound on Rosetta’s utility. If it can derive an independent,
molecular dynamics ASIC evaluated in our case-study), and verifiable artifact from a compressed PDF to serve readers
serve as artifacts that guide follow-on work. and reviewers, it is even more capable when applied to
Despitethisvalue,rigorousanalyticalmodelsrarelyaccom- the ongoing, parameter-rich drafts of active researchers (as
panyarchitecturepapers.Buildingonebyhandrequiresweeks demonstratedinCaseStudy3)orthehighlydetailedtechnical
ofskilledeffort,mathematicalfluency,workloadandhardware specificationsusedinindustry.Morebroadly,thecorequestion
intuition. Consequently, the research community recognizes Rosetta answers for any technical document is: did I build
1

what I think I built, and are the benefits and limitations formalization output directly caused changes to the paper:
what I claimed they were? Automating this process raises a simulation methodology comparison in one case, and a
four challenges: LLMs defaulting to circular reasoning (using sharpened separation of GPU and custom-accelerator con-
reportedresultsasinputsratherthancalibratingagainstthem), tributions in the other.
low-quality single-shot specifications, code that faithfully im- • Human evaluators confirm correctness and insight.
plements scientifically invalid specs, and LLM stochasticity. Across 12 CS1 papers, independent domain-competent re-
Rosetta addresses these via a scientific constitution (the searchers scored specification quality at 4–5/5 on 10 of 12
PRIME DIRECTIVE) enforcing first-principles derivation, papers with zero significant hallucinations, and rated 11 of
a verify-repair loop with independent critic agents, dual 12papersat4/5or5/5overallusefulness.Noevaluatorsaid
verification separating functional correctness from scientific “No” to future use.
validity, and a best-of-N ensemble to ensure output quality Rosetta generalizes at scale. In CS2, 60% of 97 unfiltered
•
and insight. conference papers score in Tier A (9–10/10) on the auto-
RecentworkhasbeguntoargueforGenAI-assisteddiscov- mated selector’s insight quality metric, and 86% score 7/10
| ery in architecture |     | more broadly |     | [24], [68]; | Rosetta | addresses |     | or above. |     |     |     |     |     |     |
| ------------------- | --- | ------------ | --- | ----------- | ------- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
onespecific,thusfarunresolvedtoolprobleminthatemerging • Researcherswanttouseitagain—anditchangedtheir
space. papers. Five of six CS3 evaluators said “Definitely” for
|     |     |     |     |     |     |     |     | future | use; four | had | concrete | paper impact | (revised | claims, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --------- | --- | -------- | ------------ | -------- | ------- |
Contributions
|     |     |     |     |     |     |     |     | new experiments, |     | sharpened |     | exposition). | The adoption | sig- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --------- | --- | ------------ | ------------ | ---- |
Rosetta: an end-to-end multi-agent pipeline that produces nal is not about numerical accuracy: as one evaluator put
•
first-principlesanalyticalperformancemodelsfromresearch it, “No reviewer would have the time to write a simulation
paper PDFs, with a median end-to-end wall-clock time of to validate a paper’s empirical results, but with Rosetta it’s
72 minutes, reducible to ∼25 minutes by running ensemble a 5-minute task.” Another noted it “may have helped us
instances in parallel. It is released open-source with this earlierforideadevelopmentandeliminatinglesspromising
| paper, including |     | all code, | prompts, | and | evaluation | artifacts, |     | ideas.” |     |     |     |     |     |     |
| ---------------- | --- | --------- | -------- | --- | ---------- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- |
with Anthropic API implementation. Paper organization. Section II provides Rosetta’s problem
• The PRIME DIRECTIVE: a shared scientific constitution definition and design goals. Section III describes the system
| enforcing | first-principles |     | derivation, | calibration-as-overlay, |     |     |     |                   |     |           |     |              |             |          |
| --------- | ---------------- | --- | ----------- | ----------------------- | --- | --- | --- | ----------------- | --- | --------- | --- | ------------ | ----------- | -------- |
|           |                  |     |             |                         |     |     |     | design, including |     | empirical |     | evidence for | each design | decision |
self-containment, and baseline vs. proposed comparison (Section III-G). Section IV frames the evaluation method-
| across all | agents. | We show | empirically |     | that removing |     | the |                 |     |       |         |           |      |               |
| ---------- | ------- | ------- | ----------- | --- | ------------- | --- | --- | --------------- | --- | ----- | ------- | --------- | ---- | ------------- |
|            |         |         |             |     |               |     |     | ology. Sections |     | V–VII | present | the three | case | study tracks. |
constitution degrades model quality substantially. Section VIII surveys related work. Section IX concludes.
| • A verify-repair |     | architecture |     | with dual | verification: |     | in- |     |     |     |     |     |     |     |
| ----------------- | --- | ------------ | --- | --------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
dependently separating functional correctness (spec-to-code II. THEPROBLEMFORMULATION
fidelity) from scientific validity (constitution compliance), Thestandardartifactofarchitectureevaluationisasimulator
closing a failure mode where a faithful implementation of or measurement harness — a tool that produces performance
a bad spec passes single-verifier review. numbers but embeds its assumptions in code rather than
• Evaluationacrossthreecasestudy(CS)tracks:CS1eval- exposing them mathematically. When a paper’s performance
uates12landmarkarchitecturepapersagainstdomain-expert claims rest on such tools, independent verification requires
rubrics;CS2appliesRosettainbreadthto97ISCA2025and accesstothefullinfrastructure.Rosetta’staskistoproducethe
HPCA 2026 papers without expert evaluation; CS3 gives complementary artifact: a mathematical specification and ex-
Rosettato6researchersandcollectsauthorself-evaluations. ecutable model derived solely from the paper’s prose, against
• CAAM-Bench: the first benchmark for evaluating ana- which the paper’s claims can be independently checked. We
lytical model generators on architecture papers — 12 define this task as follows.
| landmark          | papers   | with       | human-vetted |           | reference | artifacts |        |                    |               |               |            |                |          |              |
| ----------------- | -------- | ---------- | ------------ | --------- | --------- | --------- | ------ | ------------------ | ------------- | ------------- | ---------- | -------------- | -------- | ------------ |
|                   |          |            |              |           |           |           |        | Definition         | 1 (Analytical |               | Model      | Generation).   |          | Given a re-  |
| (SPECIFICATION.md |          |            | and          | model.py) |           | and a     | four-  |                    |               |               |            |                |          |              |
|                   |          |            |              |           |           |           |        | search             | paper         | PDF P         | describing | a              | computer | architecture |
| dimension         | scoring  | rubric.    | Rosetta’s    | CS1       | scores    | serve     | as the |                    |               |               |            |                |          |              |
|                   |          |            |              |           |           |           |        | or systems         | contribution  |               | with       | performance    | claims,  | produce:     |
| published         | baseline | for future | tools.       |           |           |           |        |                    |               |               |            |                |          |              |
|                   |          |            |              |           |           |           |        | (i) a mathematical |               | specification |            | S defining     | the      | hardware     |
|                   |          |            |              |           |           |           |        | parameters,        | workload      |               | model,     | and analytical | cost     | functions    |
Key Findings
|                     |                  |           |             |          |           |             |        | for both       | the baseline |           | and   | proposed          | systems, derived | from         |
| ------------------- | ---------------- | --------- | ----------- | -------- | --------- | ----------- | ------ | -------------- | ------------ | --------- | ----- | ----------------- | ---------------- | ------------ |
| • The formalization |                  | itself    | is the      | primary  | value.    | Every       | CS3    |                |              |           |       |                   |                  |              |
|                     |                  |           |             |          |           |             |        | the paper’s    | prose        | without   | using | reported          | results          | as inputs;   |
| author named        | SPECIFICATION.md |           |             |          | — not     | the quanti- |        |                |              |           |       |                   |                  |              |
|                     |                  |           |             |          |           |             |        | (ii) an        | executable   | model     | M     | implementing      | S;               | and (iii) an |
| tative model        | —                | as the    | most        | valuable | output.   | The act     | of     |                |              |           |       |                   |                  |              |
|                     |                  |           |             |          |           |             |        | interpretation | I            | reporting | the   | model’s findings, | including        | any          |
| reverse-engineering |                  | a paper’s | performance |          | structure |             | into a |                |              |           |       |                   |                  |              |
quantifieddiscrepancybetweenM’sfirst-principlesprediction
| mathematical | specification |     | surfaces | implicit |     | assumptions, |     |         |         |          |          |     |     |     |
| ------------ | ------------- | --- | -------- | -------- | --- | ------------ | --- | ------- | ------- | -------- | -------- | --- | --- | --- |
|              |               |     |          |          |     |              |     | and the | paper’s | reported | results. |     |     |     |
flagsmissingparameters,andproducesareadableanalytical
skeleton—valuethatisdecoupledfromwhetherthemodel The key constraint is first-principles derivation: M must
achieves numerical accuracy. In two CS3 cases, Rosetta’s compute performance from physical parameters (S), not from
2

|                 |                     |                  |                  | A. Phase                  | 1: Specification |            | (Text       | →                 | Math)         |            |               |        |
| --------------- | ------------------- | ---------------- | ---------------- | ------------------------- | ---------------- | ---------- | ----------- | ----------------- | ------------- | ---------- | ------------- | ------ |
|                 |                     |                  |                  | The goal                  | of               | Phase      | 1 is to     | reverse-engineer  |               | a rigorous |               | math-  |
|                 |                     |                  |                  | ematical                  | specification    |            | from        | the paper’s       | prose         | —          | the “physics” |        |
|                 |                     |                  |                  | of the described          |                  | system     | expressed   |                   | as concrete   |            | variables,    | cost   |
|                 |                     |                  |                  | functions,                | and              | workload   | models.     |                   |               |            |               |        |
|                 |                     |                  |                  | Generation                | (Prof.           | Aximo).    |             | The specification |               | generator, |               | char-  |
|                 |                     |                  |                  | acterized                 | as               | a rigorous | expert      |                   | in analytical |            | performance   |        |
|                 |                     |                  |                  | modeling                  | who              | “only      | trusts      | variables,        | equations,    |            | and           | con-   |
|                 |                     |                  |                  | crete data                | points,”         | reads      | the         | full              | paper text    | and        | produces      | a      |
|                 |                     |                  |                  | structured                | document         |            | containing: | (i)               | all hardware  |            | parameters    |        |
|                 |                     |                  |                  | with Python-compatible    |                  |            | names       | and               | suggested     |            | value         | ranges |
|                 |                     |                  |                  | (e.g., dram_bandwidth_gbs |                  |            |             | =                 | 51.2);        | (ii)       | a workload    |        |
| Fig. 2: Rosetta | pipeline.           | Three sequential | phases transform | a                         |                  |            |             |                   |               |            |               |        |
|                 |                     |                  |                  | model specifying          |                  | the        | synthetic   | input             | distribution  |            | the           | model  |
| paper PDF       | into a mathematical | spec, executable | model, and       |                           |                  |            |             |                   |               |            |               |        |
|                 |                     |                  |                  | will use;                 | (iii)            | analytical | cost        | functions         | for           | both       | the baseline  |        |
interpretation. Phases 1 and 2 run verify-repair loops of up to and proposed systems, derived bottom-up from hardware
| three iterations. | The full      | pipeline runs N=3 | times; a selector |               |            |                 |      |            |            |         |           |         |
| ----------------- | ------------- | ----------------- | ----------------- | ------------- | ---------- | --------------- | ---- | ---------- | ---------- | ------- | --------- | ------- |
|                   |               |                   |                   | constraints;  | (iv)       | calibration     |      | targets    | — concrete |         | data      | points  |
| agent picks       | the best run. |                   |                   |               |            |                 |      |            |            |         |           |         |
|                   |               |                   |                   | extracted     | from       | the paper’s     |      | figures    | and        | tables, | formatted | as      |
|                   |               |                   |                   | (input_state, |            | claimed_output, |      |            |            | source) |           | tuples; |
|                   |               |                   |                   | and (v)       | an initial | “magic          | gap” | hypothesis |            | noting  | any       | visible |
thepaper’sreportedresults.Thepaper’sresultsappearinM’s discrepancy between what the mechanism implies and what
outputascalibrationscatterpoints—avisualrepresentationof
|     |     |     |     | the paper | reports. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- |
whether the first-principles prediction and the reported result Verification(Dr.Logic).Anindependentverifier—a“pedan-
agree.Whentheydisagreesignificantly,thediscrepancyisthe tic senior technical reviewer” — audits the specification
magic gap. This formulation reflects Box’s principle that “all against the original paper and the shared constitution (Sec-
models are wrong, but some are useful” [8]: the goal is not tion III-D). It checks for missing variables, hallucinated
numericalprecisionbutmechanisticunderstandingthatmakes
|     |     |     |     | formulas, | absent | calibration |     | data, | and | — most | critically |     |
| --- | --- | --- | --- | --------- | ------ | ----------- | --- | ----- | --- | ------ | ---------- | --- |
the paper’s performance claims independently auditable. — circular reasoning: using the paper’s own reported re-
This formulation has a natural failure mode: if the paper sults as formula inputs rather than as calibration overlays.
does not expose the hardware parameters needed to derive The agent responds with exactly APPROVED: <reason>
performance from first principles, M cannot be fully derived. or REVISION NEEDED: <detailed critique>. The
Itcanstillproducebounds,calibration-modeestimateslabeled complete critique is saved to disk regardless of outcome,
as such, and a diagnostic listing of which parameters are creating an audit trail.
missing. This is the correct behavior when the paper’s study Repair loop and audit trail. If the spec is rejected, the
reports measured speedups without exposing the underlying generator agent is re-invoked in “Correction Mode” with the
hardware configuration. original paper, the rejected spec, and Dr. Logic’s critique.
|     |     |     |     | The loop       | runs | for up   | to three | iterations; |         | in practice, |              | most |
| --- | --- | --- | --- | -------------- | ---- | -------- | -------- | ----------- | ------- | ------------ | ------------ | ---- |
|     |     |     |     | specifications |      | converge | within   | one         | or two. | Every        | intermediate |      |
III. SYSTEMDESIGN artifact is saved (draft specs, draft models, all critique files),
providingfulltransparency:aresearchercantraceexactlyhow
| Rosetta | is a closed-loop | pipeline that transforms | a research |                 |     |     |          |     |             |     |                |     |
| ------- | ---------------- | ------------------------ | ---------- | --------------- | --- | --- | -------- | --- | ----------- | --- | -------------- | --- |
|         |                  |                          |            | each conclusion |     | was | reached, | and | a diagnosis |     | tool evaluates |     |
paper PDF into three artifacts: a mathematical specifica- whether each iteration made genuine progress.
| tion (SPECIFICATION.md), |             | an executable       | Python perfor- |          |                   |     |     |       |           |     |     |     |
| ------------------------ | ----------- | ------------------- | -------------- | -------- | ----------------- | --- | --- | ----- | --------- | --- | --- | --- |
|                          |             |                     |                | B. Phase | 2: Implementation |     |     | (Math | → Python) |     |     |     |
| mance model              | (model.py), | and a plain-English | interpreta-    |          |                   |     |     |       |           |     |     |     |
tion (INTERPRETATION.md). Figure 2 shows the overall Phase 2 translates the approved specification into a self-
architecture. The pipeline is organized into three sequential contained, executable Python performance model.
phases, each driven by one or more large language model Implementation (Vector). The implementer agent — a “bril-
(LLM) agents operating under a shared scientific constitu- liantPythondatascientistandsimulationengineer”—receives
tion. To mitigate LLM stochasticity, the entire pipeline runs both the approved specification and the original paper text
multiple times and a selector agent chooses the best output and produces a Python script with a fixed structure: (i) a
(Section III-E). The complete system — including all agent Config dataclass holding all parameters from the spec;
prompts,thePRIMEDIRECTIVEconstitution,andevaluation (ii) cost_baseline() and cost_proposed() func-
artifacts — is released as open-source with this paper; the tions implementing the spec’s cost formulas exactly; (iii) a
prompts are the primary design artifact and are integral to simulation loop sweeping over the parameter ranges defined
reproducibility.Aconciseusageguideaccompaniestherelease in the spec; and (iv) a matplotlib visualization with a
to help users interpret outputs without reading this paper or dashed blue baseline curve, a solid green proposed curve, and
becoming LLM experts. red X scatter markers for the paper’s claimed results, saved as
3

evaluation_plot.png (never plt.show(), since the Forbidden (circular): per_vcu = paper_reported_20vcu
pipelinerunsheadless).Generatedcodeissyntax-validatedvia / 20; throughput_8vcu = per_vcu * 8
Python’s ast.parse() before saving. Required (first principles):
Dual verification. Phase 2 uses two independent verifiers mpix_per_core = pixels * fps / 1e6 (from Section
because code quality has two orthogonal failure modes. The 3.1)
compute_bound = mpix_per_core * cores_per_vcu
QA Engineer performs a line-by-line functional audit: do
theoretical_max = min(compute_bound,
variable names match the spec, are formulas implemented
memory_bound)
correctly, will numpy broadcasting work? The PI (Principal efficiency = paper_claimed / theoretical_max
Investigator) performs a scientific validity audit: is there a (15% gap!)
baseline vs. proposed comparison, are calibration overlays
Fig. 3: The PRIME DIRECTIVE’s first-principles law illus-
present,isthecodeself-contained,and—mostimportantly—
trated. The forbidden pattern validates paper results against
is performance derived from physical constraints rather than
scaled versions of themselves — no independent derivation.
from table data? The PI’s test is concrete: “If you removed
Therequiredpatternderivesperformancefromhardwarespecs
all Table/Figure data from the code, would it still calculate
and then compares the result to the paper’s reported value.
performance?Ifnot,itisviolatingfirstprinciples.”Bothagents
must return APPROVED for the loop to exit; either rejection
triggers a repair.
and plot them as scatter markers on top of the theoretical
Repair loop. The implementer agent, in “Debug Mode,”
curves. If a claimed data point sits above the theoretical
receives both the QA Engineer’s and PI’s critiques simulta-
curve, the paper is asserting performance that its described
neously and rewrites the model from scratch addressing all
mechanism cannot support — this is the “magic gap.”
issues. The loop again runs for up to three iterations, saving
3) Self-Containment. The final model.py must run as
all draft versions and critique files as an audit trail.
python model.pywithnoarguments,noexternalfiles,
C. Phase 3: Interpretation (Python → Insight) andnonetworkaccess.Itgeneratesitsownsyntheticwork-
load data from distributions defined in the specification.
The final phase is a single-shot generation by a Technical
4) Baseline vs. Proposed. Every analysis must model both
Communicatoragent.ItreadsthefinalSPECIFICATION.md
the status quo and the new contribution side-by-side. A
and model.py and produces a plain-English document cov-
proposedsystemanalyzedinisolation—withoutabaseline
ering: the workload the model assumes; how the baseline is
— is scientifically meaningless.
modeled and what it implies; the proposed mechanism and
what changes; the critical variables and threshold conditions The constitution is the mechanism by which Rosetta en-
where the proposed system wins or loses; and any gaps forcesscientificrigoracrossheterogeneousagents.Withoutit,
betweenthetheoreticalcurvesandthepaper’sclaimedresults. agents routinely produce plausible-looking but methodologi-
The tone guidance is “insightful and explanatory — explain cally invalid models — a finding confirmed by ablation.
model semantics, not Python syntax.” This phase has no
E. The Best-of-N Ensemble
verify-repair loop: interpretation quality improves less from
iteration than specification or code correctness. LLM outputs are stochastic: the same pipeline on the same
paper produces different specifications, models, and interpre-
D. The Scientific Constitution
tations across runs. Some runs surface sharp insights; others
Every agent in the pipeline receives a shared document — miss key bottlenecks or make incorrect assumptions. Drawing
the PRIME DIRECTIVE — prepended to its role-specific on recent findings in LLM self-consistency and Best-of-N
prompt before any LLM call. This constitution defines four reasoning [9], [15], Rosetta runs the full three-phase pipeline
immutable laws that govern all agents: N=3 times on each paper and uses a selector agent to choose
1) First-Principles Derivation. Models must derive perfor- the best run.
mance from physical and architectural constraints, never Theselectorexecutespython model.pyforeachrunto
by scaling or fitting reported numbers. The distinction is confirm it runs without errors, then evaluates three criteria in
illustrated with explicit code examples (Figure 3). The priority order: Correctness (primary; a model that crashes or
forbidden pattern takes a paper’s reported throughput and is trivially wrong is disqualified regardless of other merits),
divides by the number of units to get per-unit through- Insight Quality (primary differentiator; does the run identify
put, then multiplies back — validating the paper’s claims concrete bottlenecks, quantify magic gaps, and go beyond
against scaled versions of the same claims. The required restating the paper?), and Completeness (secondary; are all
patternderivesthroughputfromhardwareparameters(core subsystems modeled, are calibration targets included?). The
count, frequency, memory bandwidth), then compares the selector produces a per-run evaluation report and a final
result to the paper’s reported values as an independent recommendation with explicit justification.
check. Ensemble quality in practice. Across our case study papers,
2) Calibration (The Truth Overlay). Agents must extract the three ensemble runs diverged meaningfully — not merely
specificdatapointsfromthepaper’sfigures,tables,andtext as minor numerical variations, but in modeling philosophy
4

TABLE I: Rosetta agent inventory. All agents receive the
and interpretation quality. Consider two failure modes we
PRIME DIRECTIVE prepended to their role-specific prompt.
observed. In one run on the Anton paper, the model predicted
performance 5–6× higher than the paper claimed, yet the
Agent Phase Role
interpretation document declared this a validation success
Prof. Aximo 1 Spec generator
— a failure of critical thinking that the selector identified
Dr. Logic 1 Spec verifier
and rejected. In another run on the CraterLake paper, a bug
Prof. Aximo (CM) 1 Spec repair
in the baseline formulation made the proposed-vs-baseline Vector 2 Model implementer
comparison meaningless, despite the individual cost functions QA Engineer 2 Functional verifier
being correct. PI 2 Directive verifier
Vector (DM) 2 Model repair
The selector’s primary differentiator — insight quality —
Tech. Communicator 3 Interpretation
consistently surfaces the run that treats unexplained gaps as
signals to flag rather than problems to rationalize away. In
the Darwin analysis, only one of three runs correctly noted
a 1.5× budget multiplier per attempt (16,384 → 24,576 →
thattheheadline“15,000×speedup”appliesonlytoONT_2D
36,864 → 55,296, capped at 64,000), accommodating long
readsanddropsto1,244×forONT_1Dreadsduetoerror-rate
papers and complex derivations without permanently inflating
cascade — a nuance buried in the paper’s details.
the budget.
Notably, there is no consistent bias toward which run
G. Why Naive Design Fails
number wins: across our papers, runs 1, 2, and 3 each won
in roughly equal proportion. This confirms that the ensemble Each design decision in the pipeline addresses a specific,
is not redundant — each run is a genuinely independent empirically observed failure mode. The examples below are
draw from the model’s hypothesis space. The ensemble also from Case Study 1. To prevent evaluation bias, the papers
provides containment when the verify-repair loop does not usedduringRosetta’sinitialdevelopment(Cambricon-SR[50]
fully converge: in one case study, a flaw in the F1+ baseline and F1 [65]) were strictly excluded from our case studies;
model survived three spec critique rounds and was faithfully instead,theyservedastheformativetestbedsthatrevealedthe
propagated into the model by the functional verifier — which failure modes described below and helped develop and refine
checks code-to-spec fidelity, not spec-to-physics correctness. Rosetta’s current design.
The selector identified the affected run and chose an alternate Constitution and spec verification. Without the PRIME
with a sound baseline derivation. DIRECTIVE, LLMs default to circular reasoning: an un-
guided CraterLake run back-calculated efficiency from the
F. Agent Inventory and Implementation
paper’s claimed 11.2× speedup and predicted an impossible
Table I summarizes the eight agents in the system. The 465×. Careful prompting alone is insufficient; the constitu-
pipeline is implemented as a fully automated Python program tion provides concrete code-level anti-patterns that all agents
that orchestrates LLM API calls, parses structured outputs, enforce. Even with the constitution, spec-level errors can
manages file I/O, and executes generated code — no interac- survivegenerationandpropagatefaithfullyintocode.Aflawed
tive chat interface is involved. Six of the eight agents come CraterLake spec assigned CraterLake-specific hardware (the
in generator/verifier or generator/repair pairs — a deliberate CRB unit) to the F1+ baseline, which does not have one;
separation of concerns where no agent ever evaluates its own the resulting model.py passed code verification because it
work. All agents run at temperature 0.5; the ensemble selects perfectlymatcheditsbuggyspec.Adedicatedspecverification
the best output across three full pipeline runs (Section III-E). loop that reads against the original paper — before any code
Ensemblerunsareexecutedsequentiallyratherthaninparallel is written — is the only mechanism that catches this class of
tosimplifydebuggingandresourcemanagement;totalruntime error.
remains practical. Dual verification and ensemble. Functional correctness and
Modelchoice.AllexperimentswererunwithClaudeOpus4.5 scientific validity are orthogonal. In one Anton run, the code
(training data cutoff May 2025). In our experiments, Gemini- passed functional verification because it matched its spec,
2.5, Gemini-3, and ChatGPT series models provided inferior but the PI agent caught that the primary computation used a
results on our task. Frontier model comparison is orthogonal table of paper results — a first-principles violation baked into
to our contributions and is an area for future work; we expect the spec itself. A single verifier checking both axes reliably
that other models will improve over time and that Rosetta’s deprioritizes one. Finally, LLM stochasticity makes single-
architecture will be able to leverage those improvements as run output unreliable: on NeuRex, Run 1 predicted a 3×
they arise. slowdown; Run 2 crashed yet hallucinated an interpretation;
Output token budgets follow a consistent two-tier design: only Run 3 produced a sound derivation. On Darwin, only
generator and repair agents start at 16,384 tokens, while one of three runs correctly decomposed the 15,000× head-
verifier agents start at 8,192 tokens, reflecting that verifica- line speedup into per-workload components. The best-of-N
tion requires shorter structured responses than generation. All ensemblewithaselectoragentexploitsthisvariancetoreliably
agentsshareahardcapof64,000tokens.Ifanagentterminates extract the most analytically sound output. Advanced single-
due to a context-length error, it retries up to three times with agent environments (e.g., Claude Code) offer execution and
5

error-repairloopsbutcollapseallofthesesafeguards:asingle help an outsider understand a paper’s performance claims —
agent critiquing its own spec suffers from confirmation bias, correctly identifying bottlenecks, surfacing implicit assump-
cannot perform orthogonal dual verification, and precludes tions, and quantifying gaps between the described mechanism
the stochastic variance the ensemble exploits. Multi-agent and the reported results? We curated a set of architecture
separationisnotscaffolding;itisthecoremechanismguarding papers spanning diverse problem domains, asked experienced
against self-consistent but flawed reasoning. architecture researchers to evaluate Rosetta’s outputs against
both the paper and their own understanding using a structured
IV. EVALUATIONMETHODOLOGY
rubric, and analyzed the results.
Rosetta outputs mechanistic understanding, not numerical
predictions alone. Evaluating it faces the same challenge as A. Experimental Setup
evaluating simulation frameworks [7], [40], [46] and bench- Paperselection.Weselected12papersfromISCA,ASPLOS,
marksuites[20]:nosingleautomatedmetriccaptureswhether and MICRO spanning seven domains (Table II), chosen to
an analytical artifact is correct, insightful, and useful. We cover a wide difficulty spectrum: from papers with explicit
evaluate across three complementary tracks — correctness, analytical formulas (e.g., CraterLake) to those supported pri-
generalization, and practitioner adoption as detailed below marily by simulation (e.g., Warehouse-scale Video), with
across three types of case studies (CS). citation counts ranging from 39 to over 1,000.
CS1 (Section V) evaluates correctness and insight: 12 Evaluation protocol. The automated selector chose the best
landmark papers spanning diverse domains, each assessed by of three ensemble runs per paper (Section III-E). Each human
an independent human evaluator using a structured rubric — evaluator1 then read or re-read the paper, examined all three
analogous to validating a simulator against known microar- outputartifacts,andcompletedtherubricprovided(3–7hours
chitectural behavior. CS2 (Section VI) tests generalization: perpaper).Evaluatorswerearchitectureresearcherswithbroad
Rosetta runs on 97 uncurated ISCA 2025 and HPCA 2026 hardware-systems competence (self-rated 1–3/5 on domain-
papers, scored by the automated selector, to confirm that specific expertise), recruited independently of Rosetta, given
CS1’s curated selection does not flatter the system. CS3 no briefing on what constitutes “good” output, and instructed
(Section VII) measures practitioner value: we give Rosetta to be as critical as appropriate. They completed rubrics inde-
to 6 active research groups whose authors have simulation pendentlywithnoaccesstopapercode,orsimulators,andare
groundtruthanddesignintentabsentfromthePDF,andcollect not co-authors on this paper.
self-evaluations including concrete impact on the paper under Rubricstructure.Thiscasestudy’srubriccoversfourdimen-
development. sions:
All results reported here are from Rosetta running in fully
• Specification quality (Part 1): correctness of core relation-
autonomous mode (a single launch of the multi-agent pipeline
ship extraction, richness and completeness (1–5), hallucina-
withonlythepaperPDFasinput,zerohumanintervention,no
tion check, and quality of the plain-English interpretation
post-hoc editing) to establish a lower bound on capability. In
(1–5).
practice, the generated artifacts are self-contained and well-
• Modelquality(Part2):execution,specfidelity,baselinevs.
commented; researchers can load them into any AI-assisted
proposed comparison, calibration overlay, self-containment,
coding environment (e.g., Claude Code, Cursor) alongside the
code clarity (1–5).
PDF and iterate directly.
• Insight value (Part 3): parametric understanding (1–5), as-
Frontier model training data. The CS1 landmark papers
sumption surfacing (1–5), insight beyond reading the paper
(published2007–2023)arelikelyinClaudeOpus4.5’straining
alone (1–5), and gap identification.
data (cutoff May 2025). However, Rosetta’s task — deriving
• Overall assessment (Part 4): overall usefulness (1–5), best
a structured mathematical specification and executable model
concrete output, biggest failure, and whether the Evaluator
cognizant of hardware constraints is distinct from recall or
would use Rosetta again on papers in this area.
summarization. CS2’s ISCA 2025 and HPCA 2026 papers
Parts1d,3a–3c,and4arequirethemostevaluatorjudgment
werepublishedatorafterthetrainingcutoff,andCS3’spapers
and show the greatest variance across papers.
are unpublished work no frontier model has seen. CS1 is
thusthemostconservativeevaluationcondition;CS2andCS3 B. NeuRex (Neural Rendering) Deepdive
provide progressively stronger completely contamination-free
We begin with a look into one of the evaluator reports to
evidence. The PRIME DIRECTIVE explicitly prohibits using
illustrate the depth and nature of the insights produced by
reported results as formula inputs, so even memorized paper
Rosetta, and then synthesize across all 12 papers to identify
content cannot enter the derivation.
recurring patterns and conditions that predict when Rosetta
In the main text we present synthesized findings and repre-
adds the most value.
sentativedeepdives.Thefullgeneratedcorpuswillbereleased
NeuRex [44] is a custom hardware accelerator for neural
as a companion artifact.
radiance field (NeRF) rendering (ISCA 2023) that achieves
V. CASESTUDY1:CORRECTNESSANDINSIGHT
1We use “human evaluator” throughout to distinguish the independent
As described in Section IV, CS1 evaluates correctness and
researchers who assessed Rosetta’s outputs from the automated selector and
insight depth: does Rosetta produce analytical models that verifieragentswithinthepipeline.
6

Frommodel.py—GPUbandwidthefficiency(excerpt):
|     |     |     |     |     |     |     | def              | compute_gpu_bandwidth_efficiency( |                     |                   |                   |                 |             |             |         |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --------------------------------- | ------------------- | ----------------- | ----------------- | --------------- | ----------- | ----------- | ------- |
|     |     |     |     |     |     |     | cacheline_bytes, |                                   |                     | bytes_per_entry): |                   |                 |             |             |         |
|     |     |     |     |     |     |     | """From          |                                   | Sec 3.4:            | ‘each             | hash              | entry           | access      |             |         |
|     |     |     |     |     |     |     | only             | uses                              | four                | out of            | 64 bytes’"""      |                 |             |             |         |
|     |     |     |     |     |     |     | return           | bytes_per_entry                   |                     |                   | / cacheline_bytes |                 |             |             |         |
|     |     |     |     |     |     |     | # 4/64           | =                                 | 0.0625              |                   |                   |                 |             |             |         |
|     |     |     |     |     |     |     | # Cache          |                                   | fit analysis        |                   | (first            | principles):    |             |             |         |
|     |     |     |     |     |     |     | # Xavier         |                                   | NX: 2               | MB table          | > 256             | KB              | L2 ->       | misses      |         |
|     |     |     |     |     |     |     | # RTX            | 3070:                             | 2                   | MB table          | < 4               | MB L2           | ->          | fits        |         |
|     |     |     |     |     |     |     | table_fits       |                                   | = gpu.l2_cache      |                   | >=                | hash.table_size |             |             |         |
|     |     |     |     |     |     |     | # Speedup        |                                   | = T_gpu             | / T_neurex        |                   | (NOT            | calibrated) |             |         |
|     |     |     |     |     |     |     | # eta_util       |                                   | swept               | in [0.10,         |                   | 0.40]           |             |             |         |
|     |     |     |     |     |     |     | Fig.             | 6: Excerpt                        | from                | the               | generated         | model.py        |             | for         | NeuRex. |
|     |     |     |     |     |     |     | The              | code                              | derives performance |                   | from              | hardware        |             | parameters; | the     |
Fig. 4: Sensitivity analysis from the NeuRex model: predicted paper’s reported results appear only as scatter overlays for
|     |     |     |     |     |     |     | comparison, |     | never | as formula | inputs. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----- | ---------- | ------- | --- | --- | --- | --- |
speedupvs.GPUutilizationηfortheEdge(XavierNX,green)
| and Server | (RTX    | 3070, purple) | configurations. |     | Dashed | lines |        |                  |                    |      |            |     |        |      |          |
| ---------- | ------- | ------------- | --------------- | --- | ------ | ----- | ------ | ---------------- | ------------------ | ---- | ---------- | --- | ------ | ---- | -------- |
| show the   | paper’s | claimed       | speedups.       |     |        |       |        |                  |                    |      |            |     |        |      |          |
|            |         |               |                 |     |        |       | NeuRex | is               | a first-principles |      | derivation |     | of why | GPUs | struggle |
|            |         |               |                 |     |        |       | with   | multi-resolution |                    | hash | encoding:  |     |        |      |          |
FromSPECIFICATION.md—HardwareParameters(excerpt):
|     |     |     |     |     |     |     |     |     |     | B   |     | 4bytes |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
entry
| Variable              |     | Edge | Server |     | Source    |     |     | η BW,GPU |     | =         |     | =       |     | =6.25% |     |
| --------------------- | --- | ---- | ------ | --- | --------- | --- | --- | -------- | --- | --------- | --- | ------- | --- | ------ | --- |
|                       |     |      |        |     |           |     |     |          |     | B         |     | 64bytes |     |        |     |
| NIGU (IndexGen.Units) |     | 8    | 64     |     | §4.4,Tab4 |     |     |          |     | cacheline |     |         |     |        |     |
SGC
(Gridcache) 64KB 64KB Tab4,§6.4 Each hash table entry stores two 16-bit features, but GPU
| SSB (Subgridbuffer)  |     | 128KB | 128KB |     | Tab4    |     |        |         |         |     |       |                |     |       |          |
| -------------------- | --- | ----- | ----- | --- | ------- | --- | ------ | ------- | ------- | --- | ----- | -------------- | --- | ----- | -------- |
|                      |     |       |       |     |         |     | memory | fetches | 64-byte |     | cache | lines, wasting |     | 60 of | every 64 |
| NSA (Systolicarrays) |     | 1     | 16    |     | §5,Tab4 |     |        |         |         |     |       |                |     |       |          |
f clk 1GHz 1GHz §5 bytes. This structural inefficiency explains why NeuRex-Edge
BaselineGPUparameters: (9.17×) outpaces NeuRex-Server (2.88×) by such a wide
|                    | XavierNX |           | RTX3070 | Source            |              |     |         |      |           |         |        |        |       |         |           |
| ------------------ | -------- | --------- | ------- | ----------------- | ------------ | --- | ------- | ---- | --------- | ------- | ------ | ------ | ----- | ------- | --------- |
|                    |          |           |         |                   |              |     | margin: | the  | Xavier    | NX’s    | 256 KB | L2     | cache | cannot  | hold the  |
| SL2 (L2cache)      | 256KB    |           | 4MB     | Sec3.4,publicspec |              |     |         |      |           |         |        |        |       |         |           |
|                    |          |           |         |                   |              |     | 2 MB    | hash | table,    | forcing | every  | lookup | to    | LPDDR4  | main      |
| BWmem              | 51.2GB/s |           | 448GB/s | Publicspec        |              |     |         |      |           |         |        |        |       |         |           |
|                    |          |           |         |                   |              |     | memory, |      | while the | RTX     | 3070’s | 4 MB   | L2    | already | partially |
| BWEff(GPU):ηBW,GPU |          | =Bentry/B |         |                   | =4/64=0.0625 |     |         |      |           |         |        |        |       |         |           |
cacheline
Source:Sec3.4,“eachhashentryaccessonlyuses4outof64bytes.” solvestheproblemNeuRexisdesignedtoaddress.Themodel
|     |     |     |     |     |     |     | sweeps | GPU | utilization |     | η ∈ [0.10,0.40] |     | without | calibrating |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ----------- | --- | --------------- | --- | ------- | ----------- | --- |
Fig.5:ExcerptfromthegeneratedSPECIFICATION.mdfor
|         |       |           |           |      |                |     | to the    | paper’s | claims;      | both | speedup |       | figures   | fall within | the |
| ------- | ----- | --------- | --------- | ---- | -------------- | --- | --------- | ------- | ------------ | ---- | ------- | ----- | --------- | ----------- | --- |
| NeuRex. | Every | parameter | is traced | to a | paper section; | the |           |         |              |      |         |       |           |             |     |
|         |       |           |           |      |                |     | predicted |         | band (Figure | 4).  | The     | human | evaluator | captured    | the |
bandwidth efficiency is derived from hardware fundamentals. mode of value precisely:
|               |            |         |           |           |                  |        |     | “Makes        | plain    | from        | base   | principles | how      | the     | new |
| ------------- | ---------- | ------- | --------- | --------- | ---------------- | ------ | --- | ------------- | -------- | ----------- | ------ | ---------- | -------- | ------- | --- |
|               |            |         |           |           |                  |        |     | accelerator   | outpaces |             | GPUs.  | It         | provides | upfront |     |
| 9.17× speedup | over       | an edge | GPU       | and 2.88× | over a           | server |     |               |          |             |        |            |          |         |     |
|               |            |         |           |           |                  |        |     | analysis      | of the   | paper’s     | claims |            | and      | exposes | the |
| GPU using     | restricted | hashing | to shrink | the       | multi-resolution |        |     |               |          |             |        |            |          |         |     |
|               |            |         |           |           |                  |        |     | gaps/withheld |          | information |        | of the     | paper.”  |         |     |
| hash table    | working    | set     | from 2 MB | to        | 32 KB. It        | earned |     |               |          |             |        |            |          |         |     |
the highest scores across all CS1 dimensions (Spec, Model, C. Aggregate Results
| Insight, | Overall | all 5/5). | To illustrate | exactly | what | Rosetta |     |     |     |     |     |     |     |     |     |
| -------- | ------- | --------- | ------------- | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TableIIsummarizesevaluationscoresacrossthe12papers,
generates, we show concrete excerpts from the NeuRex arti- which we analyze further below.
| facts before | discussing | the | findings. |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Specandinterpretationqualityisthemostreliableoutput.
What Rosetta generates: artifact excerpts. Figure 5 shows Across all 12 evaluations, Spec+Interpretation quality scores
a representative excerpt from the generated specification: the range from 3 to 5, with ten of twelve papers at 4 or above.
hardwareparametertablefortheNeuRexacceleratorandbase- Human evaluators found that Rosetta reliably identifies the
lineGPUs,witheveryvaluetracedtoaspecificpapersection. correct hardware parameters, constructs analytically reason-
Figure6showsthecorrespondingmodel.pyimplementation
|     |     |     |     |     |     |     | able | cost | functions, | and | produces | an interpretation |     |     | document |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ---------- | --- | -------- | ----------------- | --- | --- | -------- |
of the GPU bandwidth-efficiency derivation — the core first- that genuinely helps a newcomer orient to the paper. One
principles calculation that drives the model’s predictions. The human evaluator noted: “I found myself using the interpre-
full specification is 643 lines; the full model is 1,177 lines of tation to help guide me through a re-read of the paper.”
self-contained Python. Figure 4 is one of the graphs produced Zero expert evaluations reported significant hallucinations;
bythemodel(detailsshortly).Allthreeartifacts(spec,model,
|     |     |     |     |     |     |     | four | reported | minor | ones | (CraterLake: |     | assumed | register | file |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------- | ----- | ---- | ------------ | --- | ------- | -------- | ---- |
interpretation) are generated autonomously typically in 30 to port counts and an arbitrary F1+ bandwidth value; Darwin:
40 minutes. a bandwidth unit misinterpretation in the de novo throughput
Key analytical finding. Rosetta’s primary contribution for path; Warehouse: assumed combined read/write accounting;
7

TABLEII:CS1scores(12papers,1–5scale).S=Spec+Interp,
open; (ii) the paper reports performance at a single operating
M=Model,R=Richness,P=Parametric,A=Assumptionsurfac-
point, and the parametric model reveals behavior across a
ing,I=Insight>Paper,O=Overall.?=UseAgain(D=Definitely,
design space. The CraterLake L-dependence sweep is the
P=Probably, U=Unsure).
clearest example of (ii): the paper reports speedup at fixed
benchmarks, but Rosetta produced a continuous speedup vs.
Paper Domain S M R P A I O ?
L curve showing 4× at low L (shallow FHE) to 51× at
BASALISC[22] FHE 5 5 4 4 4 4 5 D
high L (deep FHE) — a result not available from the paper’s
Darwin[74] Genomics 4 5 5 3 2 5 5 D
CraterLake[66] FHE 4 3 4 4 1 4 5 P tables alone. NeureX and Darwin are the two papers reaching
Warehouse[61] Video 4 4 3 5 3 3 4 U 5/5 insight; in both cases the paper describes dense hardware
Anton[69] Mol.Dyn. 4 5 4 2 3 4 4 P
mechanisms whose parametric interaction the model resolves
GenAx[21] Genomics 4 4 4 4 3 4 5 P
Genesis[26] Genomics 5 4 4 5 3 4 5 P into a navigable design-space map.
SeGraM[10] Genomics 3 2 3 3 1 3 4 P
GZKP[54] ZKProofs 3 5 4 3 3 3 4 P Key takeaway: Insight value is highest when papers have
PipeZK[88] ZKProofs 4 3 3 4 4 4 5 P richhardwaredescriptionsbutsparseexplicitmath,andwhen
NeuRex[44] Neur.Rend. 5 5 4 4 4 5 5 D
parametric sweeps reveal design-space behavior hidden in
MD-Pipe[37] Mol.Dyn. 4 4 4 3 3 4 5 P
point results.
Whereinsightisbounded.Threepapersscore3/5oninsight,
SeGraM: an HBM channel–accelerator topology assumption) each for a distinct structural reason. Warehouse-scale Video
that human evaluators considered inconsequential to the core illustrates a parameter-withholding ceiling: key configuration
derivation. valuesarewithheldforproprietaryreasons,preventingRosetta
Key takeaway: The specification and interpretation are from explaining the 6.5× gap between theoretical peak and
Rosetta’smostreliableoutputs,scoring4+on10of12papers observed throughput. The Evaluator credited the model for
with zero significant hallucinations. correctly reaching this conclusion and flagging it: “the model
Model quality is strong but bounded by spec quality. knows why the model is lean — I don’t think a human
Model quality scores range from 2 to 5, with five papers coulddoanybetter.”GZKPillustratesacomponent-divergence
at 5/5 (BASALISC, Darwin, Anton, GZKP, NeureX). In one ceiling: NTT results are confirmed analytically, but the MSM
confirmed case, the model corrects a minor spec-level error: component model diverges substantially from empirical re-
Darwin’s model.py fixes an incorrect de novo throughput sults, “calling more questions about itself than the paper it
formulathatpropagatedfromthespecification.Intheopposite is meant to reflect.” SeGraM illustrates a missing-baseline
direction, Anton’s incorrect T
long-range
formula is faithfully ceiling:withoutamodelfortheCPUbaselinethatimplements
reproduced from the spec into the model, illustrating that MinSeed and BitAlign, the comparative insight is limited to
the pipeline’s verify step catches scientific invalidity but does confirming the accelerator’s own scalability properties rather
not independently audit arithmetic against the paper. The 3/5 than explaining the relative speedup. Across all three, Rosetta
scoresforCraterLakeandPipeZKbothreflectspec-levelgaps correctly diagnoses the ceiling rather than producing spuri-
propagated into code: for CraterLake, the F1+ baseline incor- ously confident output.
rectly used CraterLake’s CRB unit cycles when F1+ has no
Key takeaway: When insight is bounded, Rosetta identifies
suchhardware;thesingle2/5(SeGraM)reflectsaninadequate
why — parameter withholding, component divergence, or
baseline model: the BitAlign accelerator derivation correctly
missing baselines — rather than spuriously confident output.
follows Algorithm 1 line-by-line, and the 100× end-to-end
latency gap is correctly identified as the central analytical When Does Rosetta Add Most Value? Across all 12
finding, but the CPU comparison system is modeled as a evaluations,Rosetta’sinsightvalueisafunctionofthepaper’s
generic processor rather than one implementing the MinSeed mathematical disclosure posture, not of Rosetta’s intrinsic
andBitAlignalgorithmsthatSeGraMaccelerates—agapthe capability. Crucially, the three papers scoring 3/5 on insight
paper’sownsparsebaselinedescriptionmakesdifficulttoclose — Warehouse-scale Video, SeGraM, and GZKP — share a
from the PDF alone; and flagged in the SPEC critique, and common characteristic: Rosetta correctly diagnosed its own
observed in INTERPRETATION. This confirms a key design ceiling rather than producing spuriously confident output, a
constraint:modelqualityisboundedbelowbyspecquality— property that makes its confirmed findings credible. Table III
a sound model cannot be built on an insufficient specification. catalogs the eight recurring finding types observed across the
Key takeaway: Model quality (2–5) is never higher than 12 papers; four conditions consistently predict high insight
spec quality; the verify-repair loop’s primary leverage point value: (1) rich hardware description with sparse explicit math
is the specification phase. (forces assumptions into the open); (2) single-point results
Insight value is the most discriminating dimension. The whose latent parametric structure the model reveals; (3) a
“insight beyond paper” score varies most widely (3–5) and is gapbetweenfirst-principlespredictionandclaimedresultsthat
thestrongestpredictorofoverallusefulness.Rosettaaddsmost characterizes rather than condemns; and (4) formalization as
value when: (i) the paper presents sparse mathematical detail standalone value, where the specification delivers insight even
but rich hardware description, forcing assumptions into the when the quantitative model is imperfect.
8

TABLE III: Recurring finding types across CS1, with representative papers and concrete outputs.
Finding type Papers What Rosetta produced
Structural hardware bottleneck NeuRex,Genesis 6.25% BW efficiency (4/64 bytes/cache-line); 2.08× achieved is
from first principles within 1.4% of Amdahl ceiling
Parametric sweep reveals hidden CraterLake, L-dependence curve (4× → 51×); η-sweep bracketing claimed
design-space behavior NeuRex,PipeZK speedup without calibration; degradation from 197× to 30× across
problem sizes
Module-to-systemgapclosedan- PipeZK, Genesis Amdahl prediction 5.2× vs. paper’s 5.8×; ceiling identifies true
alytically performance floor
Formalizationasstandalonevalue PipeZK 5/5 Overalldespite 3/5 Model; qualitativepaper statements converted
(model imperfect) to quantified boundaries
Component-levelaudit:confirma- GZKP NTT O(NlogN) scaling verified; MSM sign-flip inverts speedup
tion and divergence prediction
Modelcorrectsaspec-levelpaper Darwin Incorrectdenovothroughputformulacaughtinimplementationphase
error
Paperwithholdsquantitativedata; NeuRex, η-sweep without calibration; proprietary ceiling correctly diagnosed
model makes claims checkable Warehouse
Missing-baselineceilingcorrectly SeGraM 100× latency gap attributed to undocumented optimizations; generic-
diagnosed CPU baseline limits comparative insight
D. CAAM-Bench: CompArch Analytical Model Benchmark ISCA 2025 (80) and HPCA 2026 (17). An independent
fit judge excluded 17 papers unsuitable for first-principles
No standard benchmark exists for evaluating tools that
analysis (scheduling heuristics, purely algorithmic work); the
automatically generate analytical models from architecture
remaining 78 papers form the reported corpus. Across these,
papers,makingreproduciblecomparisonacrossapproachesor
meanInsightQualityis8.2/10andmeanCorrectnessis7.8/10;
over time impossible. We release the CS1 evaluation set as
56% reach Tier A (9–10) and 91% score 7+. We classified
CAAM-Bench (CompArch Analytical Model Benchmark) to
outcomesintothreecategories:GAP-ONLY(60,77%)where
fill this gap. CAAM-Bench has three components:
the model quantifies a discrepancy without attributing a cause
• 12landmarkarchitecturepapersspanningsevendomains
it cannot derive; SHOWS-NEW-INSIGHT (12, 15%) where
(TableII),selectedtocoverawidedifficultyspectrumfrom
the derivation surfaces a tension with a specific claim not
paperswithexplicitanalyticalformulastosimulation-heavy
visible from reading alone; and VALIDATES (5, 6%) where
works, with citation counts from 39 to over 1,000.
the derivation independently confirms the paper’s result. The
• Reference artifacts: for each paper, a human-vetted
median pipeline runtime is 73 minutes at ∼$39/paper ($3,800
SPECIFICATION.md and model.py produced by
total).
Rosetta and confirmed by an independent domain-expert
Keytakeaway:Rosettageneralizesatconferencescale,with
evaluator. These serve as a quality baseline — a concrete
15% of papers surfacing analytical tensions not visible from
target for future tools to match or exceed.
reading the paper alone.
• A scoring protocol: the four-dimension CS1 rubric (spec-
ification quality, model quality, insight value, overall use- VII. CASESTUDY3:RESEARCHERUSE
fulness) applied to the spec and model produced by any
As described in Section IV, CS3 tests practitioner value:
tool or LLM on the same 12 papers. The rubric can be
does Rosetta add value during active research? We gave
applied by human evaluators or, following CS2’s approach,
Rosetta to six research groups with papers at premier ar-
by an automated scorer calibrated against the human-vetted
chitecture venues (submitted, under revision, or accepted)
reference. Rosetta’s scores (Table II) serve as the published
and collected author self-evaluations using a structured rubric
baseline.
(Figure 7). Authors evaluated Rosetta’s output against their
CAAM-Bench enables reproducible evaluation of future
own simulation ground truth and design intent — context
analyticalmodelgeneratorsbyprovidingafixedpapercorpus,
absent from the PDF and unavailable to CS1’s external eval-
reference artifacts, and a common scoring protocol. The 12
uators. Titles and venues are redacted as the papers are active
papers span sufficient domain diversity — FHE, genomics, submissions2.
molecular dynamics, ZK proofs, neural rendering, and video
— that performance on any single domain is unlikely to A. Researchers Want to Use Rosetta Again
generalize without genuine analytical depth. All benchmark
We do not bury the lede. Five of six CS3 evaluators —
materials are released with this paper.
including those who gave the lowest overall scores — said
“Definitely” when asked whether they would run Rosetta on
VI. CASESTUDY2:BREADTHSTUDY
their next paper; the sixth said “Unsure” only because their
To confirm that CS1’s curated selection does not flatter
the system, we ran Rosetta on 97 unfiltered papers from 2Allpaperstargettop-3architectureorsystemsvenues.
9

paper was a simulation study at the hardest analytical ceiling. the PDF. The author rated the output 2/5; we report that as
The impact these researchers describe goes beyond anything ground truth.
asingleaccuracynumbercancapture.SYMI’sevaluator:“No Readingsynthesisvalue.Beforetheperformancemodelruns,
reviewerwouldhavethetimetowriteasimulationtovalidate Rosetta’s reading assistant independently flagged four analyt-
a paper’s empirical results, but with Rosetta it’s a 5-minute ical observations: the headline speedup over a prior FPGA
task.” SgBend’s evaluator: “If we had used this from the baseline includes a clock-frequency component alongside the
beginning, we might have been able to have a more profound architectural improvement; benchmark selection was bounded
influence on the final work — it also may have helped us by a wall-clock simulation budget, omitting larger instances;
earlier for idea development and eliminating less promising most selected instances fit on-chip, concentrating the off-chip
ideas.” D-Com’s evaluator: “Made assumptions explicit, and scalabilityevidenceinasinglereduced-cacheexperiment;and
the generated spec is useful.” The Mamba evaluator gave the heuristic-solver comparison involves asymmetric capabil-
the only 5/5 spec richness in the CS3 set: “Did a great ity sets. The author confirmed post-hoc that the paper was
job comprehending the Einsums, the fusion taxonomy, and subsequently rewritten to address exactly these concerns —
the 2D/1D reconfigurable array. Surprisingly well.” Even the the reading synthesis had identified the same objections that
GT evaluator, who rated overall usefulness at 2/5, confirmed program-committee reviewers later raised in writing.
that Rosetta’s bandwidth under-utilization derivation “is very Quantitative model: one confirmed finding, one error.
similar to our simulation results.” The model derives baseline cycles per traversal step as
Keytakeaway:Acrosssixindependentevaluationsspanning tbase ≈ 167 cycles, implying memory bandwidth utilization
step
fivedifferentsystemdomains,theconsistentsignalisadoption of only ≈ 3.8% — the system is severely latency-bound,
intent — not because the models are perfect, but because the not bandwidth-bound. The author explicitly confirmed this
formalization process itself changes how researchers engage against simulation. A second finding — that the accelerator
with their own work. has worse vertex-data cache hit rates than the baseline (60%
vs. 70%) but better adjacency-list hit rates (85% vs. 65%) —
B. Other Per-Paper Technical Findings wasalsoverifiedagainstsimulationandfoundtobewrong.We
reportthisasagenuinemodelerror.First-principlesderivation
We summarize the key Rosetta-driven finding from each
closes to 9.19× speedup against the paper’s 22.77×, a 2.48×
paper below.
unexplained gap.
SYMI (MoE training): Rosetta reproduced the paper’s
Author verdict and scope implication. The author rated
communication-costformulasandindependentlyconstructeda
overall usefulness at 2/5 and “Unsure” for future use, and
Zipfian-distributiontrainingsimulation—anapproachtheau-
offered the most precise diagnosis of the gap: not missing
thorhadstartedandabandonedforthesamereason(toomany
hardwareparameters,buttheLLM’slackofalgorithm-specific
assumptions about the skewness parameter). The convergence
understandingofhowthecorepropagationalgorithminteracts
ratiomatchedprecisely(29%faster).Theauthornotedthatan
with memory access patterns. This is a hard scope boundary:
earlierinteractiverun“couldhavebeenincorporateddirectly”
even a complete parameter checklist cannot bridge it. The
into the paper.
author’smostactionablesuggestion:“AddingaQ&Apartwith
D-Com (LLM inference): SPECIFICATION.md revealed
a planning phase could help make sure the model stays on
that the paper’s exposition insufficiently separated the moti-
track” — a pre-flight audit that enumerates which analytical
vational GPU analysis from the proposed custom accelerator;
inputs are and are not recoverable from the paper alone.
the paper was updated to sharpen this boundary.
Mamba (SSM accelerator): Earned 5/5 spec richness and D. Aggregate Results
surfaced a terminological tension — whether “fully fused”
Spec richness averages 4.0/5 with five of six at 4+,
is accurate when DRAM traffic exists at skip-connection
consistent with CS1’s finding that the specification is the
boundaries.
pipeline’s most reliable phase. Every CS3 evaluator named
TOPO (sparsity/RT core): Hardware pipeline captured
SPECIFICATION.md as the most valuable output, indepen-
correctly; workload abstractions too generic to match simula-
dent of model accuracy. Four of six evaluations produced a
tion, establishing the dataset-dependence boundary condition.
documented change to the paper.
SgBend (SpGEMM): Strongest concrete impact: Rosetta
Keytakeaway:Theformalizationpassaddsvalueregardless
identified an IPM lookup latency the authors’ own simulator
of whether model.py closes numerically; four of six papers
had underestimated, directly motivating a new experiment
were changed as a direct result.
added to the paper.
TheSPECIFICATION.mdartifactisthemostconsistently
valued output. Every CS3 evaluator named it as the most
C. A Graph Traversal Accelerator(GT)
valuable output, independent of model accuracy. SYMI’s spec
We now highlight the graph traversal simulation study (the enabled an independent rediscovery of the author’s own aban-
hardest analytical case) This paper studies a graph traver- doned simulation; D-Com’s surfaced a structural exposition
sal accelerator. The lead author compared Rosetta’s output problem in the paper; SgBend’s introduced a new analytical
against cycle-accurate simulation ground truth not present in techniqueforcapturingdata-dependenthardwarebehaviorthat
10

claimverification,andliteraturesynthesis[4],[51],[72],[76],
| Dimension     |      | What it                              | asks     |                  |                |          |               |           |                |                     |              |     |           |         |
| ------------- | ---- | ------------------------------------ | -------- | ---------------- | -------------- | -------- | ------------- | --------- | -------------- | ------------------- | ------------ | --- | --------- | ------- |
|               |      |                                      |          |                  |                |          | [79], [82].   | Beyond    | comprehension, |                     | systems      |     | like The  | AI Sci- |
| Core capture  | (2a) | Did Rosetta                          | identify | the              | key analytical | re-      |               |           |                |                     |              |     |           |         |
|               |      |                                      |          |                  |                |          | entist [52],  | FunSearch |                | [63], AlphaGeometry |              |     | [73], and | formal  |
|               |      | lationships                          | the      | author considers |                | central? |               |           |                |                     |              |     |           |         |
|               |      |                                      |          |                  |                |          | provers [60], | [84]      | attempt        | automated           | mathematical |     | discovery |         |
| Spec richness | (2b) | Doesthespeccapturebaseline+proposed, |          |                  |                |          |               |           |                |                     |              |     |           |         |
parameters, operating conditions? and experimentation. LLMs are also explored for automated
Interpquality(2e) Does INTERPRETATION.md accurately peer review [47], [48]. Rosetta fundamentally differs: it does
|                   |      | explain                               | the work | to an outsider? |           |         |                   |            |             |             |          |               |                |          |
| ----------------- | ---- | ------------------------------------- | -------- | --------------- | --------- | ------- | ----------------- | ---------- | ----------- | ----------- | -------- | ------------- | -------------- | -------- |
|                   |      |                                       |          |                 |           |         | not generate      | novel      | hypotheses, |             | train    | models,       | or recommend   |          |
| Assumption        | sur- | Did formalizing                       |          | expose          | implicit  | assump- |                   |            |             |             |          |               |                |          |
|                   |      |                                       |          |                 |           |         | paper acceptance. |            | Instead,    | it operates | as       | an analytical |                | auditor, |
| facing            | (3a) | tionstheauthorhadnotpreviouslystated? |          |                 |           |         |                   |            |             |             |          |               |                |          |
|                   |      |                                       |          |                 |           |         | extracting        | parameters |             | from        | existing | text to       | mathematically |          |
| Parametricclarity |      | Did the                               | model    | illuminate      | parameter | sensi-  |                   |            |             |             |          |               |                |          |
(3b) tivity the author hadn’t fully explored? verify claimed mechanisms against first principles.
Impact on paper Did Rosetta’s output change any claim, Multi-Agent Architectures and Verification Rosetta lever-
| (3c)    |            | section, | or experiment? |        |     |     |             |            |     |          |               |     |             |      |
| ------- | ---------- | -------- | -------------- | ------ | --- | --- | ----------- | ---------- | --- | -------- | ------------- | --- | ----------- | ---- |
|         |            |          |                |        |     |     | ages recent | advances   |     | in LLM   | reasoning     |     | (Chain/Tree | of   |
| Overall | usefulness | Holistic | author         | rating |     |     |             |            |     |          |               |     |             |      |
|         |            |          |                |        |     |     | Thought     | [80], [85] | to  | mitigate | hallucination |     | [36]), code | gen- |
(5a)
|            |      |                                     |     |     |     |     | eration [13], | [64], | [78], | [86], | and multi-agent |     | roles | [30], |
| ---------- | ---- | ----------------------------------- | --- | --- | --- | --- | ------------- | ----- | ----- | ----- | --------------- | --- | ----- | ----- |
| Use again? | (4c) | WouldyourunRosettaduringdevelopment |     |     |     |     |               |       |       |       |                 |     |       |       |
of your next paper? [45], [83]. To ensure robustness, we build upon iterative
|       |        |      |      |      |      |      | self-refinement |     | [33],       | [42], [55], | [59],         | [70], | multi-agent | de-     |
| ----- | ------ | ---- | ---- | ---- | ---- | ---- | --------------- | --- | ----------- | ----------- | ------------- | ----- | ----------- | ------- |
| Paper | Domain | (2a) | (2b) | (2e) | (5a) | (4c) |                 |     |             |             |               |       |             |         |
|       |        |      |      |      |      |      | bate/evaluation |     | [12], [18], | [89],       | and Best-of-N |       | process     | verifi- |
GT⋆ GraphTrav. Partly 4 3 2 Unsure cation [9], [15], [49]. However, while Constitutional AI [6]
SYMI† MoE Sys. Mostly 4 – 3 Definitely enforces behavioral norms via RLHF, Rosetta pioneers a
D-Com‡
LLM Inf. Yes 4 3 4 Definitely scientific constitution (the PRIME DIRECTIVE) enforced via
Mamba⋆
SSM Yes 5 3 3 Definitely strict generator-verifier separation. Crucially, we introduce
TOPO‡
|         | Sparsity | Partly |     | 3 3 | 3   | Definitely |               |                   |     |          |                  |      |                |        |
| ------- | -------- | ------ | --- | --- | --- | ---------- | ------------- | ----------------- | --- | -------- | ---------------- | ---- | -------------- | ------ |
|         |          |        |     |     |     |            | an orthogonal | dual-verification |     |          | step (functional |      | vs. scientific |        |
| SgBend† | SpGEMM   | Partly |     | 4 5 | 4   | Definitely |               |                   |     |          |                  |      |                |        |
|         |          |        |     |     |     |            | validity)     | to prevent        | the | specific | failure          | mode | where          | an LLM |
faithfullyimplementsacircular,non-first-principlesmathemat-
| Fig. 7: | CS3 rubric | dimensions | (top) | and | scores | (bottom). |     |     |     |     |     |     |     |     |
| ------- | ---------- | ---------- | ----- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Scoreddimensionsuse1–5;categorical:Yes/Mostly/Partly/No icalspecification.WhilerecentsystemslikePaperBanana[90]
|          |                               |     |     |       |            |     | orchestrate | specialized |     | agents | to automate | the | generation | and |
| -------- | ----------------------------- | --- | --- | ----- | ---------- | --- | ----------- | ----------- | --- | ------ | ----------- | --- | ---------- | --- |
| (2a) and | Definitely/Probably/Unsure/No |     |     | (4c). | ⋆Rejected, | be- |             |             |     |        |             |     |            |     |
ing revised; †Accepted; ‡New submission. critique of academic visual illustrations, Rosetta applies a
|                  |           |            |          |               |              |           | similar multi-agent |     | decomposition   |            | to the       | extraction | of  | mathe- |
| ---------------- | --------- | ---------- | -------- | ------------- | ------------ | --------- | ------------------- | --- | --------------- | ---------- | ------------ | ---------- | --- | ------ |
|                  |           |            |          |               |              |           | matical artifacts   |     | in architecture |            | and systems. |            |     |        |
| the evaluator    | intends   | to adopt.  | The      | formalization |              | pass adds |                     |     |                 |            |              |            |     |        |
| value regardless |           | of whether | model.py | closes        | numerically. |           |                     |     |                 |            |              |            |     |        |
|                  |           |            |          |               |              |           |                     |     | IX.             | CONCLUSION |              |            |     |        |
| Key              | takeaway: | Every      | CS3      | evaluator     |              | named     |                     |     |                 |            |              |            |     |        |
SPECIFICATION.md as the most valuable output, Analytical performance models explain why performance
independent of model accuracy. bounds exist, yet they rarely accompany architecture papers.
|     |     |                   |     |     |     |     | Rosetta automates |     | this: | given | a PDF, it | produces | a mathemat- |     |
| --- | --- | ----------------- | --- | --- | --- | --- | ----------------- | --- | ----- | ----- | --------- | -------- | ----------- | --- |
|     |     | VIII. RELATEDWORK |     |     |     |     |                   |     |       |       |           |          |             |     |
icalspecification,executablePythonmodel,andplain-English
Rosettasitsattheintersectionofanalyticalmodeling,LLM- interpretation with zero human intervention, using a scientific
best-of-N
based scientific reasoning, and multi-agent system design. constitution, dual verification, and a ensemble to
We survey each area, emphasizing how prior work addresses address the failure modes of naive LLM-based generation.
subsets of the problem Rosetta solves end-to-end. Acrossthreetracks,Rosettademonstratescorrectness(10of12
Analytical Modeling and Simulation Analytical models CS1papersat4–5/5specificationquality,zerosignificanthal-
like Roofline [17], [58], [81] and Amdahl’s Law [1], [25], lucinations), generalization (56% Tier A across 78 unfiltered
|             |      |                     |     |             |     |         | conference | papers), | and | practitioner | value |     | (five of | six CS3 |
| ----------- | ---- | ------------------- | --- | ----------- | --- | ------- | ---------- | -------- | --- | ------------ | ----- | --- | -------- | ------- |
| [27], [29], | [35] | provide fundamental |     | performance |     | bounds. |            |          |     |              |       |     |          |         |
Deep learning models [14], [16], [34], [38], [56] apply IO- researchers said “Definitely” for future use). The consistent
complexity and empirical scaling laws. More detailed first- finding is that formalization itself is the primary value: it
principles processor [19], [39] and GPU models [5], [31], surfaces implicit assumptions, flags missing parameters, and
[32], [41], [43], [57], [71], [77], [87] rely on manual interval changes how researchers engage with their own work.
and reuse-distance analysis. Others tailor models to specific We release Rosetta open-source together with CAAM-
workloads or hybridize with simulation [2], [23], [28], [75]. Bench, the first benchmark for evaluating analytical model
However, all are manually constructed by experts. In contrast, generatorsonarchitecturepapers,comprising12human-vetted
cycle-level simulators [3], [7], [11], [53], [62], [67] require paper–artifact pairs and a four-dimension rubric to enable
precise hardware specifications and binaries. Rosetta occupies reproduciblecomparisonoffuturetools.Morebroadly,Rosetta
automates
a unique space: it the creation of analytical models points toward a new community norm: architecture papers
directly from unstructured paper prose. accompanied by a generated spec and model, making every
LLM-Based Science and Peer Review LLMs increasingly performance claim independently auditable by any reader,
assist in scientific document understanding, including QA, without access to the authors’ simulation infrastructure.
11

REFERENCES
[19] S.Eyerman,L.Eeckhout,T.Karkhanis,andJ.E.Smith,“Amechanis-
|     |     |     |     |     |     |     | tic performance |     | model | for superscalar | out-of-order |     | processors,” | ACM |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ----- | --------------- | ------------ | --- | ------------ | --- |
TransactionsonComputerSystems,vol.27,no.2,pp.1–37,2009.
[1] G.M.Amdahl,“Validityofthesingleprocessorapproachtoachieving
[20] M.Ferdman,A.Adileh,O.Koçberber,S.Volos,M.Alisafaee,D.Jevd-
| large | scale computing |     | capabilities,” | AFIPS Conference |     | Proceedings, |     |     |     |     |     |     |     |     |
| ----- | --------------- | --- | -------------- | ---------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
jic,C.Kaynak,A.D.Popescu,A.Ailamaki,andB.Falsafi,“Clearingthe
vol.30,pp.483–485,1967.
clouds:Astudyofemergingscale-outworkloadsonmodernhardware,”
[2] Y.Arafa,A.-H.Badawy,A.ElWazir,A.Barai,A.Eker,G.Chennupati, in Proceedings of the 17th International Conference on Architectural
N.Santhi,andS.Eidenbenz,“Hybrid,scalable,trace-drivenperformance SupportforProgrammingLanguagesandOperatingSystems(ASPLOS),
modelingofGPGPUs,”inProceedingsoftheInternationalConference
2012,pp.37–48.
| for High | Performance       | Computing, | Networking, |     | Storage | and Analysis |                 |                  |               |         |           |            |               |            |
| -------- | ----------------- | ---------- | ----------- | --- | ------- | ------------ | --------------- | ---------------- | ------------- | ------- | --------- | ---------- | ------------- | ---------- |
|          |                   |            |             |     |         |              | [21] D. Fujiki, | A.               | Subramaniyan, | T.      | Zhang, Y. | Zeng,      | R. Das,       | D. Blaauw, |
| (SC).    | ACM,2021,pp.1–15. |            |             |     |         |              |                 |                  |               |         |           |            |               |            |
|          |                   |            |             |     |         |              | and             | S. Narayanasamy, |               | “Genax: | A genome  | sequencing | accelerator,” | in         |
[3] T.Austin,E.Larson,andD.Ernst,“Simplescalar:aninfrastructurefor 2018 ACM/IEEE 45th Annual International Symposium on Computer
computersystemmodeling,”Computer,vol.35,no.2,pp.59–67,2002. Architecture(ISCA),2018,pp.69–82.
[4] J.Baek,S.K.Jauhar,S.Cucerzan,andS.J.Hwang,“ResearchAgent: [22] R. Geelen, M. V. Beirendonck, H. V. L. Pereira, B. Huffman,
Iterative research idea generation over scientific literature with large T. McAuley, B. Selfridge, D. Wagner, G. Dimou, I. Verbauwhede,
languagemodels,”inarXivpreprintarXiv:2404.07738,2024.
|     |     |     |     |     |     |     | F. Vercauteren, |     | and | D. W. | Archer, “BASALISC: |     | Programmable |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | ----- | ------------------ | --- | ------------ | --- |
[5] S.S.Baghsorkhi,M.Delahaye,S.J.Patel,W.D.Gropp,andW.-m.W.
|     |     |     |     |     |     |     | hardware | accelerator |     | for BGV | fully | homomorphic |     | encryption,” |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | ------- | ----- | ----------- | --- | ------------ |
Hwu,“AnadaptiveperformancemodelingtoolforGPUarchitectures,” CryptologyePrintArchive,Paper2022/657,2022.[Online].Available:
inProceedingsofthe15thACMSIGPLANSymposiumonPrinciplesand https://eprint.iacr.org/2022/657
PracticeofParallelProgramming(PPoPP). ACM,2010,pp.105–114. [23] X.Gong,C.Hu,andC.-C.Lim,“PAQSIM:Fastperformancemodelfor
[6] Y.Bai,S.Kadavath,S.Kundu,A.Askell,J.Kernion,A.Jones,A.Chen, graphics workload on mobile GPUs,” in Proceedings of the 21st ACM
et al.,
A. Goldie, A. Mirhoseini, C. McKinnon “Constitutional AI: SIGPLAN/SIGBEDConferenceonLanguages,Compilers,andToolsfor
Harmlessness from AI feedback,” arXiv preprint arXiv:2212.08073, EmbeddedSystems(LCTES).
ACM,2020,pp.127–138.
2022. [24] R. Gupta, A. Jain, A. Gonzalez, A. Novikov, P.-S. Huang,
[7] N.Binkert,B.Beckmann,G.Black,S.K.Reinhardt,A.Saidi,A.Basu, M. Balog, M. Eisenberger, S. Shirobokov, N. Vu˜, M. Dixon,
J. Hestness, D. R. Hower, T. Krishna, S. Sardashti et al., “The gem5 B. Nikolic´, P. Ranganathan, and S. Karandikar, “Archagent: Agentic
simulator,”ACMSIGARCHComputerArchitectureNews,vol.39,no.2, ai-driven computer architecture discovery,” 2026. [Online]. Available:
pp.1–7,2011.
https://arxiv.org/abs/2602.22425
[8] G.E.P.Box,“Scienceandstatistics,”JournaloftheAmericanStatistical
|     |     |     |     |     |     |     | [25] J. L. | Gustafson, | “Reevaluating | Amdahl’s |     | law,” Communications |     | of the |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ------------- | -------- | --- | -------------------- | --- | ------ |
Association,vol.71,no.356,pp.791–799,1976. ACM,vol.31,no.5,pp.532–533,1988.
[9] B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, [26] T.J.Ham,D.Bruns-Smith,B.Sweeney,Y.Lee,S.H.Seo,U.G.Song,
and A. Mirhoseini, “Large language monkeys: Scaling inference Y.H.Oh,K.Asanovic,J.W.Lee,andL.W.Wills,“Genesis:Ahardware
compute with repeated sampling,” 2024. [Online]. Available: https: accelerationframeworkforgenomicdataanalysis,”in2020ACM/IEEE
//arxiv.org/abs/2407.21787 47thAnnualInternationalSymposiumonComputerArchitecture(ISCA),
2020,pp.254–267.
| [10] D. S. | Cali, K. | Kanellopoulos, | J. Lindegger, |     | Z. Bingöl, | G. S. Kalsi, |     |     |     |     |     |     |     |     |
| ---------- | -------- | -------------- | ------------- | --- | ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Z. Zuo, C. Firtina, M. B. Cavlak, J. Kim, N. M. Ghiasi, G. Singh, [27] J.L.HennessyandD.A.Patterson,ComputerArchitecture:AQuanti-
J. Gómez-Luna, N. A. Alserr, M. Alser, S. Subramoney, C. Alkan, tativeApproach,6thed. MorganKaufmann,2019.
S. Ghose, and O. Mutlu, “Segram: a universal hardware accelerator [28] S.Heo,S.Cho,Y.Kim,andH.Kim,“Real-timeobjectdetectionsystem
forgenomicsequence-to-graphandsequence-to-sequencemapping,”in withmulti-pathneuralnetworks,”inProceedingsofthe26thIEEEReal-
Proceedingsofthe49thAnnualInternationalSymposiumonComputer
|     |     |     |     |     |     |     | Time | and Embedded |     | Technology | and Applications |     | Symposium | (RTAS). |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------------ | --- | ---------- | ---------------- | --- | --------- | ------- |
Architecture, ser. ISCA ’22. New York, NY, USA: Association IEEE,2020,pp.174–187.
for Computing Machinery, 2022, p. 638–655. [Online]. Available: [29] M. D. Hill and M. R. Marty, “Amdahl’s law in the multicore era,”
https://doi.org/10.1145/3470496.3527436 Computer,vol.41,no.7,pp.33–38,2008.
[11] T.E.Carlson,W.Heirman,andL.Eeckhout,“Sniper:Exploringthelevel [30] S.Hong,M.Zhuge,J.Chen,X.Zheng,Y.Cheng,J.Wang,C.Zhang,
ofabstractionforscalableandaccurateparallelmulti-coresimulation,” Z. Wang, S. K. S. Yau, Z. Lin et al., “MetaGPT: Meta programming
| in Proceedings |     | of the International | Conference |     | for High | Performance |     |               |               |     |             |     |             |        |
| -------------- | --- | -------------------- | ---------- | --- | -------- | ----------- | --- | ------------- | ------------- | --- | ----------- | --- | ----------- | ------ |
|                |     |                      |            |     |          |             | for | a multi-agent | collaborative |     | framework,” | in  | Proceedings | of the |
Computing,Networking,StorageandAnalysis(SC),2011,pp.1–12. InternationalConferenceonLearningRepresentations(ICLR),2024.
[12] C.-M.Chan,W.Chen,Y.Su,J.Yu,W.Xue,S.Zhang,J.Fu,andZ.Liu, [31] S.HongandH.Kim,“AnanalyticalmodelforaGPUarchitecturewith
“ChatEval: Towards better LLM-based evaluators through multi-agent memory-level and thread-level parallelism awareness,” in Proceedings
debate,”arXivpreprintarXiv:2308.07201,2023. ofthe36thAnnualInternationalSymposiumonComputerArchitecture
[13] M.Chen,J.Tworek,H.Jun,Q.Yuan,H.P.deOliveiraPinto,J.Kaplan, (ISCA). ACM,2009,pp.152–163.
H.Edwards,Y.Burda,N.Joseph,G.Brockmanetal.,“Evaluatinglarge
|     |     |     |     |     |     |     | [32] J.-C. | Huang, | J. H. | Lee, H. Kim, | and | H.-H. S. | Lee, | “GPUMech: |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | ----- | ------------ | --- | -------- | ---- | --------- |
languagemodelstrainedoncode,”inarXivpreprintarXiv:2107.03374,
|     |     |     |     |     |     |     | GPU | performance | modeling | technique | based | on interval |     | analysis,” in |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --------- | ----- | ----------- | --- | ------------- |
2021. Proceedings of the 47th Annual IEEE/ACM International Symposium
[14] A.Chowdhery,S.Narang,J.Devlin,M.Bosma,G.Mishra,A.Roberts, onMicroarchitecture(MICRO). IEEE,2014,pp.268–279.
P.Barham,H.W.Chung,C.Sutton,S.Gehrmannetal.,“PaLM:Scaling [33] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and
language modeling with pathways,” in Journal of Machine Learning D. Zhou, “Large language models cannot self-correct reasoning yet,”
Research,vol.24,no.240,2023,pp.1–113.
2024.[Online].Available:https://arxiv.org/abs/2310.01798
| [15] K. Cobbe, | V.  | Kosaraju, | M. Bavarian, | M. Chen, | H. Jun, | L. Kaiser, |         |         |            |             |     |         |             |       |
| -------------- | --- | --------- | ------------ | -------- | ------- | ---------- | ------- | ------- | ---------- | ----------- | --- | ------- | ----------- | ----- |
|                |     |           |              |          |         |            | [34] A. | Ivanov, | N. Dryden, | T. Ben-Nun, | S.  | Li, and | T. Hoefler, | “Data |
M.Plappert,J.Tworek,J.Hilton,R.Nakanoetal.,“Trainingverifiers movement is all you need: A case study on optimizing transformers,”
tosolvemathwordproblems,”arXivpreprintarXiv:2110.14168,2021. in Proceedings of the International Conference on Machine Learning
[16] T. Dao, D. Fu, S. Ermon, A. Rudra, and C. Ré, “FlashAttention: Fast (MLSys),2021,pp.711–722.
andmemory-efficientexactattentionwithIO-awareness,”inProceedings [35] R. Jain, The Art of Computer Systems Performance Analysis. John
| of the | 36th Conference |     | on Neural | Information | Processing | Systems | Wiley&Sons,1991. |     |     |     |     |     |     |     |
| ------ | --------------- | --- | --------- | ----------- | ---------- | ------- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
(NeurIPS),2022,pp.16344–16359.
|     |     |     |     |     |     |     | [36] Z. Ji, | N. Lee, | R. Frieske, | T. Yu, | D. Su, | Y. Xu, E. | Ishii, | Y. J. Bang, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | ----------- | ------ | ------ | --------- | ------ | ----------- |
[17] N.Ding,M.Awan,andS.Williams,“Instructionroofline:Aninsightful A.Madotto,andP.Fung,“Surveyofhallucinationinnaturallanguage
visual performance model for gpus.” Lawrence Berkeley National generation,”inACMComputingSurveys,vol.55,no.12. ACM,2023,
| Laboratory | (LBNL), | Berkeley, | CA (United | States), | 01 2021. | [Online]. | pp.1–38. |     |     |     |     |     |     |     |
| ---------- | ------- | --------- | ---------- | -------- | -------- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- |
Available:https://www.osti.gov/biblio/1844927 [37] N. Kang, G. Yuan, Z. Yan, B. Zhang, B. Li, Z. Li, S. Wang,
[18] Y.Du,S.Li,A.Torralba,J.B.Tenenbaum,andI.Mordatch,“Improving G. Chen, J. Rao, Z. Wang, W. Jia, N. Sun, and G. Tan, “Md-pipe:
factualityandreasoninginlanguagemodelsthroughmultiagentdebate,” A strong scaling enhanced pipeline architecture for ab initio accuracy
in Proceedings of the International Conference on Machine Learning moleculardynamics,”inProceedingsofthe52ndAnnualInternational
(ICML),2024. Symposium on Computer Architecture, ser. ISCA ’25. New York,
12

NY,USA:AssociationforComputingMachinery,2025,p.1956–1968. [55] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe,
[Online].Available:https://doi.org/10.1145/3695053.3731052 U.Alon,N.Dziri,S.Prabhumoye,Y.Yangetal.,“Self-refine:Iterative
[38] J.Kaplan,S.McCandlish,T.Henighan,T.B.Brown,B.Chess,R.Child, refinement with self-feedback,” in Proceedings of the 37th Conference
S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws for neural onNeuralInformationProcessingSystems(NeurIPS),2023.
languagemodels,”arXivpreprintarXiv:2001.08361,2020. [56] D.Narayanan,M.Shoeybi,J.Casper,P.LeGresley,M.Patwary,V.Ko-
[39] T. S. Karkhanis and J. E. Smith, “A first-order superscalar processor rthikanti, D. Vainbrand, P. Kasber, H. Andriasyan, and B. Catanzaro,
model,”inProceedingsofthe31stAnnualInternationalSymposiumon “Efficient large-scale language model training on GPU clusters using
ComputerArchitecture(ISCA). IEEE,2004,pp.338–349. Megatron-LM,”inProceedingsoftheInternationalConferenceforHigh
[40] M. Khairy, Z. Shen, T. M. Aamodt, and T. G. Rogers, “Accel-sim: PerformanceComputing,Networking,StorageandAnalysis(SC),2021,
an extensible simulation framework for validated gpu modeling,” in pp.1–15.
ProceedingsoftheACM/IEEE47thAnnualInternationalSymposiumon [57] C.Nugteren,G.-J.vandenBraak,H.Corporaal,andH.Bal,“Adetailed
ComputerArchitecture,ser.ISCA’20. IEEEPress,2020,p.473–486. GPU cache model based on reuse distance theory,” in Proceedings of
[Online].Available:https://doi.org/10.1109/ISCA45697.2020.00047 the20thIEEEInternationalSymposiumonHighPerformanceComputer
[41] M.KianiandA.Rajabzadeh,“Efficientcacheperformancemodelingin Architecture(HPCA). IEEE,2014,pp.37–48.
GPUsusingreusedistanceanalysis,”ACMTransactionsonArchitecture [58] G. Ofenbeck, R. Steinmann, V. Caparros, D. G. Spampinato, and
andCodeOptimization(TACO),vol.15,no.4,pp.1–24,2018. M. Püschel, “Applying the roofline model,” in Proceedings of the
[42] H. Le, H. Chen, A. Saha, A. Gokul, D. Sahoo, and S. Joty, IEEEInternationalSymposiumonPerformanceAnalysisofSystemsand
“Codechain: Towards modular code generation through chain of self- Software(ISPASS). IEEE,2014,pp.76–85.
revisions with representative sub-modules,” 2024. [Online]. Available: [59] T.X.Olausson,J.P.Inala,C.Wang,J.Gao,andA.Solar-Lezama,“Is
https://arxiv.org/abs/2310.08992 self-repair a silver bullet for code generation?” in Proceedings of the
[43] J. Lee, Y. Ha, S. Lee, J. Woo, J. Lee, H. Jang, and Y. Kim, “GCoM: InternationalConferenceonLearningRepresentations(ICLR),2024.
AdetailedGPUcoremodelforaccurateanalyticalmodelingofmodern [60] S. Polu, J. M. Han, K. Zheng, M. Bousquet-Mélou, G. Lample, and
GPUs,”inProceedingsofthe49thAnnualInternationalSymposiumon C.Szegedy,“Formalmathematicsstatementcurriculumlearning,”arXiv
ComputerArchitecture(ISCA). ACM,2022,pp.424–436. preprintarXiv:2202.01344,2022.
[44] J. Lee, K. Choi, J. Lee, S. Lee, J. Whangbo, and J. Sim, “Neurex: [61] P.Ranganathan,D.Stodolsky,J.Calow,J.Dorfman,M.Guevara,C.W.
A case for neural rendering acceleration,” in Proceedings of the 50th Smullen IV, A. Kuusela, R. Balasubramanian, S. Bhatia, P. Chauhan,
Annual International Symposium on Computer Architecture, ser. ISCA A. Cheung, I. S. Chong, N. Dasharathi, J. Feng, B. Fosco, S. Foss,
’23. New York, NY, USA: Association for Computing Machinery, B.Gelb,S.J.Gwin,Y.Hase,D.-k.He,C.R.Ho,R.W.HuffmanJr.,
2023.[Online].Available:https://doi.org/10.1145/3579371.3589056 E.Indupalli,I.Jayaram,P.Kongetira,C.M.Kyaw,A.Laursen,Y.Li,
[45] G.Li,H.A.A.K.Hammoud,H.Itani,D.Khizbullin,andB.Ghanem, F. Lou, K. A. Lucke, J. Maaninen, R. Macias, M. Mahony, D. A.
“CAMEL: Communicative agents for “mind” exploration of large lan- Munday, S. Muroor, N. Penukonda, E. Perkins-Argueta, D. Persaud,
guagemodelsociety,”inProceedingsofthe37thConferenceonNeural A. Ramirez, V.-M. Rautio, Y. Ripley, A. Salek, S. Sekar, S. N.
InformationProcessingSystems(NeurIPS),2023. Sokolov,R.Springer,D.Stark,M.Tan,M.S.Wachsler,A.C.Walton,
[46] S. Li, J. H. Ahn, R. D. Strong, J. B. Brockman, D. M. Tullsen, D. A. Wickeraad, A. Wijaya, and H. K. Wu, “Warehouse-scale video
and N. P. Jouppi, “McPAT: An integrated power, area, and timing acceleration:co-designanddeploymentinthewild,”inProceedingsof
modeling framework for multicore and manycore architectures,” in the 26th ACM International Conference on Architectural Support for
Proceedings of the 42nd Annual IEEE/ACM International Symposium Programming Languages and Operating Systems, ser. ASPLOS ’21.
onMicroarchitecture(MICRO),2009,pp.469–480. New York, NY, USA: Association for Computing Machinery, 2021, p.
[47] W. Liang, Y. Iber, Y. Li, Z. Cao, L. Chen, T. Hashimoto, and J. Zou, 600–615.[Online].Available:https://doi.org/10.1145/3445814.3446723
“Canlargelanguagemodelsprovideusefulfeedbackonresearchpapers? [62] A.F.Rodrigues,K.S.Hemmert,B.W.Barrett,C.Kersey,R.Oldfield,
a large-scale empirical analysis,” in arXiv preprint arXiv:2310.01783, M. Weston, R. Risen, J. Cook, P. Rosenfeld, E. Cooper-Balis et al.,
2024. “The structural simulation toolkit,” ACM SIGMETRICS Performance
[48] W. Liang, Y. Zhang, Z. Cao, H. Xu, Y. Yu, D. Schwieterman, J. Z. EvaluationReview,vol.38,no.4,pp.37–42,2011.
Kolter,T.Goldstein,andT.Hashimoto,“Mappingtheincreasinguseof [63] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog,
LLMsinscientificpapers,”arXivpreprintarXiv:2404.01268,2024. M. Pranay Kumar, E. Dupont, F. J. R. Ruiz, J. S. Ellenberg,
[49] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, P. Wang, O. Fawzi et al., “Mathematical discoveries from program
J. Leike, J. Schulman, I. Sutskever, and K. Cobbe, “Let’s verify step search with large language models,” in Nature, vol. 625, 2024, pp.
by step,” in Proceedings of the International Conference on Learning 468–475.
Representations(ICLR),2024. [64] B.Rozière,J.Gehring,F.Gloeckle,S.Sootla,I.Gat,X.E.Tan,Y.Adi,
[50] T. Liu, X. Song, Z. Yue, R. Wen, X. Hu, Z. Song, Y. Wen, J. Liu, R. Sauvestre, T. Remez et al., “Code Llama: Open foundation
Y. Hao, W. Li, Z. Du, R. Zhang, J. Guo, D. Huang, S. Peng, modelsforcode,”inarXivpreprintarXiv:2308.12950,2023.
G. Sun, Q. Guo, and T. Chen, “Cambricon-sr: An accelerator [65] N. Samardzic, A. Feldmann, A. Krastev, S. Devadas, R. Dreslinski,
for neural scene representation with sparse encoding table,” in C.Peikert,andD.Sanchez,“F1:Afastandprogrammableaccelerator
Proceedingsofthe52ndAnnualInternationalSymposiumonComputer for fully homomorphic encryption,” in MICRO-54: 54th Annual
Architecture, ser. ISCA ’25. New York, NY, USA: Association IEEE/ACMInternationalSymposiumonMicroarchitecture,ser.MICRO
for Computing Machinery, 2025, p. 1254–1268. [Online]. Available: ’21. New York, NY, USA: Association for Computing Machinery,
https://doi.org/10.1145/3695053.3731018 2021,p.238–252.[Online].Available:https://doi.org/10.1145/3466752.
[51] K.Lo,L.L.Wang,M.Neumann,R.Kinney,andD.S.Weld,“S2ORC: 3480070
Thesemanticscholaropenresearchcorpus,”inProceedingsofthe58th [66] N. Samardzic, A. Feldmann, A. Krastev, N. Manohar, N. Genise,
AnnualMeetingoftheAssociationforComputationalLinguistics(ACL), S. Devadas, K. Eldefrawy, C. Peikert, and D. Sanchez, “Craterlake: a
2020,pp.4969–4983. hardwareacceleratorforefficientunboundedcomputationonencrypted
[52] C. Lu, C. Lu, R. T. Lange, J. Foerster, J. Clune, and D. Ha, “The AI data,” in Proceedings of the 49th Annual International Symposium
scientist: Towards fully automated open-ended scientific discovery,” in on Computer Architecture, ser. ISCA ’22. New York, NY, USA:
arXivpreprintarXiv:2408.06292,2024. Association for Computing Machinery, 2022, p. 173–187. [Online].
[53] H.Luo,A.Olgun,A.G.Yaglikci,Y.Kim,andO.Mutlu,“Ramulator Available:https://doi.org/10.1145/3470496.3527393
2.0: A modern, modular, and extensible DRAM simulator,” in IEEE [67] D. Sanchez and C. Kozyrakis, “ZSim: Fast and accurate microarchi-
ComputerArchitectureLetters,vol.22,no.2,2023,pp.101–104. tectural simulation of thousand-core systems,” in Proceedings of the
[54] W.Ma,Q.Xiong,X.Shi,X.Ma,H.Jin,H.Kuang,M.Gao,Y.Zhang, 40thAnnualInternationalSymposiumonComputerArchitecture(ISCA).
H. Shen, and W. Hu, “Gzkp: A gpu accelerated zero-knowledge proof ACM,2013,pp.475–486.
system,” in Proceedings of the 28th ACM International Conference [68] K. Sankaralingam, “Computer architecture’s alphazero moment:
on Architectural Support for Programming Languages and Operating Automateddiscoveryinanencircledworld,”2026.[Online].Available:
Systems, Volume 2, ser. ASPLOS 2023. New York, NY, USA: https://arxiv.org/abs/2604.03312
Association for Computing Machinery, 2023, p. 340–353. [Online]. [69] D. E. Shaw, M. M. Deneroff, R. O. Dror, J. S. Kuskin, R. H. Larson,
Available:https://doi.org/10.1145/3575693.3575711 J. K. Salmon, C. Young, B. Batson, K. J. Bowers, J. C. Chao, M. P.
13

Eastwood, J. Gagliardo, J. P. Grossman, C. R. Ho, D. J. Ierardi, [87] Y.ZhangandJ.D.Owens,“Aquantitativeperformanceanalysismodel
I.Kolossváry,J.L.Klepeis,T.Layman,C.McLeavey,M.A.Moraes, for GPU architectures,” in Proceedings of the 17th IEEE Interna-
R.Mueller,E.C.Priest,Y.Shan,J.Spengler,M.Theobald,B.Towles, tionalSymposiumonHighPerformanceComputerArchitecture(HPCA).
and S. C. Wang, “Anton, a special-purpose machine for molecular IEEE,2011,pp.382–393.
dynamics simulation,” Commun. ACM, vol. 51, no. 7, p. 91–97, Jul. [88] Y. Zhang, S. Wang, X. Zhang, J. Dong, X. Mao, F. Long,
2008.[Online].Available:https://doi.org/10.1145/1364782.1364802 C. Wang, D. Zhou, M. Gao, and G. Sun, “Pipezk: accelerating
[70] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, zero-knowledgeproofwithapipelinedarchitecture,”inProceedingsof
“Reflexion: Language agents with verbal reinforcement learning,” in the 48th Annual International Symposium on Computer Architecture,
Proceedingsofthe37thConferenceonNeuralInformationProcessing ser. ISCA ’21. IEEE Press, 2021, p. 416–428. [Online]. Available:
Systems(NeurIPS),2023. https://doi.org/10.1109/ISCA52012.2021.00040
[71] J. Sim, A. Dasgupta, H. Kim,and R. Vuduc, “A performance analysis [89] L.Zheng,W.-L.Chiang,Y.Sheng,S.Zhuang,Z.Wu,Y.Zhuang,Z.Lin,
frameworkforidentifyingpotentialbenefitsinGPGPUapplications,”in Z.Li,D.Li,E.P.Xingetal.,“JudgingLLM-as-a-judgewithMT-Bench
Proceedingsofthe17thACMSIGPLANSymposiumonPrinciplesand and chatbot arena,” in Proceedings of the 37th Conference on Neural
PracticeofParallelProgramming(PPoPP). ACM,2012,pp.11–22. InformationProcessingSystems(NeurIPS),2023.
[72] R.Taylor,M.Kardas,G.Cucurull,T.Scialom,A.Hartshorn,E.Saravia, [90] D. Zhu, R. Meng, Y. Song, X. Wei, S. Li, T. Pfister, and J. Yoon,
A. Poulton, V. Kerkez, and R. Stojnic, “Galactica: A large language “Paperbanana:Automatingacademicillustrationforaiscientists,”2026.
modelforscience,”arXivpreprintarXiv:2211.09085,2022. [Online].Available:https://arxiv.org/abs/2601.23265
[73] T.H.Trinh,Y.Wu,Q.V.Le,H.He,andT.Luong,“Solvingolympiad
geometrywithouthumandemonstrations,”inNature,vol.625,2024,pp.
476–482.
[74] Y. Turakhia, G. Bejerano, and W. J. Dally, “Darwin: A genomics co-
processorprovidesupto15,000xaccelerationonlongreadassembly,”
in Proceedings of the Twenty-Third International Conference on
Architectural Support for Programming Languages and Operating
Systems, ser. ASPLOS ’18. New York, NY, USA: Association
for Computing Machinery, 2018, p. 199–213. [Online]. Available:
https://doi.org/10.1145/3173162.3173193
[75] O.Villa,D.Lustig,Z.Yan,E.Bolotin,Y.Fu,N.Chatterjee,N.Jiang,
and D. Nellans, “Need for speed: Experiences building a trustworthy
system-levelGPUsimulator,”inProceedingsofthe27thIEEEInterna-
tionalSymposiumonHigh-PerformanceComputerArchitecture(HPCA).
IEEE,2021,pp.868–880.
[76] D. Wadden, S. Lin, K. Lo, L. L. Wang, M. van Zuylen, A. Cohan,
and H. Hajishirzi, “Fact or fiction: Verifying scientific claims,” in
Proceedingsofthe2020ConferenceonEmpiricalMethodsinNatural
LanguageProcessing(EMNLP),2020,pp.7534–7550.
[77] L.Wang,M.Jahre,A.Adileh,andL.Eeckhout,“MDM:TheGPUmem-
ory divergence model,” in Proceedings of the 53rd Annual IEEE/ACM
InternationalSymposiumonMicroarchitecture(MICRO). IEEE,2020,
pp.1089–1101.
[78] X. Wang, Y. Chen, L. Yuan, Y. Zhang, Y. Li, H. Peng, and H. Ji,
“Executable code actions elicit better LLM agents,” in Proceedings of
theInternationalConferenceonMachineLearning(ICML),2024.
[79] Y. Wang, Q. Guo, W. Yao, H. Zhang, X. Zhang, Z. Wu, M. Zhang,
X. Dai, M. Zhang, Q. Wen, W. Ye, S. Zhang, and Y. Zhang,
“Autosurvey:Largelanguagemodelscanautomaticallywritesurveys,”
2024.[Online].Available:https://arxiv.org/abs/2406.10252
[80] J.Wei,X.Wang,D.Schuurmans,M.Bosma,B.Ichter,F.Xia,E.Chi,
Q. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning
in large language models,” in Proceedings of the 36th Conference on
NeuralInformationProcessingSystems(NeurIPS),2022.
[81] S. Williams, A. Waterman, and D. Patterson, “Roofline: An insightful
visualperformancemodelformulticorearchitectures,”inCommunica-
tionsoftheACM,vol.52,no.4. ACM,2009,pp.65–76.
[82] D. Wright and I. Augenstein, “Citeworth: Cite-worthiness detection
for improved scientific document understanding,” in Findings of the
Association for Computational Linguistics: ACL-IJCNLP 2021, 2021,
pp.1796–1807.
[83] Q.Wu,G.Bansal,J.Zhang,Y.Wu,B.Li,E.Zhu,L.Jiang,X.Zhang,
S.Zhang,J.Liuetal.,“AutoGen:Enablingnext-genLLMapplications
viamulti-agentconversation,”inarXivpreprintarXiv:2308.08155,2023.
[84] K.Yang,A.M.Swope,A.Gu,R.Chalamala,P.Song,S.Yu,S.Godil,
R. Prenger, and A. Anandkumar, “LeanDojo: Theorem proving with
retrieval-augmentedlanguagemodels,”Proceedingsofthe37thConfer-
enceonNeuralInformationProcessingSystems(NeurIPS),2023.
[85] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and
K.Narasimhan,“Treeofthoughts:Deliberateproblemsolvingwithlarge
language models,” in Proceedings of the 37th Conference on Neural
InformationProcessingSystems(NeurIPS),2024.
[86] S.Yao,J.Zhao,D.Yu,N.Du,I.Shafran,K.Narasimhan,andY.Cao,
“ReAct:Synergizingreasoningandactinginlanguagemodels,”inPro-
ceedings of the International Conference on Learning Representations
(ICLR),2023.
14