| Harnessing |     |     | agent     |     | memory | to         | build | lifelong |     | AI  |
| ---------- | --- | --- | --------- | --- | ------ | ---------- | ----- | -------- | --- | --- |
| partners   |     | for | materials |     |        | scientists |       |          |     |     |
SiyuLiu1,2,∗,BoHu1,∗,BeilinYe1,∗,HeCao3,DavidJ.Srolovitz1,2,†,TongqiWen1,2,†
1 Center for Structural Materials, Department of Mechanical Engineering, The University of
| Hong | Kong, | Hong Kong, | China |     |     |     |     |     |     |     |
| ---- | ----- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
2
Materials Innovation Institute for Life Sciences and Energy (MILES), HKU-SIRI,
| Shenzhen,       |              | China   |         |         |     |                   |       |     |     |     |
| --------------- | ------------ | ------- | ------- | ------- | --- | ----------------- | ----- | --- | --- | --- |
| 3 International |              | Digital | Economy | Academy |     | (IDEA), Shenzhen, | China |     |     |     |
| ∗Equal          | contribution |         |         |         |     |                   |       |     |     |     |
Materials research advances through accumulated experience – scripts that work, protocols that are
trusted, warnings attached to failed calculations or experiments, and judgement that links a new
question to an old result. This experience is essential for reproducibility and knowledge transfer,
yet it is usually fragmented across notebooks, repositories, job logs and individual memory, and it
is rarely portable across artificial-intelligence agents. Here we argue that a lifelong AI partner for
6202 luJ 52  ]IA.sc[  1v42211.8062:viXra
materials science can be designed around persistent memory rather than around a particular agent
implementation. We introduce a self-evolving memory framework that stores scientific experience
as inspectable facts and executable skills, so that observations, failure boundaries, protocols and
validation checks can be retrieved, revised and migrated across models. We evaluate the idea in three
computational settings that expose different layers of materials-research competence. In 49 real-world
materials-tool-usequestionscomprising138executablesubtasks, memorynearlydoublesGPT-5.2task
success without model-parameter updates. In elemental-solid equation-of-state calculations, memory
converts a wavefunction-initialization failure into a pre-execution guardrail, improving outcomes from
22/1/4 to 25/2/0 Correct/Partial/Error and avoiding 92% of repeated errors. In 13 practical material
simulation workflows, remembered skills and failure facts halve the aggregate trace burden (tokens)
andreducetoolcallsbyoverafactoroftwobythethirdround,whilepreservingphysicallymeaningful
outputs in band-gap, phonon, vacancy and work-function analyses. These results show that agent
memory can serve as a durable scientific asset; a portable, self-improving record of materials-research
| experience    |     | that outlives | any single       | model | or agent | stack. |     |     |     |     |
| ------------- | --- | ------------- | ---------------- | ----- | -------- | ------ | --- | --- | --- | --- |
| Corresponding |     | authors†:     | tongqwen@hku.hk, |       |          |        |     |     |     |     |
srol@hku.hk
Introduction
|     |     |     |     |     |     | years,       | these experiences |     | crystallize | into scien-   |
| --- | --- | --- | --- | --- | --- | ------------ | ----------------- | --- | ----------- | ------------- |
|     |     |     |     |     |     | tific taste: | the ability       | to  | recognize   | opportunities |
The most valuable companion to a materials and/or suspicious results, choose a reliable pro-
scientist, as for all scientists, is not a single in- tocol and link a new question to an old lesson.
| strument, | a   | single database | or a | single | model; |          |               |     |          |                |
| --------- | --- | --------------- | ---- | ------ | ------ | -------- | ------------- | --- | -------- | -------------- |
|           |     |                 |      |        |        | The cost | of forgetting | is  | concrete | and recurring. |
it is accumulated research memory. A scientist In experimental materials research, noting that
learnsthefieldbyreadingpapers, attendingsem- a precursor must be dried longer than the pro-
| inars and | discussing | with | colleagues. | They | learn |               |      |           |           |           |
| --------- | ---------- | ---- | ----------- | ---- | ----- | ------------- | ---- | --------- | --------- | --------- |
|           |            |      |             |      |       | tocol states, | that | nominally | identical | annealing |
how the work is actually done by running calcu- schedules leave metastable phases unless the fur-
lations, synthesizing samples, debugging tools, nace is cooled in a particular way, or that a weak
writing scripts, preparing figures and discovering spectral feature is caused by surface prepara-
| which | apparently | reasonable | paths | fail. | Over |     |     |     |     |     |
| ----- | ---------- | ---------- | ----- | ----- | ---- | --- | --- | --- | --- | --- |

tion rather than by a distinct phase can decide facilities, atomic force microscopes and simula-
whether a research team spends days rediscov- tion pipelines under human-in-the-loop supervi-
ering a known trap or moves directly to the sion[22,23,24,25,26,27,28,29]. Theparadigm
scientific question. In computational research, has even been pushed to fully automated paper
the same pattern appears as reusable judgement writing [30], and reviews are starting to char-
about which settings make phase-stability com- acterize an emerging “generalist material intelli-
parisonsmeaningful,whichstructuresmustbere- gence” across these threads [31, 32, 33, 34]. To-
laxed before a vibrational or electronic-property gether, these advances make individual scientific
calculation is meaningful, and which recurring actions measurably faster and more autonomous.
failures are the result of numerical rather than Yet each effort is built around the agent rather
physical issues. Such memories are not merely than around what the agent has learned, so the
workflow conveniences: they determine whether operational knowledge produced inside one sys-
materials claims are comparable, reproducible tem rarely survives the next model release or
and credible. Yet today this memory lives in framework change. The closest attempts to ad-
the mind of the scientist, handwritten or digi- dress this are systems that move toward skill
tal notes, in code repositories, in failed-job logs acquisition or tool evolution: CASCADE consol-
and in analysed rather than raw data. The frag- idates memory through continuous learning and
mentsarepreciousbutdiscrete,unformattedand self-reflection [35] and test-time tool evolution
densely connected, which makes them difficult synthesizes executable tools as inference-time ar-
to retrieve at the moment of need and prone to tifacts [36]. Yet even these treat the agent as the
decay when research personnel move on, when carrier of progress; the accumulated experience
folders are reorganized, when models change or does not exist as an inspectable, portable object.
when the original context is forgotten.
The open problem is therefore not whether
The recent wave of artificial intelligence has agents can act faster or accumulate tools inside
dramatically accelerated individual steps of the one framework, but whether the experience of
materials-research loop. Autonomous agents can the scientist—operational knowledge that car-
now plan and execute end-to-end chemical syn- ries provenance, boundary conditions and fail-
thesis[1,2,3],mobileroboticmaterialsscientists ure history—can persist across models, projects
can drive multi-instrument self-driving labora- and the inevitable framework evolution. The
tories such as A-Lab [4, 5, 6], and multi-agent distinction is important: a tool or skill can en-
stacks can coordinate literature reading, exper- code how to perform a procedure, whereas re-
imental design and hardware execution on de- search experience also includes the conditions
mand [7, 8]. Predictive and generative models under which a procedure is trustworthy, which
have expanded the known space of stable phases failure produced a warning, what evidence sup-
(by an order of magnitude), unlocked control- ports the validity of a boundary condition and
lable inverse design, and been transferred to whether another model or project should inherit
alloy, macromolecule and inorganic-compound it. Three structural problems converge. First,
generation [9, 10, 11, 12, 13, 14]. On the com- theagentistreatedastheunitofprogress: when
putational side, multi-agent frameworks weave a stronger foundation model arrives, or when
LLM reasoning, knowledge graphs and physics- the orchestration framework changes, the oper-
aware simulations for applications in alloy de- ational knowledge accumulated inside the pre-
sign, proteindiscovery, metal–organicframework vious agent—what works with a given machine
prediction, organic-semiconductor optimization learningpotential, whereagivenDFTfunctional
and broader multi-task computational materi- fails, which k-point sampling is a sufficient an-
als science [15, 16, 17, 18, 19, 20, 21], while chorforaclassofcompounds—doesnotautomat-
DFT- and interatomic-potential-oriented agents ically migrate, and there is no consensus on how
automate large parts of atomic-scale workflows, to even quantify “what the system has learned”
and tool-augmented agents now operate user across runs of a self-driving lab [37]. Second,
2

large language models hallucinate confidently sandbox-grounded feedback.
and inconsistently [38, 39], so a one-off conver-
Figure 1 places this design in a single diagram;
sation history cannot be trusted as a knowledge
i.e.,anagentacquiresexperiencesfromrealtasks,
source without explicit verification, and recent
consolidatesthemintohuman-readablefactsand
benchmarks of LLM agents on real laboratory
skills, and retrieves or updates them when a new
instruments show that even strong models fail
problem appears, with execution-feedback clos-
to translate domain question-answering ability
ing the loop. Figure 1d shows the resulting rep-
into reliable execution [25]. Third, when the
resentation on a concrete VASP phonon failure
model itself is updated, naive continual learn-
– the observed imaginary mode, the maximum
ing causes catastrophic forgetting of previously
force of 0.56 eV/Å and the recommendation to
acquired domain skills [40]. Existing agent-side
relax before DFPT are stored as a fact with
memories address only fragments of this need:
job provenance, while the corresponding skill
chains of thought retained inside a single tra-
records DFT relaxation followed by a Gamma-
jectory [41], verbal post-mortems written after
point DFPT phonon calculation, together with
a failed attempt [42], environment-specific code
HPC submission details and failure alerts.
skillsindexedbyembedding[43],OS-stylevirtual
context paging [44], or episodic logs designed for We instantiate this design as a memory-centric
plausible behaviour in a sandbox [45]. None of agent for computational materials research and
these treat scientific memory as a first-class arti- probe three layers of materials competence: exe-
fact: human-readable, peer-editable, provenance- cutable tool use, atomistic-simulation reliabil-
linked, model-agnostic and portable across the ity and practical workflow reuse. For exam-
agent stacks that come and go. ple, in the real-world tool-use subset of Mat-
Tools [46] (49 pymatgen.analysis.defects
We therefore reframe the issue. The lasting con-
questions, 138 evaluated subtasks), memory
tribution of these tools for a scientist is not the
raises the GPT-5.2 task success rate from 44.2%
agents, but the memory that outlives the agents
to75.4%overthreeroundswithoutchangingany
and the nature of the research workflow that is
model parameters, and a memory produced by
sufficiently rich to take advantage of this mem-
GPT-5.4transferstoaweakerGPT-5.4-nanostu-
ory(ratherthana, forexample, flatconversation
dent with a 50.8% gain over the student model’s
log). The core object in our framework is a self-
own three-round memory. On Sol27LC [47], a
evolving knowledge base composed of two com-
recurring wavefunction-initialization failure in
plementary, textual artifacts. Facts are stored
ABACUS (DFT) equation-of-state fitting is cap-
scientific observations, warnings, interpretations
tured once and avoided in 91.7% of subsequent
andboundaryconditions; e.g.,averifiedmachine
cases across structurally related families. In 13
learning potential for particular applications, a
VASP (DFT) and LAMMPS (molecular dynam-
documented convergence failure, or a calibrated
ics) workflows covering band-gap, phonon, va-
reference value. Skills are stored, reusable pro-
cancy and work-function calculations, retrieved
cedures, scripts, protocols and checklists; e.g.,
facts and skills halve aggregate token use by the
a relax-then-DFPT (density functional pertur-
third round while preserving physically meaning-
bation theory) workflow, an EOS-fit script, or
fuloutputs. Togetherthesesettingsdemonstrate
a slab work-function pipeline. Both are human-
that memory is not a benchmark trick but a
readable and provenance-linked; e.g., a scientist
durable carrier of executable materials-research
can inspect what the agent saved, edit it, version
experience across tasks, sessions and models.
it across projects, and migrate it to a stronger
model when one becomes available. This po-
sitions memory itself as a long-lived scientific
asset (closer to a laboratory protocol than to a
model weight) and the agent as an interface that
reads, executes and updates that asset under
3

(a)
Successful experiences
|     |     | Literature Notes |                  |     | Scientific taste |     |           |     |     |
| --- | --- | ---------------- | ---------------- | --- | ---------------- | --- | --------- | --- | --- |
|     |     |                  | Failureguardrail |     |                  |     | Materials |     |     |
Graduate
| student |     |             |                  |     |     |              | scientist |     |     |
| ------- | --- | ----------- | ---------------- | --- | --- | ------------ | --------- | --- | --- |
|         |     | Early stage | Developing stage |     |     | Mature stage |           |     |     |
Ideallifelong materials research experiences
(b)
|     |     |     |     | Instructionfollowing |           |     |     | Tracessummary     |     |
| --- | --- | --- | --- | -------------------- | --------- | --- | --- | ----------------- | --- |
|     |     |     |     |                      | Toolusing |     |     | Experiencesreplay |     |
|     |     |     |     | Structured output    |           |     |     | Skillsupdating    |     |
AI: Strong execution, but no mechanism for
Human:Continuous self-evolution, but fragmented experience
test-timeknowledgeaccumulation
(c)
| Phase 1: Experience Acquisitionfrom |            |     | Phase 2: Memory Formation & Evolution |     |     |     | Phase 3: Memory-Driven  |     |     |
| ----------------------------------- | ---------- | --- | ------------------------------------- | --- | --- | --- | ----------------------- | --- | --- |
|                                     | Real-world |     |                                       |     |     |     | Problem Solving         |     |     |
Retrieve
|     | Humaninstruction |     |     |     |     |     | Newquestion |     |     |
| --- | ---------------- | --- | --- | --- | --- | --- | ----------- | --- | --- |
Literature
|           |     | HPCjobs |     |               |     |     |     | Reusable |     |
| --------- | --- | ------- | --- | ------------- | --- | --- | --- | -------- | --- |
| knowledge |     |         |     | Knowledgebase |     |     |     | scripts  |     |
(facts+skillsmemory)
Standardized
docs
Validated
| D a ta  |      | Environmentfeedback |       |                        |     | Delete |             | p r o t oc | o l    |
| ------- | ---- | ------------------- | ----- | ---------------------- | --- | ------ | ----------- | ---------- | ------ |
| an a ly | sis  | A I                 |       |                        |     |        | Re l at e d |            |        |
|         |      |                     | Reuse |                        |     |        | m e m o r y | So l v e d | t a sk |
|         | scie | n tist              |       | Successful experiences |     |        |             |            |        |
|         |      |                     |       | Failureguardrail       |     |        |             | results    |        |
Experiencetraces
Create
Other
|     | Insights | Consolidation machine |     |     | Update |     | AIscientists | Human |     |
| --- | -------- | --------------------- | --- | --- | ------ | --- | ------------ | ----- | --- |
migrate
👉Solution: Memory-centric agent with structured, evolving knowledge
→ A lifelong research partner for materials scientists
| (d)               |     |     |     |     | (e)              |     |     |     |     |
| ----------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- |
| Factmemoryexample |     |     |     |     | (cid:18)(cid:10) |     |     |     |     |
Meta-info:job vasp_si_dfpt_gamma_fix(job_group_id:16030862) (cid:17)(cid:15)(cid:9)(cid:14)
(cid:17)(cid:15)
-What happened
Phonon shows imaginary mode → structure unstable
| -Why suspicious                      |     |     |     |     | (cid:17)(cid:10)                                                                                                                       |     | (cid:16)(cid:18)(cid:9)(cid:18) |     |     |
| ------------------------------------ | --- | --- | --- | --- | -------------------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------------- | --- | --- |
| Max force = 0.56 eV/Å(not converged) |     |     |     |     | (cid:6)(cid:4)(cid:5)(cid:3)(cid:33))(cid:29)(cid:26)(cid:3)(((cid:33)(cid:31)(cid:31)(cid:42)(cid:27)(cid:3)(cid:34)((cid:29)(cid:28) |     |                                 |     |     |
| -What to do next                     |     |     |     |     | (cid:16)(cid:15)                                                                                                                       |     |                                 |     |     |
(cid:16)(cid:12)(cid:9)(cid:13)
| Relax structure before phonon calculation |     |     |     |     |                                                  |     | (cid:15)(cid:19)(cid:9)(cid:14) |     | (cid:16)(cid:10)(cid:9)(cid:11) |
| ----------------------------------------- | --- | --- | --- | --- | ------------------------------------------------ | --- | ------------------------------- | --- | ------------------------------- |
| Skillexample                              |     |     |     |     | (cid:16)(cid:10) (cid:15)(cid:18)(cid:9)(cid:17) |     |                                 |     |                                 |
Description: Robust two-stage VASP workflow for physically correct Si  (cid:15)(cid:15) (cid:15)(cid:17)(cid:9)(cid:12) (cid:15)(cid:18)(cid:9)(cid:10) (cid:21)(cid:42)(cid:35)(cid:35)(cid:3)(cid:27)(cid:44)()(cid:33)(cid:36) (cid:15)(cid:18)(cid:9)(cid:17)
| diamond Γ optical phonon:relax to true minimum then compute Γ |     |     |     |     |     |     |     | (cid:7)(cid:27)(cid:29)% (cid:30)(cid:38)+(cid:3)(cid:38)%(cid:35)(cid:44) |     |
| ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------------------------------- | --- |
phonons via DFPT, avoiding spurious imaginary modes.
|     |     |     |     |     | (cid:15)(cid:10) |     |     | (cid:7)(cid:24)(cid:33)(cid:36)(cid:38)(cid:39)(cid:44)(cid:3)(cid:38)%(cid:35)(cid:44) |     |
| --- | --- | --- | --- | --- | ---------------- | --- | --- | --------------------------------------------------------------------------------------- | --- |
Stage A: Relaxation AdditionalInfo: (cid:20)(cid:29)(cid:39)(cid:33)(cid:3)(cid:23)(cid:23)(cid:24)(cid:3)(cid:5)(cid:22)(cid:25)(cid:28)(cid:8)(cid:15)(cid:9)(cid:12)(cid:6)
| [detailedparameters] |     | -Bohrium(HPC)submissionfileformat |     |     | (cid:14)(cid:15) (cid:14)(cid:14)(cid:9)(cid:12) |     |     |     |     |
| -------------------- | --- | --------------------------------- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- |
-Calculationexamples
StageB:DFPT Γ phonons
| ( o n   re l a xe | d   C O N T C A | R) - P a s t r e a l e x e c | u tio ntracessummary |     | (cid:14)(cid:10) |     |     |     |     |
| ----------------- | --------------- | ---------------------------- | -------------------- | --- | ---------------- | --- | --- | --- | --- |
[d e t a il e d p a r a m et e rs ] - Fa i lu r e   m o d e   a le rt (cid:26)(cid:11) (cid:26) (cid:12) (cid:26)(cid:13)
|     |     |     |     |     |     |     | (cid:26)(cid:38) (cid:42) %  |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- |
Figure 1 - Memory-centric self-evolving agent for lifelong materials research. (a) Materials scientists
develop judgement by accumulating literature, notes, successful experiences, failure guardrails and scientific
taste. (b) Human experience is cumulative but fragmented, whereas current AI agents execute strongly but
usually lack a mechanism for test-time knowledge accumulation. (c) A memory-centric agent acquires
experience from real tasks, consolidates it into structured facts and skills, and retrieves it for new problems.
(d) Examples of fact-memory and skill-memory from a VASP phonon workflow, including job provenance,
failure diagnosis, recommended action, DFT relaxation followed by a DFPT phonon calculation and HPC
execution notes. (e) Three-round task-success trends on the MatTools materials-tool-use benchmark show
that full memory evolution improves GPT-5.2 from 62.3% to 75.4%, beyond sandbox-only and memory-only
variants.
4

A memory format for lifelong ence value is stored as boundary-knowledge the
agent can consult, not as the answer it should
materials research
report. This distinction may be seen in the
practical-workflow cases below.
A lifelong partner for a materials scientist must
remember more than documents; it should re-
A useful representation is one that is intention-
member concepts, decisions, partial attempts,
ally textual and provenance-linked. A text mem-
failed boundaries, successful protocols, scripts,
ory is not bound to the weights of one model,
parameters and the reasoning that connects
the schema of one software stack or the inter-
them. Weusetwocomplementarymemorytypes
face of one agent; rather, it can be embedded
to span this spectrum. Fact-memory stores com-
for retrieval, linked in a graph, inspected by a
pact scientific statements: what happened, in
human, edited, exported to another system or
what context, why it matters, what evidence
reused by a future model. The same representa-
supports it and what should be done next. Skill-
tion evolves with execution feedback; failed runs
memory stores actionable know-how: a goal, ap-
create guardrails, successful runs create skills,
plicability conditions, prerequisites, a procedure,
and partially successful runs revise existing pro-
code or parameter notes, validation checks, fail-
cedures after sandbox, job or output validation,
ure modes and provenance links to the traces
so the memory store grows as a curated trace of
that created or revised the skill.
what has been verified rather than as a passive
log of what has been said.
This separation in memory types matters be-
cause scientific experience is not uniform. Ma-
terials research generates two complementary Quantifying memory growth in a
classes of knowledge that should be remembered
controlled test bed
in different forms. Boundary-knowledge records
where a method, parameter or interpretation
Can memory improve executable materials-tool
ceases to be trustworthy: an unrelaxed Si struc-
use without updating model parameters? This
ture that produces an imaginary DFPT phonon,
is the first capability a practical materials agent
a default wavefunction initialization that pre-
must acquire – not simply answering ques-
vents SCF convergence, a pseudopotential en-
tions about materials science, but selecting
ergy cut-off below which energies drift, or a
APIs, writing code, satisfying structured out-
calibrated lattice constant that should be con-
put contracts and repairing errors after execu-
sulted as a reference rather than reported as a
tion. We therefore use the real-world tool-use
newmeasurement. Procedural-knowledge records
subset of MatTools [46]: 49 questions from the
the executable know-how that the scientist has
pymatgen.analysis.defectstestsuite, decom-
gained; e.g., a relax-then-DFPT protocol, an
posed into 138 evaluated subtasks covering de-
EOS-fit script, a slab work-function pipeline,
fect construction, vacancy, interstitial and sub-
the sandbox-validated code fragment that turns
stitution generators, supercell matching, charge-
these protocols into reproducible outputs. Con-
density and local-extrema analysis, formation-
flating the two is a recurring source of error in
energydiagrams,electrostaticcorrections,defect-
agenttraces–aprocedurethatrunsiseasilymis-
state localization, and radiative or Shockley–
taken for a procedure that is trustworthy. We
Read–Hall recombination calculations – the full
therefore route boundary-knowledge into facts
question-level explanation is provided in Supple-
and procedural-knowledge into skills – facts pre-
mentary Table 1. This subset is well suited to
serve context, skills preserve ordered procedures,
memoryevaluationbecausemanyfailurescannot
parameters and validation checks, applicability
be repaired through correcting scientific vocab-
conditions and cautions. Together they enable
ulary alone; they involve API selection, output
the system to remember both what to do and
schemas, numerical conventions and code that
what not to do. In particular, a calibrated refer-
must actually run.
5

Figure 2a compares bare-model performance Figure2cplotstask-successimprovementagainst
across several frontier and smaller language mod- (additional) median token-use relative to bare
els. The three bars separate question pass models, with dashed reference lines reporting
rate over the 49 top-level questions, task suc- efficiency in percentage points of task-success
cess rate over the 138 evaluated subtasks, and gain per 1,000 additional median tokens. This
executable-function reliability, which range from improvement is not free – retrieval, validation
20.4–53.1%, 23.2–66.7% and 40.8–89.8% across and memory updates add context. GPT-5.4
the bare-model cohort, respectively. Larger mod- and GPT-5.2 occupy the high-gain region but
els generally achieve higher values on all three at different token costs: GPT-5.4 gains 21.0–
metrics,butevenstrongmodelsleavesubstantial 21.7 percentage points in R2–R3 with about
room for execution-level improvement: GPT-5.4 1.3×104 additional median tokens per question,
achieves an 89.8% function runnable rate, yet its whereas GPT-5.2 gains 24.6–31.2 points with
4×103–5×103
low task-success and question-pass rates, 66.7% only additional tokens. Thus,
and 53.1%, indicate that runnable code alone although GPT-5.4 achieves a higher final task-
does not guarantee a correct scientific answer. success rate than GPT-5.2 (88.4% versus 75.4%
We then compare each bare model with the full inR3),GPT-5.2usesmemorysubstantiallymore
memory-centric system across three rounds. A efficiently, achieving 6.05–6.45 percentage points
round is one complete pass over the same 49- oftask-successimprovementper1,000additional
question tool-use set – R1 is a cold-start full- tokens, compared with 1.59–1.69 for GPT-5.4.
system pass and R2/R3 can retrieve memory Smaller models show weaker or even negative
accumulated from earlier passes – no model pa- movement in some rounds, indicating that ex-
rameters were trained between rounds. Gains tra memory simply becomes overhead when the
are largest where the baseline has enough com- target model cannot operationalize it and that
petence to produce useful traces but still makes the relevant axis for choosing a memory-enabled
repeatedtool-usemistakes. Figure2bshowsthat configurationisgainperaddedtokenratherthan
| GPT-5.2    | improves |       | from a | bare task-success |              | rate    | gain alone. |     |             |     |         |     |
| ---------- | -------- | ----- | ------ | ----------------- | ------------ | ------- | ----------- | --- | ----------- | --- | ------- | --- |
| of 44.2%   | to       | 75.4% | after  | three rounds,     |              | GPT-5.4 |             |     |             |     |         |     |
| improves   | from     | 66.7% | to     | 88.4%,            | GPT-5.4-mini |         |             |     |             |     |         |     |
|            |          |       |        |                   |              |         | Memory      |     | can migrate |     | between |     |
| rises from | 39.1%    | to    | 49.3%, | GPT-5.4-nano      |              | from    |             |     |             |     |         |     |
models
| 31.2%         | to 33.3% | and  | Qwen3.5-397B |                | from     | 26.1% |            |          |               |               |            |        |
| ------------- | -------- | ---- | ------------ | -------------- | -------- | ----- | ---------- | -------- | ------------- | ------------- | ---------- | ------ |
| to 33.3%.     | Smaller  |      | models       | therefore      | benefit, | but   |            |          |               |               |            |        |
|               |          |      |              |                |          |       | A lifelong | research | memory        | should        | outlive    | any    |
| less reliably | when     | they | cannot       | operationalize |          | the   |            |          |               |               |            |        |
|               |          |      |              |                |          |       | particular | agent.   | This          | is especially | urgent     | today, |
| retrieved     | memory.  |      |              |                |          |       |            |          |               |               |            |        |
|               |          |      |              |                |          |       | because    | agent    | architectures | and           | foundation | mod-   |
The ablations in Figure 1e clarify why the full elschangequickly; asystemdesignedaroundone
system matters. Sandbox-only execution im- model may be obsolete when the next model is
| proves    | robustness | by         | catching | errors    | but      | rarely |               |                |                |     |               |         |
| --------- | ---------- | ---------- | -------- | --------- | -------- | ------ | ------------- | -------------- | -------------- | --- | ------------- | ------- |
|           |            |            |          |           |          |        | released,     | while          | a well-written |     | protocol,     | warning |
| preserves | the        | correction |          | for later | sessions | and    |               |                |                |     |               |         |
|           |            |            |          |           |          |        | or scientific | interpretation |                | can | remain useful | for     |
memory-only operation can recall prior notes years. We tested this portability by allowing one
but without execution feedback risks retaining model to use memory generated by another.
| incomplete  | or  | incorrect | procedures. |         | The    | full sys- |                |     |              |        |           |      |
| ----------- | --- | --------- | ----------- | ------- | ------ | --------- | -------------- | --- | ------------ | ------ | --------- | ---- |
|             |     |           |             |         |        |           | The resulting  |     | transfer     | matrix | in Figure | 2d   |
| tem couples |     | both –    | sandbox     | signals | decide | what      |                |     |              |        |           |      |
|             |     |           |             |         |        |           | is asymmetric, |     | as expected. |        | Memories  | from |
shouldbetrustedandmemorycarriesthetrusted
|            |          |              |     |           |             |       | stronger  | source   | models       | often  | help weaker | ones   |
| ---------- | -------- | ------------ | --- | --------- | ----------- | ----- | --------- | -------- | ------------ | ------ | ----------- | ------ |
| correction | forward. |              | The | result is | a gradual   | rise  |           |          |              |        |             |        |
|            |          |              |     |           |             |       | more than | memories | from         | weaker | sources     | help   |
| from 62.3% |          | to 75.4%     | for | GPT-5.2   | over        | three |           |          |              |        |             |        |
|            |          |              |     |           |             |       | stronger  | targets. | For example, |        | GPT-5.4     | memory |
| rounds,    | while    | sandbox-only |     | and       | memory-only |       |           |          |              |        |             |        |
variants stay between 57% and 60%. raises GPT-5.4-nano performance by 50.8 per-
centagepointsoverthenanomodel’sR3memory
Memory also changes the economics of tool use. and improves GPT-5.4-mini by 35.5 percentage
6

|     | (a) |     |     |     |     |     | (b) |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:23)(cid:25)(cid:29)(cid:7)(cid:14)(cid:8)(cid:13)
(cid:23)(cid:34)(cid:39)(cid:36)((cid:36)(cid:7)(cid:12)(cid:8)(cid:10)(cid:7)(cid:25)(cid:42))
(cid:23)(cid:25)(cid:29)(cid:7)(cid:14)(cid:8)(cid:11)
(cid:23)(cid:25)(cid:29)(cid:7)(cid:14)(cid:8)(cid:13)(cid:7)(cid:39)(cid:36)((cid:36)
(cid:26).(cid:34)((cid:12)(cid:7)(cid:24)(cid:30)(cid:47)
(cid:23)(cid:25)(cid:29)(cid:7)(cid:14)(cid:8)(cid:13)(cid:7)((cid:30)()
(cid:26).(cid:34)((cid:12)(cid:8)(cid:14)(cid:7)(cid:12)(cid:18)(cid:16)(cid:20)(cid:7)(cid:19)(cid:10)(cid:16)(cid:20)
|     | (cid:21)(cid:38)(cid:30)-(cid:33)(cid:34)(cid:7)(cid:28))(((cid:34)(cid:44)(cid:7)(cid:13)(cid:8)(cid:15) |     |     |     | (cid:26) - (cid:34) (cid:43) (cid:44)(cid:36)) ( (cid:3)(cid:25) (cid:30) (cid:43) (cid:43) | (cid:3)(cid:27) (cid:30) (cid:44)(cid:34) |     |     |     |     |     |     |     |
| --- | --------------------------------------------------------------------------------------------------------- | --- | --- | --- | ------------------------------------------------------------------------------------------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |                                                                                                           |     |     |     | (cid:29)(cid:30) (cid:43) % (cid:3)(cid:28) -    (cid:34) (cid:43) (cid:43)                 | (cid:3)(cid:27) (cid:30) (cid:44)(cid:34) |     |     |     |     |     |     |     |
(cid:22)-( (cid:44)(cid:36))((cid:3)(cid:27)-(((cid:30)(cid:31)(cid:38)(cid:34)(cid:3)(cid:27)(cid:30)(cid:44)(cid:34)
|     |     | (cid:9) (cid:11)(cid:9) | (cid:13)(cid:9) | (cid:15)(cid:9) | (cid:17)(cid:9) | (cid:10)(cid:9)(cid:9) |     |     |     |     |     |     |     |
| --- | --- | ----------------------- | --------------- | --------------- | --------------- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
(cid:25)(cid:34)(cid:42) (cid:34)((cid:44)(cid:30)(cid:35)(cid:34)(cid:3)(cid:5)(cid:4)(cid:6)
|     | (c) |     |     |     |     |     | (d) |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 2 - MatTools benchmark performance and memory-driven improvements across LLMs. (a)
Comparison of question pass rate over 49 top-level questions, task success rate over 138 evaluated subtasks,
and function runnable rate across models on the real-world tool-use subset of MatTools. (b) Task-success rate
improvement from bare LLM to the full system across R1–R3. R1 is a cold-start full-system pass; R2 and R3
reuse memory accumulated from previous passes, with model parameters fixed throughout. (c) Trade-off
between task-success gain and additional median token use relative to bare LLM execution; larger markers
indicate later rounds. Absolute token increments are shown because they quantify the additional
computational cost directly and support the efficiency contours expressed as percentage-point gains per 1,000
additional tokens. (d) Cross-model memory transfer. Off-diagonal cells report the change in target-model
task-success rate when using memory produced by a source model after its own three-round run, relative to
the target model’s R3 memory; diagonal cells show each model’s R3 task-success rate.
points. Conversely, memories from smaller mod- model can therefore be reused by a cheaper or
elscanbeneutralorharmfulforstrongertargets, smaller model when the skill is written in exe-
because the stored procedures encode narrower cutable, inspectable form. The memory object
or less reliable reasoning. behaves more like a scientific protocol than a
|                   |              |              |        |               |            |         | hidden         | model       | weight;     | it can      | be read,   | checked,      |          |
| ----------------- | ------------ | ------------ | ------ | ------------- | ---------- | ------- | -------------- | ----------- | ----------- | ----------- | ---------- | ------------- | -------- |
| This portability  |              | is important |        | in practice   | because    |         |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | edited and     | migrated    | across      | models,     |            | architectures |          |
| materials         | laboratories | rarely       | have   | uniform       |            | access  |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | and systems.   |             | The same    | approach    |            | also          | exposes  |
| to the same       | compute,     | model        | or     | expertise.    |            | It also |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | a limitation.  |             | Cross-model | transfer    |            | is not        | auto-    |
| resembles         | knowledge    | transfer     |        | within        | a research |         |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | matically      | beneficial; | several     |             | cells are  | near          | zero or  |
| group; validated  |              | operational  |        | know-how      | survives   |         |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | negative       | when        | the source  | memory      | is         | less          | reliable |
| personnel         | turnover     | only         | when   | it is written |            | down    |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | than the       | target’s    | own         | experience. |            | Portability   |          |
| as an inspectable |              | protocol     | rather | than          | left       | in the  |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | must therefore |             | be paired   | with        | provenance |               | and      |
| mind of           | a single     | individual.  | A      | validated     | skill      | pro-    |                |             |             |             |            |               |          |
|                   |              |              |        |               |            |         | validation     | rather      | than        | treated     | as blind   | imitation.    |          |
| duced during      |              | an expensive | run    | with          | a stronger |         |                |             |             |             |            |               |          |
7

Mechanisms behind memory gains can retrieve and execute.
The aggregate gains are easiest to read through
Preventing repeated failures
execution traces. Figure 3 shows three mecha-
nismsbywhichmemorychangesthelifecycleofa
Can memory prevent repeated failures in a work-
scientific task; direct same-task reuse, feedback-
flow? Consider the case of a standard atomistic-
grounded repair and teacher-to-student transfer.
simulation workflow: i.e., the calculation of the
In the first case, the task asks for local extrema equation-of-state from lattice-constant fitting
in a GaN charge-density grid. The first round from DFT calculations (this is known to be
is exploratory; the system searches memory and very sensitive to input preparation, pseudopo-
skills, consults external sources, extracts pages, tential compatibility, unit conventions, SCF con-
plans the task and validates the code. A useful vergence and fit validation). We evaluated this
result is not only an answer but the memory dis- framework on Sol27LC, a benchmark of 27 cu-
tilled from the attempt; get_local_extrema is bic elemental solids with experimental lattice
anAPIforextractingfractionalcoordinatesfrom constants spanning face-centered cubic (FCC),
a CHGCAR, and the workflow should read CHGCAR, body-centered cubic (BCC) and diamond crystal
call the Pymatgen function and return the ex- lattices [47]. Each case computes an equilibrium
trema. In later rounds this memory turns an lattice constant through DFT equation-of-state
exploratory task into a short reusable procedure; fitting performed with ABACUS [48], an open-
46.6k tokens and 11 tool calls in R1 collapse to source DFT software package and less familiar
about 5k tokens and 4 tool calls in R2 and R3. to general-purpose language models than com-
moncode-analysislibraries. Caseswiththesame
In the second case, the task is to analyse a point-
crystal structure share a memory system. The
defect structure with Pymatgen. The first round
first case in each family is a cold start (FCC
is only partially correct; sandbox review exposes
Cu, BCC Li and diamond C), and later cases
textual-output errors, including string keys in
reuse memories and skills accumulated within
element_changes and non-boolean defect clas-
that family. The experiment therefore isolates
sifiers. Instead of treating this as a disposable
whether a memory system can preserve a cal-
failure, the system saves a correction and up-
culation failure as an actionable guardrail and
dates the skill. The second round exposes one
prevent its recurrence on chemically distinct yet
remaining schema problem, which is again con-
structurally related materials.
solidated. By the third round, the corrected
memory succeeds. This case illustrates why a Figure 4a shows the result. In the first round,
lifelong memory must store failures as well as the 27 cases yield 22 Correct, 1 Partial and 4
successful protocols. Error outcomes. Correct means the fitted lattice
constant deviates by less than 5% from experi-
The third case probes whether a memory can
ment. Partial denotes a scientifically valid EOS
act as a transferable scientific object. A GPT-
calculation with the correct physical result, but
5.4-mini student fails to fully reconstruct a
with the final lattice constant reported in the
formation-energy diagram for Mg_Ga-in-GaN
wrong unit (ABACUS uses Bohr-units internally,
substitutional point defects even after three self-
whereas the experimental references are in Å).
rounds. A GPT-5.4 teacher succeeds and saves
Error denotes failed runs or large deviations. Af-
a skill describing formation-energy diagram con-
ter Round 2 reruns with accumulated memory,
struction, the shifted y-coordinate handling and
all Error cases are removed and the outcome dis-
a repository-relative validation workflow. When
tribution improves to 25 Correct, 2 Partial and 0
the student uses the teacher memory, it solves
Error. Within the crystal lattice structure fam-
the task in one round. The improvement is not
ilies, FCC improves from 8/1/3 to 10/2/0 Cor-
bound to the teacher model itself; it is carried by
rect/Partial/Error, BCC improves from 10/0/1
a validated textual procedure that the student
8

(a)CASE1–Sametaskmemoryreuse (b)CASE2–Environmentfeedback-groundedcorrection
Question:Calculate the list of local extremum point Question:Analyze a point defect structurewith Pymatgen, report its composition
coordinates in the given charge density gridofGaN. change, and classify it as substitutional or vacancy.
Model:GPT5.2 Model:GPT5.4-mini
Round1 sandboxcodereview Round1 error2/4
✅validationpassed ❌element_changesused string keys:{'Mg': 1, 'Ga': -1}
external exploration defect_inequality(refers to the judgment of defect types)was not a strict bool
memory + skill search, ❌
i e n x t t e r r a n c e ts t , s p e l a a r n c n h i e n s g , t p a a s g k e s lo a c v a e l-e m x e tr m em or a y c a a n lc d .w sk o i r l k l flow explore s pa a r n tia d l b re o s x ul c t o ex d p e os r e e s v t i y e p w ed errors s pr a e v s e erv m e e E m lem or e y nt a k n e d ys u ,b p o d o a lo te utp s u k t i s ll
Fact:get_local_extremais the correct API for extracting Round2 error1/4
local-extrema fractional coordinates from aChgcar. searchmemoryandskill sandboxcodereview
Skill:Steps to compute local charge-density extrema ❌remaining error:defect_string_representationwas not a string
positionsusingpymatgen: new fact: string representation must be validated as plainstr
ReadCHGCAR->UsePymatgenfunction->Getresult
updateskillandremoveolddescription
Round2,3
Round3 success
searchmemoryandskill reuse success
searchmemoryandskill reuse success
Tracemetrics
R1 R2 R3 Tracemetrics
tokens 46.6k 5.0k 5.1k R1 R2 R3
toolcalls 11 4 4 tokens 9.2k 8.0k 4.8k
outcome ✅ ✅ ✅ outcome partial partial ✅
(c)CASE3–Cross-modelmemorytransfer
Question:Reconstruct the Mg_Ga-in-GaNdefect formation-energy diagram (FED) from DFT
outputs and return the transitionpoint coordinates across chemical-potential limits.
Teacher:GPT5.4 Student:GPT5.4-mini
Studentmodel: Teachermodel:
R1:partial R2:failed R3:partial R1/R2/R3: savememoryandskill
y_coordinatesfalse FunctionError y_coordinatesfalse success Stepstobuild and validate FED
Thestudentmodeldoesn’tfullysolvethetaskafterthreerounds. The teacher model succeeded in just one round.
Studentmodelwithteachermemory: successinoneround What the student receives?
formation-energy diagram skill for Mg_Ga-in-GaNcoordinates
searchmemoryandskill reuse success
shifted y-coordinate handling
Skill:reads the Mg_Ga-in-GaNdataset ... constructs a FED... verifies transition repository-relative test-file workflow already validated by source model
x-coordinates and minimum-shifted y-coordinates…
Figure 3 - Execution-level mechanisms behind memory gains. (a) Same-task memory reuse turns an
exploratory first run into short later executions by retrieving saved API facts and workflow skills. (b)
Feedback-grounded correction converts sandbox errors into memory facts and skill updates, progressively
repairing concrete implementation mistakes. (c) Cross-model memory transfer lets a student model solve a
previously unsolved formation-energy diagram task by reusing a teacher model’s validated skill and
supporting facts.
to 11/0/0, and diamond remains 4/0/0. trieve it before execution and avoid the same
convergence failure in 90.9% of the FCC cases,
The case study in Figure 4b explains how this
90.0% of the BCC cases and 100.0% of the di-
aggregate improvement arises. In the cold-start
amond cases (right panel in Figure 4a). The
cases, self-consistent field (SCF) calculations
overall avoided-error rate is 91.7%, measuring
with SG15 ONCV pseudopotentials [49] can fail
whether cases avoid the repeated wavefunction-
under the default wavefunction initialization.
initialization failure rather than whether every
The useful correction is simple but operationally
final report is free of formatting or unit mis-
specific; i.e., set init_wfc=random before run-
takes. The unit of generalization is the crystal
ningABACUS.Oncethisinterventionisdistilled
structural family: a fix discovered on a single
into memory as a reusable skill, later cases re-
cold-start element propagates as a durable pre-
9

execution guardrail to every chemically distinct Practical computational workflows
| member         | of the | same | family,  | so  | that | an interven- |         |      |        |     |        |          |     |       |
| -------------- | ------ | ---- | -------- | --- | ---- | ------------ | ------- | ---- | ------ | --- | ------ | -------- | --- | ----- |
|                |        |      |          |     |      |              | Can the | same | memory |     | reduce | repeated |     | setup |
| tion validated |        | on   | one FCC, |     | BCC  | or diamond   |         |      |        |     |        |          |     |       |
element protects subsequent calculations across and analysis costs in practical workflows rather
that family without further human input. This than only in controlled benchmarks? We evalu-
shows that memory captured at the right level ated the system on 13 computational materials
of abstraction generalizes across compositions tasks that resemble routine research work in
rather than being tied to the specific material a research group. The tasks include VASP (a
on which it was first observed, and mirrors the DFT package) calculations of band structures,
|          |              |     |            |     |         |       | phonons, | dielectric |     | constants, |     | effective | masses, |     |
| -------- | ------------ | --- | ---------- | --- | ------- | ----- | -------- | ---------- | --- | ---------- | --- | --------- | ------- | --- |
| function | of effective |     | laboratory |     | memory; | i.e., | a        |            |     |            |     |           |         |     |
local failure is converted into a structural-family- surfacesandworkfunctions,aswellasLAMMPS
level pre-execution warning that protects later (a molecular dynamics package) calculations for
|              |     |          |               |     |     |     | vacancy        | and | thermal | properties; |                  | the | task | IDs |
| ------------ | --- | -------- | ------------- | --- | --- | --- | -------------- | --- | ------- | ----------- | ---------------- | --- | ---- | --- |
| work without |     | external | intervention. |     |     |     |                |     |         |             |                  |     |      |     |
|              |     |          |               |     |     |     | and references |     | are     | listed      | in Supplementary |     |      | Ta- |
(a)Memory-basederrorpreventionacrossdifferenttasks ble 2. Although lifelong research memory ex-
|     |     |     |     |     |     |     | tends beyond |       | computation, |          | these       | tasks     | provide    |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | ------------ | -------- | ----------- | --------- | ---------- | --- |
|     |     |     |     |     |     |     | a measurable |       | analogue     | of       | the broader |           | materials- |     |
|     |     |     |     |     |     |     | research     | loop; | i.e.,        | defining | a question, |           | gathering  |     |
|     |     |     |     |     |     |     | knowledge,   |       | preparing    | a        | protocol,   | executing |            | it, |
|     |     |     |     |     |     |     | checking     | the   | result,      | revising | the         | workflow  |            | and |
(b)Casestudy:Preventing SCF convergence failures preserving what was learned.
| Cold-starttasks |     |     | Sandboxsignal   |     | Memory          |     |             |     |            |      |     |      |            |     |
| --------------- | --- | --- | --------------- | --- | --------------- | --- | ----------- | --- | ---------- | ---- | --- | ---- | ---------- | --- |
|                 |     |     |                 |     |                 |     | The central |     | efficiency | gain | is  | best | understood |     |
| FCCCu,BCCLi,    |     |     | SCFconvergence  |     | init_wfc=random |     |             |     |            |      |     |      |            |     |
| DiamondC        |     |     | failurewithSG15 |     |                 |     |             |     |            |      |     |      |            |     |
defaultwavefunctioninit structured feedback savedmemory as a compression of repeated cognitive and cler-
|     |     |     |     |     |     |     | ical work. | For | a human |     | researcher, |     | the | recur- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | --- | ----------- | --- | --- | ------ |
LatertasksretrievethememorybeforerunningABACUS ring parts of a familiar computational workflow
|            |             |                 |             |     |              |           | commonly      | unfold     |              | on hour-to-day |          | time            |          | scales; |
| ---------- | ----------- | --------------- | ----------- | --- | ------------ | --------- | ------------- | ---------- | ------------ | -------------- | -------- | --------------- | -------- | ------- |
| retrieve   |             | init_wfc=random |             |     | SCFconverges |           |               |            |              |                |          |                 |          |         |
|            |             |                 |             |     |              |           | i.e., framing |            | the problem, |                | locating | prior           | scripts, |         |
|            |             |                 |             |     |              |           | preparing     | input      | files,       | checking       |          | convergence     |          | pa-     |
| Figure     | 4 - Sol27LC |                 | evaluation  | and | memory-based |           |               |            |              |                |          |                 |          |         |
|            |             |                 |             |     |              |           | rameters,     | monitoring |              | jobs           | and      | post-processing |          |         |
| prevention | of          | repeated        | convergence |     |              | failures. | (a)           |            |              |                |          |                 |          |         |
Across 27 Sol27LC elemental-solid EOS-fitting results. After memory accumulation, the agent
calculations grouped by crystal structure, Round 2 can recover problem context, prior scripts, input
reruns eliminate all failed cases, improving outcomes templatesandparameterchoicesonminute-scale
| from 22/1/4    | to         | 25/2/0        | Correct/Partial/Error |                     |       |               | and           |               |       |                |           |           |        |        |
| -------------- | ---------- | ------------- | --------------------- | ------------------- | ----- | ------------- | ------------- | ------------- | ----- | -------------- | --------- | --------- | ------ | ------ |
|                |            |               |                       |                     |       |               | time budgets, |               | then  | reuse          | them      | during    | file   | prepa- |
| achieving      | an overall |               | avoided-error         |                     | rate  | of 91.7%.     |               |               |       |                |           |           |        |        |
|                |            |               |                       |                     |       |               | ration,       | analysis      | and   | summarization. |           |           | Figure | 5b     |
| Partial        | denotes    | a valid       | EOS                   | calculation         |       | whose         | final         |               |       |                |           |           |        |        |
|                |            |               |                       |                     |       |               | places        | this contrast |       | on a           | concrete  | time      | axis.  |        |
| report carries |            | a Bohr-to-Å   |                       | unit inconsistency. |       |               | The           |               |       |                |           |           |        |        |
| avoided-error  |            | rate measures |                       | the fraction        |       | of cold-start |               |               |       |                |           |           |        |        |
|                |            |               |                       |                     |       |               | Figure        | 5a quantifies |       | the            | same      | reduction | across |        |
| failures       | that are   | successfully  |                       | prevented           |       | in subsequent |               |               |       |                |           |           |        |        |
|                |            |               |                       |                     |       |               | 13 tasks.     | Total         | token | use            | decreases | from      | 17.90M |        |
| runs through   |            | the retrieval | of                    | memories            |       | distilled     | from          |               |       |                |           |           |        |        |
|                |            |               |                       |                     |       |               | in R1         | to 9.84M      | in    | R2 and         | 8.96M     | in        | R3,    | while  |
| previous       | failures.  | (b)           | Case-study            |                     | trace | showing       | how           |               |       |                |           |           |        |        |
cold-start SCF convergence failures with default non-polling tool calls decrease from 1,038 to 684
|              |     |                |     |               |     |        | and then | 481, | reaching |     | a 50.0% | token | reduction |     |
| ------------ | --- | -------------- | --- | ------------- | --- | ------ | -------- | ---- | -------- | --- | ------- | ----- | --------- | --- |
| wavefunction |     | initialization |     | are converted |     | into a |          |      |          |     |         |       |           |     |
reusable memory, init_wfc=random, which is and53.7%tool-callreductionbyR3. Thelargest
retrieved by later cases before running ABACUS drops occur where prior traces become directly
and prevents repeated convergence failures. reusable assets; i.e., the Cu monovacancy for-
|     |     |     |     |     |     |     | mation   | energy | calculation |            | falls      | from       | 3.60M      | to    |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ----------- | ---------- | ---------- | ---------- | ---------- | ----- |
|     |     |     |     |     |     |     | 387.3k   | tokens | in R2,      | the        | Si thermal |            | conductiv- |       |
|     |     |     |     |     |     |     | ity from | 2.28M  | to          | 586.1k,    | the        | Si Γ-point | optical    |       |
|     |     |     |     |     |     |     | phonon   | from   | 1.39M       | to 350.9k, |            | and the    | Cu         | equi- |
10

librium vacancy concentration from 4.17M to tion (a = 3.615 Å, E = 1.2723 eV) as a refer-
0 vf
700.2k after its initial failed run. ence (consistent with copper vacancy literature
in the practical-workflow context), while still
The per-task data also show why memory should
awaiting current-job confirmation [53, 54], re-
be interpreted as workflow reuse rather than au-
ducing tokens from 3.60M to 387.3k and tool
tomatic compression. Some tasks become heav-
calls from 81 to 26. In a graphene work-function
ier in later rounds; e.g., the fcc Al elastic con-
task,theagentreusesavalidatedPOSCAR(crys-
stant calculations expand to 2.56M tokens and
tal structure and computational cell specifica-
126 tool calls in R2, and Cu thermal expan-
tions) file with a 25 Å vacuum spacing and a
sion calculations grow in both R2 and R3 as
verified 1.420 Å C–C bond length, avoids re-
the agent performs additional checks. Individ-
dundant bond-length verification and obtains
ual failures remain non-monotonic; e.g., the Cu
Φ = 4.224eV,consistentwiththegraphenework-
lattice-constant and cohesive-energy task (Task
function reference used for this task [55], with
4) fails in R2 after a retry-heavy trace, the Si
tokens reduced from 336.2k to 173.8k and tool
thermal-conductivity task (Task 7) fails in R3,
calls from 28 to 19.
and the Cu equilibrium-vacancy-concentration
task (Task 13) fails in R1 despite substantial Theseexamplesdisplaytwocomplementaryfunc-
tool use; overall success is 10/13 in R1, 11/13 in tions of memory. Skills accelerated repeatable
R2 and 9/13 in R3. Memory reduces avoidable workflows (when the previous protocol is valid)
rediscovery, but it does not eliminate physical and facts supply cautions (when a previous re-
judgement, job variability or the need to verify sult should be treated as a reference, warning
the current calculation. or sanity check) rather than copied as a final
answer.
Figure 6 provides four concrete examples. In a
GaAs band-structure and density-of-states task,
the first round saves a VASP skill specifying re- Discussion
laxation, SCF, NSCF band and DOS steps with
ENCUT(parameter),a12×12×12k-pointmesh These results shift the unit of progress from the
(parameter) and PAW-PBE (density functional agent to the memory system in AI-for-science
choice). The second round retrieves the skill and systems. If these systems are designed around a
produces a band gap of 0.150 eV, consistent with current agent, scientific experience remains tied
the well-known semilocal-DFT underestimation to a model, prompt stack, tool interface or con-
of GaAs band gaps and therefore better inter- versation history. If they are designed around
preted as a reproduced PBE-level result than memory, the durable asset is the accumulated
as an absolute reference [50, 51], with token use record of facts, protocols, warnings and valida-
dropping from 1.06M to 459.7k and tool calls tions, while agents become replaceable interfaces
from 79 to 41. In a Si optical-phonon task, a that read, execute and revise that record. This
prior unrelaxed DFPT run had produced an framing is especially important in AI-for-science-
imaginary mode at 49.121 cm−1 and a spuri- based research, where a useful lesson is often
ous optical frequency of 366.6 cm−1; the saved operational rather than declarative; e.g., a pseu-
memory enforces a relax-first pipeline, yielding dopotential setting, a unit convention, a relax-
a Gamma-point optical phonon of 502.47 cm−1, before-property protocol or a failure mode that
softened by about 3% relative to the experimen- should be checked before submitting another job.
tal Raman value near 520 cm−1, but still physi-
Three computational layers support this shift,
cally reasonable for this workflow class [52], with
each probing a different depth of research com-
tokens reduced from 1.39M to 350.9k and tool
petence. The first is computational materials
callsfrom108to32. InanFCCCumonovacancy-
competence; MatTools shows whether the agent
formation-energy task, the system retrieves prior
can execute the right API, schema and code
lattice and vacancy-formation-energy informa-
so that a scientific calculation can actually run,
11

Si GaAs Al Cu Cu Cu
EOS band/DOS elasticity lattice/cohesion vacancy energy thermal expansion
Si Si Si GaAs Graphene Al(111) Cu vacancy
thermal conductivity dielectric constant Γ phonon effective mass work function surface energy concentration
Figure 5 - Benchmarking performance on practical computational materials science tasks. (a) Token
consumption and non-polling tool calls across three rounds for 13 VASP and LAMMPS tasks. Total tokens
decrease from 17.90M to 9.84M and 8.96M over R1–R3, while tool calls decrease from 1,038 to 684 and 481.
The aggregate trace burden decreases after R1, but failures and extra checks remain task-specific and
non-monotonic. Hatched bars indicate rounds that did not yield a valid final result; their heights still report
the tokens and tool calls consumed during those failed rounds. (b) Human-to-agent time-scale comparison for
a recurring computational materials science workflow. Human execution typically requires hours to days for
problem framing, literature search, file preparation, monitoring, post-processing and summarization; after
memory accumulation, the agent can reuse validated prior traces to perform the repeated preparation and
analysis steps on minute-scale time budgets. The comparison highlights superhuman efficiency in routine
workflow reuse, while job execution and scientific validation remain part of the process.
and whether the resulting textual record can chemically distinct members of the same fam-
transfer to a different model. The second is ily from falling into the same numerical trap.
physical reliability; Sol27LC shows that a sin- The third is workflow reuse efficiency; the VASP
gle, operationally specific failure can be encoded and LAMMPS tasks show that the same mem-
as a pre-execution guardrail that generalizes at ory format compresses the repeated cognitive
the level of the crystal lattice structure family, and clerical steps of a familiar workflow while
so that a fix learned on one element protects leaving physical judgement and current-run veri-
12

| TASK A                     |     |     |                                |     |                                |     | TASK B   |         |            |
| -------------------------- | --- | --- | ------------------------------ | --- | ------------------------------ | --- | -------- | ------- | ---------- |
|                            |     |     | # Round 1 (R1) – save skill &  |     | # Round 1 (R1) – save skill &  |     |          |         |            |
|                            |     |     | memory                         |     | memory                         |     |          |         |            |
| Band gap and DOS for GaAs  |     |     |                                |     |                                |     | Optical  | phonon  | at  Gamma  |
(zinc blende) using VASP 5.4.4   [Skill - 3a7fc90f] [Memory – Prior Si DFPT error] point for Si using VASP 5.4.4
|                        |     |     | GaAs Band Structure + DOS on  |                     | Unrelaxed DFPT result: imaginary  |     |                        |     |     |
| ---------------------- | --- | --- | ----------------------------- | ------------------- | --------------------------------- | --- | ---------------------- | --- | --- |
|                        |     |     | Bohrium                       |                     | mode 49.121 cm-1                  |     |                        |     |     |
| R1 v.s. R2 Performance |     |     |                               |                     |                                   |     | R1 v.s. R2 Performance |     |     |
|                        |     |     | Steps: Relax                  | ->SCF ->NSCF Bands- | Wrong optical frequency: 366.6    |     |                        |     |     |
|                        |     |     | >DOS                          |                     | cm-1 (should be ~520 cm-1)        |     |                        |     |     |
ENCUT = 520 eV | PAW-PBE |
|        |     |     | KPOINTS 12*12*12             |              | skill + memory saved         |                |        |     |     |
| ------ | --- | --- | ---------------------------- | ------------ | ---------------------------- | -------------- | ------ | --- | --- |
|        |     |     |                              | next session |                              | next session   |        |     |     |
|        |     |     | # Round 2 (R2) – retrieve &  |              | # Round 2 (R2) – retrieve &  |                |        |     |     |
|        |     |     | execute                      |              | execute                      |                |        |     |     |
|        |     |     | [search_skill]               |              | [search_memory]              |                |        |     |     |
| RESULT |     |     |                              |              |                              |                | RESULT |     |     |
|        |     |     | Hit: 3a7fc90f                | GaAs Band    | Hit: imaginary mode from     |                |        |     |     |
|        |     |     | Structure + DOS loaded       |              | unrelaxed run                | -> must relax  |        |     |     |
first
[call_task]
|     |             |     | Relax ->SCF ->NSCF Bands         | ->DOS | [call_task]                      |     |     |                     |     |
| --- | ----------- | --- | -------------------------------- | ----- | -------------------------------- | --- | --- | ------------------- | --- |
|     |             |     | GaAs zinc-blende F-43m |         |       | (1) Relax 2-atom Si diamond      |     | ->  |                     |     |
|     |             |     | ENCUT=520 eV | platform: Bohrium |       | (2) DFPT Gamma phonon            |     |     |                     |     |
|     |             |     | Skill + memory resolved – no     |       | Skill + memory resolved – relax- |     |     |                     |     |
|     | 𝐸!=0.150	eV |     |                                  |       | first pipeline applied           |     |     | 𝜈̃Γ "#$=502.47 cm%& |     |
retry needed
TASK D
| TASK C |     |     | # Round 1 (R1) – save skill &  |     | # Round 1 (R1) – save skill &  |     |     |     |     |
| ------ | --- | --- | ------------------------------ | --- | ------------------------------ | --- | --- | --- | --- |
memory
Monovacancy formation energy  memory Work  function  of  Graphene
for FCC Cu using LAMMPS [Memory – Computed Cu Evf] [Memory – Graphene POSCAR] surface using VASP 5.4.4
a1=[2.46,0,0] a2=[1.23,2.1304,0]
a0 = 3.615 Å | N_bulk = 4000 |
R1 v.s. R2 Performance E_bulk = -14159.9999 eV c=25 Å R1 v.s. R2 Performance
|     |     |     | N_vac = 3999 | E_vac = - |     | Atom1:(0,0,0.5)  |     |     |     |     |
| --- | --- | --- | ------------------------ | --- | ---------------- | --- | --- | --- | --- |
Atom2:(1/3,1/3,0.5)
14155.1875 eV
C-C = 1.420 Å verified x5 via
|     |     |     | Evf = 1.2723 eV              |              | execute_python_code          |              |     |     |     |
| --- | --- | --- | ---------------------------- | ------------ | ---------------------------- | ------------ | --- | --- | --- |
|     |     |     |                              | next session |                              | next session |     |     |     |
|     |     |     | # Round 2 (R2) – retrieve &  |              | # Round 2 (R2) – retrieve &  |              |     |     |     |
execute
execute
| RESULT |     |     | [monitor_job] |     | [call_task – memory hit] |     | RESULT |     |     |
| ------ | --- | --- | ------------- | --- | ------------------------ | --- | ------ | --- | --- |
Retrieved prior value:
POSCAR from R1 used – no bond-
|     |     |     | A0=3.615 Å, Evf=1.27 eV |     | length re-verification |     |     |     |     |
| --- | --- | --- | ----------------------- | --- | ---------------------- | --- | --- | --- | --- |
Held as reference only –
|     |             |     |                                 |     | Steps: SCF  -> LOCPOT             |     | -> planar  |     |     |
| --- | ----------- | --- | ------------------------------- | --- | --------------------------------- | --- | ---------- | --- | --- |
|     |             |     | awaiting current job output to  |     | avg  -> Phi                       |     |            |     |     |
|     |             |     | confirm                         |     | Platform: Bohrium                 |     |            |     |     |
|     |             |     | Skill + memory resolved –       |     | Skill + memory resolved – POSCAR  |     |            |     |     |
|     | 𝐸'(=1.27	eV |     | reference values retrieved      |     | reused, workflow applied          |     |            |     |     |
Φ=4.224 eV
Figure 6 - Cases showing the effects of memory and skill in practical computational materials science
tasks. Task A reuses a saved VASP workflow for GaAs band structure and DOS, reducing tokens from 1.06M
to 459.7k and tools from 79 to 41 while producing E =0.150 eV. Task B converts a prior Si DFPT phonon
g
failure into a relax-first memory, reducing tokens from 1.39M to 350.9k and tools from 108 to 32 while
|     | ν˜F2g | cm−1. |     |     |     |     |     |     |     |
| --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
yielding =502.47 Task C retrieves prior lattice and formation-energy information for the FCC
Γ
Cu monovacancy-formation-energy task, reducing tokens from 3.60M to 387.3k and tools from 81 to 26 while
preserving the need for current-job confirmation. Task D reuses a validated graphene POSCAR and
work-function workflow, reducing tokens from 336.2k to 173.8k and tools from 28 to 19 while producing
| Φ=4.224 | eV. |     |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fication untouched. Taken together, these layers memory is weaker than the target’s own experi-
progress from whether a calculation can run, to ence. Practical-workflow traces also show that
whether known physical pitfalls can be avoided, memory is not a universal token-compression
to whether prior work can be reused without mechanism; some tasks become longer when the
losing scientific rigor, and memory contributes agent retrieves broader context or performs addi-
at every level without changing model weights. tional validation. Sandbox review, job feedback,
|                |           |               |              |            | provenance         | and    | human inspection |             | are therefore |
| -------------- | --------- | ------------- | ------------ | ---------- | ------------------ | ------ | ---------------- | ----------- | ------------- |
| The boundaries |           | are equally   | important.   | Memory     |                    |        |                  |             |               |
|                |           |               |              |            | central            | rather | than optional.   | Text        | is portable   |
| quality        | depends   | on evidence   | quality;     | an unvali- |                    |        |                  |             |               |
|                |           |               |              |            | and scientifically |        | legible,         | but complex | multi-        |
| dated          | procedure | can propagate | errors       | and cross- |                    |        |                  |             |               |
|                |           |               |              |            | file workflows,    |        | pseudopotential  | choices,    | conver-       |
| model          | transfer  | can be        | harmful when | the source |                    |        |                  |             |               |
13

gence parameters and material-class assump- work with two layers: Facts for declarative ob-
tions should eventually be paired with stricter servations, warnings and parameter choices, and
schemas, applicability tags, repeated-success Skills for reusable procedures, scripts and proto-
counts, deprecation policies and executable vali- cols. Facts are written with infer=True so that
| dation tests.                       |     |     |     |     |     |          | mem0                    | extracts | atomic | statements |         | and      | decides |
| ----------------------------------- | --- | --- | --- | --- | --- | -------- | ----------------------- | -------- | ------ | ---------- | ------- | -------- | ------- |
|                                     |     |     |     |     |     |          | add/update/delete/no-op |          |        |            | against | existing | en-     |
| Finally,ourevidenceiscomputational. |     |     |     |     |     | Themoti- |                         |          |        |            |         |          |         |
|                                     |     |     |     |     |     |          | tries, while            | Skills   | are    | written    | with    |          |         |
infer=False
| vationextendstoexperimentalprotocols, |     |            |     |            |     | synthe-    |               |      |          |            |      |                  |      |
| ------------------------------------- | --- | ---------- | --- | ---------- | --- | ---------- | ------------- | ---- | -------- | ---------- | ---- | ---------------- | ---- |
|                                       |     |            |     |            |     |            | to preserve   | a    | complete | procedural |      | artefact.        | Vec- |
| sis know-how,                         |     | instrument |     | operation, |     | literature |               |      |          |            |      |                  |      |
|                                       |     |            |     |            |     |            | tor retrieval | uses | Qdrant   |            | with | 4096-dimensional |      |
judgementandproject-levelscientifictaste;these
|          |      |         |       |     |            |       | qwen3-embedding-8b |     |     | embeddings, |     | and | entity– |
| -------- | ---- | ------- | ----- | --- | ---------- | ----- | ------------------ | --- | --- | ----------- | --- | --- | ------- |
| settings | will | require | their | own | validation | stan- |                    |     |     |             |     |     |         |
relationmemoryusesNeo4jwithacustomgraph-
| dards. A | durable | scientific |     | memory | should | make |            |        |     |                    |     |     |            |
| -------- | ------- | ---------- | --- | ------ | ------ | ---- | ---------- | ------ | --- | ------------------ | --- | --- | ---------- |
|          |         |            |     |        |        |      | extraction | prompt |     | that canonicalizes |     |     | materials, |
futuremodelsbetterandmoreusefulratherthan
|        |                |     |           |     |          |      | libraries | and | methods. |     | Extraction | and | graph |
| ------ | -------------- | --- | --------- | --- | -------- | ---- | --------- | --- | -------- | --- | ---------- | --- | ----- |
| making | old experience |     | obsolete; |     | reaching | that |           |     |          |     |            |     |       |
constructionuseqwen3-maxindependentlyofthe
| goal requires |          | memory        | snapshots, |     | task   | harnesses, |                  |         |       |             |                 |                  |            |
| ------------- | -------- | ------------- | ---------- | --- | ------ | ---------- | ---------------- | ------- | ----- | ----------- | --------------- | ---------------- | ---------- |
|               |          |               |            |     |        |            | reasoning        | model   | under | evaluation, |                 | so               | the mem-   |
| trace release | and      | peer-editable |            |     | review | practices, |                  |         |       |             |                 |                  |            |
|               |          |               |            |     |        |            | ory policy       | remains |       | stable      | across          | model            | ablations. |
| not only      | stronger | agents.       |            |     |        |            |                  |         |       |             |                 |                  |            |
|               |          |               |            |     |        |            | Memoryisscopedby |         |       | user_id,    |                 | withSkillsstored |            |
|               |          |               |            |     |        |            | under the        | derived |       | namespace   | user_id_skills. |                  |            |
Methods
|        |              |     |     |     |     |     | Task and  | memory   |     | lifecycle                    |     |     |     |
| ------ | ------------ | --- | --- | --- | --- | --- | --------- | -------- | --- | ---------------------------- | --- | --- | --- |
| System | architecture |     |     |     |     |     |           |          |     |                              |     |     |     |
|        |              |     |     |     |     |     | Each task | executes |     | a retrieve–plan–act–reflect– |     |     |     |
The framework couples a hierarchical agent run- update loop. Before expensive actions, the agent
| time with | a session-scoped |     |     | tool | layer and | a long- |                     |     |     |     |              |     |        |
| --------- | ---------------- | --- | --- | ---- | --------- | ------- | ------------------- | --- | --- | --- | ------------ | --- | ------ |
|           |                  |     |     |      |           |         | calls search_memory |     |     | and | search_skill |     | to re- |
term memory subsystem (Figure 7; full inter- cover prior facts, scripts and failure warnings.
face and prompt definitions in Supplementary After execution, sandbox or job feedback deter-
| Notes 4–6). | The | runtime |     | is organized |     | around a |       |      |                  |     |     |            |        |
| ----------- | --- | ------- | --- | ------------ | --- | -------- | ----- | ---- | ---------------- | --- | --- | ---------- | ------ |
|             |     |         |     |              |     |          | mines | what | is consolidated: |     |     | successful | traces |
top-levelResearchAgentthatplansthescientific register or refine procedures through
save_to_-
workflow,managesthememoryandskilllifecycle, skill or update_skill, and new observations,
and delegates retrieval to a websearch-agent error fixes and parameter choices are written
| (literature, | URL, | PDF, | arXiv |     | and DOI-linked |     |         |                 |     |     |     |        |             |
| ------------ | ---- | ---- | ----- | --- | -------------- | --- | ------- | --------------- | --- | --- | --- | ------ | ----------- |
|              |      |      |       |     |                |     | through | save_to_memory. |     |     | At  | login, | locally cu- |
queries) and execution to a simulation-agent rated SKILL.md files are synchronized against
(sandboxed code and HPC job control). Agent the Skills namespace so that manually authored
| state is | checkpointed |     | in a | local SQLite |     | database. |             |            |     |     |             |     |         |
| -------- | ------------ | --- | ---- | ------------ | --- | --------- | ----------- | ---------- | --- | --- | ----------- | --- | ------- |
|          |              |     |      |              |     |           | and learned | procedures |     | are | retrievable |     | through |
The tool layer is exposed by an MCP server that the same interface. All entries are written in
mounts FastMCP endpoints behind a FastAPI human-readable text and linked to the execution
REST layer served by Uvicorn, with a shared trace that produced them.
| session_id     | routing          |             | files,      | sandbox | state     | and job |          |           |     |     |            |     |     |
| -------------- | ---------------- | ----------- | ----------- | ------- | --------- | ------- | -------- | --------- | --- | --- | ---------- | --- | --- |
| records        | into per-session |             | workspaces. |         |           | The MCP |          |           |     |     |            |     |     |
|                |                  |             |             |         |           |         | MatTools | benchmark |     |     | evaluation |     |     |
| layer provides |                  | file-system |             | access, | sandboxed |         |          |           |     |     |            |     |     |
command and Python execution with a 150s We evaluate on the real-world tool-use subset
direct-execution timeout, Pymatgen and Materi- of MatTools [46], comprising 49 questions from
|             |           |     |        |      |              |     | the pymatgen.analysis.defects |     |     |     |     | test | suite de- |
| ----------- | --------- | --- | ------ | ---- | ------------ | --- | ----------------------------- | --- | --- | --- | --- | ---- | --------- |
| als Project | structure |     | tools, | NIST | interatomic- |     |                               |     |     |     |     |      |           |
potential retrieval, and HPC job submission composed into 138 evaluated subtasks (full list,
and monitoring; longer simulations are dis- evaluated outputs and per-question prompts in
|             |         |        |                |         |     |           | Supplementary |        | Note  | 1). The  | QA-only |      | portion of  |
| ----------- | ------- | ------ | -------------- | ------- | --- | --------- | ------------- | ------ | ----- | -------- | ------- | ---- | ----------- |
| patched     | through | the    | job-management |         |     | interface |               |        |       |          |         |      |             |
|             |         |        |                |         |     |           | MatTools      | is not | used. | Question |         | pass | rate is the |
| and resumed |         | by the | agent          | through |     | an auto-  |               |        |       |          |         |      |             |
mated monitor prompt. The memory subsys- fraction of the 49 top-level questions in which all
tem is built on the open-source mem0 frame- subtasks pass; task success rate is the fraction
14

|     | AgentRuntime              |     |     |     |     | MemoryServices   |     |     |     | MCPServerSuit     |     |
| --- | ------------------------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | ----------------- | --- |
|     | Orchestration & Reasoning |     |     |     |     | TheCognitiveCore |     |     |     | Tool&ServiceLayer |     |
UnifiedMemoryLayer
|     | AgentOrchestrator |     |     |     |     |     |     |     |     | MCPIndex&Discovery |     |
| --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- |
Unifiedinterfaceformemoryoperations
|     | LLM-basedplanner               |     |     |     |        |      |        |             |            | Serviceregistry&capabilitydiscovery |         |
| --- | ------------------------------ | --- | --- | --- | ------ | ---- | ------ | ----------- | ---------- | ----------------------------------- | ------- |
|     | (decompose,reason,act,reflect) |     |     |     | Recall | Save | Update | Delete Link |            |                                     |         |
|     | AgentMiddleware                |     |     |     | Facts  |      | Skills |             | FileSystem |                                     | Sandbox |
Taskrouting Subagentmanagement
|     |     |     |     |     | Captureknowledge |     | Procedures,methods |     |     | Workspace, | Command& |
| --- | --- | --- | --- | --- | ---------------- | --- | ------------------ | --- | --- | ---------- | -------- |
ContextSummarization abouttheworld andknow-how files Pythonexecution
|                |     |                 |     |     |                          |     |     |     | Structuretools |     | Mat.Project |
| -------------- | --- | --------------- | --- | --- | ------------------------ | --- | --- | --- | -------------- | --- | ----------- |
| WebsearchAgent |     | SimulationAgent |     |     | MemorySystemOrchestrator |     |     |     |                |     |             |
Literatureretrieval Simulationplanning Pymatgen Search&download
Websiteextraction DFT/MDcalculation structuretools materialsdata
Intelligent routing, fusion and management
across heterogeneous stores
|     |     |     |     |     |     |     |     |     | MLPotential |     | JobManager |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---------- |
ToolAbstractionLayer
|             | Unifiedinterfacetotoolsandservices |                |     |     |       |     |        |     |     | Interatomic | HPCjobcontrol |
| ----------- | ---------------------------------- | -------------- | --- | --- | ----- | --- | ------ | --- | --- | ----------- | ------------- |
|             |                                    |                |     |     |       |     |        |     |     | potentials  | &monitoring   |
|             |                                    |                |     |     | Neo4j |     | Qdrant |     |     |             |               |
| SearchTools |                                    | Code&ExecTools |     |     |       |     |        |     |     |             |               |
MCPTraffic&AuditLogs
|             |                          |     |          |     | KnowledgeGraph      |     | VectorDatabase     |     |                                         |     |     |
| ----------- | ------------------------ | --- | -------- | --- | ------------------- | --- | ------------------ | --- | --------------------------------------- | --- | --- |
| DomainTools |                          |     | JobTools |     | entities,relations, |     | semanticembedding, |     |                                         |     |     |
|             |                          |     |          |     | andcontext          |     | similaritysearch   |     | Requests,toolcalls,responses,provenance |     |     |
|             | Observability&Checkpoint |     |          |     |                     |     |                    |     | ExecutionSubstrate                      |     |     |
Isolated,Reproducible,Secure
| CheckpointStore |     | RunLogs |     | Metrics&Monitoring |     |     |     |     |     |     |     |
| --------------- | --- | ------- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
Compute&
|     |     |     |     |     |     |     |     | SessionWorkspace |     | Sandbox |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------- | --- |
Persistentstate Traceability Performance&Health ExternalServices
|     |     |     |     |     |     |     |     | User/Session-scoped | Isolatedruntime |     | HPC/APIs/Database |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --------------- | --- | ----------------- |
Managedstorage
|       |        |     |            |                 |     |     |             |     | Per-usercontainer |                | Materials&Webdata |
| ----- | ------ | --- | ---------- | --------------- | --- | --- | ----------- | --- | ----------------- | -------------- | ----------------- |
| Agent | Memory |     | Tool       | Execution&Infra |     |     |             |     |                   |                |                   |
|       |        |     | UserIntent |                 |     |     | Plan&Reason |     |                   | RetrieveMemory |                   |
Data& Naturallanguagerequest Agentdecomposes&plans Recallrelevantknowledge
ControlFlow
|     |     |     |                    |     |     | Reflect&Learn |                   | ContinuousImprovement |     |              |     |
| --- | --- | --- | ------------------ | --- | --- | ------------- | ----------------- | --------------------- | --- | ------------ | --- |
|     |     |     | DeliverResult      |     |     |               | UpdateMemory      |                       |     | ActviaTools  |     |
|     |     |     | Synthesize&respond |     |     |               | Storenewknowledge |                       |     | Usetools/MCP |     |
|     |     |     |                    |     |     |               | &outcomes         |                       |     | executetasks |     |
totheuser
Figure 7 - Overview of the memory-centric agent system architecture. The framework couples an
LLM-based agent runtime with unified memory services and an MCP-based tool layer, enabling the agent to
decompose user intent, retrieve prior knowledge, execute materials science workflows in sandboxed
| environments, | and | update | memory | from | observed | outcomes. |     |     |     |     |     |
| ------------- | --- | ------ | ------ | ---- | -------- | --------- | --- | --- | --- | --- | --- |
of the 138 subtasks that pass; function runnable per configuration and the exact prompt edits
rateisthefractionofgeneratedfunctionsthatex- applied to the research, simulation and task-
ecute without runtime, import or output-schema framing prompts are summarised in Supplemen-
errors in the harness. Five configurations are tary Note 7. Sandbox feedback is exposed only
evaluated and differ only in which subsystems through mattools_code_check, which extracts
are exposed to the agent and in the correspond- the submitted function, runs it inside an isolated
ing prompt edits: full system, no-memory ab- DockerPythonenvironmentandreturnsthe cap-
lation, no-sandbox ablation, bare-LLM baseline tured execution status, stdout and stderr; it
andcross-transfermemorytest. Subsystemstate never returns the benchmark answer or a cor-
15

rected implementation. A round is one complete state, band structure and density of states, elas-
pass over the same 49 questions: R1 is a cold- ticconstants,cohesiveenergy,vacancyformation
start pass, and R2–R3 reuse memory accumu- energy, thermal expansion, thermal conductiv-
lated and consolidated in previous passes, with ity, dielectric constant, optical phonons, effective
model parameters fixed across rounds. When mass, work function, surface energy and equi-
several reasoning models are evaluated under librium vacancy concentration; identifiers, de-
the full system in the same study, each model scriptions and experimental references are listed
receives its own user_id and memory names- in Supplementary Note 2, together with the
pace so that writes do not cross models; the tool task-framing and automated-monitor prompts
semantics, prompts and agent design observed used to drive the agent during long-running jobs.
by the model are unchanged. For cross-model Calculations submitted through the MCP job-
transfer, the target model’s writes are disabled management interface return identifiers that are
and the read tools are bound to a frozen source- watched by an automated monitor prompt and
model namespace produced after that source relayed back to the agent when results are avail-
model’s own three full-system rounds; we report able,sotheagentcanresumeexecutionandfinal-
the target’s task-success change relative to its ize the task. A task is counted as successful only
own R3 memory. when a physically interpretable final result is de-
livered; failures cover calculation errors, missing
Sol27LC evaluation finalvaluesandoutputsthatcannotbevalidated
from the trace. Token counts are computed over
Sol27LC contains 27 elemental cubic solids span-
the complete agent trace per round, including
ning FCC, BCC and diamond structures with
memory retrieval, code generation, sandbox ex-
experimental lattice constants as references [47];
ecution, job submission and monitoring, post-
the structure list and per-case results are tab-
processing and final synthesis. Tool-call counts
ulated in Supplementary Note 3. Equation-of-
exclude repeated job-polling calls so that the
state fits are computed with ABACUS [48] using
statistic reflects substantive agent actions rather
SG15 ONCV pseudopotentials [49]. Initial and
than scheduler waiting.
follow-up agent prompts used to drive each case
are reproduced in Supplementary Note 3. Cases
Acknowledgments
within the same crystal-structure family share a
memory store; FCC Cu, BCC Li and diamond
The work described is partially supported by
C are the cold-start cases. R1 runs the family
a grant from the NSFC/RGC Joint Research
with memory accumulation enabled, and R2 re-
Scheme sponsored by the Research Grants Coun-
runs only the cases that failed in R1, retrieving
cil of the Hong Kong Special Administrative
the accumulated memory before execution. A
Region, China and the National Natural Sci-
case is classified Correct when the fitted lattice
ence Foundation of China (Project No. N_-
constant deviates from experiment by less than
HKU767/25). The authors would also like to
5%, Partial when the EOS fit reproduces the
thank the Materials Innovation Institute for Life
correct physical equilibrium but the reported
Sciences and Energy (MILES) for startup fund-
value carries a residual Bohr-to-Å unit inconsis-
ing and HKU-SIRI in Shenzhen for partial sup-
tency, and Error otherwise. The avoided-error
port of this work. This work was also partially
rate measures, among R1 failure cases caused by
supportedbytheResearchGrantsCouncil,Hong
wavefunction-initialization non-convergence, the
Kong SAR through the General Research Fund
fraction that no longer fail in R2.
(17210723, 17200424). T. W. acknowledges ad-
ditional support by the General Research Fund
Practical computational workflows
(17211726) and the Guangdong Natural Science
The practical-workflow evaluation comprises 13 Fund (2025A1515012129).
VASP and LAMMPS tasks covering equation-of-
16

| References          |              |               |                 |               |         | ical research |                    | with large | language |          | models. |
| ------------------- | ------------ | ------------- | --------------- | ------------- | ------- | ------------- | ------------------ | ---------- | -------- | -------- | ------- |
|                     |              |               |                 |               |         | Nature,       | 624(7992):570–578, |            |          | 2023.    |         |
| [1] Daniil          | A.           | Boiko, Robert |                 | MacKnight,    | Ben     |               |                    |            |          |          |         |
|                     |              |               |                 |               |         | [7] Yixiang   | Ruan,              | Chenyin    |          | Lu, Ning | Xu,     |
| Kline,andGabeGomes. |              |               | Autonomouschem- |               |         |               |                    |            |          |          |         |
|                     |              |               |                 |               |         | Yuchen        | He, Yixin          | Chen,      | Jian     | Zhang,   | Jun     |
| ical                | research     | with          | large           | language      | models. |               |                    |            |          |          |         |
|                     |              |               |                 |               |         | Xuan,         | Jianzhang          | Pan,       | Qun      | Fang,    | Hanyu   |
| Nature,             | 624:570–578, |               | 2023.           | doi: 10.1038/ |         |               |                    |            |          |          |         |
Gao,XiaodongShen,NingYe,QiangZhang,
s41586-023-06792-0.
|            |     |           |      |        |           | and Yiming | Mo.       | An automatic |     | end-to-end |     |
| ---------- | --- | --------- | ---- | ------ | --------- | ---------- | --------- | ------------ | --- | ---------- | --- |
| [2] Andrés | M   | Bran, Sam | Cox, | Oliver | Schilter, |            |           |              |     |            |     |
|            |     |           |      |        |           | chemical   | synthesis | development  |     | platform   |     |
Carlo Baldassari, Andrew D. White, and powered by large language models. Na-
Philippe Schwaller. Augmenting large ture Communications, 15:10160, 2024. doi:
language models with chemistry tools. 10.1038/s41467-024-54457-x.
| Nature | Machine | Intelligence,                |     | 6:525 | – 535, |          |             |      |          |       |        |
| ------ | ------- | ---------------------------- | --- | ----- | ------ | -------- | ----------- | ---- | -------- | ----- | ------ |
|        |         |                              |     |       |        | [8] Tao  | Song, Man   | Luo, | Xiaolong |       | Zhang, |
| 2023.  | doi:    | 10.1038/s42256-024-00832-8.  |     |       |        |          |             |      |          |       |        |
|        |         |                              |     |       |        | Linjiang | Chen,       | Yan  | Huang,   | Jiaqi | Cao,   |
| URL    |         | https://api.semanticscholar. |     |       |        |          |             |      |          |       |        |
|        |         |                              |     |       |        | Qing     | Zhu, Daobin | Liu, | Baicheng |       | Zhang, |
org/CorpusID:258059792.
|     |     |     |     |     |     | Gang | Zou, Guoqing |     | Zhang, | Fei | Zhang, |
| --- | --- | --- | --- | --- | --- | ---- | ------------ | --- | ------ | --- | ------ |
[3] Feifei Luo, Jinglang Zhang, Qilong Wang, Weiwei Shang, Yao Fu, Jun Jiang, and
and Chunpeng Yang. Leveraging prompt Yi Luo. A multiagent-driven robotic ai
engineering in large language models for chemist enabling autonomous chemical re-
accelerating chemical research. ACS Cen- search on demand. Journal of the Ameri-
tral Science, 11(4):511–519, Apr 2025. can Chemical Society, 147(15):12534–12545,
ISSN 2374-7943. doi: 10.1021/acscentsci. Apr 2025. ISSN 0002-7863. doi: 10.1021/
4c01935. URL https://doi.org/10. jacs.4c17738. URL https://doi.org/10.
1021/acscentsci.4c01935.
1021/jacs.4c17738.
[4] B. Burger, Phillip M. Maffettone, [9] Amil Merchant, Simon Batzner, Samuel S
Vladimir V. Gusev, Catherine M. Aitchison, Schoenholz, Muratahan Aykol, Gowoon
Yang Bai, Xiao yan Wang, Xiaobo Li, Cheon, and Ekin Dogus Cubuk. Scaling
Ben M. Alston, Buyin Li, Rob Clowes, deep learning for materials discovery. Na-
Nicola Rankin, Brianna Harris, Reiner Se- ture, 624(7990):80–85, 2023. doi: 10.1038/
| bastian | Sprick, | and                             | Andrew  | I. Cooper. | A   | s41586-023-06735-9. |        |         |          |             |         |
| ------- | ------- | ------------------------------- | ------- | ---------- | --- | ------------------- | ------ | ------- | -------- | ----------- | ------- |
| mobile  | robotic | chemist.                        | Nature, | 583:237    | –   |                     |        |         |          |             |         |
|         |         |                                 |         |            |     | [10] Claudio        | Zeni,  | Robert  | Pinsler, |             | Daniel  |
| 241,    | 2020.   | doi: 10.1038/s41586-020-2442-2. |         |            |     |                     |        |         |          |             |         |
|         |         |                                 |         |            |     | Zügner,             | Andrew | Fowler, | Matthew  |             | Horton, |
| URL     |         | https://api.semanticscholar.    |         |            |     |                     |        |         |          |             |         |
|         |         |                                 |         |            |     | Xiang               | Fu,    | Zilong  | Wang,    | Aliaksandra |         |
org/CorpusID:220420261.
|     |     |     |     |     |     | Shysheya, | John | Waldron | Crabbe, |     | Shoko |
| --- | --- | --- | --- | --- | --- | --------- | ---- | ------- | ------- | --- | ----- |
[5] Tianwei Dai, Sriram Vijayakrishnan, Ueda, Roberto Sordillo, Lixin Sun, Jake
Filip T. Szczypiński, Jean-François Ayme, Smith, Bichlien H. Nguyen, Hannes Schulz,
Ehsan Simaei, Thomas Fellowes, Rob Sarah Lewis, Chin-Wei Huang, Ziheng
Clowes, Lyubomir Kotopanov, Caitlin E. Lu, Yichi Zhou, Han Yang, Hongxia
Shields, Zhengxue Zhou, John W. Ward, Hao, Jielan Li, Chunlei Yang, Wenjie
and Andrew I. Cooper. Autonomous Li, Ryota Tomioka, and Tian Xie. A
mobile robots for exploratory synthetic generative model for inorganic materials
chemistry. Nature, 635:890 – 897, 2024. design. Nature, 639:624 – 632, 2025.
doi: 10.1038/s41586-024-08173-7. URL doi: 10.1038/s41586-025-08628-5. URL
https://api.semanticscholar.org/ https://api.semanticscholar.org/
| CorpusID:273876112. |     |     |     |     |     | CorpusID:275591809. |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- |
[6] Daniil A Boiko, Robert MacKnight, Ben [11] Bo Ni, Benjamin Glaser, and S. Mo-
Kline,andGabeGomes. Autonomouschem- hadeseh Taheri-Mousavi. End-to-end pre-
17

diction and design of additively manu- ture Communications, 15:4705, 2024. doi:
facturable alloys using a generative al- 10.1038/s41467-024-48998-4.
| loygpt              | model.     |     | npj | Computational | Mate-         |               |            |       |         |          |            |           |
| ------------------- | ---------- | --- | --- | ------------- | ------------- | ------------- | ---------- | ----- | ------- | -------- | ---------- | --------- |
|                     |            |     |     |               |               | [19] Yeonghun |            | Kang, | Wonseok |          | Lee, Taeun | Bae,      |
| rials,              | 11(1):294, |     | Sep | 2025.         | doi: 10.1038/ |               |            |       |         |          |            |           |
|                     |            |     |     |               |               | Sangbum       |            | Han,  | Huiwon  | Jang,    | and        | Jihan     |
| s41524-025-01768-2. |            |     |     | URL           | https://doi.  |               |            |       |         |          |            |           |
|                     |            |     |     |               |               | Kim.          | Harnessing |       | large   | language |            | models to |
org/10.1038/s41524-025-01768-2.
|     |     |     |     |     |     | collect | and | analyze |     | metal–organic |     | frame- |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------- | --- | ------------- | --- | ------ |
[12] Wesley F Reinhart and Antonia Statt. work property data set. Journal of the
Large language models design sequence- American Chemical Society, 147(5):3943–
defined macromolecules via evolutionary 3958, 2025. doi: 10.1021/jacs.4c11085.
| optimization. |            |     | npj   | Computational | Mate-    |               |        |     |           |     |         |        |
| ------------- | ---------- | --- | ----- | ------------- | -------- | ------------- | ------ | --- | --------- | --- | ------- | ------ |
|               |            |     |       |               |          | [20] Qian     | Zhang, |     | Yongxu    | Hu, | Jiaxin  | Yan,   |
| rials,        | 10(1):262, |     | 2024. | doi:          | 10.1038/ |               |        |     |           |     |         |        |
|               |            |     |       |               |          | HengyueZhang, |        |     | XinyiXie, |     | JieZhu, | Huchao |
s41524-024-01449-6.
|     |     |     |     |     |     | Li, | Xinxin | Niu, | Liqiang | Li, | Yajing | Sun, and |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---- | ------- | --- | ------ | -------- |
[13] Seongmin Kim, Yousung Jung, and Joshua Wenping Hu. Large-language-model-based
Schrier.Largelanguagemodelsforinorganic aiagentfororganicsemiconductordevicere-
synthesis predictions. Journal of the Ameri- search. Advanced Materials, 36(32):2405163,
can Chemical Society, 146(29):19654–19659, 2024. doi: https://doi.org/10.1002/adma.
| 2024. | doi: | 10.1021/jacs.4c05840. |     |     |     | 202405163. |     |     |     |     |     |     |
| ----- | ---- | --------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
[14] JaehwanChoi,SeongminKim,andYousung [21] Akshat Chaudhari, Janghoon Ock, and
Jung. Synthesis-aware materials redesign Amir Barati Farimani. Modular large lan-
via large language models. Journal of the guage model agents for multi-task com-
American Chemical Society, 147(43):39113– putational materials science. Communi-
39122, 2025. doi: 10.1021/jacs.5c07743. cations Materials, 2026. doi: 10.1038/
s43246-025-00994-x.
| [15] Alireza | Ghafarollahi |     |     | and Markus | J Buehler. |     |     |     |     |     |     |     |
| ------------ | ------------ | --- | --- | ---------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Automating alloy design and discovery with [22] Ziqi Wang, Hongshuo Huang, Hancheng
physics-aware multimodal multiagent ai. Zhao, Changwen Xu, Shang Zhu, Jan
Proceedings of the National Academy of Janssen, and Venkatasubramanian
Sciences, 122(4):e2414074122, 2025. doi: Viswanathan. Dreams: Density func-
10.1073/pnas.2414074122. tional theory based research engine for
|     |     |     |     |     |     | agentic |     | materials | simulation, |     | 2025. | URL |
| --- | --- | --- | --- | --- | --- | ------- | --- | --------- | ----------- | --- | ----- | --- |
[16] AlirezaGhafarollahiandMarkusJ.Buehler.
https://arxiv.org/abs/2507.14267.
| SciAgents: |     | Automating |     | scientific | discov- |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
ery through bioinspired multi-agent intel- [23] Zhengding Hu, Kuntal Talit, Zhen Wang,
ligent graph reasoning. Advanced Materi- Haseeb Ahmad, Yichen Lin, Prabhleen
als, 37:2413523, 2025. doi: 10.1002/adma. Kaur,ChristopherLane,ElizabethA.Peter-
| 202413523. |     |     |     |     |     | son, | Zhiting | Hu,   | Elizabeth  |     | A. Nowadnick, |     |
| ---------- | --- | --- | --- | --- | --- | ---- | ------- | ----- | ---------- | --- | ------------- | --- |
|            |     |     |     |     |     | and  | Yufei   | Ding. | Tritondft: |     | Automating    | dft |
[17] AlirezaGhafarollahiandMarkusJ.Buehler.
|             |     |         |     |           |           | with | a multi-agent |     |     | framework, | 2026. | URL |
| ----------- | --- | ------- | --- | --------- | --------- | ---- | ------------- | --- | --- | ---------- | ----- | --- |
| ProtAgents: |     | Protein |     | discovery | via large |      |               |     |     |            |       |     |
https://arxiv.org/abs/2603.03372.
| language |     | model | multi-agent | collaborations |     |     |     |     |     |     |     |     |
| -------- | --- | ----- | ----------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
combining physics and machine learning. [24] Michael H. Prince, Henry Chan, Aika-
DigitalDiscovery,3(7):1389–1409,2024. doi: terini Vriza, Tao Zhou, Varuni K. Sas-
| 10.1039/D4DD00013G. |       |              |          |               |              | try,          | Yanqi  | Luo,          |               | Matthew       | T.          | Dearing,   |
| ------------------- | ----- | ------------ | -------- | ------------- | ------------ | ------------- | ------ | ------------- | ------------- | ------------- | ----------- | ---------- |
|                     |       |              |          |               |              | Ross          | J.     | Harder,       | Rama          | K.            | Vasudevan,  | and        |
| [18] Yeonghun       |       | Kang         | and      | Jihan Kim.    | ChatMOF:     |               |        |               |               |               |             |            |
|                     |       |              |          |               |              | Mathew        |        | J. Cherukara. |               | Opportunities |             | for        |
| an artificial       |       | intelligence |          | system        | for predict- |               |        |               |               |               |             |            |
|                     |       |              |          |               |              | retrieval     |        | and           | tool          | augmented     |             | large lan- |
| ing                 | and   | generating   |          | metal–organic | frame-       |               |        |               |               |               |             |            |
|                     |       |              |          |               |              | guage         | models |               | in scientific |               | facilities. | npj        |
| works               | using | large        | language |               | models. Na-  |               |        |               |               |               |             |            |
|                     |       |              |          |               |              | Computational |        |               | Materials,    |               | 10(1):251,  | Nov        |
18

2024. ISSN 2057-3960. doi: 10.1038/ Foerster, David Ha, and Jeff Clune.
s41524-024-01423-2. URL https://doi. Towards end-to-end automation of ai
org/10.1038/s41524-024-01423-2. research. Nature, 651:914 – 919, 2026.
|                |     |         |          |       |      | doi: | 10.1038/s41586-026-10265-5. |     |     |     | URL |
| -------------- | --- | ------- | -------- | ----- | ---- | ---- | --------------------------- | --- | --- | --- | --- |
| [25] Indrajeet |     | Mandal, | Jitendra | Soni, | Mohd |      |                             |     |     |     |     |
https://api.semanticscholar.org/
| Zaki, | Morten | M. Smedskjaer, |     | Katrin | Won- |     |     |     |     |     |     |
| ----- | ------ | -------------- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- |
CorpusID:286823959.
| draczek, |     | Lothar Wondraczek, |     | Nitya | Nand |     |     |     |     |     |     |
| -------- | --- | ------------------ | --- | ----- | ---- | --- | --- | --- | --- | --- | --- |
Gosvami, and N. M. Anoop Krishnan. Eval- [31] Wenhao Yuan, Guangyao Chen, Zhilong
uating large language model agents for au- Wang, and Fengqi You. Empowering gener-
tomation of atomic force microscopy. Na- alist material intelligence with large lan-
ture Communications, 16:9104, 2025. doi: guage models. Advanced Materials, 37
10.1038/s41467-025-64105-7. (32):2502771, 2025. doi: 10.1002/adma.
202502771.
| [26] Adam | Lahouari, | Jutta | Rogal, | and Mark | E.  |     |     |     |     |     |     |
| --------- | --------- | ----- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
Tuckerman. Automated machine learn- [32] Mayk Caldas Ramos, Christopher J. Col-
ing pipeline: Large language models- lison, and Andrew D. White. A review
assisted automated data set generation of large language models and autonomous
for training machine-learned interatomic agents in chemistry. Chemical Science,
potentials. Journal of Chemical The- 16(6):2514–2572, 2025. doi: 10.1039/
| ory           | and Computation, |            | 22(1):305–317,      |              | Jan | D4SC03921A.     |     |         |       |       |         |
| ------------- | ---------------- | ---------- | ------------------- | ------------ | --- | --------------- | --- | ------- | ----- | ----- | ------- |
| 2026.         | ISSN             | 1549-9618. | doi:                | 10.1021/acs. |     |                 |     |         |       |       |         |
|               |                  |            |                     |              |     | [33] Benediktus |     | Madika, | Aditi | Saha, | Chaeyul |
| jctc.5c01610. |                  | URL        | https://doi.org/10. |              |     |                 |     |         |       |       |         |
Kang,BatzorigBuyantogtokh,JoshuaAgar,
1021/acs.jctc.5c01610.
|     |     |     |     |     |     | Chris | M.  | Wolverton, | Peter | Voorhees, | Pe- |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---------- | ----- | --------- | --- |
[27] Zhihan Liu, Yubo Chai, and Jianfeng ter Littlewood, Sergei Kalinin, and Seung-
Li. Toward automated simulation research bum Hong. Artificial intelligence for ma-
workflow through llm prompt engineer- terials discovery, development, and opti-
ing design. Journal of Chemical Infor- mization. ACS Nano, 19(30):27116–27158,
mation and Modeling, 65(1):114–124, Jan Aug 2025. ISSN 1936-0851. doi: 10.1021/
2025. ISSN 1549-9596. doi: 10.1021/acs. acsnano.5c04200. URL https://doi.org/
jcim.4c01653. URL https://doi.org/10. 10.1021/acsnano.5c04200.
1021/acs.jcim.4c01653.
|     |     |     |     |     |     | [34] Negin | Orouji, | Jeffrey | A   | Bennett, Richard | B   |
| --- | --- | --- | --- | --- | --- | ---------- | ------- | ------- | --- | ---------------- | --- |
[28] Xin Li, Zhixuan Huang, Shu Quan, Cheng Canty, Long Qi, Shijing Sun, Paulami Ma-
Peng, and Xiaoming Ma. Slm-matrix: a jumdar, Chong Liu, Núria López, Neil M
multi-agent trajectory reasoning and veri- Schweitzer, John R Kitchin, et al. Au-
fication framework for enhancing language tonomous catalysis research with human–
models in materials data extraction. npj ai–robot collaboration. Nature Cataly-
Computational Materials, 11(1):241, Jul sis, pages 1–11, 2025. doi: 10.1038/
| 2025.               | ISSN | 2057-3960. |     | doi: 10.1038/ |     | s41929-025-01430-6. |        |       |       |             |       |
| ------------------- | ---- | ---------- | --- | ------------- | --- | ------------------- | ------ | ----- | ----- | ----------- | ----- |
| s41524-025-01719-x. |      |            | URL | https://doi.  |     |                     |        |       |       |             |       |
|                     |      |            |     |               |     | [35] Xu             | Huang, | Junwu | Chen, | Yuxing Fei, | Zhuo- |
org/10.1038/s41524-025-01719-x.
|     |     |     |     |     |     | han | Li, Philippe |     | Schwaller, | and Gerbrand |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------- | ------------ | --- |
[29] Mehrad Ansari and Seyed Mohamad Ceder. Cascade: Cumulative agentic skill
Moosavi. Agent-based learning of mate- creation through autonomous development
rials datasets from the scientific literature. and evolution, 2026. URL https://arxiv.
Digital Discovery, 3:2607–2617, 2024. doi: org/abs/2512.23880.
10.1039/D4DD00252K.
|     |     |     |     |     |     | [36] Jiaxuan |     | Lu, Ziyu | Kong, | Yemin Wang, | Rong |
| --- | --- | --- | --- | --- | --- | ------------ | --- | -------- | ----- | ----------- | ---- |
[30] Chris Lu, Cong Lu, Robert Tjarko Lange, Fu,HaiyuanWan,ChengYang,WenjieLou,
Yutaro Yamada, Shengran Hu, Jakob Haoran Sun, Lilong Wang, Yankai Jiang,
19

Xiaosong Wang, Xiao Sun, and Dongzhan cc/paper_files/paper/2023/file/
Zhou. Beyond static tools: Test-time tool 1b44b878bb782e6954cd888628510e90-Paper-Conference.
| evolutionforscientificreasoning,2026. |     |     |     |     |     | URL | pdf. |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
https://arxiv.org/abs/2601.07641.
|     |     |     |     |     |     |     | [43] Guanzhi | Wang, | Yuqi | Xie, | Yunfan | Jiang, |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | ---- | ---- | ------ | ------ |
[37] Amanda A. Volk and Milad Abolhasani. Ajay Mandlekar, Chaowei Xiao, Yuke Zhu,
Performancemetricstounleashthepowerof Linxi Fan, and Anima Anandkumar. Voy-
self-driving labs in chemistry and materials ager: An open-ended embodied agent with
science. Nature Communications, 15:1378, largelanguagemodels. Transactions on Ma-
2024. doi: 10.1038/s41467-024-45569-5. chine Learning Research, 2024. ISSN 2835-
|                |     |           |     |        |         |        | 8856. | URL | https://openreview.net/ |     |     |     |
| -------------- | --- | --------- | --- | ------ | ------- | ------ | ----- | --- | ----------------------- | --- | --- | --- |
| [38] Sebastian |     | Farquhar, |     | Jannik | Kossen, | Lorenz |       |     |                         |     |     |     |
forum?id=ehfRiF0R3a.
| Kuhn, |     | and Yarin | Gal. | Detecting |     | halluci- |     |     |     |     |     |     |
| ----- | --- | --------- | ---- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
nations in large language models using se- [44] Charles Packer, Sarah Wooders, Kevin Lin,
mantic entropy. Nature, 630(8017):625–630, Vivian Fang, Shishir G. Patil, Ion Stoica,
2024. doi: 10.1038/s41586-024-07421-0. and Joseph E. Gonzalez. Memgpt: To-
|            |     |       |           |     |     |          | wardsllmsasoperatingsystems, |     |     |     |     | 2024. URL |
| ---------- | --- | ----- | --------- | --- | --- | -------- | ---------------------------- | --- | --- | --- | --- | --------- |
| [39] Scott | M.  | Reed. | Augmented |     | and | program- |                              |     |     |     |     |           |
https://arxiv.org/abs/2310.08560.
| matically |     | optimized |     | llm | prompts | reduce |     |     |     |     |     |     |
| --------- | --- | --------- | --- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- |
chemical hallucinations. Journal of Chemi- [45] Joon Sung Park, Joseph O’Brien, Car-
cal Information and Modeling, 65(9):4274– rie Jun Cai, Meredith Ringel Morris, Percy
4280, May 2025. ISSN 1549-9596. doi: Liang, and Michael S. Bernstein. Genera-
10.1021/acs.jcim.4c02322. URL https:// tive agents: Interactive simulacra of human
doi.org/10.1021/acs.jcim.4c02322. behavior. In Proceedings of the 36th An-
|             |              |       |                           |         |        |          | nual ACM                      |            | Symposium   |             | on User        | Interface |
| ----------- | ------------ | ----- | ------------------------- | ------- | ------ | -------- | ----------------------------- | ---------- | ----------- | ----------- | -------------- | --------- |
| [40] Liyuan |              | Wang, | Xingxing                  | Zhang,  |        | Hang Su, |                               |            |             |             |                |           |
|             |              |       |                           |         |        |          | Software                      | and        | Technology, |             | UIST           | ’23, New  |
| and         | Jun          | Zhu.  | A comprehensive           |         |        | survey   |                               |            |             |             |                |           |
|             |              |       |                           |         |        |          | York,                         | NY, USA,   | 2023.       | Association |                | for Com-  |
| of          | continual    |       | learning:                 | Theory, |        | method   |                               |            |             |             |                |           |
|             |              |       |                           |         |        |          | puting                        | Machinery. |             | ISBN        | 9798400701320. |           |
| and         | application. |       | IEEE                      |         | Trans. | Pattern  |                               |            |             |             |                |           |
|             |              |       |                           |         |        |          | doi: 10.1145/3586183.3606763. |            |             |             |                | URLhttps: |
| Anal.       | Mach.        |       | Intell., 46(8):5362–5383, |         |        | 2024.    |                               |            |             |             |                |           |
//doi.org/10.1145/3586183.3606763.
| ISSN | 0162-8828. |     | doi: | 10.1109/TPAMI. |     |     |     |     |     |     |     |     |
| ---- | ---------- | --- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
2024.3367329. URL https://doi.org/10. [46] Siyu Liu, Bo Hu, Beilin Ye, Jiamin
| 1109/TPAMI.2024.3367329. |       |          |         |         |             |         | Xu,               | David     | J Srolovitz, |           |     | and Tongqi     |
| ------------------------ | ----- | -------- | ------- | ------- | ----------- | ------- | ----------------- | --------- | ------------ | --------- | --- | -------------- |
|                          |       |          |         |         |             |         | Wen.              | Mattools: | Benchmarking |           |     | large lan-     |
| [41] Shunyu              |       | Yao,     | Jeffrey | Zhao,   | Dian        | Yu, Nan |                   |           |              |           |     |                |
|                          |       |          |         |         |             |         | guage             | models    | for          | materials |     | science tools. |
| Du,                      | Izhak | Shafran, |         | Karthik | Narasimhan, |         |                   |           |              |           |     |                |
|                          |       |          |         |         |             |         | arXiv:2505.10852, |           |              | 2025.     |     |                |
| and                      | Yuan  | Cao.     | ReAct:  |         | Synergizing | rea-    |                   |           |              |           |     |                |
soning and acting in language models. In [47] Jess Wellendorff, Keld T Lundgaard, An-
International Conference on Learning Rep- dreas Møgelhøj, Vivien Petzold, David D
resentations (ICLR), 2023. Landis, Jens K Nørskov, Thomas Bligaard,
|           |         |      |               |             |           |            | and Karsten           |             | W Jacobsen. |                      | Density     | function- |
| --------- | ------- | ---- | ------------- | ----------- | --------- | ---------- | --------------------- | ----------- | ----------- | -------------------- | ----------- | --------- |
| [42] Noah | Shinn,  |      | Federico      | Cassano,    |           | Ashwin     |                       |             |             |                      |             |           |
|           |         |      |               |             |           |            | alsforsurfacescience: |             |             | Exchange-correlation |             |           |
| Gopinath, |         |      | Karthik       | Narasimhan, |           | and        |                       |             |             |                      |             |           |
|           |         |      |               |             |           |            | model                 | development |             | with                 | bayesian    | error es- |
| Shunyu    |         | Yao. | Reflexion:    |             | language  | agents     |                       |             |             |                      |             |           |
|           |         |      |               |             |           |            | timation.             | Physical    |             | Review               | B—Condensed |           |
| with      | verbal  |      | reinforcement |             | learning. | In         |                       |             |             |                      |             |           |
|           |         |      |               |             |           |            | Matter                | and         | Materials   |                      | Physics,    | 85(23):   |
| A.        | Oh,     | T.   | Naumann,      |             | A.        | Globerson, |                       |             |             |                      |             |           |
|           |         |      |               |             |           |            | 235149,               | 2012.       | doi:        | 10.1103/PhysRevB.85. |             |           |
| K.        | Saenko, |      | M. Hardt,     |             | and       | S. Levine, |                       |             |             |                      |             |           |
235149.
| editors, |     | Advances | in  | Neural | Information |     |     |     |     |     |     |     |
| -------- | --- | -------- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
Processing Systems, volume 36, pages [48] Weiqing Zhou, Daye Zheng, Qianrui Liu,
8634–8652. Curran Associates, Inc., 2023. Denghui Lu, Yu Liu, Peize Lin, Yike Huang,
URL https://proceedings.neurips. XingliangPeng,JieJ.Bao,ChunCai,Zuxin
20

Jin, Jing Wu, Haochong Zhang, Gan Jin, and embedded-atom calculations. Phys-
Yuyang Ji, Zhenxiong Shen, Xiaohui Liu, ical Review B, 63(22):224106, 2001. doi:
LiangSun,YuCao,MenglinSun,Jianchuan 10.1103/PhysRevB.63.224106.
| Liu,   | Tao      | Chen,   | Renxi  |          | Liu,   | Yuanbo     | Li,   |                    |                |                  |            |             |            |
| ------ | -------- | ------- | ------ | -------- | ------ | ---------- | ----- | ------------------ | -------------- | ---------------- | ---------- | ----------- | ---------- |
|        |          |         |        |          |        |            |       | [54] T. Hehenkamp, |                | W.               | Berger,    | J.-E.       | Kluin,     |
| Haozhi | Han,     | Xinyuan |        | Liang,   |        | Taoni      | Bao,  |                    |                |                  |            |             |            |
|        |          |         |        |          |        |            |       | C. Lüdecke,        |                | and J.           | Wolff.     | Equilibrium |            |
| Zichao | Deng,    | Tao     | Liu,   | Nuo      | Chen,  | Hongxu     |       |                    |                |                  |            |             |            |
|        |          |         |        |          |        |            |       | vacancy            | concentrations |                  | in         | copper      | investi-   |
| Ren,   | Xiaoyang |         | Zhang, | Zhaoqing |        | Liu,       | Yiwei |                    |                |                  |            |             |            |
|        |          |         |        |          |        |            |       | gated with         | the            | absolute         | technique. |             | Physi-     |
| Fu,    | Maochang |         | Liu,   | Zhuoyuan |        | Li, Tongqi |       |                    |                |                  |            |             |            |
|        |          |         |        |          |        |            |       | cal Review         | B,             | 45(5):1998–2003, |            |             | 1992. doi: |
| Wen,   | Zechen   | Tang,   | Yong   | Xu,      | Wenhui |            | Duan, |                    |                |                  |            |             |            |
10.1103/PhysRevB.45.1998.
| Xiaoyang |     | Wang, | Qiangqiang |     |     | Gu, Fu-Zhi |     |     |     |     |     |     |     |
| -------- | --- | ----- | ---------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Dai, Qijing Zheng, Yang Zhong, Hongjun [55] R. Yan, Q. Zhang, W. Li, I. Calizo,
Xiang, Xingao Gong, Jin Zhao, Yuzhi T. Shen, C. A. Richter, A. R. Hight Walker,
Zhang, Qi Ou, Hong Jiang, Shi Liu, Ben X. Liang, A. Seabaugh, D. Jena, H. G.
Xu, Shenzhen Xu, Xinguo Ren, Lixin He, Xing, D. J. Gundlach, and N. V. Nguyen.
Linfeng Zhang, and Mohan Chen. Aba- Determination of graphene work function
cus: An electronic structure analysis pack- andgraphene-insulator-semiconductorband
age for the ai era. The Journal of Chemi- alignment by internal photoemission spec-
cal Physics, 163(19):192501, 11 2025. ISSN troscopy. Applied Physics Letters, 101(2):
0021-9606. doi: 10.1063/5.0297563. URL 022105, 2012. doi: 10.1063/1.4734955.
https://doi.org/10.1063/5.0297563.
| [49] Martin     | Schlipf           |           | and        | François | Gygi.      |         | Opti- |     |     |     |     |     |     |
| --------------- | ----------------- | --------- | ---------- | -------- | ---------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
| mization        |                   | algorithm |            | for the  | generation |         | of    |     |     |     |     |     |     |
| oncv            | pseudopotentials. |           |            | Computer |            | Physics |       |     |     |     |     |     |     |
| Communications, |                   |           | 196:36–44, |          |            | 2015.   | doi:  |     |     |     |     |     |     |
10.1016/j.cpc.2015.05.011.
| [50] Materials |     | Project.   |     |            | Gaas |        | (mp- |     |     |     |     |     |     |
| -------------- | --- | ---------- | --- | ---------- | ---- | ------ | ---- | --- | --- | --- | --- | --- | --- |
| 2534):         |     | Electronic |     | structure. |      | https: |      |     |     |     |     |     |     |
//next-gen.materialsproject.org/
materials/mp-2534?chemsys=Ga-As#
| electronic_Structure, |     |     |     |     | 2026. | Accessed |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
2026-04-24.
| [51] I. Vurgaftman, |         |                | J.                 | R. Meyer,          |              | and   | L. R.   |     |     |     |     |     |     |
| ------------------- | ------- | -------------- | ------------------ | ------------------ | ------------ | ----- | ------- | --- | --- | --- | --- | --- | --- |
| Ram-Mohan.          |         |                | Band               | parameters         |              | for   | iii–v   |     |     |     |     |     |     |
| compound            |         | semiconductors |                    |                    | and          | their | alloys. |     |     |     |     |     |     |
| Journal             | of      | Applied        |                    | Physics,           | 89(11):5815– |       |         |     |     |     |     |     |     |
| 5875,               | 2001.   | doi:           | 10.1063/1.1368156. |                    |              |       |         |     |     |     |     |     |     |
| [52] Ľubomír        |         | Vančo,         | Magdaléna          |                    | Kadlečíková, |       |         |     |     |     |     |     |     |
| Juraj               | Breza,  | Jaroslava      |                    | Škriniarová,       |              |       | and     |     |     |     |     |     |     |
| Pavol               | Hronec. |                | Interference       |                    | enhanced     |       | first-  |     |     |     |     |     |     |
| order               | raman   | band           |                    | of monocrystalline |              |       | sil-    |     |     |     |     |     |     |
| icon.               | Vacuum, |                | 110:102–105,       |                    |              | 2014. | doi:    |     |     |     |     |     |     |
10.1016/j.vacuum.2014.09.004.
| [53] Y.          | Mishin,    | M.  | J.        | Mehl,     | D.             | A.      | Papa- |     |     |     |     |     |     |
| ---------------- | ---------- | --- | --------- | --------- | -------------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
| constantopoulos, |            |     | A.        | F. Voter, |                | and     | J. D. |     |     |     |     |     |     |
| Kress.           | Structural |     | stability |           | and            | lattice | de-   |     |     |     |     |     |     |
| fects            | in copper: |     | Ab        | initio,   | tight-binding, |         |       |     |     |     |     |     |     |
21