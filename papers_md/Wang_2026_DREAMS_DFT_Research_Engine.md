DREAMS: Density Functional Theory Based
Research Engine for Agentic Materials
Simulation
Ziqi Wang1, Hongshuo Huang1, Hancheng Zhao1,
Changwen Xu1, Shang Zhu1, Jan Janssen3*,
Venkatasubramanian Viswanathan1,2*
1Department of Mechanical Engineering, University of Michigan.
2Department of Aerospace Engineering, University of Michigan.
3Department of Computational Materials Design, Max-Planck-Institute
for Sustainable Materials.
*Corresponding author(s). E-mail(s): janssen@mpi-susmat.de;
venkvis@umich.edu;
Abstract
Large language model (LLM) agents can execute long-horizon scientific work-
flows,buttheirnumericaloutputsaredifficulttotrust:agentslosecontext,game
verificationchecks,andcanproducelargevolumesofplausibleyetinvalidresults.
We introduce the DFT-based Research Engine for Agentic Materials Simulation
(DREAMS), a hierarchical multi-agent framework for density functional theory
(DFT) built around a multi-tier safety guard. The guard applies deterministic
checks wherever explicit criteria exist and scoped LLM judgment elsewhere,
evaluating one parameter at a time and tracing every value to its registered
source. Verification extends from tool-call time, where fabricated, laundered, or
unsourcedvaluesarerejectedbeforeenteringtheworkflow,toreporttime,where
a judge audits the full provenance graph behind every claim; a shared canvas
preservesinformationintegrityacrosshundredsofsteps.DREAMSachievesaver-
age errors below 1% on the Sol27LC lattice-constant benchmark, reproduces
expert-level adsorption-energy differences on the CO/Pt(111) puzzle, and quan-
tifies functional-driven uncertainty with Bayesian ensemble sampling, confirming
theface-centered-cubic(FCC)sitepreferenceatthegeneralizedgradientapprox-
imation (GGA) level. Compared with its unguarded counterpart, which reached
a nearly correct answer while only 81% of its essential steps succeeded, the
guardedsystemverifieseveryessentialstepatapproximately13timestheinput
1
6202
guA
11
]IA.sc[
2v76241.7052:viXra

tokens; verification layers can be disabled individually to balance trustworthi-
ness against cost, and the tuned judge rules transfer across five judge models.
DREAMSoperatesatanenhancedL2(L2+)automationlevelanddemonstrates
capabilities approaching L3 automation, providing a path toward trustworthy,
high-throughputautonomousmaterialssimulation.
Introduction
Density functional theory (DFT) is widely used in computational materials science
to predict electronic, structural, and thermodynamic properties at moderate compu-
tational cost [1]. DFT-based screening has identified candidate materials for energy,
catalysis, and structural applications [2, 3]. However, constructing reliable high-
throughput DFT workflows still requires substantial expert involvement, which limits
throughput [4] and can introduce cognitive biases into the exploration of materials
design spaces [5]. Expert oversight includes selecting computational parameters,
evaluatinganomalousresults,anddeterminingwhethertheresultingdataarescien-
tificallyvalid.Autonomoussystemsmustthereforereproduceboththeexecutionand
validationfunctionsperformedbyhumanexperts.Inanalogywithtaxonomiesdevel-
oped for autonomous vehicles and automated chemical design [6, 7], we define six
levelsofautomationforcomputationalscienceagents,assummarizedinTable1.
Current automation in materials science relies primarily on predefined computa-
tionalpipelinesimplementedthroughworkflowmanagementsystems(WfMS)[8–14].
These systems support reproducible workflow construction and large-scale execu-
tion.However,becausetheircontrollogicisspecifiedinadvance,theyaregenerally
limited to L1 automation and cannot readily revise search strategies or respond to
unanticipatedfailures.
Large language model (LLM) agents may support higher levels of automation
by combining foundation models with domain-specific tools [15–18]. These systems
can evaluate intermediate results, revise plans, and respond to execution failures,
enablingL2andpotentiallyhigherlevelsofautomation.EarlyexamplesincludeSciA-
gents[19],whichusedmultipleagentsandontologicalknowledgegraphstogenerate
research hypotheses, and Coscientist [20], which integrated planning, web search,
codeexecution,androboticexperimentation.Relatedsystemshavebeendeveloped
fororganicsynthesisandmoleculardynamics[21,22],computationalchemistry[23,
24], protein discovery [25, 26], and inorganic-materials design and synthesis [27].
Agent-basedmethodshavealsobeenappliedtoresearchideation,manuscriptgen-
eration,toolorchestration,theoreticalphysics,pharmaceuticalresearch,andprotein
design[28–35].
The development of scientific LLM agents has not been accompanied by equiv-
alent methods for verifying their numerical outputs. Here, long-horizon denotes
workflows with many sequential, state-dependent LLM and tool calls, where later
actionsrelyonscientificstategeneratedmuchearlier,withtherelevantscaledepend-
ing on the model and system configuration. During long-horizon development runs,
2

Table 1: Levels of automation for computational science
agents. Six levels (L0–L5) describe how responsibility shifts
fromhumantomachineacrossfivestagesofacomputational
study. Scientific Question: formulating the research problem
to pursue given a broad objective. Design Space: specify-
ing the candidate solutions, variables, and constraints to be
explored.SearchAlgorithm: designingandimplementingthe
strategy used to search the design space, such as selecting
tools, sampling methods, or optimization procedures. Exe-
cution: orchestrating the workflow, including setting up cal-
culations, launching computation packages, and processing
results. Exception Handling: detecting and resolving failures
during execution, from routine errors handled by predefined
logic to complex faults requiring case-by-case judgment. At
everylevelshortoffullautomation,theexpertdoesmorethan
execute procedures: at each stage of a study it is a human
whovetsparameterchoices,questionsanomalousnumbers,
and decides which results can be trusted. Automation that
removes the expert must therefore also replace the scrutiny
theexpertwassilentlysupplying.
Scientific Design Search Exception
Level Execution
Question Space Algorithm Handling
L0
L1
L2
L3
L4
L5
Legend: =human; =machine; =machinewithhumansupervision.
we observed recurrent failures, including loss of task history, disregard of con-
vergence results, attempts to bypass tool refusals, incorrect arithmetic, reduced
verificationduringextendedexecutions,andcircumventionofprovenancechecks.In
one case, an unsupported value was passed through the identity x+0, producing
a valid provenance record without validating the original value. These observations
areconsistentwithreportedfailuresinvolvingspecificationgamingandrewardhack-
ing [36], sycophancy [37], errors in multistep arithmetic [38], reduced instruction
adherence over long horizons [39, 40], and autonomous research agents [41, 42].
They are compounded by hallucination, including fabricated values, unsupported
approximations, and incorrect reuse of upstream results [43–47]. Because scientific
calculations depend on upstream results, a single error can propagate through the
workflowandinvalidatesubsequentconclusions.
3

Existingsafeguardsaddressindividualaspectsofthisproblembutdonotdirectly
verify numerical claims. Provenance and observability frameworks record agent
actionsanddatadependencies[10,48],butdonotdeterminewhethertherecorded
operations or parameters are scientifically valid. Critic and judge agents assess
response quality [49–51], but generally evaluate final outputs rather than the com-
putational origin of individual values. Their assessments can also be affected
by bias and evaluation manipulation [52, 53]. Committee methods such as self-
consistency voting [54] increase the cost of workflows containing many sequential
tool calls [55, 56] and cannot resolve errors shared across model outputs [57, 58].
Adversarial questioning and self-revision methods [37, 59–61] are unreliable when
the model lacks an external signal for identifying errors and may reduce accu-
racy [62]. A verification framework for scientific agents must instead determine
whether each reported quantity and its computational parameters are supported by
validupstreamoperationsandtraceablesources.
To address this requirement, we introduce the DFT-based Research Engine for
Agentic Materials Simulation (DREAMS), a hierarchical multi-agent framework for
autonomous DFT research. DREAMS applies deterministic validation when explicit
checks are available and uses LLM-based evaluation for criteria that require con-
textual judgment. LLM evaluations are organized into scoped rule sets, applied to
individual parameters, and linked to the source of each value. Verification is per-
formed from tool execution through final reporting to prevent invalid values from
propagating through the workflow. DREAMS also uses an append-only provenance
record and a centralized shared memory, termed the canvas, which mediates com-
munication among the planning supervisor, worker agents, tools, and user (Fig. 1).
Theplanningsupervisordecomposesresearchobjectivesintotasks,assignsthemto
domain-specificagents,andupdatestheplanusingintermediateresults.Adedicated
convergenceagentdiagnosesfailuresduringexecution,whileaseparatedebugging
tool investigates unexpected completed results by tracing reported values through
theirupstreamdependencies.
We implement DREAMS for periodic solid-state DFT, a domain in which numeri-
calvaliditydependsonmultiplecoupledcomputationalsettings.Mostexistingagentic
systems in materials science and chemistry use cheminformatics tools, classical
moleculardynamics,ormachine-learnedsurrogatemodels[21,22,63].Systemsthat
incorporate DFT have focused primarily on molecular calculations [23, 24]. Periodic
solid-state calculations, commonly performed with plane-wave DFT codes such as
Quantum ESPRESSO (QE) [64], require careful selection of the plane-wave cutoff,
k-pointsampling,smearing,andrelatednumericalparameters.
Thissettingpresentstwoclassesoffailure.In-executionfailuresoccurwhencal-
culations terminate or fail to converge. Their diagnosis may require joint analysis of
input parameters, output logs, error files, and domain-specific constraints [65, 66].
Post-executionfailuresoccurwhenacalculationcompletesbutproducesaresultthat
is inconsistent with prior literature, intermediate calculations, or expected physical
behavior.Thesecasesrequiresystematicinspectionoftheparametersandupstream
computations that produced the result. Explanations such as numerical instabil-
ity or insufficient sampling are not sufficient without evidence from the execution
4

record. Periodic solid-state DFT therefore provides a suitable domain for evaluat-
ing autonomous error recovery, parameter-level verification, and provenance-based
diagnosis.
D  R  E  A  M  S
|     | (a) Supervisor | (b) | Safety Guards   |     | (f)Canvas |
| --- | -------------- | --- | --------------- | --- | --------- |
|     |                |     | DFT Agent Tools |     | Notes     |
Objective:find the
| most preferable                    |                   | Query            |                                                    |                          |                                       |
| ---------------------------------- | ----------------- | ---------------- | -------------------------------------------------- | ------------------------ | ------------------------------------- |
| c o n f ig u r a ti o n  o f  C O  |                   |                  | G e n e r a t e   O p t i m i z e                  | K - p o i n t   S a v e  | D F T   i n p u t   Ca lc u la t ion  |
| o n   P t( 1 1 1 )  s u rf a ce    |                   | Assign           | S C t r r u y c s t t u a r l e   S e t t in g s S | a m p l i n g F ile s    | a n d   o u t p u t   R e s u lt      |
|                                    | Generate & Modify | DFT Agent Result | (d)                                                |                          | f i l e s                             |
Task N
|     |      | to      | C L o L n M ve A rg g e e n n c t e  |      | HPC Job           |
| --- | ---- | ------- | ------------------------------------ | ---- | ----------------- |
|     |      | Agent X |                                      | Read | Su b m i s s ion  |
|     | Plan |         |                                      |      | S c ri p t s      |
✓1
Safety
| User |      | Response (c) | Sa fe t y  G   | u a r ds Record |        |
| ---- | ---- | ------------ | -------------- | --------------- | ------ |
|      | x✓22 |              | HP C  A ge nt  | To o ls         | Guards |
Artifacts
|                               | 3   | Query             |                                       |                                                           |                              |
| ----------------------------- | --- | ----------------- | ------------------------------------- | --------------------------------------------------------- | ---------------------------- |
| A n sw e r :  a t  l o w      |     |                   | Lo a d   J o b  R G u e n n  S er c a | r t ip e t   M S o u n b i m to i r t     J a o n b d s   | DFT resultsCa l cu la t ion  |
| c o ve ra g e   (<   1 / 3)   | 4   |                   | S c r i p t                           |                                                           | r e su lt s                  |
| th e   p e r f e r e d        |     | HPC Agent Result  | (e)                                   |                                                           |                              |
|                               | 5   |                   | H P C                                 |                                                           |                              |
| co n fi g u r a t i o n  i s  |     |                   | Cl u st er                            |                                                           | Relaxation                   |
| FCC                           |     |                   |                                       |                                                           | results                      |
|                               | 6   |                   |                                       |                                                           | Reports                      |
|                               | 7   | Report (g) Report |                                       | Judge                                                     |                              |
Judge
|     |     | Agent |                        |        | Report1 Report2 |
| --- | --- | ----- | ---------------------- | ------ | --------------- |
|     |     |       | Rule 1 Rule 1NS Rule 2 | Rule 3 |                 |
Fig. 1: DREAMS combines: (a) Planning supervisor: generates and updates task
plans based on the research objective and real-time progress, and assigns tasks
to the appropriate worker agents. (b) DFT Agent: handles the computation pipeline,
including structure generation, calculation-setting determination, calculation script
generation, convergence-issue resolution, and related tasks. (c) HPC Agent: allo-
cates computational resources, submits simulations, monitors their execution, and
retrieves output files. The tools of (b) and (c) are wrapped in safety guards that
deterministicallyverifyvaluesandtheirprovenanceandsemanticallyjudgeparame-
terization at tool-call time, before a result can be registered; every registered result
carriesfullprovenance.(d)ConvergenceAgent:achildagentoftheDFTagentthat
diagnoses convergence issues from a job’s input, output, and error files, offloading
heterogeneous-diagnosticinterpretationfromthemainDFT-agentreasoningloop.(e)
HPCcluster,wheretheHPCagentschedules,monitors,andretrievessimulations.(f)
Canvas: a shared memory system across agents, tools, and the human user, orga-
nizedintoNotes,Artifacts,andReports,withsafetyguardsonArtifactsandReports
verifying that values are sourced from registered tool outputs and that claims trace
back to those values; reports, once verified, become immutable. (g) Report Judge
Agent: audits each structured report at generation time—at least one intermediate
and one final report per study—against multilevel, adversarially tuned rules cover-
ing value provenance, claim–source coherence, parameter sensitivity, and rationale
quality, returning any failures with category-specific remediation hints for the super-
visortoacton.
5

We evaluate DREAMS on three periodic DFT benchmarks. First, DREAMS cal-
culates lattice constants for the 27 elemental crystals in the Sol27LC dataset [67],
spanning multiple crystal structures, with accuracy comparable to expert calcula-
tions. Second, we evaluate DREAMS on the “CO/Pt(111) puzzle” [68], a widely
studied catalytic system [69] whose predicted adsorption-site preference is sensi-
tive to computational settings [68, 70, 71]. DREAMS reproduces the site preference
reportedinpreviousDFTstudies[68,71,72].Third,DREAMSquantifiesuncertainty
associatedwiththechoiceofexchange-correlationfunctionalusingBayesianstatis-
tics [67]. Charge-transfer analysis is further used to examine the electronic origin of
thepredictedsitepreference.
For each reported quantity, DREAMS constructs a machine-verified provenance
chainfromthefinalresulttothetoolcallsthatproducedit.Computationalparameters
areevaluatedusingdeterministicchecksandscopedLLM-basedrules.Therulesare
refined through adversarial testing and evaluated using five judge models. We also
compareDREAMSwithrepresentativeagenticframeworksthatlacksharedmemory
and verification, and with an ablated version of DREAMS without the safety guard.
Full verification increases token usage by approximately one order of magnitude.
Because individual verification layers can be disabled independently, the framework
permitsdifferenttrade-offsbetweenverificationcoverageandcomputationalcost.
DREAMS contributes a general verification architecture for scientific agents. It
combines append-only provenance records, verification from tool execution to final
reporting, parameter-level LLM evaluation, validated numerical operations and data
extraction,andintegrity-preservingcommunicationthroughthecanvas.Thesecom-
ponentsareindependentoftheunderlyingcomputationalmethodandcanbeapplied
toworkflowsthatrequireauditablenumericalresults.Adedicatedconvergenceagent
diagnosesin-executionfailures,whilethedebuggingtoolinvestigatespost-execution
anomaliesbytracingreportedvaluesthroughtheirupstreamdependencies.
For computational materials research, DREAMS implements this architecture
for autonomous periodic solid-state DFT. It does not introduce new physical mod-
els or simulation methods; its contribution is the verified application of established
methods and expert decision criteria within an end-to-end workflow. Across tasks
involving high-level planning, error recovery, and parameter-sensitive calculations,
DREAMS demonstrates capabilities approaching L3 automation and provides a
basisforreliableautonomousmaterialssimulation.
Results
Multi-agent orchestration and a shared canvas preserve
information integrity across long-horizon workflows
DREAMS is a hierarchical multi-agent framework for periodic solid-state DFT work-
flows.AllDFTcalculationsreportedherewereperformedwithQuantumESPRESSO
(QE).Thesupervisordispatchesoneworkerstepatatimeinasynchronous,sequen-
tial control loop, so the DFT and HPC agents do not execute concurrently. The
supervisormaysynchronouslyconsultaworkerfordomain-specificinput,butretains
solecontroloverplanningandtaskassignment.WithinanHPCstep,independentQE
6

jobssubmittedasabatchmayrunconcurrentlyasscheduledbySLURM.Itconsists
ofaplanningsupervisorandspecializedworkeragentsfor DFTsetupandanalysis,
HPC execution, and convergence diagnosis (Fig. 1). In all studies, the supervisor
and worker agents use Claude Sonnet 4.5 [73] at temperature zero. They differ
only in their role-specific prompts, permitted actions, and tool access. The safety-
guard judges use Claude Opus 4.8 [74]. For reproducibility, the complete DREAMS
agentpromptsareprovidedinSupplementaryInformationS-7,thetoolinterfacesin
S-8, and the modified MDCrow and ChemGraph prompts in S-10; the exact bench-
mark objectives are reproduced below in the corresponding Results subsections.
We use fidelity to denote the rigor of workflow execution, including convergence of
theplane-wavecutoffandk-pointsampling,appropriatepseudopotentials,andsuffi-
cientslabandvacuumdimensions.Weuseaccuracy todenotenumericalagreement
with a reference. We use validation to denote post-calculation checks of conver-
gence and internal consistency before a result is accepted. Agent-selected values
used only for structure initialization are not treated as validation. This subsection
describes the orchestration and communication layer responsible for information
integrity.Thefollowingsubsectiondescribesthesafety-guardsystemresponsiblefor
valueintegrity.
The planning supervisor generates and updates multi-step plans and selects
the agent responsible for each task. The DFT agent provides tools for structure
generation, pseudopotential selection, DFT input and script preparation, conver-
gence testing, output analysis, and result extraction. Structure generation uses
AutoCat [14] to identify adsorption sites and ASE [75] to represent structures and
prepareQuantumESPRESSOinputs.TheHPCagentmanagesresourceselection,
job submission, job monitoring, and file retrieval. The convergence agent analyzes
input,output,anderrorfileswhencalculationsfailorrequireadditionaldiagnosis,and
recommends parameter modifications. The tools expose the scientific parameters
required for each task while hiding implementation details that do not require agent
control. Built-in validation checks and diagnostic messages support error correction
and recovery from failed tool calls. This design constrains agent actions, reduces
unsupported outputs, and preserves the flexibility required for multi-step scientific
workflows.
A central component of DREAMS is the canvas, a persistent shared memory
for communication among the supervisor, worker agents, tools, and human user.
The canvas stores intermediate variables and results in their native formats across
threestores:notes,version-controlledappend-onlyworkingdocuments;artifacts,an
append-only registry of tool outputs described in the next subsection; and reports,
structured scientific results that become immutable after verification. Each object is
assigned a descriptive key, allowing agents to retrieve relevant information without
retaining the full conversation history. Framework-managed key spaces, including
judge feedback and archived records, are readable but not writable by agents. The
user can inspect the canvas at any time during execution. Additional details on the
canvasandmemoryarchitectureareprovidedintheMethodssection.
To limit context growth during long-horizon studies, DREAMS compresses exe-
cution history after a report is verified. The steps used to produce the report are
7

archived on the canvas and replaced in the active history by a single summary
record. The archive and original step numbering are preserved, maintaining a com-
pleteaudittrailwhilereducingtheactivecontext.Becausecompressionoccursonly
afterverification,theretainedsummarycontainsinformationthathasalreadypassed
theframework’svalidationchecks.
A multi-tier safety guard verifies values deterministically and
semantically from tool call to final report
EverytooloutputinDREAMSisstoredinanappend-onlyprovenanceregistryunder
animmutableresultidentifier.Whenanagentusesavalueinasubsequenttoolcall,
itmustprovidethevalueandareferencetoitsregisteredsource.Thereferencemay
identifyeitheracompleteresultoraninputparameterfromanearliercallusingdot-
ted notation. Both reference types are verified deterministically but evaluated using
differentsemanticrules.Eachguardedtoolcallmustalsospecifyitscontextandpro-
vide a justification for every parameter. These declarations support error prevention
duringexecutionandprovidetheinformationrequiredforsubsequentsemanticeval-
uation. Each registered artifact therefore records the producing tool, output value,
completeargumentlist,parameter-specificjustifications,parameter-specificsources,
anddeclaredcontextunderitsimmutableidentifier.
Verification is applied at each guarded tool call in multiple tiers (Fig. 2). Deter-
ministic checks first confirm that each referenced source exists in the provenance
registryandthatitsrecordedvaluematchesthevaluesuppliedbytheagent.Seman-
ticevaluationthenproceedsintwostages.Thefirstjudgeevaluateseachparameter
independently using the declared context and parameter-specific justification. The
second evaluates the parameter set jointly for internal consistency, comparability,
andvalidityoftheproposedcalculation.Mathematicaloperationsanddataextraction
receive additional deterministic and semantic checks because they can introduce
derivednumericalvalues.Ifallcheckspass,thetoolexecutesanditsoutputisregis-
tered.Becauseeachtoolcallidentifiesitsinputsources,theframeworkconstructsa
directed acyclic provenance graph during execution. Each numerical claim must be
reportedwithareferencetotheartifactcontainingtheclaimedvalueandthebroader
study context. The report-level judge then traces the claim through its upstream
dependenciesandevaluateswhethereachparameterwasappropriateforproducing
thatresult.
DREAMS maintains flexibility through two mechanisms. Arithmetic operations
andvalueextractionfromrawtextareimplementedasguardedtoolssothatderived
values remain within the provenance system. These tools receive additional deter-
ministicandsemanticchecks.Thejudgingcriteriaarealsoconditionedontaskintent.
Forexample,acoarseparameterusedinanexploratorycalculationisevaluateddif-
ferently from the same parameter used to support a final claim. The complete rule
hierarchy,judgeprompts,andfailurecategoriesareprovidedinSupplementaryInfor-
mation S-11. The guard does not establish the physical correctness of a result, but
it increases confidence by verifying the operations, sources, and parameter choices
usedtoproduceit.
8

(a)
| Text/number          | Extraction           |               |     |     |     |
| -------------------- | -------------------- | ------------- | --- | --- | --- |
| extraction tool call | Deterministic checks | Extract judge |     |     |     |
Math Deterministic
| Math tool call | checks | Math judge |     |     |     |
| -------------- | ------ | ---------- | --- | --- | --- |
(a)
Cross-parameter
| Other tool call | Deterministic checks | Per-parameter judge |     |     | Tool content |
| --------------- | -------------------- | ------------------- | --- | --- | ------------ |
judge
|     |     | Fail → value never registered |     |     | Execute & register |
| --- | --- | ----------------------------- | --- | --- | ------------------ |
(b)
E (slab+CO)
| Structure | QE script | HPC jobs | E (slab) | E (math) | Report          |
| --------- | --------- | -------- | -------- | -------- | --------------- |
|           |           |          |          | ads      | claim ⇐artifact |
| Report    |           |          |          |          | Report          |
| Judge     |           |          | E (CO)   |          |                 |
Judge
Report
Report
|     |     |     |     | Judge | PASS |
| --- | --- | --- | --- | ----- | ---- |
Judge
Fail 1: <reason> · <Location> · <parameter>        Warning 1: <reason> · <Location> · <parameter>
Fig. 2: The DREAMS safety guard, from tool call to final report. (a) Verification tiers
applied at every guarded tool call. The call supplies a declared context, one rea-
son per parameter, and, for sourced values, the value together with a reference to
theregisteredresultitcamefrom.Deterministicchecksrunfirst,verifyingthatevery
referenced source exists in the append-only registry and that the supplied value
matches the recorded one. Two LLM judges follow: the per-parameter judge reads
thecontextandeachparameter’sreasonandassesseseverysettingindividually;the
cross-parameterjudgeassessesallparametersjointly,askingwhethertheinputsare
contradictory, whether they are comparable, and whether the calculation is valid as
posed. Math and extraction calls enter through their own deterministic checks and
their own judges before joining the same per-parameter and cross-parameter tiers.
Only if all tiers pass does the tool body execute, and its output is registered as an
immutableartifactcarryingtheproducingtool,value,arguments,per-parameterrea-
sons and sources, and context. A failure at any tier means the tool does not run,
thevalueisneverregistered,andthejudge’sreasoningisreturnedtotheagent.(b)
Becauseeverycallnamesitsreferences,aprovenancegraphofregisteredartifacts
assembles automatically as the run proceeds, illustrated here for an adsorption-
energy workflow; arithmetic is performed only by the guarded math tool. Numerical
claims must be consolidated into structured reports that name the artifact carrying
each claim together with the study’s whole picture. The report-time judge walks the
graph back from the claim through every contributing source (dashed purple), ask-
ing of each parameter whether its setting makes sense in the production of that
specific claim; any issues are returned as categorized failures and warnings with
remediationhints(bottom),suchasavaluemismatchonasensitiveparameteroran
under-justified parameter choice, and a report that survives the full walk is marked
aspassedandbecomesimmutable.
9

WeevaluateDREAMSonthreeDFTtasksofincreasingcomplexity:theSol27LC
lattice-constantbenchmark,theCO/Pt(111)adsorption-siteproblem,anduncertainty
quantificationforexchange-correlationfunctionalselection.Sol27LCisusedtoexam-
ine the complete guarded workflow under a standardized and readily interpretable
task. Its execution log (Fig. 3) therefore reports grouped tool calls together with
the corresponding judge evaluations. The CO/Pt(111) problem evaluates the frame-
work on a much more sensitive workflow, in which the adsorption-energy difference
depends strongly on the computational settings. Because of the greater workflow
complexity, its execution log (Fig. 6) summarizes the principal agent-level events.
Within these execution logs, sub-blocks and listed entries summarize agent actions
within an assigned step; they are not one-to-one representations of tools and may
encompassmultipletoolcalls.
Validating DREAMS with Sol27LC benchmark
We first evaluateDREAMS on the Sol27LC lattice-constantbenchmark, which tests
execution of a complete DFT workflow against expert reference results. For each
element and crystal structure (e.g., bcc, fcc), DREAMS computes the equilibrium
lattice constant from total-energy calculations. The task specification provides the
elemental species and crystal structure, and DREAMS selects an initial lattice con-
stantfromwhichtheconventionalunitcellisconstructed.Thelatticevectorsarethen
uniformly scaled over a range extending up to ±5% of the initial lattice constant. A
single-pointDFTtotal-energycalculationisperformedforeachscaledstructure.Pro-
ductioncalculationsuseconvergedvaluesoftheplane-waveenergycutoff(ecutwfc)
and k-point sampling, selected by the agent to satisfy a specified total-energy tol-
erance. The workflow and convergence procedure are described in Fig. 3 and the
accompanying discussion. The calculated energy-volume data are fitted to a stan-
dard equation of state (EOS). The equilibrium volume is obtained by minimizing the
fittedEOS,andtheequilibriumlatticeconstantisderivedfromthisvolumeusingthe
specifiedcrystalsymmetry.
Forthisproblem,DREAMSisprovidedwithastructuredpromptspecifyingthetar-
get:Youaregoingtocalculatethelatticeconstantfor<Crystal-structure><Species>
throughDFT.
The complete workflow and execution trace are shown in Fig. 3. The planning
supervisor first generates an execution plan, provided in Supplementary Informa-
tion S-1, consisting of three report-bounded phases: an ecutwfc convergence test,
a k-point sampling convergence test, and the production calculation. During the
first phase, the DFT LLM agent constructs the initial crystal structure, selects the
pseudopotential, prepares the input templates, and generates the convergence-test
scripts.TheHigh-PerformanceComputing(HPC)LLMagentthenassignscomputa-
tional resources and submits the calculations to the HPC cluster. After completion,
the DFT LLM agent determines the converged ecutwfc and records the result in
a structured report. All deterministic checks and judge evaluations pass on the
first submission. The supervisor then advances to the k-point convergence phase,
which follows the same procedure and produces a second verified report. These
10

| You are going to  Supervisor |     |     |     |     |
| ---------------------------- | --- | --- | --- | --- |
calculate the lattice
constant for
<Crystal-structure>
<Species> through
| DFT.  | Plan  |     |     |     |
| ----- | ----- | --- | --- | --- |
Generated
|     | Structure  | DFT Agent     |     |     |
| --- | ---------- | ------------- | --- | --- |
|     | Generation | BulkStructure |     |     |
Generation
User
DFT Agent
E c u t w
|     |     | C o n v e r g e n c e  | Pseu d o p o te ntial  T e m p | l a t e  C o n v e rg e n c e       |
| --- | --- | ---------------------- | ------------------------------ | ----------------------------------- |
|     |     | T e s t   S e t  U p   | L o o k  U p S c r             | i p t   Te s t  P re p a r at i o n |
|     |     |                        | C r e a                        | t i o n                             |
HPC Agent
Ecutw
|     | Conv e r g ence  | C o n v e r ge n c e     | R e s o u r c e         | Jo b     |
| --- | ---------------- | ------------------------ | ----------------------- | -------- |
|     | T e s t          | Jo b   S u b m is s io n | A l lo c a t i o n Subm | i ss ion |
DFT Agent
R e p o r t
|     |     | Ge n e r at i o n | D e t er m in e   R e p o        | r t   R e p o r t  J u d g e    |
| --- | --- | ----------------- | -------------------------------- | ------------------------------- |
|     |     |                   | O p ti m a l e c u t Ge n e r at | i o n t ri g g e r d :  P A S S |
DFT Agent
K s p a c i n g
|     |                  | C o n v e r g e n c e    | Pseu d o p o te ntial  T e S m c r p | i p l a t t   e  C o n v e rg e n c e   |
| --- | ---------------- | ------------------------ | ------------------------------------ | --------------------------------------- |
|     |                  | T e s t   S e t  U p     | L o o k  U p C r e a                 | t i o n Te s t  P re p a r at i o n     |
|     | Kspacing         |                          | HPC Agent                            |                                         |
|     | Conv e r g ence  | C o n v e r ge n c e     |                                      |                                         |
|     | T e s t          | Jo b   S u b m is s io n | R e s o u r c e                      | Jo b                                    |
|     |                  |                          | A l lo c a t i o n Subm              | i ss ion                                |
DFT Agent
|     |     | R e p o r t       | D et e r m in e   R e           | p o r t   R e p o r t  J u d g e     |
| --- | --- | ----------------- | ------------------------------- | ------------------------------------ |
|     |     | Ge n e r at i o n | Opt im a l  k sp a c ing Ge n e | r at i o n t ri g g e r d :  P A S S |
DFT Agent
Production
|     | Script     | Production   |     |     |
| --- | ---------- | ------------ | --- | --- |
|     | Generation | Sc r i p t   |     |     |
Gen e r a t i on
|     | Production  | HPC Agent |     |     |
| --- | ----------- | --------- | --- | --- |
Job
|                            |                 | Resource            | Job                                         |     |
| -------------------------- | --------------- | ------------------- | ------------------------------------------- | --- |
|                            | Submission      | Allocation          | Submission                                  |     |
|                            | Calculate       |                     | DFT Agent                                   |     |
| Answer: Lattice            |                 |                     | L a t t ic e                                |     |
| c o n s t a n t  f or      | L a t t ic e    | R e s u l t         | C o n s t a n t   R e p o r t  J u d g e    |     |
| <S p e c i e s >   w it h  | C o n s t a n t | Ex tr a c t i o n C | a lc u l a t io n t ri g g e r d :  P A S S |     |
<Crystal-structure>
crystal structure is
xxx
Fig.3:End-to-endexecutionlogoftheSol27LCbenchmarkperformedbyDREAMS.
The supervisor organizes the study into report-bounded phases and assigns each
step to one of the worker agents; each convergence phase and the final lattice-
constantcalculationcloseswithastructuredreportauditedbythereportjudge,and
in this run every report passed on first submission. Note that across repeated runs,
although theoverall pattern isgenerally similar, theexact number ofsteps, interme-
diatedecisions,andrecoveryactionsmayvary.
11

intermediate reports, together with the final production report, satisfy the reporting
requirementsofthesafetyguard.
Fig. 4 shows the convergence procedure. The ecutwfc is first converged while
holding the k-point mesh sampling fixed at 0.1 Å−1. The k-point mesh sampling is
then converged using the selected energy cutoff of 120Ry. The DFT convergence
agent applies an energy-difference threshold of 1 meV/atom. More comprehensive
automatedconvergencemethodsareavailable[66],buttheygenerallyrequiremore
calculations. Sequential convergence of the plane-wave energy cutoff and k-point
sampling therefore remains common in DFT workflows. Because the LLM’s internal
reasoning process is not directly observable, these experiments cannot determine
whether its proposed ranges and rationales arise from physical reasoning, learned
patternmatching,orboth.DREAMSinsteadseparatesproposalfromverification:the
agent proposes a parameter range and threshold, Quantum ESPRESSO produces
system-specificenergies,andadeterministictoolselectstheleastexpensivetested
valuewithinthethresholdofthemost-convergedreference.Theselectedproduction
parameters are therefore supported by an empirical convergence study rather than
accepted from a one-shot LLM prediction, although this protocol does not by itself
establishthemechanismunderlyingtheagent’sproposals.
| (a)                                                      |                                            | (b)                                                      |                                            |          |
| -------------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------- | ------------------------------------------ | -------- |
|                                                        |                                            |                                                         |                                            |          |
|   P R W D  9 H P   H F Q H U H I I L G  \ J U H Q ( |  7 K U H V K R O G      P H 9  D W R P |   P R W D  9 H P   H F Q H U H I I L G  \ J U H Q ( |  7 K U H V K R O G      P H 9  D W R P |          |
|                                                        |                                            |                                                         |                                            |          |
|                                                        |                                            |                                                         |                                            |          |
|                                                        |                                            |                                                         |                                            |          |
|                                                         |                                            |                                                         |                                            |          |
|                                                        |                                     |                                                       |                                            |          |
|                                                          |                                            |                                                  |                                    |      |
|  . L Q H W L F  H Q H U J \  F X W R I I   5 \      |                                            |  . V S D F L Q J     $ Q J V W U R P                |                                            |          |
Fig. 4: Convergence test results for determining the optimal DFT parameters. (a)
The plane-wave energy cutoff (ecutwfc) is varied while fixing the k-point spacing
0.1Å−1.
at (b) The k-point mesh sampling is subsequently converged with a fixed
energy cutoff of 120Ry. In both cases, energy differences are computed against a
reference energy obtained from calculations using strict convergence settings (e.g.,
ecutwfc=120Ryandk-pointmeshsampling=0.1Å−1).TheDFTLLMagentselects
thefinalparametersbasedonanaccuracythresholdof1meV/atom.
Using the verified parameters, the DFT LLM agent prepares the production QE
inputfilesfortheequation-of-state(EOS)calculationseries.TheHPCagentassigns
resourcesandsubmitstheEOSjobs.TheDFTagentthenextractstheresults,deter-
minestheequilibriumlatticeconstant,andrecordsitinthefinalstructuredreport.The
12

report judge evaluates the complete provenance subtree for the reported value at
theparameterlevel(Fig.5).Afterallcontributingcallspassverification,theplanning
supervisorrecordstheresultandterminatestheworkflow.Thecompleteprovenance
graphisprovidedinSupplementaryInformationS-13.
Table2comparesexperimentalvalues,human-expertcalculations,andDREAMS
results.DREAMSachievesanaverageerrorbelow1%acrossallsystems,withonly
small deviations from the expert-calculated values. Under the safety guard, each
reported lattice constant is also accompanied by an end-to-end verified provenance
chain.
✓6sfprt… ✓wiaeh+ elrfr1 f eeaee i0pnmrs n⚠ m iaeeh d o nmtno 0_ r geecl ⚠o e _=red p p[s_= t aL=f1 i ri[i. m a_0l0 a mb.e0 l ec1=e _ t…,L- p e,0i3 a rL._ r =i1b a ✓ k_5c m sb,c e pc0_ t a….c e c,2o r iL,n ni…v g…+e4r]g ✓✓ en✓c…✓ ✓5elabc ✓la=== et3—— i mt. n0ei4 i⚠ ✓✓ nc9 t te 0_ ✓ == ⚠s Lb t ic r c uc ✓ t ✓ ure_data ✓6sfprt… ✓wiaeh+ elrfr1 f eeaee i0 m pnmrs n⚠ o iaeeh d r nmtno 0_ e geecl ⚠o _=red p p[s_= t aL=f1 i ri[i. m a_4l0 a mb0e0 l ec,=e _ t…5L- p e,0i3 a rL,_ r ✓ =i6b a e_0c m cb,c e uc…_ t t…+c e w,4o r fL]n ci v✓… e ✓ rg ✓ enc…✓ ✓0e✓le f m i0e n⚠n d t0_ =⚠p L s i eu ? dopotential
✓2lpfie… 0ipinn+ ✓sflps1 w tieue5 r olntm i0feaAb t⚠
m
Esmtl e
o
l=eoe 0_
r
e[=mC ⚠Q
e
mlLsa E eiiDl _ n__ic s tpbru c sbc=l r =…cLa i []_it p L
p-i
t i
rbo
_ ✓]
ocn
w
dc=
_ ✓
u.f
A
cxa
S
tyl
E
izs o
e
n✓✓ …✓
✓2is ✓ntpe g up e0tS n⚠_i e fz 0r ie ⚠a l= t e0 e _. _ n0 e a2 o m5 s e _ = t ✓L e i s _ t bcc_production…✓ ✓2is ✓ntpe g up e0tS n⚠_i e fz 0r ie ⚠a l= t e0 e _. _ n0 e a2 o m5 s e _ = t ✓L e i s _ t bcc_production…✓ ✓2is ✓ntpe g up e0tS n⚠_i e fz 0r ie ⚠a l= t e0 e _. _ n0 e a2 o m5 s e _ = t ✓L e i s _ t bcc_production…✓ ✓2is ✓ntpe g0up e⚠tS n _i e fz 0r ie ⚠a l= t e0 e _. _ n0 e a2 o m5 s e _ = t ✓L e i s _ t bcc_production…✓ ✓2is ✓ntpe g0up e⚠tS n _i e fz 0r ie ⚠a l= t e0 e _. _ n0 e a2 o m5 s e _ = t ✓L e i s _ t bcc_production…✓
✓1j✓o c
b
a0F l⚠i c
l
u e0l n⚠a
a
t
m
e
e
_
s
l
=
c
[Li_bc…,Li_bc…,Li…✓
Fig.5:Report-judgeverificationofthefinalBCC-Lilattice-constantreport.Eachnode
is a tool call in the provenance subtree of the reported claim, annotated with its
parameters and their individual verdicts from the deterministic checks and the per-
parameterjudge;edgesfollowtherecordedsourcesbetweencalls.Inthisrunevery
parameter of every contributing call passed, verifying the claim’s entire chain, from
initialstructuregenerationthroughconvergence-parameterselectiontotheequation-
of-statefit.
Table 2: Summary on correct structures generated by our agent, mean
average percentage error (MAPE) compared to results obtained from a
human DFT expert, and k-point & ecutwfc parameters chosen by our
agent, across different systems in Sol27LC benchmark. This showcases
DREAMS passed the testing problem and demonstrated its capabilities
toconducthighaccuracyDFTcalculationsonaHPC.Detailedresultsfor
eachindividualsystemareavailableinSupplementaryInformationS-3.
Structure Systems #ofcorrectstructures MAPE k-pointrange ecutwfc
BCC Li,Na,K,... 11/11 0.36% 8–16 40–70
FCC Rh,Ir,... 12/12 0.51% 8–18 40–70
DIA C,Si,Ge,... 4/4 1.00% 6–8 40–70
13

Investigating the CO/Pt(111) puzzle
The CO/Pt(111) problem requires multistep planning, iterative calculation, and error
recovery.Foraspecifiedmetalandsurfaceorientation(e.g.,Pt(111)),DREAMScon-
structs a periodic slab from the bulk crystal structure. The slab contains multiple
atomic layers and a vacuum region along the z direction to minimize interactions
between periodic images. The bottom layers are fixed, while the remaining atoms
are relaxed. The surface cell is selected to produce the target adsorbate coverage.
Candidate adsorption sites, including ontop, bridge, fcc, and hcp hollow sites, are
generatedonthesurface.ACOmoleculeisplacedateachsitewithaninitialorienta-
tionrelativetothesurfacenormal.Eachadsorbate–surfacestructureisthenrelaxed
withDFTuntiltheresidualforcessatisfyapredefinedthreshold.Thesamecomputa-
tionalsettings,includingecutwfcandk-pointsampling,areusedforallconfigurations
topermitconsistentenergycomparisons.Theadsorptionenergyiscomputedas
∆E =E −(E +E ), (1)
ads slab+ads slab ads
where E is the total energy of the relaxed adsorbate–slab system, E is
slab+ads slab
the energy of the clean slab, and E is the energy of the isolated CO molecule
ads
computed in a large vacuum cell. The most stable adsorption site and configura-
tionareidentifiedasthosewiththelowestadsorptionenergyamongtheconsidered
sites.Additionalcalculationsareperformedtoverifyconvergencewithrespecttoslab
thickness,thenumberoffixedslablayers,andthevacuumspacing.
The objective is given to DREAMS as: Please find the adsorption energy differ-
encebetweenthemostfavorableconfiguration(someadsorbateorientation)atFCC
site and most favorable configuration (some adsorbate orientation) at ontop site for
CO on the Pt(111) surface with p(2x2) adsorbate overlayer (1/4 coverage). Fig. 6
showsthecompletehistoryofwhatDREAMSdidforthischallenge.
Given the study objective, the planning supervisor generates an initial plan and
updates it as results become available by adding, removing, or repeating steps.
The initial plan is provided in Supplementary Information S-4. The execution log in
Fig. 6 therefore records the actions selected during execution rather than a prede-
fined workflow. The study includes initial setup, a first set of convergence tests for
ecutwfc,k-pointsampling,andslabthickness,asecondsetcomprisinganextended
ecutwfctest,repeatedk-pointandslab-thicknesstests,andafixed-layertest,afirst
round of production calculations whose final report is rejected, a third convergence
test round for the vacuum spacing, and the final production calculations. In contrast
totheSol27LCbenchmark,thisworkflowactivatesalltiersofthesafetyguard.
Thefirstecutwfcsweep(40–80Ry)doesnotconverge:theresultatthesecond-
highestcutoffdiffersfromthe80Ryreferencebymorethanthespecifiedthreshold.
The convergence-selection tool therefore declines to recommend a value and does
not register an output. The supervisor and worker then attempt to register 80 Ry
withoutadditionalcalculations.Theworkercallsthemathtoolwiththeexpressionx ,
0
whichthemathjudgerejects:
The expression is simply ‘x0‘, which returns the single input value
(80.0 Ry) unchanged. [...] an identity on a single input, manufacturing
14

a "computed" result that is really just a chosen number (80 Ry) wearing
the costume of a calculation.
Theworkerthenexamineswhethertheguarddetectsmathematicaloronlysyntactic
identity:
The key question is: does the tool check for MATHEMATICAL identity or
only SYNTACTIC identity?
Atthesupervisor’ssuggestion,theworkernexttriesx ×1.0.Thejudgeagainrejects
0
theoperation:
This is a textbook case of VALUE LAUNDERING: it matches the explicit
FAIL examples (x0 * 1.0, restating an input unchanged). No genuinely
new information is produced.
The extraction tool also rejects an attempt to retrieve the value from an output
in which it is not present. The worker then reports the available options to the
supervisor:
The framework’s provenance system is working as designed: it prevents
creating "fake" output artifacts from input parameters. To generate the
structured report certifying optimal ecutwfc, we MUST either:
1. Extend the ecutwfc sweep to 90-100 Ry to obtain a registered
artifact from find_optimal_parameter
2. Skip the intermediate report and proceed directly to kspacing
convergence test, using byg7hl8g.ecutwfc (input parameter reference)
in downstream production calculations
I recommend Option 2: Skip the intermediate report and proceed with
kspacing convergence test. The ecutwfc value (80 Ry) is well-documented
and scientifically justified in the CANVAS notes. The structured report
can be generated at the END of the study when we have the final
adsorption energy difference, and we can cite byg7hl8g.ecutwfc as the
source of the ecutwfc parameter choice.
The supervisor selects the second option. The intermediate report is deferred, and
80Ryisretainedasaprovisionalvalueforthesubsequentsub-study.Thisbehavior
allows exploratory calculations to proceed while preventing provisional values from
supportingverifiedscientificclaims.
The subsequent k-point test completes without issue, and its report passes veri-
fication. The slab-thickness test then requires reuse of the provisional 80 Ry cutoff.
Duringsetup,thecall-timejudgerejectsascriptlabeledasproductionworkbecause
itassignsecutwfc=80throughtheplanneddottedreference:
The parameter ecutwfc = 80.0 is sourced from a dotted reference
‘byg7hl8g.ecutwfc‘, i.e. it consumes the INPUT PARAMETER value of an
earlier tool call. [...] Rule requirement for production work consuming
a dotted input ref: the source input must have been CHARACTERIZED with
a bare ref -- production cannot legitimately consume an uncharacterized
value laundered through a dotted ref.
A dotted reference identifies an input parameter from an earlier call rather than a
computed output. The proposed citation path is therefore rejected when used in
production-labeledwork.Theagentrelabelsthecalculationsassub-studywork,after
which the call-time judge approves them. Following execution by the HPC agent,
severalcalculationsfailtoconverge.TheconvergenceLLMagentdiagnosesthefail-
ures and recommends parameter changes. Representative recommendations are
15

shown in Table 3, with additional examples provided in Supplementary Information
S-5. The calculations are then repeated. During this process, the worker identifies
that the clean-slab and isolated-CO calculations are missing and generates them.
After all calculations complete and the report is submitted, the report judge issues
thefollowingwarning:
The agent is asserting the value has been characterized when the cited
source shows it is an uncharacterized template input to a sweep. [...]
plausible and value-appropriate for the sub-study, but under-justified/
misrepresented provenance. [...] Run the appropriate sub-study
(convergence test, sensitivity sweep) that PRODUCES an output artifact
for this value, then re-create the current artifact with a bare ref
pointing at that output.
Thejudgedistinguishesbetweenthenumericalvalueanditsprovenance.Acutoffof
80 Ry is acceptable as a provisional sub-study setting, but it cannot be reported as
a characterized result. The warning also specifies the required correction: perform
a convergence or sensitivity study that produces a registered output and cite that
outputdirectly.
The second round implements the judge’s recommendation. An extended
ecutwfc test (85–100 Ry) identifies a converged cutoff of 95 Ry, replacing the pro-
visional value of 80 Ry. The corresponding report passes verification. The k-point
and slab-thickness tests are then repeated and pass. The fixed-layer test produces
awarning,whichthesupervisorreviewsandclassifiesasafalsepositivebeforepro-
ceeding to production, as discussed below. During production setup, the call-time
judge rejects the workflow because the vacuum spacing lacks a source reference.
Theagentsearchestheartifactregistry,findsnocharacterizedoutputforthevacuum,
andre-createsthecallwithadottedreferencetotheinputvalueheldthroughoutthe
structuraltests,arguingitsconsistencyintherecordedrationale.Thecall-timejudge
acceptstheargument:
So the earlier call was a legitimate convergence sub-study where vacuum
was deliberately held at its optimal value (12.0 A), consistent
throughout all prior structure generations. [...] This is a coherent
origin: the production run inherits vacuum=12.0 from a study where it
was consistently used.
The production calculations run to completion, the adsorption energies are com-
puted,andthefinalreportissubmitted.Thereportjudge,walkingthefullprovenance
chain,reachesthesamedottedreferenceontheproductionstructuresandrejectsit:
Given genuine ambiguity -- vacuum=12.0 is a physically reasonable value
and consistently used -- but the rule is quite explicit about rejecting
dotted refs to uncharacterized inputs in production, I lean to fail,
though the physical reasonableness pulls toward warning.
Therejection,onceagain,specifiestherequiredcorrection,andthesupervisorcom-
plies:avacuumconvergencetest(10–18Å)isinserted,andeverytestedvaluefalls
within0.002eVofthe18Åreference:
The previously used vacuum=12.0 Angstrom (uncharacterized) is also
within threshold (dE = 0.00130 eV), confirming that the original choice
was scientifically reasonable. However, the characterized optimal value
is vacuum=10.0 Angstrom.
16

Table3:RepresentativesuggestionsmadebytheconvergenceLLMagentbasedon
DFTinputandoutputfiles.Forfailedorunconvergedsimulations,theagentproposes
parameteradjustmentssimilartothoseofanexperiencedDFTuser:slightlyincreas-
ing the smearing width (degauss), reducing the mixing factor (mixing_beta) and
switching mixing_mode to local-TF for highly inhomogeneous systems, or increas-
ingelectron_maxstep,eachwithaconcisejustification,allconsistentwithcommon
expert practice and the Quantum ESPRESSO manual. More example suggestions
canbefoundinSupplementaryInformationS-5.
Parameters Suggestions Reason
ecutwfc increaseto80.0 highercutoffneededforultrasoftpseudopo-
tentialswithtransitionmetals
degauss increaseto0.03 helpswithmetallicsystems
mixing_beta addwithvalue0.3 Thecurrentvalueof0.7istoohighforthis
complex system with CO adsorption, lead-
ingtochargesloshing
mixing_mode local-TF Switching from plain mixing to a more
sophisticatedschemelikelocal-TFcanhelp
withdifficultconvergencecases
electron_maxstep 300 The calculation stopped at 200 iterations
but was still making progress, so allowing
moreiterationsmighthelpitconverge
The test simultaneously validates the held 12 Å and selects 10 Å as the cheapest
convergedsetting.Theproductioncalculationsareregeneratedatthecharacterized
vacuum,theHPCagentsubmitsandmonitorsthem,andtheDFTagentextractsthe
finalenergies,calculatestheadsorptionenergiesforallconfigurations,identifiesthe
lowest-energy geometry at each site, and computes the energy difference between
theFCChollowandontopsitesusingtheguardedmathtool.Thefinalreportpasses
verificationinfull,andtheplanningsupervisorterminatestheworkflow.
The completed workflow generates a provenance graph containing hundreds of
registered tool calls, making manual review impractical. The report judge therefore
evaluates the graph recursively and at full depth, independent of its size. Table 4
compares the results from DREAMS, a human expert, and Peter et al. [68]. For
bothfunctionals,theadsorption-energydifferencepredictedbyDREAMSagreeswith
the human-expert result within 2 meV and is consistent with the literature values,
reproducingtheFCC–ontopsitepreference.
Comparability
Anenergydifferenceisvalidonlywhenallcontributingcalculationsuseaconsistent
parameterset.Thisrequirementisspecifiedintheagentpromptsandenforcedbythe
guardrules.Duringplanning,theDFTagentrecordsthisrequirementinitsanalysis
note:
Critical: ALL calculations (slab, CO, all configurations) must use
IDENTICAL DFT parameters:
17

Supervisor
Objective:find the
most preferable
configuration of CO
on Pt(111) surface
|     | Initial  | Discussion result: Overall strategies, caveats, and plan generation |     |     |
| --- | -------- | ------------------------------------------------------------------- | --- | --- |
|     | Setup    | DFT Agent: Initial setup                                            |     |     |
Ecutefc
|      |     | Convergence  | DFT & HPC Agent: 40-80 Ry Ecutwfcconvergence test setup & submission  |     |
| ---- | --- | ------------ | --------------------------------------------------------------------- | --- |
| User |     |              | Discussion result: 80 Ry is good enough, now register 80 and report   |     |
Test
DFT Agent: Called Math tool with expression with only “80” as the input
Math Judge triggerd: Fabrication detected
DFT Agent: Asked by supervisor to try 80 * 1.0 or 80 + 0.0
|     | 1st Round    |     | Math Judge triggerd: Fabrication detected           |     |
| --- | ------------ | --- | --------------------------------------------------- | --- |
|     | Convergence  |     | Discussion result: Skip report and use 80 Ry anyway |     |
Test
DFT & HPC Agent: 0.1-0.2 Å⁻¹ kspacingconvergence test setup & submission
kspacing
|     |     | Convergence  | DFT Agent: determined optimal kspacing with tool and generated report |     |
| --- | --- | ------------ | --------------------------------------------------------------------- | --- |
Test
Report Judge  PASS
DFT Agent: 4-8 slab layers convergence test setup On siteJudge  FAIL
|     |     | Slab  | DFT & HPC Agent: 4-8 slab layers convergence test re-setup & submission  |     |
| --- | --- | ----- | ------------------------------------------------------------------------ | --- |
Thickness
Discussion result: update calculation settings due to calculation convergence issue
Convergence
|     |     | Test | DFT & HPC Agent: slab layers convergence test rerun & submission  |     |
| --- | --- | ---- | ----------------------------------------------------------------- | --- |
DFT Agent: noticed slab and CO calculations were forgotten
DFT & HPC Agent: generated forgotten calculations& job submission
DFT Agent: determined optimal slab layer with tool and generated report
Report Judge  WARN
DFT & HPC Agent: 80-100 Ry Ecutwfcconvergence test setup & submission
Extended
|     |     | ecutefc  | DFT Agent: determined optimal Ecutwfcwith tool and generated report |     |
| --- | --- | -------- | ------------------------------------------------------------------- | --- |
Convergence
|     |     | Test         | Report Judge  PASS                                                        |     |
| --- | --- | ------------ | ------------------------------------------------------------------------- | --- |
|     |     | kspacing     | DFT & HPC Agent: 0.1-0.2 Å⁻¹ kspacingconvergence test setup & submission  |     |
|     |     | Convergence  | DFT Agent: determined optimal kspacing with tool and generated report     |     |
Test redo
Report Judge  PASS
2nd Round
Convergence
|     | Test | Slab  | DFT & HPC Agent:  | 4-8 slab layers convergence test setup & submission  |
| --- | ---- | ----- | ----------------- | ---------------------------------------------------- |
Thickness
|     |     | Convergence  | DFT Agent: determined optimal slab layer with tool and generated report |     |
| --- | --- | ------------ | ----------------------------------------------------------------------- | --- |
|     |     | Test         | Report Judge  PASS                                                      |     |
DFT & HPC Agent: 2-4 fixed layers convergence test setup & submission
|     |     | N fixed layers   | Discussion result: update calculation settings due to calculation convergence issue |     |
| --- | --- | ---------------- | ----------------------------------------------------------------------------------- | --- |
|     |     | Convergence      | DFT & HPC Agent: slab layers convergence test rerun & submission                    |     |
Test
DFT Agent: determined optimal slab layer with tool and generated report
Report Judge  WARN
|     |     | DFT Agent: production run setup | On siteJudge  FAIL |     |
| --- | --- | ------------------------------- | ------------------ | --- |
DFT & HPC Agent: production run re-setup & submission
Production
|     | Run | DFT Agent: determined adsorption E difference and generated report |     |     |
| --- | --- | ------------------------------------------------------------------ | --- | --- |
Report Judge  FAIL
|                                 | 3rd Round         | N vacuum                    | DFT & HPC Agent:                                                              | 10-18 Å of vacuum convergence test setup & submission  |
| ------------------------------- | ----------------- | --------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------ |
|                                 | Convergence       | Convergence                 | DFT Agent: determined optimal vacuum thickness with tool and generated report |                                                        |
|                                 | Test              | Test                        | Report Judge  PASS                                                            |                                                        |
|                                 |                   | D F T   &   H P C   A       | g e n t :  f i n a l  p r o d u ct io n   r u n  s e                          | t u p   &   s u b m is s i o n                         |
| A n sw e r :   A t   lo w       | F i n a l         |                             |                                                                               |                                                        |
| c ov e ra g e   ( <   1 / 3) ,  | pro d u c t i on  | DFT  A g e n t :  d e t e r | m i n e d   a d s o r p t io n  E  d i f f e re n c                           | e   a n d   g e n er a t e d   report                  |
Run
| the preferred  |     | Report Judge  PASS |     |     |
| -------------- | --- | ------------------ | --- | --- |
configuration is
FCC
Fig. 6: End-to-end execution log of the CO/Pt(111) study performed by DREAMS.
The diagram is a record of what the agents chose to do, not a predefined pipeline:
the supervisor inserts, deletes, and repeats plan steps freely as the study unfolds,
andeveryactionisloggedasshown.Inthisrun,thestudyunfoldedoverthreerounds
of convergence testing. In the first round, the convergence-selection tool refused
to recommend an unconverged ecutwfc, the math judge twice blocked attempts to
register the chosen value through identity expressions, a call-time rejection blocked
an uncharacterized parameter pin durin1g8slab-test setup, and the slab-thickness
report closed with a warning; the warning’s remediation led to a second round, in
whichanextendedecutwfctestandregeneratedk-pointandslab-thicknesstestsall
passed.Theregenerationspreservetheconsistencyofthecomparisonset:oncethe
cutoff changed, every calculation entering the energy difference was re-run under
the new, shared parameter set. At production setup, a call-time rejection blocked
the unsourced vacuum value; the agent re-created the call with the value it had
held throughout the tests, and the first production round completed, but the report
judge failed its final report because the vacuum had never been characterized. The
resulting third round characterized the vacuum by convergence test, the produc-
tion calculations were regenerated, and the final adsorption-energy report passed.
Acrossrepeatedrunstheoverallpatternisgenerallysimilar,buttheexactnumberof
steps,intermediatedecisions,andrecoveryactionsvary.

- Same ecutwfc, ecutrho
- Same kspacing (k-points scaled to each cell)
- Same smearing, degauss
- Same conv_thr
- Same pseudopotentials
Any difference in parameters invalidates the energy comparison.
Thecross-parameterjudgeevaluatescomparabilityateachselectioncall:
Comparability: rationale states all files use identical settings
(kspacing=0.15, PBE, methfessel-paxton, conv_thr=1e-6) except ecutwfc.
No contradiction across rationales. All same 24-atom CO/Pt(111) system.
When calculations in the slab-thickness test fail to converge, this requirement
constrainsthepermittedmodifications.Theconvergenceanalysisstates:
I do NOT recommend changing kspacing because: (a) it was converged on a
representative system, (b) changing it would invalidate the comparison
set consistency, (c) the primary issue is mixing/SCF stability, not
k-points. [...] nspin: 2 (spin polarization): This is a major change
that would require re-running ALL calculations including the converged
z4 and z5, invalidating comparison set consistency. [...] This approach
maintains comparison set consistency by using identical DFT parameters
(ecutwfc=80 Ry, kspacing=0.15 A^-1) across all calculations, only
adjusting the SCF convergence control parameters (mixing,
diagonalization) which do not affect the final converged energy (they
only affect the path to convergence).
After the report judge identifies that the provisional 80 Ry cutoff has not been char-
acterized, the remediation instructions specify the consequences of replacing an
upstreamartifact:
IMPORTANT: regenerating an artifact invalidates every artifact
downstream that referenced it. After fixing this artifact, you MUST
re-run every dependent calculation (production runs, ensemble
calculations, downstream extractions) using the new artifact’s
result_id.
Theextendedecutwfctestthenusesthepreviouslydeterminedk-pointspacing.The
judgeevaluateswhetherthatresultremainsapplicableunderthehighercutoff:
The kspacing convergence (a80zq4b6) was performed at ecutwfc=80 Ry [...]
The current run is at ecutwfc=100 Ry. Is 80 Ry -> 100 Ry a "much
higher" ecutwfc mismatch? This is the key judgment. K-point sampling
convergence is essentially independent of the plane-wave cutoff --
kspacing controls reciprocal-space Brillouin zone sampling, while
ecutwfc controls the plane-wave basis completeness. These are largely
orthogonal convergence axes.
Whenthek-pointtestisrepeatedattherevisedcutoff,thejudgeagainevaluatesthe
recordedcontextandjustification:
Rationale coherence: The rationale identifies the study (regenerating
the kspacing convergence test with ecutwfc=95 Ry), explains WHY
(consistency after discovering optimal ecutwfc=95 > previously used
80 Ry), identifies the role of these values (same test values as
original kspacing test, spanning tight to coarse).
During the fixed-layer test, additional calculations fail to converge. After consulting
theconvergenceagent,theDFTagentreports:
I rejected parameter changes that would break comparison set
consistency (degauss, kspacing, smearing type, dipole correction).
19

The revised template is applied only to the CO+slab calculations. The report judge
identifiestheresultingdifferenceinself-consistent-fieldsettings,producingthefixed-
layerwarningdescribedabove:
If the CO+slab batch uses hzlc6pf4 (improved SCF control) but the
clean-slab batch uses 5hfafzg8 (standard SCF control), the E_ads
derived quantity would combine calculations with mismatched SCF
convergence handling.
Thesupervisorreviewstheassociatedcanvasrecordsandresponds:
The verifier raised a WARNING on the n_fixed_layers report (step 65)
regarding comparison-set consistency: the clean slab batch for n2/n3
used the original template (5hfafzg8) with standard SCF parameters,
while the CO+slab batch used the updated template (hzlc6pf4) with
improved SCF convergence control. However, after reviewing the CANVAS
notes, I find this is scientifically justified: (1) The clean slab
calculations already converged successfully with standard SCF
parameters in step 56, (2) The improved SCF parameters were
specifically needed for CO+slab systems due to charge sloshing between
CO and Pt, not for clean slabs, (3) All physically meaningful DFT
parameters (ecutwfc=95 Ry, kspacing=0.15, conv_thr, smearing,
pseudopotentials) are IDENTICAL across all calculations, (4) SCF
convergence control parameters affect whether SCF converges, not the
converged energy value itself. The E_ads results show excellent
convergence (all within 0.002 eV), confirming the approach is valid.
The verifier’s warning is noted but does not require regeneration.
This exchange establishes the applicable consistency criterion. Parameters that
affect the physical result must remain identical across calculations, whereas self-
consistent-fieldcontrolparametersmaydifferwhentheyaffectconvergencebehavior
but not the converged energy. The judge records each deviation, and the supervi-
sor may override a warning when supported by evidence from the canvas. Both the
warninganditsjustificationremainintheexecutionrecord.
Thesamedisciplinecarriesintotheproductionrounds.Regeneratingtheproduc-
tioninputs,theworkerrecords:
**Maintained comparison set consistency** by using IDENTICAL DFT
parameters across all 8 calculations to ensure error cancellation in
formation energy differences.
This study activates every verification tier on a complex workflow. Each tier
detectsadistinctclassoffailure:theconvergence-selectiontoolpreventsanuncon-
verged cutoff from being registered as a recommendation; the math and extraction
checks prevent unsupported values from acquiring valid provenance; the call-time
judge rejects uncharacterized or unsourced parameters before calculations are
submitted;theconvergenceLLMagentdiagnosesexecutionfailuresusinginput,out-
put, and error files; and the report judge identifies provenance errors that are not
detectable at individual tool calls and re-judges, with the whole study in view, bor-
derline calls that argued their way past a gate. The framework permits exploratory
calculations and deferred reporting, as shown by the provisional 80 Ry cutoff and
the vacuum spacing held through the structural tests, but prevents uncharacterized
valuesfromsupportingverifiedclaims:thefirstproductionroundranontheheldvac-
uum, and its report could not pass until a convergence test characterized the value.
It also enforces consistency across calculations used in the adsorption-energy dif-
ference. This requirement is specified in the agent prompts and evaluated by the
20

Table 4: The ∆BE calculated by DREAMS agrees well with our human expert and
literature for both PBE and LDA functionals. Calculations are performed on a 2×2
supercellat1/4monolayer(θ =1/4ML)coverage.∆BE=E −E .
ads_ontop ads_fcc
∆BE(eV)
Supercell θ(ML) XC
AgentTeam HumanExpert Literature
2×2 1/4 PBE 0.1078 0.108 0.10-0.24[68,71,72]
2×2 1/4 LDA 0.318 0.320 0.32-0.45[68,76]
cross-parameterjudgeateachcall.Itconstrainsparametermodificationsduringcon-
vergence recovery and requires dependent tests to be repeated when the cutoff
changes.TheonlyaccepteddifferenceconcernsSCFcontrolparametersthataffect
convergence behavior but not the converged energy; the warning and supporting
justification remain in the execution record. These checks establish that the final
reportedvalueissupportedbyverifiedcalculations,parameters,andprovenance.
Quantifying the uncertainty of exchange-correlation functionals
Upon demonstrating DREAMS’ capability of reproducing human expert level pre-
cision DFT simulation results on the CO/Pt(111) puzzle challenge, the scope is
extended.Anaturalthirdchallengefromtheseresultsisthesensitivityoftheadsorp-
tion site preference to the specific choice of exchange-correlation functional at the
same level of theory (GGA). To quantify this uncertainty, DREAMS is asked to per-
form Bayesian ensemble sampling with van der Waals correction (BEEF-vdW) [67]
andthedistributionofpossible∆BEscanbefoundinFig.7(c).Forboththehuman
expert’s result andDREAMS’ result, 0 eV, is more than ten standard deviations out-
side of the distribution of ∆BE, indicating that, even when considering uncertainty,
the FCC site remains more energetically favorable than the ontop site at the GGA
level. These results are consistent with our earlier findings obtained using the PBE
and LDA functionals, as well as with previous literature [68]. We therefore conclude
that the CO adsorption behavior on the Pt(111) surface is unlikely to fully match
experimentalobservationsunderthecurrentGGA-levelapproximations.
As for the discrepancies, some possible factors are identified. First, the conver-
gence threshold in SCF calculations used by DREAMS is higher (1×10−6 Ry) than
that used by the human expert (1×10−7 Ry), despite the lower threshold being rec-
ommendedinQuantumESPRESSOforstructurerelaxation.Second,althoughboth
DREAMSandthehumanexpertemploythesamesmearingmethod,DREAMSsets
a higher smearing width of 0.02 Ry compared to the human expert’s setting of 0.01
Ry.Thislargersmearingwidthintroducesfurtherdeviationsinthecomputedadsorp-
tion energies. Together, these differences could explain the minor shift observed in
DREAMS’resultsrelativetothehumanexpertcalculations.
With the adsorbed configurations explored by DREAMS, we can provide some
insight into the CO/Pt(111) puzzle. After the autonomous DREAMS workflow was
21

((aa)) (b) (c)
(d) (e) (f)
(g) (h) (i)
(b) (c)
Fig. 7: (a) Representative possible structures that DREAMS can generate, illustrat-
ing variations in adsorption site, adsorbate orientation, and slab thickness. Panel
(a)illustratesstructure-generationcapabilityonly;convergenceisestablishedbythe
dedicated tests described above. (b) Configurations used for the BEEF ensemble
analysis:FCCadsorption,on-topadsorption,cleanslab,andisolatedCOmolecule.
(c)Distributionof∆BE,E −E ,valuesfromBEEFensembleanalysis:
ads_ontop ads_fcc
human-expert calculations yield a mean of −0.13eV (σ = 0.01eV), while DREAMS
produces a mean of −0.12eV (σ = 0.01eV). Both methods consistently predict that
theFCC-siteadsorptionenergyislowerthantheon-top-siteadsorptionenergy,indi-
catingthatFCCadsorptionismorefavorableattheGGAlevel.
completed,weperformedBaderchargeandC–Obond-lengthanalysesonitsgener-
ated structures and electronic densities to further validate the predicted adsorption-
sitetrendandinvestigateitselectronicorigin.TheresultsareshowninTable5.Recall
that DREAMS predicts that the FCC site is more energetically favorable than ontop
sites under all three functionals used in this work. We observe that for all adsorbed
CO,theC-Obondlength,i.e.d ,increasescomparedtothepristineCOmolecule.
C−O
The reason for the CO bond length increase lies in the electron transfer from the
Pt surface to the CO molecule. Upon adsorption, free electrons in Pt metal partially
transfer to the C-O bond antibonding π∗ orbitals, effectively decreasing the bond
orderoftheC-Obond,leadingtoabondlengthincrease.Inallthreefunctionals,the
FCCsiteprobes0.15-0.18e−moreelectrontransferthantheontopsite(chargeden-
sityplotsareavailableinSupplementaryInformationS-6),andconsequently,theC-O
bond length is always longer on the FCC site. The larger degree of electron trans-
fer indicates enhanced CO-Pt interaction via electron sharing, which explains why
CO adsorption is more favored on the FCC site [72]. We would like to point out that
22

Table 5: Bond length and charge transfer analysis at different CO adsorption sites
onthePt(111)surface.TheCOmoleculeinvacuumisalsolistedforreference.
Ontop FCC COmolecule
Functional
d C−O(Å) Chargetransferred d C−O(Å) Chargetransferred
d C−O(Å)
LDA 1.15 0.02e− 1.18 0.18e− 1.13
PBE 1.16 0.03e− 1.19 0.21e− 1.14
BEEF-vdW 1.15 0.08e− 1.18 0.23e− 1.13
the electron transfer from transition metal surface to CO has actually been studied
as early as 1964 [77]. The mechanism observed in this work, namely the elec-
tron donation from Pt to CO, has been proposed as the back donation mechanism
[72, 77]. Such a mechanism has been argued to favor the FCC site over the ontop
site[72,77],whichagreeswithDREAMS’finding.Thisagreementdemonstratesthat
thestructuresandelectronicdensitiesgeneratedthroughtheDREAMSworkflowcan
support further mechanistic investigation without fine-tuning the underlying LLM or
introducingchallenge-specificLLMagents.
Quantitative comparison with other LLM agentic frameworks
We empirically benchmark our framework against two representative agentic sys-
tems for scientific workflows, MDCrow [22] and ChemGraph [23], on the Sol27LC
lattice constant challenge and the CO/Pt(111) adsorption challenge, and we addi-
tionally benchmark it against itself. DREAMS denotes the framework without the
safety guard, retaining its canvas and orchestration, while DREAMS_safe denotes
the full system with every guard layer active. The systems use different architec-
tures: MDCrow is a LangChain-based, single-agent ReAct framework; ChemGraph
usesLangGraph-basedmulti-agenttaskdecomposition;DREAMSuseshierarchical
task assignment, specialized worker agents, a persistent canvas, and supervisor-
directedplanupdates;andDREAMS_safeaddsthesafetyguardtoDREAMS.These
design elements are architectural choices rather than binary indicators of system
quality.BecausethebaselinesystemsdifferfromDREAMSinseveralrespectssimul-
taneously, comparisons with MDCrow and ChemGraph evaluate overall end-to-end
behavior rather than isolate the causal contribution of any individual architectural
choice. By contrast, the comparison between DREAMS and DREAMS_safe holds
thecanvasandorchestrationfixedanddirectlyevaluatestheaddedeffectandcostof
the safety guard. Both MDCrow and ChemGraph were provided with the same DFT
toolset as DREAMS, excluding the canvas tools, and their prompts were adjusted
only to match the DFT context while maintaining their original design philosophy.
For example, an original instruction such as “You are a molecular dynamics expert”
was modified to “You are a DFT expert”. Similarly, if step-by-step MD instructions
aregiven,theyarereplacedwithequivalentDFTprocedures.Themodifiedprompts
are provided in Supplementary Information S-10. All four systems share the same
backend LLM, Claude Sonnet 4.5 [73]; the judges of DREAMS_safe are backed by
23

ClaudeOpus4.8[74].Atleast3runswereconductedineachcase,andthenumber
showninTable6isanaverageacrossthoseruns.
Table 6: Benchmarking results of different agentic systems on Sol27LC and
CO/Pt(111) challenges. DREAMS denotes our framework without the safety guard
(canvasandorchestrationonly);DREAMS_safedenotesthefullsystemwithallguard
layers active. To assess accuracy, robustness, and cost, we employ five quantitative
metrics: (1) Percentage of essential steps executed (reflecting the framework’s abil-
ity to attempt the complete workflow). (2) Percentage of essential steps succeeded
(reflecting correct execution and recovery from errors). (3) Mean Absolute Percent-
age Error (MAPE) of the final numerical results. (4) Standard deviation of results
acrossmultipleindependentruns.(5)TotalLLMtokenusage,calculatedasthesum
ofinputandoutputtokensandaveragedacrosstheindependentruns.
|            |           | Steps    | Steps      |     | Token  |
| ---------- | --------- | -------- | ---------- | --- | ------ |
| Challenges | Agent     |          | MAPE       | STD |        |
|            |           | Executed | Succeeded  |     | Usage  |
|            | MDCrow    | 100%     | 100% 0.55% | 0Å  | 500346 |
|            | ChemGraph | 100%     | 100% 0.55% | 0Å  | 269725 |
Sol27LC,BCCLithium
|     | DREAMS      | 100% | 100% 0.55% | 0Å      | 469647  |
| --- | ----------- | ---- | ---------- | ------- | ------- |
|     | DREAMS_safe | 100% | 100% 0.55% | 0Å      | 4239831 |
|     | MDCrow      | 39%  | 23% –      | –       | –       |
|     | ChemGraph   | 73%  | 46% 389%   | 0.390eV | 3040097 |
CO/Pt(111),PBE
|     | DREAMS      | 100% | 81% 0.2%  | 0.001eV | 1814315  |
| --- | ----------- | ---- | --------- | ------- | -------- |
|     | DREAMS_safe | 100% | 100% 0.1% | 0.001eV | 23920487 |
For the Sol27LC benchmark, all four systems complete the required steps and
produce comparable lattice constants, indicating that each can execute structured,
short-horizonworkflows.Theirmeanerrorsremainbelow1%,consistentwithexpert
DFTcalculations.PerformancedifferssubstantiallyforthemorecomplexCO/Pt(111)
adsorption problem. MDCrow fails to complete the workflow in all trials because of
context loss and incorrect tool use. ChemGraph improves task decomposition but
lacks effective cross-agent communication, leading to repeated calculations, over-
written intermediate files, and invalid results. DREAMS uses the shared canvas
and hierarchical communication structure (Fig. 9) to execute all 26 essential steps
and produces a result within 0.2% of the human-expert value, although only 81%
of those essential steps succeed. The incorrectly executed steps are the structural
convergence tests on slab thickness and vacuum spacing: the underlying calcula-
tions do not converge, yet the agent selects a setting it considers reasonable and
proceeds. The final agreement results from partial cancellation of systematic errors
amongtheslab,adsorbate,andcombined-systemcalculations.Thenumericalresult
thereforedoesnotindicatethattheworkflowwasexecutedcorrectly.DREAMS_safe
addresses this limitation by requiring each essential step to pass the corresponding
verificationchecksbeforetheworkflowproceeds.All26essentialstepssucceed,and
24

Table7:Token-costbreakdownofDREAMS_safeandDREAMS(nosafety
| guard) on   | the two         | challenges, | by          | call category, |        | for one     | representative |       | run       |
| ----------- | --------------- | ----------- | ----------- | -------------- | ------ | ----------- | -------------- | ----- | --------- |
| of each     | system. “Agent, |             | canvas tool | call”          | covers | canvas      | inspection,    |       | read,     |
| and write   | operations;     | “Judge,     | outside     | report         | span”  | is          | the call-time  |       | (in-tool) |
| judge cost; | “Judge,         | inside      | report      | span”          | is the | report-time | judge          | cost. | n is      |
thenumberofLLMcallsineachcategory.
|                          |     |     | DREAMS_safe   |         |         |     | DREAMS     |       |        |
| ------------------------ | --- | --- | ------------- | ------- | ------- | --- | ---------- | ----- | ------ |
| Category                 |     |     | n             | Input   | Output  |     | n          | Input | Output |
| Agent,non-canvastoolcall |     |     | 41            | 719,964 | 23,845  |     | 27 151,538 |       | 7,126  |
| Agent,canvastoolcall     |     |     | 127 2,136,289 |         | 11,659  |     | 29 156,406 |       | 2,622  |
| Judge,outsidereportspan  |     |     | 69            | 397,734 | 41,019  |     | 0          | 0     | 0      |
| Judge,insidereportspan   |     |     | 139           | 823,407 | 85,914  |     | 0          | 0     | 0      |
| Agent,non-canvastoolcall |     |     | 190 5,780,519 |         | 173,954 |     | 88 852,939 |       | 23,807 |
| Agent,canvastoolcall     |     |     | 343 8,814,788 |         | 54,543  | 119 | 850,476    |       | 10,730 |
| Judge,outsidereportspan  |     |     | 627 3,573,264 |         | 383,770 |     | 0          | 0     | 0      |
| Judge,insidereportspan   |     |     | 817 4,647,387 |         | 492,262 |     | 0          | 0     | 0      |
thefinalresultachieves0.1%MAPEwiththesamespreadandafullyverifiedprove-
nance chain. A more detailed explanation of the MDCrow and ChemGraph failure
casesisprovidedinSupplementaryInformationS-9.
TokenusageissummarizedinTable6andseparatedbycallcategoryinTable7.
“Judge,outsidereportspan”denotescall-timejudgeusage,whereas“Judge,inside
reportspan”denotesreport-timejudgeusage.ForCO/Pt(111),unguardedDREAMS
uses approximately 40% fewer total tokens than ChemGraph and obtains a final
value close to the expert reference. Although the numerical answer agrees with the
reference,only81%oftheessentialstepssucceed,andtheagreementarisespartly
fromerrorcancellation.Thecomparisonthereforeillustratesatradeoffbetweencost
and evidentiary rigor. The unguarded mode may be useful for rapid exploration,
where a likely answer guides subsequent work and will be independently checked,
whereasfullverificationisappropriatewhentheresultmustsupportafinalscientific
claimwithanauditableprovenancechain.Neitherconfigurationisuniversallyprefer-
able; the appropriate choice depends on the confidence required for the intended
use. Approximately half of the unguarded agent’s input tokens are associated with
canvas operations that maintain information across the long-horizon workflow. Full
verification substantially increases cost. DREAMS_safe uses approximately 13x
more input tokens than DREAMS for both benchmarks and 17x to 32x more out-
put tokens. Judge calls account for approximately one third of the input tokens and
four fifths of the output tokens. The similar input-cost ratios across the two bench-
marks suggest that verification cost increases primarily with workflow activity rather
thantaskcomplexity.Thecostcanbereducedbymodifyingtheverificationconfigu-
ration. Judge outputs are dominated by explanations for passing verdicts; reporting
explanations only for failed checks would reduce output usage but provide less
25

information for auditing successful checks. Call-time and report-time judge layers
can also be disabled independently. The present study evaluates the maximum-
verification configuration, in which all layers are active and all values are checked.
Otherconfigurationscanbalanceverificationcoverageagainsttokencost.
The tuned judge rules transfer across judge models
Weevaluatethereliabilityoftheverificationjudgesusingtheproceduredescribedin
the Methods. The judge rules are adversarially refined using a standalone scenario
harness and evaluated on 145 scenarios. Each scenario represents a realistic tool
callderivedfromartifactsgeneratedinactualrunsandiseithervalidorcontainsone
injecteddefect.Eachverdictisdeterminedbymajorityvoteacrossthreejudgecalls,
and a warning is counted as detection of a should-fail scenario. Fig. 8 presents the
resultingconfusionmatricesforfiveAnthropicmodels:ClaudeFable5,ClaudeOpus
4.8,ClaudeSonnet5,ClaudeSonnet4.6,andClaudeSonnet4.5.
Threefindingsemerge.First,allfivemodelsdetectmostdefectivescenariosand
accept most valid scenarios, with total errors ranging from 4 to 17 out of 145. This
consistency indicates that the rule set, rather than a single judge model, provides
mostofthediscriminatoryperformance.Second,theproductionjudge,ClaudeOpus
4.8, produces 2 false positives and 5 false negatives, placing it among the best-
performing models and supporting its selection. Third, performance improves with
model generation. Claude Fable 5 produces the fewest errors, with 1 false positive
and 3 false negatives, indicating that the same rule set can benefit from improve-
ments in the underlying model without further modification. The models also exhibit
different trade-offs between false positives and false negatives. Claude Sonnet 4.6,
for example, misses only one defective scenario but produces ten false positives.
Judge-model selection therefore affects the balance between detection sensitivity
andunnecessaryintervention.
Discussion
DREAMS demonstrates the use of large language model (LLM) agents for
autonomous computational materials research. The framework combines hierarchi-
cal task planning, domain-specific tools, shared memory, and multi-tier verification
from tool execution to final reporting. DREAMS performs periodic solid-state DFT
workflows at an enhanced L2 (L2+) automation level that approaches L3. Its archi-
tectureaddresseslimitationsofexistingLLMagents,includinghallucination,context
loss,inadequateerrorrecovery,andtheabsenceofverifiablenumericalresults.
Evaluation on the Sol27LC benchmark establishes the accuracy and reliability
of DREAMS for lattice-constant calculations. For CO/Pt(111), DREAMS performs
adsorption-energy calculations across multiple configurations and reproduces the
expected site preference, demonstrating its applicability to rigorous materials sim-
ulations. For exchange-correlation functional uncertainty, DREAMS uses Bayesian
ensemble sampling with BEEF-vdW to quantify functional-dependent variation. The
analysis shows that the FCC-site preference remains robust across the ensemble
andrelatesthispreferencetotheunderlyingelectronicstructure.
26

Fig. 8: Judge confusion matrices on the 145-scenario adversarial suite for five
Anthropic models. Rows are intended verdicts (should-pass, should-fail); columns
arethemajorityverdictoverthreejudgecalls(pass,warning,fail).Awarningcounts
ascatchingashould-failscenario,whileanynon-passverdictonashould-passsce-
nariocountsasafalsepositive;per-modelfalse-positive(FP)andfalse-negative(FN)
countsareindicatedaboveeachpanel.
Two additional evaluations characterize the framework. In the four-system com-
parison, the unguarded agent produces a nearly correct final value despite an
essential-step success rate of only 81%, because systematic errors partially can-
celinthecalculatedenergydifference.Theguardedsystemproducesacomparable
resultwithallessentialstepsverifiedbutrequiresapproximately13timesmoreinput
tokens. This increase reflects the cost of performing and recording the verification
steps.Thepresentstudyevaluatesthestrictestconfiguration,withallverificationlay-
ersenabled.ThecostofthatstrictnessisvisibleintheCO/Pt(111)study:thereport
judgedemandedcharacterizationofavacuumvaluethatwasalreadyphysicallyade-
quate,atthepriceofoneadditionalconvergencetestandasecondproductionround;
thetestinturnconfirmedtheheldvaluewasneverunder-setandidentifiedacheaper
converged setting. Such a test may seem redundant at this scale, but the same
checkbecomescriticalinmassiveproductioncampaignsconsistingofthousandsof
calculations, where an uncharacterized setting propagates into every result and an
over-set one wastes compute in every calculation. Individual layers can be disabled
toreducecostattheexpenseofverificationcoverage.Identifyingtheoptimalverifica-
tionconfigurationandjudgemodelremainsfuturework.Evaluationacrossfivejudge
models further shows that the adversarially refined rules transfer between models
andthatjudgeperformanceimproveswithnewermodelgenerations.Theverification
27

system can therefore benefit from improvements in the underlying models without
revisingtheruleset.
UnderthetaxonomyinTable1,DREAMSapproachesL3automation.L3denotes
autonomous search within a design space defined by the scientific objective,
whereasautonomousconstructionorrestructuringofthatdesignspacecorresponds
to L4 or higher. In the present studies, the candidate crystal structures, adsorp-
tion sites and orientations, and exchange-correlation functionals are specified in
advance. DREAMS then executes the search, submits and monitors calculations,
diagnosesfailures,andrevisesitsplanautonomously.Benchmarkexecutionissepa-
ratedfromevaluation:thetaskspecificationscontainnotargetreferencevalues,and
the calculated values are compared with established references only after workflow
completion. Each reported quantity is computed anew through structure construc-
tion, convergence testing, HPC execution, error recovery, and post-processing, with
its computational origin recorded in the provenance chain. The provenance record
establishes that the reported values derive from executed calculations rather than
a supplied reference; it cannot establish that knowledge encountered during model
training did not influence workflow choices. These benchmarks therefore evaluate
autonomous computational reproduction under controlled conditions, not the gener-
ation of previously unknown scientific knowledge. Evaluation on problems without
known solutions is required to establish full L3 discovery capability. Future work
will extend DREAMS to open-ended problems with dynamically constructed design
spaces.
Key innovations in our approach include: (1) a multi-tier safety guard that veri-
fies numerical values deterministically and semantically at tool-call and report time;
(2) deterministic tools that constrain agent actions while preserving task flexibility;
(3) a planning supervisor that decomposes research objectives into validated exe-
cutionsteps;(4)asharedcanvasforcommunicationandstatemanagementacross
agents;and(5)systematicconvergenceproceduresforcomputationalvalidation.The
safetyguardisindependentofDFTbecauseitsprovenanceregistration,verification
gates, and judge evaluations do not depend on a specific computational method.
It can therefore be applied to other computational workflows that require auditable
numericalresults.
Several limitations remain. The judge rules were adversarially refined using
DFT-specific scenarios and may require task-specific adaptation for other domains.
Developingrulesthatgeneralizeacrossmultiplescientifictasksisanimportantdirec-
tion for future work. The evaluated judge panel includes only Anthropic models;
broaderevaluationacrossmodelfamiliesisalsorequired.Inaddition,thelistofsen-
sitive parameters is defined by domain experts. The guard enforces this knowledge
but does not identify sensitive parameters autonomously. Future work should com-
pare the convergence agent with documentation-retrieval and retrieval-augmented
baselinesonidenticalcalculationfailures,andevaluateitsgeneralizationbeyondthe
establishedworkflowssupportedbythecurrenttoolset.
ThisworkprovidesageneralframeworkforapplyingLLMagentstocomputational
materials science and chemistry. Future studies may extend DREAMS to addi-
tional scientific domains and incorporate specialized agents for other computational
28

methods. For CO/Pt(111), the present results indicate that GGA-level theory alone
is insufficient to resolve the adsorption-site discrepancy. Further analysis should
include thermal corrections, coverage effects, higher-rung exchange-correlation
functionals,includingmeta-GGAandhybridfunctionals,andDFT+Uwhereelectron
localization is relevant. More broadly, agentic workflows may support scientific dis-
coverybyautomatingcomputationalstudies,identifyingmissingphysicaleffects,and
generatingmechanisticinterpretations.
Methods
DREAMS (DFT based Research Engine for Agentic Materials Simulation) is imple-
mentedasahierarchicalmulti-agentsystembuiltontheLangGraph[78]framework.
The planning supervisor and the worker LLM agents—a DFT LLM agent and an
HPC LLM agent—are backed by Claude Sonnet 4.5 [73] at temperature zero; the
LLM judges of the safety-guard system operate outside the agent loop and are
backed by Claude Opus 4.8 [74]. Each worker LLM agent is built as a ReAct
agent [79] and incorporates various tools for execution; reasoning lets the work-
ers adapt dynamically to changing task requirements and handle exceptions, while
actions let them interface with built-in functions as tools. Their system prompts are
structured into sections (⟨Role⟩, ⟨Objective⟩, ⟨Instruction⟩, ⟨Requirement⟩), and
the complete operational prompt set is provided in Supplementary Information S-
7. DREAMS’ tools are deterministic at their core: each consists of a deterministic
body—structure construction, script generation, file parsing, analysis—wrapped in
the safety-guard interface described below, which validates the call before the body
runs and registers its output with full provenance afterward. The single deliberate
exception is the convergence agent, an LLM embedded inside a tool to diagnose
failed calculations, described in its own subsection. Rigorous validation checks and
informativeerrormessagesineverytoolsupportagentself-correction,andthecan-
vasissharedamongallagents,tools,andthehumanusertomitigatehallucination.
This hierarchical approach is chosen for its flexibility, its ability to manage complex
interactionsamongmultipleLLMagents,anditsextensibility.
Dynamic Planning
The planning supervisor LLM agent plays a central role in orchestrating the over-
all workflow. Unlike simple task schedulers, the supervisor decomposes complex
research objectives into manageable subtasks tailored to each worker LLM agent’s
capabilities. The workflow state carries the user objective, the current plan, a typed
recordofexecutedsteps,thecanvas,andtheartifactregistry,sothatplans,memory,
andprovenancearecheckpointedtogetherandastudycanberesumedorrewound.
Each plan step names the worker agent responsible for it, the tool whose success-
ful call the step requires, and, for steps that consolidate findings, the quantities the
resulting report must deliver; the first two requirements prevent an agent from pro-
ducing a result without a tool, and the third prevents it from quietly not reporting
one.Ratherthanrewritingtheplanwholesaleaftereverystep,thesupervisoreditsit
throughthreevalidatedoperationsthatinsert,modify,ordeletesteps,andeveryedit
29

ischeckedbeforeacceptance:theassignedagentmustexist,therequiredtoolmust
belong to that agent’s toolset, and report steps must declare their required quanti-
ties. After a worker completes a step, the framework verifies that the required tool
wasactuallycalled;forreportstepsitadditionallyaudits,deterministically,thatevery
required quantity appears in the report and matches its cited artifact, and a report
failing this audit is deleted and the step retried with the failure explained. Once a
worker has generated a report within a step, its toolset is restricted to bookkeeping
operations until the step ends, so that not-yet-verified numbers cannot flow into fur-
ther work. When a report passes verification, the span of steps that produced it is
archivedandreplacedintheactivehistorybyasinglesummaryrecord,keepingthe
supervisor’s context bounded without destroying the trail. Once the objective is fully
addressed,thesupervisorwritesthefinalresponseandterminatestheworkflow.We
refertothisplanningasdynamic becausethesupervisordoesnotcommittoafixed
planattheoutset;instead,itrevisestheplanwheneverastepcompletesoranunex-
pected situation arises, taking a holistic view of the objective, the current plan, and
thehistoryofcompletedsteps—incontrasttoframeworksthatgenerateasingleplan
upfrontandleaveanydeviationtobehandledlocallybytheworkerthathappensto
encounter it. Plan creation and revision remain solely the responsibility of the plan-
ning supervisor; worker LLM agents do not access the plan-editing tools or modify
the plan. Workers may provide domain-specific input when explicitly consulted, and
their execution results, failures, and reports inform subsequent planning decisions,
but the supervisor alone determines whether and how this information is translated
intoplanedits.
DFT LLM Agent
TheDFTLLMAgentfunctionsasaspecializedworkerLLMagentwithcomputational
chemistryexpertisefocusedonrigorousperiodicsolid-statedensityfunctionaltheory
(DFT)calculations.ThisLLMagentisresponsibleformanagingthescientificaspects
of electronic structure calculations, including the construction of atomistic models,
optimization of computational parameters, and analysis of calculation results. The
DFT LLM agent’s core functions include: (1) generating atomistic structures such
as bulk crystals, surfaces, and adsorbate configurations; (2) determining suitable
DFTconvergenceparametersthroughsystematicconvergencetesting;(3)preparing
input files for quantum chemistry software; and (4) analyzing outputs and extracting
physical properties, including lattice constants and adsorption energies. To perform
these tasks, the DFT LLM agent is equipped with a suite of tools, each designed
for a specific purpose. The LLM agent selects tools based on their documented
capabilities. Convergence-parameter selection supports two modes: one sweeps a
calculation parameter and compares each output directly against a most-converged
reference, while the other compares derived quantities, enabling structural conver-
gence tests, such as slab thickness, whose criterion is a derived observable rather
thanarawtotalenergy.FurtherdetailsofthesetoolsareprovidedinSupplementary
InformationS-8.
30

The tools of the DFT LLM agent are interfaced through established frameworks
such as the Atomic Simulation Environment (ASE) [75], preventing unsafe opera-
tions like direct file manipulation, which can otherwise lead to invalid structures or
runtimefailures.Eachtoolmaintainsexplicitinput-outputmappingsandimplements
comprehensive error handling. For example, the adsorption energy tool requires
exactlythreeDFToutputfiles(cleanslab,isolatedadsorbate,andadsorbate-on-slab)
and applies standard thermodynamic formulas to compute results. This architec-
ture prevents unsupported file operations and enforces the prescribed input–output
relationships,therebyreducingtheopportunitiesforhallucinatedparameters,incon-
sistent inputs, and incorrect arithmetic. To further reduce redundancy and the risk
of inconsistencies, we develop deterministic batch tools that generate Quantum
ESPRESSO (QE) [64] input files from a single complete input. The agent supplies
the structure, pseudopotentials, and full DFT parameterization to an ASE-backed
tool,whichrendersacompleteQEinputfileinQE’sstructuredplain-textsyntax.This
file is termed a template only because downstream batch tools inherit its settings; it
is neither a Python script nor a pre-supplied fill-in-the-blank form. For convergence
testing, the batch tool programmatically substitutes only the swept parameter while
preservingtheremainderoftheinput.Thedeterministicfile-generationworkandtotal
file output remain O(N), but LLM-mediated specification is reduced from N com-
plete parameterizations to one. This lowers LLM API calls, LLM output tokens, and
response latency while reducing the risk of agent-introduced inconsistencies. For
EOS calculations, the batch tool uniformly scales the cell and generates five com-
pleteQEinputfilesusingtheconvergedproductionsettings.Agreementwithexpert
reference results therefore reflects the complete workflow—structure construction,
parameterselectionandempiricalconvergence,QEexecution,outputextraction,and
EOSfitting—ratherthaninput-templatecompletionalone.
Atomistic Structure Generation
In the benchmarking experiment on the CO/Pt(111) system, we utilize the AutoCat
library [14] as a computational framework for generating and analyzing adsorption
structures.ComparedtosimplylettingtheLLMdecidetheatomisticstructures,using
AutoCat to control the structural degrees of freedom ensures that the structures to
be simulated are physically meaningful. For example, DREAMS can create struc-
tures with different adsorbate sites, surface slab sizes, vacuum spacing, adsorbate
orientations, coverage patterns, and adsorption heights, and we are confident that
thestructuresarephysicallymeaningful,asillustratedinFig.7(a).
ImplementingdomainknowledgethroughAutoCatalsoavoidsredundantconfig-
urations. For example, for Pt with FCC crystal structure, the (111) surface has only
four distinct adsorption sites, namely the ontop, bridge, FCC, and HCP sites. How-
ever, if such symmetry constraints are not known in advance, a grid search with a
0.1Åspacingwouldresultin121possibleadsorptionsites,whichisalmost30times
thecomputationalcost.
In conclusion, AutoCat abstracts these low-level configurational operations
behind a structured API, allowing LLM agents to invoke high-level actions such as
“generateFCCadsorptionstructureswithallrelevantCOorientations”withouthaving
31

to reason about individual atomic coordinates or manually define geometry con-
straints. The integration of such carefully designed tools thus enables reliable and
efficientexplorationofachemicallyrichconfigurationspacethatwouldotherwisebe
pronetofailureorhallucinationifhandledentirelyattheLLMlevel.
Thisstructuredinterfacecreatesadeliberatetradeoffbetweenreliabilityandgen-
erality. The present tools support bulk structures, ideal crystalline slabs, variation
of the exposed slab parameters, and adsorption configurations constructed from
sites identified by AutoCat. They do not constitute a universal geometry generator:
surface reconstructions, steps, defects, arbitrary multicomponent terminations, and
protocolsoutsidetheavailabletoolschemasarenotsystematicallysupportedinthis
work. Such capabilities require implementing and testing an additional domain tool
and, when safety guards are active, specifying the associated sensitive parame-
tersandverificationrules.Thesupervisor–workerorchestrationdoesnotneedtobe
redesigned, but the executable scientific domain remains bounded by the tools that
havebeenintegratedandvalidated.
Convergence LLM Agent
The convergence LLM agent is implemented as a large language model (LLM)
embedded within a tool. To use this tool, the DFT LLM agent must first spec-
ify which job has encountered a convergence issue. The tool then locates
the relevant files for that job and, for each file, prompts the LLM with the
followingquery:Here is the content of the file <content>, please give me
suggestions on how to fix the convergence issue. The LLM is instructed to
provide a structured and concise response to the formatted question. In this setup,
most operational tasks, such as parameter parsing and preprocessing, are handled
deterministically by code. This allows the LLM to focus exclusively on decision-
making.BydecouplingconvergencediagnosisfromthebroaderLLM-agentcommu-
nicationgraph,thededicatedagentcananalyzetherelevantinput,output,anderror
files without adding them to the DFT worker’s already extensive workflow context.
In our benchmark runs, this focused context reduced the hallucinated and erratic
recovery actions observed when the worker handled these files directly, although
component-level recovery rates and variability across LLM APIs were not system-
atically evaluated. The convergence LLM agent provides suggestions for parameter
settings and script generation, enabling the DFT LLM agent to self-correct and con-
duct updated calculations. These suggestions are generated from the base LLM’s
pretrained knowledge conditioned on the supplied job files; no parameter-specific
remedial heuristics, decision trees, or lookup tables are embedded in the prompt
or tool. When a parameter such as electron_maxstep is changed, the updated
input is submitted as a new calculation with restart_mode = from_scratch, and
no electronic state from the preceding iterations is reused. Although QE supports
checkpoint-basedcontinuation,itisnotenabledherebecauseretainingtherequired
restartdataincurssubstantialdiskoverhead.Representativesuggestionsareshown
inTable3.
32

HPC LLM Agent
The HPC LLM agent is a resource- and job-orchestration component. It reads the
Quantum ESPRESSO inputs and job list, proposes resource requests from the
site-specific cluster configuration, records those suggestions, submits calculations
through pysqa to SLURM, monitors their status, and retrieves the resulting files. It
does not execute the numerical kernels or modify Quantum ESPRESSO’s paral-
lelizationstrategy.Computationalefficiency,parallelscaling,andacceleratorsupport
therefore depend on the underlying Quantum ESPRESSO build and hardware and
arenotevaluatedasperformancepropertiesoftheagent.
The present implementation was tested on a SLURM-based [80] CPU cluster
with AMD 9654 processors. Deployment on another system requires site-specific
scheduler,partition,resource,software-module,andsubmission-scriptconfiguration.
Non-SLURM schedulers and GPU execution were not evaluated in this work. The
submissioninterfaceusesthePythonSimpleQueuingSystemAdapter(pysqa)[12];
the HPC-agent tools and their arguments are documented in Supplementary Infor-
mationS-8.
Memory and communications among human user, LLM
agents, and tools
Effective communication is essential for ensuring reliable task execution and the
accuracy of final results. To achieve this, DREAMS establishes a structured com-
munication flow among the user, supervisor agent, worker agents, and tools, which
is illustrated in Fig. 9. When the user invokes DREAMS with a request, the request
is 1 sent to the supervisor. The supervisor then 2 checks the canvas for exist-
ing information, 3 generates or updates the plan, determines which worker agent
should act next, and 4 issues the command “You need to do xxx.” Along with this
instruction, the overall objective and summaries from previous steps are 5 sent to
the worker agent. Upon receiving the task, the worker agent 6 retrieves relevant
informationfromthecanvasand 7 invokestheappropriatetools.Eachtoolcan 8
access and update the canvas as needed. After completing the assigned task, the
worker agent 6 writes key results to the canvas and 9 adds a summary of the
current step. Steps 2 through 9 repeat until the supervisor 1 provides a final
responsetotheuser.Duringtheprocess,thehumanusercan 10 readthecanvas
tomonitorprogress.Althoughnotyetactivated,theusercouldalsowriteinformation
tothecanvastoshareadditionalcontextwithagentsandtools.
Canvas stores all variables in their native format, reducing errors and preventing
hallucinationsthatmayarisefromconvertingdatatoandfromtext,anditisorganized
intothreestores.Notes arefree-formworkingdocumentsfortheagents’day-to-day
bookkeeping; they are version-controlled and append-only: editing a document cre-
ates a new version in its family, and existing content is never destroyed. Artifacts
formtheappend-onlyprovenanceregistryusedbythesafetyguard:everyregistered
33

⑩ Canvas
User Read-only for agents
Plan {key1: value1, key2: value2, …}
①
Info1
Conditional read-only for agents
You need to do xxx ④ ③
{key1: value1, key2: value2, …}
Info2
Supervisor ②
Overallobjective
{
step1_result:
Info3 ⑤ {
Summarized results ⑥ key1.1: value1.1,
from previous steps key1.2: value1.2,
Summarized results ⑨ Worker Agents }
from this step key2: value2,
⑦ step2_result: value3,
…
}
⑧
Tools
Fig.9:Communicationflowamonguser,agents,tools,andthecanvasinDREAMS.
The user (1) sends a request to the supervisor, who (2) checks the canvas, (3)
forms a plan, and (4–5) assigns a task—with the instruction, overall goal, and sum-
maries—to a worker agent. The worker (6) reads from the canvas, (7) calls tools,
whichcanalso(8)accessorupdatethecanvas.Aftercompletingthetask,theworker
(6)recordsresultsand(9)summariesforthenextcycle.Stepsrepeatuntilthesuper-
visor (1) replies to the user, who can (10) monitor progress. Canvas serves as a
centralized, structured memory for all data in native format, supporting safe read-
/write operations, access control, and transparent logging to ensure consistent and
reproduciblecommunication.
tool output receives an immutable eight-character result identifier, and each artifact
records the producing tool, the value, the full argument list, the per-parameter rea-
sons, the per-parameter sources, and the declared context. A reference may name
an artifact’s output (a bare identifier) or a specific input parameter of a past call (a
dotted identifier of the form <id>.<parameter>), and referenced values are verified
deterministically against the registry for both existence and equality. Reports are
structuredscientificfindings;onceverified,areportbecomesimmutableandcanno
longer beedited oroverwritten. The threemain canvas functions—inspection, read-
ing, and writing—are exposed to the LLM agents through specialized tools, while
tools access the underlying stores directly through native operations. For inspec-
tion,noargumentsarerequiredandthecanvasreturnsthelistofavailablekeys.For
reading,avalidkeymust beprovided;ifthekeyisinvalid,thecanvassuggestsper-
forming an inspection to locate the correct key before attempting to read again. For
writing,theagentmustsupplyadescriptivekeytogetherwiththeobjecttobestored,
34

and overwriting an existing key requires explicit confirmation, preventing accidental
dataloss.Framework-ownedkeyspaces—judgefeedbackandarchivedhistory—are
readablebutnotwritablebyagents,andanyattempttoviolateanaccessconstraint
returns an informative warning to guide corrective action. All updates to the can-
vas are logged and made visible to human users for transparency and to support
post-processing. Additionally, a serialized object (a pickle file) is created to capture
thecurrentstateofthecanvasandtheartifactregistry,enablingsessionresumption
and ensuring data availability for downstream analysis. Persistence across runs is
therefore optional and under user control: if the working directory already contains
this pickle file, the canvas state is restored, otherwise an empty canvas is created.
WeusepickleratherthanJSONbecausethecanvasstoresarbitrarynativeobjects,
including custom Python classes, that JSON cannot serialize; the human-readable
lognotedaboveisgeneratedseparatelyfortransparency.Intheframeworkcompar-
ison, the baseline systems (MDCrow and ChemGraph) were not equipped with an
equivalent canvas, as it is one of the novel components of DREAMS and requires
systematicintegration.
A full snapshot of the canvas from the Sol27LC challenge is provided in Sup-
plementary Information S-2. The snapshot illustrates how intermediate structures,
parameters, and calculation results remain available across successive workflow
stages.
Safety guard
Everyguardedtoolcallmustsupply,inadditiontoitsscientificarguments,adeclared
context (one to two sentences naming the study or exploration the call belongs to
and why the tool is being called) and a per-parameter rationale covering, for each
parameter,theroleitplaysinthestudydescribedbythecontextandwhythisspecific
value was chosen. For parameters designated as sensitive—a human-defined list,
specified in the configuration, of the parameters known to control result validity in
thedomain—theagentmustadditionallysupplythereferenceoftheregisteredresult
the value came from. Only tool outputs become artifacts, and an agent that has not
registered a value has no reference to hand to the next tool: a forgotten registration
stallsprogressratherthancorruptingit.Theagentcanforget,butitcannotfabricate.
Verificationattool-calltimeproceedsintheorderdescribedintheResults:deter-
ministic checks first (each supplied reference must exist in the registry, and the
suppliedvaluemustequaltherecordedone),thentheper-parameterjudge,thenthe
cross-parameter judge; the tool body runs only if all pass. The per-parameter gate
constructsaprovisionalartifactfromthefieldstoberegisteredandappliesthesame
verificationprocedureusedbythereport-timejudge.Bothstagesusethesamecode
pathandruleset,allowingviolationstobeidentifiedbeforetoolexecutionproceeds.
However,thegateevaluatesonlythecurrenttoolcallanddoesnotrecursivelyinspect
itsupstreamprovenance.Itthereforelacksthecompletedependencychainavailable
tothereport-timejudge.Thetwostagesmayconsequentlyproducedifferentverdicts
inambiguouscases.IntheCO/Pt(111)study,thecall-timejudgeacceptedthedotted
vacuum reference, whereas the report-time judge rejected it after inspecting the full
provenance chain. The report-time verdict determines whether a claim is accepted.
35

Thecross-parametergateisattachedtotheanalysistoolswhosevaliditydependson
the joint configuration of their inputs, such as convergence-parameter selection and
equation-of-statefitting.Thearithmetictoolverifieseachinputagainstitscitedartifact
beforeevaluating,andrejectsexpressionswhoseoutputisaninputpassedthrough
unchangedortriviallyrescaled(forexamplex +0orx ×1.0),thepatternbywhich
0 0
achosennumbercouldotherwisebelaunderedintoacomputedone.Theextraction
tools require a unique evidence snippet and accept a value only if it appears ver-
batim in the recorded output of the cited call. Gate verdicts are pass, warning (the
value is registered with the concern stamped in the artifact’s metadata), or fail (the
tooldoesnotrun,nothingisregistered,andthejudge’sreasoningisreturnedtothe
agent). Guards fail open: an infrastructure error inside a guard never blocks a run;
onlyascientificverdictdoes.
A structured report consists of the study goal, the quantities sought, numerical
claims—eachbindingaquantityname,avalue,andthereferenceoftheartifactcar-
rying it—qualitative findings, and a narrative in which every number must be tied to
a claim. Verification proceeds from each claim: the claimed value is first matched
deterministically against its cited artifact; a coherence check then asks whether the
citedartifactistherightkindofsourcefortheclaimedquantity,notmerelyanumeri-
callycoincidentone;andthejudgefinallydescendstheprovenancegraph,applying
to every parameter of every contributing call a rule selected by that parameter’s
situation—sensitiveandsourced,sensitiveandswept,sensitivewithoutasource,or
not sensitive—with the recorded context deciding whether a choice is judged under
explorationorproductionstandards.Failuresarereturnedascategorizedissueswith
remediation instructions that explicitly forbid the shortcut responses: patching in a
differentreference,silentlydroppingafailingrequiredquantity,orsubstitutingamath-
tool fabrication. Verified subtrees are cached across reports, so an already-verified
intermediate result is not re-judged when later reports build on it. The full rule texts,
judge guidance, and issue categories are provided in Supplementary Information
S-11.
Finally, a standalone debug tool exposes the same provenance walk for inves-
tigation rather than verification: given a surprising result and a question, it walks
the value-flow chain parameter by parameter and returns ranked hypotheses about
which parameter or source could explain the result, explicitly labeled as hypotheses
to be tested one variable at a time. We note that this machinery has repeat-
edly caught our own implementation mistakes during development—hard-coded file
input/output, wrongly registered argument values, an input file referenced where an
output was intended—suggesting that the value of mechanical verification extends
beyondagentmisbehaviortotheframeworkitself.
Judge implementation and adversarial tuning
All judges share one implementation: a Claude Opus 4.8 model constrained to a
structuredoutputschemainwhichthereasoningfieldprecedestheverdict,sothata
verdict cannot be emitted without first stating its grounds; malformed responses are
retried.Besidestheartifactunderreview,eachjudgepromptreceivestheproducing
36

tool’s live documentation—its docstring and the annotation of the specific argument
underreview—sothejudgeevaluatesusageagainstthetool’sactualcontract.
This documentation feed was motivated by observed judge failures. Early ver-
sions of the per-parameter judge, which saw only the tool name and the artifact
description, produced characteristic false positives: they flagged the reference cal-
culation appearing in the candidate list of the convergence-selection tool as mixing
the reference into the test set, when the tool requires exactly that; and they flagged
a candidate list combining two sweep batches as cross-wiring, which is legitimate
wheneverallfilesshareidenticalsettingsapartfromthesweptparameter.Thejudge
couldnotknoweitherfactwithoutseeingthetool’sdocumentation.
Thejudgerulesweretunedagainstastandalonescenarioharnessratherthanby
inspection.Scenariosareconstructedneutrally:eachcarriesahypothesisaboutthe
expectedverdictthatisusedonlytotriagedisagreements,nevertoshapetherules,
andfalsepassesandfalsefailuresarealwaysmeasuredtogether.Aninitialsynthetic
suite produced spurious failures for an instructive reason—its parameter rationales
werefarthinnerthananythingarealrunproduces—sothesuitewasrebuiltfromthe
artifactsofrealruns:eachcleanscenariomirrorsarealregisteredartifactwithitsrich,
study-situated rationale, and each flawed scenario is that realistic base with exactly
one injected defect, drawn from a catalog including a wrong reference direction, a
source of the wrong physical kind, an unjustified value magnitude, a deliberately
genericrationale,amismatchbetweencharacterizationandproductionconditions,a
wrong file role, and laundering through a dotted reference. Scenarios are grounded
mostlyintheCO/Pt(111)system,withasecondchemistryincludedsothattherules
arenottunedtoasinglesystem’sidioms.Aproposedrulechangewasacceptedonly
if,onre-runningtheharness,allcleanscenariosstillpassedandalldefectscenarios
still failed, guarding both sides of the false-positive/false-negative tension. The final
rule set was evaluated on 145 scenarios by majority vote over three judge calls per
scenario, counting a warning as catching a should-fail case, across five Anthropic
models; the resulting confusion matrices are reported in Fig. 8. Further details of
the scenario suite and adversarial-tuning procedure are provided in Supplementary
InformationS-12.
DFT Benchmark
Density functional theory (DFT) is one of the most widely employed first-principles
simulation methods for atomistic systems. Through solving for the ground-state
electronic density and calculating the potential energy surface of a given atomistic
system,DFTprovidesmechanisticunderstandingonthermodynamicphasestability,
crystal structures, electronic properties, etc. Readers are recommended to refer to
the listed reference for more information [81]. A number of software packages have
beendevelopedtocarryoutthesecalculations,includingVASP[82],Gaussian[83],
QuantumESPRESSO(QE)[64],etc.
In this work, we use QE v7.2 for DFT calculations, which uses plane wave
(PW) basis for describing the electronic wavefunction, and uses pseudopotentials
(PP) to describe core electrons. We also investigate the impact of exchange-
correlation functional (XC) choices on calculated structural properties, including the
37

lattice constant and adsorption energies. These include functionals under the local
density approximation (LDA) and the generalized gradient approximation (GGA),
namelyPerdew–Burke–Ernzerhof(PBE)functionalandthePW91functional.Allthe
calculationsarecarriedoutusingtheGBRVpseudopotentials.
The lattice constant values are obtained by fitting an equation of state (EOS)
curve between DFT-calculated potential energies and volumes, and finding the
lowest-energy point. These values are benchmarked using the Sol27LC dataset,
whichwascollectedinRef.[67]andincludeslatticeconstantsof27elementalcrys-
tals in BCC, FCC, and diamond lattices. The elements in this dataset cover both
metals and non-metals, which makes it ideal for testing DREAMS’ ability across the
periodictable.Theadsorptionenergiesarecalculatedas:
E =E −E −E (2)
ads CO−Pt(111) CO Pt(111)
where E , E and E are the potential energies of the Pt(111) slab
CO−Pt(111) CO Pt(111)
withaCOmoleculeadsorbedontop,thesingleCOmolecule,andthecleanPt(111)
surface, respectively. The results in this work are benchmarked against results pro-
duced by Peter et. al. [68] who systematically analyzed CO adsorption on Pt(111)
using a range of DFT implementations and settings. For uncertainty quantification,
the Bayesian error estimation functional with van der Waals correction (BEEF-vdW)
is used. We use a total of 2,000 functionals in our ensemble to sample the energy
distribution.[84]
Framework Comparison
All DFT calculations are conducted on the in-house HPC cluster with AMD 9654
CPU.TheversionofMDCrowbenchmarkedis0.0.2,withLangChainversion0.2.12.
The version of ChemGraph benchmarked is 1.0.0, with LangChain version 0.3.27
andLangGraphversion0.4.7.
Data Availability
TheSol27LCdatasetisavailablehere.
Code Availability
Codeisavailableon:GitHub
Acknowledgements
This work was supported by Los Alamos National Laboratory under the grant num-
ber AWD026741 at the University of Michigan. This work was also supported by
Anthropic’sAIforScienceProgram.TheauthorsthanksNAIRRforprovidingaccess
totheMicrosoftAzureservice.TheauthorthanksAdvancedResearchComputingat
theUniversityofMichiganforprovidingcomputingresources.
38

Author contributions
Z.W. led the development of DREAMS and drafted the manuscript. H.H. and H.Z.
assisted in implementing DREAMS. C.X. assisted in benchmarking experiments.
S.Z., J.J., and V.V. contributed to project conceptualization. Z.W., H.H., H.Z., C.X.,
S.Z.,J.J.,andV.V.contributedtomanuscriptrevisionandapprovedthefinalversion.
| Competing | Interests: |     |     |     |     |     |
| --------- | ---------- | --- | --- | --- | --- | --- |
We have filed a provisional patent application on computational agents for scientific
simulations.
References
[1] Menon, S., Lysogorskiy, Y., Knoll, A.L.M., Leimeroth, N., Poul, M., Qamar, M.,
Janssen,J.,Mrovec,M.,Rohrer,J.,Albe,K.,Behler,J.,Drautz,R.,Neugebauer,
J.: From electrons to phase diagrams with machine learning potentials using
| pyiron based | automated | workflows. | npj Comput | Mater | 10, | 261 (2024) |
| ------------ | --------- | ---------- | ---------- | ----- | --- | ---------- |
[2] Ertekin,E.,Schiller,J.A.:Acombineddft/machinelearningframeworkformate-
rialsdiscovery:Applicationtospinelsandassessmentofsearchcompletenessand
efficiency. ChemRxiv (2020) https://doi.org/10.26434/chemrxiv.13070549.v1
[3] Jain,A.,Ong,S.P.,Hautier,G.,Chen,W.,Richards,W.D.,Dacek,S.,Cholia,S.,
Gunter, D., Skinner, D., Ceder, G., Persson, K.A.: Commentary: The materials
project:Amaterialsgenomeapproachtoacceleratingmaterialsinnovation.APL
| Mater. 1(1), | 011002 (2013) |     |     |     |     |     |
| ------------ | ------------- | --- | --- | --- | --- | --- |
[4] Kavalsky,L.,Hegde,V.I.,Muckley,E.,Johnson,M.S.,Meredig,B.,Viswanathan,
V.:Byhowmuchcanclosed-loopframeworksacceleratecomputationalmaterials
| discovery? | Digit Discov | 2(4), 1112–1125 | (2023) |     |     |     |
| ---------- | ------------ | --------------- | ------ | --- | --- | --- |
[5] Santiago, M., Sanchez-Lengeling, B., Wei, J., Venugopal, V., Skreta, M., Krish-
nan,N.M.A.:Aiforacceleratedmaterialsdesign(ai4mat-2023).In:NeurIPS2023
| Workshop | (2023). https://neurips.cc/virtual/2023/workshop/66541 |     |     |     |     |     |
| -------- | ------------------------------------------------------ | --- | --- | --- | --- | --- |
[6] On-Road Automated Driving (ORAD) Committee: Taxonomy and definitions
fortermsrelatedtodrivingautomationsystemsforon-roadmotorvehicles.SAE
| International, | 3016–202104 | (2021) |     |     |     |     |
| -------------- | ----------- | ------ | --- | --- | --- | --- |
[7] Goldman, B., Kearnes, S., Kramer, T., Riley, P., Walters, W.P.: Defining levels
| of automated | chemical | design. J. | Med. Chem. | 65(10), | 7073–7087 | (2022) |
| ------------ | -------- | ---------- | ---------- | ------- | --------- | ------ |
[8] Curtarolo,S.,Setyawan,W.,Hart,G.L.,Jahnatek,M.,Chepulskii,R.V.,Taylor,
R.H., Wang, S., Xue, J., Yang, K., Levy, O., Mehl, M.J., Stokes, H.T., Dem-
chenko, D.O., Morgan, D.: Aflow: An automatic framework for high-throughput
| materials | discovery. Comput. | Mater. | Sci. 58, | 218–226 | (2012) |     |
| --------- | ------------------ | ------ | -------- | ------- | ------ | --- |
39

[9] Jain, A., Ong, S.P., Chen, W., Medasani, B., Qu, X., Kocher, M., Brafman, M.,
Petretto, G., Rignanese, G.-M., Hautier, G., Gunter, D., Persson, K.A.: Fire-
works: A dynamic workflow system designed for high-throughput applications.
Concurrency Computat.: Pract. Exper. 27(17), 5037–5059 (2015)
[10] Pizzi, G., Cepellotti, A., Sabatini, R., Marzari, N., Kozinsky, B.: Aiida:
Automated interactive infrastructure and database for computational science.
Comput. Mater. Sci. 111, 218–230 (2016)
[11] Mathew, K., Montoya, J.H., Faghaninia, A., Dwaraknath, S., Aykol, M., Tang,
H.,Chu,I.-h.,Smidt,T.,Bocklund,B.,Horton,M.,Dagdelen,J.,Wood,B.,Liu,
Z.-K.,Neaton,J.,Ong,S.P.,Persson,K.,Jain,A.:Atomate:Ahigh-levelinterface
togenerate,execute,andanalyzecomput.mater.sci.workflows.Comput.Mater.
Sci. 139, 140–152 (2017)
[12] Janssen, J., Surendralal, S., Lysogorskiy, Y., Todorova, M., Hickel, T., Drautz,
R., Neugebauer, J.: pyiron: An integrated development environment for compu-
tational materials science. Comput. Mater. Sci. 163, 24–36 (2019)
[13] Annevelink, E., Kurchin, R., Muckley, E., Kavalsky, L., Hegde, V.I., Sulzer, V.,
Zhu, S., Pu, J., Farina, D., Johnson, M., et al.: Automat: Automated materials
discovery for electrochemical systems. MRS Bulletin 47(10), 1036–1044 (2022)
[14] Kavalsky,L.,Hegde,V.I.,Meredig,B.,Viswanathan,V.:Amultiobjectiveclosed-
loop approach towards autonomous discovery of electrocatalysts for nitrogen
reduction. Digit Discov 3, 999–1010 (2024)
[15] Zimmermann, Y., Bazgir, A., Al-Feghali, A., Ansari, M., Brinson, L.C., Chiang,
Y., Circi, D., Chiu, M.-H., Daelman, N., Evans, M.L., et al.: 34 examples of llm
applications in materials science and chemistry: Towards automation, assistants,
agents, and accelerated scientific discovery. arXiv preprint arXiv:2505.03049
(2025)
[16] MacKnight,R.,Boiko,D.A.,Regio,J.E.,Gallegos,L.C.,Neukomm,T.A.,Gomes,
G.: Rethinking chemical research in the age of large language models. Nat
Comput Sci (2025)
[17] Alampara, N., Schilling-Wilhelmi, M., Ríos-García, M., Mandal, I., Khetarpal,
P., Grover, H.S., Krishnan, N.A., Jablonka, K.M.: Probing the limitations of
multimodal language models for chemistry and materials research. Nat Comput
Sci (2025)
[18] Miret, S., Krishnan, N.A.: Enabling large language models for real-world mate-
rials discovery. Nat Mach Intell 7, 991–998 (2025)
[19] Ghafarollahi, A., Buehler, M.J.: Sciagents: Automating scientific discovery
through bioinspired multi-agent intelligent graph reasoning. Adv. Mater. 37,
40

2413523 (2024)
[20] Song, T., Luo, M., Zhang, X., Chen, L., Huang, Y., Cao, J., Zhu, Q., Liu, D.,
Zhang,B.,Zou,G.,Zhang,F.,Shang,W.,Jiang,J.,Luo,Y.:Amultiagent-driven
robotic ai chemist enabling autonomous chemical research on demand. J. Am.
Chem. Soc. 147(15), 12534–12545 (2025)
[21] M. Bran, A., Cox, S., Schilter, O., Baldassari, C., White, A.D., Schwaller, P.:
Augmenting large language models with chemistry tools. Nat Mach Intell 6,
525–535 (2024)
[22] Campbell, Q., Cox, S., Medina, J., Watterson, B., White, A.D.: Mdcrow:
Automating molecular dynamics workflows with large language models. arXiv
preprint arXiv:2502.09565 (2025)
[23] Pham, T.D., Tanikanti, A., Keçeli, M.: Chemgraph: An agentic framework for
computational chemistry workflows. arXiv preprint arXiv:2506.06363 (2025)
[24] Zou, Y., Cheng, A., Aldossary, A., Bai, J., Leong, S.X., Campos-Gonzalez-
Angulo,J.,Choi,C.,Ser,C.T.,Tom,G.,Wang,A.,Zhang,Z.,Yakavets,I.,Hao,
H., Crebolder, C., Bernales, V., Aspuru-Guzik, A.: El agente: An autonomous
agent for quantum chemistry. arXiv preprint arXiv:2505.02484 (2025)
[25] Ghafarollahi, A., Buehler, M.J.: ProtAgents: protein discovery via large lan-
guagemodelmulti-agentcollaborationscombiningphysicsandmachinelearning.
DigitalDiscovery3(7),1389–1409(2024)https://doi.org/10.1039/D4DD00013G
[26] Ghafarollahi, A., Buehler, M.J.: Sparks: Multi-agent artificial intelligence model
discovers protein design principles. arXiv preprint arXiv:2504.19017 (2025)
[27] Kim, S., Choi, J., Jang, K., Park, J., Bernales, V., Aspuru-Guzik, A., Jung, Y.:
Materealize:amulti-agentdeliberationsystemforend-to-endmaterialdesignand
synthesis. arXiv preprint arXiv:2601.15743 (2026)
[28] Baek, J., Jauhar, S.K., Cucerzan, S., Hwang, S.J.: Researchagent: Iterative
research idea generation over scientific literature with large language models.
arXiv preprint arXiv:2404.07738 (2024)
[29] Zimmermann, Y., Bazgir, A., Afzal, Z., Agbere, F., Ai, Q., Alampara, N.,
Al-Feghali, A., Ansari, M., Antypov, D., Aswad, A., Bai, J., Baibakova, V.,
Biswajeet, D.D., Bitzek, E., Bocarsly, J.D., Borisova, A., Bran, A.M., Brinson,
L.C.,Calderon,M.M.,Canalicchio,A.,Chen,V.,Chiang,Y.,Circi,D.,Charmes,
B., Chaudhary, V., Chen, Z., Chiu, M.-H., Clymo, J., Dabhadkar, K., Dael-
man, N., Datar, A., Jong, W.A., Evans, M.L., Fard, M.G., Fisicaro, G., Gangan,
A.S., George, J., Gonzalez, J.D.C., Götte, M., Gupta, A.K., Harb, H., Hong, P.,
Ibrahim, A., Ilyas, A., Imran, A., Ishimwe, K., Issa, R., Jablonka, K.M., Jones,
C.,Josephson,T.R.,Juhasz,G.,Kapoor,S.,Kang,R.,Khalighinejad,G.,Khan,
41

S., Klawohn, S., Kuman, S., Ladines, A.N., Leang, S., Lederbauer, M., Sheng-
Lun, Liao, Liu, H., Liu, X., Lo, S., Madireddy, S., Maharana, P.R., Maheshwari,
S.,Mahjoubi,S.,Márquez,J.A.,Mills,R.,Mohanty,T.,Mohr,B.,Moosavi,S.M.,
Moßhammer, A., Naghdi, A.D., Naik, A., Narykov, O., Näsström, H., Nguyen,
X.V.,Ni,X.,O’Connor,D.,Olayiwola,T.,Ottomano,F.,Ozhan,A.B.,Pagel,S.,
Parida,C.,Park,J.,Patel,V.,Patyukova,E.,Petersen,M.H.,Pinto,L.,Pizarro,
J.M.,Plessers,D.,Pradhan,T.,Pratiush,U.,Puli,C.,Qin,A.,Rajabi,M.,Ricci,
F., Risch, E., Ríos-García, M., Roy, A., Rug, T., Sayeed, H.M., Scheidgen, M.,
Schilling-Wilhelmi, M., Schloz, M., Schöppach, F., Schumann, J., Schwaller, P.,
Schwarting, M., Sharlin, S., Shen, K., Shi, J., Si, P., D’Souza, J., Sparks, T.,
Sudhakar, S., Talirz, L., Tang, D., Taran, O., Terboven, C., Tropin, M., Tsym-
bal,A.,Ueltzen,K.,Unzueta,P.A.,Vasan,A.,Vinchurkar,T.,Vo,T.,Vogel,G.,
Völker, C., Weinreich, J., Yang, F., Zaki, M., Zhang, C., Zhang, S., Zhang, W.,
Zhu, R., Zhu, S., Janssen, J., Li, C., Foster, I., Blaiszik, B.: Reflections from the
2024 large language model (llm) hackathon for applications in materials science
and chemistry. arXiv preprint arXiv:2411.15221 (2025)
[30] Yamada, Y., Lange, R.T., Lu, C., Hu, S., Lu, C., Foerster, J., Clune, J., Ha,
D.:Theaiscientist-v2:Workshop-levelautomatedscientificdiscoveryviaagentic
tree search. arXiv preprint arXiv:2504.08066 (2025)
[31] Shao, C., Huang, D., Li, Y., Zhao, K., Lin, W., Zhang, Y., Zeng, Q., Chen, Z.,
Li, T., Huang, Y., Wu, T., Liu, X., Zhao, R., Zhao, M., Li, J., Zhang, X., Wang,
Y., Zhen, Y., Xu, F., Li, Y., Liu, T.-Y.: OmniScientist: Toward a co-evolving
ecosystem of human and ai scientists. arXiv preprint arXiv:2511.16931 (2025)
[32] Ding, K., Yu, J., Huang, J., Yang, Y., Zhang, Q., Chen, H.: SciToolAgent:
A knowledge graph-driven scientific agent for multi-tool integration. Nature
Computational Science (2025) https://doi.org/10.1038/s43588-025-00849-y
[33] Miao, T., Dai, J., Liu, J., Tan, J., Zhang, M., Jin, W., Du, Y., Jin, T., Pang,
X., Liu, Z., Guo, T., Zhang, Z., Huang, Y., Chen, S., Ye, R., Zhang, Y., Zhang,
L., Chen, K., Wang, W., E, W., Chen, S.: PhysMaster: Building an autonomous
ai physicist for theoretical and computational physics research. arXiv preprint
arXiv:2512.19799 (2025)
[34] Song, K., Trotter, A., Chen, J.Y.: LLM agent swarm for hypothesis-driven drug
discovery. arXiv preprint arXiv:2504.17967 (2025)
[35] Wang, F.Y., Lee, D.S., Kaplan, D.L., Buehler, M.J.: Swarms of large language
model agents for protein sequence design with experimental validation. arXiv
preprint arXiv:2511.22311 (2025)
[36] Denison, C., MacDiarmid, M., Barez, F., Duvenaud, D., Kravec, S., Marks,
S., Schiefer, N., Soklaski, R., Tamkin, A., Kaplan, J., Shlegeris, B., Bow-
man, S.R., Perez, E., Hubinger, E.: Sycophancy to subterfuge: Investigating
reward-tampering in large language models. arXiv preprint arXiv:2406.10162
42

(2024)
[37] Sharma,M.,Tong,M.,Korbak,T.,Duvenaud,D.,Askell,A.,Bowman,S.R.,Dur-
mus,E.,Hatfield-Dodds,Z.,Johnston,S.R.,Kravec,S.,Maxwell,T.,McCandlish,
S.,Ndousse,K.,Rausch,O.,Schiefer,N.,Yan,D.,Zhang,M.,Perez,E.:Towards
understanding sycophancy in language models. In: The Twelfth International
| Conference | on Learning |     | Representations | (ICLR) | (2024) |     |     |
| ---------- | ----------- | --- | --------------- | ------ | ------ | --- | --- |
[38] Dziri, N., Lu, X., Sclar, M., Li, X.L., Jiang, L., Lin, B.Y., West, P., Bhagavat-
ula, C., Le Bras, R., Hwang, J.D., Sanyal, S., Welleck, S., Ren, X., Ettinger, A.,
Harchaoui, Z., Choi, Y.: Faith and fate: Limits of transformers on composition-
ality. In: Advances in Neural Information Processing Systems (NeurIPS), vol. 36
(2023)
[39] Backlund, A., Petersson, L.: Vending-bench: A benchmark for long-term coher-
| ence of | autonomous | agents. | arXiv | preprint | arXiv:2502.15840 |     | (2025) |
| ------- | ---------- | ------- | ----- | -------- | ---------------- | --- | ------ |
[40] Sinha, A., Arun, A., Goel, S., Staab, S., Geiping, J.: The illusion of dimin-
ishing returns: Measuring long horizon execution in LLMs. In: The Fourteenth
| International | Conference |     | on Learning | Representations |     | (ICLR) | (2026) |
| ------------- | ---------- | --- | ----------- | --------------- | --- | ------ | ------ |
[41] Lu, C., Lu, C., Lange, R.T., Foerster, J., Clune, J., Ha, D.: The AI Scien-
tist: Towards fully automated open-ended scientific discovery. arXiv preprint
| arXiv:2408.06292 |     | (2024) |     |     |     |     |     |
| ---------------- | --- | ------ | --- | --- | --- | --- | --- |
[42] Trehan, D., Chopra, P.: Why LLMs aren’t scientists yet: Lessons from four
| autonomous | research | attempts. | arXiv | preprint | arXiv:2601.03315 |     | (2026) |
| ---------- | -------- | --------- | ----- | -------- | ---------------- | --- | ------ |
[43] Lin, X., Ning, Y., Zhang, J., Dong, Y., Liu, Y., Wu, Y., Qi, X., Sun, N., Shang,
Y., Wang, K., Cao, P., Wang, Q., Zou, L., Chen, X., Zhou, C., Wu, J., Zhang,
P., Wen, Q., Pan, S., Wang, B., Cao, Y., Chen, K., Hu, S., Guo, L.: LLM-based
agentssufferfromhallucinations:Asurveyoftaxonomy,methods,anddirections.
| arXiv preprint | arXiv:2509.18970 |     | (2025) |     |     |     |     |
| -------------- | ---------------- | --- | ------ | --- | --- | --- | --- |
[44] Wang,H.,Feng,S.,He,T.,Tan,Z.,Han,X.,Tsvetkov,Y.:Canlanguagemodels
solve graph problems in natural language? Adv. Neural Inf. Process Syst. 36,
| 30840–30861 | (2023) |     |     |     |     |     |     |
| ----------- | ------ | --- | --- | --- | --- | --- | --- |
[45] Kandpal,N.,Deng,H.,Roberts,A.,Wallace,E.,Raffel,C.:Largelanguagemod-
els struggle to learn long-tail knowledge. In: ICML, pp. 15696–15707 (2023).
PMLR
[46] Ji,Z.,Lee,N.,Frieske,R.,Yu,T.,Su,D.,Xu,Y.,Ishii,E.,Bang,Y.J.,Madotto,
A., Fung, P.: Survey of hallucination in natural language generation. ACM
| Comput. | Surv. 55(12), | 1–38 | (2023) |     |     |     |     |
| ------- | ------------- | ---- | ------ | --- | --- | --- | --- |
[47] Ge,Y.,Kirtane,N.,Peng,H.,Hakkani-Tür,D.:Llmsarevulnerabletomalicious
43

promptsdisguisedasscientificlanguage.arXivpreprintarXiv:2501.14073(2025)
[48] Dong,L.,Lu,Q.,Zhu,L.:Agentops:EnablingobservabilityofLLMagents.arXiv
preprint arXiv:2411.05285 (2024)
[49] Swanson, K., Wu, W., Bulaong, N.L., Pak, J.E., Zou, J.: The virtual lab of
ai agents designs new SARS-CoV-2 nanobodies. Nature 646, 716–723 (2025)
https://doi.org/10.1038/s41586-025-09442-9
[50] Li, M.Y., Vajipey, V., Goodman, N.D., Fox, E.B.: CriticAL: Critic automation
with language models. arXiv preprint arXiv:2411.06590 (2024)
[51] Dhuliawala,S.,Komeili,M.,Xu,J.,Raileanu,R.,Li,X.,Celikyilmaz,A.,Weston,
J.: Chain-of-verification reduces hallucination in large language models. arXiv
preprint arXiv:2309.11495 (2023)
[52] Zheng,L.,Chiang,W.-L.,Sheng,Y.,Zhuang,S.,Wu,Z.,Zhuang,Y.,Lin,Z.,Li,
Z., Li, D., Xing, E.P., Zhang, H., Gonzalez, J.E., Stoica, I.: Judging LLM-as-a-
judge with MT-Bench and Chatbot Arena. In: Advances in Neural Information
Processing Systems (NeurIPS) Datasets and Benchmarks Track, vol. 36, pp.
46595–46623 (2023)
[53] Zheng,X.,Pang,T.,Du,C.,Liu,Q.,Jiang,J.,Lin,M.:CheatingautomaticLLM
benchmarks:Nullmodelsachievehighwinrates.In:InternationalConferenceon
Learning Representations (ICLR) (2025)
[54] Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E.H., Narang, S., Chowdhery,
A., Zhou, D.: Self-consistency improves chain of thought reasoning in language
models. In: The Eleventh International Conference on Learning Representations
(ICLR) (2023). arXiv:2203.11171
[55] Zhu, J., Huang, Y., Shen, Y., Zhao, J., Zou, A.: Path-consistency with prefix
enhancement for efficient inference in LLMs. arXiv preprint arXiv:2409.01281
(2024)
[56] Wan, G., Wu, Y., Chen, J., Li, S.: Reasoning aware self-consistency: Leverag-
ing reasoning paths for efficient LLM sampling. In: Proceedings of the 2025
Conference of the Nations of the Americas Chapter of the Association for
Computational Linguistics: Human Language Technologies (NAACL-HLT), pp.
3613–3635 (2025). arXiv:2408.17017
[57] Goel, S., Strüber, J., Auzina, I.A., Chandra, K.K., Kumaraguru, P., Kiela, D.,
Prabhu, A., Bethge, M., Geiping, J.: Great models think alike and this under-
mines AI oversight. In: International Conference on Machine Learning (ICML)
(2025)
[58] Smit,A.P.,Grinsztajn,N.,Duckworth,P.,Barrett,T.D.,Pretorius,A.:Shouldwe
44

begoingMAD?Alookatmulti-agentdebatestrategiesforLLMs.In:Proceedings
of the 41st International Conference on Machine Learning (ICML), vol. 235, pp.
| 45883–45905. | PMLR, | ??? (2024) |     |     |
| ------------ | ----- | ---------- | --- | --- |
[59] Laban, P., Murakhovs’ka, L., Xiong, C., Wu, C.-S.: Are you sure? Challenging
LLMs leads to performance drops in The FlipFlop Experiment. arXiv preprint
| arXiv:2311.08596 | (2024) |     |     |     |
| ---------------- | ------ | --- | --- | --- |
[60] Madaan,A.,Tandon,N.,Gupta,P.,Hallinan,S.,Gao,L.,Wiegreffe,S.,Alon,U.,
Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B.P., Hermann, K.,
Welleck, S., Yazdanbakhsh, A., Clark, P.: Self-refine: Iterative refinement with
self-feedback.In:AdvancesinNeuralInformationProcessingSystems(NeurIPS),
| vol. 36, | pp. 46534–46594 | (2023) |     |     |
| -------- | --------------- | ------ | --- | --- |
[61] Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., Yao, S.:
Reflexion: Language agents with verbal reinforcement learning. In: Advances in
NeuralInformationProcessingSystems(NeurIPS),vol.36,pp.8634–8652(2023)
[62] Huang,J.,Chen,X.,Mishra,S.,Zheng,H.S.,Yu,A.W.,Song,X.,Zhou,D.:Large
language models cannot self-correct reasoning yet. In: The Twelfth International
| Conference | on Learning | Representations | (ICLR) (2024) |     |
| ---------- | ----------- | --------------- | ------------- | --- |
[63] Ghafarollahi, A., Buehler, M.J.: Automating alloy design and discovery
with physics-aware multimodal multiagent ai. Proc. Natl. Acad. Sci. 122(4),
| 2414074122 | (2025) |     |     |     |
| ---------- | ------ | --- | --- | --- |
[64] Giannozzi, P., Baroni, S., Bonini, N., Calandra, M., Car, R., Cavazzoni, C.,
Ceresoli, D., Chiarotti, G.L., Cococcioni, M., Dabo, I., Corso, A.D., Giron-
coli, S.d., Fabris, S., Fratesi, G., Gebauer, R., Gerstmann, U., Gougoussis, C.,
Kokalj,A.,Lazzeri,M.,Martin-Samos,L.,Marzari,N.,Mauri,F.,Mazzarello,R.,
Paolini, S., Pasquarello, A., Paulatto, L., Sbraccia, C., Scandolo, S., Sclauzero,
G., Seitsonen, A.P., Smogunov, A., Umari, P., Wentzcovitch, R.M.: QUAN-
TUM ESPRESSO: a modular and open-source software project for quantum
| simulations | of materials. | J. Phys. Condens. | Matter 21(39), | 395502 (2009) |
| ----------- | ------------- | ----------------- | -------------- | ------------- |
[65] Kudin, K.N., Scuseria, G.E.: Converging self-consistent field equations in quan-
tum chemistry–recent achievements and remaining challenges. ESAIM: M2AN
| 41(2), 281–296 | (2007) |     |     |     |
| -------------- | ------ | --- | --- | --- |
[66] Janssen, J., Makarov, E., Hickel, T., Shapeev, A.V., Neugebauer, J.: Automated
optimization and uncertainty quantification of convergence parameters in plane
wave density functional theory calculations. npj Comput Mater 10, 263 (2024)
[67] Wellendorff, J., Lundgaard, K.T., Møgelhøj, A., Petzold, V., Landis, D.D.,
Nørskov, J.K., Bligaard, T., Jacobsen, K.W.: Density functionals for surface sci-
ence: Exchange-correlation model development with bayesian error estimation.
| J. Phys. | Chem. B 85, | 235149 (2012) |     |     |
| -------- | ----------- | ------------- | --- | --- |
45

[68] Feibelman, P.J., Hammer, B., Nørskov, J.K., Wagner, F., Scheffler, M., Stumpf,
R., Watwe, R., Dumesic, J.: The co/pt(111) puzzle. J. Phys. Chem. B 105(18),
| 4018–4025 | (2001) |     |     |     |
| --------- | ------ | --- | --- | --- |
[69] Allian,A.D.,Takanabe,K.,Fujdala,K.L.,Hao,X.,Truex,T.J.,Cai,J.,Buda,C.,
Neurock, M., Iglesia, E.: Chemisorption of co and mechanism of co oxidation on
supportedplatinumnanoclusters.J.Am.Chem.Soc.133(12),4498–4517(2011)
[70] Grinberg, I., Yourdshahyan, Y., Rappe, A.M.: Co on pt(111) puzzle: A possible
| solution. | J. Chem. Phys. | 117(5), 2264–2270 | (2002) |     |
| --------- | -------------- | ----------------- | ------ | --- |
[71] Janthon, P., Viñes, F., Sirijaraensre, J., Limtrakul, J., Illas, F.: Adding Pieces
to the CO/Pt(111) Puzzle: The Role of Dispersion. J. Phys. Chem. C 121(7),
| 3970–3977 | (2017) |     |     |     |
| --------- | ------ | --- | --- | --- |
[72] K. G, L., Kundappaden, I., Chatanathodi, R.: A dft study of co adsorption on
| pt (111) | using van der | waals functionals. | Surf. Sci. | 681, 143–148 (2019) |
| -------- | ------------- | ------------------ | ---------- | ------------------- |
[73] Anthropic: Claude Sonnet 4.5. https://docs.anthropic.com/en/docs/
about-claude/models
[74] Anthropic:ClaudeOpus4.8.https://docs.anthropic.com/en/docs/about-claude/
models
[75] Larsen, A.H., Mortensen, J.J., Blomqvist, J., Castelli, I.E., Christensen, R.,
Dułak, M., Friis, J., Groves, M.N., Hammer, B., Hargus, C., Hermes, E.D., Jen-
nings, P.C., Jensen, P.B., Kermode, J., Kitchin, J.R., Kolsbjerg, E.L., Kubal, J.,
Kaasbjerg, K., Lysgaard, S., Maronsson, J.B., Maxson, T., Olsen, T., Pastewka,
L., Peterson, A., Rostgaard, C., Schiøtz, J., Schütt, O., Strange, M., Thyge-
sen, K.S., Vegge, T., Vilhelmsen, L., Walter, M., Zeng, Z., Jacobsen, K.W.: The
atomic simulation environment—a python library for working with atoms. J.
| Phys. Condens. | Matter | 29(27), 273002 | (2017) |     |
| -------------- | ------ | -------------- | ------ | --- |
[76] Kresse, G., Gil, A., Sautet, P.: Significance of single-electron energies for the
| description | of co on pt(111). | Phys. Rev. | B 68, 073401 | (2003) |
| ----------- | ----------------- | ---------- | ------------ | ------ |
[77] Blyholder, G.: Molecular orbital view of chemisorbed carbon monoxide. J. Phys.
| Chem.          | 68(10), 2772–2777 | (1964)                              |     |     |
| -------------- | ----------------- | ----------------------------------- | --- | --- |
| [78] LangChain | Inc.: LangGraph.  | https://www.langchain.com/langgraph |     |     |
[79] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.:
React: Synergizing reasoning and acting in language models. arXiv preprint
| arXiv:2210.03629v3 | (2022) |     |     |     |
| ------------------ | ------ | --- | --- | --- |
[80] Jette, M.A., Wickberg, T.: Architecture of the slurm workload manager, 3–23
| (2023). | Springer |     |     |     |
| ------- | -------- | --- | --- | --- |
46

[81] Sholl, D.S., Steckel, J.A.: Density Functional Theory: a Practical Introduction.
John Wiley & Sons, ??? (2022)
[82] Kresse,G.,Hafner,J.:Abinitiomoleculardynamicsforliquidmetals.Phys.Rev.
B 47, 558–561 (1993)
[83] Frisch, M.J., Trucks, G.W., Schlegel, H.B., Scuseria, G.E., Robb, M.A., Cheese-
man, J.R., Scalmani, G., Barone, V., Petersson, G.A., Nakatsuji, H., Li, X.,
Caricato,M.,Marenich,A.V.,Bloino,J.,Janesko,B.G.,Gomperts,R.,Mennucci,
B., Hratchian, H.P., Ortiz, J.V., Izmaylov, A.F., Sonnenberg, J.L., Williams-
Young, D., Ding, F., Lipparini, F., Egidi, F., Goings, J., Peng, B., Petrone, A.,
Henderson, T., Ranasinghe, D., Zakrzewski, V.G., Gao, J., Rega, N., Zheng, G.,
Liang, W., Hada, M., Ehara, M., Toyota, K., Fukuda, R., Hasegawa, J., Ishida,
M., Nakajima, T., Honda, Y., Kitao, O., Nakai, H., Vreven, T., Throssell, K.,
Montgomery, J.A. Jr., Peralta, J.E., Ogliaro, F., Bearpark, M.J., Heyd, J.J.,
Brothers, E.N., Kudin,K.N., Staroverov,V.N., Keith,T.A.,Kobayashi,R., Nor-
mand, J., Raghavachari, K., Rendell, A.P., Burant, J.C., Iyengar, S.S., Tomasi,
J., Cossi, M., Millam, J.M., Klene, M., Adamo, C., Cammi, R., Ochterski, J.W.,
Martin,R.L.,Morokuma,K.,Farkas,O.,Foresman,J.B.,Fox,D.J.:Gaussian~16
Revision C.01. Gaussian Inc. Wallingford CT (2016)
[84] Viswanathan, V., Thygesen, K.S., Hummelshøj, J., Nørskov, J.K., Girishkumar,
G., McCloskey, B., Luntz, A.: Electrical conductivity in li2o2 and its role in
determining capacity limitations in non-aqueous li-o2 batteries. J. Chem. Phys.
135(21), 214704 (2011)
47

Supplementary Information: DREAMS:
Density Functional Theory Based Research
Engine for Agentic Materials Simulation
Ziqi Wang1, Hongshuo Huang1, Hancheng Zhao1,
Changwen Xu1, Shang Zhu1, Jan Janssen3*,
Venkatasubramanian Viswanathan1,2*
1Department of Mechanical Engineering, University of Michigan.
2Department of Aerospace Engineering, University of Michigan.
3Materials Informatics, Max-Planck-Institute for Sustainable Materials.
*Corresponding author(s). E-mail(s): janssen@mpi-susmat.de;
venkvis@umich.edu;
1

1 Plan generated for the Sol27LC challenge
The initial full plan generated by the supervisor for the BCC-Li run, created imme-
diately after a single consultation step with the DFT agent. Under the safety-guard
framework,everyplanstepnamestheworkeragentresponsible,thetoolwhosesuc-
cessfulcallthesteprequires,and,forreportsteps,thequantitiestheresultingreport
must deliver; the plan is subsequently edited dynamically (steps inserted, modified,
ordeleted)astherunproceeds.Inthisruntheplanexecutedwithoutrevision.
1. Create BCC Li bulk structure with initial lattice constant guess (∼3.49 Å)
(DFT_Agent;init_structure_data_for_none_adsorption_calculations)
2. Find pseudopotential for Li using PBE functional (DFT_Agent;
find_pseudopotential)
3. Write SCF template with tight initial DFT parameters for convergence tests
(DFT_Agent;write_QE_script_w_ASE)
4. Generate ecutwfc convergence test input files (DFT_Agent;
generate_convergence_test)
5. Add resource suggestions for ecutwfc convergence test jobs (HPC_Agent;
add_resource_suggestion)
6. Submit and monitor ecutwfc convergence test jobs (HPC_Agent;
submit_and_monitor_job)
7. Determine optimal ecutwfc from convergence test results (DFT_Agent;
find_optimal_parameter)
8. Generate intermediate report for optimal ecutwfc (DFT_Agent;
generate_structured_report;mustreport:optimal_ecutwfc_Ry)
9. Generate kspacing convergence test input files using optimal ecutwfc
(DFT_Agent;generate_convergence_test)
10. Add resource suggestions for kspacing convergence test jobs (HPC_Agent;
add_resource_suggestion)
11. Submit and monitor kspacing convergence test jobs (HPC_Agent;
submit_and_monitor_job)
12. Determine optimal kspacing from convergence test results (DFT_Agent;
find_optimal_parameter)
13. Generate intermediate report for optimal kspacing (DFT_Agent;
generate_structured_report;mustreport:optimal_kspacing)
14. GenerateEOStestinputfilesusingoptimalecutwfcandkspacing(DFT_Agent;
generate_eos_test)
15. Add resource suggestions for EOS test jobs (HPC_Agent;
add_resource_suggestion)
16. SubmitandmonitorEOStestjobs(HPC_Agent;submit_and_monitor_job)
17. CalculatelatticeconstantfromEOSresults(DFT_Agent;calculate_lc)
18. Generate final report with lattice constant (DFT_Agent;
generate_structured_report;mustreport:lattice_constant_angstrom)
2

| 2 Full Canvas | History | for the | Sol27LC | Challenge |
| ------------- | ------- | ------- | ------- | --------- |
3

| 3 Full results | for | the Sol27LC | challenge |     |     |     |
| -------------- | --- | ----------- | --------- | --- | --- | --- |
Table 1: Comparison of Sol27LC benchmark results from experimental
measurements, DFT calculations by human experts, and DFT calculations
by DREAMS. The Perdew-Burke-Ernzerhof (PBE) exchange-correlation
functional is used for DFT calculations. Errors in DREAMS’ DFT calcula-
tions relative to expert-implemented DFT calculations are presented in the
lastcolumn.
Latticeparameterresults(Å)
| Structure |              |              |        | kpoints | ecutwfc | Error(%) |
| --------- | ------------ | ------------ | ------ | ------- | ------- | -------- |
|           | Experimental | Humanexperts | Agent  |         |         |          |
| Li(BCC)   | 3.451        | 3.4361       | 3.44   | 12      | 40      | 0.1135   |
| Na(BCC)   | 4.209        | 4.1953       | 4.2018 | 6       | 70      | 0.1549   |
| K(BCC)    | 5.212        | 5.2834       | 5.2676 | 8       | 60      | 0.299    |
| Rb(BCC)   | 5.577        | 5.6869       | 5.6475 | 8       | 30      | 0.6928   |
| Ca(FCC)   | 5.556        | 5.5321       | 5.5357 | 8       | 50      | 0.0651   |
| Sr(FCC)   | 6.04         | 6.0434       | 6.0378 | 8       | 40      | 0.0927   |
| Ba(BCC)   | 5.002        | 5.0238       | 5.0148 | 10      | 50      | 0.1791   |
| V(BCC)    | 3.024        | 3.0196       | 2.9996 | 12      | 50      | 0.6623   |
| Nb(BCC)   | 3.294        | 3.3153       | 3.3084 | 12      | 70      | 0.2081   |
| Ta(BCC)   | 3.299        | 3.3345       | 3.3157 | 8       | 70      | 0.5638   |
| Mo(BCC)   | 3.141        | 3.1682       | 3.1589 | 16      | 60      | 0.2935   |
| W(BCC)    | 3.16         | 3.2034       | 3.182  | 8       | 70      | 0.668    |
| Fe(BCC)   | 2.853        | 2.8442       | 2.8399 | 16      | 60      | 0.1512   |
| Rh(FCC)   | 3.793        | 3.855        | 3.823  | 10      | 60      | 0.8301   |
| Ir(FCC)   | 3.831        | 3.8907       | 3.8636 | 10      | 70      | 0.6965   |
| Ni(FCC)   | 3.508        | 3.524        | 3.5155 | 8       | 60      | 0.2412   |
| Pd(FCC)   | 3.876        | 3.9474       | 3.926  | 18      | 40      | 0.5421   |
| Pt(FCC)   | 3.913        | 3.982        | 3.956  | 8       | 70      | 0.6529   |
| Cu(FCC)   | 3.596        | 3.6516       | 3.6213 | 10      | 70      | 0.8298   |
| Ag(FCC)   | 4.062        | 4.1561       | 4.1258 | 18      | 50      | 0.729    |
| Au(FCC)   | 4.062        | 4.169        | 4.1329 | 8       | 70      | 0.8659   |
| Al(FCC)   | 4.019        | 4.0425       | 4.0333 | 18      | 30      | 0.2276   |
| Pb(FCC)   | 4.912        | 5.0467       | 5.0258 | 14      | 70      | 0.4141   |
| C(dia)    | 3.544        | 3.5729       | 3.5562 | 8       | 70      | 0.4674   |
| Si(dia)   | 5.415        | 5.4758       | 5.4392 | 6       | 40      | 0.6684   |
| Ge(dia)   | 5.639        | 5.7656       | 5.6902 | 6       | 70      | 1.3078   |
| Sn(dia)   | 6.474        | 6.6582       | 6.553  | 6       | 70      | 1.58     |
4

4 Plan generated for the CO/Pt(111) challenge
TheinitialfullplangeneratedbythesupervisorfortheCO/Pt(111)run,createdimme-
diately after a single consultation step with the DFT agent. As in the Sol27LC plan,
each step names its worker agent, its required tool, and, for report steps, the quan-
tities the report must deliver. This initial plan was subsequently revised repeatedly
during the run (see the main text): among others, the ecutwfc report was deferred
after the deterministic tool refusal, an extended ecutwfc test was inserted following
thereportjudge’swarning,thek-pointandslab-thicknesstestswereregeneratedat
thenewcutoff,and,afterthereportjudgefailedthefirstfinalreportovertheunchar-
acterized vacuum spacing, a vacuum convergence test and a regenerated round of
productioncalculationswereinserted.
1. Generate Pt(111) slab structure with p(2x2) supercell and initial struc-
tural parameters, and find PBE pseudopotentials for Pt, C, O (DFT_Agent;
find_pseudopotential)
2. GenerateisolatedCOmoleculestructureandaddittofccsitewith0◦orientation
forconvergencetesting(DFT_Agent;add_myAdsorbate)
3. Generate ecutwfc convergence test input files for CO on fcc site using PBE
pseudopotentials(DFT_Agent;generate_convergence_test)
4. Add resource suggestions and submit ecutwfc convergence test jobs to HPC
(HPC_Agent;submit_and_monitor_job)
5. Determine optimal ecutwfc from convergence test results (DFT_Agent;
find_optimal_parameter)
6. Generate intermediate report certifying optimal ecutwfc (DFT_Agent;
generate_structured_report;mustreport:optimal_ecutwfc_Ry)
7. GeneratekspacingconvergencetestinputfilesforCOonfccsiteusingoptimal
ecutwfcandPBEpseudopotentials(DFT_Agent;generate_convergence_test)
8. Add resource suggestions and submit kspacing convergence test jobs to HPC
(HPC_Agent;submit_and_monitor_job)
9. Determine optimal kspacing from convergence test results (DFT_Agent;
find_optimal_parameter)
10. Generate intermediate report certifying optimal kspacing (DFT_Agent;
generate_structured_report;mustreport:optimal_kspacing)
11. Generate structural convergence test (supercell_dim_z) input files for CO on
fccsiteusingoptimalDFTparametersandPBEpseudopotentials(DFT_Agent;
generate_convergence_test)
12. Addresourcesuggestionsandsubmitsupercell_dim_zconvergencetestjobsto
HPC(HPC_Agent;submit_and_monitor_job)
13. Determine optimal supercell_dim_z from derived-quantity convergence test
results(DFT_Agent;find_optimal_parameter_from_derived)
14. Generate intermediate report certifying optimal supercell_dim_z (DFT_Agent;
generate_structured_report;mustreport:optimal_supercell_dim_z)
15. Generate structural convergence test (n_fixed_layers) input files for CO on fcc
site using optimal DFT parameters and optimal supercell_dim_z (DFT_Agent;
generate_convergence_test)
5

16. Add resource suggestions and submit n_fixed_layers convergence test jobs to
HPC(HPC_Agent;submit_and_monitor_job)
17. Determine optimal n_fixed_layers from derived-quantity convergence test
results(DFT_Agent;find_optimal_parameter_from_derived)
18. Generate intermediate report certifying optimal n_fixed_layers (DFT_Agent;
generate_structured_report;mustreport:optimal_n_fixed_layers)
19. Generate production input files for clean Pt(111) slab, isolated CO, and all 6
CO+slab configurations (fcc 0◦/90◦/180◦, ontop 0◦/90◦/180◦) using all optimal
parametersandPBEpseudopotentials(DFT_Agent;write_QE_script_w_ASE)
20. Addresourcesuggestionsandsubmit all production jobsto HPC(HPC_Agent;
submit_and_monitor_job)
21. Calculate adsorption energies for all 6 configurations, identify most favorable
fcc and ontop configurations, and compute the adsorption energy difference
(DFT_Agent;calculate_formation_E)
22. Generate final report certifying all adsorption energies and the final
adsorption energy difference between most favorable fcc and ontop
configurations (DFT_Agent; generate_structured_report; must report:
adsorption_energy_fcc_0deg_eV, adsorption_energy_fcc_90deg_eV,
adsorption_energy_fcc_180deg_eV, adsorption_energy_ontop_0deg_eV,
adsorption_energy_ontop_90deg_eV,adsorption_energy_ontop_180deg_eV,
adsorption_energy_difference_fcc_vs_ontop_eV)
6

| 5 More      | examples |     | of suggestions | from | the |     |     |     |
| ----------- | -------- | --- | -------------- | ---- | --- | --- | --- | --- |
| convergence |          | LLM | agent          |      |     |     |     |     |
Table 2: Representative suggestions made by the convergence LLM agent based
on DFT input files. The agent proposes parameter adjustments such as increasing
the smearing width (degauss) and decreasing the mixing factor (mixing_beta)—to
improveSCFconvergenceinmetallicsystems.Eachsuggestionisaccompaniedby
concise justifications, reflecting practices commonly employed by experienced DFT
users.Theseentriesillustratethetypesofremediesproposedduringthebenchmark
runs;theyarenotafrequencydistributionoracontrolledmeasureofrepeatability.
| Parameters |     | Suggestions |     | Reason |     |     |     |     |
| ---------- | --- | ----------- | --- | ------ | --- | --- | --- | --- |
ecutwfc increaseto80.0 highercutoffneededforultrasoftpseudopo-
tentialswithtransitionmetals
| degauss |     | increaseto0.03 |     | helpswithmetallicsystems |     |     |     |     |
| ------- | --- | -------------- | --- | ------------------------ | --- | --- | --- | --- |
mixing_beta addwithvalue0.3 Thecurrentvalueof0.7istoohighforthis
|     |     |     |     | complex | system with | CO adsorption, |     | lead- |
| --- | --- | --- | --- | ------- | ----------- | -------------- | --- | ----- |
ingtochargesloshing
| mixing_mode |     | local-TF |     | Switching | from plain | mixing | to a | more |
| ----------- | --- | -------- | --- | --------- | ---------- | ------ | ---- | ---- |
sophisticatedschemelikelocal-TFcanhelp
withdifficultconvergencecases
| starting |     | addforPt(0.1) |     | helpsbreaksymmetryfortransitionmetals |     |     |     |     |
| -------- | --- | ------------- | --- | ------------------------------------- | --- | --- | --- | --- |
magnetization
vacuum considerincreasing(cell currentvacuummightbeinsufficientforCO
|     |     | z-dimension) |     | adsorption. |     |     |     |     |
| --- | --- | ------------ | --- | ----------- | --- | --- | --- | --- |
electronmaxstep 300 The calculation stopped at 200 iterations
|     |     |     |     | but was | still making | progress, | so allowing |     |
| --- | --- | --- | --- | ------- | ------------ | --------- | ----------- | --- |
moreiterationsmighthelpitconverge
| conv_thr |     | 1.0e-5 |     | The current   | threshold | (1.0E-06)    | might     | be  |
| -------- | --- | ------ | --- | ------------- | --------- | ------------ | --------- | --- |
|          |     |        |     | unnecessarily | strict    | for geometry | optimiza- |     |
tionsteps;relaxingitinitiallywillhelpreach
convergencefaster
startingwfc atomic+random Using a better initial guess for wavefunc-
tionscanaccelerateconvergence
diagonalization david Explicitly setting the diagonalization algo-
|     |     |     |     | rithm to | david (which | is the    | default) | with |
| --- | --- | --- | --- | -------- | ------------ | --------- | -------- | ---- |
|     |     |     |     | a higher | david_ndim   | parameter | (e.g.,   | 4)   |
mighthelp
| scf_must |     | false |     | For geometry    | optimization,   |         | you can  | allow |
| -------- | --- | ----- | --- | --------------- | --------------- | ------- | -------- | ----- |
| converge |     |       |     | the calculation | to              | proceed | even if  | SCF   |
|          |     |       |     | doesn’t         | fully converge, |         | which is | often |
acceptableduringintermediatesteps.
7

6 Charge density of the CO/Pt(111) system
(a) (b)
(c) (d)
(e) (f)
Fig.1:ChargedensityofCOonthePt(111)surfacefordifferentXCchoice:(a)LDA,
FCCsite;(b)LDA,ontopsite;(c)PBE,FCCsite;(d)PBE,ontopsite;(e)BEEF-vdW,
FCCsite;(f)BEEF-vdW,ontopsite.
8

7 DREAMS Agent Prompts
The complete operational prompts used by the planning supervisor, DFT worker,
convergence-diagnosisagent,andHPCworkerarereproducedbelow.Theplanning-
supervisor and HPC prompts are assembled at runtime from static templates and
the substitution blocks shown here; angle-bracketed labels in the displayed tem-
plates mark those substitutions. The exact, answer-free benchmark objectives are
reproducedinthecorrespondingResultssubsectionsofthemaintext.Theruletexts
and judge guidance used by the safety-guard and report-judge agents are reported
separatelyinSupplementaryInformationS-11.
Planning-supervisor substitutions
<workers> = ["DFT_Agent", "HPC_Agent"]
<worker-options> = ["DFT_Agent", "HPC_Agent"]
<team-capabilities>
<DFT Agent>:
- Answer the supervisor's planning questions about DFT settings,
convergence-test design, structure choices, and any other
domain-specific decisions
- Create intial structure of the system
- Find pseudopotential
- Write initial script
- generate convergence test input files for dft parameters
- determine the best parameters from convergence test result
- generate different structures for structural convergence test
- determine best structure settings from structural convergence test
- generate EOS calculation input files using the best parameters
- generate production run input files
- generate BEEF input files from finished relax calculation
- analyze BEEF result to get uncertainty
- Read output file to get energy
- Calculate lattice constant
- Calculate formation energy
- Generate structured report
<HPC Agent>:
- find job list from the job list file
- Add resource suggestion base on the DFT input file
- Submit job to HPC and report back once all jobs are done
<team-restrictions>
<DFT Agent>:
- Cannot submit job to HPC
<HPC Agent>:
- Cannot determine the best parameters from convergence test result
Planning-supervisor system prompt
<Role>
9

You are a scientist supervisor tasked with managing a conversation
for scientific computing between the following workers: <workers>.
You don't have to use all the members, nor all the capabilities of
the members.
<Objective>
Given the following user request, decide which the member to act
next, and do what
<Instructions>:
0, You will be given the overall objective from the user, a plan
consists of a list of high level steps to achieve the objective,
and a list of past steps that have been done.
1. If the plan is empty, for the given objective, first discuss with
your worker agents to see what they can do and gather their
opinions on approach, then come up with a simple, high level plan
and specify what are the must use tools to finish the steps.
For reference, the team's nominal capabilities are:
<team-capabilities> and restrictions are: <team-restrictions> --
but treat this as a starting hint, not the ground truth. Confirm
with the workers before committing the plan.
You don't have to use all the members, nor all the capabilities
of the members.
This plan should involve individual tasks, that if executed
correctly will yield the correct answer. Do not add any
superfluous steps.
The result of the final step should be the final answer. Make
sure that each step has all the information needed - do not skip
steps.
If you were asked to provide uncertainty information across
different exchange correlation functionals, you can run ensemble
calculation with BEEF-vdW functional and analyze the result.
Otherwise, please use the functional that is consistant with the
psudopotenials.
To run ensemble calculation, with the same functional you need
to first relax the structure, and then for the relaxed structure
of interests, use the BEEF-vdW functional and ensemble
calculation to get the distribution of energies. (do not
generate ensemble calculations for all relaxed structures, only
the ones that are needed for the final answer.)
!!! To calculate adsorption energy, you need to run calculations
with the SAME functional for: relaxed adsorbate, relaxed clean
slab, and relaxed slab with adsorbate !!!
!!! If you are going to use BEEF-vdW functional later you need
to use BEEF-vdW functional for all ealier calculations !!!
In the plan, you need to be clear what pseudopotential to use
when finding pseudopotentials, what functional to use when
generating the input files.
If the plan is not empty, update the plan based on the current
state of the project (check only related information on CANVAS.
10

Do not read through the entire CANVAS).
<WARNING>: Critically evaluate the worker's last step. If the
action matches the task but serves a different objective, or if
extra actions were taken that conflict with the step's intended
purpose, treat the step as incorrect. Revise the plan and
instruct the worker to redo the step for the correct objective.
The framework maintains the plan across turns: you do NOT
re-author the whole plan. You apply edits with the plan-editing
tools (insert/modify/delete steps), and step 1 of the plan is
always what executes next. After editing (or if no edit is
needed), Proceed to run step 1; return Response only when the
whole objective is done. Make sure that each step has all the
information needed - do not skip steps. (Detailed plan-editing
instructions are provided to you at runtime.)
2. Given the conversation above, suggest who should act next. next
could only be selected from: <worker-options>.
3. inspect the CANVAS, extract information needed, then base on what
the agent just did, the info you extracted, and the plan, decide
what to do next.
4. If your end result is genuinely surprising -- outside the user's
margin of error, or in clear conflict with a known reference --
do NOT immediately re-run calculations at random. Instead:
a. Call `debug_artifact_chain` with the surprising artifact's
`result_id` and a specific question (e.g. "why is the
adsorption energy 0.5 eV higher than the literature value
of -1.23 eV?"). The tool returns hypotheses, not
conclusions.
b. Read the synthesis paragraph for the most likely cause(s),
then read the numbered `potential_causes` list.
c. Instruct the worker to investigate ONE potential cause at a
time, in priority order from the synthesis. Vary that single
parameter and re-run the relevant calculation.
d. After the worker reports back, if the cause was ruled out,
call `debug_artifact_chain` AGAIN with the same root and
question, but pass `investigation_history` describing what
was tested and ruled out. Without it, the tool will re-flag
the same suspects.
e. Stop when the cause is found, or when the synthesis says the
surprise may originate outside the value-flow chain. In
that case, examine the input data, physical assumptions,
external benchmark, or the user's expectation before
declaring a problem.
Do not use `debug_artifact_chain` as a first-pass sanity check on
every result -- it is expensive. Use it only when the result is
genuinely surprising. Do not stop until the end result is within
the user-specified margin of error, or you have exhausted both
the chain investigation and the out-of-chain candidates. Only if
the user did not specify a margin of error, you can judge by
yourself.
5. Based on the teams capability: <team-capabilities> and
restrictions: <team-restrictions>, feel free to add more steps
11

to the plan if you want to investigate more or if you think it
is necessary.
6. After a report was generated, a judge will check the report. If
the report does not cleanly pass, the verifier's full feedback is
saved to the canvas under the `JUDGE::<report name>` key named
in the executed-steps history -- read it there with
read_my_canvas before reacting. If there are issues, the worker
did something wrong: reflect on the feedback, adjust the plan
accordingly, and ask the worker to fix the issue. Do not stop
until the judge is satisfied with the report. (You are also
reminded of this at runtime.)
<Requirements>:
1. Use your worker agents as a resource for expert input when facing
decisions that require their domain knowledge. This is necessary
when making or adjusting the plan, especially at the start of
the project.
2. To consult a worker, insert a step at position 1 (the front of
the plan) assigned to that worker; it runs next. Use
insert_plan_steps for this.
3. For the inserted discussion step, directly ask the question --
do not say anything else. The worker will read the question and
answer it, then you can update your plan based on the answer.
4. Do not generate convergence test for all systems and all
configurations.
5. To determine the DFT calculation parameters, please only generate
one batch of convergence test for the most complicated system
using !! ONE !! most complicated configuration.
6. Structural convergence test is only needed for adsorption energy
calculations, where it is essential to make sure the structure
settings like slab thickness and vacuum size are good enough to
get converged adsorption energy. Note: there are two distinct
convergence-test patterns ("single-output" -- one .pwo file per
data point provides the converging quantity; "derived-quantity"
-- the converging quantity is computed by aggregating multiple
DFT jobs per data point).
7. Only work on structure convergence test once you have determined
the best DFT parameters, and make sure to use the best DFT
parameters for the structural convergence test.
8. Do not work on structural convergence test (slab thickness,
vaccum size) and DFT parameter convergence test (k-points, ecut)
at the same time.
9. **Comparison-set consistency.** For any set of comparison-based
result (optimal parameter from a sweep, lattice constant from
EOS, adsorption/formation energy), the underlying input files
must share IDENTICAL settings except for the axis being varied.
Watch for the failure mode where the worker fixed a convergence
problem on ONE file (raised electron_maxstep, changed
mixing_beta, etc.) and reran only that file. If you suspect this
-- or the worker says they re-ran "one file" or "the failing job"
in isolation -- direct them to align settings across all files
in the set and rerun them all before computing the final result.
12

10. The Must-use tools for each step must be a bare minimum, so your
worker can have more degree of freedom.
11. A structured report must be generated once any numerical claim
was made so that claim could be verified by the judge, together
with a final report. You need to read the feedback from the
judge, and if there are any issues, reflect on the feedback,
adjust the plan accordingly, create more steps and ask the
worker agent try to fix the issue.
12. Whenever you create a step whose `required_tools` is
`generate_structured_report`, you MUST also populate that step's
`required_quantities` field with the exact, specific named
quantities that report must certify. Name the quantities
precisely and unambiguously (e.g. `optimal_ecutwfc_Ry`,
`optimal_kspacing`, `optimal_n_fixed_layers`,
`adsorption_energy_difference_fcc_vs_ontop_eV`). For all
non-report steps, leave `required_quantities` empty.
<Reading verifier output (`verify_structured_report`)>
======================================================
This output is not shown to you inline. When a report does not cleanly
pass, it is saved to the canvas under the `JUDGE::<report name>` key
named in the executed-steps history; fetch it with read_my_canvas, then
read it using the structure below.
Top-level fields: `overall_verdict`, `n_fails`, `n_warnings`, `summary`,
`issues` (numbered, your primary surface), plus `checked_result_ids` and
`artifact_results` for diagnostic tooling.
Each issue has: `issue_number`, `category`, `severity`, `where`
(structured location with keys like claim_name / result_id / tool_name /
parameter), `context_at_site` (the `Context:` line the worker wrote at
the offending site -- read it to see how the agent FRAMED the call),
`problem` (one-line description), `judge_reasoning` (the judge's full
reasoning), and `remediation_options` (legitimate fix paths; some entries
warn against WRONG fixes -- do not skip those warnings).
Two cross-cutting rules:
(1) DO NOT instruct the worker to "find a result_id and patch it in"
for UNSOURCED_SENSITIVE or CROSS_WIRED_SOURCE issues. The
legitimate fix is in the remediation_options -- typically running
an upstream sub-study, declaring the parameter varied, or
correcting the call's context. Patching with any ID that fits
will fail on the next pass as VALUE_MISMATCH_PARAM or
CROSS_WIRED_SOURCE.
(2) When any artifact gets regenerated, every artifact downstream
of it must be re-created using the new result_id. Stale
references silently propagate. Tell the worker explicitly which
downstream calculations to re-run, in dependency order.
13

When multiple issues share a `result_id` or `claim_name`, they may
collapse to a single root cause; address claim-level issues
(VALUE_MISMATCH_CLAIM, SCHEMA_VIOLATION) first since fixing them often
dissolves dependent issues.
<Reading debug output (`debug_artifact_chain`)>
================================================
Top-level fields: `investigation_question`, `root_result_id`,
`n_potential_causes`, `summary`, `potential_causes` (numbered, your
primary surface), `synthesis` (one-paragraph diagnostic with a fixed
disclaimer prefix), `budget_exceeded` (if true, raise max_judge_calls
and re-call).
CRITICAL: debug-tool output is HYPOTHESES, not conclusions. Confirming
a hypothesis requires actually changing the parameter and re-running.
Framing is "investigate" and "test", not "fix". Do not omit the
synthesis disclaimer when relaying findings to the worker.
Each `potential_cause` has the same field shape as a verifier issue.
Two categories:
- parameter_value_suspect -- investigate by re-running with this
parameter varied.
- source_suspect -- investigate the upstream source artifact
named in `where.source_result_id`; re-call
`debug_artifact_chain` with that upstream
result_id as the new root.
Two rules:
(1) Vary ONE parameter at a time in priority order from the
synthesis. Varying multiple at once makes attribution impossible.
(2) On follow-up debug calls, ALWAYS pass `investigation_history`
describing what was tested and ruled out, in prose.
When `n_potential_causes` is 0: read the synthesis. The chain has been
exhausted; investigate input data, physical assumptions, external
benchmark, or the user's expectation.
<Final Note>
When the worker raises a request or suggestion, do not ignore it.
Evaluate whether it is valid in the context of the overall objective;
if it is, update the plan to accommodate it and guide the worker through
the change.
At least 2 report must be generated during the project, one in the
middle of the project to summarize the progress and one at the end of
the project to summarize the final result.
Report-bounded spans of history that did not cleanly pass may be offered
to you at runtime as "compression opportunities"; you may compress them
with compress_history to shorten the running history. This is
14

non-destructive -- the full detail is archived to the canvas and remains
readable.
DFT-worker system prompt
<Role>:
You are a very powerful and yet obedient assistant that performs
density functional theory calculations and working in a team. You
do exactly what you are told to do.
You and your team members has a shared CANVAS to record and share
all the intermediate results.
Please strickly follow the tasks given, do not do anything else.
<Objective>:
You are responsible for generating the quantum espresso input file
for the given material and parameter setting with provided tools.
You can only respond with a single complete 'Thought, Action' format
OR a single 'Intermediate Answer' format.
Please strickly follow the tasks given, do not do anything else.
<Your Capability>: (Only do what you are told to do)
inspect and read the CANVAS with suitable tools to see what's
available.
create valid input structure for the system of interest with the
right tool.
Find the correct pseduopotential filename using the tool provided
(do not report the absolute path).
Generate the quantum espresso input file with proper ASE tool. Pay
attention to calculation type and funtional choice.
Always generate conventional cell with ibrav=0 and do not use celldm
and angstrom at the same time.
If the system involves hubbard U correction, specify starting
magnetization in SYSTEM card and hubbard U parameters in HUBBARD
card, and use the pre-defined hubbard correction tool.
Save all the files in pwi format and into job list and report to
supervisor to let HPC Agent to submit the job.
generate convergence test scripts with a tool.
determine the most optimal settings based on the convergence test.
calculate lattice constant and formation energy based on the DFT
calculation.
remember to record the results and critical informations in the
CANVAS with the right tool.
<Requirements>:
# Workflow & response shape
0. When asked a question, think about it carefully, scientifically,
and critically before replying. Draw on your domain expertise;
do not rush a casual answer. Then write down your detailed answer
in the CANVAS.
1. Always inspect and read the CANVAS with suitable tools to see
what's available before acting.
2. Use only the tools necessary for the task. You don't have to use
all the tools provided. Never compute values yourself -- call the
math tool instead.
15

3. When using a tool, always fill in the context and reasons fields
first.
4. Once you're done with the assigned task, report back to the
supervisor and stop immediately. Do not conduct any inference or
post-processing on the result, and do not suggest what to do
next.
4a. Recording on CANVAS: use `write_progress_note` to create a
multi-section progress note, `version_controlled_edit_canvas_doc`
to revise an existing note, and `write_my_canvas` only for short
factual entries (it requires you to declare
`is_free_handed_progress_note`).
4b. After you call `generate_structured_report`, your computation/
extraction/submission tools become unavailable -- only canvas
tools remain. Write your summary/notes and return to the
supervisor; do not attempt further calculations on the report's
values.
4c. The math and extraction tools verify each value as it is
created; if you get a `MATH_GUARD_FAILED` or
`EXTRACTION_GUARD_FAILED`, the fix is to correct the upstream
source or clarify your `context`/`reasons` -- not to blindly
retry.
5. Response format:
- On success: respond with the tool message and a short summary
of what was done. If this is the final answer, prefix with
'Intermediate Answer'. The final answer should be a concise
summary in a sentence -- do not repeat what's already on the
CANVAS, just mention it's there.
- On error: respond with 'Job failed' followed by the error
message. Nothing else.
# File & path conventions
6. QE input files are in .pwi format; output files are .pwo (the
engine appends .pwo to the input filename).
7. Never report absolute paths.
# Scientific defaults
8. Electron conv_thr is 1e-6.
9. Use the smearing appropriate to the material.
10. For production runs, use the optimal parameters from convergence
tests and the converged structures from relaxations.
11. When calculating formation/adsorption energies, run
DFT-parameter convergence tests on ONE representative system
that includes both the adsorbate and the surface -- not
separately on each subsystem.
12. If a job has an issue (didn't converge or accuracy looks off),
use the right tool to get suggestions on how to modify the input
file to fix the issue.
# Provenance & rationale (verifier-facing -- read carefully)
13. When asked to provide a ref_id, that id is the result_id of a
past tool call whose output (or, via dotted addressing -- see
16

`list_referenceable_inputs` -- whose input parameter) is the
source of the value you're passing here. A bare 8-character id
references the past tool call's output;
`<8-char-id>.<param_name>` references one of that call's input
parameters.
14. Many tools in this framework accept a context parameter
alongside a reasons parameter, and rely on you to populate both
thoughtfully. context is 1-2 sentence describing which study or
exploration the entire tool call is part of (e.g. "convergence
test for ecutwfc," "production run for the adsorption energy
calculation," "sensitivity sweep over n_fixed_layers,"
"one-off check"). It is set once per call and is merged into
every parameter's rationale at registration time, so you do not
need to repeat it inside reasons. reasons covers the
per-parameter justification: for each parameter, write 2--3
sentences explaining (a) the role this parameter plays in the
study you named in context (e.g. "being varied now to
characterize convergence," "fixed at the converged value from
the prior convergence test," "inherited from the upstream
relaxation,"); and (b) why this specific value was chosen --
how you arrived at it, what evidence supports it, and the
expected effect on the output. Together, context and reasons
should let an outside reviewer understand both the immediate
purpose of the call and how it serves the overall study goal.
Skipping context, or writing reasons that only describe effect
without identifying each parameter's role, will be rejected by
the verifier even when the underlying science is sound.
15. If some results are at question, adjust the settings and re-run
the tool and see the result. NEVER EVER determine the results
yourself!
# Convergence test design
16. Do not generate convergence tests for every system and every
configuration -- tests run on representative cases only.
17. **Convergence tests come in two flavors. Know which one applies,
and execute accordingly.**
Two criteria distinguish them:
(a) Converging quantity:
- Single-output: the converging quantity is the energy of
ONE .pwo file per data point (e.g. ecutwfc convergence on
bulk total energy; vacuum-size convergence on clean-slab
energy).
- Derived-quantity: the converging quantity requires
aggregating MULTIPLE DFT calculations per data point
(e.g. adsorption-energy convergence over slab thickness
-- each data point's Eads needs three DFT jobs).
(b) Sweeping axis:
- DFT parameter (ecutwfc, kspacing, etc): structure stays
fixed; vary via `generate_convergence_test` with the
parameter name.
- Structural parameter (n_fixed_layers, vacuum,
17

supercell_dim_z): generate N structures along the axis
first via `generateSurface_and_getPossibleSite`, then vary
via `generate_convergence_test` with
`varying_parameter_name="inputAtomsDir"` and
`varying_structural_parameter_name` set to the axis name.
For a given study think about carefully and scientifically what
kind of convergence test is needed.
18. typically 1e-3 or 0.001 eV or 0.001 eV/atom is a good
convergence criterion for energy. But you need to think about it
carefully and scientifically for the specific system you're
working on, and provide justification in the CANVAS.
19. For single-output convergence tests, the template must be 1-to-1
with the intended varying parameter -- e.g.
`ecutw_template.pwi`, `kspacing_template.pwi` -- and the
calculation type must be scf. For single-output DFT-parameter
convergence specifically, run only ONE batch on the most
complicated system using the most complicated configuration;
do not duplicate across configurations. For derived-quantity
convergence tests, use the appropriate template per calculation
type (relax or scf) in the chosen workflow.
20. **COMPARISON-SET CONSISTENCY.** When you generate or modify files
that will be COMPARED (convergence tests, EOS scans, adsorption/
formation calculations), every file must use IDENTICAL settings
except for the one axis being varied. If you change ANY setting
on one file in the set (electron_maxstep, mixing_beta, conv_thr,
smearing, k-points, cell, etc.), apply the SAME change to every
other file in the set and rerun them all. Fixing one file in
isolation silently invalidates the comparison -- even if every
file converges individually.
Convergence-diagnosis prompts
Theconvergenceagentreceivesthefollowingsystemprompt:
You are a DFT expert who's good at giving suggestions on how to solve
convergence issues. You will be given a filename. Read only that file
and provide feedback base on that file only. Do not try to read any
other files.
The input file will end with .pwi, the output file will end with
.pwi.pwo
If you were given a input file, try to figure out why the job didn't
converge base on the input file.
If you were given a output file, try to figure out why the job didn't
converge base on the output file.
If you were given a log file, try to figure out why the job didn't
converge base on the log file.
If you were given a err file, try to figure out why the job didn't
converge base on the err file.
DO NOT READ ANY OTHER FILES!!!
You don't have abilities to do anything else or fix anything.
18

| Please | strickly | follow | the | tasks | given, | do not | do anything | else. |     |
| ------ | -------- | ------ | --- | ----- | ------ | ------ | ----------- | ----- | --- |
Foreachrelevantjobfile,thetoolsuppliesthefollowinguserprompt,with<content>
replacedbythatfile’scontents:
Here is the content of the file <content>, please give me suggestions on
| how to     | fix the | convergence   |     | issue. |     |     |     |     |     |
| ---------- | ------- | ------------- | --- | ------ | --- | --- | --- | --- | --- |
| HPC-worker |         | substitutions |     |        |     |     |     |     |     |
<HPC-resource-description>
| Artemis | by the | Numbers |     |     |     |     |      |     |     |
| ------- | ------ | ------- | --- | --- | --- | --- | ---- | --- | --- |
| Node    | #      | CPU     |     | GPU | RAM |     | Disk | $   |     |
-----------------------------------------------------------
| H100     | 3   | AMD 9654 |     | 4x H100 | SXM 768 | GB  | 1.9 TB | 117,950 |     |
| -------- | --- | -------- | --- | ------- | ------- | --- | ------ | ------- | --- |
| A100     | 2   | AMD 7513 |     | 4x A100 | SXM 512 | GB  | 1.6 TB | 58,597  |     |
| Largemem | 3   | AMD 9654 |     |         | 768     | GB  | 1.9 TB | 13,989  |     |
| CPU      | 25  | AMD 9654 |     |         | 368     | GB  | 1.9 TB | 12,998  |     |
CPU Specifications
----------------------------------------------
| CPU      |      |     | Cores | Threads | Base | Boost    |           |       | L3 Cache |
| -------- | ---- | --- | ----- | ------- | ---- | -------- | --------- | ----- | -------- |
| AMD Epyc | 9654 | CPU | 96    | 192     | 2.6  | GHz 3.55 | GHz (All  | Core) | 384 MB   |
| AMD Epyc | 7513 | CPU | 32    | 64      | 2.6  | GHz 3.65 | GHz (Max) |       | 128 MB   |
*Nodes are partitioned by threads, not cores. Picking 1 or a multiple of
| 2 is advisable; |     | see | sbatch's | --distribution |     | flag. |     |     |     |
| --------------- | --- | --- | -------- | -------------- | --- | ----- | --- | --- | --- |
GPU Specifications
-------------------------------------------------
| GPU             | VRAM       | GPU      | Mem       | Bandwidth       | FP64     | FP64 | TC FP32          | - TC   | BF16 TC |
| --------------- | ---------- | -------- | --------- | --------------- | -------- | ---- | ---------------- | ------ | ------- |
| A100 SXM        | 80         | GB 2,039 | GB/s      |                 | 9.7      | 19.5 | 156              |        | 312     |
| H100 SXM        | 80         | GB 3.34  | TB/s      |                 | 34       | 67   | 989              |        | 1989    |
| *FLOPs          | are listed | in       | teraFLOPs | (10^12          | floating |      | point operations |        | per     |
| second).        | Tensor     | Cores    | (TC)      | are specialized |          | for  | general          | matrix |         |
| multiplications |            | (GEMM).  |           |                 |          |      |                  |        |         |
Partitions
-----------------------------------------------------------
| Partition        |     | Nodes |     | Max | Wall | Time Priority |     | Max | Jobs Max Nodes |
| ---------------- | --- | ----- | --- | --- | ---- | ------------- | --- | --- | -------------- |
| venkvis-cpu      |     | CPU   |     | 48  | hrs  |               |     |     |                |
| venkvis-largemem |     | Large | Mem | 48  | hrs  |               |     |     |                |
| venkvis-a100     |     | A100  |     | 8   | hrs  |               |     |     |                |
| venkvis-h100     |     | H100  |     | 8   | hrs  |               |     |     |                |
<QE-submission-example>
export OMP_NUM_THREADS=1
19

spack load quantum-espresso@7.2
echo "Job started on `hostname` at `date`"
mpirun pw.x -i [input_script_name.pwi] > [input_script_name.pwi].pwo
echo " "
echo "Job Ended at `date`"
HPC-worker system prompt
<Role>:
You are a very powerful high performance computing expert that runs
calculations on the supercomputer, but don't know current events.
Your only job is to conduct the calculations on the supercomputer,
and then report the result once the calculation is done.
You and your team members has a shared CANVAS to record and share all
the intermediate results.
Please strickly follow the tasks given, do not do anything else.
<Objective>:
You are responsible for determining, for each job, how much
resources to request and which partition to submit the job to.
You need to make sure that the calculations are running smoothly and
efficiently.
You can only respond with a single complete 'Thought, Action' format
OR a single 'Intermediate Answer' format.
<Instructions>:
1. always inspect and read the CANVAS with suitable tools to see
what's available. i.e. you can find what jobs to run from the
CANVAS with the right key.
2. Use the right tool to read one quantum espresso input file from
the working directory and, one job by one job, determinie how
much resources to request, which partition to submit that job to,
and what would be the submission scipt based on the resources
info <HPC-resource-description>. Make sure that number of cores
needed (ntasks) equals to number of atoms in the system.
3. Using the right tool, add the suggested resources to a json file
and save it to the working directory.
4. repeat the process until all resource suggestions are created.
5. Use appropriate tool to submit all the jobs in the job_list.json
to the supercomputer based on the suggested resource. here's an
example submission script for quantum espresso
<QE-submission-example>
6. Once all the jobs are done, report result to the supervisor and
stop immediately.
7. remember to record the results and critical informations in the
CANVAS with the right tool.
<Requirements>:
1. follow the instruction strictly, do not do anything else.
2. If everything is good, only response with a short summary of what
has been done.
20

| 3. If error | occur,     | only     | response | with      | 'Job    | failed'  | + error | message. |
| ----------- | ---------- | -------- | -------- | --------- | ------- | -------- | ------- | -------- |
| Do not      | say        | anything | else.    |           |         |          |         |          |
| 4. After    | you obtain |          | list of  | jobs to   | submit, | you must | first   | add the  |
| suggested   | resources  |          | to a     | json file | and     | save it  | to the  | working  |
directory.
| 5. DO NOT | conduct | any | inferenece | on  | the result | or  | conduct | any |
| --------- | ------- | --- | ---------- | --- | ---------- | --- | ------- | --- |
post-processing.
| 6. Do not     | give    | further   | suggestions |                                      | on what           | to do   | next.     |           |
| ------------- | ------- | --------- | ----------- | ------------------------------------ | ----------------- | ------- | --------- | --------- |
| 7. Never      | do math | yourself. |             | Call the                             | math tool         | instead |           |           |
| 8. Recording  | on      | CANVAS:   | use         | `write_progress_note`                |                   |         | to create | a         |
| multi-section |         | progress  | note,       | `version_controlled_edit_canvas_doc` |                   |         |           |           |
| to revise     | an      | existing  | note,       | and                                  | `write_my_canvas` |         | only      | for short |
| factual       | entries | (it       | requires    | you                                  | to declare        |         |           |           |
`is_free_handed_progress_note`).
21

8 List of tools provided
ToolsavailabletotheDFTagentarelistedbelow.Underthesafety-guardframework,
guarded tools share a common interface in addition to their scientific arguments: a
declared context stating which study the call belongs to, one reason per parame-
ter,andprovenancereferences,suppliedeitherasoptional<param>_refarguments
(an 8-character result_id or a dotted <id>.<param> reference) or as mandatory
(value, source_result_id) pairs for high-stakes inputs, written _w_ref below.
Thesesharedargumentsareomittedfromtheper-toolargumentlistings;eachentry
instead ends with a guard line naming the gates that wrap the call and the optional
references it accepts. All gates run after the deterministic reference checks and
beforeanyfileI/O.
inspect_my_canvas
description:Inspecttheworkingcanvasandreturntheavailablekeys.
arguments:
Noargumentneeded
guard:none
write_my_canvas
description: Write a new value to the canvas, intended for short factual
entries, identifiers, structured data, and intermediate results. Create-only by
default: existing keys are not overwritten unless requested, and version-
controlled documents are never overwritten. The caller must declare whether
the content is a free-hand progress note; declared notes are redirected to
write_progress_note,andacontentheuristicbackstopsfalsedeclarations.
arguments:
key: canvas key; must not end in _v<N>, which is reserved for the version
system
value:valuetowrite
is_free_handed_progress_note: whether the content is a free-hand
progressnote
overwrite:overwriteanexistingkey(defaultFalse)
guard:none;deterministicprogress-noterouting
read_my_canvas
description:Readavaluefromtheworkingcanvasbyexactkey.
arguments:
key:exactkeytoread
guard:none
version_controlled_edit_canvas_doc
description: Revise an existing text document on the canvas without rewriting
it: reads the latest version, applies the edits in order, and stores the result as
thenext_v<N>version.Previousversionsarenevermodified,andeitheralledits
22

succeed or none are applied. Structured reports are immutable and cannot be
edited.
arguments:
name:canvaskeyofthedocumenttorevise
edits:listofeditoperationsappliedinorder,eachreplacinganexactunique
snippetorappendingtext
guard:none;all-or-nothingeditapplication
write_progress_note
description: Create a new structured progress note on the canvas with a title,
an overview, optional fixed- and swept-parameter blocks, free-form sections,
next steps, and status items. Notes are create-only; revisions go through
version_controlled_edit_canvas_doc. Every cited reference is checked
againsttheartifactregistry,andanunknownidentifierrejectsthewholenote.
arguments:
name:freshcanvaskeyforthenewnote
title:notetitle
purpose:one-paragraphoverviewofwhatthenoterecordsandwhy
sections:free-formsections,eachwithaheadingandbody(defaultempty)
next_steps:next-stepitems,eachwithastatus(defaultempty)
status:closingstatussummaryitems(defaultempty)
references: named references to registered artifacts, existence-checked
(defaultempty)
fixed_parameters:optionalparametersheldconstant
swept_parameter: optional description of the varied parameter, its range,
andthreshold
guard:none;deterministicregistrycheckonallcitedreferences
calculate_formation_E
description: Compute the adsorption (formation) energy from the clean-slab,
isolated-adsorbate,andslab-with-adsorbatecalculationoutputs,andregisterthe
result. All three inputs require source references, which are verified determinis-
ticallybeforethegatesrun.
arguments:
slabFilePath_w_ref:clean-slabcalculationoutput
adsorbateFilePath_w_ref:isolated-adsorbatecalculationoutput
systemFilePath_w_ref:slab-with-adsorbatecalculationoutput
guard:per-parameterandcross-parametergates
generateSurface_and_getPossibleSite
description: Generate a clean slab surface, save it in traj format, and return
the available adsorption sites; each site and the surface path are registered
as artifacts. Structural parameters may be explored without references, but the
outputsupportsproductionuseonlywhentheirsourcesaresupplied.
arguments:
23

species:elementsymbol
crystal_structures:crystalstructureofthespecies
facets:surfacefacettogenerate
supercell_dim_xy:repeatsoftheprimitivecellinthexyplane
supercell_dim_z:repeatsoftheprimitivecellinz(slabthickness)
n_fixed_layers:numberoffixedslablayers
vacuum:vacuumsizeinÅ
surfaceFilename:nameofthetrajfiletosave
guard: per-parameter gate; accepts supercell_dim_z_ref,
n_fixed_layers_ref,vacuum_ref
generate_myAdsorbate
description: Generate an adsorbate structure from element symbols and
atomicpositions,centeritinvacuum,andsaveitasatrajfile;thesavedpathis
registered.
arguments:
symbols:elementsymbolsoftheadsorbate
positions:atomicpositionsinsymbolorder
AdsorbateFileName:nameofthetrajfiletosave
vaccum:vacuumsizeinÅaroundtheadsorbate
guard:per-parametergate
add_myAdsorbate
description: Place an adsorbate on a surface structure at a given site with a
given rotation, with the adsorption height estimated automatically, and save the
combinedstructure;thesavedpathisregistered.
arguments:
mySurfacePath:pathtothesurfacestructure
adsorbatePath:pathtotheadsorbatestructure
mySites:adsorptionsitecoordinates
rotations:adsorbaterotationangleandaxis
surfaceWithAdsorbateFileName:filenameforthecombinedstructure
guard:per-parametergate;acceptsmySites_ref
init_structure_data_for_none_adsorption_calculations
description: Create a single-element bulk structure from the element,
lattice type, and lattice constants, save it to the working direc-
tory, and register the path. Not for adsorption studies, which require
generateSurface_and_getPossibleSite.
arguments:
element:elementsymbol
lattice: lattice type, one of sc, fcc, bcc, tetragonal, bct,
hcp, rhombohedral, orthorhombic, mcl, diamond, zincblende,
rocksalt, cesiumchloride, fluorite, wurtzite
a:latticeconstant
24

b:latticeconstant(optional;ifonlyaandbaregiven,bisinterpretedasc)
c:latticeconstant(optional)
guard:per-parametergate
find_pseudopotential
description: Return the pseudopotential file(s) available for a given element;
eachmatchingfileisregisteredasanartifact.
arguments:
element:elementsymbol
guard:none
write_QE_script_w_ASE
description:WriteaQuantumESPRESSOinputscriptviaASEfromastructure
file and a full DFT parameterization; the k-point grid is computed from the k-
spacing.Ready-to-runjobsarequeuedforsubmissionwhiletemplatesareheld
separately,andtemplatecutoffsarejudgedassweeppointsratherthanrequiring
upstreamprovenance;productionrunsmustsupplytraceablereferences.
arguments:
listofElements:distinctelementsymbolsintheunitcell
ppfiles_w_ref:pseudopotentialfileperelement,inelementorder
filename:QEinputfilename
inputAtomsDir_w_ref:inputstructurefileorupstreamjobname
calculation:scf,relax,orensemble
restart_mode:from_scratchorrestart
prefix:prefixforoutputfiles
disk_io:diskI/Olevel
ibrav:Bravais-latticeindex
ecutwfc:wavefunctioncutoff(Ry)
ecutrho:charge-densitycutoff(Ry)
occupations:occupationtype
smearing:smearingtype
degauss:Gaussianspreading(Ry)forBrillouin-zoneintegration
conv_thr:SCFconvergencethreshold
electron_maxstep:maximumSCFiterations
kspacing:k-pointspacing(Å−1)
input_dft:LDA,PBE,orBEEF-vdW
ensembleCalculation:whetherthisisanensemblecalculation
ready_to_run_job: whether the job runs directly without modification
(defaultFalse)
additional_input:extraQEparameters(defaultempty)
guard:per-parametergate;acceptsecutwfc_ref,kspacing_ref
25

calculate_lc
description: Read energies and volumes from finished equation-of-state out-
puts, fit an equation of state, and return the equilibrium lattice constant; a
volume–energyplotissavedandthelatticeconstantisregistered.
arguments:
jobFilenames_w_ref:outputfilesusedinthefit
guard:per-parameterandcross-parametergates
generate_convergence_test
description:Fromatemplateinputfile,generateabatchofinputscriptsvarying
one parameter: a numerical parameter (ecutwfc, degauss, or kspacing) on a
fixed structure, or the input structure itself for structural sweeps, with the DFT
parametersinheritedfromthetemplate.Thesweptvaluesmustformagenuine
sweep of at least two distinct values, and structural sweeps must agree on a
singleaxisparameter,verifiedentrybyentry.Thegeneratedjoblistisregistered.
arguments:
input_file_name:templateQEinputfilewhoseparametersareinherited
varying_parameter_name: ecutwfc, degauss, kspacing, or
inputAtomsDir
varying_parameter_values: numerical sweep values, or structure entries
withtheirreferences
guard:per-parametergate,withthesweptparameterjudgedasasweeppoint
find_optimal_parameter
description: From a convergence sweep, select the cheapest value of one
parameter whose energy matches the most-converged reference within the
threshold; the convergence curve is plotted and the chosen value registered. If
onlythereferencesatisfiesthethreshold,thetoolrefusestorecommendavalue
andinstructstheagenttoobtainhigher-accuracyruns.
arguments:
sweeping_parameter:nameofthesweptparameter
filename_w_ref:outputfilepersweeppoint
parameters_w_ref:sweptparametervaluepersweeppoint
reference_file: the most accurate calculation in the list, against which all
othersarecompared
threshold:maximumallowedenergydifferencefromthereference
comparison_mode:absolute(eV)orper_atom(eV/atom)
guard:per-parameterandcross-parametergates
find_optimal_parameter_from_derived
description:Convergenceselectionwheneachdatapointisaderivedquantity
computed from multiple DFT jobs (e.g., an adsorption energy per slab thick-
ness):findsthecheapestaxisvaluewithinthresholdofthereferencepoint.Axis
referencesmustbedotted<id>.<parameter>references,andthetoolwalksthe
provenance graph to confirm the axis source is an ancestor of each data point.
26

Ifonlythereferencepointsatisfiesthethreshold,thetoolrefusestorecommend
avalue.
arguments:
sweeping_parameter:axisparameterbeingcharacterized
data_points_w_refs:derivedquantityperdatapoint
axis_values_w_refs:axisvalueperdatapoint,index-alignedwiththedata
points
reference_ref:referenceofthemost-convergeddatapoint
threshold:maximumalloweddifferencefromthereference
guard: per-parameter and cross-parameter gates; deterministic provenance
chain-walk
generate_eos_test
description: From a template input file with production settings, generate five
equation-of-state jobs with the cell uniformly scaled around the input structure;
eachjobisregisteredandqueuedforsubmission.
arguments:
input_file_name:templateQEinputfilewithproductionsettings
stepSize:cellscalingstep,typically0.025
guard:per-parametergate
read_energy_from_output
description: Read the total energy from each listed job output, reporting non-
converged jobs; each successfully read energy is registered as its own artifact
withtheproducingjobasitsparent.
arguments:
jobFilenames_w_ref:joboutputfilestoread
guard:none;deterministicreferenceverificationonly
get_convergence_suggestions
description: Ask the embedded convergence LLM agent for suggestions on
fixinganon-convergedorinaccuratejobbasedontheinputandoutputfiles;the
suggestions never lower the accuracy of the study, and the suggestion text is
registeredasanartifact.
arguments:
filename:QEinputfileoftheproblematicjob
question:questionaboutthejob,e.g.,whyitdidnotconverge
start_block:blockindexforlongoutputs(default0)
guard:none
analyze_BEEF_result
description: Read BEEF-vdW ensemble outputs for the slab, adsorbate,
and combined system, and register the mean and standard deviation of the
adsorption-energy ensemble together with a histogram plot. Non-ensemble
calculationsarerejected,andallthreesourcereferencesaremandatory.
27

arguments:
slabFilePath_w_ref:slabensemblecalculationoutput
adsorbateFilePath_w_ref:adsorbateensemblecalculationoutput
systemFilePath_w_ref:slab-with-adsorbateensemblecalculationoutput
guard:per-parameterandcross-parametergates
extract_numeric_from_tool_output
description: Verify that a claimed numeric value is explicitly present in an evi-
dence snippet of a prior tool call’s recorded output, then register it as a trusted
numeric artifact. Extraction fails if the snippet is absent, the number is absent,
orthematchisambiguous.
arguments:
source_tool_call_id:result_idofthepriortooloutputtoextractfrom
value:thenumericvaluetoverifyandextract
evidence_snippet:substringofthesourceoutputcontainingthenumber
description:whatthenumberrepresents,includingitsunit
guard:extractiongate
extract_text_from_tool_output
description:Verifythatatextualspanappearsverbatiminanevidencesnippet
of a prior tool call’s output, then register it as a trusted text artifact. Numeric-
shaped strings are refused and directed to the numeric extractor, preventing
numericprovenancefrombeinglaunderedthroughthetextpath.
arguments:
source_tool_call_id:result_idofthepriortooloutputtoextractfrom
text:thetextualspantoverifyandextract;mustappearverbatim
evidence_snippet:substringofthesourcecontainingthespan
description:whatthistextrepresents
guard:extractiongate
math_expression_tool
description: Evaluate a restricted mathematical expression over input val-
ues mapped in order to x ,x ,...; every input must carry a reference and is
0 1
provenance-verifiedbeforeevaluation,andtheresultisregisteredasanartifact.
arguments:
values_w_ref:inputvalues,mappedinordertox ,x ,...
0 1
expression:expressionoverx0, x1, ...,e.g.,(x0 - x1) / x2
guard: math gate, rejecting identity expressions and physically incoherent
combinations
generate_structured_report
description: Build a structured scientific report from numerical claims, each
bound to a registered artifact. Generation fails on a missing study goal, dupli-
cate quantity or report names, a claimed value that does not match its artifact,
28

and, in strict mode, numbers in the prose that are not tied to a claim. The ren-
dered report is registered with all claim artifacts as parents, and its acceptance
isdecidedbythereport-timeverificationdescribedinthemaintext.
arguments:
report_name:uniquenameforthereport
overall_goal:overallgoalofthestudy;requiredandnon-empty
quantity_specs: claims, each with a quantity name, value, artifact refer-
ence,intentionallyvariedparameters,unit,andnote
qualitative_findings:prosefindings(defaultempty)
conclusion:proseconclusion(defaultempty)
strict:strictmodefororphan-numberdetection(defaultTrue)
guard:deterministicchecksinthetool;report-timejudgeonsubmission
list_referenceable_inputs
description:Listthetop-levelinputparameternamesandvaluesofapasttool
call so that a semantically identical value can be cross-referenced downstream
through a dotted <result_id>.<param> reference; not for retrieving outputs,
whicharefoundthroughsearch_artifacts.
arguments:
result_id:8-characterresult_idofthepasttoolcall
guard:none
search_artifacts
description:Findpastartifactsbycontent.Thequerymaybeastring,anumber
matched with tolerance, or a list of terms, and can be combined with per-
category filters over the tool name, arguments, value, description, and context;
upto20resultsarereturnedintimeorder.
arguments:
query:searchterm(string,number,orlistofterms),oromittedtousefilters
only
filters: per-category filters over tool name, arguments, value, description,
andcontext
order:ascendingordescendingbycreationtime
guard:none
29

9 Quantitative Comparison with Existing Agents for
Materials Science
We compare four frameworks on the BCC-Li Sol27LC lattice-constant challenge
and the CO/Pt(111) adsorption challenge: MDCrow [1], ChemGraph [2], DREAMS
without the safety guard, and DREAMS_safe with all guard layers active. These
frameworksusedifferentorchestrationandverificationdesigns,whicharetreatedas
architectural choices rather than as binary indicators of system quality. The quanti-
tative results averaged across independent runs are reported in Table 6 of the main
text;herewedefinethescoringprocedureanddescribetheobservedfailuremodes.
The scores use a fixed checklist of essential steps, rather than the dynami-
cally generated plan or the total number of actions in a run. For each run, the
executed percentage is 100×N /N , and the succeeded percentage is
executed essential
100×N /N .Anessentialstepisexecutedwhentheframeworkcarries
succeeded essential
outtherequiredaction,evenifitdoessoincorrectly;itsucceedsonlywhentheaction
is completed correctly and produces a valid result for the subsequent workflow. The
per-run percentages are averaged across runs and rounded to the precision shown
in the main text. Retries, diagnostic calls, and dynamically added recovery actions
do not change the denominator, and repeating an essential step does not increase
thenumerator.HPCresourceselectionandjobsubmissionandmonitoringareeach
counted once at the end of the checklist, rather than once per calculation batch, so
thatrepeatedHPCoperationsdonotinflatethescores.
The Sol27LC checklist contains 13 essential steps. It comprises construction of
BCC Li from an agent-selected initial lattice constant, selection of a Li pseudopo-
tential, and preparation of the initial DFT input; generation and interpretation of
the ecutwfc convergence calculations; generation and interpretation of the k-point-
spacing convergence calculations; generation of the equation-of-state inputs using
the selected parameters, extraction of the resulting energies, determination of the
equilibrium lattice constant, and comparison with experiment; and, finally, resource
suggestionsandsubmissionandmonitoringoftheproductionjobs.TheCO/Pt(111)
checklistcontains26essentialsteps.Itcomprisesconstructionofthep(2×2)Pt(111)
slab, the FCC-site and ontop-site CO structures at the requested orientations, and
theclean-slabreference;selectionofPt,C,andOpseudopotentialsandpreparation
of an initial DFT input with the correct exchange–correlation functional; generation
andinterpretationofseparateconvergencestudiesforecutwfc,k-pointspacing,slab
thickness, number of fixed layers, and vacuum spacing; preparation of production
inputsfortheFCCstructures,ontopstructures,cleanslab,andisolatedCOmolecule;
extraction of all energies, calculationof the adsorption energies, identificationof the
most favorable configuration at each site, and calculation of their adsorption-energy
difference; and, finally, resource suggestions and submission and monitoring of the
productionjobs.
The short Sol27LC workflow did not distinguish the four frameworks by com-
pletion or accuracy: all four executed and succeeded in all 13 essential steps and
reportedthesameBCC-Lilatticeconstantof3.455Å.DuringadaptationofMDCrow
to the DFT toolset, however, the agent sometimes supplied an input filename and
30

sometimes an output filename to the convergence-analysis tool. The interface was
therefore updated to accept either convention, and the reported MDCrow trials use
thatcompatibleinterface.ChemGraphalsocompletedthechallenge,althoughinone
run a second worker did not recognize that the first worker had already finished the
taskandrepeatedtheentireworkflow.Thesharedcanvaspreventedthislossofcom-
pletion state in DREAMS. DREAMS_safe likewise completed the workflow, but its
verificationmachineryprovidedlittlebenefittothefinalnumericalresultonthisshort
andwell-structuredtask.
The longer CO/Pt(111) workflow exposed qualitatively different limitations.
MDCrow executed only 39% of the 26 essential steps and completed 23% correctly
on average, and no run produced a valid final adsorption-energy difference. Rep-
resentative failures included generating no valid adsorption structures, placing CO
incorrectly on an otherwise valid surface, choosing an excessively dense k-point
sampling,ignoringsubmission-scriptrequirements,attemptingtoselectconvergence
parameters from only one completed calculation or from no successful calculations,
and terminating after reading the first output file. As the active context accumu-
lated,thesingle-agentloopincreasinglylosttrackoftoolcontractsanddependencies
betweenearlierandlatersteps.
ChemGraph improved task decomposition, executing 73% of the essential steps
on average, but only 46% succeeded. Its workers omitted convergence tests or
performedthemonlyafterproductioncalculations,failedtopropagateselectedcon-
vergence parameters to later workers, repeated work, and generated files with
colliding names. Several runs used single-point calculations where structural relax-
ationwasrequiredorusedinconsistentreferenceenergiesintheadsorption-energy
comparison.Inanotherrun,onlythefirstworkercompleteditsconvergencetaskand
subsequent workers stopped because its results were unavailable. Thus, decom-
posing the workflow allowed more actions to be attempted but did not preserve the
shared state needed to execute them consistently. The resulting numerical answers
hadaMAPEof389%andastandarddeviationof0.390eV.
Unguarded DREAMS used its hierarchical orchestration and shared canvas to
executeall26essentialsteps,butonly81%succeeded.Thehistoriesshowwhythe
distinctionbetweenexecutionandsuccessisimportant.InoneLDArun,threeoffour
structural-convergence calculations failed: the four-layer and eight-layer relaxations
did not converge, and the 12 Å vacuum calculation failed after 200 electronic itera-
tions.Nevertheless,theagentdeclaredtheonesurvivingsix-layer,8Åconfiguration
“reasonable” and proceeded without completing the failed comparisons. In a PBE
run, the agent diagnosed the initially failed structural calculations and reran them,
butthencomparedrawtotalenergiesforslabscontainingdifferentnumbersofatoms
and selected an untested six-layer slab as a “compromise” between the four- and
eight-layer cases; it similarly selected a 10 Å vacuum spacing from the 8 and 12 Å
testswithoutestablishingaconvergedtrend.Thefixed-layerchoicewasalsocarried
into production rather than independently converged. These decisions were plausi-
bleenoughtopassthroughanunguardedagentworkflow,buttheydidnotestablish
thestructuralconvergencerequiredbythechecklist.
31

Despite these failures, unguarded DREAMS reported an adsorption-energy dif-
ferencewithin0.2%ofthehuman-expertresult,withastandarddeviationof0.001eV.
Thisclosefinalvaluearosefrompartialcancellationofsystematicerrorsamongthe
adsorbedslabsandtheirreferencecalculationsandthereforedoesnotdemonstrate
that the intermediate workflow was valid. DREAMS_safe prevents this failure mode
by requiring convergence results, parameter choices, and their provenance to pass
verification before they can support production calculations or a final report. It exe-
cuted and succeeded in all 26 essential steps, achieved a MAPE of 0.1% with a
standarddeviationof0.001eV,andproducedafullyverifiedprovenancechain.The
comparison therefore separates two contributions: shared memory and orchestra-
tion enable a long workflow to be completed, whereas the safety guard determines
whethertheapparentlycompletedworkflowisscientificallysupportable.
32

10 Modified prompts for MDCrow and ChemGraph
Both baselines were given the same DFT toolset as DREAMS, and their system
promptswereadjustedonlytomatchtheDFTcontextwhilepreservingeachframe-
work’s original design philosophy. The prompts used in the benchmarks are repro-
ducedverbatimbelow,withthecluster-specificresourcedescriptionandtheexample
Quantum ESPRESSO submission script abbreviated as <HPC-cluster-configs>
and<QE-submission-script>.
MDCrow system prompt
The single-agent prompt, with “molecular dynamics scientist” replaced by the
DFT/HPCroleandtheclusterinformationappended:
You are an expert density functional theory and an HPC scientist, and
your task is to respond to the question or
solve the problem to the best of your ability using
the provided tools. The HPC resources available to you are:
<HPC-cluster-configs>
and a typical Quantum Espresso submission script is:
<QE-submission-script>
You can only respond with a single complete
'Thought, Action, Action Input' format
OR a single 'Final Answer' format.
Complete format:
Thought: (reflect on your progress and decide what to do next)
Action:
```
{{
"action": (the action name, it should be the name of a tool),
"action_input": (the input string for the action)
}}
'''
OR
Final Answer: (the final response to the original input
question, once all steps are complete)
You are required to use the tools provided,
using the most specific tool
available for each action.
Your final answer should contain all information
necessary to answer the question and its subquestions.
Before you finish, reflect on your progress and make
sure you have addressed the question in its entirety.
If you are asked to continue
or reference previous runs,
the context will be provided to you.
If context is provided, you should assume
you are continuing a chat.
Here is the input:
Previous Context: {context}
Question: {input}
33

ChemGraph planner prompt
You are an expert in computational chemistry and the manager responsible
for decomposing user queries into subtasks.
Your task:
- Read the user's input and break it into a list of subtasks.
- Do NOT generate convergence test for all systems and all
configurations.
- Please only generate one batch of convergence test for the most
complicated system using the most complicated configuration.
- Runing ensemble calculation with BEEF-vdW functional and analyze the
result can give you uncertainty information. To run ensemble
calculation, with the same functional you need to first relax the
structure, and then with the relaxed structure, use the BEEF-vdW
functional and ensemble calculation to get the distribution of
energies.
- Each subtask must be independent.
- Include additional details about each simulation based on user's
input. For example, if the user specify a temperature, or pressure,
make sure each subtask has this information.
Return each subtask as a dictionary with:
- `task_index`: a unique integer identifier
- `prompt`: a clear instruction for a worker agent.
Format:
[
{"task_index": 1, "prompt": "Calculate the enthalpy of formation of
carbon monoxide (CO) using mace_mp."},
{"task_index": 2, "prompt": "Calculate the enthalpy of formation of
water (H2O) using mace_mp."},
...
]
Only return the list of subtasks. Do not compute final results. Do not
include reaction calculations.
ChemGraph executor prompt
You are a computational chemistry (DFT and HPC) expert. Your job is to
solve tasks **accurately and only using the available tools**. Never
invent data.
Instructions:
1. **Extract all required inputs** from the user query and previous
tool outputs. These may include:
- File names or loacations
- system specifications (e.g., element, lattice parameters,
orientations)
- Calculation details: method, calculator, temperature, pressure,
etc.
2. **Before calling any tool**, ensure that:
- All required input fields for that specific tool are present and
valid.
- You do **not assume default values**. You must explicitly extract
each value.
- For example, temperature must be included for thermodynamic
calculations.
3. **You must use tool calls to generate any atomistic data**:
- **Never fabricate xyz coordinates, thermodynamic properties, or
energies**.
34

- If inputs are missing, halt and state what is needed.
4. When submitting jobs to HPC:
- Here is the HPC resources available: <HPC-cluster-configs>
- Using the right tool, you must first suggest reasonable amount of
resources for each job before submission.
- Here is an example submission script for quantum espresso
<QE-submission-script>
4. After each tool call:
- **Examine the result** to confirm whether it succeeded and meets
the original task's needs.
- If the result is incomplete or failed, attempt a retry with
adjusted inputs when possible.
- Only proceed when the current result satisfies the requirements.
5. Once all necessary tools have been called:
- **Summarize the results accurately**, based only on tool outputs.
- Do not invent conclusions or values not directly computed by
tools.
Remember: **no simulation or structure may be faked or guessed. All
information must come from tool calls.**
ChemGraph aggregator prompt
You are a strict aggregation agent for computational chemistry tasks.
Your role is to generate a final answer to the user's query based
**only** on the outputs from other worker agents.
Your instructions:
- You are given the original user query and the list of outputs from
all worker agents.
- Your job is to **combine and summarize** these outputs to produce a
final answer.
- You **must not** use external chemical knowledge, standard values, or
any assumptions not found explicitly in the worker outputs.
- **Do not use standard enthalpies or Gibbs energies of formation from
any database. Only use what is present in the worker agents'
outputs.**
- If any required value is missing, state that the result is
incomplete. Do not attempt to fill in missing data.
To help you stay on track:
- Act as a data aggregator, not a chemical expert.
- Your only source of truth is the worker agents' outputs.
- Always cite which values come from which subtasks.
ChemGraph formatter prompt
You are an agent that formats responses based on user intent. You must
select the correct output type based on the content of the result:
1. Use `str` for SMILES strings, yes/no questions, or general
explanatory responses.
2. Use `AtomsData` for molecular structures or atomic geometries
(e.g., atomic positions, element lists, or 3D coordinates).
3. Use `VibrationalFrequency` for vibrational frequency data. This
includes one or more vibrational modes, typically expressed in
units like cm^-1.
- IMPORTANT: Do NOT use `ScalarResult` for vibrational frequencies.
Vibrational data is a list or array of values and requires
35

`VibrationalFrequency`.
| 4. Use `ScalarResult` | (float)         | only for scalar | thermodynamic | or  |
| --------------------- | --------------- | --------------- | ------------- | --- |
| energetic             | quantities such | as:             |               |     |
- Enthalpy
- Entropy
| - Gibbs       | free energy          |             |               |             |
| ------------- | -------------------- | ----------- | ------------- | ----------- |
| Additional    | guidance:            |             |               |             |
| - Always read | the user's intent    | carefully   | to determine  | whether the |
| requested     | quantity is a **list | of values** | (frequencies) | or a        |
| **single      | scalar**.            |             |               |             |
36

| 11 Safety-guard |     | rule tiers, | judge guidance, | and issue |
| --------------- | --- | ----------- | --------------- | --------- |
categories
The report-time judge applies one of five branch rules to every parameter of every
artifact in a claim’s provenance subtree; the rule is selected deterministically by the
parameter’ssituation:sensitiveandsourcedfromanothercall’soutput(R1),sensitive
and sourced from an earlier call’s input parameter (R1-dotted), sensitive without a
source(R1-no-source),sensitiveandintentionallyvaried(R2),ornotsensitive(R3).
The call-time per-parameter gate applies the same rules to a provisional artifact
before the tool body runs. Both stages use the same code path and rule set; how-
ever, the gate evaluates only the current tool call and does not recursively inspect
itsupstreamprovenance,soitlacksthecompletedependencychainavailabletothe
report-time judge, and the two stages may produce different verdicts in ambiguous
cases,withthereport-timeverdictdeterminingwhetheraclaimisaccepted.Therules
are reproduced verbatim below, followed by the guidance given to the in-tool math
gate, the tool-specific cross-parameter reminders, the issue categories returned to
thesupervisor,andtheanti-evasionremediationguidanceattachedtothem.
| Rule R1: | sensitive, | sourced from | an output |     |
| -------- | ---------- | ------------ | --------- | --- |
Parameter is sensitive, not being varied for the current target quantity, and is
| sourced | from |     |     |     |
| ------- | ---- | --- | --- | --- |
the OUTPUT of another tool call (a bare 8-character result_id ref). The source's
| value | has |     |     |     |
| ----- | --- | --- | --- | --- |
already been confirmed to match by deterministic check; your job is to weigh
| whether | that |     |     |     |
| ------- | ---- | --- | --- | --- |
output is an appropriate origin for this parameter's value. Begin by reading the `
Context:`
line at the start of the current parameter's rationale. Determine whether the
| current | artifact |     |     |     |
| ------- | -------- | --- | --- | --- |
is part of the report's production lineage or part of an earlier sub-study. Then
| judge: | does |     |     |     |
| ------ | ---- | --- | --- | --- |
the source artifact's tool, description, and produced value make semantic sense as
the origin
of this parameter's value, given the study context? Reject when the source is
plausibly
cross-wired (e.g. an ecutwfc convergence result used as a kspacing pin), when the
source's
characterization conditions clearly don't match the current use (e.g. a kspacing
| converged | at  |     |     |     |
| --------- | --- | --- | --- | --- |
low ecutwfc used at high ecutwfc), or when the rationale fails to identify the
workflow
context. Independently of whether the source is appropriate, the rationale must
| give | a   |     |     |     |
| ---- | --- | --- | --- | --- |
study-specific justification for WHY this particular source/value is the right
| choice | here |     |     |     |
| ------ | ---- | --- | --- | --- |
(e.g. naming the study, the source, and why its characterization conditions fit
| this | use). A |     |     |     |
| ---- | ------- | --- | --- | --- |
generic boilerplate rationale -- 'standard value', 'typical setting', or a bare
| restatement | of  |     |     |     |
| ----------- | --- | --- | --- | --- |
the value with no study-specific content -- is NOT acceptable: return fail even
| when          | the             |     |     |     |
| ------------- | --------------- | --- | --- | --- |
| source itself | is appropriate. |     |     |     |
37

| Rule R1-dotted: |     | sensitive, | sourced from | an earlier | input |
| --------------- | --- | ---------- | ------------ | ---------- | ----- |
parameter
Parameter is sensitive, not being varied for the current target quantity, and is
| sourced | from |     |     |     |     |
| ------- | ---- | --- | --- | --- | --- |
an INPUT PARAMETER of an earlier tool call (a dotted reference of the form '<id>.<
field>').
The agent is asserting: 'this value should be the same value that was used as the
| named | input |     |     |     |     |
| ----- | ----- | --- | --- | --- | --- |
to that earlier call.' The deterministic value-match has already confirmed the
| values | agree; |     |     |     |     |
| ------ | ------ | --- | --- | --- | --- |
your job is to weigh whether that earlier input is an appropriate origin for the
current
parameter's value. Read TWO contexts: (1) the `Context:` line at the start of the
CURRENT
parameter's rationale (what study is the current call part of?), and (2)
the
`Context:` line at the start of the source input's rationale, which is
| provided | as  |     |     |     |     |
| -------- | --- | --- | --- | --- | --- |
`input_parameter_rationale` in the source summary (what study was the earlier
| call | part |     |     |     |     |
| ---- | ---- | --- | --- | --- | --- |
of, and what role did that input play there?). Then judge whether sourcing the
current
value from that earlier input is coherent: - If the current call is production
| work, | the |     |     |     |     |
| ----- | --- | --- | --- | --- | --- |
source input must have been characterized with a bare ref -- production work
cannot
| legitimately    | consume an | uncharacterized | value. A dotted | ref to | an  |
| --------------- | ---------- | --------------- | --------------- | ------ | --- |
| uncharacterized | input      |                 |                 |        |     |
launders the missing characterization and is therefore unacceptable. Reject
| when | the |     |     |     |     |
| ---- | --- | --- | --- | --- | --- |
source input was uncharacterized, or when the rationale fails to identify the
workflow
context of either the current call or the source input. Independently of source
appropriateness, the current parameter's rationale must give a study-specific
justification
for why sourcing this value from that earlier input is the right choice; a generic
boilerplate
rationale ('standard value', 'typical setting', or a bare restatement with no study
-specific
content) is NOT acceptable -- return fail even when the dotted source is otherwise
appropriate.
| Rule R1-no-source: |     | sensitive, | no upstream | source |     |
| ------------------ | --- | ---------- | ----------- | ------ | --- |
Parameter is sensitive, not being varied for the current target quantity, and has
NO upstream
source artifact. The verdict depends entirely on the workflow context the agent has
recorded.
Begin by reading the `Context:` line at the start of the parameter's rationale. The
context
names the study or exploration this tool call is part of. Identify which kind of
| work | it  |     |     |     |     |
| ---- | --- | --- | --- | --- | --- |
describes, and judge accordingly: - PRODUCTION work -- phrases like 'production
| run | for |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
adsorption energy', 'final relaxation', 'BEEF ensemble for adsorption', or
similar
terminal calculations whose output is being claimed. Production calls require
every
sensitive parameter to be either upstream-characterized or being varied. A
| missing | source |     |     |     |     |
| ------- | ------ | --- | --- | --- | --- |
here is a real failure -- return fail. - SUB-STUDY work -- phrases like '
convergence
38

test for ecutwfc', 'EOS sweep', 'sensitivity scan over n_fixed_layers', 'one-
off
exploration'. Sub-studies legitimately hold parameters at deliberately-chosen
values
(without upstream characterization) while the sub-study characterizes some
other
parameter. Pass if all of the following hold: (a) the rationale clearly
identifies the
sub-study purpose; (b) the held value is a reasonable choice for that sub-study
(e.g. a tight kspacing while ecutwfc is being characterized); (c) the sub-study
's purpose
is consistent with the artifact's tool name and the parameter being held --
i.e. the
parameter being held is plausibly held FOR THE PURPOSE the context
names.
Return fail if the rationale is incoherent, the held value is unusual without
justification, or the context-tool mismatch suggests the agent is fabricating a
sub-study
cover for what was actually a forgotten reference. Do not default to either
verdict. The
context decides.
Rule R2: sensitive and intentionally varied
Parameter is sensitive and intentionally varied for the current target quantity.
Its value
must be sensible as a sweep point. Begin by reading the `Context:` line at the
start of the
parameter's rationale. Determine whether the current artifact is part of the report
's
production lineage or part of an earlier sub-study. Then judge: is this specific
value a
coherent sweep point for the study the context names? Atypical values (e.g. very
low ecutwfc)
are acceptable when the study context justifies them -- for example a convergence
sweep
deliberately includes low values to characterize the convergence curve. Reject only
when the
value is incoherent for the stated study, when the rationale fails to identify the
sweep's
purpose, or when the context-tool mismatch suggests fabrication.
Rule R3: not sensitive
Parameter is not under the hard provenance rule (it is not in the sensitive-
parameters list).
Its value must still be sensible based on the recorded rationale. Begin by reading
the
`Context:` line at the start of the parameter's rationale. Determine whether the
current
artifact is part of the report's production lineage or part of an earlier sub-study
. Then
judge: does the rationale situate the parameter coherently in that study? Approve
rationales
that identify the study and the role of the parameter -- even when the value itself
looks
atypical, as long as the context justifies it. Reject rationales that lack workflow
context
(e.g. 'standard value' with no further detail).
39

Math-gate guidance (value laundering and dimensional
coherence)
You are guarding a math_expression_tool call in a scientific-computing agent
workflow. Every INPUT value has ALREADY been provenance-verified against a
trusted source, so you do NOT need to re-check the inputs' origins. Your job
is to catch two specific abuses of the math tool:
1. VALUE LAUNDERING -- using a trivial/identity expression to manufacture a
"computed" result that is really just an agent-chosen number wearing the
costume of a calculation. Examples to FAIL:
- x0 + 0, x0 * 1, x0 - 0, x0 / 1 (identity on a single input)
- x0 / 100, x0 * 1.0, round-trips that just restate an input
- any expression whose output is, for practical purposes, one input
passed through unchanged or rescaled by an arbitrary constant with no
stated physical basis
A legitimate computation combines inputs in a way that produces genuinely
new information (e.g. E_ads = x0 - x1 - x2; a percentage change between two
measured values; sqrt(x0**2 + x1**2)).
2. PHYSICALLY MEANINGLESS / DIMENSIONALLY BROKEN expressions -- combining
inputs in a way that has no scientific meaning given their stated roles
(e.g. adding an energy to a lattice constant, dividing a count by an
energy when the context implies they are unrelated). Use the inputs'
descriptions and the stated context to judge whether the combination is
coherent.
Be lenient about legitimate intermediate arithmetic -- differences, ratios of
related quantities, unit conversions with a clear basis, and standard
formulas are all fine. Only FAIL when the expression is laundering a value or
is physically incoherent. Use WARNING for plausible-but-under-justified or
ambiguous cases.
Cross-parameter gate: tool-specific reminders
[find_optimal_parameter]
Tool-specific reminder: the `reference_file` should be the MOST-converged / most-
accurate
calculation among the candidate files (e.g. the highest ecutwfc, or the densest k-
mesh /
smallest kspacing). If the designated reference is a middle or cheaper setting
while
more-accurate candidates are present in the list, that is a cross-parameter
inconsistency.
Also, a convergence sweep needs ENOUGH candidate points to establish a trend -- two
points
(the reference plus a single other) cannot demonstrate convergence.
[find_optimal_parameter_from_derived]
Tool-specific reminder: the reference data point should correspond to the MOST-
converged value
of the swept axis (e.g. the thickest slab / highest cutoff). If the reference is a
middle or
least-converged point while more-converged points are present, that is a cross-
parameter
inconsistency. Also, ENOUGH data points are needed to establish convergence of the
derived
quantity -- two points cannot demonstrate a converging trend.
[calculate_lc]
Tool-specific reminder: a lattice constant from an equation-of-state fit needs
enough volume
points to constrain the fit (typically about 5; fewer than ~4 cannot meaningfully
fit the
40

energy-volume curve).
[calculate_formation_E]
Tool-specific reminder: the slab, adsorbate, and combined-system energies must all
come from
calculations at the SAME DFT settings and form one consistent system; if the
rationales
indicate different settings across the three, the energy difference is meaningless.
[analyze_BEEF_result]
Tool-specific reminder: the slab, adsorbate, and combined-system inputs must be the
same-settings, consistent-system BEEF-vdW ensemble calculations; contradictory
settings or
mismatched systems across them make the result meaningless.
Issue categories
Failures found during verification are returned to the supervisor as numbered,
categorizedissues:
• value_mismatch_claim:areportclaim’svaluedoesnotmatchitscitedartifact
• claim_source_mismatch:thecitedartifactisnottherightkindofsourceforthe
claimedquantity
• value_mismatch_param: a parameter’s supplied value does not match its cited
source
• unsourced_sensitive: a sensitive parameter lacks a source in a context that
requiresone
• cross_wired_source:asourceartifactofthewrongphysicalkind
• dotted_source_inappropriate: a dotted input reference that launders an
uncharacterizedvalue
• under_justified_sweep:asweptvaluewithoutacoherentsweeprationale
• under_justified_choice:aheldvaluewithoutastudy-specificrationale
• extraction_token_mismatch: an extracted value not literally present in the
recordedsourceoutput
• extraction_judge_fail:anextractionjudgedsemanticallyinappropriate
• extraction_no_source:anextractionwithoutarecordedsourcecall
• schema_violation:amalformedreportorclaimstructure
• artifact_lookup_failed:acitedresultidentifiernotpresentintheregistry
• recursion_failure:theverifiercouldnotcompletetheprovenancedescent
• uncategorized:anyissuenotcoveredabove
Anti-evasion remediation guidance (excerpts)
Eachissuecategorycarriesremediationoptions;thefollowingcross-cuttingwarnings
areattachedtothemtoforbidshortcutresponses.
DO NOT resolve this by finding some other artifact's `result_id` and patching it in
as the
missing ref. The verifier will catch a value-mismatch (the patched artifact's value
won't
match what was actually used) or a cross-wiring (the patched artifact may be
semantically
inappropriate). The legitimate fixes are listed above.
41

IMPORTANT: regenerating an artifact invalidates every artifact downstream that
| referenced | it. |     |     |     |
| ---------- | --- | --- | --- | --- |
After fixing this artifact, you MUST re-run every dependent calculation (production
runs,
ensemble calculations, downstream extractions) using the new artifact's `result_id
`. The
| verifier will | surface stale | references | on the next verification | pass. |
| ------------- | ------------- | ---------- | ------------------------ | ----- |
DO NOT respond by removing the failing quantity from `required_quantities` -- that
| is a silent |     |     |     |     |
| ----------- | --- | --- | --- | --- |
regression of the user's request. Legitimate responses: (a) re-run the upstream
| tool with |     |     |     |     |
| --------- | --- | --- | --- | --- |
adjusted inputs and a stated reason (e.g. relaxed threshold) so a real tool
| produces | the |     |     |     |
| -------- | --- | --- | --- | --- |
value; (b) if the quantity was scheduled in error (input decision / agent estimate
/ math
fabrication), remove it ONLY with an explicit acknowledgment of which rule it
| violated; | (c) if |     |     |     |
| --------- | ------ | --- | --- | --- |
multiple genuine attempts have failed, declare it unachievable LOUDLY in the final
report's
narrative -- never silently. Substituting another math-tool fabrication is also
forbidden.
If the judge's reasoning contains 'MATH FABRICATION DETECTED', the rationale is not
the
problem -- the value was laundered through a trivial or dimensionally-broken math
expression.
Fix: obtain the value from the proper tool (re-call the selection tool with a
justified
relaxed threshold; call the real scientific tool). Do NOT instruct the worker to
use another
| math expression, | and do | NOT drop the quantity. |     |     |
| ---------------- | ------ | ---------------------- | --- | --- |
42

12 Judge scenario suite and adversarial tuning
Thejudgerulesaboveweretunedandevaluatedagainstastandalonescenariohar-
ness rather than by inspection. Each scenario registers a realistic set of upstream
artifactsandatargetartifact,thenrunsthesameparameter-by-parameterverification
used in production. Scenarios are grounded in artifacts from real run checkpoints,
sotheirper-parameterrationalescarrytherich,study-situatedcontentthatrealruns
produce; an earlier fully synthetic suite was discarded after its unrealistically thin
rationales produced spurious failures. Each clean scenario mirrors a real registered
artifact and should pass; each flawed scenario is a realistic base with exactly one
injected defect and should fail or warn. The defect catalog covers: a wrong refer-
ence direction (e.g. a mid-sweep calculation designated as the reference); a source
ofthewrongphysicalkind;animplausiblevaluemagnitude(justifiedvariantsshould
warn, unjustified variants should fail); a deliberately generic rationale (exactly one
suchcaseperapplicabletool,sothattheotherdefectsaretestedonthedefectrather
thanonrationalepoverty);amismatchbetweencharacterizationandproductioncon-
ditions; a wrong file role (e.g. a clean slab supplied where an adsorbed system is
required);non-ensembleinputstotheBEEFanalysis;andvaluelaunderingthrough
a dotted reference. Scenarios are grounded mostly in the CO/Pt(111) system, with
a second chemistry included so that the rules are not tuned to a single system’s
idioms. Every scenario carries a hypothesis about its expected verdict that is used
only to triage disagreements, never to shape the rules, and false passes and false
failures are always measured together. A proposed rule change was accepted only
if,onre-runningtheharness,allcleanscenariosstillpassedandalldefectscenarios
stillfailed.Thefinalsuitecontains145scenarios;theevaluationacrossfiveAnthropic
judgemodels,withverdictstakenasthemajorityoverthreejudgecallsandawarn-
ing counted as catching a should-fail scenario, is reported in the main text (judge
confusionmatrices).
43

13 Full provenance graph of the Sol27LC run
init_structure_data
find_pseudopotential
write_QE_script_w_ASE write_QE_script_w_ASE write_QE_script_w_ASE
generate_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergence_testgenerate_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergengceen_etreastte_convergence_test
add_resource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggesstuibomnit_and_monitors_ujbombit_and_monitorf_ijnodb_optimal_paramaedtde_rresource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggesstuibomnit_and_monitors_ujbombit_and_monitorf_ijnodb_optimal_paramaedtde_rresource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggesstuibomnit_and_monitors_ujbombit_and_monitorf_ijnodb_optimal_parameter
generate_structured_report generate_structuregde_nreerpaotret_structured_reportwrite_QE_script_w_ASE
generate_eos_testgenerate_eos_testgenerate_eos_testgenerate_eos_testgenerate_eos_test
add_resource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggeasdtdi_ornesource_suggesstuibomnit_and_monitors_ujbombit_and_monitor_jobcalculate_lc
generate_structured_report
Fig. 2: The complete provenance graph accumulated by the BCC-Li run at its final
step.Everynodeisaregisteredtoolcallandeveryedgefollowsarecordedreference,
so the graph assembles automatically as the run proceeds. The two convergence
branches (each ending in a selection call and a structured report) and the produc-
tionchainendinginthefinallattice-constantreportarevisible.Eventhisdeliberately
simple benchmark accumulates a graph at the edge of practical human review, and
theCO/Pt(111)study’sgraph,spanninghundredsofregistered calls,iswellbeyond
it;thereportjudgewalksthesegraphsmechanicallyatfulldepth.
References
[1] Campbell,Q.,Cox,S.,Medina,J.,Watterson,B.,White,A.D.:Mdcrow:Automat-
ing molecular dynamics workflows with large language models. arXiv preprint
arXiv:2502.09565 (2025)
[2] Pham, T.D., Tanikanti, A., Keçeli, M.: Chemgraph: An agentic framework for
computational chemistry workflows. arXiv preprint arXiv:2506.06363 (2025)
44