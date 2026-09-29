Can Autonomous LLM Agents Execute Multireference Quantum Chemistry
Calculations?
Victor Chang Lee and James M. Rondinelli∗
Department of Materials Science and Engineering, Northwestern University, Evanston, IL, USA
(Dated: September 15, 2026)
Multireference electronic-structure calculations remain difficult to automate because critical
workflow decisions, including active-space selection, state averaging, convergence recovery, and state
identification, traditionally rely on expert judgment. Here, we investigate whether an autonomous
large language model (LLM) agent can perform these tasks without human intervention. The agent
selectsactivespacesusingliterature-groundedanalogiesorexplicitlydocumentedchemicalreasoning,
generatesandsubmitsORCAcalculations,analyzesoutputs,andrecordsalldecisionsinanauditable
reasoning log. Benchmarking against 558 vertical transition energies (VTEs) from QUESTDB shows
that an unguided baseline agent achieves 24.9% coverage with a mean absolute error (MAE) of
0.373 eV. Introducing a structured decision ladder increases coverage to 44.1% while reducing the
MAEto0.339eV.ThelargestgainsareobservedfordoubleandRydbergexcitations,demonstrating
that expert-informed procedural guidance substantially improves active-space construction and
state identification. When provided with complete workflow information, the agent successfully
reproduces published QUEST calculations with an MAE of only 23 meV, resolving 75% of target
configurationswithinsevenattempts. TheseresultsdemonstratethatcontemporaryLLMagentscan
autonomously execute and reproduce complex multireference quantum-chemical workflows, while
highlightingtheimportanceofstructuredreasoningframeworksforachievingreliablehigh-throughput
and high-fidelity electronic-structure calculations.
I. INTRODUCTION A primary bottleneck in applying multiconfigurational
methods at scale lies in determining which electrons and
In recent years, the generation of large-scale computa- orbitals need to be treated explicitly within the corre-
tional databases has emerged as a major breakthrough in lated wavefunction [14]. Omitting essential orbitals fails
materials research and molecular chemistry. At the first- to capture critical static correlation, whereas an exces-
principles level, density functional theory (DFT) serves sively large active space rapidly becomes computationally
as the primary method for data generation [1–3]. Ben- intractable. Traditionally, active space selection relies
efiting from standardized computational pipelines that on manual choices grounded in chemical intuition and
are straightforward to automate, along with a reasonable literature precedents; it is also often biased towards a
computational cost, DFT has enabled high-throughput particular property of interest, presenting a major barrier
databases that collectively span millions of systems, such to the large-scale generation of high-accuracy data for
as Meta FAIR’s OMol25 [4], the Materials Project [5], multiple or yet specified purposes.
and the Open Quantum Materials Database (OQMD) [6], To minimize reliance on user intervention, several auto-
among others. However, standard exchange-correlation mated selection protocols have been introduced [14]. The
functionals to DFT fail systematically when static elec- two prominent examples are the atomic valence active
tron correlation is strong, impacting predictive capability space (AVAS) and AutoCAS [15–18]. The former uses a
of excited states [7], d- and f-block complexes [8, 9], di- setofatomicorbitals(AO)ofaminimalbasissetthatare
radicals, bioinorganic active sites [10], and photochemical sufficient to qualitatively represent the final CASSCF ac-
reaction paths [11]. tiveorbitalswhilethelateruseslarge-active-spacedensity
Multiconfigurational (multireference) electronic struc- matrix renormalization group (DMRG) [19] calculations
ture methods, such as the Complete Active Space Self- to identify orbitals characterized by strong correlation.
Consistent Field (CASSCF) [12, 13], more accurately Other efforts have tailored active space automation to
describe these strongly correlated regimes. The so-called high-throughput workflows and machine learning (ML)
active space in CASSCF is a subset of electrons and applications. To that end, Gagliardi and coworkers de-
orbitals that are optimized using a full configuration it- veloped an automated protocol for molecular dynamics
eration (FCI) to obtain the configuration iteration (CI) and ML potentials that generates initial active space
coefficients and the multiconfigurational wave function. guesses by interpolating molecular orbital coefficient ma-
To account for remaining dynamic correlation, CASSCF tricesfrompreviouslyoptimizedwavefunctions[20]. More
calculations are refined using multireference perturbative recently, the same group developed an automated algo-
methods. One of the most prominent approaches is the rithmforhigh-throughputmagneticpropertycalculations
N-electron valence state perturbation theory (NEVPT2). of lanthanides complexes [21].
Recent advances in large language models (LLMs) of-
fer a promising pathway to overcome this bottleneck.
LLMs have demonstrated rapid improvements in techni-
∗ jrondinelli@northwestern.edu
6202
peS
11
]hp-mehc.scisyhp[
1v75331.9062:viXra

2
calreadingcomprehension,structuredinformationextrac-
LLM Agent
tion, and scientific reasoning [22–24]. In computational
chemistry, LLMs have been studied as tools for molec- AIMdb
ular structure generation and prediction [25, 26]. More Execution
Input
recently, LLM agents have recently been suggested for
ORCA
multireference computational chemistry tasks [27]. How- Molecular Claude Opus 5 code CASSCF
structure Results
ever, the full extent of their operational autonomy and
decision making fidelity has not been systematically eval- Tools
ORCA Decision
uated. Moving beyond static script generation or simple Manual Ladder Python
code execution requires quantifying how effectively an SLURM
Guide
agentcanindependentlyhandlenon-trivialchemicaljudg-
ments, including active-space selection, state-averaging
schemes, and dynamic failure recovery, especially when FIG. 1. Overview of the autonomous LLM agent workflow
confronted with challenging electronic structures. Lever- for quantum chemical calculations. Input molecular struc-
tures, along with reference documentation (ORCA manual
aging these capabilities, we benchmark an autonomous
and SLURM workload manager guide), are passed to the core
LLM agent on executing complex multiconfigurational
agentpoweredbyClaudeOpus5. Theagentinteractswithan
CASSCF calculations. By combining literature-derived
internal database (AIMdb) and operates under a structured
domain context with dynamic decision scaffolding, the
decisionladdertoguideexecutionlogic. Duringexecution,the
agent autonomously selects active spaces, constructs and agent leverages Python scripting tools, consults its knowledge
executes a quantum chemistry software package. This sources to generate CASSCF results.
frameworkallowsustosystematicallyevaluatetheagent’s
ability to exercise expert-level chemical judgment, estab-
lishing both its baseline predictive accuracy and the key B. Knowledge Sources
challenges in scaling autonomous multiconfigurational
workflows. Benchmarking LLM-guided workflows is challenging
because undisclosed training data can introduce data-
contaminationeffects[29]. Tomitigatethisrisk,wesupply
II. AGENT ARCHITECTURE AND theagentwithacuratedreferencedatabaseandexplicitly
BENCHMARK DESIGN instruct it to exclude any prior knowledge or literature
precedents contained in QUESTDB [30]. The literature
A. Overview database was extracted from AIMdb [31], and is searched
using the compound name or formula, metal center, d/f
As illustrated in Figure 1, the autonomous LLM de- electroncount,andligandenvironmentwhenatransition-
cision agent operates as a transparent reasoning engine metal or lanthanide/actinide center is present. For each
rather than a black-box automation pipeline. The agent matching entry, the agent retrieves the active-space size,
evaluates each molecule’s geometry, consults a curated orbitaldescription, computationalprotocol, multiplicities,
literature database, constructs and submits ORCA v6.1 method, and associated citation.
[28] inputs. In CASSCF calculations, a geometry file Analogical reasoning is defined narrowly and explicitly
alone is insufficient to start a calculation; it requires, at in the agent policy. For a transition-metal and f-electron
minimum, the electron/orbital counts of the active space, complex, a literature precedent is considered analogous
the multiplicities to compute, and the number of roots only when it shares the same metal, oxidation state, and
per multiplicity. These initial selections are informed by coordination environment. For organic and main-group
the knowledge sources provided to the model (see below). systems, analogy requires the same functional group and
The LLM agent dynamically constructs the Python tools conjugation pattern. Every active-space recommenda-
it deems necessary to complete its assigned task. To tion derived from an analogous precedent must cite the
that end, the LLM agent makes all substantive chemistry corresponding database entry. When no genuinely anal-
decisionsandrecordsitsreasoninginanappend-only,per- ogous examples are found, the agent policy defaults to
molecule audit log. The escalation logic (decision ladder) sizing the active space directly from general quantum-
is kept strictly advisory and is never automatically exe- chemical principles. The resulting record is explicitly
cuted. This design choice, enforced in code, stems from tagged so that readers can distinguish literature-based
the realization that per-molecule quantum chemical judg- from agent-derived choices throughout the workflow and
ment requires dynamic reasoning that static programs in all downstream data exports.
cannot provide. When the target active orbitals can be specified in
terms of atomic orbitals (AOs), the policy requires build-
ing the active space using the Atomic Valence Active
Space (AVAS) approach rather than specifying explic-
itly the electron/orbital counts (n , n ) and allowing
el orb
ORCA to populate the window strictly from the orbital-

3
| energy | frontier | [15, 16]. | Because | AVAS | derives |     | the active | 2.           |     |     |                           |     |     |     |      |
| ------ | -------- | --------- | ------- | ---- | ------- | --- | ---------- | ------------ | --- | --- | ------------------------- | --- | --- | --- | ---- |
|        |          |           |         |      |         |     |            | Ground-state |     |     | configuration-interaction |     |     |     | (CI) |
space from chemically motivated AO targets, agreement weight: Theweight ofthedominantelectroniccon-
with cited active-space sizes provides confidence in the figuration is monitored as a measure of static cor-
selected space, while disagreements prompt additional relation. A leading configuration with a CI weight
examination of the orbital content and space definition. approaching unity indicates that the active space
|     |     |            |     |           |     |       |     | is contributing |             | little    | to  | the wave    | function  |          | and that   |
| --- | --- | ---------- | --- | --------- | --- | ----- | --- | --------------- | ----------- | --------- | --- | ----------- | --------- | -------- | ---------- |
|     |     |            |     |           |     |       |     | the             | calculation | may       | be  | effectively |           | single   | reference. |
|     |     |            |     |           |     |       |     | Rather          | than        | applying  |     | a fixed     | universal |          | threshold, |
|     | C.  | Governance |     | and Audit |     | Trail |     |                 |             |           |     |             |           |          |            |
|     |     |            |     |           |     |       |     | the             | policy      | evaluates | the | ground      | state     | dominant | CI         |
Allchemicalandtechnicaldecisionsaredelegatedtothe weights relative to normally correlating attempts
|                                         |     |      |             |     |            |     |            | for that | molecule. |     |     |     |     |     |     |
| --------------------------------------- | --- | ---- | ----------- | --- | ---------- | --- | ---------- | -------- | --------- | --- | --- | --- | --- | --- | --- |
| LLMagentwithoutrequiringahumanapproval. |     |      |             |     |            |     | However,   |          |           |     |     |     |     |     |     |
| every decision                          |     | must | be grounded | in  | literature |     | precedent, |          |           |     |     |     |     |     |     |
3.
the escalation ladder, or explicitly-flagged chemical in- Irreducible representation (irrep) distribu-
tuition, and logged with reasoning to a per-molecule, in tion: The symmetry distribution of active orbitals
|              |         |             |            |             |            |          |            | is compared |          | with       | the intended |          | active-space. |                  | Agree-     |
| ------------ | ------- | ----------- | ---------- | ----------- | ---------- | -------- | ---------- | ----------- | -------- | ---------- | ------------ | -------- | ------------- | ---------------- | ---------- |
| append-only  |         | files.      |            |             |            |          |            |             |          |            |              |          |               |                  |            |
|              |         |             |            |             |            |          |            | ment        | in the   | total      | number       | of       | orbitals      | is insufficient; |            |
| The          | agent   | is required | to         | stop        | and flag   | a        | particular |             |          |            |              |          |               |                  |            |
|              |         |             |            |             |            |          |            | the         | orbitals | must       | also occupy  |          | the correct   |                  | irreps and |
| calculation  | for     | four        | categories | only:       | a          | genuine  | give-up    |             |          |            |              |          |               |                  |            |
|              |         |             |            |             |            |          |            | correspond  |          | to the     | intended     | chemical |               | subspace.        | An         |
| condition    | (the    | attempt     | budget     | exhausted   |            | with     | every dis- |             |          |            |              |          |               |                  |            |
|              |         |             |            |             |            |          |            | apparently  |          | correct    | irrep        | can      | still arise   | from             | an ac-     |
| tinct action |         | tried and   | recorded), |             | literature | conflict | too        |             |          |            |              |          |               |                  |            |
|              |         |             |            |             |            |          |            | tive        | space    | containing | orbitals     |          | of incorrect  |                  | chemical   |
| large to     | explain | (Rule       | F,         | see below), |            | anything | resem-     |             |          |            |              |          |               |                  |            |
character.
| bling data     | corruption |           | and      | infrastructure |              | failure   | outside |               |           |            |         |                  |         |     |           |
| -------------- | ---------- | --------- | -------- | -------------- | ------------ | --------- | ------- | ------------- | --------- | ---------- | ------- | ---------------- | ------- | --- | --------- |
| the ladder’s   |            | scope.    | No early | stopping       |              | condition | exists  | 4.            |           |            |         |                  |         |     |           |
|                |            |           |          |                |              |           |         | Orbital       | indices   |            | and     | CI-configuration |         |     | posi-     |
| for a repeated |            | diagnosis | and      | a recurring    |              | failure   | mode is |               |           |            |         |                  |         |     |           |
|                |            |           |          |                |              |           |         | tions:        | Molecular |            | orbital | (MO)             | indices |     | and CI-   |
| explicitly     | defined    | as        | evidence | that           | the previous |           | fix was |               |           |            |         |                  |         |     |           |
|                |            |           |          |                |              |           |         | configuration |           | identifies |         | are valid        | only    | for | the exact |
wrong, not that the molecule is intractable. The decision wave-function state that generated it. Because or-
| ladder          | enumerates | the   | number   | of        | genuinely | distinct   | ac-    |         |              |     |     |         |           |           |        |
| --------------- | ---------- | ----- | -------- | --------- | --------- | ---------- | ------ | ------- | ------------ | --- | --- | ------- | --------- | --------- | ------ |
|                 |            |       |          |           |           |            |        | bital   | ordering     | and | CI  | string  | positions | can       | change |
| tions available |            | under | a single | diagnosis |           | to clarify | that a |         |              |     |     |         |           |           |        |
|                 |            |       |          |           |           |            |        | between | optimization |     |     | stages, | state     | averages, | and    |
diagnosis is rarely exhausted after two or three attempts. restarted calculations, the policy requires contin-
Overruling the ladder or a cited literature entry is uous verification of orbital indices and CI string
| permitted   | but        | carries           | three    | obligations:  |           |              |         |               |                |            |             |               |              |           |          |
| ----------- | ---------- | ----------------- | -------- | ------------- | --------- | ------------ | ------- | ------------- | -------------- | ---------- | ----------- | ------------- | ------------ | --------- | -------- |
|             |            |                   |          |               |           |              |         | positions     | at             | every      | decision    | point.        | Historical   |           | index    |
|             |            |                   |          |               |           |              |         | lists         | are never      | assumed    |             | to remain     |              | valid,    | as doing |
| 1. State    | explicitly |                   | what     | is being      | overruled | and          | provide |               |                |            |             |               |              |           |          |
|             |            |                   |          |               |           |              |         | so can        | lead           | to orbital |             | rotations,    | active-space |           | mod-     |
| the         | rational   | for               | doing    | so.           |           |              |         |               |                |            |             |               |              |           |          |
|             |            |                   |          |               |           |              |         | ifications,   |                | or state   | assignments |               | being        | applied   | to       |
|             |            |                   |          |               |           |              |         | unintended    |                | targets.   |             |               |              |           |          |
| 2. Ground   |            | the override      |          | in something  |           | that         | can be  |               |                |            |             |               |              |           |          |
| checked     |            | against           | the same | output        | (e.g.,    | composition, |         |               |                |            |             |               |              |           |          |
| occupation, |            | symmetry,         |          | etc.).        |           |              |         |               |                |            |             |               |              |           |          |
|             |            |                   |          |               |           |              |         |               |                | E.         | Decision    | ladder        |              |           |          |
| 3. Document |            | the               | override | appropriately |           | rather       | than    |               |                |            |             |               |              |           |          |
| framing     |            | it as established |          | precedent.    |           |              |         |               |                |            |             |               |              |           |          |
|             |            |                   |          |               |           |              |         | The decision  |                | ladder     | defines     | a prioritized |              | hierarchy | of       |
|             |            |                   |          |               |           |              |         | corrective    | and diagnostic |            | actions     | used          | by           | the agent | when     |
|             |            |                   |          |               |           |              |         | a calculation | deviates       |            | from        | the desired   |              | outcome.  | The      |
D. Convergence criteria rulesareevaluatedsequentiallyfromhighesttolowestpri-
|     |     |     |     |     |     |     |     | ority, ensuring | that | fundamental |     | execution |     | and | numerical |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | ---- | ----------- | --- | --------- | --- | --- | --------- |
TodeterminedwhetheraCASSCFcalculationhasboth issues are resolved before chemically motivated refine-
numerically converged and produced a physically mean- ments are considered. Rather than serving as rigid, hard-
ingful wave function, the agent is required to evaluate coded constraints, the ladder functions as a collection of
four independent validation criteria: expert-informed heuristics and policy recommendations
|     |     |     |     |     |     |     |     | that guide | autonomous |     | decision-making |     | while | preserving |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | --- | --------------- | --- | ----- | ---------- | --- |
1.
Total energy relative to Hartree-Fock (HF): flexibility across diverse chemical systems.
| The | CASSCF | energy |     | is compared | against |     | the corre- |     |     |     |     |     |     |     |     |
| --- | ------ | ------ | --- | ----------- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
sponding HF energy obtained with the same molec- • Rule A: Job execution failure. Detect and
ular geometry and basis set. For a given state, the resolve scheduler- or infrastructure-level failures,
CASSCF energy should generally be lower than including SLURM submission errors, node failures,
the HF reference. Although state-averaged calcula- wall-time limits, and missing output files.
| tions | spanning |     | many | roots may | occasionally |     | yield |     |     |     |     |     |     |     |     |
| ----- | -------- | --- | ---- | --------- | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
energies slightly above the HF value, substantial in- • Rule B: SCF non-convergence. Addressfailures
|             |     |          |                |                  |         |              |        | of the        | underlying |             | Hartree–Fock |        | procedure |             | through |
| ----------- | --- | -------- | -------------- | ---------------- | ------- | ------------ | ------ | ------------- | ---------- | ----------- | ------------ | ------ | --------- | ----------- | ------- |
| creases     |     | indicate | an incorrectly |                  | defined | active       | space, |               |            |             |              |        |           |             |         |
|             |     |          |                |                  |         |              |        | appropriate   |            | convergence |              | aids,  | restart   | strategies, | or      |
| convergence |     | failure, |                | or wave-function |         | instability. |        |               |            |             |              |        |           |             |         |
|             |     |          |                |                  |         |              |        | modifications |            | to          | the initial  | guess. |           |             |         |

4
• Rule C: CASSCF non-convergence. Remedy When an incorrect active-space composition is iden-
failures of the multiconfigurational optimization, tified, the primary corrective action is orbital rotation.
including problematic orbital rotations, inadequate Orbital rotations are used to bias the calculations toward
active spaces, or unstable state averaging. a targetelectronic stateby exchanging pairs ofMOs from
apreviouscalculation. Withinthedecisionladder,orbital
• Rule D: Convergence to an incorrect elec- rotation is treated as a core state-targeting mechanism
tronic state. Identify situations in which the cal- ratherthanaposthocworkaround. Tomaintainphysical
culation converges formally but yields a chemically
consistency, however, rotations are strictly constrained
incorrectsolution,suchasanunintendedoccupation
from converged orbitals. Furthermore, when point-group
pattern, spin state, or orbital character.
symmetry is enabled, rotations must strictly preserve spa-
tial symmetry by operating within individual irreps. To
• Rule E: Incomplete correlation treatment.
further prevent active-space drift, this rule pairs orbital
Recognize cases where convergence is achieved but
rotations are coupled with level shifting and adaptive
the selected active space or state-averaging win-
solver-selection strategies that stabilize retention of the
dow is insufficient to capture the relevant electronic
intended active-space manifold.
structure.
• Rule F: Strong disagreement with literature
precedent. Compare converged results with analo- Rule E: Clean convergence with an Incomplete Correlation
gous literature benchmarks and investigate signifi- Space or Truncated Energy-root Window
cantdiscrepanciesinactive-spacecomposition,state
ordering, or qualitative electronic structure. A CASSCF calculation may converge smoothly with
a modest number of active electrons, orbitals, and state-
• Rule G: Rydberg or diffuse-state contamina- averaged roots yet still fail to provide an adequate de-
tion. Detectandappropriatelytreatdiffuseexcited scription of the electronic structure. Such cases arise
states that may require specialized basis functions, when the active space is too small to capture the relevant
enlarged active spaces, or revised state-selection correlation effects or when the state-averaging window
strategies. excludes energetically accessible states that influence the
target solution. Rule E therefore probes the complete-
• Rule H: Successful completion. Confirm that
ness of both the active space and the root window. For
the calculation has converged, the active orbitals
active-space validation, the agent examines the natural
possess the intended chemical character, orbital oc-
orbital occupation numbers (NOONs), paying particular
cupations are physically reasonable, and the results
attention to the least occupied active orbital. A small
are consistent with available literature expectations.
but non-negligible occupation suggests that additional
correlating orbitals may be contributing to the wave func-
The agent’s ability to make chemically and physically
tion. In response, the subsequent calculation expands the
informed calculations is concentrated within Rules D, E,
active space and records the occupations of the newly
and G, which address scenarios where formal numerical
introduced orbitals. The decision to retain the larger
convergence alone is insufficient to guarantee a physically
active space is based on the observed occupation pattern,
meaningful wave function. These rules, described below,
e.g., mutual degeneracy, rather than a fixed threshold.
govern incorrect electronic states, incomplete correlation
Selection of the state-averaging window is governed by
treatment, and diffuse-state character.
the energetic and symmetry relationships among the tar-
get states rather than by an arbitrary root count. When
near-degenerate states are present, the window is ex-
Rule D: Convergence to an Incorrect Electronic State
panded to ensure a balanced description of the relevant
electronic manifold. Further expansion is constrained
During orbital optimization, the solver can gradually
by available literature precedent and chemical justifica-
rotate a physically relevant active orbital into the inac-
tion. Beyond this regime, the policy favors performing
tive or virtual space while simultaneously replacing it
separate calculations for distinct sets of states instead of
with an unintended orbital. Consequently, the calcula-
indefinitely widening a single state-averaged calculation.
tion may formally converge, yet the final active space
Excessively large state-averaging windows can degrade
can differ substantially from the intended one and con-
the quality of the optimized molecular orbitals, as the
tain orbitals with incorrect chemical character. To detect
orbitals must simultaneously accommodate an increas-
such failures, Rule D performs a comprehensive orbital-
ingly diverse set of electronic states. Consistent with this
composition analysis based on three complementary di-
expectation, calculations performed with narrow state-
agonistics: natural orbital occupation numbers (NOON),
averaging windows typically yield slightly lower energies
L¨owdin orbital decomposition analysis, and geometric
for a given target state than otherwise identical calcula-
atomic-contribution analysis. Together, these metrics as-
tions employing much broader root windows.
sess both the correlation character and chemical identity
of the active orbitals.

5
|     |     | CLAUDE.md           |     |     |     |     | TASK.md           |     |     |     | /runs/ & /logs/    |     |     |     |
| --- | --- | ------------------- | --- | --- | --- | --- | ----------------- | --- | --- | --- | ------------------ | --- | --- | --- |
|     |     | Agent Configuration |     |     |     |     | Execution control |     |     |     | Outputs & Verdicts |     |     |     |
Calculation directories
|     |     | Limit: 150k Characters |     |     |     |     | Set objectives & limits |     |     |     |                      |     |     |     |
| --- | --- | ---------------------- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | -------------------- | --- | --- | --- |
|     |     | Core Purpose           |     |     |     |     | Loop control            |     |     |     | Results & reasonings |     |     |     |
/runs/
|     |     | Decision ladder |     |     |     |     | • Reopen     |     |     |     |                  |     |     |     |
| --- | --- | --------------- | --- | --- | --- | --- | ------------ | --- | --- | --- | ---------------- | --- | --- | --- |
|     |     |                 |     |     |     |     | periodically |     |     |     | • ORCA inputs &  |     |     |     |
|     |     | • Guidance      |     |     |     |     |              |     |     |     | Outputs          |     |     |     |
• Prompt to re-read
|     |     | • Systematic Checks |     |     |     |     |     |     |     |     | • Verdicts.md files |     |     |     |
| --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- |
CLAUDE.md
/logs/
• Prevent context
loss
• decisions.csv
• results.csv
Evidence.md
Supporting information
FIG.2. Agentarchitectureoverviewshowinginteractionsbetweenagentconfiguration(CLAUDE.mdandEvidence.md),execution
loop control (TASK.md), and output directories containing calculation runs (/runs/) and structured verdict logs (/logs/).
|     |      |     |         |           |        |     |     | retaining | the quantitative |     | accuracy | of  | the final | correlated |
| --- | ---- | --- | ------- | --------- | ------ | --- | --- | --------- | ---------------- | --- | -------- | --- | --------- | ---------- |
|     | Rule | G:  | Rydberg | (diffuse) | states |     |     |           |                  |     |          |     |           |            |
treatment.
| The preceding        |     | rules        | are designed |         | to identify |              | deficien- |     |     |     |     |     |     |     |
| -------------------- | --- | ------------ | ------------ | ------- | ----------- | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- |
| cies in active-space |     | composition, |              | orbital |             | occupations, | and       |     |     |     |     |     |     |     |
stateselection;however,theyarenotsufficientforreliably F. Agent Implementation
| detectingRydbergexcitations. |        |                   |     | Unlikevalenceexcitations, |           |     |           |            |     |        |       |              |     |              |
| ---------------------------- | ------ | ----------------- | --- | ------------------------- | --------- | --- | --------- | ---------- | --- | ------ | ----- | ------------ | --- | ------------ |
|                              |        |                   |     |                           |           |     |           | The Claude |     | Opus 5 | model | was deployed |     | using a mod- |
| Rydberg                      | states | are distinguished |     |                           | primarily | by  | the large |            |     |        |       |              |     |              |
spatial extent and diffuse character of the orbitals in- ular instruction architecture (Figure 2). Claude Code
volved rather than by their occupation patterns alone. initializeseachagentsessionfromaCLAUDE.mdfile,which
Consequently, identifying such states requires explicit definesthesysteminstructionsandoperationalframework
analysis of orbital diffuseness in addition to conventional governing the agent’s behavior. In practice, however, the
active-space diagnostics. size of this file is constrained, with performance often
To address this limitation, the policy employs degrading as the instruction set grows beyond approxi-
|        |                      |     |     |        |       |            |     | mately150,000characters. |     |     | Furthermore, |     | duringextended |     |
| ------ | -------------------- | --- | --- | ------ | ----- | ---------- | --- | ------------------------ | --- | --- | ------------ | --- | -------------- | --- |
| ORCA’s | multiconfigurational |     |     | random | phase | approxima- |     |                          |     |     |              |     |                |     |
tion (MCRPA) linear-response module using a converged execution, newly generated content progressively occu-
CASSCF reference wave function. MCRPA is used exclu- pies the context window (capped at 1 million tokens),
|           |              |     |         |          |           |     |         | increasing | the | risk that | critical | instructions, |     | policy de- |
| --------- | ------------ | --- | ------- | -------- | --------- | --- | ------- | ---------- | --- | --------- | -------- | ------------- | --- | ---------- |
| sively as | a diagnostic |     | tool to | identify | candidate |     | excited |            |     |           |          |               |     |            |
states and the orbitals that contribute to them. Be- tails, or reasoning guidance will receive less attention or
cause MCRPA excitation energies are obtained within be displaced from the model’s active context.
a CASSCF linear-response framework, they do not re- To improve instruction persistence and reduce context-
|           |         |             |     |              |     |          |     | management | failures, |     | the agent | architecture |     | separates |
| --------- | ------- | ----------- | --- | ------------ | --- | -------- | --- | ---------- | --------- | --- | --------- | ------------ | --- | --------- |
| cover the | dynamic | correlation |     | subsequently |     | captured | by  |            |           |     |           |              |     |           |
NEVPT2 and are therefore not used for reporting final information across three specialized files:
| excitation     | energies. |          |      |      |             |     |            |              |     |                                     |     |     |     |     |
| -------------- | --------- | -------- | ---- | ---- | ----------- | --- | ---------- | ------------ | --- | ----------------------------------- | --- | --- | --- | --- |
|                |           |          |      |      |             |     |            | • CLAUDE.md: |     | Definesthesystemcontext,operational |     |     |     |     |
| Once candidate |           | orbitals | have | been | identified, |     | their dif- |              |     |                                     |     |     |     |     |
boundaries,andcorepolicies(includingthedecision
| fuse character                    |          | is quantified |     | by evaluating |                  | the      | smallest |            |     |         |           |          |       |               |
| --------------------------------- | -------- | ------------- | --- | ------------- | ---------------- | -------- | -------- | ---------- | --- | ------- | --------- | -------- | ----- | ------------- |
|                                   |          |               |     |               |                  |          |          | ladder     | and | ORCA’s  | manual    | checks). |       |               |
| Gaussian                          | exponent | associated    |     | with          | the              | relevant | atomic   |            |     |         |           |          |       |               |
| centerandangular-momentumchannel. |          |               |     |               | Orbitalswithsig- |          |          |            |     |         |           |          |       |               |
|                                   |          |               |     |               |                  |          |          | • TASK.md: |     | Manages | execution |          | state | and objective |
nificant contributions from highly diffuse basis functions tracking, forcing the agent to re-read system in-
| are classified | as  | Rydberg | candidates |     | and | ranked | accord- |            |     |         |           |       |     |     |
| -------------- | --- | ------- | ---------- | --- | --- | ------ | ------- | ---------- | --- | ------- | --------- | ----- | --- | --- |
|                |     |         |            |     |     |        |         | structions |     | at each | iteration | loop. |     |     |
ingly. Theidentifieddiffuseorbitalsarethenincorporated
intoanexpandedactivespace,afterwhichthetargetstate • EVIDENCE.md: Serves as an auxiliary knowledge
is recomputed using SA-CASSCF followed by NEVPT2. store, holding detailed reasoning, supporting con-
This procedure enables the agent to describe Rydberg text, and rule-specific justifications for the primary
states within a physically meaningful active space while policies in CLAUDE.md.

6
FIG. 3. Framework for evaluating LLM agents performance across varying levels of domain context. The benchmark progresses
along a gradient of model knowledge from minimal contextual information to extensive domain-specific guidance, enabling
systematic assessment of replication fidelity and agent reliability. (DB: Database; VTE: Vertical transition energies; SA: State
Average)
Thisseperationminimizescompetitionforcontext-window calculations, we benchmarked the workflow against the
resources, improves retention of critical operational poli- vertical transition energy (VTE) dataset contained in
cies, and provides a scalable framework for long-running QUESTDBusingonlythemolecularstructurefiles. Three
autonomous calculations. information regimes were considered (Figure 3)
1. Baseline model: Access to the ORCA documen-
tation and the literature database only.
III. COMPUTATIONAL METHODS
2. Decision model: The Baseline model supple-
Complete active space self-consistent field (CASSCF) mented with the decision ladder described in Sec-
calculations followed by strongly contracted N-electron tion IIE.
valencestateperturbationtheory(SC-NEVPT2)wereper-
formedusingtheORCAv6.1softwarepackage[28,32,33]. 3. Replication model: Access to all available
For all calculations, the aug-cc-pVTZ basis set was em- QUESTDB knowledge, including all information
ployed,consistentwiththedefaultprotocolofQUESTDB. required to reproduce published calculations.
To accelerate the calculation of two-electron integrals,
These three tiers define a controlled knowledge gradient,
the resolution-of-identity chain-of-spheres exchange (RI-
ranging from general quantum-chemistry resources to
JCOSX) approximation was utilized [34] together with
completetask-specificinformation. Thisframeworkallows
auxiliary basis sets automatically generated via ORCA’s
the effects of domain context on agent performance to be
AutoAux feature. Active space construction and orbital
isolated and quantified.
selection were governed autonomously by an LLM agent
workflow powered by Anthropic’s Claude Opus 5 model The Baseline model establishes the capabilities of
an essential unguided LLM agent operating with access
[35].
only to standard software documentation and literature
To evaluate the autonomous decision-making perfor-
precedents. The ORCA manual provides methodological
mance of the agent, a curated benchmark set of 84
and implementation details, while the literature database
molecules was selected from the 2025 QUESTDB[30]
supplies externally grounded examples of active spaces,
obtained with similar CASSCF/SC-NEVPT2 proto-
stateselections,andcomputationalprotocols. Thisdesign
col. Although the reference benchmark calculations
also serves as a partial control for potential training-data
in QUESTDB were generated using MolPro [36], all
contamination, allowing decisions supported by explicit
CASSCF/SC-NEVPT2 calculations in this work were
literature retrieval to be distinguished from those de-
executed using the ORCA v6.1 software package to align
rived from the model’s internal chemical reasoning [31].
with our local computational workflow.
Acrossthebenchmarkset,theagentidentifieddirectliter-
ature analogues for the vast majority of molecules. Only
four molecules from the QUESTDB benchmark dataset
IV. RESULTS AND DISCUSSION
were deemed dissimilar from available precedents that
active-space selection and state-averaging choices were
A. Benchmark Framework
were based primarily on chemical intuition rather that
literature-grounded analogy [37–134].
To evaluate the ability of the LLM agent to au-
The Decision model augments the Baseline model
tonomously perform multireference electronic-structure
withadecisionladder,providingastructuredsetofexpert-

7
informed policies for diagnosing and correcting common
14
failures in mulitreference calculation workflows. Impor-
tantly, the decision ladder neither overrides the LLM’s
intrinsic reasoning process nor prescribes specific calcu-
12
lation inputs; it also does not have final authority over
task-level decisions. Instead, it supplies procedural guid-
ance while leaving final decisions to the agent, thereby 10
isolating the value of formalized domain expertise inde-
pendent of detailed task-specific instructions.
8
Finally, the Replication model provides the agent
withallworkflowinformationtoreproducetheQUESTDB
results, including access to their repository resources, 6
calculation protocols, and supporting and documentation.
This regime represents an upper bound on the contextual
4
informationavailabletotheagentandevaluatesitsability
to reproduce published multireference calculations when
complete domain knowledge is accessible. 2
0
B. Impact of the Decision Ladder 0 2 4 6 8 10 12 14
Reference SC-NEVPT2 (eV)
To quantify the role of structural domain guidance, we
compare the performance of the Baseline and Decision
models for predicting VTEs from molecular structures
using CASSCF/SC-NEVPT2. Statistical error metrics,
including the mean absolute error (MAE) and coefficient
of determination (R2), were computed exclusively for
VTEswhoseidentityagainstthereferencecouldbeunam-
biguouslyverifiedagainstthereferencebenchmark. VTEs
identified solely by energy ordering or those belonging
to a manifold of degenerate/near-degenerate states with
ambiguousassignmentswereexcludedfromtheerroranal-
ysis and classified as unidentified. Consequently, failures
in state assignment are reflected through the reduced cov-
erage rather than artificially skewing the reported MAE
or R2 values.
The addition of the decision ladder significantly im-
proves the overall performance. As shown in Figure 4,
R2 =0.713fortheBaselinemodelincreasestoR2 =0.832
fortheDecisionmodel,whilethenumberofverifiedVTEs
N increased from 139 to 246. This simultaneous im-
scored
provement in accuracy and coverage indicates that the
procedural knowledge encoded within the decision ladder
enables the agents to solve and execute a substantially
larger fraction of multireference quantum chemistry prob-
lemswithoutsacrificingpredictivequality. Thisisfurther
supported by the distribution of errors. In the Baseline
model,22outof139scoredVTEs(15.8%)exhibitedabso-
lute errors greater than 0.5 eV, with a maximum error of
3.97 eV. In comparison, the Decision model increased the
number of successfully identified VTEs to 246, of which
46 (18.7%) exhibited absolute errors exceeding 0.5 eV
and a maximum error of 3.76 eV. Although the decision
ladder greatly expands the range of molecules that can
be successfully treated, these results indicate that addi-
tional refinement of the decision policies are necessary to
systematically reduce the largest energy errors.
Performance is evaluated separately for each class of
)Ve(
2TPVEN-CS
detupmoC
Decision n=246 R2=0.832
Baseline n=139 R2=0.713
FIG. 4. Comparison of computed and reference vertical tran-
sition energies for the Baseline and Decision models. The
dashed line denotes perfect agreement.
VTEs so that accuracy and coverage are assessed inde-
pendently (Table I). Across the full benchmark out of
N =558referenceVTEs,theDecisionmodelincreased
refs
dataset coverage from 24.9% (N =138 in the Base-
scored
line model) to 44.1% while simultaneously reducing the
overall MAE of 0.373 eV to 0.339 eV. However, perfor-
mance varied substantially depending on the underlying
electronic character of the VTE. For successfully scored
VTEs, the agent was reasonable stable and there were no
catastrophic outliers (Figure 4).
The largest volume of scored cases belonged to sin-
gle (valence) excitations (N = 352). The Decision
refs
model increased both metrics substantially, yielding 165
scored VTEs (46.3% coverage) and reducing the MAE
to 0.332 eV compared to the Baseline model with 124
scored VTEs (34.8% coverage) and an MAE of 0.384 eV.
Double excitations proved more difficult for the Baseline
model, which failed to produce any verified assignments.
In contrast, the Decision model successfully identified 14
out of the 30 double excitations (46.7% coverage). This
result highlights the importance of explicit policies for
diagnosing incomplete active spaces and incorrect state
assignments.
C. Recovery of Rydberg States
The most dramatic improvement was observed for Ryd-
bergexcitations,wherecoverageincreasedfromonly4.8%
to 46.0% while keeping a MAE of 0.308 eV comparable
to that of single excitations. This behavior is consistent

8
TABLE I. Evaluation metrics by VTE excitation classes for the Baseline and Decision models. N denotes the number of
scored
verifiedcomputedverticaltransitionsincludedinthestatisticalanalysis,andN isthetotalnumberofreferencetransitionsin
refs
QUESTDB.
|         |     |      |     |        |          | Baseline |     |          |     |        |          | Decision |     |       |      |
| ------- | --- | ---- | --- | ------ | -------- | -------- | --- | -------- | --- | ------ | -------- | -------- | --- | ----- | ---- |
| Class   |     | N    | N   |        | Coverage | (%)      |     | MAE (eV) | N   |        | Coverage | (%)      |     | MAE   | (eV) |
|         |     | refs |     | scored |          |          |     |          |     | scored |          |          |     |       |      |
| Single  |     | 356  |     | 124    |          | 34.8     |     | 0.384    |     | 165    |          | 46.3     |     | 0.332 |      |
| Double  |     | 30   |     | 0      |          | 0.0      |     | –        |     | 14     |          | 46.7     |     | 0.488 |      |
| Rydberg |     | 124  |     | 6      |          | 4.8      |     | 0.116    |     | 57     |          | 46.0     |     | 0.308 |      |
| TM      |     | 48   |     | 9      |          | 18.8     |     | 0.393    |     | 10     |          | 20.8     |     | 0.429 |      |
| Total   |     | 558  |     | 139    |          | 24.9     |     | 0.373    |     | 246    |          | 44.1     |     | 0.339 |      |
with the design of Rule G, which explicitly introduces E. Coverage
| orbital-diffuseness |                   | analysis |                 | and targeted | active-space |         | ex-   |           |     |            |     |               |     |          |     |
| ------------------- | ----------------- | -------- | --------------- | ------------ | ------------ | ------- | ----- | --------- | --- | ---------- | --- | ------------- | --- | -------- | --- |
| pansion             | for Rydberg-state |          | identification. |              |              | Without | these |           |     |            |     |               |     |          |     |
|                     |                   |          |                 |              |              |         |       | To assess | the | robustness | of  | our workflow, |     | coverage | was |
diagnostics, the Baseline model rarely selected the dif- evaluated across all 84 target molecules. The Baseline
fuse orbitals required to describe Rydberg excitations. modelfailedtoreproduceasinglereference-matchedVTE
| Transition-metal |            | systems | remained |              | the most | challenging |        |                   |     |         |           |          |        |         |     |
| ---------------- | ---------- | ------- | -------- | ------------ | -------- | ----------- | ------ | ----------------- | --- | ------- | --------- | -------- | ------ | ------- | --- |
|                  |            |         |          |              |          |             |        | for 33 molecules, |     | whereas | the       | Decision | model  | failed  | on  |
| category,        | exhibiting | only    | modest   | improvements |          | in          | cover- |                   |     |         |           |          |        |         |     |
|                  |            |         |          |              |          |             |        | 29 molecules.     | Of  | these   | failures, | 23 were  | shared | between |     |
age and similar MAEs between the two models. These both models, while 7 and 3 were unique to the Baseline
| results demonstrate |     | that | identifying |     | diffuse | orbital | char- |              |         |     |               |     |          |     |        |
| ------------------- | --- | ---- | ----------- | --- | ------- | ------- | ----- | ------------ | ------- | --- | ------------- | --- | -------- | --- | ------ |
|                     |     |      |             |     |         |         |       | and Decision | models, |     | respectively. | The | decision |     | ladder |
acterisacriticalcapabilitythatisnotnaturallycaptured
|     |     |     |     |     |     |     |     | substantially | improved |     | molecular-level |     | coverage. |     | The |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | -------- | --- | --------------- | --- | --------- | --- | --- |
through occupation analysis alone. Decision model achieved an MAE below 0.3 eV for 38
|     |     |     |     |     |     |     |     | molecules,   | including   | 15  | for which | all reference |     | VTEs         | were |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ----------- | --- | --------- | ------------- | --- | ------------ | ---- |
|     |     |     |     |     |     |     |     | successfully | reproduced. |     | In        | comparison,   |     | the Baseline |      |
D. Transition-Metal Systems model achieved an MAE below 0.3 eV for 35 molecules,
|                  |     |             |     |          |     |          |       | but only | 3 reproduced |     | the complete |     | reference | VTE | set. |
| ---------------- | --- | ----------- | --- | -------- | --- | -------- | ----- | -------- | ------------ | --- | ------------ | --- | --------- | --- | ---- |
| Transition-metal |     | excitations |     | remained |     | the most | chal- |          |              |     |              |     |           |     |      |
TheincreasedbreadthoftheDecisionmodelisexemplified
lenging class in the benchmark. Although the decision- bytriazine,forwhichall14referenceVTEswererecovered,
guided workflow substantially improved the accuracy of whereas the best Baseline result reproduced only 6 of 8
successfully identified states, increasing reliability came VTEs for acrolein.
at the expense of benchmark coverage. For the subset of Acrossmoleculeswithatleastonesuccessfullyidentified
four VTEs successfully evaluated by both workflows, the VTE, the Decision model reproduced 71.7% of reference
Decision model consistently outperformed the Baseline VTEspermoleculecomparedwith46.7%fortheBaseline
| model, | reducing | the MAE | from | 0.348 | to 0.217 | eV. |     |        |         |        |        |      |            |     |      |
| ------ | -------- | ------- | ---- | ----- | -------- | --- | --- | ------ | ------- | ------ | ------ | ---- | ---------- | --- | ---- |
|        |          |         |      |       |          |     |     | model. | For the | subset | of 109 | VTEs | identified | by  | both |
The reduction in coverage highlights a difficulty of workflows, the two models exhibited comparable accu-
transition-metalelectronicstructures. Unlikethepredom- racy, with MAEs of 0.268 and 0.242 eV for the Decision
inantlyorganicsystemsfoundelsewhereinthebenchmark,
|     |     |     |     |     |     |     |     | and Baseline | models, |     | respectively. | The | largest | error | in  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | --- | ------------- | --- | ------- | ----- | --- |
transition-metal can exhibit near-degenerate d-orbital both workflows occurred for cyclopentadienone, which
manifolds, competing spin states, and complex excited exhibited MAEs of 3.763 (Decision model) and 3.774 eV
manifolds and state-averaging. These features increase (Baseline model).
| ambiguity | in active-space |     | selection |     | and state | assignment, |     |              |     |             |     |             |     |      |        |
| --------- | --------------- | --- | --------- | --- | --------- | ----------- | --- | ------------ | --- | ----------- | --- | ----------- | --- | ---- | ------ |
|           |                 |     |           |     |           |             |     | The increase |     | in coverage | was | accompanied |     | by a | higher |
makingitdifficulttodistinguishphysicallymeaningfulso- computational cost. The Baseline model completed 131
lutions from formally converged but chemically incorrect calculations spanning 84 distinct structure, active-space,
| wave functions. |     | The improved |     | accuracy | achieved |     | by the |                     |     |                 |     |     |           |     |       |
| --------------- | --- | ------------ | --- | -------- | -------- | --- | ------ | ------------------- | --- | --------------- | --- | --- | --------- | --- | ----- |
|                 |     |              |     |          |          |     |        | and state-averaging |     | configurations. |     | In  | contrast, | the | Deci- |
Decision model suggests that the additional validation sion model executed 576 calculations across 148 config-
procedures successfully filtered out a fraction of these in- urations and reached the maximum eight-attempt limit
correct solutions. However, the accompanying reduction for two molecules without obtaining a successful result.
| in coverage | indicates |     | that | the current | decision | policies |     |               |      |           |     |          |              |     |      |
| ----------- | --------- | --- | ---- | ----------- | -------- | -------- | --- | ------------- | ---- | --------- | --- | -------- | ------------ | --- | ---- |
|             |           |     |      |             |          |          |     | Nevertheless, | both | workflows |     | remained | conservative |     | rel- |
remain insufficiently robust for general transition-metal ative to the QUESTDB benchmark, which contains 502
chemistry. Future improvements will likely require more distinct active-space and state-averaging protocols.
| specialized | active-space |     | construction |     | strategies, | stronger |     |     |     |     |     |     |     |     |     |
| ----------- | ------------ | --- | ------------ | --- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
state-trackingprocedures,andalargerbodyoftransition-
metal-specific literature precedents. F. Failure Modes and Limitations
|     |     |     |     |     |     |     |     | The dominant |          | failure | mode   | for both  | models          | was | the in- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | -------- | ------- | ------ | --------- | --------------- | --- | ------- |
|     |     |     |     |     |     |     |     | ability to   | identify | an      | active | space and | state-averaging |     |         |

9
TABLE II. Evaluation metrics by VTE excitation classes for 14
the Replication model. N denotes the number of verified scored
computed vertical transitions, and N the total number of
refs
reference transitions in QUESTDB. 12
Replication
Class N N Coverage (%) MAE (eV) 10
refs scored
Single 356 266 74.7 0.023
Double 30 19 63.3 0.019
Rydberg 124 61 49.2 0.021 8
TM 48 32 66.7 0.037
Total 558 378 67.7 0.023
6
strategy to reproduce the reference electronic states. 4
These failures led into incorrect underlying orbital mani-
folds, missed VTEs, and incomplete descriptions of elec-
2
tronically complex systems, particularly molecules con-
taining transition-metals.
Morebroadly,mostunsuccessfulbenchmarkcasesarose 0
0 2 4 6 8 10 12 14
fromincorrectorambiguousstateassignmentsratherthan
Published SC-NEVPT2 (eV)
large numerical errors in successfully identified states.
This observation suggests that future improvements are
more likely to come from enhanced orbital interpreta-
tion, state tracking, and active-space construction than
fromincrementalrefinementsintheunderlyingelectronic-
structuremethods. Accuratelyidentifyingthedesiredelec-
tronic states remains a difficult problem even for expert
practitioners, especially when little a priori information
is available.
Despite these limitations, the benchmark demonstrates
that LLM agents can achieve reasonable quantitative
accuracywhen appropriateactivespaces andstate assign-
ments are obtained. More importantly, the results show
that structured decision policies substantially improve
the autonomous execution of multireference quantum-
chemical workflows by increasing both the reliability and
breadthofsuccessfulcalculations. Thishighlightopportu-
nities for improving state-selection strategies rather than
fundamental limitations of the agent-based framework
itself.
G. Replication Test
To establish an upper bound on agent performance, we
evaluated a Replication model provided with all infor-
mation necessary to reproduce the QUESTDB reference
calculations. This included the active space definitions,
state-averaging specifications by irrep, and the associated
publications and supplementary information. As shown
in Figure 5, the replicated calculations exhibit excellent
agreement with the reference data, without evidence of
systematic bias or significant outliers. This result shows
thattheLLMagentcanreliablyreproducepublishedmul-
tireference workflows when provided with the necessary
computational context.
Unlike the previous benchmarks, which only verified
)Ve(
2TPVEN-CS
detupmoC
R2 = 0.9995
FIG. 5. Comparison of computed and reference vertical tran-
sition energies for the Replication model. The dashed line
denotes perfect agreement.
VTE identity matches, successful replication additionally
requiredreproducingthepublishedactive-spaceandstate-
averaging protocols. Under these stricter criteria, the
Replication model achieved an overall MAE of 23 meV,
representing an order-of-magnitude improvement over
both the Baseline and Decision models. Performance
was remarkably consistent across excitation classes, with
transition-metal systems showing only a modest increase
in error (Table II).
In total, 201 VTEs were reproduced with errors below
5 meV, including 51 reproduced exactly. The remaining
overall MAE of 0.023 eV is primarily due to differences in
state-average weighting between ORCA and MOLPRO.
56 states were computing using weighting schemes that
differedfromtheoriginalMOLPROcalculations,resulting
inahigheraverageMAEof45.1meV.WhereasMOLPRO
applies equal weighting to all roots, ORCA weights roots
by blocks. Although this discrepancy is documented in
thedecisionladder,itwasnotstrictlyenforcedwithinthe
decision-making process, leading to it being overlooked in
multiple instances. In contrast, when the agent explicitly
corrected the state-average weights to match the refer-
ence protocol (22 states), the average MAE decreased to
8.1 meV. Thus, the residual discrepancies arise primarily
fromworkflowimplementationdetailsratherthanfailures
in state identification or active-space selection.
Overall, coverage reached 67.7%, with most unrepro-
duced VTEs attributable to the imposed limit of eight
calculation attempts: 117 VTEs reached the attempt cap
without a successful result, 51 produced incorrect solu-
tions, 9 converged without yielding a usable assignment,

10
250
200
150
100
50
0
1 2 3 4 5 6 7 8 >8
Attempts submitted
n
V. CONCLUSIONS
210
42%
We benchmarked an autonomous LLM agent capable
of executing multireference quantum-chemical workflows,
including active-space selection, ORCA input generation, 114
23% outputanalysis,convergencerecovery,andelectronic-state
identification. Across 558 reference vertical transition 62
12% energies from QUESTDB, introducing a structured de-
29 27
6% 5% 15 20 16 9 cision ladder increased benchmark coverage from 24.9%
3% 4% 3% 2% to 44.1% while reducing the overall MAE from 0.373
to 0.339 eV. The largest gains were observed for dou-
ble and Rydberg excitations, demonstrating that expert-
informed decision policies can substantially improve the
FIG. 6. Distribution of calculation attempts executed by the reliability and breadth of autonomous multireference cal-
LLM agent per target specification. Percentages and absolute culations. Transition-metal systems remained the most
counts (n) are shown above each bar. The imposed attempt challenging class, highlighting the need for more special-
threshold is capped at 8 (n=9, 2%), while the gray-hatched ized active-space construction, state-tracking procedures,
bar (> 8, n = 114, 23%) corresponds to specifications that and domain-specific guidance.
failed to converge within the maximum allowed attempt limit Thereplicationbenchmarkestablishesapracticalupper
and would require additional calculations to complete.
bound on agent performance when complete contextual
information is available. Under these conditions, the
agent reproduced published calculations with an overall
and only 3 failed due to other errors. Thus, the principal
MAE of only 23 meV, with 42% of target calculations
constraint on coverage was not accuracy but the compu-
completed on the first attempt and 75% within seven
tational budget allocated to autonomous exploration.
attempts. Our results show that LLM agents are capable
While increasing the allowed attempts could improve
of reliably reproducing complex multireference workflows.
coverage, the resulting computational cost must be fac-
The dominant remaining limitations arise from workflow
tored into evaluations of LLM replication capabilities
efficiency and search strategy rather than an inability to
as the computational cost of replication was substantial.
recover the correct electronic structure. The ability to
The agent submitted 2,459 ORCA jobs, of which 1,253
autonomouslyreplicatepublishedcalculationscreatesnew
successfully reproduced the target VTEs. For these suc-
opportunities for automated verification, cross-platform
cessful runs, the agent needed 3.48 calculation attempts
benchmarking, and large-scale reproducibility studies of
on average to successfully reproduce a calculation. The
quantum chemical data.
largest contributor to unsuccessful calculations was the
To that end, our results demonstrate that the effec-
eight-attempt cap, accounting for 776 jobs. Nevertheless,
tiveness of LLM agents in scientific computing depends
42% of target specifications (n = 210) were reproduced
strongly on the quality of the reasoning framework pro-
on the first attempt, typically when MP2 natural orbitals
vided to them. General-purpose language models possess
already generated the correct active space. Moreover,
substantial chemical knowledge but often lack the struc-
75% of successful reproductions were completed within
tured decision-making processes required for demanding
sevenattempts,and77%withintheimposedlimitofeight
multistep workflows. Embedding expert knowledge in the
attempts. These results indicate that roughly one-third
form of decision ladders, validation criteria, and domain-
of benchmark calculations required at least one corrective
specific retrieval systems offers a practical route toward
intervention by the agent.
improvingreliabilitywhileretainingtheflexibilityoffoun-
The distribution in Figure 6 also suggests diminishing
dationmodels. Futureprogresswilllikelycomefromagent
returns beyond approximately eight attempts, as increas-
architecturesthatcombinespecializedscientificknowledge
ingly large computational effort is required to recover a
bases, more sophisticated state identification and active-
progressively smaller fraction of remaining targets. Con-
spaceselectionstrategies, andtighterintegrationbetween
sequently, future improvements are likely to be achieved
machine reasoning and electronic-structure theory. Such
more effectively through refinement of the decision poli-
developments could substantially reduce computational
cies than by simply increasing the allowed number of
overheadwhileincreasingcoverageandaccuracy,enabling
attempts. Additionally, the agent could be used as a
autonomous, high-throughput multireference quantum
screening or ranking tool to filter out routine calculations
chemistry and accelerating the generation, verification,
while reserving challenging cases for human experts.
and dissemination of computational benchmark data.

11
|                            |           |     |                        |              |           |     |       | CESS) program,    |     | which is supported | by U.S. National | Sci-      |
| -------------------------- | --------- | --- | ---------------------- | ------------ | --------- | --- | ----- | ----------------- | --- | ------------------ | ---------------- | --------- |
|                            | CODE      | AND | DATA                   | AVAILABILITY |           |     |       |                   |     |                    |                  |           |
|                            |           |     |                        |              |           |     |       | ence Foundation   |     | grants #2138259,   | #2138286,        | #2138307, |
|                            |           |     |                        |              |           |     |       | #2137603,         | and | #2138296. During   | the preparation  | of this   |
| All data                   | presented | in  | this work              | were         | generated |     | using |                   |     |                    |                  |           |
|                            |           |     |                        |              |           |     |       | manuscript/study, |     | the author(s)      | used Microsoft   | Copilot   |
| publiclyavailablesoftware. |           |     | TheLLMagentanddocumen- |              |           |     |       |                   |     |                    |                  |           |
tation,thegenerateddataandLLMreasoningisavailable (institutional instance) for the purposes of editing and
at [Placeholder]. language polishing. No new content was generated, and
theauthorshavereviewedandeditedtheoutputandtake
|     |     |     |     |     |     |     |     | full responsibility |     | for the content | of this publication. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --------------- | -------------------- | --- |
ACKNOWLEDGMENTS
ThismaterialisbaseduponworksupportedbytheU.S. AUTHOR CONTRIBUTIONS
| Department |          | of Energy, | Office | of Science, |               | Office of | Basic |        |           |            |                           |     |
| ---------- | -------- | ---------- | ------ | ----------- | ------------- | --------- | ----- | ------ | --------- | ---------- | ------------------------- | --- |
|            |          |            |        |             |               |           |       | V.C.L. | - Writing | - Original | Draft, Conceptualization, |     |
| Energy     | Sciences | under      | Award  | Number      | DE-SC0025176. |           |       |        |           |            |                           |     |
Methodology,Software,Formalanalysis,Investigation,Vi-
| This research |     | was supported |     | in part | through | the | com- |     |     |     |     |     |
| ------------- | --- | ------------- | --- | ------- | ------- | --- | ---- | --- | --- | --- | --- | --- |
putational resources and staff contributions provided sualization,Resources. J.M.R.-Writing-OriginalDraft,
|              |       |                  |             |            |             |           |         | Supervision, | Project   | administration, | Funding  | acquisition. |
| ------------ | ----- | ---------------- | ----------- | ---------- | ----------- | --------- | ------- | ------------ | --------- | --------------- | -------- | ------------ |
| for the      | Quest | high performance |             | computing  |             | facility  | at      |              |           |                 |          |              |
| Northwestern |       | University       | which       | is jointly |             | supported | by      |              |           |                 |          |              |
| the Office   | of    | the Provost,     | the         | Office     | for         | Research, | and     |              |           |                 |          |              |
|              |       |                  |             |            |             |           |         |              | COMPETING |                 | INTEREST |              |
| Northwestern |       | University       | Information |            | Technology. |           | This    |              |           |                 |          |              |
| work used    | Anvil | at Purdue        | University  |            | through     |           | alloca- |              |           |                 |          |              |
tion PHY250069 from the Advanced Cyberinfrastruc- The authors declare no competing interests.
| ture Coordination |     | Ecosystem: |     | Services | &   | Support | (AC- |     |     |     |     |     |
| ----------------- | --- | ---------- | --- | -------- | --- | ------- | ---- | --- | --- | --- | --- | --- |
[1] K. Burke, Perspective on density functional theory, The lene, Journal of Chemical Theory and Computation
Journal of Chemical Physics 136, 150901 (2012). 20, 5105 (2024), https://pubs.acs.org/jctcce/article-
[2] P. Hohenberg and W. Kohn, Inhomogeneous electron pdf/20/12/5105/1775462/ct4c00212.pdf.
gas, Phys. Rev. 136, B864 (1964). [8] R. Khurana, M. R. Hermes, V. Agarawal, C. Knight,
[3] W. Kohn, A. D. Becke, and R. G. Parr, L. Gagliardi, and C. Liu, Multireference investigations
Density functional theory of electronic struc- of ethylene hydrogenation over bimetallic catalysts, npj
ture, The Journal of Physical Chemistry 100, Computational Materials 10.1038/s41524-026-02255-y
| 12974 |     | (1996), https://pubs.acs.org/jpchax/article- |     |     |     |     |     | (2026). |     |     |     |     |
| ----- | --- | -------------------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
pdf/100/31/12974/16073344/jp960669l.pdf. [9] W. T. Morrillo, A. Mattioni, W. J. A. Blackmore, D. P.
[4] D. S. Levine, M. Shuaibi, E. W. C. Spotte-Smith, Mills, and N. F. Chilton, Modelling electric field con-
M. G. Taylor, M. R. Hasyim, K. Michel, I. Batatia, trol in a 4f molecular qudit with hyperfine coupling,
G. Cs´anyi, M. Dzamba, P. Eastman, N. C. Frey, X. Fu, Communications Chemistry 9, 45 (2025).
V. Gharakhanyan, A. S. Krishnapriyan, J. A. Rackers, [10] D. Barreiro-Lage, V. Ledentu, J. D’Ascenzi,
S. Raja, A. Rizvi, A. S. Rosen, Z. Ulissi, S. Vargas, M. Huix-Rotllant, and N. Ferr´e, Investigating
C. L. Zitnick, S. M. Blau, and B. M. Wood, The open the origin of automatic rhodopsin modeling out-
molecules 2025 (omol25) dataset, evaluations, and mod- liers using the microbial gloeobacter rhodopsin as
els (2026), arXiv:2505.08762 [physics.chem-ph]. testbed, The Journal of Physical Chemistry B 128,
[5] M. K. Horton, P. Huck, R. X. Yang, J. M. Munro, 12368 (2024), https://pubs.acs.org/jpcbfk/article-
S.Dwaraknath,A.M.Ganose,R.S.Kingsbury,M.Wen, pdf/128/50/12368/14969665/jp4c05962.pdf.
J. X. Shen, T. S. Mathis, A. D. Kaplan, K. Berket, [11] X. Miao, K. Diemer, and R. Mitri´c, A casscf/mrci tra-
J. Riebesell, J. George, A. S. Rosen, E. W. C. Spotte- jectory surface hopping simulation of the photochemical
Smith, M. J. McDermott, O. A. Cohen, A. Dunn, M. C. dynamics and the gas phase ultrafast electron diffrac-
Kuner, G.-M. Rignanese, G. Petretto, D. Waroquiers, tionpatternsofcyclobutanone,TheJournalofChemical
S. M. Griffin, J. B. Neaton, D. C. Chrzan, M. Asta, Physics 160, 124309 (2024).
G.Hautier,S.Cholia,G.Ceder,S.P.Ong,A.Jain,and [12] P. E. M. Siegbahn, J. Alml¨of, A. Heiberg, and B. O.
K.A.Persson,Accelerateddata-drivenmaterialsscience Roos, The complete active space scf (casscf) method in
with the materials project, Nature Materials 24, 1522 a newton–raphson formulation with application to the
| (2025). |          |             |             |     |              |     |       | hnomolecule,TheJournalofChemicalPhysics74,2384 |     |     |     |     |
| ------- | -------- | ----------- | ----------- | --- | ------------ | --- | ----- | ---------------------------------------------- | --- | --- | --- | --- |
| [6] S.  | Kirklin, | J. E. Saal, | B. Meredig, |     | A. Thompson, |     | J. W. | (1981).                                        |     |     |     |     |
Doak, M. Aykol, S. Ru¨hl, and C. Wolverton, The open [13] D.-K. Dang and P. M. Zimmerman, Fully variational
quantum materials database (oqmd): assessing the ac- incremental casscf, The Journal of Chemical Physics
curacy of dft formation energies, npj Computational 154, 014105 (2021).
Materials 1, 15010 (2015). [14] J. J. Wardzala, M. R. Hennefarth, V. Agarawal,
[7] S. Saade and H. G. A. Burton, Excited state- B. Jangid, A. Seal, M. R. Hermes, D. S. King,
specific casscf theory for the torsion of ethy- and L. Gagliardi, Multireference methods for

12
chemistry and materials science: Automated datasets for metal–organic frameworks, Digital Dis-
active spaces, efficient dynamic correlation, covery 4, 2676 (2025), https://pubs.rsc.org/dd/article-
and extended systems, Chemical Reviews 126, pdf/4/10/2676/10331351/d5dd00081e.pdf.
4592 (2026), https://pubs.acs.org/chreay/article- [25] J. M. Cavanagh, K. Sun, A. Gritsevskiy, D. Bagni,
pdf/126/8/4592/65005694/cr5c00866.pdf. Y. Wang, T. D. Bannister, and T. Head-Gordon, Smi-
[15] E. R. Sayfutyarova, Q. Sun, G. K.-L. Chan, leyllama: modifying large language models for directed
and G. Knizia, Automated construction of molec- chemical space exploration, Nature Computational Sci-
ular active spaces from atomic valence orbitals, ence 6, 856 (2026).
Journal of Chemical Theory and Computation [26] J. M. Cavanagh, J. B. Arnold, G. B. Alteri, A. Grit-
13, 4063 (2017), https://pubs.acs.org/jctcce/article- sevskiy, and T. Head-Gordon, How well can frontier
pdf/13/9/4063/7645019/ct7b00128.pdf. large language models generate structures? high qual-
[16] E. R. Sayfutyarova and S. Hammes-Schiffer, Con- ity prediction of molecular geometries with help from
structing molecular π-orbital active spaces for fine-tuning (2026), arXiv:2607.13350 [physics.chem-ph].
multireference calculations of conjugated systems, [27] Y.Chen,D.G.Truhlar,andX.He,Cof26: Anewon-top
Journal of Chemical Theory and Computation 15, functional for multiconfiguration pair-density functional
1679 (2019), https://pubs.acs.org/jctcce/article- theory (2026), arXiv:2605.06215 [physics.chem-ph].
pdf/15/3/1679/10312694/ct8b01196.pdf. [28] F. Neese, Software update: The orca program system—
[17] C. J. Stein and M. Reiher, Automated se- version 6.0, Wiley Interdiscip. Rev. Comput. Mol. Sci.
lection of active orbital spaces, Journal of 15, e70019 (2025).
Chemical Theory and Computation 12, 1760 [29] K. Zhou, Y. Zhu, Z. Chen, W. Chen, W. X. Zhao,
(2016), https://pubs.acs.org/jctcce/article- X. Chen, Y. Lin, J.-R. Wen, and J. Han, Don’t
pdf/12/4/1760/8916165/ct6b00156.pdf. make your llm an evaluation benchmark cheater (2023),
[18] C. J. Stein and M. Reiher, autocas: A program for arXiv:2311.01964 [cs.CL].
fully automated multiconfigurational calculations, [30] P.-F. Loos, M. Boggio-Pasqua, A. Blondel,
Journal of Computational Chemistry 40, 2216 (2019), F. Lipparini, and D. Jacquemin, Quest database
https://onlinelibrary.wiley.com/doi/pdf/10.1002/jcc.25869. of highly-accurate excitation energies, Jour-
[19] G. K.-L. Chan, An algorithm for large scale density nal of Chemical Theory and Computation 21,
matrix renormalization group calculations, The Journal 8010 (2025), https://pubs.acs.org/jctcce/article-
of Chemical Physics 120, 3172 (2004). pdf/21/16/8010/41269129/ct5c00975.pdf.
[20] W. Jeong, S. J. Stoneburner, D. King, R. Li, [31] V. C. Lee, J. Lee, and J. M. Rondinelli,
A. Walker, R. Lindh, and L. Gagliardi, Automa- Aimdb: Artificial intelligence multiconfigu-
tion of active space selection for multireference meth- rational database, ChemRxiv 2026 (2026),
ods via machine learning on chemical bond disso- https://chemrxiv.org/doi/pdf/10.26434/chemrxiv.15007136/v1.
ciation, Journal of Chemical Theory and Computa- [32] F. Neese, The orca program system, Wiley Interdiscip.
tion16,2389(2020),https://pubs.acs.org/jctcce/article- Rev. Comput. Mol. Sci. 2, 73 (2012).
pdf/16/4/2389/6275351/ct9b01297.pdf. [33] C. Angeli, R. Cimiraglia, S. Evangelisti, T. Leininger,
[21] J. Zhou, B. Jangid, M. R. Hermes, and and J.-P. Malrieu, Introduction of n-electron valence
L. Gagliardi, High-throughput multireference states for multireference perturbation theory, The Jour-
calculations of magnetic properties of lan- nal of Chemical Physics 114, 10252 (2001).
thanide complexes, ChemRxiv 2026 (2026), [34] S. Kossmann and F. Neese, Efficient structure
https://chemrxiv.org/doi/pdf/10.26434/chemrxiv.15003428/v2. optimization with second-order many-body per-
[22] J. Gottweis, W.-H. Weng, A. Daryin, T. Tu, P. Sirkovic, turbation theory: The rijcosx-mp2 method, Jour-
A. Myaskovsky, G. Glowaty, F. Weissenberger, A. Or- nal of Chemical Theory and Computation 6,
landi, D. Popovici, A. Palepu, K. Rong, R. Tanno, 2325 (2010), https://pubs.acs.org/jctcce/article-
K. Saab, F. Zhang, J. Blum, A. Carroll, K. Kulka- pdf/6/8/2325/1961783/ct100199k.pdf.
rni, N. Tomaˇsev, D. Zverinski, I. Rendulic, E. Vedadi, [35] Anthropic, Claude, Large language model (2026), ac-
F. Hasler, L. Rimanic, M. Boia, I. Budiselic, B. Fe- cessed: [Date, e.g., July 31, 2026].
instein, M. Bellaiche, T. Sheffer, J. Freyberg, J. Rat- [36] H.-J. Werner, P. J. Knowles, F. R. Manby, J. A. Black,
cliff, O. Bertolli, K. Chou, A. Hassidim, B. Gokturk, K. Doll, A. Heßelmann, D. Kats, A. K¨ohn, T. Ko-
A.Vahdat,Y.Guan,V.Dhillon,E.D.Vaishnav,B.Lee, rona, D. A. Kreplin, Q. Ma, I. Miller, Thomas F.,
T. R. D. Costa, J. R. Penad´es, G. Peltz, Y. Matias, A.Mitrushchenkov,K.A.Peterson,I.Polyak,G.Rauhut,
J. Manyika, D. Hassabis, Y. Xu, P. Kohli, A. Pawlosky, andM.Sibaev,Themolproquantumchemistrypackage,
A. Karthikesalingam, and V. Natarajan, Accelerating The Journal of Chemical Physics 152, 144107 (2020).
scientific discovery with co-scientist, Nature 655, 487 [37] M. Hapka, M. Przybytek, and K. Pernal, Second-Order
(2026). Exchange-Dispersion Energy Based on a Multireference
[23] A. E. Ghareeb, B. Chang, L. Mitchener, A. Yiu, C. J. Description of Monomers, Journal of Chemical Theory
Szostkiewicz, D. Shved, G. J. Gyimesi, J. M. Laurent, and Computation 10.1021/acs.jctc.9b00925 (2019).
S. M. Wright, M. T. Razzak, A. D. White, S. C. Finne- [38] B.C.Hoffman,Y.Yamaguchi,andH.F.Schaefer,TheX˜
mann,M.M.Hinks,andS.G.Rodriques,Amulti-agent 1A1,a˜3B1andA˜ 1B1ElectronicStatesoftheAluminum
system for automating scientific discovery, Nature 655, Dihydride Anion, The Journal of Physical Chemistry A
497 (2026). 10.1021/jp984714w (1999).
[24] Y. Shi, N. Rampal, C. Zhao, D. J. Fu, C. Borgs, J. T. [39] A. Kerridge, Oxidation state and covalency in f-
Chayes, and O. M. Yaghi, Comparison of llms in ex- element metallocenes (M = Ce, Th, Pu): a combined
tracting synthesis conditions and generating q&amp;a CASSCF and topological study, Dalton Transactions

13
10.1039/c3dt52279b (2013). [53] S. Battaglia and R. Lindh, On the role of symmetry
[40] J.Lennartz,E.Dumas,L.Ramirez,andJ.M.Galbraith, in XDW-CASPT2, The Journal of Chemical Physics
A Computational Determination of the Lowest Energy 10.1063/5.0030944 (2021).
Electronic and Geometric States of First Row Transi- [54] C.W.BauschlicherandS.R.Langhoff,Theoreticaldeter-
tion Metal Dioxygen Dications, Journal of Theoretical mination of the radiative lifetime of the A 2Σ+ state of
Chemistry 10.1155/2013/734354 (2013). OH, The Journal of Chemical Physics 10.1063/1.452829
[41] X. Li, W. Ai, and N. Q. Su, A Benchmark Database for (1987).
Spin-FlipGapCalculationsinSingle-andMultireference [55] P. P. Bera, Y. Yamaguchi, H. F. Schaefer, and T. D.
Systems Using ∆DFT and Beyond, Journal of Chemi- Crawford, Born−Oppenheimer Symmetry Breaking in
cal Theory and Computation 10.1021/acs.jctc.5c01411 the C˜ State of NO2: Importance of Static and Dynamic
(2025). Correlation Effects, The Journal of Physical Chemistry
[42] F. Feixas, J. Vandenbussche, P. Bultinck, E. Matito, A 10.1021/jp077561y (2008).
and M. Sol`a, Electron delocalization and aromatic- [56] R. Berger, C. Fischer, and M. Klessinger, Calculation
ity in low-lying excited states of archetypal organic of the Vibronic Fine Structure in Electronic Spectra at
compounds, Physical Chemistry Chemical Physics Higher Temperatures. 1. Benzene and Pyrazine, The
10.1039/c1cp22239b (2011). Journal of Physical Chemistry A 10.1021/jp981597w
[43] A. O. Lykhin, D. G. Truhlar, and L. Gagliardi, Dipole (1998).
Moment Calculations Using Multiconfiguration Pair- [57] N. A. Besley and J. D. Hirst, Ab Initio Study of
Density Functional Theory and Hybrid Multiconfigu- the Electronic Spectrum of Formamide with Explicit
rationPair-DensityFunctionalTheory,JournalofChem- Solvent, Journal of the American Chemical Society
ical Theory and Computation 10.1021/acs.jctc.1c00915 10.1021/ja990064d (1999).
(2021). [58] I. Bhattacharjee, D. Ghosh, and A. Paul, Resolving the
[44] S. A. do Monte, R. F. K. Spada, R. L. R. Alves, Quadruple Bonding Conundrum in C2 Using Insights
L.Belcher,R.Shepard,H.Lischka,andF.Plasser,Quan- Derived from Excited State Potential Energy Surfaces:
tification of the Ionic Character of Multiconfigurational A Molecular Orbital Perspective, ChemRxiv preprint
Wave Functions: The Qat Diagnostic, The Journal of (2019).
Physical Chemistry A 10.1021/acs.jpca.3c05559 (2023). [59] N. Blaise, J. A. Green, C. Benitez-Martin, C. Kaiser,
[45] J. G. F. Romeu, J. L. Gole, and D. A. Dixon, The M. Braun, J. M. Schaible, J. Andr´easson, I. Burghardt,
ElectronicStructureofBoron,Aluminum,andScandium and J. Wachtveitl, Isomerization dynamics of a
Monoxides: BO,AlO,andScO,TheJournalofPhysical novel cis/trans-only merocyanine, ChemPhotoChem
Chemistry A 10.1021/acs.jpca.5c05513 (2025). 10.1002/cptc.202300327 (2024).
[46] C. Sepali, L. Goletto, P. Lafiosca, M. Rinaldi, T. Gio- [60] J. Bone, J. Carmona-Garc´ıa, D. Hollas, and B. F. E.
vannini, and C. Cappelli, Fully Polarizable Multicon- Curchod, Benchmarking Electronic-Structure Methods
figurational Self-Consistent Field/Fluctuating Charges for the Description of Dark Transitions in Carbonyls at
Approach,JournalofChemicalTheoryandComputation and Beyond the Franck–Condon Point, The Journal of
10.1021/acs.jctc.4c01125 (2024). Physical Chemistry A 10.1021/acs.jpca.5c05510 (2025).
[47] C. Sousa, W. A. de Jong, R. Broer, and W. C. Nieuw- [61] W. J. Buma and F. Zerbetto, Vibronic activity in
poort, Theoretical characterization of the low-lying ex- trans,trans-1,3,5,7 octatetraene: The S0→S1 spectrum,
citedstatesoftheCuClmolecule,TheJournalofChem- The Journal of Chemical Physics 10.1063/1.469899
ical Physics 10.1063/1.473161 (1997). (1995).
[48] S. An, T. Wang, L. Xiao, D. Liu, X. Zhang, [62] D. Buzs´aki, S. Mandal, and M. P´apai, Trajectory
and B. Yan, Opacities of X2Σ+, A2Π, and B2Σ+ excited-state dynamics study of pyrazine: Assessment
states of CO+ molecule ion, Acta Physica Sinica of potential energy surfaces and simulation of pi-
10.7498/aps.74.20250380 (2025). cosecond timescales, The Journal of Chemical Physics
[49] J. M. Anglada, J. M. Bofill, S. Olivella, and A. Sol´e, 10.1063/5.0320535 (2026).
Unimolecular Isomerizations and Oxygen Atom Loss [63] P. B. Calio, D. G. Truhlar, and L. Gagliardi, Nonadia-
in Formaldehyde and Acetaldehyde Carbonyl Oxides. batic Molecular Dynamics by Multiconfiguration Pair-
A Theoretical Investigation, Journal of the American Density Functional Theory, Journal of Chemical Theory
Chemical Society 10.1021/ja953858a (1996). and Computation 10.1021/acs.jctc.1c01048 (2022).
[50] J.M.Anglada,S.Olivella,andA.Sol´e,OntheDissocia- [64] M. Chachisvilis and A. H. Zewail, Femtosecond Dynam-
tion of Ground State trans-HOOO Radical: A Theoreti- icsofPyridineintheCondensedPhase: ValenceIsomer-
calStudy,JournalofChemicalTheoryandComputation izationbyConicalIntersections,TheJournalofPhysical
10.1021/ct100358e (2010). Chemistry A 10.1021/jp991821x (1999).
[51] J. F. Arenas, I. L´opez-Toc´on, J. C. Otero, and J. Soto, [65] G. Cui and W. Fang, Channels to Singlet and Triplet
Carbene Formation in Its Lower Singlet State from PhenylcarbenesinPhenyldiazomethane: ACASSCFand
Photoexcited 3H-Diazirine or Diazomethane. A Com- MRCI Study, ChemPhysChem 10.1002/cphc.201100025
bined CASPT2 and ab Initio Direct Dynamics Trajec- (2011).
tory Study, Journal of the American Chemical Society [66] W.-J. Ding, W.-H. Fang, and R.-Z. Liu, A combined
10.1021/ja010750o (2002). CASSCFandTDDFTstudyonthestructuresandprop-
[52] J.F.BabbandB.M.McLaughlin,Radiativeassociation erties of formyl cyanide in low-lying electronic states,
of C(3P) and H+: triplet states, Monthly Notices of Chemical Physics Letters 10.1016/s0009-2614(03)00006-
the Royal Astronomical Society 10.1093/mnras/stx630 x (2003).
(2017). [67] Q.FangandY.-J.Liu,Wavelength-DependentPhotodis-
sociation of Benzoic Acid Monomer in α C−O Fission,

14
TheJournalofPhysicalChemistryA10.1021/jp908567m [82] B. Helmich-Paris, E. R. Kjellgren, and H. J. A. Jensen,
(2010). Excited-state methods based on state-averaged long-
[68] M. Feh´er and P. A. Martin, Ab initio calculation of the range CASSCF short-range DFT, Physical Chemistry
electricalpropertiesoftheX2Σg+groundandA2Π Chemical Physics 10.1039/d5cp00881f (2025).
uexcitedstatesofN2+,J.Chem.Soc.,FaradayTrans. [83] B. Helmich-Paris, A Two-Level Preconditioner for the
10.1039/ft9959101063 (1995). CASSCF Linear-Response Equations, The Journal of
[69] B. E. S. de Freitas, Espectroscopia dos ´ıons molecu- Physical Chemistry A 10.1021/acs.jpca.5c04385 (2025).
lares CH+, CF+, CCl+, CBr+, CI+: busca por sistemas [84] E.G.Hohenstein,M.E.F.Bouduban,C.Song,N.Luehr,
adequadosparamedidadeconstantesfundamentais,Mas- I. S. Ufimtsev, and T. J. Mart´ınez, Analytic first
ter’sthesis,UniversidadedeSaoPaulo,AgenciaUSPde derivatives of floating occupation molecular orbital-
Gestao da Informacao Academica (AGUIA) (2023). completeactivespaceconfigurationinteractionongraph-
[70] D. Ganyushin and F. Neese, A fully variational spin- ical processing units, The Journal of Chemical Physics
orbit coupled complete active space self-consistent field 10.1063/1.4923259 (2015).
approach: Application to electron paramagnetic res- [85] D. Hu, Y. Xie, X. Li, L. Li, and Z. Lan, Inclusion of
onance g-tensors, The Journal of Chemical Physics Machine Learning Kernel Ridge Regression Potential
10.1063/1.4793736 (2013). Energy Surfaces in On-the-Fly Nonadiabatic Molecular
[71] D. Ghosh, J. Hachmann, T. Yanai, and G. K.-L. Chan, DynamicsSimulation,TheJournalofPhysicalChemistry
Orbital optimization in the density matrix renormaliza- Letters 10.1021/acs.jpclett.8b00684 (2018).
tiongroup,withapplicationstopolyenesandβ-carotene, [86] M. R. Jangrouei, A. Krzemin´ska, M. Hapka, E. Pastor-
The Journal of Chemical Physics 10.1063/1.2883976 czak, and K. Pernal, Dispersion Interactions in Exciton-
(2008). Localized States. Theory and Applications to π–π* and
[72] M. Gonz´alez, I. Miquel, and R. Say´os, VTST kinet- n−π* Excited States, Journal of Chemical Theory and
ics study of the ()+(Σ)→(Π)+(,) reactions based on Computation 10.1021/acs.jctc.2c00221 (2022).
CASSCF and CASPT2 ab initio calculations including [87] J. Jiang, M. Zhang, A. Gu, R. J. D. Miller, and
excited potential energy surfaces, Chemical Physics Let- Z.Li,Quantumtomographyofmoleculesusingultrafast
ters 10.1016/s0009-2614(00)01468-8 (2001). electron diffraction, The Journal of Chemical Physics
[73] J. Gonz´alez-V´azquez and L. Gonz´alez, A CASSCF 10.1063/5.0183568 (2024).
and CASPT2 study of the photochemistry of [88] V. Jovanovi´c, I. Lyskov, M. Kleinschmidt, and C. M.
1,1- and 1,2-difluoroethylenes, Chemical Physics Marian, On the performance of DFT/MRCI-R and MR-
10.1016/j.chemphys.2008.01.043 (2008). MP2 in spin–orbit coupling calculations on diatomics
[74] J.Greiner,I.Gianni,T.Nottoli,F.Lipparini,J.J.Erik- and polyatomic organic molecules, Molecular Physics
sen,andJ.Gauss,MBE-CASSCFApproachfortheAccu- 10.1080/00268976.2016.1201600 (2017).
rateTreatmentofLargeActiveSpaces,JournalofChem- [89] S. Keller, K. Boguslawski, T. Janowski, M. Reiher, and
ical Theory and Computation 10.1021/acs.jctc.4c00388 P. Pulay, Selection of active spaces for multiconfigura-
(2024). tional wavefunctions, The Journal of Chemical Physics
[75] P.-J.GuanandW.-H.Fang,ThecombinedCASPT2and 10.1063/1.4922352 (2015).
CASSCFstudiesonphotolysisof3-thienyldiazomethane [90] N. Koga and K. Morokuma, Comparison of biradical
and subsequent reactions, Theoretical Chemistry Ac- formation between enediyne and enyne-allene. Ab initio
counts 10.1007/s00214-014-1532-3 (2014). CASSCF and MRSDCI study, Journal of the American
[76] R.GuareschiandC.Filippi,Ground-andExcited-State Chemical Society 10.1021/ja00006a006 (1991).
GeometryOptimizationofSmallOrganicMoleculeswith [91] J.KubelkaandT.A.Keiderling,AbInitioCalculationof
QuantumMonteCarlo,JournalofChemicalTheoryand Amide Carbonyl Stretch Vibrational Frequencies in So-
Computation 10.1021/ct400876y (2013). lutionwithModifiedBasisSets.1.N-MethylAcetamide,
[77] R. Guareschi, F. M. Floris, C. Amovilli, and C. Filippi, TheJournalofPhysicalChemistryA10.1021/jp013203y
SolventEffectsonExcited-StateStructures: AQuantum (2001).
Monte Carlo and Density Functional Study, Journal of [92] T.S.Kuhlman,W.J.Glover,T.Mori,K.B.Møller,and
Chemical Theory and Computation 10.1021/ct500723s T.J.Mart´ınez,Betweenethyleneandpolyenes-thenon-
(2014). adiabatic dynamics of cis-dienes, Faraday Discussions
[78] M. Gudem, A. Yadav, and A. Vijayan, Mecha- 10.1039/c2fd20055d (2012).
nism of Chemiluminescence in the Air Afterglow [93] T.N.Lan,Y.Kurashige,andT.Yanai,TowardReliable
Reaction, The Journal of Physical Chemistry A Prediction of Hyperfine Coupling Constants Using Ab
10.1021/acs.jpca.5c01912 (2025). Initio Density Matrix Renormalization Group Method:
[79] Y. Guo and K. Pernal, Approximation to Second Order Diatomic 2Σ and Vinyl Radicals as Test Cases, Journal
N-ElectronValenceStatePerturbationTheory: Limiting ofChemicalTheoryandComputation10.1021/ct400978j
the Wave Function within Singles, Journal of Chemi- (2014).
cal Theory and Computation 10.1021/acs.jctc.5c00582 [94] S. R. Langhoff, C. W. Bauschlicher, and H. Partridge,
(2025). TheoreticalstudyoftheN+2Meinelsystem,TheJournal
[80] T. Hashimoto, H. Nakano, and K. Hirao, Theoretical of Chemical Physics 10.1063/1.452835 (1987).
study of the valence π→π* excited states of polyacenes: [95] S.R.LanghoffandC.W.Bauschlicher,Theoreticalstudy
Benzene and naphthalene, The Journal of Chemical of the first and second negative systems of N+2, The
Physics 10.1063/1.471286 (1996). Journal of Chemical Physics 10.1063/1.454604 (1988).
[81] B.Helmich-Paris,BenchmarksforElectronicallyExcited [96] D. Lavorato, J. K. Terlouw, T. K. Dargel, W. Koch,
StateswithCASSCFMethods,JournalofChemicalThe- G. A. McGibbon, and H. Schwarz, Observation of the
ory and Computation 10.1021/acs.jctc.9b00325 (2019). HammickIntermediate: ReductionofthePyridine-2-ylid

15
IonintheGasPhase,JournaloftheAmericanChemical able”efficientabinitiomany-bodymethodfordescribing
Society 10.1021/ja961954l (1996). electronically excited states, The Journal of Chemical
[97] G. Luo and X. Chen, Ground-State Intermolecular Pro- Physics 10.1063/1.1337053 (2001).
tonTransferofN2O4andH2O:AnImportantSourceof [111] K. Rowell, S. Kable, and M. J. T. Jordan, Structural
AtmosphericHydroxylRadical?,TheJournalofPhysical Causes of Singlet/triplet Preferences of Norrish Type II
Chemistry Letters 10.1021/jz300336s (2012). Reactions in Carbonyls, ChemRxiv preprint (2020).
[98] A. Lykhin, D. Truhlar, and L. Gagliardi, Dipole Mo- [112] S. Saade and H. G. A. Burton, Excited State-
mentCalculationsUsingMulticonfigurationPair-Density Specific CASSCF Theory for the Torsion of Ethy-
Functional Theory and Hybrid Multiconfiguration Pair- lene, Journal of Chemical Theory and Computation
Density Functional Theory, ChemRxiv preprint (2021). 10.1021/acs.jctc.4c00212 (2024).
[99] S. Mai, A. J. Atkins, F. Plasser, and L. Gonz´alez, The [113] S. Saha, L. L. E. Cigrang, and G. A. Worth, Direct
Influence of the Electronic Structure Method on Inter- wavepacket dynamics with spin–orbit coupling: simula-
system Crossing Dynamics. The Case of Thioformalde- tion of thioformaldehyde, Physical Chemistry Chemical
hyde, Journal of Chemical Theory and Computation Physics 10.1039/d5cp04004c (2026).
10.1021/acs.jctc.9b00282 (2019). [114] V. Santolini, J. P. Malhado, M. A. Robb, M. Garavelli,
[100] Z. B. Maksi´c, D. Bari´c, and I. Petanjek, On the Corre- and M. J. Bearpark, Photochemical reaction paths of
lation Energy of π-Electrons in Planar Hydrocarbons, cis-dienes studied with RASSCF: the changing balance
TheJournalofPhysicalChemistryA10.1021/jp0015473 between ionic and covalent excited states, Molecular
(2000). Physics 10.1080/00268976.2015.1025880 (2015).
[101] N. O. J. Malcolm and J. J. W. McDouall, Combining [115] R. Say´os, C. Oliva, and M. Gonz´alez, The lowest dou-
MulticonfigurationalWaveFunctionswithDensityFunc- blet and quartet potential energy surfaces involved
tional Estimates of Dynamic Electron Correlation. 2. in the N(4S)+O2 reaction. I. Ab initio study of
Effect of Improved Valence Correlation, The Journal of the Cs-symmetry (2A′, 4A′) abstraction and inser-
Physical Chemistry A 10.1021/jp971605t (1997). tion mechanisms, The Journal of Chemical Physics
[102] Q. Meng and M.-B. Huang, CASSCF and CASPT2 10.1063/1.1381012 (2001).
Study on O- and Cl-Loss Predissociation Mechanisms [116] T. R. Scott, M. R. Hermes, A. M. Sand, M. S. Oak-
of OClO (A2A2), The Journal of Physical Chemistry A ley, D. G. Truhlar, and L. Gagliardi, Analytic gradi-
10.1021/jp110894v (2011). ents for state-averaged multiconfiguration pair-density
[103] M.F.S.J.MengerandH.Ko¨ppel,OntheFluorescence functional theory, The Journal of Chemical Physics
Properties and Nonradiative Transitions in Medium- 10.1063/5.0007040 (2020).
SizedAll-TransPolyenes,TheJournalofPhysicalChem- [117] L. Serrano-Andr´es, R. Pou-Am´erigo, M. P. Fu¨lscher,
istry A 10.1021/acs.jpca.3c03117 (2023). and A. C. Borin, Electronic excited states of conjugated
[104] T. Nakajima and S. Kato, Theoretical Study of the cyclicketonesandthioketones: Atheoreticalstudy,The
Effect of the Intermolecular Spin−Orbit Interaction in Journal of Chemical Physics 10.1063/1.1482706 (2002).
the Collision-Induced Intersystem Crossing of S1 State [118] S. Olsen, Canonical-ensemble SA-CASSCF strategy for
Glyoxal by Ar, The Journal of Physical Chemistry A problems with more diabatic than adiabatic states:
10.1021/jp012970u (2001). Charge-bondresonanceinmonomethinecyanines,arXiv
[105] Y. Nishimoto, Analytic First-Order Derivatives of preprint arXiv:1407.6063 (2014), arXiv:1407.6063.
CASPT2 Combined with the Polarizable Continuum [119] P. Sharma, V. Bernales, S. Knecht, D. G. Truhlar,
Model, Journal of Chemical Theory and Computation and L. Gagliardi, Density matrix renormalization group
10.1021/acs.jctc.4c01473 (2025). pair-density functional theory (DMRG-PDFT): singlet–
[106] J. M. Oliva, M. E. D. G. Azenha, H. D. Burrows, triplet gaps in polyacenes and polyacetylenes, Chemical
R.Coimbra,J.S.S.deMelo,M.C.L.,M.I.Ferna´ndez, Science 10.1039/c8sc03569e (2019).
J. A. Santaballa, and L. Serrano-Andr´es, On the Low- [120] T. Shiozaki, C. Woywod, and H.-J. Werner, Pyrazine
Lying Excited States of sym-Triazine-Based Herbicides, excited states revisited using the extended multi-state
ChemPhysChem 10.1002/cphc.200400349 (2005). completeactivespacesecond-orderperturbationmethod,
[107] D.Pela´ez,J.F.Arenas,J.C.Otero,andJ.Soto,Depen- Phys. Chem. Chem. Phys. 10.1039/c2cp43381h (2013).
dence ofN-Nitrosodimethylamine Photodecomposition [121] T.ShiozakiandT.Yanai,HyperfineCouplingConstants
ontheIrradiationWavelength: ExcitationtotheS2State from Internally Contracted Multireference Perturbation
as a Doorway to the Dimethylamine Radical Ground- Theory, Journal of Chemical Theory and Computation
State Chemistry, The Journal of Organic Chemistry 10.1021/acs.jctc.6b00646 (2016).
10.1021/jo070399a (2007). [122] P. E. M. Siegbahn, J. Alml¨of, A. Heiberg, and B. O.
[108] D.PicconiandS.Y.Grebenshchikov,Photodissociation Roos,ThecompleteactivespaceSCF(CASSCF)method
dynamicsinthefirstabsorptionbandofpyrrole.I.Molec- in a Newton–Raphson formulation with application to
ular Hamiltonian and the Herzberg-Teller absorption the HNO molecule, The Journal of Chemical Physics
spectrumfortheA21(πσ*)←X˜1A1(ππ)transition,The 10.1063/1.441359 (1981).
Journal of Chemical Physics 10.1063/1.5019735 (2018). [123] A. L. Sobolewski and L. Adamowicz, Ab initio charac-
[109] A. Ponzi, M. Sapunar, C. Angeli, R. Cimiraglia, terizationofelectronicallyexcitedstatesinhighlyunsat-
N.Doˇsli´c,andP.Decleva,Photoionizationoffuranfrom urated hydrocarbons, The Journal of Chemical Physics
the ground and excited electronic states, The Journal of 10.1063/1.469414 (1995).
Chemical Physics 10.1063/1.4941608 (2016). [124] J. Soto, D. Pel´aez, and J. C. Otero, A SA-CASSCF
[110] D. M. Potts, C. M. Taylor, R. K. Chaudhuri, and and MS-CASPT2 study on the electronic structure of
K. F. Freed, The improved virtual orbital-complete ac- nitrosobenzeneanditsrelationtoitsdissociationdynam-
tive space configuration interaction method, a “package- ics, The Journal of Chemical Physics 10.1063/5.0033181

16
(2021). states of OCLO radical, cation, and anion using the
[125] G.Stock,C.Woywod,W.Domcke,T.Swinney,andB.S. CASSCF/CASPT2 method, Journal of Computational
Hudson, Resonance Raman spectroscopy of the S1 and Chemistry 10.1002/jcc.20538 (2007).
S2 states of pyrazine: Experiment and first principles [131] Z. Xu, S. R. Federman, W. M. Jackson, C.-Y. Ng, L.-
calculation of spectra, The Journal of Chemical Physics P. Wang, and K. N. Crabtree, Multireference config-
10.1063/1.470689 (1995). uration interaction study of the predissociation of C2
[126] K. Sugisaki, K. Toyota, K. Sato, D. Shiomi, M. Kita- via its F1Π u state, The Journal of Chemical Physics
gawa, and T. Takui, Ab initio calculations of spin– 10.1063/5.0097451 (2022).
orbit contribution to the zero-field splitting tensors [132] M. C. Zammit, J. A. Leiding, J. Colgan, W. Even, C. J.
of nπ∗ excited states by the CASSCF method with Fontes, and E. Timmermans, A comprehensive study of
MRMP2 energy correction, Chemical Physics Letters theradiativepropertiesofNO—afirststeptowardacom-
10.1016/j.cplett.2009.07.007 (2009). pleteairopacity,JournalofPhysicsB:Atomic,Molecular
[127] P. C. Varras, P. S. Gritzapis, and K. C. Fylaktakidou, and Optical Physics 10.1088/1361-6455/ac8213 (2022).
Anexplanationoftheverylowfluorescenceandphospho- [133] P. Zhang, S. Irle, K. Morokuma, and G. S. Tschumper,
rescenceinpyridine: aCASSCF/CASMP2study,Molec- Ab initio theoretical studies of potential energy sur-
ular Physics 10.1080/00268976.2017.1371800 (2018). faces in the photodissociation of the vinyl radical. I.
[128] L. R. Ventura, R. S. da Silva, J. Amorim, and C. E. A˜ state dissociation, The Journal of Chemical Physics
Fellows, A new look at N 2 + electronic transitions: An 10.1063/1.1604378 (2003).
experimentalandtheoreticalstudy,JournalofMolecular [134] J. Zhang, W. Wu, L. Wang, X. Chen, and Z. Cao, Elec-
Spectroscopy 10.1016/j.jms.2024.111902 (2024). tronic Spectra of Linear Isoelectronic Clusters C2n+1S
[129] A.VenturiniandJ.Gonza´lez,ACASPT2andCASSCF and C2n+1Cl+ (n = 0−4): An ab Initio Study, The
Approach to the Cycloaddition of Ketene and Imine: A Journal of Physical Chemistry A 10.1021/jp063109n
New Mechanistic Scheme of the Staudinger Reaction, (2006).
The Journal of Organic Chemistry 10.1021/jo026188h
(2002).
[130] Z.-Z. Wei, B.-T. Li, H.-X. Zhang, C.-C. Sun, and
K.-L. Han, A theoretical investigation of the excited