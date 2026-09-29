|     | Simthesizer: |           |      |     |     | An  | Agent-Driven |         |     |     | Simulation |       |     |     |     |
| --- | ------------ | --------- | ---- | --- | --- | --- | ------------ | ------- | --- | --- | ---------- | ----- | --- | --- | --- |
|     |              | Framework |      |     |     | for | LLM          | Serving |     |     | Systems    |       |     |     |     |
|     | Wonung       |           | Kim† |     |     |     | Hyunmin      | Choi†   |     |     |            | Minsu | Kim |     |     |
|     |              | KAIST     |      |     |     |     |              | KAIST   |     |     |            | KAIST |     |     |     |
Daejeon, Republic of Korea Daejeon, Republic of Korea Daejeon, Republic of Korea
wukim@casys.kaist.ac.kr hmchoi@casys.kaist.ac.kr mskim@casys.kaist.ac.kr
|     |     | Jaehong | Cho |     |     |     | Yeongwook | Kim   |     |     |     | Jongse | Park |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --------- | ----- | --- | --- | --- | ------ | ---- | --- | --- |
|     |     | KAIST   |     |     |     |     |           | KAIST |     |     |     | KAIST  |      |     |     |
Daejeon, Republic of Korea Daejeon, Republic of Korea Daejeon, Republic of Korea
6202 guA 62  ]RA.sc[  2v05642.8062:viXra
jhcho@casys.kaist.ac.kr ywkim@casys.kaist.ac.kr jspark@casys.kaist.ac.kr
Abstract—System-level simulation is an essential tool for ex- Implement Feature A Implement Feature A
| ploring the | rapidly | expanding |     | design | space of | LLM | serving sys- |     |     |     |     |     |     |     |     |
| ----------- | ------- | --------- | --- | ------ | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
tems,whererealdeploymentsremaincostlyandofteninfeasible. User  User
| However,                                                | modern | LLM  | serving | now evolves |     | faster        | than human- |          |     |       |     |     |     |     |     |
| ------------------------------------------------------- | ------ | ---- | ------- | ----------- | --- | ------------- | ----------- | -------- | --- | ----- | --- | --- | --- | --- | --- |
|                                                         |        |      |         |             |     |               |             | Add/Edit |     | Debug |     |     |     |     |     |
| drivensimulatordevelopmentcantrack,andemergingworkloads |        |      |         |             |     |               |             |          |     |       |     | DAG |     |     |     |
| and mechanisms,                                         |        | from | agentic | workflows   | to  | disaggregated | serv-       |          |     |       |     |     |     |     |     |
ing,nolongerfitthemonolithicsimulationpipelinethatexisting
|            |          |         |            |                |             |            |             | Scheduler |     | Memory    |     | High-level Abstraction |                     |     |     |
| ---------- | -------- | ------- | ---------- | -------------- | ----------- | ---------- | ----------- | --------- | --- | --------- | --- | ---------------------- | ------------------- | --- | --- |
| simulators | assume.  | Each    | new        | mechanism      | therefore   |            | demands     | an        |     |           |     |                        |                     |     |     |
| invasive   | rewrite, | leaving | a widening |                | development |            | gap between |           |     |           |     |                        |                     |     |     |
|            |          |         |            |                |             |            |             | Network   |     | Execution |     |                        |      Agent Lowering |     |     |
| deployed   | serving  | systems | and        | the simulators |             | that model | them.       |           |     |           |     |                        |                     |     |     |
</ >   Low-level
| To close | this | gap, | we present | Simthesizer, |     | a   | framework |     |     |     |     |     |     |     |     |
| -------- | ---- | ---- | ---------- | ------------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
that realizes agent-driven simulator development. Simthesizer Implementation Executable Simulation
| introduces | a composable |     | simulator | infrastructure |           | that | uniformly   |                          |     |     |     |                           |     |     |     |
| ---------- | ------------ | --- | --------- | -------------- | --------- | ---- | ----------- | ------------------------ | --- | --- | --- | ------------------------- | --- | --- | --- |
|            |              |     |           |                |           |      |             | (a) Existing LLM Serving |     |     |     | (b) Simthesizer Framework |     |     |     |
| expresses  | the complete |     | serving   | workflow,      | including |      | the control |                          |     |     |     |                           |     |     |     |
Simulators
| decisions | that coordinate |            | it, and | realizes    | it as | a unified | dynamic     |     |     |     |     |     |     |     |     |
| --------- | --------------- | ---------- | ------- | ----------- | ----- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
| graph in  | Simthesizer     | simulator. |         | Synthesizer |       | agent,    | a harnessed |     |     |     |     |     |     |     |     |
Fig.1. (a)ExistingLLMservingsimulatorsrequiremanuallyimplementing
codingagent,thenlowersnatural-languagefeaturerequestsonto
newservingmechanismsastheyemerge,leadingtolow-levelmodifications,
this abstraction under simulator-specific guardrails and fidelity while (b) Simthesizer framework instead composes the complete serving
validation, evolving one shared simulator instead of building workflow from uniform elements of a unified dynamic DAG, which is
a new one for every feature. Under the same coding agent automatically lowered into executable simulation through agent-driven de-
| and harnesses, |            | extensions | built | on Simthesizer |             | follow | a vLLM-       | velopment. |            |     |      |          |          |         |         |
| -------------- | ---------- | ---------- | ----- | -------------- | ----------- | ------ | ------------- | ---------- | ---------- | --- | ---- | -------- | -------- | ------- | ------- |
| based real     | system     | with       | 2.51% | average        | throughput  |        | error, versus |            |            |     |      |          |          |         |         |
| 6.03% for      | extensions | built      | on    | existing       | simulators. |        | On identical  |            |            |     |      |          |          |         |         |
|                |            |            |       |                |             |        |               | This shift | transforms |     | both | the pace | at which | serving | systems |
workloads,Simthesizeralsosimulatesupto284.96×and23.19×
|             |     |                  |     |             |     |                  |     | evolve | and the | way | requests | and | serving | mechanisms | are |
| ----------- | --- | ---------------- | --- | ----------- | --- | ---------------- | --- | ------ | ------- | --- | -------- | --- | ------- | ---------- | --- |
| faster than | two | state-of-the-art |     | simulators, |     | LLMServingSim2.0 |     |        |         |     |          |     |         |            |     |
and Vidur, respectively. structured, demanding a rethinking of system-level simulator
|     |     |     |              |     |     |     |     | design.            | Specifically, |     | it introduces | two       | key changes: |      |           |
| --- | --- | --- | ------------ | --- | --- | --- | --- | ------------------ | ------------- | --- | ------------- | --------- | ------------ | ---- | --------- |
|     |     | I.  | INTRODUCTION |     |     |     |     |                    |               |     |               |           |              |      |           |
|     |     |     |              |     |     |     |     | 1) Fast evolution: |               | The | LLM           | ecosystem | evolves      | at a | fast pace |
asnewmodels,applications,andsystem-leveloptimizations
DesigningefficientLLMservingsystemsrequiresexploring
|     |     |     |     |     |     |     |     | continuously |     | emerge. | Serving | techniques |     | and execution |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------- | ------- | ---------- | --- | ------------- | --- |
anexpandingdesignspacespanninghardware,scheduling,and
systemoptimizations.Evaluatingthesechoicesonrealsystems patterns consequently change over time, rapidly invalidat-
|          |               |     |           |     |           |     |              | ing a | simulator’s |     | assumptions | about | system | behavior | and |
| -------- | ------------- | --- | --------- | --- | --------- | --- | ------------ | ----- | ----------- | --- | ----------- | ----- | ------ | -------- | --- |
| is often | prohibitively |     | expensive | and | difficult | to  | scale, espe- |       |             |     |             |       |        |          |     |
cially as emerging hardware accelerators are not yet available requiring repeated manual effort to keep it up to date.
|                  |     |             |             |      |             |     |            | 2) Non-monolithic |      | serving: |       | Agentic     | requests | expand      | a single |
| ---------------- | --- | ----------- | ----------- | ---- | ----------- | --- | ---------- | ----------------- | ---- | -------- | ----- | ----------- | -------- | ----------- | -------- |
| as off-the-shelf |     | platforms.  | Even        | when | deployable, |     | bringing   |                   |      |          |       |             |          |             |          |
|                  |     |             |             |      |             |     |            | query             | into | multiple | model | invocations |          | interleaved | with     |
| such systems     |     | up requires | substantial |      | engineering |     | effort and |                   |      |          |       |             |          |             |          |
cost. As a result, system-level simulation has become an external tool calls and decision-making stages, following
dynamicexecutionpathsdeterminedbyintermediateresults.
| essential | tool | for LLM | serving | research, | enabling |     | rapid and |     |     |     |     |     |     |     |     |
| --------- | ---- | ------- | ------- | --------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
cost-effective exploration of design trade-offs [1], [6], [7]. Meanwhile, serving mechanisms such as disaggregated ex-
ecutionandspeculativedecodingbreaktheonce-monolithic
| However, | these | simulators |          | are now | challenged |             | by a fun- |           |      |      |          |             |         |      |        |
| -------- | ----- | ---------- | -------- | ------- | ---------- | ----------- | --------- | --------- | ---- | ---- | -------- | ----------- | ------- | ---- | ------ |
|          |       |            |          |         |            |             |           | inference | flow | into | multiple | interacting | stages. | Both | trends |
| damental | shift | in LLM     | serving, | from    | the        | traditional | single-   |           |      |      |          |             |         |      |        |
inference execution flow to diverse and dynamic workflows. replace the predetermined serving flow that existing simu-
|     |     |     |     |     |     |     |     | lators | assume | with | dynamically | composed |     | stages. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ | ---- | ----------- | -------- | --- | ------- | --- |
†Theseauthorscontributedequally. To cope with these challenges, it is natural to ask whether

existing LLM serving simulators can keep up, but they are We instruct OpenAI Codex [33] to serve as Synthesizer
fundamentally limited. Most simulators rest on two premises, agent, extending Simthesizer simulator with new serving fea-
that serving systems evolve slowly enough for manual en- tures and implementing the same features on existing simula-
gineering to keep pace and that serving behavior can be tors with the same set of harnesses. Comparing the resulting
capturedbyasinglemonolithicsimulationpipeline.Asthetwo extensions, we find that Simthesizer more closely follows the
changesaboveinvalidatethesepremises,everynon-monolithic behaviors of a vLLM-based real system, achieving an average
mechanism now forces an invasive restructuring of the fixed throughput error of 2.51%, whereas extensions built on exist-
simulationpipeline,whiletrackingfastevolutionleavesdevel- ing simulators exhibit a significantly higher throughput error
opers repeatedly modifying andvalidating simulator internals. of6.03%.Lastly,usingidenticalLLMworkloads,Simthesizer
achieves up to 284.96× and 23.19× faster simulation time
To address these limitations, we propose a novel frame-
than two state-of-the-art simulators, LLMServingSim2.0 [6]
work, Simthesizer, for developing modern LLM serving sim-
and Vidur [1], respectively.
ulators, as illustrated in Figure 1. Our approach captures
These results demonstrate that our framework effectively
non-monolithic serving through a composable and extensible
supports the development and extension of modern LLM
simulatorinfrastructurethatuniformlyexpressesthecomplete
servingsimulators,enablingaccurateandextensiblemodeling
serving workflow, and tracks fast evolution through agent-
of complex and rapidly evolving workloads. While our evalu-
driven lowering that translates natural language specifications
ation focuses on LLM serving simulation, the combination of
into executable simulation. Our contributions are as follows:
composablesimulatorinfrastructureandagent-drivenlowering
(1) Composable and extensible simulator infrastructure suggests a promising direction for building simulators in
for LLM serving simulation. We introduce Simthesizer other systems domains. We view this work as an initial step
simulator, a simulator infrastructure that expresses every toward such a direction, and hope it encourages further ex-
element of the serving workflow, rather than only its ploration of more scalable and automated simulation method-
compute and communication operations, in one uniform, ologies. Simthesizer is available at https://github.com/casys-
composable form. Simthesizer simulator realizes this de- kaist/Simthesizer.
signasadirectedacyclicgraph(DAG)wherelogicalnodes
II. BACKGROUNDANDMOTIVATION
expresscontroldecisionssuchasrequestroutingandbatch
A. LLM Serving Simulation
formation alongside compute and communication nodes.
A modular control layer implements these decisions as ChallengesinevaluatingLLMservingsystems.Asthescale
interchangeable components, so new serving mechanisms and complexity of LLM serving systems continue to grow,
areintegratedbycomposingcomponentsandreconnecting theirdesignspacehasexpandedtoencompassawiderangeof
nodes without restructuring the execution engine. deploymentchoices,includingparallelismstrategies[34],[45],
(2) Agent-driven lowering for scalable simulator exten- [58], scheduling policies [2], [41], [53], batch formation [2],
sion. We develop Synthesizer agent, a harnessed coding [53], [59], KV-cache management [8], [16], [20], [35], and
agent that systematically lowers high-level specifications workload composition [52], [54]. However, evaluating these
intoexecutablesimulationlogic,bridgingthegapbetween choices on real systems is often prohibitively expensive and
specifiedbehaviorandlow-levelexecution.Insteadofman- difficulttoscale.Moreover,manycandidatedesigns,including
ually implementing new system behaviors, our approach emerging accelerators, interconnects, and cluster configura-
exposesstructuredinterfacesandmodularcomponentsthat tions, are not yet available for direct measurement.
agents extend or compose, guided by harness engineering SimulationforLLMserving.Toaddressthesechallenges,the
that constrains task scope, enabling reliable integration of systemscommunityhasturnedtosystem-levelsimulatorsasa
emerging serving mechanisms. practicalmeansofexploringdesigntrade-offsinLLMserving
(3) End-to-end implementation and verification of an systems [1], [6], [7], [28]. These simulators allow researchers
extensible simulator. We implement Simthesizer end- toexploreandvalidateearlyideasacrossscheduling,hardware
to-end, combining Simthesizer simulator and Synthesizer architectures, and system configurations before implementa-
agent into a complete framework for developing and ex- tion or deployment [5], [19], [34], [58].
tending LLM serving simulators. To extend the simulator, Vidur [1] predicts LLM inference performance across par-
Synthesizeragentrefinesanaturallanguagefeaturerequest allelism strategies, batch sizes, and scheduling policies using
into a specification, maps it onto Simthesizer simulator’s a random-forest model trained on profiled GPU operator
abstractions, implements any missing functionality, and latencies. Similarly, APEX [28] predicts performance across
validates the result against real-system measurements or models, quantization formats, batching policies, and device-
reference evidence. We demonstrate this workflow by clusterconfigurations.Todoso,itconstructscandidateserving
extending Simthesizer simulator with Synthesizer agent configurations using predefined modules and feeds them to
across modern serving mechanisms, including KV cache itssimulator.LLMServingSim[7]andLLMServingSim2.0[6]
quantization, speculative decoding, and hybrid Mamba modeladditionalmodernservingmechanisms,includingprefix
model support, evolving one shared simulator rather than caching, prefill/decode disaggregation, and KV-cache offload-
building a new one per feature. ing, through higher-level abstractions.

|           |     |     |     |        |          |     | disaggregated | serving | splits | prefill | and | decode | across | separate |
| --------- | --- | --- | --- | ------ | -------- | --- | ------------- | ------- | ------ | ------- | --- | ------ | ------ | -------- |
| Workload  |     |     |     | System | Workload |     |               |         |        |         |     |        |        |          |
Fixed  Programmable machine pools [34], [58], speculative decoding coordinates
Inference App defined User Query draftandtargetmodelswithinadecodingloop[21],[30],and
|     |     |     |     |     |     |     | KV-cache | management |     | distributes |     | request | state | across turns |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | ----------- | --- | ------- | ----- | ------------ |
LLM Inference
Decoding Mechanism
Disaggregated Serving and storage tiers [8], [14], [44]. Despite optimizing different
Baseline Tree-based Speculative Decoding resources, they all replace the self-contained inference lifecy-
| Decoding | Suffix-decoding |     |     | Cache Management |     |     |     |     |     |     |     |     |     |     |
| -------- | --------------- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
clewithorchestrationacrossseparatelymanagedcomponents.
|                      |     |     |     |      |            |     | Implications | for | existing | simulators. |     | These | two | trends un- |
| -------------------- | --- | --- | --- | ---- | ---------- | --- | ------------ | --- | -------- | ----------- | --- | ----- | --- | ---------- |
| Serving Architecture |     |     |     | Tool | Sub Refine |     |              |     |          |             |     |       |     |            |
Calls Agent dermine the premises of existing simulators. New serving be-
P/D Disagg.
Monolithic
Serving haviors emerge faster than human developers can implement,
|                |                     | A/F Disagg. |          |                            | Answer        |          |             |              |            |               |                |            |         |             |
| -------------- | ------------------- | ----------- | -------- | -------------------------- | ------------- | -------- | ----------- | ------------ | ---------- | ------------- | -------------- | ---------- | ------- | ----------- |
|                |                     |             |          |                            |               |          | integrate,  | and validate |            | them,         | leaving        | a widening |         | development |
|                | (a) Fast Evolution  |             |          | (b) Non-monolithic Serving |               |          |             |              |            |               |                |            |         |             |
|                |                     |             |          |                            |               |          | gap between | deployed     |            | serving       | systems        |            | and the | simulators  |
|                |                     |             |          |                            |               |          | that model  | them.        | Meanwhile, |               | non-monolithic |            | serving | breaks      |
| Fig. 2. Shifts | in modern           | LLM         | serving: | (a) fast                   | evolution and | (b) non- |             |              |            |               |                |            |         |             |
|                |                     |             |          |                            |               |          | the fixed   | serving      | loop       | that existing |                | simulators | assume  | every       |
monolithicserving.
|     |     |     |     |     |     |     | request | follows | (Section | II-A). | A   | feature | that | falls outside |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | -------- | ------ | --- | ------- | ---- | ------------- |
Two outdated premises. Although these simulators adopt this loop therefore requires restructuring its control flow and
| different | abstractions, | they | all | encode | serving behavior | as  |             |         |        |          |     |        |     |     |
| --------- | ------------- | ---- | --- | ------ | ---------------- | --- | ----------- | ------- | ------ | -------- | --- | ------ | --- | --- |
|           |               |      |     |        |                  |     | propagating | changes | across | existing |     | paths. |     |     |
componentsthathumandevelopersimplementinadvanceand
|           |              |            |     |           |             |        | C. Rethinking | Simulation |     | Design       | for | Modern | LLM          | Serving |
| --------- | ------------ | ---------- | --- | --------- | ----------- | ------ | ------------- | ---------- | --- | ------------ | --- | ------ | ------------ | ------- |
| integrate | into a fixed | simulation |     | pipeline. | This shared | design |               |            |     |              |     |        |              |         |
| remains   | practical    | only under | two | premises: | (1) the     | target |               |            |     |              |     |        |              |         |
|           |              |            |     |           |             |        | Agent-driven  | simulator  |     | development. |     | Both   | implications | ul-     |
serving system evolves slowly, and (2) serving behavior can timately stem from a shortage of engineering labor. Fast
be captured by a monolithic simulation pipeline. The first evolution multiplies how often developers must extend a
premiseassumesthatnewservingbehaviorsariseinfrequently
|     |     |     |     |     |     |     | simulator | to close | the development |     |     | gap, while | non-monolithic |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --------------- | --- | --- | ---------- | -------------- | --- |
enough to amortize the substantial human effort required to serving turns each extension into an invasive rewrite. Sustain-
| implement | them. The | second | assumes |     | that a single, | tightly |                |         |     |                |     |       |                |     |
| --------- | --------- | ------ | ------- | --- | -------------- | ------- | -------------- | ------- | --- | -------------- | --- | ----- | -------------- | --- |
|           |           |        |         |     |                |         | ing simulators | against |     | both pressures |     | calls | for automating | the |
integrated control flow can encode diverse serving techniques implementation work itself. Recent LLM-based coding agents
aspredefinedpolicies.AswediscussinSectionII-B,however, make this automation practical, and the systems community
therapidevolutionofservingmechanismsandtheshifttoward
|     |     |     |     |     |     |     | already | employs | them | [4], [48], | [57]. | We  | therefore | envision |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ---- | ---------- | ----- | --- | --------- | -------- |
non-monolithic serving call both premises into question. agent-driven simulator development, in which coding agents
|                 |           |     |        |         |     |     | implement | new    | serving | mechanisms |          | as they | emerge.  |            |
| --------------- | --------- | --- | ------ | ------- | --- | --- | --------- | ------ | ------- | ---------- | -------- | ------- | -------- | ---------- |
| B. The Shifting | Landscape |     | of LLM | Serving |     |     |           |        |         |            |          |         |          |            |
|                 |           |     |        |         |     |     | However,  | simply | adding  | an         | AI agent | to      | existing | simulators |
Modern LLM serving is shifting along two coupled di- isinsufficient.Boundtoamonolithicpipeline,anagentinher-
rections: (1) its workloads and mechanisms evolve at an its the same structural coupling, so each extension remains
unprecedented pace, and (2) many of them no longer take a broad, system-wide rewriting that is difficult to review
the form of a monolithic inference flow. and may introduce silent regressions. Keeping modifications
Fast evolution. First, LLM workloads and serving mech- local requires a representation that captures inference and
anisms now evolve rapidly and concurrently across every non-inference stages, and the control flow coordinating them
level of the serving stack. In just a few years, agentic within a single abstraction. Even then, generated code that
workloads have pushed serving systems from fixed inference compilesandpassesfunctionaltestscanstillmodelthewrong
flows [20] toward programmable, application-defined work- system, demanding simulator-specific guardrails and fidelity
flows [9], [27]. Over the same period, speculative decoding validation. From these requirements, we derive two design
has raced through successive generations, from conventional principles for next-generation serving simulators:
draft-and-verify methods to tree-based and suffix-decoding • (Principle 1) Composable simulation from a uniform
schemes [21], [23]–[25], [30], [32]. Serving architectures representation. Existing simulators bind serving mecha-
likewise keep diversifying toward P/D and attention–FFN nisms to technique-specific control paths, making each ex-
disaggregation [34], [58], [60]. Each new wave arrives before tension a system-wide change. A modern simulator should
the previous one settles into standard practice. instead express workloads and mechanisms in a uniform,
Non-monolithic serving. Second, many emerging workloads composable representation that captures stages, dependen-
and serving mechanisms no longer fit within a single, self- cies, and state transitions, allowing humans or agents to
contained inference lifecycle. On the workload side, as shown add and compose components without restructuring the
in Figure 2, agentic requests expand a single user query into execution engine.
multiple LLM inferences interleaved with external tool calls, (Principle 2) Guarded agent-driven implementation.
•
sub-agent execution, and iterative context refinement [13], Structural locality bounds an agent’s changes, but does
[37], [39], [40], [46], [51]. A request is thus no longer a not ensure simulation fidelity, as an extension can compile
single inference call but a runtime-dependent composition and produce plausible outputs while omitting performance-
of inference and non-inference stages. On the system side, critical state or violating simulator-specific invariants. A

Simthesizer Framework Output
Simthesizer Simulator Synthesizer Agent
Validation Documents Modular Control Layer Harnessed Lowering
Input TTFT ITL Tok/s Design Scheduler Router Model Task Sim Sim
Implement Validation Dynamic DAG API Design Mapping Dev
Feature A Synthesizer Simthesizer Simthesizer Unified Dynamic DAG
Agent Simulator Simulator Comp. Guided Validation
Logic. Logic.
Harness Feature A Feature A Comm. Trace Reference
(a) Simthesizer Framework (b) Simthesizer Simulator (c) Synthesizer Agent
Fig.3. OverviewoftheSimthesizerframework.
modern simulator must therefore pair bounded extension Compute Comm. Logical
System
interfaces and simulator-specific guardrails with validation DAG Event Engine
methods that evaluate simulation semantics. Scheduler Model Model Runner Queue Execute
Control Layer Compute Network
III. OVERVIEWOFSIMTHESIZER Interface
Execution Layer
Guided by these principles, we present Simthesizer, a Next
Engine DAG Event Queue
simulation framework that realizes agent-driven simulator
development for modern LLM serving. Simthesizer pairs a
Fig.4. ArchitectureofSimthesizersimulator.
composable,extensiblesimulationsubstrate(Principle1)with
a guarded agent workflow (Principle 2), as illustrated in lowers a user request through three stages, task-design,
Figure 3. sim-mapping,andsim-dev,whichrespectivelyproducea
Simthesizer framework. Simthesizer comprises two compo- simulator-facingspecification,mapeachdecisiontoaSimthe-
nents,(1)Simthesizersimulator,aunifiedandextensibleLLM sizer simulator abstraction, and extend the implementation.
serving simulator, and (2)Synthesizer agent,a harnessedcod- The agent then evaluates simulation fidelity through trace-
ingagentthatintegratesnewservingmechanismsintoSimthe- guided validation when real-system measurements are avail-
sizer simulator. The workflow begins with a user request able and reference-guided validation otherwise. Users may
specifying the feature to implement. Synthesizer agent refines resolve performance-critical ambiguities and review the spec-
theintendedbehavior,mapsitontoSimthesizersimulator’sab- ification, implementation map, and validation report, while
stractions, and implements any functionality Simthesizer sim- Synthesizer agent performs the low-level implementation and
ulator does not already provide. Then, Simthesizer validates revision work. Together, Simthesizer simulator and Synthe-
the observed behavior against real-system measurements or sizer agent make simulator extension both compositional and
reference evidence. The workflow finally returns the extended reviewable, allowing Simthesizer to track new serving mech-
Simthesizer simulator together with inspectable artifacts ex- anisms without restructuring a monolithic simulation pipeline
posing its modeling decisions, implementation decisions, and (Section V).
validation results.
Simthesizer simulator. Existing simulators use static DAGs IV. SIMTHESIZERSIMULATOR
and pipelines to encode compute and communication oper-
Figure4showsthetwo-layerarchitectureoftheSimthesizer
ations, so any mechanism that alters this pipeline demands
simulator.Theexecutionlayerrealizesthecomposablesimula-
an invasive, end-to-end redesign. To address this, Simthesizer
torinfrastructureasaunifieddynamicDAGthatrepresentsan
simulator composes the entire serving workflow from a uni-
LLM serving workflow, allowing new mechanisms to extend
form set of elements, using compute, communication, and
the graph without restructuring the execution engine. The
logicalnodesofaunifieddynamicDAGtocapturebothLLM
control layer constructs and modifies these graphs through
operations and the control decisions. Through Dynamic DAG
modular components that implement serving policies. This
APIs, logical nodes insert operations and rewire dependencies
separation gives Simthesizer simulator a stable execution
at runtime, allowing Simthesizer simulator to integrate new
substrate while its serving behavior evolves through localized
mechanisms and express runtime-dependent workflows with-
extensions.
out modifying the execution engine. Above this substrate, a
modularcontrollayerimplementsservingpoliciesthroughin-
A. Unified Dynamic DAG Abstraction
terchangeable components such as schedulers, routers, model
runners, and resource simulators. Existing components com- Execution graph representation. Simthesizer simulator rep-
pose through structured configuration, and a new mechanism resentsthecompletesimulatedexecutionasaunifieddynamic
requires implementing only the behavior the control layer DAG with three node types: (1) compute nodes that specify
lacks (Section IV). whichmodeloperationexecutesonwhichdevice,(2)commu-
Synthesizer agent. Synthesizer agent is a coding agent with nicationnodesforinter-devicetransfers,and(3)logicalnodes
a harness tailored to developing LLM serving simulators. It for policy events such as request arrival and scheduling. Each

TABLEI
DYNAMICDAGMODIFICATIONAPIS.
Interface Description
add_logical_node(operation, state) -> node Insertalogicalnodecarryingapolicyoperationanditsstate.The_at
add_logical_node_at(operation, state, at) -> node variantseedsanexplicitstarttime,e.g.,forrequestarrival.
add_compute_node(layer, batch) -> node Insertacomputenodetaggedwithasemanticlayerdescriptorandthe
scheduledbatchstate.
add_network_node(src, dst, bytes) -> node Insertapoint-to-pointtransferbetweentwonetworkdevices.Itstiming
modelresolveslatency,includingmulti-hoproutingwhenconfigured.
add_edge(parent, child) Declare a precedence constraint. A child becomes runnable only after
allofitspredecessorscomplete.
pop_edges(node) -> list[node] Detachthecurrentnode’soutgoingedgessothecallercanspliceanew
subgraphbeforetheoriginalsuccessor.
edge encodes an execution-order dependency, and simulation time, and processes the corresponding node. A deterministic
executes each node once all of its predecessors complete. node schedules a fixed completion event at dispatch, whereas
Node taxonomy. At execution, each node differs along two a change in resource state can invalidate and replace the
dimensions:(1)latencyisdeterministicwhenfixedatdispatch completion event of a non-deterministic node. A stateful node
and non-deterministic when later activity can change the may additionally update serving state or modify the execution
completion time, and (2) behavior is stateful when execution graph. Upon completion, the execution layer propagates the
alters subsequent control flow or updates serving state and node’s completion time to its successors, resolves incoming
stateless otherwise. The three node types occupy distinct dependencies, and enqueues each newly runnable node.
points in this taxonomy, which determines how the execution
layer processes each of them. B. Dynamic DAG APIs
Compute nodes. Simthesizer simulator treats compute nodes
LLM serving is inherently dynamic, as batch composition,
as deterministic and stateless by construction. A compute
placement, and even the stages a request traverses depend
node represents an already scheduled model operation on
on runtime state, so a simulator cannot enumerate every
a target device, with shared-device ordering encoded by its
operation and dependency in advance. Existing simulators
dependencies. Once runnable, its operation, batch, and device
sidestepthisdynamismbykeepingruntimedecisionsinafixed
model determine a single latency, and kernel-level effects
simulation pipeline outside their compute and communication
remain encapsulated within that latency model.
DAGs [1], [6], [7], [28]. Simthesizer simulator instead lets
Communication nodes. Communication nodes are non- logical nodes grow the graph as decisions become known,
deterministic and stateless, as link contention can affect their using the Dynamic DAG APIs in Table I to insert new nodes
completion time while their execution leaves state unchanged. andrewiredependencies,keepingworkflowchangeslocalized.
To model non-deterministic latency, Simthesizer simulator Node construction. Dynamic expansion first materializes
allows the network model to invalidate a node’s scheduled each runtime-selected action as one of the three node types.
completion event when resource state changes and to pro- add_logical_node records the operation and state for
vide a revised completion time for rescheduling. This event- a policy event, add_compute_node records the seman-
invalidation interface supports dynamic contention without tic layer and scheduled batch, and add_network_node
binding the execution layer to a particular network model. records the source, destination, and transfer size. Each API
Logical nodes. Logical nodes are deterministic and stateful. returns a node handle for later connections, and these typed
They encode control decisions such as request routing, batch constructors keep newly added nodes consistent with the
formation,andstatetransitions,withafixedexecutionlatency execution semantics of the initial graph.
and explicit updates to request or system state. Existing Dependency construction. Creating nodes alone does not
simulators implement these decisions in fixed control flow determine when they execute; the add_edge(parent,
outside their compute and communication DAGs; Simthesizer child) API specifies that the child can run only after the
simulatorinsteadmakesthemfirst-classnodesintheexecution parent completes. A logical node may also alter existing
graph. A new serving workflow can therefore be constructed dependencies;indisaggregatedserving,forexample,adecode
by adding and reconnecting compute, communication, and stage already follows its prefill stage, but assigning decode
logical nodes, leaving the core execution engine untouched. to another machine requires a KV-cache transfer to complete
Event-driven processing. The execution layer processes all in between. The pop_edges API detaches and returns the
node types through a common event-driven loop. It first prefillnode’soutgoingedges,lettingthelogicalnodesplicein
initializes simulated time and inserts every node with no the transfer node and reconnect the decode stage after it. This
unresolved predecessor into a time-ordered event queue. At local rewrite preserves the surrounding graph while enforcing
each step, it dequeues the earliest event, advances simulated the new execution order.

|     |                      |        |                 |          |     | state to       | the implementation |            | that  | realizes       | it (Figure | 5(b)).        |
| --- | -------------------- | ------ | --------------- | -------- | --- | -------------- | ------------------ | ---------- | ----- | -------------- | ---------- | ------------- |
| 1   | interface            | System | extends         | Logical: |     |                |                    |            |       |                |            |               |
|     | into_results()       |        | -> list[result] |          |     | ChunkedPrefill |                    |            |       | Scheduler      |            |               |
| 2   |                      |        |                 |          |     |                |                    | implements |       |                |            | and privately |
| 3   | Logical::handle(...) |        |                 | -> time  |     |                |                    |            |       |                |            |               |
| 4   |                      |        |                 |          |     | tracks its     | prefix-caching     | flag,      | while | SingleInstance |            | im-           |
5 interface Scheduler: plements System, holding its scheduler only through the
6 enqueue_sub_request(sub_request)
7 schedule() -> batch interface. Swapping in another scheduler thus touches neither
(a) Component interfaces SingleInstance nor the execution layer.
1 impl System for SingleInstance: Configuration composes a system. A structured configura-
|     | scheduler: |     | Scheduler |     |     |                |     |                  |     |      |            |           |
| --- | ---------- | --- | --------- | --- | --- | -------------- | --- | ---------------- | --- | ---- | ---------- | --------- |
| 2   |            |     |           |     |     | tion assembles |     | these components |     | into | a complete | simulator |
3
4 def into_results() -> list[result] (Figure 5(c)). Each kind field selects an implementation for
| 5   | def | Logical::handle(...) |     | -> time |     |                                                         |     |     |     |     |     |     |
| --- | --- | -------------------- | --- | ------- | --- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
| 6   |     |                      |     |         |     | oneinterface,nestedentriesselectsubcomponents,andthere- |     |     |     |     |     |     |
7 impl Scheduler for ChunkedPrefill: mainingfieldssetimplementation-specificparameters.Theex-
| 8   | enable_prefix_caching: |                                  |     | bool |     |              |                |     |     |      |                |     |
| --- | ---------------------- | -------------------------------- | --- | ---- | --- | ------------ | -------------- | --- | --- | ---- | -------------- | --- |
|     |                        |                                  |     |      |     |              | SingleInstance |     |     |      | ChunkedPrefill |     |
| 9   |                        |                                  |     |      |     | ample builds |                |     |     | over |                |     |
| 10  | def                    | enqueue_sub_request(sub_request) |     |      |     |              |                |     |     |      |                |     |
def schedule() -> batch and enables prefix caching without touching simulator code.
11
|     |     |               |     |                 |     | This composition |     | bounds | the cost | of extending |     | Simthesizer |
| --- | --- | ------------- | --- | --------------- | --- | ---------------- | --- | ------ | -------- | ------------ | --- | ----------- |
|     |     | (b) Component |     | implementations |     |                  |     |        |          |              |     |             |
simulator.Wheneveryrequiredpolicyexists,auserorSynthe-
1 system:
2 kind = "SingleInstance" sizer agent composes the target system through configuration
3 scheduler:
4 kind = "ChunkedPrefill" alone; when one is missing, Synthesizer agent implements
5 enable_prefix_caching = true only that policy behind its interface and reuses the remain-
(c) Compositional configuration ing components. An extension is thus a configuration edit
|      |             |        |                     |           |                 | or a component-local |     | implementation, |     |     | never a | control-layer |
| ---- | ----------- | ------ | ------------------- | --------- | --------------- | -------------------- | --- | --------------- | --- | --- | ------- | ------------- |
| Fig. | 5. Examples | of (a) | abstract interfaces | capturing | general serving | be-                  |     |                 |     |     |         |               |
rewrite.
haviors;(b)concreteimplementationsofinterfaceswithencapsulatedstates;
| and                           | (c) structured | configuration | composing | implementations | and | defining          |             |            |             |         |             |            |
| ----------------------------- | -------------- | ------------- | --------- | --------------- | --- | ----------------- | ----------- | ---------- | ----------- | ------- | ----------- | ---------- |
| component-specificparameters. |                |               |           |                 |     | D. Implementation |             |            |             |         |             |            |
|                               |                |               |           |                 |     | Built-in          | components. | We         | instantiate | the     | control     | layer with |
|                               |                |               |           |                 |     | seven component   |             | interfaces | that        | mirror  | a request’s | path       |
| C.                            | Modular        | Control       | Layer     |                 |     |                   |             |            |             |         |             |            |
|                               |                |               |           |                 |     | through           | a serving   | system,    | namely      | request | routing,    | system     |
Components own serving roles. The Dynamic DAG APIs orchestration, batch scheduling, model execution, model de-
define how the execution graph can grow at runtime, but not scription, and compute and network timing. This mirroring
whogrowsit.Asinglehandlermakingeveryservingdecision places every serving decision that a new mechanism may
wouldrecreateamonolithicpipelineabovetheexecutionlayer, change behind a distinct interface. Behind these interfaces,
forcing each new mechanism to modify shared control code. Simthesizer simulator ships built-in implementations covering
To address this, Simthesizer simulator partitions the control common serving configurations.
layer into components, each owning one serving role such At the system level, built-ins cover single- and multi-
as request routing, batch scheduling, or model execution. instance serving, prefill–decode disaggregation with explicit
Each component keeps its role’s policy state, handles that KV-cache handoff, and expert-parallel MoE serving, with
role’s logical nodes, and materializes its decisions through routing policies that place requests round-robin or by per-
theDynamicDAGAPIs.Thisownershipconfineseachpolicy instance load. Along the execution path, the built-in sched-
| change | to  | the component | that | makes the | decision. |                 |     |         |         |      |              |       |
| ------ | --- | ------------- | ---- | --------- | --------- | --------------- | --- | ------- | ------- | ---- | ------------ | ----- |
|        |     |               |      |           |           | uler implements |     | chunked | prefill | with | memory-aware | batch |
Interfaces capture stable roles. Serving roles remain sta- admission and block-aligned prefix caching, model runners
ble even as the policies filling them change rapidly; every expand each scheduled batch into layer-level compute and
serving system forms batches, but the batching policy evolves communication nodes under tensor or expert parallelism, and
with each new mechanism. Simthesizer simulator therefore model descriptions cover dense and MoE architectures. These
fixes each role’s operations in an interface and leaves pol- built-ins reduce common serving studies to configuration,
icy and state to concrete implementations. In Figure 5(a), reserving Synthesizer agent for new mechanisms.
System orchestrates one serving instance, handling its log- Pluggabletimingbackends.Theexecutionandcontrollayers
ical events through handle and emitting results through consume completion times without depending on how they
into_results.Schedulerownsiteration-levelbatching, are produced. This boundary lets detailed architecture and
enqueue_sub_request
receiving sub-requests through network simulators [12], [17], [36], [42] serve as backends
and returning the next batch through schedule. Because when their fidelity is required, while Simthesizer simulator
System depends only on this interface, any conforming provides lightweight defaults for end-to-end serving studies.
scheduler can fill the same position in the hierarchy. Profile-based compute backend. The default compute back-
Implementations encapsulate policy state. A policy is more end estimates each compute node’s latency from offline pro-
than a function; it carries state such as request queues, cache files[3],[6],[7],[22].Becauseasingletotal-tokenkeycannot
metadata, and tuning parameters. If this state leaked across capturelayerswhoselatencydependsonmorethanbatchsize,
components, replacing one policy would ripple through the the backend indexes each layer type with at most two layer-
others. Simthesizer simulator therefore confines each policy’s specific keys, such as the cached KV footprint and query–

|     |     |     |     |     |     |     |     | A. Simulator-Specific |     | Synthesis |     | Requirements |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --------- | --- | ------------ | --- | --- | --- |
User Prompt
Tools
“Add feature A” Synthesis begins when the user asks Synthesizer agent to
Search
❶
</> Bash      integrate a new serving mechanism. However, the initial re-
Human Synthesizer File  quest alone rarely resolves the modeling decisions needed for
|     |     | User |     | Agent |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
❷ ❷ MCP afaithfulimplementation,leavingperformance-criticalchoices
|     |     | Interrupt user for |     | ❸   | Add details using |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------------ | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
external tools implicit even though they directly affect simulation behavior.
options/details
|     |     |     |     |     |     |     |     | We identify | three | recurring | requirements |     | for | translating | the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | --------- | ------------ | --- | --- | ----------- | --- |
Spec. Document
 “Describes how the target system behaves” request into an implementation that captures the intention:
|     |     |     |     |     |     |     |     | • Semantic | completeness.Thesimulator-facingspecification |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
(a) /task-design
|     |     |     |     |     |     |     |     | must identify |     | the quantities |     | and assumptions |     | that | determine |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | -------------- | --- | --------------- | --- | ---- | --------- |
Spec. Document Spec. Document Impl. Map simulation time, resource contention, state lifetime, depen-
|     |                    |     |     |     |     |     |           | dency    | structure, | and  | metric    | boundaries. | Each | performance-      |     |
| --- | ------------------ | --- | --- | --- | --- | --- | --------- | -------- | ---------- | ---- | --------- | ----------- | ---- | ----------------- | --- |
|     | ❶ Expose relevant  |     |     | ❶   |     |     |           |          |            |      |           |             |      |                   |     |
|     | contexts           |     |     |     |     |     | Simulator |          |            |      |           |             |      |                   |     |
|     |                    |     |     |     |     |     |           | relevant | choice     | must | be either | resolved    | in   | the specification |     |
Impl. Codebase
Synthesizer ❷ Simulator Synthesizer ❷ or surfaced explicitly for human review.
Agent Codebase Agent Structural alignment. Each modeling decision must map
|     |                   |     |     |     | Validate |     |            | •   |     |     |     |     |     |     |     |
| --- | ----------------- | --- | --- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | Map decisions to  |     |     | ❸   |          |     | Guardrails |     |     |     |     |     |     |     |     |
❸ to the Simthesizer simulator abstraction responsible for the
implementation map
|     |     |     |     |     |     |     |     | corresponding |     | state | transition, | graph | update, | or  | resource |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----- | ----------- | ----- | ------- | --- | -------- |
Impl. Map
Simulator w/ New Feature A interaction. This mapping avoids scattering a mechanism
 “To Add Feature A, …”
(b) /sim-mapping (c) /sim-dev across unrelated control paths and preserves a traceable
|     |        |                                        |     |     |     |     |     | connection      | between   |     | the specification |     | and | the  | generated |
| --- | ------ | -------------------------------------- | --- | --- | --- | --- | --- | --------------- | --------- | --- | ----------------- | --- | --- | ---- | --------- |
|     | Fig.6. | Agent-drivensimulatorextensionprocess. |     |     |     |     |     | implementation. |           |     |                   |     |     |      |           |
|     |        |                                        |     |     |     |     |     | • Modeling      | fidelity. | The | implementation    |     |     | must | model the |
servingmechanismatthelevelofdetailrequiredbythetar-
| context | interaction |     | count for | attention | or  | the token | count and |     |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --------- | --------- | --- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
activated experts for MoE. The profiler samples these keys get performance question. When exact modeling is unavail-
|            |                  |         |          |            |         |         |         | able,       | it may | introduce   | approximations, |     | such    | as       | aggregate |
| ---------- | ---------------- | ------- | -------- | ---------- | ------- | ------- | ------- | ----------- | ------ | ----------- | --------------- | --- | ------- | -------- | --------- |
| offline    | and interpolates |         | over     | the table. |         |         |         |             |        |             |                 |     |         |          |           |
|            |                  |         |          |            |         |         |         | multipliers | or     | statistical | proxies.        | The | harness | requires | ex-       |
| Flow-based |                  | network | backend. | The        | default | network | backend |             |        |             |                 |     |         |          |           |
plicitassumptions,supportingevidence,andvaliditybound-
| models | communication |         | at    | flow granularity |          | rather  | than simu- |           |      |                |     |     |     |     |     |
| ------ | ------------- | ------- | ----- | ---------------- | -------- | ------- | ---------- | --------- | ---- | -------------- | --- | --- | --- | --- | --- |
|        |               |         |       |                  |          |         |            | aries for | each | approximation. |     |     |     |     |     |
| lating | individual    | packets | [22]; | each             | transfer | follows | a routed   |           |      |                |     |     |     |     |     |
path over a device–link connectivity graph and receives the B. Harnessed Lowering Process
| minimum | available |     | bandwidth | along | it. | When | a flow starts |        |         |               |     |          |        |     |         |
| ------- | --------- | --- | --------- | ----- | --- | ---- | ------------- | ------ | ------- | ------------- | --- | -------- | ------ | --- | ------- |
|         |           |     |           |       |     |      |               | Figure | 6 shows | Simthesizer’s |     | lowering | stages | for | meeting |
or completes, the backend recomputes the affected band- thesynthesisrequirements:task-design,sim-mapping,
| widths       | and reschedules |           | completion |        | events  | through | the event-    |              |           |            |           |        |                   |             |       |
| ------------ | --------------- | --------- | ---------- | ------ | ------- | ------- | ------------- | ------------ | --------- | ---------- | --------- | ------ | ----------------- | ----------- | ----- |
|              |                 |           |            |        |         |         |               | and sim-dev. |           | Each stage | addresses |        | a distinct        | requirement |       |
| invalidation |                 | interface | (Section   | IV-A). | Because |         | both backends |              |           |            |           |        |                   |             |       |
|              |                 |           |            |        |         |         |               | and produces | documents |            | that      | record | the corresponding |             | deci- |
sitbehindcomponentinterfaces,eithercanbereplacedwithout
|          |     |           |       |            |     |           |     | sions. This | linkage | routes | each | issue back | to  | the stage | where |
| -------- | --- | --------- | ----- | ---------- | --- | --------- | --- | ----------- | ------- | ------ | ---- | ---------- | --- | --------- | ----- |
| changing | the | execution | layer | or serving |     | policies. |     |             |         |        |      |            |     |           |       |
therelevantdecisionwasmade,ratherthantreatingeveryissue
|     |     |     |     |     |     |     |     | as an implementation |     | bug. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | ---- | --- | --- | --- | --- | --- |
(1)task-design.Thefirststagetargetssemanticcomplete-
|     |     | V.  | SYNTHESIZERAGENT |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
nessbyrefiningtheinitialuserrequestintoasimulator-facing
|     |     |     |     |     |     |     |     | specification. | Synthesizer |     | agent | consults | available | mechanism |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ----------- | --- | ----- | -------- | --------- | --------- | --- |
Grounded in Simthesizer simulator, Simthesizer translates descriptions,externalsources,andSimthesizersimulatorinter-
natural language specifications into executable simulation faces.Itspecifiesthetargetconfiguration,states,dependencies,
through agent-driven development that keeps pace with fast- metrics, and the assumptions and evidence for any approxi-
evolving serving mechanisms. Synthesizer agent realizes this mation.Theresultingspecificationdocumentrecordsresolved
lowering by wrapping a coding agent in a harness tailored to decisionsandexplicitmodelingboundariesandremainsinthe
developing LLM serving simulators, leveraging Simthesizer synthesis context throughout subsequent stages.
simulator’smodularinterfacestoextendthesimulatorwithout (2) sim-mapping.Thesecondstagetargetsstructuralalign-
reworking its internals. The harness makes simulator-specific mentbymappingthesimulator-facingspecificationtothecor-
constraints explicit and organizes synthesis around three in- responding Simthesizer simulator components and interfaces.
spectable artifacts: a specification, an implementation map, Theresultingimplementationmaprecordswherestateresides,
and a validation report. This design shifts human judgment which Dynamic DAG operations encode dependencies, which
from low-level code editing to resolving performance-critical components model compute and communication, and which
ambiguities and reviewing implementation decisions and val- observable signals support subsequent validation. Rather than
idation evidence. We first describe the synthesis requirements asequenceofcodeedits,themaptieseachmodelingdecision
andloweringprocess,thenpresenttwovalidationregimesand to the Simthesizer simulator abstraction responsible for the
their human review points. behavior, its implementation site, and its validation strategy.

TABLEII
[Target System Config]
scheduler = chunked_prefill + prefix_caching
IMPLEMENTATIONMAPFORSPECULATIVEDECODING.
speculative_width = K=2
[Modeling Input] Behavior Implementationmap
algorithm_reference = EAGLE-3
acceptance_model = empirical distribution Targetmodel RouteW throughtheexistingrequestrepresentation
sampling = stochastic verification tothemodelrunnerandcomputesimulator.
[Simulator Semantics]
Committedrequest AssignM toscheduler-managedrequestandKV
remaining_output = R
verification_width = W =min(K+1,R) state state,exposingonlythecommittedprefixtothe
accepted_drafts = A∼pacc existingcacheinterface.
committed_progress = M =A+1
target_compute = evaluate W positions Speculationround ReusethecommonDAGschedulingandexecution
persistent_state = advance and retain M tokens execution pathwithoutaddingamechanism-specificevent
[Validation Protocol] loop.
min_validation_step = 3
validation_data = ShareGPT trace, system data
crepancies, their possible sources, and the modeling decisions
Fig.7. Structuredsummaryofthedocumentproducedbytask-design. that require revision, providing concrete targets for the next
Thefullspecificationpresentsthesamecontentinnaturallanguage. synthesis run.
Reference-guided validation. When comparable measure-
(3) sim-dev. The third stage implements the changes de- ments are unavailable, as in cases involving unreleased hard-
scribed in the implementation map and checks for deviations. ware, unavailable software stacks, or novel mechanisms,
Synthesizer agent edits the simulator components and iterates Simthesizer performs reference-guided validation by ground-
on compiler diagnostics, runtime failures, test results, and ing its modeling decisions in available technical evidence.
violations of the specification. Simulator-specific guardrails Synthesizer agent derives performance criteria from reference
detect undeclared approximations, unexplained constants, and implementations, results reported in prior works, and other
code changes that depart from the implementation map. This evidence, then assesses whether the candidate simulator re-
stage records the implemented behavior, approximations, and produces the expected behavior under comparable conditions.
uncertainties in the validation report for human review. The validation report identifies evidence-grounded decisions,
Synthesis-time human involvement. Most revisions proceed unresolved assumptions, and approximations that define the
without continuous human intervention. Incorrect component validityboundary.Althoughthisregimedoesnotestablishem-
mappings rewind the lowering process to sim-mapping, pirical agreement with the target system, it provides traceable
while implementation bugs are resolved within sim-dev. technical justification and exposes the remaining uncertainty.
Duringtask-design,theavailablereferencesandsimulator
context may be insufficient to resolve a performance-critical
VI. SIMULATORSYNTHESISINACTION
modeling choice. In that case, Synthesizer agent requests We explain how Simthesizer’s two core components jointly
human clarification of the intended behavior, missing param- support a concrete simulator extension using EAGLE-style
eters, and modeling boundaries rather than silently selecting a speculative decoding [25] as a case study. This mechanism
default. At the end of the synthesis run, the user reviews the uses a lightweight drafter model to rapidly generate several
generated documents and, if necessary, revises the specifica- draft tokens. The target model then verifies drafted tokens in
tion and initiates another run. a single inference iteration, while only the accepted tokens
advancethegeneration.Althoughthismechanismisconciseat
C. Evidence-Guided Validation
the algorithmic level, its simulation must distinguish the work
The harnessed Synthesizer agent produces a candidate sim- performedbythetargetmodelfromtheprogressmadebyeach
ulator that is consistent with its specification and implemen- request. We trace the interaction of Simthesizer simulator and
tation map. However, this consistency does not guarantee that Synthesizeragentfromtheinitialuserrequestthroughseman-
the design itself faithfully captures the target mechanism. ticrefinement,lowering,andvalidation-drivenrevision.Across
Simthesizer addresses this gap through evidence-guided val- five synthesis runs, we follow a representative trial through
idation, which comprises the following two complementary specification, mapping, implementation, and validation.
regimes.
A. Resolving Simulator Semantics
Trace-guided validation. When real-system measurements
are available, Simthesizer compares the candidate simulator The initial user request states target algorithmic details
with the system under the same workload, serving config- including the number of draft tokens and the acceptance
urations, and hardware settings. It aligns internal execution model,butleavessomemodelingdecisionsunspecified.Based
signals,suchasqueuelength,batchcomposition,andresource on the reference and the supplied statistics, task-design
utilization, to identify the modeling decisions responsible for resolves these decisions into explicit simulator semantics. For
the observed discrepancies. Together with the implementation example, Synthesizer agent derives four semantic variables
map, these signals help associate each divergence with the from the algorithm reference: the verification width W, the
correspondingscheduling,compute,communication,ordepen- remaining output length R, the accepted draft length A, and
dencybehavior.Thevalidationreportrecordstheobserveddis- the committed request progress M. Figure 7 presents the

|                               |     |     |     |     |     |     | vLLM | Simthesizer |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | ---- | ----------- | --- | --- | --- | --- | --- | --- |
|                               | 500 |     |     |     |     |     |      | 1500        |     |     |     |     |     |     |
| )s/kot( tuphguorhT noitareneG |     |     |     |     |     |     |      | 1000        |     |     |     |     |     |     |
250
500
|     | 0   |     |     |     |     |     |     | 0   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0 30 60 90 120 150 180 210 240 0 30 60 90 120 150 180 210 240
|     |     |     |     | Time (s)      |     |     |     |     |     |               | Time (s) |     |     |     |
| --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | ------------- | -------- | --- | --- | --- |
|     |     |     |     | (a) Dense-SWE |     |     |     |     |     | (b) Dense-tau |          |     |     |     |
|     | 900 |     |     |               |     |     |     | 900 |     |               |          |     |     |     |
|     | 600 |     |     |               |     |     |     | 600 |     |               |          |     |     |     |
|     | 300 |     |     |               |     |     |     | 300 |     |               |          |     |     |     |
|     | 0   |     |     |               |     |     |     | 0   |     |               |          |     |     |     |
0 30 60 90 120 150 180 210 240 0 30 60 90 120 150 180 210 240
|     |     |     |     | Time (s)    |     |     |     |     |     |             | Time (s) |     |     |     |
| --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | ----------- | -------- | --- | --- | --- |
|     |     |     |     | (c) MoE-SWE |     |     |     |     |     | (d) MoE-tau |          |     |     |     |
Fig.8. ComparisonofthroughputbetweenunmodifiedSimthesizer(withoutanyagent-synthesizedextension)andaGPU-basedservingsystemrunningvLLM
underagenticworkloads:(a)Llama3.1densemodelonmini-SWE-bench,(b)Llama3.1densemodelontau-bench,(c)Qwen3MoEmodelonmini-SWE-bench,
and(d)Qwen3MoEmodelontau-bench.
examplespecificationdocumentgeneratedbytask-design communication. The validation evidence isolated the problem
from an underspecified user request, capturing the resulting to the verification-width semantics rather than the component
modeling decisions and state semantics. mapping or DAG execution path.
|         |         |     |                |     |     |     |     | The validation |     | report | fed this | finding | back to Synthesizer |     |
| ------- | ------- | --- | -------------- | --- | --- | --- | --- | -------------- | --- | ------ | -------- | ------- | ------------------- | --- |
| B. From | Mapping | to  | Implementation |     |     |     |     |                |     |        |          |         |                     |     |
agent,whichinitiatedanotheriterationtocorrectthesemantic
sim-mapping maps the simulator-facing specification error. With the corrected semantics, the subsequent candidate
onto the Simthesizer simulator components and interfaces, showed a 6.7% throughput divergence from the real system
recording the resulting mappings in an implementation map andunderestimatedaggregatethroughputonlyby4.7%onthe
for subsequent simulator development. Rather than adding samevalidationtrace.Thiscasestudyshowshowtrace-guided
mechanism-specific machinery, Synthesizer agent localizes validation converts a simulation discrepancy into a semantic
extension logic within existing Simthesizer simulator com- correction while preserving the localized integration design.
| ponents | and minimizes |     | the | required | changes. | For | example, |     |     |     |     |     |     |     |
| ------- | ------------- | --- | --- | -------- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
D. Joint Effect
| in speculative |     | decoding, | the | map | incorporates | simulator | se- |     |     |     |     |     |     |     |
| -------------- | --- | --------- | --- | --- | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
mantics, W and M, into the existing request-processing and Simthesizer simulator provides reusable components for
scheduling,compute,cachemanagement,andDAGexecution,
| scheduling | mechanisms, |           | while | reusing | the           | common | DAG      |                   |     |       |      |                |          |      |
| ---------- | ----------- | --------- | ----- | ------- | ------------- | ------ | -------- | ----------------- | --- | ----- | ---- | -------------- | -------- | ---- |
|            |             |           |       |         |               |        |          | while Synthesizer |     | agent | maps | underspecified | behavior | onto |
| scheduling | and         | execution | path. | Table   | II summarizes |        | this re- |                   |     |       |      |                |          |      |
thesecomponents.Inthisspeculativedecodingcase,thiscom-
sulting map.
|     |     |     |     |     |     |     |     | bination | localizes | mechanism-specific |     | logic | to the acceptance |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --------- | ------------------ | --- | ----- | ----------------- | --- |
Duringthesim-devstage,Synthesizeragenttranslatesthe
mapped design into localized simulator code changes guided policyandscheduler,preservessharedexecutionandresource-
modelingpaths,andlinksobservedperformancediscrepancies
bytheimplementationmap.Theresultingextensionintroduces
toconcretemodelingdecisions.Together,thetwocomponents
| no new           | events,     | node      | types,   | graph      | APIs, model-runner |        | paths,      |                |                |                |             |            |               |     |
| ---------------- | ----------- | --------- | -------- | ---------- | ------------------ | ------ | ----------- | -------------- | -------------- | -------------- | ----------- | ---------- | ------------- | --- |
|                  |             |           |          |            |                    |        |             | of Simthesizer |                | make simulator |             | extension  | compositional | and |
| compute          | interfaces, | cache     | APIs,    | or         | execution          | loops, | leaving     |                |                |                |             |            |               |     |
|                  |             |           |          |            |                    |        |             | reviewable,    | exposing       | each           | extension’s | semantics, | integration   |     |
| most Simthesizer |             | simulator |          | components | unchanged.         |        | Overall,    |                |                |                |             |            |               |     |
|                  |             |           |          |            |                    |        |             | choices,       | and validation |                | evidence    | to human   | review.       |     |
| Simthesizer’s    | harnessed   |           | lowering | process    |                    | allows | Synthesizer |                |                |                |             |            |               |     |
agent to focus on the algorithmic details and state semantics VII. EVALUATION
| specific | to speculative |         | decoding,    | while | Simthesizer |      | simulator |                |     |         |      |            |          |         |
| -------- | -------------- | ------- | ------------ | ----- | ----------- | ---- | --------- | -------------- | --- | ------- | ---- | ---------- | -------- | ------- |
|          |                |         |              |       |             |      |           | Our evaluation |     | answers | five | questions: | (Q1) Can | Simthe- |
| supports | them           | through | its reusable |       | components, | cost | models,   |                |     |         |      |            |          |         |
sizeraccuratelymodelcomplexworkloadssuchasagentserv-
and interfaces.
|                      |     |              |          |               |     |           |       | ing? (Q2)        | Can       | Simthesizer    | faithfully | implement     | features  | not  |
| -------------------- | --- | ------------ | -------- | ------------- | --- | --------- | ----- | ---------------- | --------- | -------------- | ---------- | ------------- | --------- | ---- |
|                      |     |              |          |               |     |           |       | natively         | supported | by Simthesizer |            | simulator,    | and how   | much |
| C. Validation-Driven |     |              | Revision |               |     |           |       |                  |           |                |            |               |           |      |
|                      |     |              |          |               |     |           |       | does Simthesizer |           | simulator      | contribute | to simulation | accuracy? |      |
| The synthesis        |     | run produces |          | an executable |     | candidate | simu- |                  |           |                |            |               |           |      |
(Q3)HowmuchdoestheSynthesizeragentharnesscontribute
| lator. In | this representative |     | run, | trace-guided |     | validation | found |     |     |     |     |     |     |     |
| --------- | ------------------- | --- | ---- | ------------ | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
toaccuracy?(Q4)HowfastdoesSimthesizerrunLLMserving
| that the | candidate | overestimated |        | target     | system | throughput        | by  |              |      |      |              |        |           |        |
| -------- | --------- | ------------- | ------ | ---------- | ------ | ----------------- | --- | ------------ | ---- | ---- | ------------ | ------ | --------- | ------ |
|          |           |               |        |            |        |                   |     | simulations? | (Q5) | Does | the workflow | remain | effective | across |
| 13.4% on | the       | validation    | trace. | Inspecting |        | its specification |     |              |      |      |              |        |           |        |
coding agents?
| and computation |     | trace | revealed | that | the | synthesized | imple- |     |     |     |     |     |     |     |
| --------------- | --- | ----- | -------- | ---- | --- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- |
A. Methodology
| mentation | applied | W   | only | to the | final layer | and | modeled |     |     |     |     |     |     |     |
| --------- | ------- | --- | ---- | ------ | ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
the remaining target model layers over K positions, causing Baselines. We compare Simthesizer against two state-of-
the candidate to underestimate the required compute and the-art LLM serving simulators: LLMServingSim2.0 [6] and

4K 4K 9K
3K 3K 6K
2K 2K
1K 1K 3K
0 0 0
0 25 50 75 100 0 25 50 75 100 0 25 50 75 100
Time (s) Time (s) Time (s)
(a) KV Cache Quantization (b) Speculative Decoding (c) Hybrid-Mamba
noitareneG
)s/kot(
tuphguorhT
vLLM Simthesizer LLMServingSim2.0 Vidur
Fig.9. ThroughputcomparisonofSimthesizer,LLMServingSim2.0,andVidureachindependentlyextendedbytheSynthesizeragentunderasharedharness
andcodingagentacrossthreefeature-extensiontasks:(a)KVcachequantization,(b)speculativedecoding,and(c)hybridMambamodelsupport.Eachpanel
thuscomparesthreedistinctsimulatorsextendedwiththesamefeature;thesameconventionappliestoFig.10andFig.11.
Vidur[1].Toevaluateagent-drivensimulatorextension,wede- TABLEIII
fine three feature-extension tasks unsupported by Simthesizer ERRORRATESOFSIMTHESIZERPERFORMANCEMETRICSRELATIVETO
THEREALSERVINGSYSTEMACROSSTWOWORKLOADSANDTWO
simulator and both baselines: (1) FP8 KV cache quantization,
MODELS.
(2) EAGLE3-based speculative decoding [25], and (3) hybrid
Mamba model support. We use the Qwen3 32B model [47] mini-SWE-agent tau-bench
Error rate (%)
for the first two tasks and the Nemotron-3-Nano 30B-A3B Llama3.1-8B Qwen3-30B Llama3.1-8B Qwen3-30B
model [31] for the hybrid Mamba task. Within Simthesizer, Mean TTFT 4.10 19.83 17.23 21.87
Median TTFT 0.64 4.72 6.09 0.13
Synthesizer agent adds each requested feature directly to
Mean TPOT 0.27 2.82 0.93 4.16
Simthesizer simulator; for each baseline, the same coding
Median TPOT 0.40 1.45 0.40 0.28
agent and harness add the same mechanism to the simulator’s Mean ITL 0.97 2.17 0.74 3.74
native implementation. We repeat each extension task over Median ITL 0.65 14.75 11.44 11.94
multiple independent trials without human intervention and Throughput 0.20 2.78 0.51 4.54
Running Time 0.20 2.71 0.51 4.34
report metrics averaged across trials to account for coding-
agent variability.
For the dense model (Figure 8(a) and (b)), the simulation
Synthesizer agent setup. Unless otherwise specified, we use
closely matches the real system, as dense execution is largely
GPT-5.4(xhigh),accessedthroughOpenAICodex(v0.118.0),
deterministic. For the MoE model (Figure 8(c) and (d)), the
as Synthesizer agent. Importantly, the Synthesizer agent har-
simulated throughput deviates more visibly. This discrepancy
nessdoesnotencodeanySimthesizer-specificinformation.For
arisesfromthestatisticalmodelingofMoErouting;expertse-
faircomparison,weprovideallthreesimulatorswithidentical
lection and synchronization under data and expert parallelism
prompts, references, specifications, and profiled model data.
areestimatedfromprofiledstatisticsratherthanactualrequest-
Workloads and datasets. We sample 50–100 requests from
specific routing decisions. Nevertheless, Simthesizer captures
SWE-bench [15] and tau-bench [50], which are agentic work-
the interaction between LLM generation and tool calls and
loads, and we sample 400 requests from ShareGPT [38] as
closely follows the real system’s performance trends.
a non-agentic workload. For agentic workloads, we collect
Table III reports the error rates of Simthesizer for TTFT,
output and tool-call trajectories from a real system matching
TPOT, and ITL. TTFT and ITL exhibit higher errors than
the simulated environment and replay them in the simulator.
TPOT because real systems involve tail-latency factors, such
System specifications. We conduct all experiments on a
as network traffic and kernel launch delays, that are dif-
machineequippedwithtwoNVIDIARTXPro6000Blackwell
ficult to simulate precisely. TPOT, which primarily reflects
GPUs and an Intel Xeon Gold 6326 CPU. We use vLLM
generation-phase latency, shows lower error, indicating that
(v0.19.1) as the LLM serving framework when evaluating the
Simthesizeraccuratelymodelsbatchingandscheduling,where
real GPU-based serving system [20].
these system-level effects are less dominant. Despite these
B. Evaluation Results hard-to-simulate system-level effects, Simthesizer closely re-
(Q1) Complex-workload fidelity. We evaluate whether produces the real system’s overall behavior across all metrics,
Simthesizercapturesdynamicandcomplexworkloadbehavior workloads, and models.
by comparing it against a real GPU-based serving system (Q2) Extension fidelity. We next evaluate the three feature-
running vLLM on mini-SWE-bench and tau-bench. Both extension tasks that Synthesizer agent adds to Simthesizer
benchmarks define their agentic workflows in a pre-defined simulatorandtoeachbaselinesimulator.Figure9presentsthe
form, which Simthesizer models directly as multiple model generation throughput, and Figure 10 shows the error rates of
invocations interleaved with tool calls. For each tool call, we key performance metrics across the three simulators.
executeitonthehostinadvanceandrecorditslatency,which ForKVcachequantization,allsimulatorsachievelowerror
the simulation replays at the corresponding stage. Figure 8 rates because the task primarily requires tracking memory
illustrates the generation throughput over 240 seconds for the usage and modeling quantization overhead. In contrast, spec-
Llama3.18Bdensemodel[29]andtheQwen330B-A3BMoE ulative decoding and hybrid Mamba support require coordi-
model [47]. nated changes across execution scheduling, model structure,

TABLEIV
ERRORRATESOFSIMTHESIZERWITHANDWITHOUTTHESYNTHESIZER
100
AGENTHARNESS,RELATIVETOTHEREALVLLM-BASEDSERVING
80
SYSTEM. 60
40
Error rate (%) Throughput TTFT TPOT ITL 20
Without Harness 4.70 10.73 5.71 11.05 0
With Harness 2.84 4.52 1.55 5.28
Throughput TTFT TPOT
T
I
h
T
r
L oughput TTFT TPOT
T
I
h
T
r
L oughput TTFT TPOT ITL
and performance modeling. For these two tasks, Simthesizer
consistently achieves the highest accuracy, whereas the base-
lines exhibit substantially larger errors. This difference arises
because Simthesizer simulator’s modular interfaces localize
each extension, while the fixed pipelines of existing simu-
lators require changes across tightly coupled components to
represent interactions among Mamba, MoE, and transformer
layers.
Because the coding agent, harness, specifications, and pro-
filing data are identical across all three systems, the accuracy
differenceisolatesthecontributionoftheunderlyingsimulator.
Overall, Simthesizer achieves an average throughput error of
2.51%, whereas the baseline-built extensions exhibit 6.03%,
showing that Simthesizer faithfully adds functionality absent
fromSimthesizersimulatorandthatSimthesizersimulatorpro-
vides a more effective foundation for agent-driven extension.
(Q3) Impact of the Synthesizer agent harness. Table IV
comparesSimthesizerafterSynthesizeragentaddsspeculative
decoding with and without its harness, using the ShareGPT
workload and the Qwen3 32B model. Without the harness,
simulation error rises by 1.65×–3.69× across throughput
and latency metrics. This occurs because the coding agent
frequentlyomitscriticalsystemdetailsandproceedstoimple-
mentation despite insufficient specifications. In contrast, the
harness supplies a knowledge base, blocks implementation
until required specifications are resolved, and enforces self-
validation through its verification loop. Because this com-
parison holds Simthesizer simulator, the coding agent, and
all inputs fixed, the error reduction quantifies the harness’s
contribution to accuracy.
(Q4) Simulation speed. Figure 11 compares the execution
time of Simthesizer, LLMServingSim2.0, and Vidur across
the three extension tasks under the ShareGPT workload.
Simthesizer runs on average 164.9× (up to 284.96×) faster
than LLMServingSim2.0 and 6.65× (up to 23.19×) faster
thanVidur.Thisgaparisesfromhoweachextensionisimple-
mented.Existingsimulatorsexposenomodularboundariesfor
new mechanisms, so extension logic is built directly into their
simulation pipelines, adding overhead to every simulated iter-
ation. In contrast, on Simthesizer, the same extensions remain
confined to localized component changes behind Simthesizer
simulator’sinterfaces,leavingtheexecutionengineuntouched.
ForhybridMamba,Simthesizertakeslongerthanontheother
tasks because Simthesizer simulator normally simulates one
transformerlayerandreusesitslatencyacrossrepeatedlayers,
whereas the heterogeneous layers of hybrid Mamba leads
Simthesizersimulatortosimulateeverylayerindividually.Ex-
plicitrequestofthisreusewouldfurtherreducethesimulation
)%(
etar
rorrE
KV Quant Speculative Hybrid-Mamba
(a) Mean
80
60
40
20
0
TTFT TPOT ITL TTFT TPOT ITL TTFT TPOT ITL
)%(
etar
rorrE
Simthesizer LLMServingSim2.0 Vidur
KV Quant Speculative Hybrid-Mamba
(b) Median
Fig. 10. Error rate comparison of (a) mean and (b) median performance
metricsforSimthesizer,LLMServingSim2.0,andViduracrossthreefeature-
extensiontasksunderasharedharnessandcodingagent.
2400
2200
50
25
0
KV Quant Speculative Hybrid-Mamba
)s(
emit
noitalumiS
Simthesizer LLMServingSim2.0 Vidur
2326
429 225
33
19 23
Fig.11. ComparisonofsimulationtimeforSimthesizer,LLMServingSim2.0,
andViduracrossthreefeature-extensiontasks.
time, yet even without it, Simthesizer models hybrid Mamba
more accurately than both baselines.
(Q5)Coding-agentgenerality.Figure12comparesthegener-
ationthroughputofvLLMwiththatofthesimulatorsproduced
by Codex and Claude Code (Opus 4.7 high, v2.1.204) for
speculative decoding. Both simulators closely follow the real-
system trajectory, achieving average error rates of 4.1% and
4.9%, respectively, across throughput, TTFT, TPOT, and ITL.
This generality follows from the agent- and LLM-agnostic
harness design, which relies on no agent-specific tools or
prompting strategies and applies the same specification-to-
implementation and validation workflow to any coding agent.
These results show that Synthesizer agent generalizes beyond
Codex, guiding different coding agents to faithful extensions.
VIII. RELATEDWORK
LLM and system simulators. ADOR [18], ONNXim [11],
LLMCompass [55], and PyTorchSim [49] simulate LLM
workloadsatthehardwareleveltoexplorearchitecturaldesign
spaces. At the system level, Vidur [1], APEX [28], and
LLMServingSim2.0 [6] model LLM serving across nodes and
devices, while vTrain [3], TrioSim [22], and Multiverse [10]
target distributed training. Across all these levels, however,
human developers implement system behavior in advance and
fixitintoasimulationpipeline,soeveryemergingmechanism

vLLM Simthesizer (Codex) Simthesizer (Claude) [6] J. Cho, H. Choi, G. Heo, and J. Park, “LLMServingSim 2.0: A
|     |     |     |     |     |     |     | Unified | Simulator | for Heterogeneous |     | and | Disaggregated |     | LLM Serving |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | ----------------- | --- | --- | ------------- | --- | ----------- |
)s/kot( tuphguorhT 3K
Infrastructure,”inISPASS,2026.
noitareneG
2K [7] J. Cho, M. Kim, H. Choi, G. Heo, and J. Park, “LLMServingSim: A
|     |     |     |     |     |     |     | HW/SW | Co-Simulation |     | Infrastructure |     | for LLM | Inference | Serving at |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------------- | --- | -------------- | --- | ------- | --------- | ---------- |
Scale,”inIISWC,2024.
1K
|     |     |     |     |     |     |     | [8] B. Gao, | Z.  | He, P. Sharma, | Q.  | Kang, | D. Jevdjic, | J. Deng, | X. Yang, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------------- | --- | ----- | ----------- | -------- | -------- |
0 Z. Yu, and P. Zuo, “Cost-Efficient Large Language Model Serving for
|     | 0   | 20 40 | 60  | 80 100 | 120 | 140 160 |     |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | ------ | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Multi-turnConversationswithCachedAttention,”inATC,2024.
Time (s)
[9] I.Gim,Z.Ma,S.-s.Lee,andL.Zhong,“Pie:AProgrammableServing
Fig.12. GenerationthroughputcomparisonbetweenvLLMandthesimulators SystemforEmergingLLMApplications,”inSOSP,2025.
producedbyCodexandClaudeCodeforspeculativedecoding. [10] F.Gui,K.Gao,L.Chen,D.Li,V.Liu,R.Zhang,H.Yang,andD.Xiong,
“AcceleratingdesignspaceexplorationforLLMtrainingsystemswith
multi-experimentparallelsimulation,”inNSDI,2025.
| triggers | another      | round       | of manual | restructuring |     | and revalida-    |              |     |          |          |      |         |         |              |
| -------- | ------------ | ----------- | --------- | ------------- | --- | ---------------- | ------------ | --- | -------- | -------- | ---- | ------- | ------- | ------------ |
|          |              |             |           |               |     |                  | [11] H. Ham, | W.  | Yang, Y. | Shin, O. | Woo, | G. Heo, | S. Lee, | J. Park, and |
| tion.    | In contrast, | Simthesizer |           | composes      | the | complete serving |              |     |          |          |      |         |         |              |
G.Kim,“ONNXim:AFast,Cycle-LevelMulti-CoreNPUSimulator,”
IEEEComputerArchitectureLetters,vol.23,no.2,pp.219–222,2024.
| workflow       | from | uniform | elements   | of  | a unified | dynamic DAG,   |            |            |            |     |           |            |     |            |
| -------------- | ---- | ------- | ---------- | --- | --------- | -------------- | ---------- | ---------- | ---------- | --- | --------- | ---------- | --- | ---------- |
|                |      |         |            |     |           |                | [12] T. R. | Henderson, | M. Lacage, | G.  | F. Riley, | C. Dowell, | and | J. Kopena, |
| and integrates |      | new     | mechanisms | by  | adding    | and connecting |            |            |            |     |           |            |     |            |
“Networksimulationswiththens-3simulator,”SIGCOMMdemonstra-
| nodes | through | agent-driven | lowering. |     |     |     |     |     |     |     |     |     |     |     |
| ----- | ------- | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tion,vol.14,no.14,p.527,2008.
AI agents for systems research. KNighter [48] synthesizes [13] S.Hong,M.Zhuge,J.Chen,X.Zheng,Y.Cheng,J.Wang,C.Zhang,
|                 |     |           |          |     |               |            | Z. Wang, | S.  | K. S. Yau, | Z. Lin, | L. Zhou, | C.  | Ran, L. | Xiao, C. Wu, |
| --------------- | --- | --------- | -------- | --- | ------------- | ---------- | -------- | --- | ---------- | ------- | -------- | --- | ------- | ------------ |
| static-analysis |     | checkers, | AIOpsLab |     | [4] evaluates | agents for |          |     |            |         |          |     |         |              |
andJ.Schmidhuber,“MetaGPT:MetaProgrammingforAMulti-Agent
autonomous cloud operation, LOOPRAG [57] and LLM- CollaborativeFramework,”inICLR,2024.
Vectorizer[43]vectorizeloops,andCUDAForge[56]andKer- [14] J. Jeong and J. Ahn, “Accelerating LLM Serving for Multi-turn Dia-
nelEvolve [26] generate and optimize GPU kernels. Simthe- logueswithEfficientResourceManagement,”inASPLOS,2025.
|     |     |     |     |     |     |     | [15] C. E. | Jimenez, | J. Yang, | A. Wettig, | S.  | Yao, | K. Pei, | O. Press, and |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | -------- | ---------- | --- | ---- | ------- | ------------- |
sizer further demonstrates that coding agents can be applied K. Narasimhan, “Swe-bench: Can language models resolve real-world
to develop an LLM serving simulator, showing the feasibility github issues?” in International Conference on Learning Representa-
tions,vol.2024,2024,pp.54107–54157.
ofagent-baseddevelopmentandoptimizationthroughartifacts
|     |     |     |     |     |     |     | [16] A. K. | Kamath, | R. Prabhu, | J.  | Mohan, | S. Peter, | R.  | Ramjee, and |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ---------- | --- | ------ | --------- | --- | ----------- |
and workflows co-designed for agents. A. Panwar, “POD-Attention: Unlocking Full Prefill-Decode Overlap
|     |     |     |     |     |     |     | for | Faster LLM | Inference,” | in  | ASPLOS, | 2025. | [Online]. | Available: |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | --- | ------- | ----- | --------- | ---------- |
IX. CONCLUSION https://asplos-conference.org/asplos2025/program.html
|     |     |     |     |     |     |     | [17] M. Khairy, |     | Z. Shen, T. | M. Aamodt, | and | T. G. | Rogers, | “Accel-Sim: |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ----------- | ---------- | --- | ----- | ------- | ----------- |
ThispaperpresentsSimthesizer,aframeworkfordeveloping AnExtensibleSimulationFrameworkforValidatedGPUModeling,”in
ISCA,2020.
| LLM            | serving | simulators | that        | keep | pace with  | fast-evolving, |              |     |                    |          |           |     |           |              |
| -------------- | ------- | ---------- | ----------- | ---- | ---------- | -------------- | ------------ | --- | ------------------ | -------- | --------- | --- | --------- | ------------ |
|                |         |            |             |      |            |                | [18] J. Kim, | H.  | Lee, G. Ko,        | G. Choi, | S. Ham,   | S.  | Hong, and | J.-Y. Kim,   |
| non-monolithic |         | serving.   | Simthesizer |      | introduces | a composable   |              |     |                    |          |           |     |           |              |
|                |         |            |             |      |            |                | “ADOR:       | A   | Design Exploration |          | Framework | for | LLM       | Serving with |
simulator infrastructure that uniformly expresses the complete EnhancedLatencyandThroughput,”inISPASS,2025.
serving workflow, including its control decisions, realized as [19] W. Kim, Y. Lee, Y. Kim, J. Hwang, S. Oh, J. Jung, A. Huseynov,
W.G.Park,C.H.Park,D.Mahajan,andJ.Park,“Pimba:AProcessing-
a unified dynamic DAG (Simthesizer simulator), and lowers in-Memory Acceleration for Post-Transformer Large Language Model
high-level specifications into executable extensions through a Serving,”inMICRO,2025.
harnessed coding agent (Synthesizer agent). Extensions syn- [20] W.Kwon,Z.Li,S.Zhuang,Y.Sheng,L.Zheng,C.H.Yu,J.Gonzalez,
|     |     |     |     |     |     |     | H. Zhang, | and | I. Stoica, | “Efficient | Memory | Management |     | for Large |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------- | ---------- | ------ | ---------- | --- | --------- |
thesizedonSimthesizerachieveanaveragethroughputerrorof LanguageModelServingwithPagedAttention,”inSOSP,2023.
2.51%,comparedwith6.03%forthesameextensionsbuilton [21] Y. Leviathan, M. Kalman, and Y. Matias, “Fast Inference from Trans-
formersviaSpeculativeDecoding,”inICML,2023.
| existing | simulators, | while | simulating |     | up to | 23.19×–284.96× |     |     |     |     |     |     |     |     |
| -------- | ----------- | ----- | ---------- | --- | ----- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
[22] Y.Li,Y.Bao,G.Wang,X.Mei,P.Vaid,A.Ghosh,A.Jog,D.Bunandar,
faster.Theseresultssuggestthatpairingcomposablesimulator
|     |     |     |     |     |     |     | A. Joshi, | and | Y. Sun, | “TrioSim: | A Lightweight |     | Simulator | for Large- |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | --------- | ------------- | --- | --------- | ---------- |
infrastructurewithagent-drivenloweringoffersascalablepath ScaleDNNWorkloadsonMulti-GPUSystems,”inISCA,2025.
[23] Y.Li,F.Wei,C.Zhang,andH.Zhang,“EAGLE-2:FasterInferenceof
| toward | building | simulators | in  | other | rapidly | evolving systems |     |     |     |     |     |     |     |     |
| ------ | -------- | ---------- | --- | ----- | ------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
LanguageModelswithDynamicDraftTrees,”inEMNLP,2024.
domains.
[24] Y.Li,F.Wei,C.Zhang,andH.Zhang,“EAGLE:SpeculativeSampling
RequiresRethinkingFeatureUncertainty,”inICML,2024.
REFERENCES [25] Y.Li,F.Wei,C.Zhang,andH.Zhang,“EAGLE-3:ScalingupInference
|                                                               |     |     |     |     |     |     | Acceleration  |     | of Large | Language | Models | via Training-Time |     | Test,” in |
| ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------- | --- | -------- | -------- | ------ | ----------------- | --- | --------- |
| [1] A.Agrawal,N.Kedia,J.Mohan,A.Panwar,N.Kwatra,B.S.Gulavani, |     |     |     |     |     |     | NeurIPS,2025. |     |          |          |        |                   |     |           |
R.Ramjee,andA.Tumanov,“VIDUR:ALARGE-SCALESIMULA- [26] G.Liao,H.Qin,Y.Wang,A.Golden,M.Kuchnik,Y.Yetim,J.J.Ang,
TIONFRAMEWORKFORLLMINFERENCE,”inMLSys,2024. C. Fu, Y. He, S. Hsia, Z. Jiang, D. Li, U. Pashkevich, V. Puvvada,
[2] A.Agrawal,N.Kedia,A.Panwar,J.Mohan,N.Kwatra,B.S.Gulavani, F. Shi, M. Steiner, R. Xiao, N. Yan, X. Yu, Z. Fang, R. Levenstein,
A.Tumanov,andR.Ramjee,“TamingThroughput-LatencyTradeoffin K. Ho, H. Zhu, A. Hammond, R. Li, A. Mathews, K. Gondkar,
LLMInferencewithSarathi-Serve,”OSDI,2024. A. Zainul-Abedin, K. Singh, H. Yu, W. Chi, B. Huang, S. Zhang,
[3] J.Bang,Y.Choi,M.Kim,Y.Kim,andM.Rhu,“vTrain:ASimulation N.Weller,Z.Marine,W.Cook,C.-J.Wu,andG.Liu,“KernelEvolve:
Framework for Evaluating Cost-Effective and Compute-Optimal Large Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at
LanguageModelTraining,”inMICRO,2024. Meta,”2026.[Online].Available:https://arxiv.org/abs/2512.23236
[4] Y. Chen, M. Shetty, G. Somashekar, M. Ma, Y. Simmhan, J. Mace, [27] C. Lin, Z. Han, C. Zhang, Y. Yang, F. Yang, C. Chen, and L. Qiu,
C.Bansal,R.Wang,andS.Rajmohan,“AIOpsLab:AHolisticFrame- “Parrot: Efficient Serving of LLM-based Applications with Semantic
work to Evaluate AI Agents for Enabling Autonomous Clouds,” in Variable,”inOSDI,2024.
MLSys,2025. [28] Y.-C. Lin, W. Kwon, R. Pineda, and F. N. Paravecino, “APEX:
[5] E.Cho,J.Bang,R.Hwang,andM.Rhu,“PASCAL:APhase-Aware An Extensible and Dynamism-Aware Simulator for Automated
Scheduling Algorithm for Serving Reasoning-based Large Language Parallel Execution in LLM Serving,” 2025. [Online]. Available:
| Models,”inHPCA,2026. |     |     |     |     |     |     | https://arxiv.org/abs/2411.17651 |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- |

[29] Meta AI, “Llama 3.1 8B Instruct,” https://huggingface.co/meta-llama/ [52] X. Yao, Q. Hu, and A. Klimovic, “DeltaZip: Efficient Serving of
Llama-3.1-8B-Instruct,Jul.2024,accessed:2026-04-09. MultipleFull-Model-TunedLLMs,”inEuroSys,2025.
[30] X.Miao,G.Oliaro,Z.Zhang,X.Cheng,Z.Wang,Z.Zhang,R.Y.Y. [53] G.-I. Yu, J. S. Jeong, G.-W. Kim, S. Kim, and B.-G. Chun, “Orca: A
Wong, A. Zhu, L. Yang, X. Shi, C. Shi, Z. Chen, D. Arfeen, R. Ab- DistributedServingSystemforTransformer-BasedGenerativeModels,”
| hyankar, | and | Z. Jia, | “SpecInfer: | Accelerating |     | Large Language |     | Model | inOSDI,2022. |     |     |     |     |     |     |
| -------- | --- | ------- | ----------- | ------------ | --- | -------------- | --- | ----- | ------------ | --- | --- | --- | --- | --- | --- |
[54] L.Yu,J.Lin,andJ.Li,“StatefulLargeLanguageModelServingwith
| Serving      | with | Tree-based | Speculative |     | Inference | and | Verification,” | in  |                           |     |     |     |     |     |     |
| ------------ | ---- | ---------- | ----------- | --- | --------- | --- | -------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
| ASPLOS,2024. |      |            |             |     |           |     |                |     | Pensieve,”inEuroSys,2025. |     |     |     |     |     |     |
[31] NVIDIA Corporation, “NVIDIA Nemotron-3 Nano 30B A3B [55] H. Zhang, A. Ning, R. B. Prabhakar, and D. Wentzlaff, “LLMCom-
BF16,” https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B- pass: Enabling Efficient Hardware Design for Large Language Model
A3B-BF16,Dec.2025,accessed:2026-04-09. Inference,”inISCA,2025.
|     |     |     |     |     |     |     |     |     | [56] Z. Zhang, | R. Wang, | S. Li, | Y. Luo, | M. Hong, | and | C. Ding, |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | -------- | ------ | ------- | -------- | --- | -------- |
[32] G.Oliaro,Z.Jia,D.F.Campos,andA.Qiao,“SuffixDecoding:Extreme
SpeculativeDecodingforEmergingAIApplications,”inNeurIPS,2025. “CudaForge:AnAgentFrameworkwithHardwareFeedbackforCUDA
[33] OpenAI,“Codex,”https://openai.com/codex/,2025. KernelOptimization,”arXivpreprintarXiv:2511.01884,2025.[Online].
[34] P. Patel, E. Choukse, C. Zhang, A. Shah, I. n. Goiri, S. Maleki, and Available:https://arxiv.org/abs/2511.01884
R. Bianchini, “Splitwise: Efficient Generative LLM Inference Using [57] Y. Zhi, Y. Cao, J. Dai, X. Han, J. Pu, Q. Wu, S. Cheng, and
|     |     |     |     |     |     |     |     |     | M. Cai, | “LOOPRAG: | Enhancing | Loop Transformation |     | Optimization |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --------- | ------------------- | --- | ------------ | --- |
PhaseSplitting,”inISCA,2024.
[35] R.Prabhu,A.Nayak,J.Mohan,R.Ramjee,andA.Panwar,“vAttention: withRetrieval-AugmentedLargeLanguageModels,”inASPLOS,2026.
DynamicMemoryManagementforServingLLMswithoutPagedAtten- [58] Y.Zhong,S.Liu,J.Chen,J.Hu,Y.Zhu,X.Liu,X.Jin,andH.Zhang,
tion,”inASPLOS,2025. “DistServe:DisaggregatingPrefillandDecodingforGoodput-optimized
[36] S.Rashidi,S.Sridharan,S.Srinivasan,andT.Krishna,“ASTRA-SIM: LargeLanguageModelServing,”inOSDI,2024.
[59] K.Zhu,Y.Gao,Y.Zhao,L.Zhao,G.Zuo,Y.Gu,D.Xie,T.Tang,Q.Xu,
| Enabling | SW/HW | Co-Design |     | Exploration | for | Distributed | DL Training |     |     |     |     |     |     |     |     |
| -------- | ----- | --------- | --- | ----------- | --- | ----------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
Platforms,”inISPASS,2020. Z.Ye,K.Kamahori,C.-Y.Lin,Z.Wang,S.Wang,A.Krishnamurthy,
[37] T.Schick,J.Dwivedi-Yu,R.Dessi,R.Raileanu,M.Lomeli,E.Hambro, and B. Kasikci, “NanoFlow: Towards Optimal Large Language Model
L. Zettlemoyer, N. Cancedda, and T. Scialom, “Toolformer: Language ServingThroughput,”inOSDI,2025.
ModelsCanTeachThemselvestoUseTools,”inNeurIPS,2023. [60] R. Zhu, Z. Jiang, C. Jin, P. Wu, C. A. Stuardo, D. Wang, X. Zhang,
|               |       |             |     |                       |     |     |                 |     | H. Zhou, | H. Wei, | Y. Cheng, J. Xiao, | X. Zhang, | L.  | Liu, H. | Lin, L.-W. |
| ------------- | ----- | ----------- | --- | --------------------- | --- | --- | --------------- | --- | -------- | ------- | ------------------ | --------- | --- | ------- | ---------- |
| [38] ShareGPT | Team, | “ShareGPT,” |     | https://sharegpt.com, |     |     | 2023, accessed: |     |          |         |                    |           |     |         |            |
2026-04-09. Chang, J. Ye, X. Yu, X. Liu, X. Jin, and X. Liu, “MegaScale-Infer:
[39] Y.Shen,K.Song,X.Tan,D.Li,W.Lu,andY.Zhuang,“HuggingGPT: EfficientMixture-of-ExpertsModelServingwithDisaggregatedExpert
Solving AI Tasks with ChatGPT and its Friends in Hugging Face,” in Parallelism,”inSIGCOMM,2025.
NeurIPS,2023.
| [40] N. Shinn, | F.  | Cassano, | A.     | Gopinath,   | K. Narasimhan, |     | and        | S. Yao, |     |     |     |     |     |     |     |
| -------------- | --- | -------- | ------ | ----------- | -------------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| “Reflexion:    |     | language | agents | with verbal | reinforcement  |     | learning,” | in      |     |     |     |     |     |     |     |
NeurIPS,2023.
| [41] B. Sun, | Z. Huang, | H.  | Zhao, | W. Xiao, | X. Zhang, | Y.  | Li, and | W. Lin, |     |     |     |     |     |     |     |
| ------------ | --------- | --- | ----- | -------- | --------- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
“Llumnix:DynamicSchedulingforLargeLanguageModelServing,”in
OSDI,2024.
| [42] Y. Sun, | T. Baruah, | S.  | A. Mojumder, |     | S. Dong, | X. Gong, | S. Treadway, |     |     |     |     |     |     |     |     |
| ------------ | ---------- | --- | ------------ | --- | -------- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Y.Bao,S.Hance,C.McCardwell,V.Zhao,H.Barclay,A.K.Ziabari,
Z.Chen,R.Ubal,J.L.Abella´n,J.Kim,A.Joshi,andD.Kaeli,“MG-
PUSim:enablingmulti-GPUperformancemodelingandoptimization,”
inISCA,2019.
| [43] J. Taneja, | A.  | Laird, | C. Yan, | M. Musuvathi, | and | S. K. | Lahiri, | “LLM- |     |     |     |     |     |     |     |
| --------------- | --- | ------ | ------- | ------------- | --- | ----- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
Vectorizer:LLM-BasedVerifiedLoopVectorizer,”inCGO,2025.
[44] J.Wang,J.Han,X.Wei,S.Shen,D.Zhang,C.Fang,R.Chen,W.Yu,
| and        | H. Chen,  | “{KVCache} |       | Cache | in the Wild: | Characterizing |     | and  |     |     |     |     |     |     |     |
| ---------- | --------- | ---------- | ----- | ----- | ------------ | -------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
| Optimizing | {KVCache} |            | Cache | at a  | Large Cloud  | Provider,”     | in  | ATC, |     |     |     |     |     |     |     |
2025.
| [45] B. Wu, | S. Liu, | Y. Zhong, | P.  | Sun, X. | Liu, and | X. Jin, | “LoongServe: |     |     |     |     |     |     |     |     |
| ----------- | ------- | --------- | --- | ------- | -------- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
EfficientlyServingLong-ContextLargeLanguageModelswithElastic
SequenceParallelism,”inSOSP,2024.
[46] Q.Wu,G.Bansal,J.Zhang,Y.Wu,B.Li,E.Zhu,L.Jiang,X.Zhang,
| S. Zhang, | J.  | Liu, A. | H. Awadallah, |     | R. W. | White, | D. Burger, | and |     |     |     |     |     |     |     |
| --------- | --- | ------- | ------------- | --- | ----- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
C.Wang,“AutoGen:EnablingNext-GenLLMApplicationsviaMulti-
AgentConversations,”inCOLM,2024.
[47] A.Yang,A.Li,B.Yang,B.Zhang,B.Hui,B.Zheng,B.Yu,C.Gao,
C.Huang,C.Lv,C.Zheng,D.Liu,F.Zhou,F.Huang,F.Hu,H.Ge,
| H. Wei,  | H.       | Lin, J. Tang, | J.            | Yang, J. | Tu, J. Zhang, | J.       | Yang, J.  | Yang,   |     |     |     |     |     |     |     |
| -------- | -------- | ------------- | ------------- | -------- | ------------- | -------- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| J. Zhou, | J. Zhou, | J.            | Lin, K.       | Dang, K. | Bao, K.       | Yang,    | L. Yu, L. | Deng,   |     |     |     |     |     |     |     |
| M. Li,   | M. Xue,  | M.            | Li, P. Zhang, | P.       | Wang, Q.      | Zhu, R.  | Men,      | R. Gao, |     |     |     |     |     |     |     |
| S. Liu,  | S. Luo,  | T. Li,        | T. Tang,      | W. Yin,  | X. Ren,       | X. Wang, | X.        | Zhang,  |     |     |     |     |     |     |     |
X.Ren,Y.Fan,Y.Su,Y.Zhang,Y.Zhang,Y.Wan,Y.Liu,Z.Wang,
| Z. Cui, | Z. Zhang, | Z.  | Zhou, | and Z. | Qiu, “Qwen3 | Technical | Report,” |     |     |     |     |     |     |     |     |
| ------- | --------- | --- | ----- | ------ | ----------- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
2025.[Online].Available:https://arxiv.org/abs/2505.09388
[48] C.Yang,Z.Zhao,Z.Xie,H.Li,andL.Zhang,“KNighter:Transforming
StaticAnalysiswithLLM-SynthesizedCheckers,”inSOSP,2025.
| [49] W. Yang, | Y.           | Shin, O. | Woo,             | G. Park, | H. Ham, | J. Kang, | J. Park, | and |     |     |     |     |     |     |     |
| ------------- | ------------ | -------- | ---------------- | -------- | ------- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| G. Kim,       | “PyTorchSim: |          | A Comprehensive, |          | Fast,   | and      | Accurate | NPU |     |     |     |     |     |     |     |
SimulationFramework,”inMICRO,2025.
| [50] S. Yao, | N.  | Shinn, P.       | Razavi, | and         | K. R. Narasimhan, |            | “τ-bench: | A   |     |     |     |     |     |     |     |
| ------------ | --- | --------------- | ------- | ----------- | ----------------- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Benchmark    | for | Tool-Agent-User |         | Interaction | in                | Real-World | Domains,” |     |     |     |     |     |     |     |     |
inICLR,2025.
[51] S.Yao,J.Zhao,D.Yu,N.Du,I.Shafran,K.R.Narasimhan,andY.Cao,
| “ReAct: | Synergizing |     | Reasoning | and | Acting in | Language | Models,” | in  |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --------- | --- | --------- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
ICLR,2023.