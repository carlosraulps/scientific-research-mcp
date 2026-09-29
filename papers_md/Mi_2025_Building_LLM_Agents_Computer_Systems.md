Building LLM Agents by Incorporating Insights from Computer Systems
YapengMi12 ZhiGao13 XiaojianMa1 QingLi1
Abstract generalityandscalability. Atthesametime,thelackofa
systematicapproachtodevelopingLLMagentslimitsthe
LLM-driven autonomous agents have emerged
abilitytoguidefutureresearchdirections. Therefore, we
as a promising direction in recent years. How- arefacedwithacriticalquestion: HowcangeneralLLM
ever, many of these LLM agents are designed agentsbesystematicallyconstructedandevolved?
empirically or based on intuition, often lacking
systematicdesignprinciples,whichresultsindi- In this paper, we advocate for building LLM agents by
verseagentstructureswithlimitedgeneralityand incorporatinginsightsfromcomputersystems. Looking
scalability. Inthispaper,weadvocateforbuild- backattheevolutionofcomputersystemdesign(Campbell-
ingLLMagentsbyincorporatinginsightsfrom Kelly&Aspray,1996),wefindthatitoncewitnessedapro-
computersystems. InspiredbythevonNeumann liferationofvariousstructuralapproaches. Intheearlydays
architecture,weproposeastructuredframework of computing, systems were often designed with specific
forLLMagenticsystems,emphasizingmodular architecturestailoredtoparticulartasks,suchastheABC
designanduniversalprinciples. Specifically,this computerin1942forsolvinglinearequations(Burksetal.,
paper first provides a comprehensive review of 1946). This specificity meant that these systems lacked
LLMagentsfromthecomputersystemperspec- general-purposecapabilities. Astimegoeson,moderncom-
tive, then identifies key challenges and future putersystemshavelargelyconvergedonaunifiedtheoretical
directions inspired by computer system design, framework: thevonNeumannarchitecture,whichhassig-
andfinallyexploresthelearningmechanismsfor nificantlyadvancedthefield. Similarly,thedesignofagents
LLMagentsbeyondthecomputersystem. The todayrevolvesaroundsystem-levelconsiderations,much
insightsgainedfromthiscomparativeanalysisof- likecomputersystemsdesign. Astraightforwardcompar-
ferafoundationforsystematicLLMagentdesign isonbetweenthevonNeumannarchitectureandtheagent
andadvancement. architectureshowstheirhighsimilarityinbothstructural
designandtaskworkflows,asshowninFigure1. Thispar-
alleloffersnumerousopportunitiesforcomparativeanalysis
betweenthesetwofields. Forexample,bothsystemshave
1.Introduction
memorymodules,andthecomputerstoragehierarchycan
In recent years, autonomous agents have emerged as a guideagents’finer-grainedmemorydesign. Furthermore,
promisingdirection,withwidespreadapplicationsinvari- computersystemshavedevelopedseveralgoldeninsights
ousdomains,suchascomputeruse(Hongetal.,2024;Lin overtime,suchasparallelization.Theseprinciplescanbeef-
etal.,2024),codeassistance(Wangetal.,2024a;Yangetal., fectivelytransferredtothedesignofLLMagents,providing
2024),andothers(Kimetal.,2024;Fanetal.,2025). These foundationalguidancefortheirconstruction.
agents,poweredbylargelanguagemodels(LLMs)(Achiam
Therefore,thispaperproposesbuildingandevolvinggeneral
etal.,2023)ascontrollers,integratekeycomponentssuch
LLMagentsbydrawinginsightsfromcomputersystems,
asmemory,tools,andactionwhileallowingeffectiveenvi-
includingvonNeumannarchitectureandotherrelatedprin-
ronmentalinteraction. Currently,manystudies(Xieetal.,
ciples. We will conduct a comprehensive analysis of the
2024;Duranteetal.,2024)relyonintuitionorexperience
LLMagentcomparedwiththecomputersystems,thenin-
todesignagents,oftenlackingsystematicdesignprinciples.
vestigatethepotentialfutureresearchdirectioninspiredby
Asaresult,thesignificantdivergenceamongthesedesigns
thecomputersystems,andexplorethelearningcapability
makesitdifficulttoestablishastandardizedstructurewith
ofagentsbeyondthecomputersystems. Specifically,this
1StateKeyLaboratoryofGeneralArtificialIntelligence,BIGAI workprovidesacomparativeanalysisofLLMagentsforthe
2HarbinInstituteofTechnology3SchoolofIntelligenceScience framework,inspiredbythevonNeumannarchitecture(Sec-
andTechnology,PekingUniversity.Correspondenceto:QingLi tion2). WeproposeLLMagentsasacollectionofdistinct
<dylan.liqing@gmail.com>.
modules that dynamically interact with the environment.
Thisframeworkeffectivelyencapsulatesexistingresearch
1
5202
rpA
6
]VC.sc[
1v58440.4052:viXra

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
|                          |     |     | Input/Perception                                       |     | Control Unit/Cognition |     |     | Memory | Logic Unit/Tool |     |     | Output/Action |
| ------------------------ | --- | --- | ------------------------------------------------------ | --- | ---------------------- | --- | --- | ------ | --------------- | --- | --- | ------------- |
| Von Neumann architecture |     |     | Task: Count the total size of images in one directory. |     |                        |     |     |        |                 |     |     |               |
Output
O u t p u t :
|     |     |     | I n p u t : | D e c i s i o     | n - m a k i n g  | : R e a d   M e m o r      | y : D e        | c i s i o n - m a k       | i n g : C | o m p u t e :           |         |                                      |
| --- | --- | --- | ----------- | ----------------- | ---------------- | -------------------------- | -------------- | ------------------------- | --------- | ----------------------- | ------- | ------------------------------------ |
|     |     |     | P y t h o n | C a l l   a   f u | n c t io n   t o | R e a d  d a t a   f r o m | d is k s C h e | c k   t h e   c o n d i t | i o n g   | e t t h e r e s u l t 5 | 5 6 4 3 | T o t a l si z e   o f   i m a g e s |
M em o ry Co n t r ol L o g i c s o l v e t h e t a s k : t o  m a i n   m e m o r y a n d c h o o s e p a t h c o d e : f i l e _ s i ze = g e t s i z e () i n   ' . / im a g e s ' :   55 6 4 3
U ni t run. p y . / i m ages c o d e : C a l c u l a t e _ S iz e s( ) c o d e : o s . w a l k ( d i r e c t or y) … co d e : I f o s .p a th . s p l i t e x t. i n.. s u m = s u m + f il e_ s i z e b y t e s
|     | U n i t | U n i t |     |     |     |     |     |     |     |     |     | code: print(f " Total ...") |
| --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------- |
Images
|     | Input |     |     |     |     | Variable |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
LLMagent architecture Task:WhichelectronicproductdoIuseandcheckitslatestprice.
Action
Question: Planning: Get Read Memory: Decision-making: Tool Use: Web Answer: "Youusea
|     |     |     | Which electronic |                     |     |                 | Usethewebsearch |                         |     |              |     | MacBook Pro. The |
| --- | --- | --- | ---------------- | ------------------- | --- | --------------- | --------------- | ----------------------- | --- | ------------ | --- | ---------------- |
|     |     |     |                  | Profile Information |     | Frommylong-term | t o o           | l  t o  ge t  p r ic e  | for | Search tool→ |     |                  |
Memory Cognition Tool pr o d u c t  d o  I   u se → S ea r ch  pr ic e → m e m o ry ,  I  k n o w :  Y o u F o u nd   $ 1, 5 9 9  fo r 1 4 - in c h   M a c B o o k
a n d  c h e c k  i t s Val id a te → O u tp ut. us e  a  M a c B o o k  P r o . r e al - t im e  p r ic in g th e  M a c B o o k  P ro . P r o st a r t s a t $ 1 ,5 99."
|     |     |     | latestprice. |     |     |     | updates. |     |     |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
MacBookPro
Perception
Figure1.AnanalogybetweenvonNeumannarchitectureandLLMagentarchitecturewithtaskexecutionworkflows(AppendixA).
whileinspiringfuturedirections. Then,thispaperwilldis- externalenvironment,denotedo. Attimestept,theaction
cusspotentialdirectionsinspiredbycomputers,including a canbederivedusingthefollowingequation:
t
finer-grainedmemory,parallelization,andotherpotential (cid:18) (cid:19)
advances(Section3). Finally,weanalyzecurrentlearning a =A C (cid:0) P(o ,a ,...,o ,a ,o ),M ,T (cid:1) . (1)
|     |     |     |     |     |     | t   |     | 1 1 | t−1 | t−1 | t   | r c |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
mechanismsandexplorehowsuchagentscanlearnfrom
| theirenvironment,throughwhichtheagentscouldgobe- |     |     |     |     |     | M           |                                          |     |         |           |     |            |
| ------------------------------------------------ | --- | --- | --- | --- | --- | ----------- | ---------------------------------------- | --- | ------- | --------- | --- | ---------- |
|                                                  |     |     |     |     |     | Here,       | r represents                             | the | content | retrieved | by  | the memory |
| yondsomelimitationsofcomputersystems(Section4).  |     |     |     |     | We  |             |                                          |     |         |           |     |            |
|                                                  |     |     |     |     |     | module,andT | representstheoutputofthecallingtool.This |     |         |           |     |            |
c
believethatbetterlearningmethodsarekeytotheevolution equation briefly illustrates how our framework generates
| ofLLMagents. | Tothebestofourknowledge, |     |     | thisisthe |     |            |                                              |     |     |     |     |     |
| ------------ | ------------------------ | --- | --- | --------- | --- | ---------- | -------------------------------------------- | --- | --- | --- | --- | --- |
|              |                          |     |     |           |     | theactiona | t byintegratingthehistoricalsequencestarting |     |     |     |     |     |
firstanalogydrawnbetweencomputersystemsandLLM
|     |     |     |     |     |     | fromtheinitialprompt-guidedobservationo |     |     |     |     |     | ,followedby |
| --- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ----------- |
1
agents,andwehopeitcanbenefitthecommunity. actionsandobservations,combinedwithmemorycontent
|     |     |     |     |     |     | andtooloutputs. |     | MoredetailscanbefoundinAppendixB. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | --------------------------------- | --- | --- | --- | --- |
2.LLMAgentFrameworkInspiredbyVon
| NeumannArchitecture |     |     |     |     |     | 2.1.Perception |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- |
One important insight from computer systems is the von Foragentsinteractinginreal-worldenvironments,thecapa-
bilityofperceptionisindispensable,similartotheroleof
Neumannarchitecture,whichestablishedthefoundational
|     |     |     |     |     |     | inputmodulesincomputersystems. |     |     |     | Justascomputersuse |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | ------------------ | --- | --- |
frameworkofmoderncomputingbyintegratingacentral
processingunit,memory,andinput/outputsystems(Burks inputsuchaskeyboardsandcameras,agentsgathervarious
typesofinformation,suchastext,images,video,andaudio.
| etal.,1946). | Inthissection,wefollowasystematicperspec- |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tiveanddrawinspirationfromvonNeumannarchitecture Basedonexistingresearch,theperceptionofagentscanbe
|     |     |     |     |     |     | dividedintotwoparts: |     | unimodalandmultimodal. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | ---------------------- | --- | --- | --- | --- |
(Figure1)toexplorehowtoconstructgeneralLLMagents.
WepositthatanLLMagentcomprisesinterconnectedcom-
|     |     |     |     |     |     | Unimodal: | Unimodalperceptionmeansthattheagentper- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --------------------------------------- | --- | --- | --- | --- | --- |
ponents: perception,cognition,memory,tools,andaction,
|     |     |     |     |     |     | ceives only | one | type of | information. |     | Due | to the signifi- |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | ------------ | --- | --- | --------------- |
which dynamically interact with each other and the envi- cantachievementsofLLMsinnaturallanguageprocessing,
| ronment,asshowninFigure2. |     |     | Weconductedaliterature |     |     |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
earlyagentsusedLLMsascoreprocessors,relyingonthe
reviewbasedonthisdefinition. Duringthisprocess,wealso model’sinherentperceptioncapabilities. Inpreviousstud-
conductedacomparativeanalysiswiththevonNeumann
ies(Wangetal.,2023;Shenetal.,2024),theseagentsonly
architecture,revealingsharedprinciplesinsystemdesign
utilizetextualinformationinenvironmentsforprocessing
betweenthetwo. andplanning,andrestrictaccurateunderstandingofmulti-
Tofurthersupportthefoundationalframework,thispaper modalinformation,drivingthedevelopmentofsubsequent
multimodalperceptionagents.
| providesaconciseformulation.          |     |     | Toformalize,eachmodule |                 |         |             |                                          |        |              |     |     |            |
| ------------------------------------- | --- | --- | ---------------------- | --------------- | ------- | ----------- | ---------------------------------------- | ------ | ------------ | --- | --- | ---------- |
| isdenotedbyitsuppercaseinitial(e.g.,P |     |     |                        | forperception). |         |             |                                          |        |              |     |     |            |
|                                       |     |     |                        |                 |         | Multimodal: | With                                     | recent | advancements |     | in  | multimodal |
| TheframeworkisdefinedasF              |     |     | =(P,C,M,T,A).          |                 | Specif- |             |                                          |        |              |     |     |            |
|                                       |     |     |                        |                 |         | LLMs,       | moreagents(Hongetal.,2024;Kimetal.,2024) |        |              |     |     |            |
ically,theLLMagentalsoreceivesobservationsfromthe nowadoptmultimodalmodelsascontrollers,enablingthe
2

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
| Internal | External |     |     |     |     |     |     |
| -------- | -------- | --- | --- | --- | --- | --- | --- |
Ac�on
| Actions | Actions |     |     |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- | --- | --- |
Output
Short-Term
Context Window
Long-Term
Environment
| RAG          |     | Model    |     | Tool Set       |     |     |     |
| ------------ | --- | -------- | --- | -------------- | --- | --- | --- |
| Memory       |     | Cogni�on |     | Tool           |     |     |     |
| Memory Write |     | Planning |     | Tool Retrieval |     |     |     |
Reasoning
Open-World
| Memory Read |     | COT |     | Tool Calling |     |     |     |
| ----------- | --- | --- | --- | ------------ | --- | --- | --- |
TOT
| Memory Manage |            | Reflection |     | Tool Update |     |     |     |
| ------------- | ---------- | ---------- | --- | ----------- | --- | --- | --- |
| Unimodal      | Multimodal | Percep�on  |     |             |     |     |     |
Input
Figure2.AframeworkdiagramofLLMagentsinspiredbythevonNeumannarchitecture. Thisframeworkillustratesthedifferent
componentsofLLMagentsandspecificclassificationswithineachmodule,alongwiththeinteractionsbetweenthemodules.
integrationofdiversemodalitiessuchastext,images,and ofthoughtandreflectiontofacilitatebetterplanning. Anal-
videos. Forcomplexscenarios,externalencoders(Fanetal., ogously,planningcanbeseenasthecentralfunctionofthe
2022)canalsobeusedtoconvertinformationintoforms controlunit,whilereasoningrepresentstheunderlyinglogic
perceivablebyagents. Insummary,multimodalhasbecome thatdrivesitsdecision-makingprocesses.
amainstreamdirectionforagentperception.
|     |     |     | Planning: | Planningisafoundationalcapabilityofcogni- |     |     |     |
| --- | --- | --- | --------- | ----------------------------------------- | --- | --- | --- |
Notably, a crucial principle of von Neumann architec- tion. Givenagoal,OK,planningdecidesonasequenceof
tureisthatvarioustypesofinformationaretransformed actions(a ,a ,...,a )thatwillleadtoastateachieving
|     |     |     |     | 0 1 | n   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
intoacommonrepresentationwithinthesystem. Com- thegoal. Earlystudies(Liuetal.,2023;Yaoetal.,2020)ex-
putersystemsrepresentinformationinadataspaceof0s ploredtheuseofexternalplannerstoassistplanning. With
and1s,modernagentsrepresentperceivedinformationin thefurtherenhancementofLLMsinreasoning(Weietal.,
the language space, which offers several distinct advan- 2022),planningisexpectedtobeincorporatedintothecon-
tages. Firstly, language space demonstrates higher fault trollersthemselves. Forexample,WebDreamer(Guetal.,
tolerance during agent task execution due to the superior 2024)usesLLMstosimulatecandidateactionsandevaluate
generalizationcapabilitiesofnaturallanguage. Secondly, theiroutcomestoselecttheoptimalstep. Therefore,wecan
languagespaceenablestheexpressionofmoreabstractand seethatfutureplanningmethodsarelikelytobecentered
ambiguousconcepts,whichisoftenbeyondthecapacityof around LLMs, requiring less scaffolding. This is largely
conventionalcomputersystems. Lastly,sincetheoutputin attributedtotheimprovementofreasoningcapabilitiesof
theprocessoftaskcompletioncanbeobservedinnatural LLMs,whichiscrucialincognition.
language,representinginformationinthelanguagespace
|     |     |     | Reasoning: | Reasoningisafundamentalunitofcognition, |     |     |     |
| --- | --- | --- | ---------- | --------------------------------------- | --- | --- | --- |
inherentlyprovidesbetterInterpretability.
|     |     |     | anditsupportsthethinkingcapabilityofLLMagents. |                 |              |            | Ob-     |
| --- | --- | --- | ---------------------------------------------- | --------------- | ------------ | ---------- | ------- |
|     |     |     | jectively,                                     | the development | of reasoning | is closely | tied to |
2.2.Cognition
|     |     |     | LLMs,                                   | significantly | expanding their | ability to think | and |
| --- | --- | --- | --------------------------------------- | ------------- | --------------- | ---------------- | --- |
|     |     |     | enablingthemtosolvemorecomplexproblems. |               |                 | Inrecent         |     |
ThecognitionmoduleplaysacrucialroleinLLMagents,
muchlikethepositionofthecontrolunitinthecomputer years,theadvancementofreasoningbasedonLLMsbegan
architecture. Cognitiongovernstheagent’sdecisions,en- withCoT(Weietal.,2022),whichallowsthemodeltode-
composecomplexproblemsintoasequenceofintermediate
compassingplanningandreasoningcapabilities. Planning
isanessentialcapabilityforalmosteveryLLMagent,while reasoningsteps. CoT-SC(Wangetal.,2022)buildsupon
|     |     |     | CoT by | generating | multiple answers | simultaneously | and |
| --- | --- | --- | ------ | ---------- | ---------------- | -------------- | --- |
reasoninginvolvesvariousthoughtprocessessuchaschain
3

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
| selectingtheoptimalone.                              |     | ToT(Yaoetal.,2024)adoptsa |     |     |      |                  |     |     |                  |     |
| ---------------------------------------------------- | --- | ------------------------- | --- | --- | ---- | ---------------- | --- | --- | ---------------- | --- |
| treestructuretoexploremultiplereasoningpathsandself- |     |                           |     |     | P r  | im a ry Register |     |     |                  |     |
|                                                      |     |                           |     |     | St o | ra g e           |     |     |                  |     |
|                                                      |     |                           |     |     |      |                  |     |     | S h o rt -t e rm |     |
evaluate for a globally optimal decision. These methods Cache M e m o r y
Faster Access
enable the cognition module to engage in deep thinking, Context window
Main Memory
| therebysignificantlyenhancingitsdecision-makingcapabil- |     |     |     |     | Higher Capacity |     |     |     |                  |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --------------- | --- | --- | --- | ---------------- | --- |
| ities.                                                  |     |     |     |     |                 |     |     |     | Long-term Memory |     |
Disk
Database , Knowledge Graph
| Another | key capability | in reasoning | is  | known as self- |     |     |     |     |     |     |
| ------- | -------------- | ------------ | --- | -------------- | --- | --- | --- | --- | --- | --- |
refinement or reflection. This ability allows LLM agents Computer Memory Hierarchy Agent Memory Hierarchy
toreflectontheirpastactionsandfurtheroptimizefuture
Figure3.Anintuitivecomparisonbetweencomputermemoryhi-
| decisions. | Essentially,ittransformsalinearthoughtprocess |     |     |     |     |     |     |     |     |     |
| ---------- | --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
erarchyandagentmemoryhierarchy.
intoacyclicalonebytreatingthedecision-makingprocess
| ascontinuous.             | TheReAct(Yaoetal.,2022)frameworkisa |                           |     |     |     |     |     |     |     |     |
| ------------------------- | ----------------------------------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| notablepioneerinthisarea. |                                     | ItenhancesLLMsbyintegrat- |     |     |     |     |     |     |     |     |
ingtask-specificactionsforenvironmentalinteractionand tainagenttaskinteractionworkflows,short-termmemory
isoftenusedtostorecontextualinput-outputinformation
| naturallanguagereasoningforsituationalreflection. |     |     |     | Reflex- |     |     |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
ion(Shinnetal.,2024)convertsbinaryorscalarfeedback relatedtothetask,includingreasoningdetails,toolusage
from the environment into textual summaries, which are data, andpaststateinformation. Therefore, itisoftenre-
ferredtoasworkingmemory,whichsupportscontextually
thenincorporatedasadditionalcontextforLLMagentsin
subsequent iterations. Most self-refinement mechanisms appropriateresponsesduringongoinginteractions.
enableagentstoimprovethroughtrial-and-errorprocesses,
|     |     |     |     |     | Long-Term | Memory: | In contrast, | long-term | memory | is  |
| --- | --- | --- | --- | --- | --------- | ------- | ------------ | --------- | ------ | --- |
enhancingtheirrobustness.
designedtostoreinformationforextendedperiods,enabling
Notably,inthehistoryofelectroniccomputing,theevolu- LLMagentstoretrieveandutilizepastknowledgeorskills
tionofCPUs,followingtheunifiedvonNeumannarchitec- acrossdifferentinteractions,likedisksinthememoryhier-
ture,hasconsistentlybeenthemostcriticaldevelopmentin archy (see Figure 3). Long-term memory encompasses a
diverserangeofcontenttypes,includingtext,images,codes,
| computers. | Fromthisperspective,thecognitionmoduleof |     |     |     |     |     |     |     |     |     |
| ---------- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
LLMagentsislikelytofollowasimilartrajectory. Inthe trajectories,profileinformation,andsuccessfuldemonstra-
future,advancedplanningandreasoningunitsmayemerge tions,significantlybroadeningthescopeofinformationthat
|     |     |     |     |     | agents can | leverage. | Long-term | memory | is typically | im- |
| --- | --- | --- | --- | --- | ---------- | --------- | --------- | ------ | ------------ | --- |
asthecoredirectionforLLMagents,furtherunderscoring
thecentralroleofcognitionintheirdevelopment. plementedthroughexternalmemorysystems,enhancingan
agent’sreliability.
2.3.Memory
MemoryReadandWrite:Memoryreadingandwritingare
fundamentaloperationsinthevonNeumannarchitecture,
InthevonNeumannarchitecture,thememoryunitserves
asthecentralrepositoryforbothdataandinstructions. This servingasthecriticallinkbetweentheCPUandmemory.
Similarly,LLMagentsareincreasinglyequippedwithmech-
essentialunitcanbeanalogouslyextendedtoLLMagents,
|                     |     |           |                |           | anismstoreadandwritetheirmemory. |     |     |     | Thesecapabilities |     |
| ------------------- | --- | --------- | -------------- | --------- | -------------------------------- | --- | --- | --- | ----------------- | --- |
| where a memory-like |     | component | is constructed | for stor- |                                  |     |     |     |                   |     |
allowagentstoadaptdynamicallytochangingenvironments
| ing states, | knowledge, | or learned | behaviors, | facilitating |     |     |     |     |     |     |
| ----------- | ---------- | ---------- | ---------- | ------------ | --- | --- | --- | --- | --- | --- |
byeditingstoredinformation,ensuringthatthememoryre-
| decision-makinganddynamicadaptation. |     |     | Incomputersys- |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
tems,thememoryunitsfollowamemoryhierarchy,which mainsrelevanttospecifictasks. Formemoryreading,most
methodsselectmemoryvaluesthatexhibitthehighestsimi-
| isagoodinsightfromcomputersystems. |     |     | Wefindastrong |     |                         |     |                             |     |     |     |
| ---------------------------------- | --- | --- | ------------- | --- | ----------------------- | --- | --------------------------- | --- | --- | --- |
|                                    |     |     |               |     | laritytothequeryobject. |     | Furthermore,manyagentsadopt |     |     |     |
analogybetweenthememorybetweencomputersandLLM
agents, as illustrated in Figure 3. Short-term memory is Retrieval-Augmented Generation (Lewis et al., 2020) to
|     |     |     |     |     | formacompletereadingandgenerationworkflow. |     |     |     |     | Genera- |
| --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | ------- |
smallerthanlong-termmemorybutisfast,andlong-term
memoryrestoresinformationlongerbutshort-termmemory tiveAgents(Parketal.,2023)retrievenecessaryinformation
intextformbasedonrelevance,recency,andimportance.
cannot. Therefore,memoryofLLMagentscanbecatego-
Memorywritingoftenfollowsthestorageformatofmem-
rizedintoshort-termandlong-termmemory,accompanied
byassociatedreadandwriteoperations,aligningwiththe oryreading. Forexample,inMemoChat(Luetal.,2023),
agentssummarizeeachconversationsegmentbyidentifying
aforementionedperspective.
themaintopicsdiscussedandstoringthemaskeystoindex
Short-TermMemory:Short-termmemoryisoftenincorpo-
|     |     |     |     |     | memory | pieces. | This structured | approach | facilitates | effi- |
| --- | --- | --- | --- | --- | ------ | ------- | --------------- | -------- | ----------- | ----- |
ratedintoLLMs,likeprimarymemoryincomputerarchitec- cientmemoryretrievalduringreadingoperations. Memory
| ture,asillustratedinFigure3. |     | Short-termmemoryrefersto |     |     |     |     |     |     |     |     |
| ---------------------------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
readingandwritingoperationsarecollaborative,collectively
anLLMagent’scontextualunderstandingwithinitscontext enhancingthecapabilitiesofLLMagents. Moreover,from
window,whichiscriticalforimmediateoperations. Incer- acomputationalperspective,thespeedofmemoryreadand
4

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
writeoperationsremainsanareatobeexploredforLLM ingactions. Theseinternalactionsmodifyagents’internal
agents, as it directly impacts information processing and state,enablingittobetterlearnandadapttoenvironments.
taskexecutionefficiency. Specifically,reasoningrepresentsanovelinternalactionthat
doesnotexistintraditionalcomputersystems,highlighting
thatLLMagentshaveabroaderactionspaceduetotheir
2.4.Tool
abilitytooperatewithinabstractsemanticspaces.
AuniquefeatureisthatLLMagentscouldutilizeexternal
|     |     |     |     |     | ExternalActions: | Externalactionsrefertotheactionsout- |     |     |
| --- | --- | --- | --- | --- | ---------------- | ------------------------------------ | --- | --- |
tools,whichissimilartoalogicunitincomputersystems.
Asthelogicunitisthetrueexecutorofarithmeticoperations, putbyLLMagentsthattargetexternalenvironments. These
actionsarecloselytiedtotheexternalcontextandprimarily
| the tools | within LLM agents | concrete | execution | of tasks. |     |     |     |     |
| --------- | ----------------- | -------- | --------- | --------- | --- | --- | --- | --- |
ToolusageisoftenpresentedasAPIs,enablingagentsto includeexecutionactionsinGUIorembodiedenvironments,
selecttheappropriatetoolsbasedontheirobjectivesquickly. aswellasinteractionactionsinnaturallanguagedialogue.
Forexample,SayCan(Ahnetal.,2022)generatesaction-
Commonlyusedtoolsinexistingmethodsarediverseand
dependonthedesignofthetoolset,suchascalculatorsfor able steps for robots, ShowUI (Lin et al., 2024) outputs
actionsandcoordinatesforvirtualenvironments,andMDa-
arithmeticoperations,andGooglesearchforretrievingthe
latestinformation. Therearetwomaininteractionsintool gents(Kimetal.,2024)performconversationalactionsto
use,whicharenamedtoolretrievalandtoolcalling. providemedicaladvice. Itisworthnotingthatsomeaction
formatsrequirespecificagentstouseanadditionalaction
| ToolRetrieval: | Whengivenaquestionthatneedstoolsto |     |     |     |     |     |     |     |
| -------------- | ---------------------------------- | --- | --- | --- | --- | --- | --- | --- |
processingfunctiontogenerateexecutableactions.
solve,LLMagentsperformreasoningandplanningtogen-
| erateresponsescontainingtoolinformation. |     |     | Toolretrieval |     |     |     |     |     |
| ---------------------------------------- | --- | --- | ------------- | --- | --- | --- | --- | --- |
2.6.Environment
| means selecting | the right | tools using | a retriever | or LLM. |     |     |     |     |
| --------------- | --------- | ----------- | ----------- | ------- | --- | --- | --- | --- |
Forinstance,Gorilla(Patiletal.,2023)employsBM25and Incomputersystems,computersinteractwithenvironments
GPT-Index to construct a retriever to implement tool re- inwaysdesignedbyhumans. Similarly, anagentsystem
trieval. ToolLLM(Qinetal.,2023)trainsaSentence-BERT only exerts its unique capabilities through environmental
modeltoserveasatoolretriever,allowinghighlyefficient interaction. TheinteractionenvironmentofagentLLMsis
retrievalofrelevanttools. highly diverse; it could be a human (Chen et al., 2023b),
|              |                   |                     |     |     | a game (Wang   | et al., 2023), | or a real-world | setting (Ahn     |
| ------------ | ----------------- | ------------------- | --- | --- | -------------- | -------------- | --------------- | ---------------- |
| ToolCalling: | Asfortoolcalling, | itmeansarighttoolis |     |     |                |                |                 |                  |
|              |                   |                     |     |     | et al., 2022). | Typically,     | an agent acts   | and receives new |
correctlyprovidedwithrequiredparametersandexecuted
observationsandfeedbackfromtheenvironmentafterexe-
| successfully | to return results | for LLM | agents, making | it  |     |     |     |     |
| ------------ | ----------------- | ------- | -------------- | --- | --- | --- | --- | --- |
cution,andthisprocessiscalledacompleteinteractionloop.
| a successful | call. In EasyTool | (Yuan | et al., 2024), | it im- |     |     |     |     |
| ------------ | ----------------- | ----- | -------------- | ------ | --- | --- | --- | --- |
What’smore,peopledesigneffectivehuman-computerinter-
provesLLMs’understandingoftoolfunctionsandparam-
actionecosystems,suchasVSCode.Similarly,thereisasig-
| eter requirements | by prompting | ChatGPT | to rewrite | tool |     |     |     |     |
| ----------------- | ------------ | ------- | ---------- | ---- | --- | --- | --- | --- |
nificantunexploredecosystemspacebetweenLLMagents
| descriptions. | ConAgents(Shietal.,2024)presentsamulti- |     |     |     |                          |     |                           |     |
| ------------- | --------------------------------------- | --- | --- | --- | ------------------------ | --- | ------------------------- | --- |
|               |                                         |     |     |     | andexternalenvironments. |     | Forexample,SWE-agent(Yang |     |
agentcollaborativeframework,incorporatingadedicated
etal.,2024)constructsafriendlyinterfacebetweenLLM
| execution       | agent responsible                    | for parameter | extraction | and |                               |     |                       |     |
| --------------- | ------------------------------------ | ------------- | ---------- | --- | ----------------------------- | --- | --------------------- | --- |
|                 |                                      |               |            |     | agentsandsoftwareengineering. |     | Thisanalogyhighlights |     |
| toolinvocation. | Notably,LLMssometimesactastools,rep- |               |            |     |                               |     |                       |     |
thepotentialforenhancedenvironmentalinteraction.
resentingtheexecutionendbeyonddecision-making,not
limitedtospecificinstruments. In summary, inspired by the von Neumann architecture,
wedesignedthecorrespondingLLMagentstructurewhile
2.5.Action conductingacomparativeanalysis. Wealsofindthatthis
structureeffectivelyencompassesexistingwork,asshown
Similar to the output modules in computer systems, the inTable1. Wecanobservetheriseofmultimodalagents,
| action module | in LLM agents | serves | as the interface | for |     |     |     |     |
| ------------- | ------------- | ------ | ---------------- | --- | --- | --- | --- | --- |
mostofwhichpossessreasoningcapabilities,yetlong-term
| interactionwithenvironments. |     | Thefunctionalityandmech- |     |     |                            |     |                            |     |
| ---------------------------- | --- | ------------------------ | --- | --- | -------------------------- | --- | -------------------------- | --- |
|                              |     |                          |     |     | memoryisnotwidelyutilized. |     | Thisindicatesthattheframe- |     |
anismsoftheactionmodulearetypicallygoal-orientedand
|                                               |     |     |     |      | work we designed | effectively                        | summarizes | the current de- |
| --------------------------------------------- | --- | --- | --- | ---- | ---------------- | ---------------------------------- | ---------- | --------------- |
| closelytiedtoLLMagents’operatingenvironments. |     |     |     | Fun- |                  |                                    |            |                 |
|                                               |     |     |     |      | velopmenttrends. | Thisanalogy-baseddesignconfirmsthe |            |                 |
damentally,theactionmoduletransformshigh-levelactions significantsimilaritiesbetweenthetwodesigns,inspiring
| intolow-levelactionsthroughappropriateconversions. |     |     |     | The |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
ustodrawinsightsfromcomputersystems.
| action module | can be simply | categorized | into two | types: |     |     |     |     |
| ------------- | ------------- | ----------- | -------- | ------ | --- | --- | --- | --- |
internalactionsandexternalactions.
3.FutureDirectionsInspiredbyComputers
| InternalActions: | InternalActionsrefertotheinternalop- |     |     |     |          |                  |                 |                |
| ---------------- | ------------------------------------ | --- | --- | --- | -------- | ---------------- | --------------- | -------------- |
|                  |                                      |     |     |     | To guide | future research, | it is important | to address key |
erationsperformedbyLLMagentsduringtaskexecution,
includingmemoryread/write,toolinvocation,andreason- challenges and realize the future direction. Building on
5

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
Table1.SummaryofmoduleinclusioninlandmarkLLMagentstudiesbasedontheproposedframework.Specifically,wealsoincludea
summaryofthelearningmechanismsofLLMagents.Weabbreviatethelearningmechanismsubclassesusinginitials.
|                          |       |     |            |     | Cognition |           | Memory    |            |      |             | LearningMechanisms |        |      |
| ------------------------ | ----- | --- | ---------- | --- | --------- | --------- | --------- | ---------- | ---- | ----------- | ------------------ | ------ | ---- |
|                          | Agent |     | Perception |     |           |           |           |            | Tool | Environment |                    |        |      |
|                          |       |     |            |     | Model     | Reasoning | Long-Term | Short-Term |      |             | LLM                | Memory | Tool |
|                          |       |     |            |     |           | ✗         | ✗         | ✓          | ✓    |             |                    | ✗      | ✗    |
| WebGPT(Nakanoetal.,2021) |       |     | Unimodal   |     | GPT-3     |           |           |            |      | GUI         | FT&RL              |        |      |
SayCan(Ahnetal.,2022) Multimodal PaLM ✓ ✗ ✓ ✓ PhysicalWorld ICL ✗ ✗
| ReAct(Yaoetal.,2022) |     |     | Unimodal |     | PaLM | ✓   | ✗   | ✓   | ✓   | QA  | ICL | ✗   | ✗   |
| -------------------- | --- | --- | -------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
Voyager(Wangetal.,2023) Multimodal GPT-4 ✓ ✓ ✓ ✓ Game ICL ✓ ✓
|     |     |     |     |     |     | ✓   | ✓   | ✓   | ✗   |     |     | ✓   | ✗   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
GenerativeAgents(Parketal.,2023) Unimodal GPT-3.5 VirtualWorld ICL
AppAgent(Zhangetal.,2023) Multimodal GPT-4 ✗ ✓ ✓ ✗ GUI ICL ✗ ✗
ChemCrow(Branetal.,2023) Unimodal GPT-4 ✓ ✗ ✓ ✓ Chemistry ICL ✗ ✗
|                          |     |     |          |     |       | ✗   | ✓   | ✓   | ✗   |     |     | ✓   | ✗   |
| ------------------------ | --- | --- | -------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| MemGPT(Packeretal.,2023) |     |     | Unimodal |     | GPT-4 |     |     |     |     | QA  | ICL |     |     |
ChatDev(Qianetal.,2023) Unimodal GPT-3.5 ✗ ✓ ✓ ✓ Software ICL ✓ ✗
LEO(Huangetal.,2024) Multimodal Vicuna-7B ✓ ✗ ✓ ✗ VirtualWorld ICL&FT ✗ ✗
|                           |     |     |            |     |       | ✓   | ✓   | ✓   | ✓   |     |     | ✓   | ✗   |
| ------------------------- | --- | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| VideoAgent(Fanetal.,2025) |     |     | Multimodal |     | GPT-4 |     |     |     |     | QA  | ICL |     |     |
AgentQ(Puttaetal.,2024) Multimodal LLaMA-3 ✓ ✗ ✓ ✗ GUI FT&RL ✗ ✗
Reflexion(Shinnetal.,2024) Unimodal GPT-3 ✓ ✓ ✓ ✓ CodeExecution ICL&RL ✓ ✗
HuggingGPT(Shenetal.,2024) Multimodal GPT-4 ✓ ✗ ✓ ✓ QA ICL ✗ ✓
|                           |     |     |            |     |       | ✓   | ✓   | ✓   | ✓   |      |     | ✓   | ✓   |
| ------------------------- | --- | --- | ---------- | --- | ----- | --- | --- | --- | --- | ---- | --- | --- | --- |
| Jarvis-1(Wangetal.,2024b) |     |     | Multimodal |     | GPT-4 |     |     |     |     | Game | ICL |     |     |
SWE-agent(Yangetal.,2024) Unimodal GPT-4 ✓ ✗ ✓ ✓ Software ICL ✗ ✗
DigiRL(Baietal.,2024) Multimodal DigiRL-1.3B ✗ ✗ ✓ ✓ GUI FT&RL ✗ ✗
|                         |     |     |            |     |       | ✓   | ✗   | ✓   | ✓   |     |        | ✗   | ✓   |
| ----------------------- | --- | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- | ------ | --- | --- |
| CLOVA(Gaoetal.,2024)    |     |     | Multimodal |     | GPT-4 |     |     |     |     | QA  | ICL&FT |     |     |
| MDagents(Kimetal.,2024) |     |     | Multimodal |     | GPT-4 | ✓   | ✓   | ✓   | ✗   | QA  | ICL    | ✓   | ✗   |
OS-Copilot(Wuetal.,2024) Multimodal GPT4 ✓ ✓ ✓ ✓ GUI ICL&FT ✓ ✓
detailedanalysesofvariouscomponentsofLLMagentsand
PrinciplesofBuilding LLM Agents
thecomparisondrawnwiththevonNeumannarchitecture,
Can LLMs solve the task?
weobservestrikingsimilaritiesthatcaninspireagentdesign.
| At the | same time, | viewing | from | a computer |     | perspective |     | Yes |     | No  |     |     |     |
| ------ | ---------- | ------- | ---- | ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
allowsustoidentifyshortcomingsincurrentagentdesigns
| and gain | further | inspiration. |     | In this | section, | we outline |     |          |                              |     |     |     |     |
| -------- | ------- | ------------ | --- | ------- | -------- | ---------- | --- | -------- | ---------------------------- | --- | --- | --- | --- |
|          |         |              |     |         |          |            |     | Use LLMs | Canaworkflow solve the task? |     |     |     |     |
somefuturedirectionsandcriticalchallengesthatdemand
|            |                                            |     |     |     |     |     |     |     |     | Yes | No  |     |     |
| ---------- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| attention. | Thesechallengeshighlighttheopportunitiesto |     |     |     |     |     |     |     |     |     |     |     |     |
advancethefield.
|     |     |     |     |     |     |     |     | Use a workflow with LLMs |     | DesignLLM agents |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | ---------------- | --- | --- | --- |
3.1.ThePrinciplesofBuildingAgents Follow three rules: abstraction,
modularity and scalability
Numerousprincipleshavebeenaccumulatedintheevolu-
tionofcomputers(AppendixC),whichguidethedevelop-
Figure4.Adesigndecisiondiagramillustratingtheprinciplesof
mentofcomputerarchitectures(Saltzer&Kaashoek,2009).
buildingLLMagents.
| By drawing | an  | analogy | and comparing |     | computer | system |     |     |     |     |     |     |     |
| ---------- | --- | ------- | ------------- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
designprinciples,wecanseethatbuildingLLMagentsalso
| requirescertainprinciples. |     |     | Here,weadvocatetheprinciple |     |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3.2.RefiningMemoryforGreaterImpact
| of “Build | agents | for demand”. |     | This | means | that agents |     |     |     |     |     |     |     |
| --------- | ------ | ------------ | --- | ---- | ----- | ----------- | --- | --- | --- | --- | --- | --- | --- |
shouldbedesignedonlywhenaproblemcannotbedirectly
|                                               |     |     |     |     |     |     | Theimportanceandroleofmemoryarewellrecognized. |     |     |     |     |     | In  |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- |
| solvedbyanLLMitselforbyconstructingaworkflow. |     |     |     |     |     | For |                                                |     |     |     |     |     |     |
computersystems,memoryisstructuredintofiner-grained
example,whenanAIisneededtoautonomouslyusevari-
levels,incorporatingcachemechanismsanddiverseread-
oustoolsandbrowsetheinternettocompletetasks,agents
and-writeoperationstooptimizeperformanceandefficiency.
| shouldbebuilt.                  |     | Thisprincipleisaccompaniedbythead- |     |                 |     |      |          |                                            |     |     |     |     |     |
| ------------------------------- | --- | ---------------------------------- | --- | --------------- | --- | ---- | -------- | ------------------------------------------ | --- | --- | --- | --- | --- |
|                                 |     |                                    |     |                 |     |      | However, | suchexplorationsremaininsufficientinthedo- |     |     |     |     |     |
| herencetothreedesignprinciples: |     |                                    |     | (1)Abstraction: |     | Hide |          |                                            |     |     |     |     |     |
mainofLLMagents,highlightingtheneedtorefinetheir
implementationdetailsandprovidesimplifiedinterfacesto
memorymechanismsforgreaterimpact.
| reducecomplexity. |     | (2)Modularity: |     | Breakagentsintofunc- |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------------- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tionalmoduleswithclearinterfaces. (3)Scalability: Agents Finer-GrainedMemory: AsshowninFigure3,computer
systemsformafine-grainedmemoryhierarchy,including
shouldbedesignedtoscaleefficientlywithgrowingusers,
data,orcomputationaldemandswithoutmajorchanges. A componentslikemainmemory,cache,andregisters. Agents
designdecisiondiagramisshowninFigure4. Moreover, can adopt this idea to design analogous modules. The
webelievethatmoreprincipleswillbediscovered. existing context window is similar to main memory, and
|     |     |     |     |     |     |     | databasesareakintodisks. |            |     | Wehavefoundthatthecache |     |      |         |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | ---------- | --- | ----------------------- | --- | ---- | ------- |
|     |     |     |     |     |     |     | module                   | is missing |     | in agents. Therefore,   | we  | call | for re- |
6

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
searchintothecachemoduleinLLMagents. Commonly andpowerefficiency,makingitidealformoderncomput-
used information in agents can be stored in a cache-like ingworkloads. Weadvocateincorporatingamulti-core
module,enablingquickretrievalofpastexperiencestoeffi- mechanismintoLLMagents,utilizinganappropriatenum-
cientlycompletecomplextasks.Thiscachemodulenotonly berofmodelstoserveasthecognitionmodulewithinthe
reducesmemorypressurebutalsofacilitatesthetrainingof agent. Specifically,theuniqueBig.LITTLE(ARM,2011)
LLMagents. Furthermore,theconstructionofthememory architectureinmulti-coresystemsreferstoadesignwhere
pyramidislargelydrivenbytheprincipleoflocality,which high-performance”big”coresandenergy-efficient”little”
emphasizesfocusingonthe”mostimportant20%.”Weposit coresareusedtogether,enablingoptimalperformanceand
thatasimilarformoflocalityexistsduringtheinteractions powerconsumption. LLMagentscandrawinspirationfrom
ofLLMagents,whichcouldserveasavaluableguidefor thisdesign. Largermodelscanberesponsibleforcomplex
futurememorydesign. planning and reasoning tasks, while smaller models can
managebasicoperationssuchasdialogueandinteractions
| DMA is | Useful in Memory: | When | drawing an | analogy                   |     |     |                       |     |     |
| ------ | ----------------- | ---- | ---------- | ------------------------- | --- | --- | --------------------- | --- | --- |
|        |                   |      |            | withmemoryandtoolmodules. |     |     | Thisdesignisanalogous |     |     |
withcomputermemorymechanisms,wefoundthatDirect
tothehumanbrain’sSystem1andSystem2,reflectingthe
MemoryAccess(DMA)(Khawaja&Khan,2014)canbe
rationalityofsuchadesign.
| effectiveforagents. | DMAimprovesdatatransferefficiency |     |     |     |     |     |     |     |     |
| ------------------- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
byenablingperipheraldevices(suchasharddrives)toex-
3.4.ParallelizationandPipelining
changedatawithmemorydirectly,bypassingtheCPUand
enhancingoverallsystemperformance. ForLLMagents, Parallelization: Parallelizationincomputersreferstothe
thismeansthataccessinstructionsdonotalwayshaveto techniqueofexecutingmultipleinstructionssimultaneously
gothroughtheLLM.Thisapproachcanoptimizedatare-
|     |     |     |     | by utilizing | multiple | processing | threads. | This highlights |     |
| --- | --- | --- | --- | ------------ | -------- | ---------- | -------- | --------------- | --- |
trievalbyallowinglong-termmemorytobewrittendirectly thecorrectnessofbreakingdownlargetasksintosub-tasks
| to short-term | memory. | At the same | time, LLMs | can fo- |     |     |     |     |     |
| ------------- | ------- | ----------- | ---------- | ------- | --- | --- | --- | --- | --- |
withinagents,whilealsosuggestingthatexistingagentsmay
cusonhandlingothertasksmoreefficiently. Forexample, benefitfromparallelprocessing. Consideringparalleliza-
VideoAgent(Fanetal.,2025)employssomeuniquemem- tion from both single-agentand multi-agent perspectives,
oryqueryingtoolstoretrievelong-termmemoryduringthe
forasingleagent,parallelizationmeansthatataskcanbe
question-answeringprocesswithoutrequiringdirectLLM processedsimultaneouslybyleveragingmultipletoolsor
access, enablingittoperformeffectivelyinlong-horizon
|     |     |     |     | LLMstoachieveacceleration. |     |     | Inamulti-agentsystem,a |     |     |
| --- | --- | --- | --- | -------------------------- | --- | --- | ---------------------- | --- | --- |
videounderstanding. taskcanbedistributedamongdifferentagents,whichthen
|                              |     |     |                | integrate | their outputs | to achieve | parallel | processing | and |
| ---------------------------- | --- | --- | -------------- | --------- | ------------- | ---------- | -------- | ---------- | --- |
| MemoryastheCenterofDataFlow: |     |     | Throughoutcom- |           |               |            |          |            |     |
improveaccuracy.
putersystemdevelopment,thevonNeumannarchitecture
initially centered on the CPU but shifted to a memory- Pipelining: Pipeliningincomputersisatechniquethatim-
| centric model | to optimize | data storage | and retrieval | effi- |     |     |     |     |     |
| ------------- | ----------- | ------------ | ------------- | ----- | --- | --- | --- | --- | --- |
provesinstructionthroughputbyoverlappingtheexecution
ciency. In current agent designs, LLMs drive the agent’s of multiple instructions. It divides the instruction cycle
| reasoningprocesses. | However,whenagentsinteractinreal- |     |     |     |     |     |     |     |     |
| ------------------- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
intodiscretestages,wheredifferentstagesofmultiplein-
worldenvironments,thelimitationsofthecontextwindow structionscanbeprocessedsimultaneously. Thisallowsfor
withinmodelsrestricttheirabilitytorespondeffectivelyto continuousdataflowandminimizesidletime,enhancing
| rapidlychangingconditions. |     | Thisraisesthepossibilitythat |     |         |              |           |            |          |     |
| -------------------------- | --- | ---------------------------- | --- | ------- | ------------ | --------- | ---------- | -------- | --- |
|                            |     |                              |     | overall | performance. | A similar | pipelining | approach | can |
futureagentsystemsmayadoptamemory-centricapproach alsobeadoptedinopen-worldagentstoimprovethespeed
to handle vast external information and enable real-time and accuracy of processing continuous external environ-
| interactionmoreeffectively. |     | Existingworks,suchasGen- |     |     |     |     |     |     |     |
| --------------------------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- |
mentalfeedback,whichisparticularlyevidentinembodied
erative Agents (Park et al., 2023), have explored designs intelligenceandautonomousdriving.
inthisdirection,butreal-timeinteractionremainsanarea
Inadditiontothemechanismsmentionedabove,webelieve
requiringfurtherstudy.
|     |     |     |     | that many | insights | can be drawn | from | computer | systems. |
| --- | --- | --- | --- | --------- | -------- | ------------ | ---- | -------- | -------- |
Thesedirectionsfurtherillustratethestrongcorrelationbe-
3.3.Multi-CoreSystem
|     |     |     |     | tween the | two fields, | suggesting | that the | current | design |
| --- | --- | --- | --- | --------- | ----------- | ---------- | -------- | ------- | ------ |
Multi-coremechanismsincomputersystemsenableparallel of LLM agents can fully leverage advancements in com-
processingbyintegratingmultipleprocessingcoreswithin putersystems. Furthermore,thesoftwarelayersdeveloped
a single CPU, allowing concurrent execution of tasks to throughtheevolutionofcomputing—suchassoftwaresys-
enhance performance and efficiency (Hennessy & Patter- tems and user interfaces—can also be applied to the ad-
son, 2011). Each core operates independently, handling vancementofLLMagents,highlightingtheirpotential.
separatethreadsorprocesses,improvingmultitaskingand
| throughput. | Thisarchitectureoptimizesresourceutilization |     |     |     |     |     |     |     |     |
| ----------- | -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
7

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
4.GobeyondComputers: LearningCapability tionedthreeapproacheswilllikelyformastandardized
| inLLMAgents               |              |                          |                |     |         | learningprocessforagentsinthefuture. |                  |         |              |           |
| ------------------------- | ------------ | ------------------------ | -------------- | --- | ------- | ------------------------------------ | ---------------- | ------- | ------------ | --------- |
|                           |              |                          |                |     |         | Memory Manage                        | and Tool         | Update: | In addition, | updat-    |
| If LLM agents             | only include | the                      | aforementioned |     | modules |                                      |                  |         |              |           |
|                           |              |                          |                |     |         | ing the memory                       | and tool modules |         | is another   | promising |
| andinteractionmechanisms, |              | theirrolesinanopen-world |                |     |         |                                      |                  |         |              |           |
setting would resemble that of a computer, which cannot direction, as such updates can enable agents to develop
|                    |         |              |     |        |           | uniquecharacteristics. | Memorymanagementreferstothe |     |     |     |
| ------------------ | ------- | ------------ | --- | ------ | --------- | ---------------------- | --------------------------- | --- | --- | --- |
| achieve Artificial | General | Intelligence |     | (AGI). | To answer |                        |                             |     |     |     |
processesofstoringandorganizinginformationduringsuch
howgeneralagentswillevolveafterconstruction,wefind
thatthecriticalfactorliesinthelearningmechanism,which interactions, forming a memory module characterized by
|                                |     |     |                      |     |     | specificenvironmentalfeatures. |     | Forinstance,Generative |     |     |
| ------------------------------ | --- | --- | -------------------- | --- | --- | ------------------------------ | --- | ---------------------- | --- | --- |
| doesnotexistincomputersystems. |     |     | Therefore,inthissec- |     |     |                                |     |                        |     |     |
tion,wewillexplorethefuturelearningmethodsofagents Agents(Parketal.,2023)placeamemorystreamattheir
core,extractingobservationsfromtheenvironmentintothe
| to go beyond | computers. | The | analysis | and | summary of |     |     |     |     |     |
| ------------ | ---------- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- |
mainmemoryandretrievingthembasedonspecificrules.
learningapproachesinexistingstudiescanalsobefoundin
| Table1. |     |     |     |     |     | Withoutmemorymanagement, |     | agentswouldlackconsis- |     |     |
| ------- | --- | --- | --- | --- | --- | ------------------------ | --- | ---------------------- | --- | --- |
tentbehaviors,underscoringtheeffectivenessoflearning
| LLM Learning: | LLMs           | are at      | the heart | of  | LLM agents,  |                                 |     |     |                  |     |
| ------------- | -------------- | ----------- | --------- | --- | ------------ | ------------------------------- | --- | --- | ---------------- | --- |
|               |                |             |           |     |              | withmemorymanagementmechanisms. |     |     | ICAL(Sarchetal., |     |
| and most      | agent learning | is achieved | through   |     | the learning |                                 |     |     |                  |     |
2024)introducesamethodforbuildingamemoryofmul-
capabilities of LLMs. Key learning methods include In- timodalexperiencesfromsub-optimaldemonstrationsand
contextLearning(ICL),Fine-tuning(FT),andReinforce-
|     |     |     |     |     |     | humanfeedback. | Itdemonstratesthatbydistillingandfil- |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------- | ------------------------------------- | --- | --- | --- |
mentLearning(RL).In-contextlearningisaparadigmthat teringexperiences,astheagent’slibraryofexamplesgrows,
allowslanguagemodelstolearntasksgivenonlyafewex- the agent becomes more efficient. Tool update refers to
| amples in | the form of | demonstration |     | (Dong | et al., 2022). |     |     |     |     |     |
| --------- | ----------- | ------------- | --- | ----- | -------------- | --- | --- | --- | --- | --- |
theprocessbywhichtoolsareupdatedthroughinteraction.
Specifically,earlystudiessuchasReAct(Yaoetal.,2022) The motivation for tool updates arises from the fact that
| and Voyager | (Wang et | al., 2023) | use | ICL to | drive LLMs |     |     |     |     |     |
| ----------- | -------- | ---------- | --- | ------ | ---------- | --- | --- | --- | --- | --- |
sometoolsoftenbecomeoutdatedormalfunction,suchas
inbuildingagents,achievinggoodresults. However,since anagentfailingtoretrieveupdateddatafromanoutdated
LLMs are not specifically trained for agent tasks and in- APIendpoint. OneinterestingworknamedCLOVA(Gao
| context learning | does | not modify | model | parameters, | the |     |     |     |     |     |
| ---------------- | ---- | ---------- | ----- | ----------- | --- | --- | --- | --- | --- | --- |
etal.,2024)introducesanoveltraining-validationprompt
performanceimprovementsachievablethroughin-context tuning scheme to efficiently update tools while avoiding
| learning | remain limited. | Fine-tuning |     | is a technique | that |                         |                              |     |     |     |
| -------- | --------------- | ----------- | --- | -------------- | ---- | ----------------------- | ---------------------------- | --- | --- | --- |
|          |                 |             |     |                |      | catastrophicforgetting. | Thisworkdemonstratesthattool |     |     |     |
updatesmodelparametersonagivendatasettoenablean
learningcanoptimizeboththemodelandthetoolsthem-
agenttolearnspecifictasks. Unlikefine-tuningforLLMs, selves. Insummary,thelearnablecomponentsofLLM
agentfine-tuninginvolvestrainingondiverselevelsofagent
agentsarenotlimitedtoLLMs;boththememoryandtool
trajectory data. Consequently, many studies (Chen et al., modulescanbeupdatedandlearnedthroughinteractions.
2023a;Zengetal.,2023;Yinetal.,2024)focusonobtain-
inghigh-qualitytrajectoryoperationdata,aimingtoequip
5.Conclusion
LLMagentswithrobustcapabilitiesintoolusage,memory
retrieval, and long-term trajectory planning. However, it This paper advocates for a novel perspective on building
cannotaddressout-of-domainchallengesduetotheabsence LLMagentsbydrawinginsightsfromcomputersystems,
of environmental learning. To address this issue, recent particularlythevonNeumannarchitecture. Tosupportour
studieshaveattemptedtointegrateRLintothelearningpro- claim,wehavedrawninspirationfromthevonNeumann
cess of LLM agents, enabling them to interact with their architectureanddesignedastructuredframeworkconsist-
environment. Forexample,AGILE(Heetal.,2024)treats ingofdistinctmodulesforagentcomponents—perception,
|     |     |     |     |     |     | cognition,memory,tools,andactions. |     |     | Wethensummarize |     |
| --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --------------- | --- |
theconstructionofLLMagentsasanRLproblem,using
theLLMasapolicymodelandfine-tuningitthroughProx- futuredirectionsbydrawinganalogiestothedevelopment
imal Policy Optimization (PPO) (Schulman et al., 2017). ofcomputersystems. Keyareasforimprovementinclude
DigiRL(Baietal.,2024)trainsdevicecontrolagentsvia establishing principles for building LLM agents, refining
atwo-stagefine-tuningprocess: firstinitializingthemodel memorystructures,utilizingmulti-coresystems,andlever-
|     |     |     |     |     |     | aging parallelization | and pipelining |     | to boost LLM | agent |
| --- | --- | --- | --- | --- | --- | --------------------- | -------------- | --- | ------------ | ----- |
withofflineRLandthentransitioningfromofflinetoonline
RL.However,RLtraininginLLMagentsoftensuffersfrom efficiency. Finally,wehaveinvestigatedthelearningmecha-
instabilityandthechallengeofdesigningeffectivereward nismsofLLMagentsandpointedoutthatimprovedlearning
functions,whichrequirefurtherresearchtoaddress. Itis methods are key to their future evolution. By leveraging
worthnotingthattheselearningmethodsarenotisolated. theseinsights,weaimtoguidethesystematicconstruction
ThepracticehasshownthatanLLMagentoftenemploys andevolutionofgeneralLLMagents. Inaddition,thesein-
multiplemethodssimultaneouslyduringthelearningpro- sightsstillrequirethoroughexperimentalvalidation,which
cess.Thishighlightsthattheintegrationoftheaforemen- wewillcontinuetoexploreinourfutureresearch.
8

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
References Fan, Y., Ma, X., Wu, R., Du, Y., Li, J., Gao, Z., and Li,
|     |     |     |     |     |     |     | Q. Videoagent: | Amemory-augmentedmultimodalagent |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | -------------------------------- | --- | --- | --- | --- |
Achiam,J.,Adler,S.,Agarwal,S.,Ahmad,L.,Akkaya,I.,
|     |     |     |     |     |     |     | for video | understanding. | In  | European | Conference | on  |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | -------- | ---------- | --- |
Aleman,F.L.,Almeida,D.,Altenschmidt,J.,Altman,S.,
ComputerVision,pp.75–92.Springer,2025.
| Anadkat,S.,etal. |     | Gpt-4technicalreport. |     |     | arXivpreprint |     |     |     |     |     |     |     |
| ---------------- | --- | --------------------- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:2303.08774,2023. Gao, Z., Du, Y., Zhang, X., Ma, X., Han, W., Zhu, S.-C.,
Ahn,M.,Brohan,A.,Brown,N.,Chebotar,Y.,Cortes,O., and Li, Q. Clova: A closed-loop visual assistant with
|     |     |     |     |     |     |     | toolusageandupdate. |     | InProceedingsoftheIEEE/CVF |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | -------------------------- | --- | --- | --- |
David,B.,Finn,C.,Fu,C.,Gopalakrishnan,K.,Hausman,
K.,etal. Doasican,notasisay: Groundinglanguage ConferenceonComputerVisionandPatternRecognition,
inroboticaffordances. arXivpreprintarXiv:2204.01691, pp.13258–13268,2024.
2022.
Gu,Y.,Zheng,B.,Gou,B.,Zhang,K.,Chang,C.,Srivas-
| ARM. Big.littleprocessing. |     |     | InARMWhitePaper.ARM |     |     |     |                                      |     |     |     |     |           |
| -------------------------- | --- | --- | ------------------- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --------- |
|                            |     |     |                     |     |     |     | tava,S.,Xie,Y.,Qi,P.,Sun,H.,andSu,Y. |     |     |     |     | Isyourllm |
Holdings,2011. secretlyaworldmodeloftheinternet? model-basedplan-
arXivpreprintarXiv:2411.06559,
ningforwebagents.
| Bai, H., | Zhou, | Y., Cemri, | M., | Pan, J., | Suhr, | A., Levine, |     |     |     |     |     |     |
| -------- | ----- | ---------- | --- | -------- | ----- | ----------- | --- | --- | --- | --- | --- | --- |
2024.
| S., andKumar, |        | A. Digirl: | Trainingin-the-wilddevice- |               |     |        |                |          |            |     |        |             |
| ------------- | ------ | ---------- | -------------------------- | ------------- | --- | ------ | -------------- | -------- | ---------- | --- | ------ | ----------- |
| control       | agents | with       | autonomous                 | reinforcement |     | learn- |                |          |            |     |        |             |
|               |        |            |                            |               |     |        | He, Y., Huang, | G., Lin, | Y., Zhang, | H., | Zhang, | Y., Li, H., |
ing. AdvancesinNeuralInformationProcessingSystems
|     |     |     |     |     |     |     | etal. Agile: | Anovelreinforcementlearningframework |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------------------------------------ | --- | --- | --- | --- |
(NeurIPS),2024.
|     |     |     |     |     |     |     | ofllmagents. | InTheThirty-eighthAnnualConference |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---------------------------------- | --- | --- | --- | --- |
onNeuralInformationProcessingSystems,2024.
| Bran, A.             | M., Cox, | S.,  | Schilter, | O., Baldassari, |                  | C., White, |                                |     |                      |                       |     |     |
| -------------------- | -------- | ---- | --------- | --------------- | ---------------- | ---------- | ------------------------------ | --- | -------------------- | --------------------- | --- | --- |
| A.D.,andSchwaller,P. |          |      | Chemcrow: |                 | Augmentinglarge- |            |                                |     |                      |                       |     |     |
|                      |          |      |           |                 |                  |            | Hennessy,J.L.andPatterson,D.A. |     |                      | ComputerArchitecture: |     |     |
| language             | models   | with | chemistry | tools.          | arXiv            | preprint   |                                |     |                      |                       |     |     |
|                      |          |      |           |                 |                  |            | AQuantitativeApproach.         |     | MorganKaufmann,2011. |                       |     |     |
arXiv:2304.05376,2023.
Burks,A.W.,Goldstine,H.H.,andvonNeumann,J. Pre- Hong,W.,Wang,W.,Lv,Q.,Xu,J.,Yu,W.,Ji,J.,Wang,Y.,
liminarydiscussionofthelogicaldesignofanelectronic Wang,Z.,Dong,Y.,Ding,M.,etal. Cogagent: Avisual
computing instrument. Institute for Advanced Study, language model for gui agents. In Proceedings of the
| 1946. |     |     |     |     |     |     | IEEE/CVFConferenceonComputerVisionandPattern |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- |
Recognition,pp.14281–14290,2024.
| Campbell-Kelly,M.andAspray,W. |     |     |     | Computer:      |     | AHistory |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
| oftheInformationMachine.      |     |     |     | WestviewPress, |     | Boulder, |     |     |     |     |     |     |
Huang,J.,Yong,S.,Ma,X.,Linghu,X.,Li,P.,Wang,Y.,
CO,1996.
|     |     |     |     |     |     |     | Li, Q.,                      | Zhu, S.-C., Jia, | B., and | Huang,             | S.  | An embod- |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | ---------------- | ------- | ------------------ | --- | --------- |
|     |     |     |     |     |     |     | iedgeneralistagentin3dworld. |                  |         | InProceedingsofthe |     |           |
Chen,B.,Shu,C.,Shareghi,E.,Collier,N.,Narasimhan,K.,
andYao,S. Fireact: Towardlanguageagentfine-tuning. InternationalConferenceonMachineLearning(ICML),
2024.
arXivpreprintarXiv:2310.05915,2023a.
Chen,W.-G.,Spiridonova,I.,Yang,J.,Gao,J.,andLi,C.
|     |     |     |     |     |     |     | Khawaja, | K. K. A. M. | and Khan, | A.  | A. Direct | memory |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --------- | --- | --------- | ------ |
Llava-interactive: An all-in-one demo for image chat, access:Overviewandapplications. InternationalJournal
segmentation, generation and editing. arXiv preprint ofComputerApplications,94(1):1–7,2014.
arXiv:2311.00571,2023b.
Kim,Y.,Park,C.,Jeong,H.,Chan,Y.S.,Xu,X.,McDuff,
| Dong, Q., | Li, L., | Dai, | D., Zheng, | C., | Ma, J., | Li, R., Xia, |                             |     |     |                       |     |     |
| --------- | ------- | ---- | ---------- | --- | ------- | ------------ | --------------------------- | --- | --- | --------------------- | --- | --- |
|           |         |      |            |     |         |              | D.,Breazeal,C.,andPark,H.W. |     |     | Adaptivecollaboration |     |     |
H.,Xu,J.,Wu,Z.,Liu,T.,etal. Asurveyonin-context strategyforllmsinmedicaldecisionmaking.Advancesin
| learning. | AnnualMeetingoftheAssociationforCompu- |     |     |     |     |     |     |     |     |     |     |     |
| --------- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
NeuralInformationProcessingSystems(NeurIPS),2024.
tationalLinguistics(ACL),2022.
Langley,P.Craftingpapersonmachinelearning.InLangley,
| Durante, | Z., Huang, | Q., | Wake, | N., Gong, | R., | Park, J. S., |     |     |     |     |     |     |
| -------- | ---------- | --- | ----- | --------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Sarkar,B.,Taori,R.,Noda,Y.,Terzopoulos,D.,Choi,Y., P.(ed.),Proceedingsofthe17thInternationalConference
onMachineLearning(ICML2000),pp.1207–1216,Stan-
| et al. | Agent | ai: Surveying | the | horizons | of  | multimodal |     |     |     |     |     |     |
| ------ | ----- | ------------- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
ford,CA,2000.MorganKaufmann.
| interaction. | arXivpreprintarXiv:2401.03568,2024. |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Fan,L.,Wang,G.,Jiang,Y.,Mandlekar,A.,Yang,Y.,Zhu, Lewis,P.,Perez,E.,Piktus,A.,Petroni,F.,Karpukhin,V.,
H.,Tang,A.,Huang,D.-A.,Zhu,Y.,andAnandkumar,A. Goyal,N.,Ku¨ttler,H.,Lewis,M.,Yih,W.-t.,Rockta¨schel,
Minedojo: Buildingopen-endedembodiedagentswith T.,etal. Retrieval-augmentedgenerationforknowledge-
internet-scaleknowledge. AdvancesinNeuralInforma- intensivenlptasks. AdvancesinNeuralInformationPro-
tionProcessingSystems,35:18343–18362,2022. cessingSystems,33:9459–9474,2020.
9

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
Lin, K. Q., Li, L., Gao, D., Yang, Z., Wu, S., Bai, Z., Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and
Lei, W., Wang, L., and Shou, M. Z. Showui: One Klimov, O. Proximal policy optimization algorithms.
vision-language-actionmodelforguivisualagent. arXiv arXivpreprintarXiv:1707.06347,2017.
preprintarXiv:2411.17465,2024.
|                                       |     |         |               |     |               |             | Shen, Y.,             | Song, K., | Tan,    | X., Li,                     | D., Lu, | W., and | Zhuang, |
| ------------------------------------- | --- | ------- | ------------- | --- | ------------- | ----------- | --------------------- | --------- | ------- | --------------------------- | ------- | ------- | ------- |
| Liu, B., Jiang,                       | Y., | Zhang,  | X., Liu,      | Q., | Zhang,        | S., Biswas, |                       |           |         |                             |         |         |         |
|                                       |     |         |               |     |               |             | Y. Hugginggpt:        |           | Solving | ai tasks                    | with    | chatgpt | and its |
| J., and Stone,                        |     | P. Llm+ | p: Empowering |     | large         | language    |                       |           |         |                             |         |         |         |
|                                       |     |         |               |     |               |             | friendsinhuggingface. |           |         | AdvancesinNeuralInformation |         |         |         |
| modelswithoptimalplanningproficiency. |     |         |               |     | arXivpreprint |             |                       |           |         |                             |         |         |         |
ProcessingSystems,36,2024.
arXiv:2304.11477,2023.
Lu,J.,An,S.,Lin,M.,Pergola,G.,He,Y.,Yin,D.,Sun,X., Shi,Z.,Gao,S.,Chen,X.,Feng,Y.,Yan,L.,Shi,H.,Yin,D.,
andWu,Y. Memochat: Tuningllmstousememosfor Ren,P.,Verberne,S.,andRen,Z. Learningtousetools
|     |     |     |     |     |     | arXiv | via cooperative |     | and interactive |     | agents. | arXiv | preprint |
| --- | --- | --- | --- | --- | --- | ----- | --------------- | --- | --------------- | --- | ------- | ----- | -------- |
consistentlong-rangeopen-domainconversation.
| preprintarXiv:2308.08239,2023. |     |     |     |     |     |     | arXiv:2403.03031,2024. |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |
Nakano,R.,Hilton,J.,Balaji,S.,Wu,J.,Ouyang,L.,Kim,
Shinn,N.,Cassano,F.,Gopinath,A.,Narasimhan,K.,and
C.,Hesse,C.,Jain,S.,Kosaraju,V.,Saunders,W.,etal.
|              |                                           |                                     |     |     |     |     | Yao, S.   | Reflexion: | Language |     | agents    | with        | verbal rein- |
| ------------ | ----------------------------------------- | ----------------------------------- | --- | --- | --- | --- | --------- | ---------- | -------- | --- | --------- | ----------- | ------------ |
| Webgpt:      | Browser-assistedquestion-answeringwithhu- |                                     |     |     |     |     |           |            |          |     |           |             |              |
|              |                                           |                                     |     |     |     |     | forcement | learning.  | Advances |     | in Neural | Information |              |
| manfeedback. |                                           | arXivpreprintarXiv:2112.09332,2021. |     |     |     |     |           |            |          |     |           |             |              |
ProcessingSystems,36,2024.
| Packer, C., | Wooders, | S., | Lin, | K., Fang, | V., Patil, | S. G., |     |     |     |     |     |     |     |
| ----------- | -------- | --- | ---- | --------- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
Stoica, I., andGonzalez, J.E. Memgpt: Towardsllms Wang,G.,Xie,Y.,Jiang,Y.,Mandlekar,A.,Xiao,C.,Zhu,
asoperatingsystems. arXivpreprintarXiv:2310.08560, Y., Fan, L., and Anandkumar, A. Voyager: An open-
|     |     |     |     |     |     |     | endedembodiedagentwithlargelanguagemodels. |     |     |     |     |     | arXiv |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | ----- |
2023.
preprintarXiv:2305.16291,2023.
| Park, J. S.,         | O’Brien, | J., | Cai, C.           | J., Morris, | M.  | R., Liang,  |     |     |     |     |     |     |     |
| -------------------- | -------- | --- | ----------------- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| P.,andBernstein,M.S. |          |     | Generativeagents: |             |     | Interactive |     |     |     |     |     |     |     |
Wang,X.,Wei,J.,Schuurmans,D.,Le,Q.,Chi,E.,Narang,
| simulacraofhumanbehavior. |     |     |     | InProceedingsofthe36th |     |     |                |     |         |       |                     |     |     |
| ------------------------- | --- | --- | --- | ---------------------- | --- | --- | -------------- | --- | ------- | ----- | ------------------- | --- | --- |
|                           |     |     |     |                        |     |     | S., Chowdhery, |     | A., and | Zhou, | D. Self-consistency |     | im- |
annualacmsymposiumonuserinterfacesoftwareand proves chain of thought reasoning in language models.
technology,pp.1–22,2023.
arXivpreprintarXiv:2203.11171,2022.
Patil,S.G.,Zhang,T.,Wang,X.,andGonzalez,J.E.Gorilla:
Largelanguagemodelconnectedwithmassiveapis.arXiv Wang,X.,Li,B.,Song,Y.,Xu,F.F.,Tang,X.,Zhuge,M.,
|     |     |     |     |     |     |     | Pan,J.,Song,Y.,Li,B.,Singh,J.,etal. |     |     |     |     | Openhands: | An  |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | ---------- | --- |
preprintarXiv:2305.15334,2023.
|     |     |     |     |     |     |     | open platform | for | ai software |     | developers | as  | generalist |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----------- | --- | ---------- | --- | ---------- |
Putta,P.,Mills,E.,Garg,N.,Motwani,S.,Finn,C.,Garg,
|                                   |           |     |       |             |               |           | agents.   | arXivpreprintarXiv:2407.16741,2024a. |      |          |          |     |            |
| --------------------------------- | --------- | --- | ----- | ----------- | ------------- | --------- | --------- | ------------------------------------ | ---- | -------- | -------- | --- | ---------- |
| D., and                           | Rafailov, | R.  | Agent | q: Advanced |               | reasoning |           |                                      |      |          |          |     |            |
| andlearningforautonomousaiagents. |           |     |       |             | arXivpreprint |           |           |                                      |      |          |          |     |            |
|                                   |           |     |       |             |               |           | Wang, Z., | Cai, S.,                             | Liu, | A., Jin, | Y., Hou, | J., | Zhang, B., |
arXiv:2408.07199,2024. Lin, H., He, Z., Zheng, Z., Yang, Y., et al. Jarvis-1:
Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J., Open-worldmulti-taskagentswithmemory-augmented
|                  |     |                                |     |     |     |     | multimodal | language |     | models. | IEEE | Transactions | on  |
| ---------------- | --- | ------------------------------ | --- | --- | --- | --- | ---------- | -------- | --- | ------- | ---- | ------------ | --- |
| Liu,Z.,andSun,M. |     | Communicativeagentsforsoftware |     |     |     |     |            |          |     |         |      |              |     |
PatternAnalysisandMachineIntelligence,2024b.
| development. |     | arXiv preprint |     | arXiv:2307.07924, |     | 6(3), |     |     |     |     |     |     |     |
| ------------ | --- | -------------- | --- | ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
2023.
Wei,J.,Wang,X.,Schuurmans,D.,Bosma,M.,Xia,F.,Chi,
Qin,Y.,Liang,S.,Ye,Y.,Zhu,K.,Yan,L.,Lu,Y.,Lin,Y.,
E.,Le,Q.V.,Zhou,D.,etal.Chain-of-thoughtprompting
Cong,X.,Tang,X.,Qian,B.,etal. Toolllm: Facilitating elicitsreasoninginlargelanguagemodels. Advancesin
largelanguagemodelstomaster16000+real-worldapis. neuralinformationprocessingsystems,35:24824–24837,
| arXivpreprintarXiv:2307.16789,2023. |     |                  |     |                      |        |           | 2022.        |           |       |             |         |          |            |
| ----------------------------------- | --- | ---------------- | --- | -------------------- | ------ | --------- | ------------ | --------- | ----- | ----------- | ------- | -------- | ---------- |
| Saltzer,J.H.andKaashoek,M.F.        |     |                  |     | PrinciplesofComputer |        |           |              |           |       |             |         |          |            |
|                                     |     |                  |     |                      |        |           | Wu, Z., Han, | C.,       | Ding, | Z., Weng,   | Z.,     | Liu, Z., | Yao, S.,   |
| System Design:                      |     | An Introduction. |     |                      | Morgan | Kaufmann, |              |           |       |             |         |          |            |
|                                     |     |                  |     |                      |        |           | Yu, T.,      | and Kong, | L.    | Os-copilot: | Towards |          | generalist |
2009. ISBN978-0123749574.
|     |     |     |     |     |     |     | computeragentswithself-improvement. |     |     |     |     | arXivpreprint |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | ------------- | --- |
Sarch, G., Jang, L., Tarr, M. J., Cohen, W. W., Marino, arXiv:2402.07456,2024.
| K., and | Fragkiadaki, |     | K. Vlm | agents | generate | their |     |     |     |     |     |     |     |
| ------- | ------------ | --- | ------ | ------ | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
ownmemories: Distillingexperienceintoembodiedpro- Xie, J., Chen, Z., Zhang, R., Wan, X., and Li, G.
grams. AdvancesinNeuralInformationProcessingSys- Large multimodal agents: A survey. arXiv preprint
| tems(NeurIPS),2024. |     |     |     |     |     |     | arXiv:2402.15116,2024. |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |
10

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
| Yang, J.,       | Jimenez, C. | E., Wettig, |     | A., Lieret, | K., Yao, |
| --------------- | ----------- | ----------- | --- | ----------- | -------- |
| S., Narasimhan, | K.,         | and Press,  | O.  | Swe-agent:  | Agent-   |
computerinterfacesenableautomatedsoftwareengineer-
ing. AdvancesinNeuralInformationProcessingSystems
(NeurIPS),2024.
Yao,S.,Rao,R.,Hausknecht,M.,andNarasimhan,K.Keep
calmandexplore:Languagemodelsforactiongeneration
| intext-basedgames. |     | arXivpreprintarXiv:2010.02903, |     |     |     |
| ------------------ | --- | ------------------------------ | --- | --- | --- |
2020.
Yao,S.,Zhao,J.,Yu,D.,Du,N.,Shafran,I.,Narasimhan,
| K.,andCao,Y.      | React: | Synergizingreasoningandacting  |     |     |     |
| ----------------- | ------ | ------------------------------ | --- | --- | --- |
| inlanguagemodels. |        | arXivpreprintarXiv:2210.03629, |     |     |     |
2022.
Yao,S.,Yu,D.,Zhao,J.,Shafran,I.,Griffiths,T.,Cao,Y.,
andNarasimhan,K.Treeofthoughts:Deliberateproblem
| solvingwithlargelanguagemodels. |     |     |     | AdvancesinNeural |     |
| ------------------------------- | --- | --- | --- | ---------------- | --- |
InformationProcessingSystems,36,2024.
Yin,D.,Brahman,F.,Ravichander,A.,Chandu,K.,Chang,
| K.-W., Choi, | Y., and  | Lin, B.         | Y. Agent | lumos:   | Unified |
| ------------ | -------- | --------------- | -------- | -------- | ------- |
| and modular  | training | for open-source |          | language | agents. |
InProceedingsofthe62ndAnnualMeetingoftheAsso-
| ciationforComputationalLinguistics(Volume1: |     |     |     |     | Long |
| ------------------------------------------- | --- | --- | --- | --- | ---- |
Papers),pp.12380–12403,2024.
| Yuan, S., Song, | K., Chen, | J.,               | Tan, X.,  | Shen, | Y., Kan, R., |
| --------------- | --------- | ----------------- | --------- | ----- | ------------ |
| Li, D., and     | Yang, D.  | Easytool:         | Enhancing |       | llm-based    |
| agents with     | concise   | tool instruction. |           | arXiv | preprint     |
arXiv:2401.06201,2024.
| Zeng, A.,         | Liu, M., Lu,                     | R., Wang, | B.,                      | Liu, X., | Dong, Y., |
| ----------------- | -------------------------------- | --------- | ------------------------ | -------- | --------- |
| andTang,          | J. Agenttuning:                  |           | Enablinggeneralizedagent |          |           |
| abilitiesforllms. | AnnualMeetingoftheAssociationfor |           |                          |          |           |
ComputationalLinguistics(ACL),2023.
| Zhang, C.,         | Yang, Z., Liu, | J.,                            | Han, Y., | Chen,      | X., Huang, |
| ------------------ | -------------- | ------------------------------ | -------- | ---------- | ---------- |
| Z., Fu, B.,        | and Yu, G.     | Appagent:                      |          | Multimodal | agents     |
| assmartphoneusers. |                | arXivpreprintarXiv:2312.13771, |          |            |            |
2023.
11

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
A.AnalogyExamples
OurFigure1comparesvonNeumannarchitectureandLLMagentarchitecturewithtaskexecutionworkflows.Thestructural
comparisonontheleftsidedemonstratesthesimilaritybetweenthetwoarchitectures,showingthattheyarehighlyalikein
termsofmodulesandtheirinterconnections. Ontherightside,theworkflowcomparisonduringtaskexecutionillustrates
thattheyalsosharesimilaritiesinhowtasksareperformed.
A.1.vonNeumannarchitecture
Tointuitivelydemonstratetheworkingprocessofacomputer(vonNeumannarchitecture),theexampleinourdiagramis
presentedusingthefollowingcode. ThefollowingPythonscriptnamedrun.pycalculatesthetotalsizeofallimagefilesina
givendirectory.
import os, sys
def Calculate_Sizes(directory):
image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
total_size = 0
for root, _, files in os.walk(directory):
for file in files:
if os.path.splitext(file)[1].lower() in image_extensions:
file_size = os.path.getsize(os.path.join(root, file))
total_size = total_size + file_size
print(f"Total size of images in ’{directory}’: {total_size} bytes")
if __name__ == "__main__":
directory = sys.argv[1]
Calculate_Sizes(directory)
A.2.LLMagentarchitecture
ForLLMagentarchitecture,weasksomeagenticsystemslikeChatGPT.Thequeryis”WhichelectronicproductdoIuse
andcheckitslatestprice”. Sincethediagramweuseisapreliminaryconceptualframeworkmainlyintendedtoillustrate
thesimilaritybetweenthetwo. Additionally,toprotectpersonalprivacy,wedonotprovideexecutiondiagramsforthe
exampleshere. YoucantrythispromptusingthemostadvancedmodelonyourpersonalChatGPT.
B.FrameworkFormalization
Inthisappendix,weprovideadetaileddescriptionofeachcomponentintheproposedframeworkF =(P,C,M,T,A),
asillustratedin Figure2. Thisframeworkconsistsofperception,cognition,memory,toolusage,andactionexecution,
facilitatinginteractionwithanopen-worldenvironment.
B.1.PerceptionModule
Theperceptionmoduleprocessesexternalinputsfromtheenvironment,supportingbothunimodalandmultimodaldata
processing:
P :O →X, (2)
whereOrepresentsrawobservations,andX denotestheextractedfeaturerepresentations. Thismoduleenablestheagentto
interpretsensorydatafrommultiplesourcessuchasimages,text,andaudio. Itisnoteworthythatpastobservationsare
oftencombinedwithpastactionsforperception,whereactionsalsoserveasanexternalsourceofinformation. Ofcourse,
indifferentdesigns,pastactionsandobservationscanbestoredinmemory,butthistransformationdoesnotbringabout
significantchanges.
12

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
B.2.CognitionModule
Thecognitionmoduleservesasthecorereasoningengine,responsibleforplanninganddecision-making. Ittakesperceptual
inputsx ,memorycontentM ,andtooluseoutputT asinputstogenerateintermediatedecisions.
| t   |     | r   |     | c   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
C :(X,M,T)→D,
(3)
whereDrepresentsthecognitivedecisionoutputspace. AdvancedreasoningtechniquessuchasChain-of-Thought(CoT),
Tree-of-Thought(ToT),andReflectionmechanismsareemployedtoenhancedecision-making.
B.3.MemoryModule
Memorymanagementintheframeworkincludesbothshort-term(contextwindow)andlong-term(retrieval-augmented
generation,RAG)storage,formulatedas:
|     |     |     |     | M   | :H→M, |     |     | (4) |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- |
whereHrepresentsthehistoricalinteractionsequence,andMdenotesthememorycontentretrievedforcurrentprocessing.
Keymemoryoperationsinclude:
| • MemoryWrite: | Storingnewexperiencem |     |     | .   |     |     |     |     |
| -------------- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
t
| • MemoryRead:   | Retrievingrelevanthistoricaldata. |                              |     |     |     |     |     |     |
| --------------- | --------------------------------- | ---------------------------- | --- | --- | --- | --- | --- | --- |
| • MemoryManage: |                                   | Optimizingmemoryutilization. |     |     |     |     |     |     |
B.4.ToolModule
ThetoolmoduleenablesinteractionwithexternaltoolsetsourcessuchasGoogleSearchandArxiv. Itincludesoperations
likeretrieval,calling,andupdating:
|     |     |     |     | T   | :(Q,E)→T, |     |     | (5) |
| --- | --- | --- | --- | --- | --------- | --- | --- | --- |
whereQisthequeryspace,E denotestoolsetresources,andT representsthetooloutputusedindecision-making.
B.5.ActionModule
Theactionmoduleselectsandexecutesactionsbasedoncognitiveoutputsandtoolassistance:
|     |     |     |     | a =A(C(x | ,M  | ,T )), |     | (6) |
| --- | --- | --- | --- | -------- | --- | ------ | --- | --- |
|     |     |     |     | t        | t   | r c    |     |     |
fortimestept,ithas:
|     |     |     | (cid:18) |         |        |       | (cid:19) |     |
| --- | --- | --- | -------- | ------- | ------ | ----- | -------- | --- |
|     |     |     |          | (cid:0) |        |       | (cid:1)  |     |
|     |     |     | a =A C   | P(o ,a  | ,...,o | ,a ,o | ),M ,T , | (7) |
|     |     |     | t        | 1 1     | t−1    | t−1   | t r c    |     |
whereT istheretrievedtoolinformation. Actionscanbecategorizedintointernalandexternaltypes. Forexternalactions,
c
theyaltertheexternalenvironment,transitioningfromo t−1 too t . Internalactionsinvolvesearchingmemory,invokingtools,
andperformingreasoning,whichdonotdirectlyaffectexternalobservationsbutinsteadmodifytheinternalstateofthe
LLMagents.
B.6.LearningParadigms
Ourframeworksupportsmultiplelearningapproachestoenhanceperformanceovertime:
B.6.1.IN-CONTEXTLEARNING
In-contextlearningallowsthemodeltomakepredictionsbasedonprovidedexampleswithoutupdatingparameters:
|     |     |     | a =argmaxP(a|o |     | ,a  | ,...,o | ,a ,o ) | (8) |
| --- | --- | --- | -------------- | --- | --- | ------ | ------- | --- |
|     |     |     | t              |     | 1   | 1 t−1  | t−1 t   |     |
a∈A
13

BuildingLLMAgentsbyIncorporatingInsightsfromComputerSystems
B.6.2.FINE-TUNING
Fine-tuningadjustsmodelparametersusingadatasetDwithgradient-basedoptimization:
(cid:88)
θ∗ =argmin L(f (x),y) (9)
θ
θ
(x,y)∈D
whereLrepresentsthelossfunctionandθaremodelparameters.
B.6.3.REINFORCEMENTLEARNING
In reinforcement learning (RL), the agent learns through interactions with the environment by maximizing cumulative
rewards:
(cid:34) T (cid:35)
(cid:88)
π∗ =argmaxE γtR(s ,a ) (10)
t t
π
t=0
whereπisthepolicy,γ isthediscountfactor,andRrepresentstherewardfunction.
C.Goldeninsightsofcomputersystemdesign
Goldeninsightsofcomputersystemdesign
Abstraction: Hideimplementationdetailsandprovidesimplifiedinterfacestoreducecomplexity.
Modularity: Breakthesystemintofunctionalmoduleswithclearinterfaces.
Unifieddatarepresentation: Unifieddatarepresentationensuresseamlessmoduleintegration.
Scalability: Systemsshouldbedesignedtohandlegrowthintermsofusers,data,orcomputationalrequirements
withoutsignificantre-architecture.
Theend-to-endprinciple: Thisprinciplestatesthatcertainfunctionsinasystemshouldbeimplementedatthe
endpointsratherthaninthemiddleofacommunicationsystem. Forexample,reliabilitymechanismslikeerror
checkingaremoreeffectivewhenplacedattheapplication’sendpointsratherthaninintermediatenetworklayers.
Theprincipleofleastprivilege: Asystemcomponentorusershouldonlyhavetheminimumprivilegesnecessary
toperformitstasks. Thisminimizestheriskofmisuseorerrorsaffectingtheoverallsystem.
Layering: Systemsshouldbebuiltinlayers,whereeachlayerprovidesaspecificsetofservicestothelayerabove
whileusingtheservicesofthelayerbelow. Thishierarchicalapproachaidsinabstractionandsimplifiesdebugging
andmaintenance.
The robustness principle (Postel’s Law): “Be conservative in what you do, be liberal in what you accept
fromothers.”Thisprincipleencouragesdesigningsystemstobestrictinoutputandtolerantininputtopromote
interoperability.
Fail-FastSystems: Asystemshoulddetectandreporterrorsasearlyaspossible, ratherthanallowingthemto
propagateunnoticed. Thishelpsmaintainsystemintegrityandsimplifiesdebugging.
Concurrency: Systemsshouldefficientlymanagemultiplesimultaneousactivities,takingadvantageofparallelism
whenpossible.
Transparency: A system should aim to hide complexity from users where appropriate, such as in distributed
systems,wherefailuresorlocationdetailsareoftenmasked.
Trade-off: System design involves balancing trade-offs, such as performance vs. correctness, simplicity vs.
flexibility,andlatencyvs. throughput.
14