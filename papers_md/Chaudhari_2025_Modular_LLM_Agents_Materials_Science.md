communications materials
Article
ANaturePortfoliojournal
https://doi.org/10.1038/s43246-025-00994-x
Modular large language model agents for
multi-task computational materials
science
Checkforupdates
AkshatChaudhari1,JanghoonOck 2,3 &AmirBaratiFarimani 2,4,5,6
Theintegrationoflargelanguagemodels(LLMs)withdomain-specificcomputationaltoolsprovidesa
pathwaytostreamlineandenhancematerialsscienceworkflows.ThispaperintroducesMatSciAgent,
amulti-agentframeworksupportingtaskssuchasmaterialsdataretrieval,continuumsimulation,
crystalstructuregeneration,andmoleculardynamicssimulation.Atitscoreisamasteragentthat
interpretsuserqueries,identifiesthetasktype,anddelegatestotask-specificagent(s)equippedwith
tools.LeveragingdatabasessuchasMaterialsProjectandMatWeb,theframeworkretrievesand
summarizesmaterialsdatawithgrounded,factualresponses,addressinglimitationsofvanillaLLMs.
Whenatargetmaterialisabsentfromdatabases,agenerativeagentcanproposeplausiblecrystal
structures.Forsimulations,specializedagentsextractparameterstoperformcontinuumand
moleculardynamicssimulationsusingexistingsoftwareorcustomcode.MatSciAgentdemonstrates
stability,withparameterextractionachieving100%successacrossfiverunsandmaterialsextraction
consistentin9of10runs.Itsmodulardesignensuresseamlessextensibilitytoevolveasnew
capabilitiesareintegrated.
Materials science and engineering are central to technological progress, remainsasignificantchallenge.Thislackofintegrationlimitstheseamless
enabling the discovery, design, and optimization of materials tailored to use of computational resources and hinders the pace of innovation in
specificperformancerequirements.Emergingindustriessuchasaerospace, materialsdesign11.
energy, and biotechnology increasingly demand materials with precisely Recentadvancesinartificialintelligence–especiallytheemergenceof
engineeredmechanical,thermal,andelectricalproperties.Designingsuch largelanguagemodels(LLMs)havereshapedhowresearchersengagewith
materials is a complex and iterative process that requires deep domain complex data and derive scientific insights. Built on transformer
expertiseandadvancedcomputationaltechniques.Asaresult,researchers architectures12,thesemodelsexcelatunderstandingandgeneratingnatural
are increasingly leveraging computational tools to predict and optimize languagethroughself-attentionmechanisms,enablingscalableprocessing
materialbehavior,acceleratingthedevelopmentofmaterialswithtargeted oflanguage-basedinformation.LLMs,suchasOpenAI’sGPTmodels13,14,
functionalities1,2. Meta’sLLaMA15,andAnthropic’sClaude16,havedemonstratedexceptional
This shift has driven the creation of large-scale materials databases capabilities in interpreting user queries, synthesizing information from
including the Materials Project3, MatWeb4, OQMD5, and ICSD6–which diverse sources, and producing actionable insights. In the context of
serve as critical resources for data-driven materials discovery. Predictive materialsscience,LLMssupporttaskssuchasinformationextractionfrom
modelsbuilton these databasesareincreasinglyusedto guide materials largedatabases,literaturemining,andhypothesisgeneration.Theirability
designdecisions7.Inparticular,generativemodels–machinelearningalgo- to process unstructured natural language queries allows researchers to
rithmsthatlearnpatternsfromdatatogeneratenew,plausiblecandidates intuitively explore complex datasets, reducing manual effort and accel-
arebeingadoptedtoproposematerialcompositionsorstructures,further eratingscientificworkflows17–19.Additionally,transformer-basedlanguage
acceleratingdiscovery8–10.However,despitetheseadvancements,integrat- models have proven effective as encoders for property prediction tasks
ing various simulation tools and data sources into a unified framework acrossarangeofscientificdomains,includingmetal-organicframeworks20,
1DepartmentofMaterialScienceandEngineering,CarnegieMellonUniversity,5000ForbesAvenue,Pittsburgh,PA,USA.2DepartmentofChemicalEngineering,
CarnegieMellonUniversity,5000ForbesAvenue,Pittsburgh,PA,USA.3DepartmentofChemicalandBiomolecularEngineering,UniversityofNebraska–Lincoln,
Lincoln,NE,USA.4DepartmentofMechanicalEngineering,CarnegieMellonUniversity,5000ForbesAvenue,Pittsburgh,PA,USA.5DepartmentofBiomedical
Engineering,CarnegieMellonUniversity,5000ForbesAvenue,Pittsburgh,PA,USA.6MachineLearningDepartment,CarnegieMellonUniversity,5000Forbes
Avenue,Pittsburgh,PA,USA. e-mail:jock2@unl.edu;barati@cmu.edu
CommunicationsMaterials| ( 2026) 7:131 1
;,:)(0987654321 ;,:)(0987654321

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.1|MatSciAgentarchitecture.Thisillustrationshowcaseshoweachagentleveragesinputfromtheuser,integrateswithdomain-specifictools,andutilizesthereasoning
capabilitiesoftheLLMtoprocesstasksandgenerateoutputs.OpenAI'sGPT-3.5-turboservesasthecoreLLMinthisframework.
polymers21, catalysis18,19, proteins22–25, inorganic crystals26,27, and additive proxiesthatautomatethesetupandexecutionofsimulationworkflows.
manufacturing28. Severalhybridframeworkshaveemergedtosupportthisvision–LLaMP40,
LLMsarenowbeingintegratedintoagenticframeworksthatextend HoneyComb41,andAtomAgents42whichcoupleLLMswithscientifictools
theirutilityfrompassivequeryinterpretationtoactivescientificproblem- anddatabases.LLaMP andHoneyCombprimarilyfunctionasretrieval
solving29,30. These LLM agents leverage the model’s language under- agents, leveraging data sources like the Materials Project, arXiv, and
standing, pre-trained knowledge, and emerging planning abilities to Wikipedia. AtomAgents is a specialized intelligent system for alloy
autonomously perform complex tasks. For instance, Boiko et al. intro- development, integrating multimodal perception (e.g., microstructure
duced Coscientist, an LLM-driven agent that automates experimental images, compositional data, phase diagrams) with domain-specific rea-
design and execution, substantially reducing manual effort31. Similarly, soningandmaterialsdesigntools.Itscorefunctionalityliesingenerating
ChemCrow combines LLMs with chemistry-specific tools to support andoptimizingalloycompositions,predictingproperties,andsuggesting
synthesis planning and materials discovery32. Such agentic systems are processing pathways tailored towards performance requirements. As
beingappliedacrossdiversescientificdomains,includingnotonlymate- researchcontinues,thereisagrowingneedforamoregeneralizableand
rialsscienceandchemistrybutalsofieldslike3Dprintingandengineering modularframeworkthatcanaccommodateabroaderrangeofmaterials
design33,34. systemsandsimulationtasks,whileremainingflexibleenoughtoincor-
While LLMs demonstrate strong capabilities in natural language poratenewlydevelopedcomputationaltools.
processing and general reasoning, their application in specialized WeproposeMatSciAgent,amulti-agentframeworkthatintegratesan
scientific domainssuchasmaterialssciencepresentsseveralchallenges. LLMwithspecializedcomputationaltoolstoperformtasksbasedonnatural
Oneofthemostsignificantconcernsishallucination,whereLLMsproduce languageuserqueries.AsillustratedinFig.1,thesystemsupportsfourtask
information that appears plausible but is factually incorrect35–37. Such types:materialsretrieval,continuumsimulation,crystalstructuregenera-
outputscanmisleadresearchers,disruptworkflows,andleadtowasted tion,andmoleculardynamicssimulation.Eachtaskishandledbyadedi-
resources.Thisissueisparticularlyproblematicwheninterpretingtech- catedtask-specificagent,coordinatedbyacentralmasteragent.Themaster
nicaldatasets,asLLMsaretypicallytrainedongeneral-purposecorpora agentinterpretstheuser’sinput,determinesthetypeoftask,anddelegates
that lack sufficient coverage of domain-specific materials science thequerytotheappropriatetask-specificagent.Theassignedagentthen
knowledge38,39. selectstherelevantcomputationaltoolsneededtocompletethetask.All
Furthermore,LLMsaloneareinherentlylimitedindeliveringrigor- decisions,fromtaskclassificationtotoolselection,areguidedbytherea-
ousscientificpredictionsforcomplexphysicalphenomena,assuchtasks soningcapabilitiesoftheLLM.ThisframeworkdemonstrateshowLLMs
requirehigh-precision,physics-basedsimulationsandvalidatednumerical can enhance computational materials science by automating workflows,
methods. To overcome this limitation, LLMs must be integrated with improving accessibility to simulation tools, and accelerating research
domain-specific scientific software, enabling them to function as user processes.
CommunicationsMaterials| ( 2026) 7:131 2

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.2|ComponentsofanLLMagent.Userinputisstructuredusingaprompt enginerunsthespecifiedtoolandupdatesthescratchpadwiththeresults.This
templatethatincludesasystemmessage,dialoguehistory,userquery,anda updatedscratchpadisreintegratedintotheprompttemplateforiterativeprocessing.
scratchpadforintermediateresults.TheLLMprocessestheprompt,andanoutput Thefinalresultisproducedoncenofurthertoolinvocationsarerequired.
parserdetermineswhetheratoolinvocationisneeded.Ifso,thetoolexecution
Resultsanddiscussions property data extraction. The LLM remains focused on reasoning and
Multi-agentsystem decision-makingwhiledelegatingcomputationallyintensiveoperationsto
Theworkflowconsistsoftwokeysteps:First,whenausersubmitsaquery,a thesetools.Acentralizedexecutionframeworkmanagesinputparsing,tool
masteragentclassifiesthetasktypeandroutesthequerytotheappropriate invocation,andresponseformatting,ensuringseamlessinteractionbetween
task-specific agent. Then, the task-specific agent selects and deploys the theLLM’sreasoningandthetools’deterministiccomputations.Fordetails
mostsuitablecomputationaltoolstosolvetheproblem,deliveringresults abouttheindividualagents,kindlyrefertotheMethodssection.
backtotheuser.BuiltonOpenAI’sGPT-3.5-turbo,itemployscustomized
promptsfordomain-specificreasoningandtoolintegration.Themodular Materialsextraction∣Case1.Synthesisofperovskiteoxidesfor
architecturesupportsdiversetasks,includingdataextraction,continuum solarcells
simulations, crystal structure generation, and molecular dynamics (MD) Thetaskbeginswiththeuserquery:"Providesynthesisdetailsforperovskite
simulations,ensuringeasyexpansionwithnewagents,tools,orworkflows. oxides used in solar cells.” (Full prompt and response shown in Supple-
Each individual agent is powered by an LLM, equipped with task- mentary Information Case 1.) A comparison between the materials
specifictools,andoperateswithsharedmemorysupportedbyascratchpad, extractionagentandthevanillaGPT-3.5-turboissummarizedinFig.3.The
asshowninFig.2.Akeystrengthisitsagenticdesign,whereeachagent materialsextractionagentfirstidentifieskeytermsfromthequerynamely
operatesindependentlyandisequippedwithspecializedtoolsandprompts. "perovskite”and"solarcells”usingitsreasoningcapabilities.Ittheninvokes
Thescratchpadmechanismfacilitatesinformationexchangeprocesswithin thematerialsprojectAPItoretrieverelevantdatafromthedatabase.
theframework.Whenauserqueryentersthesystem,theMatSciAgent This approach enables the agent to deliver more specific and detailed
selects the appropriate agent to handle the request. Initially empty, the information than the vanilla GPT-3.5-turbo. For example, it identifies
scratchpadbeginsrecordingtheagent’sreasoningandactions.Astheagent specific compositions such as La 0.8 Sr 0.2 Co x Fe 1−x O 3 and provides corre-
identifiesaneedforspecificinformation,itinvokesappropriatetoolsand sponding precursor details. It also outlines precise synthesis protocols,
theseinvocationsareaddedtointermediatesteps.Thetoolexecutesand includingtemperatureconditionsandduration.Incontrast,GPT-3.5-turbo
returns results, which are then formatted and pushed back into the returns only generic information and fails to offer detailed synthesis
scratchpad.Eachtimetheagentiscalled,itreceivesthisupdatedscratchpad procedures.
containingallprevioustoolcallsandresults,enablingcontinuous,coherent
reasoning.Thisprocessallowstheagenttoprogressivelybuildknowledgeby Materialsextraction∣Case2.BondinginformationforTiO
2
trackingpreviousfindings,connectingdifferentpiecesofinformation,and The user input query in this task specifies a particular material and
maintainingcontextthroughoutmulti-stepworkflows.Theagentcontinues requested properties, such as: "Retrieve bond length and coordination
thiscycleuntilithasgatheredsufficientinformationtoformafinalresponse, informationforTiO .Listyourresults.”(Fullpromptandresponseshown
2
whichisthenextractedandpresentedtotheuser.TheLLMservesasthe inSupplementaryInformationCase2).Theagentfirstidentifiesthetaskas
reasoninglayer,dynamicallyinterpretingqueriesandorchestratingtooluse. a material/property extraction query and summarizes the retrieved
BycombiningLLM-drivenreasoningwiththe precisionofcomputation information,asshowninFig.4.Inthiscase,thetargetmaterialisTiO ,and
2
tools,thesystemcanhandlecomplexqueries,performprecisecalculations, thepropertiesofinterestarebondlengthsandcoordinationenvironments.
andgenerateanalyzableinsights. BecauseTiO existsinmultiplestructuralformseachassociatedwitha
2
Promptengineeringandstructuredtoolintegrationenhanceadapt- uniquematerialIDtheagentbeginsbyretrievingallrelevantmaterialIDs.
ability.Carefullydesignedpromptsdefineeachagent’soperations,while It then uses a set of tools to extract the bonding properties for each
integratedtoolshandlespecializedcomputationslikeMDsimulationsor structure.
CommunicationsMaterials| ( 2026) 7:131 3

| https://doi.org/10.1038/s43246-025-00994-x |     |     |     |     |     | Article |
| ------------------------------------------ | --- | --- | --- | --- | --- | ------- |
Fig.3|Synthesisdetailsgeneration.aUserqueryspecifyingtheintendedretrievalobjective.bOutputfromthematerialsextractionagent(fullpromptinSupporting
Information).cOutputfromGPT-3.5-turbo.
BecausetheagenthasaccesstotheMaterialsProjectdatabase,itgen- materialsandgeneratesastructuredresponse(Fig.5b).Forcomparison,
eratesresponsepromptsbasedonreal,up-to-datedata.Incontrast,thevanilla Fig. 5c shows the output from the vanilla GPT-3.5-turbo for the
| GPT-3.5-turboreliessolelyonitspre-trainedknowledge,withoutaccessto |     |     | sameinput. |     |     |     |
| ------------------------------------------------------------------ | --- | --- | ---------- | --- | --- | --- |
externalsources.Althoughonlyonesummaryisshownbelowforillustration, The agent identifies example materials within the specified heat
theagentproducesaseparatesummaryforeachretrievedstructure,ensuring capacityrangeandsupplementsthiswithadditionalthermal,mechanical,
thoroughcoverageofallknownstructuralvariantsofthematerial. andcompositionalproperties.Forinstance,silver(Ag)isretrievedwitha
specificheatcapacityof0.234J/g⋅°C,alongwithadensityof10.491g/cc,
| Materialsextraction∣Case3:Materialswithinaspecificheat |     |     |                      |           | ⋅              |                    |
| ------------------------------------------------------ | --- | --- | -------------------- | --------- | -------------- | ------------------ |
|                                                        |     |     | thermal conductivity | of 419W/m | K, and melting | point of 961.93°C. |
capacityrange Aluminum (Al), with a specific heat capacity of 0.900J/g ⋅ °C, is also
Theuserqueryspecifiesatargetpropertyrange–specificheatcapacities returned,featuringalowdensityof2.6989g/ccandthermalconductivityof
between 0.1 and 2.0J/g ⋅ °C–along with additional guidelines, such as 210W/m ⋅ K. Additionally, the agent includes argon (Ar), a gas with a
ensuringmaterialdiversityandprioritizingexperimentallyverifieddata specificheatcapacityof0.520J/g⋅°C,demonstratingitsabilitytohandlea
(Fig.5a)(FullpromptandresponseshowninSupplementaryInformation widerangeofmaterialtypes.
Case3).Theagentbeginsbyidentifyingthepropertyofinterestandits Incontrast,thevanillaGPT-3.5-turbocanidentifymaterialsthatfall
specified withinthespecifiedheatcapacityrangebutfailstoprovideaccompanying
| range, then queries | the MatWeb database | to retrieve relevant |     |     |     |     |
| ------------------- | ------------------- | -------------------- | --- | --- | --- | --- |
CommunicationsMaterials|  (        2026) 7:131  4

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.4|Material-specificinformationretrieval.aUserqueryspecifyingthetargetmaterial.bOutputfromthematerialsextractionagent(fullpromptinSupporting
Information).cOutputfromGPT-3.5-turbo.
propertydata.Thisomissionwouldrequireadditionalsearches,reducingits Continuumsimulation∣Case3:Polycrystallinegraingrowth
overallutilityforcomprehensivematerialsanalysis. usingMonteCarloannealing
This task involves performing an MCA simulation to model poly-
Continuumsimulation∣Case1:Al-Cu-Mgalloysolidificationwith crystalline grain growth as shown in Fig. 8. Unlike the previous two
diffusion-controlledgrowth casestudies,theagentappliestheMCAsimulationtoolbasedonthe
Theuserprovidesaqueryspecifyingthedesiredsimulationconditions,as descriptionprovidedintheuserquery.Thesimulation,conductedon
illustrated in Fig. 6a. The agent interprets the input, extracts actionable a 50×50 lattice grid, demonstrates classic grain coarsening
simulation parameters such as: width, attachment probability, and the behavior–larger grains grow at the expense of smaller ones. The
numberofsolidphases;andselectstheappropriatetool–inthiscase,theCA lattice initially contains randomly oriented grains, but over the
toolforsimulatingphasetransformations.ItthenrunstheCAsimulation course of 100 Monte Carlo steps, the system evolves to minimize
using the derived parameters and generates a summary of the results, interfacial energy. Grain boundaries shift, especially at interfaces
including a visualization of the phase diagram. The evolution of the where different grains meet, driving the reduction of total grain
microstructureiscapturedframebyframe,asshowninFig.6b,highlighting boundary energy. This results in a coarser microstructure, char-
randomlyseedednucleidistributedacrossthedomainandformingden- acterized by fewer, larger grains–consistent with the typical grain
driticgrowthpatternstypicalofdiffusion-controlledsolidification. growth behavior observed during the annealing of polycrystalline
materials.
Continuumsimulation∣Case2:Ti-Alintermetallicalloysolidifi-
cationwithinterface-controlledgrowth Crystalgeneration∣Case1:CIFforalloy
In this case study, the continuum simulation agent is applied to model The task begins with a user query specifying the chemical formula
interface-controlledgrowthinanalloysystem.Theagentinterpretstheuser’s andspacegroupofacrystalmaterial(Fig.9(a)).Theagentinterprets
natural language query, extracts the relevant simulation parameters, and thispromptandextractstherelevantcrystallographicparameters–in
executes a CA simulation to generate frame-by-frame images of micro- this case, the composition of the Ni Al alloy and the space group
3
structuralevolutionduringsolidification,asshowninFig.7.Thesimulation Pm3m. Using CrystaLLM8 as a tool, the agent generates a corre-
resultsrevealsmooth,isotropicgrowthbehavior,characterizedbyuniformly sponding CIF file, which describes the crystal structure visualized in
expandinggrainswithouttheformationofdendriticarms–consistentwith Fig. 9(b). Based on the CIF file, the agent constructs a natural lan-
thehighattachmentprobabilityconditions.Controllednucleation,setat50 guage response that includes precise lattice parameters (a=b=c=
nucleiper unit area, leads to evenly distributedgrains across the domain, 3.5555)andatomicpositions(Alat(0,0,0)andNiat (0,0.5,0.5)),
resultinginahomogeneousmicrostructure.Thehighattachmentprobability consistent with the specified symmetry and stoichiometry. In addi-
also enhances solid-liquid interface kinetics, promoting the formation of tion to atomic coordinates, the CIF file also contains elemental
uniformlysizedgrainswithminimalsolutesegregation. properties such as electronegativity and ionic radii.
CommunicationsMaterials| ( 2026) 7:131 5

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.5|Materialsextractionbasedontargetpropertyrange.aUserqueryspecifyingthedesiredpropertyrange.bOutputfromthematerialsextractionagent(fullprompt
inSupportingInformation).cOutputfromGPT-3.5-turbo.
CrystalGeneration∣Case2:CIFforarbitrarycompounds temperaturestabilizeswithinarangeof~471K−685K.Thecorresponding
Foranarbitrarymaterial,SrFeMoO inthedoubleperovskitestructure,the MDtrajectorycanbefoundinSupplementaryData1.
2 6
agentdemonstrateditsabilitytotranslatenaturallanguage-basedqueries
intocrystallographicdescription,asshowninFig.10.TheresultingCIFfile JointImplementation
provides structural details, including lattice parameters (a=b=5.65Å, To demonstrate the capability of our LLM agent system to coordinate
c=3.9733Å,α=β=γ=90°)andatomicpositionsforSr,Fe,Mo,andO multipledomain-specializedagentsforamulti-stepmaterialssciencetask,
withinthespecifiedspacegroupP4/mmm.Thishighlightstheagent’sability wedesignedatwo-stageexperimentinvolvingcrystalstructuregeneration
toaddresscomplexandarbitrarymaterialcompositions. followedbyMDsimulationasshowninFig.12.Thefirststageinvolveda
userpromptrequestingaCIFfortheintermetalliccompoundNiAlinthe
Moleculardynamics∣Case1:MDsimulationofaluminumat cubicPm-3mspacegroup.MatSciAgent,correctlydelegatedthetaskto
constantenergy theCrystalGenerationAgent,whichisresponsibleforgenerating
Inthiscase,themoleculardynamicsagentperformsanMDsimulationof crystalstructures.ThisagentinvokedtheCrystaLLMtoolwiththespe-
aluminum(Al).Itinterpretsthenaturallanguagequerytoextractsimula- cified parameters (composition=‘NiAl’, space group=‘Pm-3m’) and
1 1
tionconditions,identifyingaconstantenergy(NVE)ensemblewithatarget successfullyproducedthecorrespondingCIFfile.
temperatureof660°C,whichitcorrectlyconvertsto933.15K,asillustrated Inthesecondstage,afollow-uppromptrequestedanMDsimulationof
inFig.11. the generated AlNi structure under NVT conditions, using the EMT
The system is initialized using a face-centered cubic (FCC) crystal potentialandaLangevinthermostatsettoaninitialtemperatureof550Kfor
structure with a lattice constant of 4.05Å. Interatomic interactions are 100,000steps.ThecorrespondingMDtrajectorycanbefoundinSupple-
modeledusingtheEffectiveMediumTheory(EMT)potential,asspecified mentaryData2.ThesystemagainselectedtheappropriateagentMole-
inthequery.Thesimulationrunsfor100,000steps(Fig.11b).Theresults cularDynamicsAgentwhichusedtheMDSimulationNVTToolto
show that the system’s total energy remains constant throughout the carryoutthesimulation,automaticallyextractingrelevantparametersfrom
simulation,consistentwiththeexpectedbehaviorofanNVEensemble.The thepreviouslygeneratedCIFfile.
temperaturefluctuatesaroundthetargetvalue,withkineticandpotential This experiment illustrates the system’s ability to preserve context
energy components varying over time. During the simulation, the across agent transitions and demonstrates seamless operation between
CommunicationsMaterials| ( 2026) 7:131 6

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.6|CellularAutomatasimulationofdiffusion-controlledgrowth.aUserqueryspecifyingthesimulationtask.bAgent-generatedoutput,includingframe-by-frame
microstructureevolution.
Fig.7|Cellularautomatasimulationofinterface-controlledgrowth.aUserqueryspecifyingthesimulationtask.bAgent-generatedoutput,includingframe-by-frame
microstructureevolution.
CommunicationsMaterials| ( 2026) 7:131 7

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.8|MonteCarloAnnealingsimulationofpolycrystallinegraingrowth.aUserqueryspecifyingthesimulationtask.bAgent-generatedoutput,includingframe-by-
framemicrostructureevolution.
Fig.9|CrystallographicgenerationforNiAl.aUserqueryspecifyingthechemicalcompositionandspacegroup.bAgent-generatedCIFfiledescriptionand
3
correspondingvisualizationofthecrystalstructure.
CommunicationsMaterials| ( 2026) 7:131 8

| https://doi.org/10.1038/s43246-025-00994-x |     |     |     |     |     |     |     |     | Article |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
Fig.10|CrystallographicgenerationforSrFeMoO.aUserqueryspecifyingthechemicalcompositionandapplication.bAgent-generatedCIFfiledescriptionand
2 6
correspondingvisualizationofthecrystalstructure.
| Table1|CommonmaterialsIDsacrossruns |             |             |         | bothruns.                                      |     |         |         |                    |     |
| ----------------------------------- | ----------- | ----------- | ------- | ---------------------------------------------- | --- | ------- | ------- | ------------------ | --- |
| 0 1                                 | 2 3 4       | 5 6 7       | 8 9     |                                                |     |         |         |                    |     |
|                                     |             |             |         |                                                |     |         | jA \Aj  |                    |     |
|                                     |             |             |         |                                                |     |         | ¼ i j   |                    |     |
| 0 1.0 1.0                           | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 |                                                |     | IoU i;j |         |                    |     |
|                                     |             |             |         |                                                |     |         | jA ∪A j |                    |     |
| 1 1.0 1.0                           | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 |                                                |     |         | i j     |                    |     |
| 2 1.0 1.0                           | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 |                                                |     |         |         |                    |     |
|                                     |             |             |         | whereA isthesetofmaterialIDsreturnedinruni,A   |     |         |         | isthesetofmaterial |     |
| 3 1.0 1.0                           | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 | i                                              |     |         |         | j                  |     |
|                                     |             |             |         | IDsretur nedinrunj,A∩Adenotestheintersection(i |     |         |         | .e.,commonmaterial |     |
i j
4 1.0 1.0 1.0 1.0 1.0 0.0 1.0 1.0 1.0 1.0 IDs)betweenrunsiandjandA ∪A denotestheunion(i.e.,totalunique
i j
5 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 materialIDs)acrossrunsiandj.
6 1.0 1.0 1.0 1.0 1.0 0.0 1.0 1.0 1.0 1.0 TheIntersectionoverUnion(IoU)matrixofmaterialIDsetsacross
runsisshowninTable1.AnIoUof1.0indicatesperfectoverlap.Asseenin
| 7 1.0 1.0 | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 |     |     |     |     |     |     |
| --------- | ----------- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
thematrix,allrunsexceptrun5showperfectagreement(IoU=1.0),while
| 8 1.0 1.0 | 1.0 1.0 1.0 | 0.0 1.0 1.0 | 1.0 1.0 |     |     |     |     |     |     |
| --------- | ----------- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
run5showszerooverlap(IoU=0.0)withallothers.
9 1.0 1.0 1.0 1.0 1.0 0.0 1.0 1.0 1.0 1.0 Minimum,maximum,andaveragebondlengthsperrunarelistedin
Fig.13.Bondlengthvaluesareconsistentlydistributedacrossallsuccess-
IoUMatrixofMaterialIDsBetweenRuns.
fulruns.
Thestandarddeviationsforminimum,maximumandaveragebond
σ =0.05025Å,
independentlyfunctioningagents.Italsohighlightsthepotentialofusing lengths across all runs (excluding run 5) are
min
thisagentframeworktohandlemultipletaskseffectively. σ =0.06833Åandσ =0.05890Å.Theselowvaluesconfirmthatbond
|     |     |     |     | max               |           | avg    |              |                  |          |
| --- | --- | --- | --- | ----------------- | --------- | ------ | ------------ | ---------------- | -------- |
|     |     |     |     | length extraction | is highly | stable | across runs. | Every successful | run con- |
Reliabilityanalysis∣Materialsextraction sistentlyidentifiedthesamecoordinationpatterns:O2−–Ti4+andTi4+–O2−.
ToevaluatetheconsistencyoftheLLMagent,weperformed10independent Toassessconsistencyinresponsesgeneratedformaterialssynthesis
runsofthesameprompt.Allrunsselected:MaterialExtractionAgentand queries10promptexecutionsareanalyzed.Eachresponsewasloggedand
tools: get_material_ids and MaterialsProjectBonds. Among the 10 runs, reviewed to evaluate agent/toolselection, compounds of focus,synthesis
runs0–4and6–9yieldedidenticalsetsof47materialIDs.Run5failedto
|     |     |     |     | method association, | output | formatting, | and level | of detail. | For all 10 |
| --- | --- | --- | --- | ------------------- | ------ | ----------- | --------- | ---------- | ---------- |
extractanymaterialIDs,suggestinganisolatederror.Theconsistencyinthe responses MatSciAgent delegated the task to MaterialEx-
other nine runs demonstrates the stability and reproducibility of the tractionAgent and MPSynthesisTool which is specialized for
materialextractioncomponentoftheagent. extractingsynthesis-relatedinformation.Thisdemonstratedperfectcon-
To gauge the similarity between the different materials ids that the sistencyinagentandtoolselectionrationale.Themostfrequentlyextracted
agentwasreturningwedecidedtocalculatetheIntersectionoverUnion materials across runs are listed below, along with their frequencies and
(IoU)matrixbetweenalltheruns.Thisisbasicallythenumberofcommon synthesismethodsinTable2.Thebasiccontentsoftheresponseandtheir
materialidsreturnedintherunsdividedbythecombinedmaterialidsacross correspondingformatscanbefoundinTable3.
| CommunicationsMaterials|  (        2026) 7:131  |     |     |     |     |     |     |     |     | 9   |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| https://doi.org/10.1038/s43246-025-00994-x |     |     |     |     |     | Article |
| ------------------------------------------ | --- | --- | --- | --- | --- | ------- |
Fig.11|MDsimulationofaluminum.aUserqueryspecifyingthesimulationconditions,includingensembletypeandtemperature.bAgent-generatedoutputshowinga
summaryofthesimulationsetupandtheresultingMDtrajectory.
Table2|FrequencyofExtractedCompoundsAcross10Runs 3. PolycrystallineAluminumGrainGrowth(MonteCarloAnnealing)
| Compound | Runs Frequency | Run Synthesis |     |     |     |     |
| -------- | -------------- | ------------- | --- | --- | --- | --- |
Theagentselectionandtoolinvocationwerefullydeterministicacross
|     | Found | Indices Method |     |     |     |     |
| --- | ----- | -------------- | --- | --- | --- | --- |
allruns.
| BiCuVOx | 6 60% | 0,1,3,6, Sol-Gel |                          |     |                  |             |
| ------- | ----- | ---------------- | ------------------------ | --- | ---------------- | ----------- |
|         |       |                  | ContinuumSimulationAgent |     | was consistently | selected by |
7,8
MatSciAgentacrossallpromptsandallruns.FortheAl-Cu-MgandTi-
Cu2Zn(Sn)Se4 4 40% 2,4,5,9 Solid-State Alsolidificationprompts,theagentinvokedtheCASolidTool(Cel-
La0.8Sr0.2CoxFe1-xO3 3 30% 4,5,9 Solid-State lularAutomataPhaseTransform), suitable for cellular automata-
La0.6Sr0.4M0.2Fe0.8O3-δ 5 50% 1,3,6, Sol-Gel basedsimulations.Forthepolycrystallinealuminumgraingrowthprompt,
|     |     | 7,8 | the agent invoked | the MCAnnealingTool | (BiasedPottsMonte- |     |
| --- | --- | --- | ----------------- | ------------------- | ------------------ | --- |
SrFeO 4 40% 0,1,6,7 Solid-State CarloAnnealing), which is designed for Monte Carlo annealing
3-δ
simulationsofgraingrowth.
| (KNa x 1-x )NbO 3 | 6 60% | 0,1,3,6, Sol-Gel |     |     |     |     |
| ----------------- | ----- | ---------------- | --- | --- | --- | --- |
7,8 Acrossallruns,keysimulationparametersincludinggriddimensions,
attachmentprobability,andnumberofnucleiorphaseswereconsistently
| BaZr0.1Ce0.7Y0.2O3 | 6 60% | 0,1,3,6, Solid-State |     |     |     |     |
| ------------------ | ----- | -------------------- | --- | --- | --- | --- |
interpretedandasshowninTable4.Nodiscrepancieswereobservedinthe
7,8
AlxZn1-xO 2 20% 0,6 Sol-Gel parsed values. Additionally, the agent reliably mapped each simulation
prompttothecorrectmodelingtechnique(CellularAutomataorMonte
Thistabledisplaysanalysisofthecompoundsandtheirmethodsreturnedduringconsistency
CarloAnnealing),regardlessofrunindex.
analysis.
Reliabilityanalysis∣MDsimulation
Reliabilityanalysis∣Continuumsimulation Toevaluatetherobustnessandreproducibilityofouragentframework,we
We tested reproducibility for three continuum simulation prompts by performeda consistency analysis by executing the same MD simulation
executingeachpromptfivetimes.Thesimulationswere: prompttentimes.Thisanalysisassessestheagent’sabilitytoconsistently
Al-Cu-MgAlloySolidification(CellularAutomata)
1. selectthecorrectagent,extractparameters,invoketools,andexecutethe
Ti-AlIntermetallicAlloySolidification(CellularAutomata)
2. simulation, as illustrated in Table 5. All 10 runs correctly selected the
| CommunicationsMaterials|  (        2026) 7:131  |     |     |     |     |     | 10  |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- |

https://doi.org/10.1038/s43246-025-00994-x Article
Fig.12|Coordinatingmultipleagentsforjointtask.AftergeneratingtheCIFfilethemasteragentsuccessfullydeployedMolecularDynamicsAgenttousetheciffile
generatedpreviouslytoruntheMDsimulation.
MolecularDynamicsAgent as the appropriate sub-agent to handle parametersandsearch keywordsfromnaturallanguage inputwithhigh
thesimulationtask.Ineveryrun,theagentsuccessfullyextractedall8key accuracy.
simulationparametersandinvokedtheMDSimulationNVEToolwith The reliability analysis demonstrates that the framework maintains
anidenticaldictionary: consistentagentandtoolselection,parameterextraction,andsimulation
executionacrossrepeatedruns.Withnear-perfectreproducibilityinmost
tasksandonlyminor,non-impactingvariationsinformattingorisolated
extraction failures, the system shows the stability required for materials
research.
Akeystrengthoftheframeworkisitsmodulardesign,whichallowsit
to expand as new tools are added. Broadening data sources beyond the
Materials Project and MatWeb would further enhance its applicability.
Simulationcapabilitiescouldbeimprovedthroughadvancedworkflows,
multiscalemodeling,andML-guidedoptimization.Moreover,enablingthe
agent to dynamically write or adapt code would increase its flexibility,
makingitbettersuitedforunseenorspecializedtasks.
Eachrunexecutedfor10,000stepswithenergyconservationmain-
tainedacrossthesimulation.Minorvariationinphysicaloutputs,suchas Methods
energyandfinaltemperature,wereobservedasexpectedwheretheinitial Languagemodel
totalenergyrangedfrom3.63eVto4.29eVandfinaltemperaturesranged We utilize OpenAI’s ChatGPT API, specifically the gpt-3.5-turbo
from~130K−180K. modelconfiguredwithtemperaturevalueof0,tosupportnaturallanguage
The results highlight the high reliability and reproducibility of the understanding and generation within the MatSciAgent framework. This
agentframeworkwhentaskedwithmoleculardynamicssimulations.The configurationwasapplieduniformlyacrossallagenttypes(Master,Material
agentconsistentlyselectedthecorrecttools,interpretedparameterswithout Extraction, Continuum Simulation, Crystal Generation, and Molecular
error, and completed valid simulations under NVE conditions. The Dynamics)toensureconsistentqueryroutingandtoolexecution.GPT-3.5-
observedvariabilityinthermodynamicoutputsisphysicallyexpecteddueto turboispartoftheGenerativePretrainedTransformer(GPT)series43,which
stochasticeffectsinherenttoMD.Minorvariationsinthepresentationstyle is based on the transformer architecture and leverages self-attention
do not affect the scientific correctness or repeatability of the simulation mechanisms44 to model complex language patterns and dependencies.
process. While GPT-3.5-turbo is used in our current implementation due to its
favorablebalancebetweenperformanceandcost,themodulardesignofour
Conclusion framework allows for easy substitution with more advanced models,
The integration of LLMs with simulation tools demonstrates their dependingontaskrequirementsorresourceavailability.
growingutilityincomputationalmaterialsscience.Thispapershowcases To manage the interactions between the language model and the
their effectiveness in structure retrieval and generation, as well as in systemmodules,weusetheLangChainframework45.LangChainprovides
runningcontinuumandMDsimulations.Thecasestudieshighlightthe tools for prompt management, output parsing, and tool integration,
flexibilityofLLMsinautomatingworkflowsthatincorporatebothcustom enabling structured communication and orchestration between the lan-
code and established software. The agent consistently extracts relevant guagemodelandexternalAPIsorcomputationalcomponents.Asofthis
CommunicationsMaterials| ( 2026) 7:131 11

| https://doi.org/10.1038/s43246-025-00994-x |     |     |     |     |     | Article |
| ------------------------------------------ | --- | --- | --- | --- | --- | ------- |
Fig.13|Spreadofbondlengthsacross9runs.Box
plotofminimum,maximum,andaverageatomic
distancesacross9successfulsimulationruns.The
narrowdeviationbetweentherunsdemonstrates
thattheagentconsistentlyproducesstableand
reproducibleoutputs.
Table3|SynthesisOutputCharacteristicsAcrossAgentRuns
Run FormatType Structure ReactionEq. Temp. Duration Atmosphere
| 0   | BulletPoints | Nested     | ✓   | ✓   | ✓   |     |
| --- | ------------ | ---------- | --- | --- | --- | --- |
| 1   | Paragraph    | Continuous | ✓   | ✓   | ✓   | ✓   |
| 2   | BulletPoints | Nested     | ✓   | ✓   | ✓   | ✓   |
| 3   | BulletPoints | Nested     | ✓   | ✓   | ✓   |     |
|     |              |            | ✓   | ✓   | ✓   | ✓   |
| 4   | Paragraph    | Structured |     |     |     |     |
| 5   | Paragraph    | Continuous | ✓   | ✓   | ✓   | ✓   |
| 6   | Paragraph    | Continuous | ✓   | ✓   | ✓   | ✓   |
| 7   | Paragraph    | Continuous | ✓   | ✓   | ✓   |     |
| 8   | BulletPoints | Flat       | ✓   | ✓   | ✓   |     |
|     |              |            | ✓   | ✓   | ✓   | ✓   |
| 9   | Paragraph    | Structured |     |     |     |     |
Thistableshowstheresponseformatthatthebroadsynthesisdetailsincludedineachoutputduringreliabilityanalysis.
Table4|Consistencyofagentandtoolselection
SolidificationAl-Cu-MgAlloy SolidificationTi-AlIntermetallicAlloy
GrainGrowthviaMonteCarloAnnealing
Agent:ContinuumSimulationAgent Agent:ContinuumSimulationAgent Agent:ContinuumSimulationAgent
| Tool:CASolidTool |     | Tool:MCAnnealingTool |     | Tool:CASolidTool |     |     |
| ---------------- | --- | -------------------- | --- | ---------------- | --- | --- |
Parameters:{"width":100,"attach_prob": Parameters:{"Q":20,"L":50,"MC_steps": Parameters:{"width":150,"attach_prob":
0.2,"num_solid_states":3, 100,"biasing_strategy":3} 0.9,"num_solid_states":2,
| "num_nuclei":5} |     |     |     | "num_nuclei":50} |     |     |
| --------------- | --- | --- | --- | ---------------- | --- | --- |
Thistableshowstherepetitionstabilityoftheagentacrossthreecontinuumsimulationtasks(5runseach)
writing, the API cost forgpt-3.5-turbo is $0.0015 per1,000input states, elastic tensors, bulk and shear moduli, Poisson’s ratio, dielectric
tokens and $0.002 per 1,000 output tokens (https://openai.com/pricing), constants,magneticproperties,phonondispersion(forselectedmaterials),
makingitapracticalchoiceforiterative,multi-turninteractionsinmaterials andsurfaceenergies.Thedatasetiscontinuouslyupdated,anduserscan
scienceworkflows.
accessitprogrammaticallyviaawell-documentedAPI,commonlythrough
toolslikepymatgen.
Materialsdatabase MatWebisanonlinedatabasethatfocusesonexperimentallymea-
The Materials Project is an open-access database designed to support sured or manufacturer-provided material properties4. It features over
computationalmaterialsscienceresearch3.Itcontainsover170,000material 180,000materialdatasheets,coveringawidevarietyofmaterialssuchas
entries,allgeneratedusingfirst-principlesdensityfunctionaltheory(DFT)
metals,alloys,polymers,ceramics,composites,andglasses.MatWebpro-
calculations.Thedatabaseoffersacomprehensivesetofmaterialproperties, videsdetailedinformationonmechanicalproperties(e.g.,tensilestrength,
includingcrystalstructures,formationenergies,bandstructures,densityof yield strength, hardness), thermal properties (e.g., thermal conductivity,
CommunicationsMaterials|  (        2026) 7:131  12

https://doi.org/10.1038/s43246-025-00994-x Article
Table5|ReliabilityanalysisforMoleculardynamicsagent probabilistic growth behavior. The num_solid_states parameter
determineshowmanydistinctsolidphasescanexistinthesystem.Whenset
Metric Consistency Notes to1,themodelsimulatesbasicsolidificationwithasinglegrowingphase;
AgentSelection 100% Alwaysselected when>1,itenablesmorecomplexrecrystallizationscenarios,wheremul-
MolecularDynamicsAgent
tiplephasesgrowandcompeteforspace.
Parameter 100% All8keyparametersextractedcorrectly Nucleationisintroducedthroughtheplace_nuclei(num_nu-
Extraction clei)function,whichrandomlyplacesaspecifiednumberofinitialsolid
ToolInvocation 100% IdenticalcallstoMDSimulationNVETool cellsthroughoutthegrid.Eachnucleusisassignedarandomsolidphase.
Simulation 100% Allcompleted10,000steps The system then evolves over a series of discrete time steps using the
Execution evolve(Nsteps)function,whichupdateseachcellbasedonthestates
OutputFormat 80% Minorvariationsinstyle(bulletvs ofitsneighbors.
paragraph) The output of the simulation includes visual snapshots of the
Content 100% Allessentialinformationwasincluded evolving microstructure at each time step,as well as a plot showing the
Accuracy fractionofthetransformedareaovertime.Thistransformationcurvecanbe
QuantitativeConsistencyMetricsAcross10Runsformoleculardynamicsreliabilityanalysis. comparedtoanalyticalpredictionsbasedontheJohnson-Mehl-Avrami-
Kolmogorov(JMAK)theory49,providingameansofvalidatingthemodel’s
behavior.
expansioncoefficients),electrical properties, chemical compositions, and MonteCarloannealing
physicalconstantslikedensityandspecificheat. MonteCarloAnnealingisusedtosimulategraingrowthorspinorderingin
atwo-dimensionalPottsmodelatverylowtemperatures(T≈0),wherethe
Materialsextractionagent systemdynamicsaregovernedprimarilybyenergyminimization50.This
LLMs, while powerful, are typically trained on general-purpose natural correspondstozero-temperatureMetropolisdynamics,inwhichspinflips
languagedatasetsandlackaccesstothespecialized,structureddatarequired areonlyacceptediftheylowerormaintainthesystem’senergy.Eachsiteon
formaterialsscienceapplications46,47.Becausetheyrelyonstatic,pre-trained the2DlatticecanexistinoneofQpossiblestates,andthesystemevolvesby
knowledge,theycannotdynamicallyqueryauthoritativedatabases,often locallyminimizinginterfacialenergybetweendifferentstates.
resulting in outdated or incomplete information. Furthermore, their Themodelischaracterizedbyseveralkeyparameters.ThevariableQ
probabilisticnaturecanleadtoovergeneralizationormisinterpretationof definesthenumberofpossiblestatesor“flavors”perlatticesite,whichcan
complexscientificqueries48. represent, for example, distinct grain orientations in a polycrystalline
To overcome these limitations, we introduce a materials extraction material.TheparameterLsetsthesizeofthesquarelattice,resultingina
agentthatintegratestheMaterialsProjectAPIandcustomweb-scrapingfor totalofL×Lsites.ThesimulationproceedsforagivennumberofMonte
MatWeb, enabling real-time access to validated, domain-specific data. Carlosteps,witheachstepconsistingofL2spin-flipattempts.Thebiasing
Upon receiving a user query, the agent retrieves relevant material strategydetermineshowboththesiteandthetrialstateareselectedduring
properties–such as thermal, dielectric, and surface characteristics–by simulation. Strategies include selecting a random new state from all Q
invokingtheappropriatedatabasecall,eitherviaAPIorwebscraping.It options, choosing from neighboring states at any site, or restricting to
thensynthesizesanaturallanguageresponsebasedontheretrieveddata. neighboring states only at interfacial sites (i.e., those bordering unlike
Thismethodensuresthatresponsesaregroundedincurrent,authoritative neighbors).
sources, allowing for more accurate contextualization of materials, ver- This simulation produces several outputs that help analyze the
ification of properties under specific conditions, and delivery of reliable, system’s behavior. The energy history tracks how the total energy of
data-driven insights critical for real-world applications. Importantly, by the lattice evolves over time, typically decreasing as the system anneals.
relying on scientifically validated sources, the system also enhances the The acceptance history records the number of accepted spin flips per
reproducibilityofoutputpromptgeneration. Monte Carlo step, providing insight into how active or “frozen” the
The agent retrieves data from structured databases, including the system becomes during the simulation. The configuration history
MaterialsProject3andMatWeb4.TheMaterialsProjectoffersaccesstoover stores snapshots of the lattice at each step, allowing visualization of
150,000materialswithpropertiessuchaselasticity,phononspectra,and the evolving microstructure and phase ordering. If plotting is enabled,
thermodynamicstability–essentialforpredictivemodeling.MatWebcom- thesimulationalsogeneratesvisualizationsoftheenergycurve,acceptance
plementsthiswithexperimentallyvalidatedmaterialdata,enablingdirect rate, and both initial and final configurations. Additionally, it can save
comparisonsbetweencomputationalpredictionsandempiricalbehavior. all configuration snapshots as images in a results directory for further
FurtherimplementationdetailsareprovidedintheMethodssection. analysis.
Cellularautomata Continuumsimulationagent
In this work, the Cellular Automata model is used to simulate phase The continuum simulation agent executes advanced materials science
transformations such as solidification or recrystallization within a two- simulations,integratingtwokeymodelingtechniques:CellularAutomata
dimensional,grid-basedsystem.Eachcellinthegridrepresentsapointin (CA)51,52forphasetransformationsandMonteCarloAnnealing(MCA)50,53
spaceandcanexisteitherintheliquidphase,denotedby0,orinoneof formicrostructuralevolutionduringannealing.Usersprovidesimulation
severalsolidphases,representedbypositiveintegers.Thetransformation conditionsinnaturallanguage,whichtheagenttranslatesintoactionable
processisdrivenbylocalinteractionsbetweenneighboringcellsandgov- parametersbeforeexecutingthesimulation.
ernedbyanattachmentprobability,allowingthemodeltoeffectivelycap- TheCAtoolmodelsphasetransformationssuchassolidificationand
turetheevolutionofmicrostructuresduringphasechanges. recrystallization by iteratively updating a 2D grid based on local neigh-
Themodelisdefinedbyseveralkeyparameters.Thewidthspecifies borhood conditions. It accounts for attachment probabilities and tracks
thesizeofthesquaresimulationgrid,andthesimulationisrestrictedtothe transformed regions over time, offering insights into grain growth and
interior cells to avoid boundary effects. The attach_prob parameter nucleationinbothsingle-phaseandmultiphasesystems.
controlsthelikelihoodthataliquidcellwilltransformintoasolidphase MCAtool,usingthePottsmodel54,simulatestheevolutionofthegrain
basedonitsneighbors.Whenthisvalueissetto1,thetransformationis structureunderannealingconditions.Operatingnearzerotemperature,it
deterministic, while lower values introduce randomness, resulting in employs three biasing strategies: unbiased selection, neighboring flavor
CommunicationsMaterials| ( 2026) 7:131 13

https://doi.org/10.1038/s43246-025-00994-x Article
selection, and interface bias selection to model interface and bulk site Berendsen thermostat for temperature regulation and the Berendsen
behaviors. This method enables a detailed analysis of grain boundary barostatforpressureregulationinNPTsimulations.
dynamics and energy minimization during thermal processing, offering Keysimulationparametersincludethetimestepfornumericalinte-
predictiveinsightsintomicrostructuralstability. gration,targettemperature,andthetotalnumberofMDsteps.Forensemble
Understandingphasetransformationsandmicrostructuralevolution control,thethermostatandbarostattimeconstantswerespecified,along
isessentialfortailoringmaterialpropertiesinmanufacturingandproces- withexternalpressureandbarostatcouplingstrengthforNPTconditions.
sing.ByintegratingCAandMCAwithinanLLMframework,itenhances Additionally,aloggingintervalwasdefinedtorecordsystempropertiesand
traditional modeling tools with natural language interaction, parameter trajectoriesatregulartimesteps.Simulationoutputsconsistofatomictra-
customization, and visualization. It delivers actionable insights through jectoriessavedin.trajformat,logfilesdetailingtheevolutionofenergy,
simulationresults. temperature, and stress, and corresponding visualizations of energy and
temperatureprofilesovertime.
CrystaLLM
CrystaLLMisadomain-specificLLMdesignedtogeneratecrystallographic Moleculardynamicsagent
structuresinCIFformatfrombasiccompositionalinput.BuiltontheGPT-2 Atomic-scale simulations are essential for understanding fundamental
architecture and adapted using the nanoGPT implementation55,56, Crys- materialbehaviors,suchasthermalconductivity,mechanicalstrength,and
taLLMhasbeenpurposefullytrainedforapplicationsininorganicmaterials phasetransitions58,59.TheMDsimulationagentisdesignedtoautomateand
science. Rather than relying on general-purpose vocabularies, it uses a streamlineatomic-scalesimulations.Itinterpretsuserinputqueries,setsup
custombyte-leveltokenizerwithavocabularyof371tokenstailoredtothe theappropriatesimulationparameters,andexecutestheMDsimulation
syntacticpatternsofCIFfiles. accordingly. Specifically, the agent initializes atomic structures, defines
The training dataset for CrystaLLM was assembled from multiple interatomicpotentials,andrunssimulationsusingtoolsprimarilybasedon
high-qualitymaterialssciencedatabases,includingtheMaterialsProject3, theAtomicSimulationEnvironment(ASE)package60.
theOpenQuantumMaterialsDatabase5,andtheNOMAD57.Thesesources Itsupportstheconstructionofatomicstructureswithvariouscrystal
provideadiverserangeofinorganiccrystalstructures,enablingthemodelto symmetriesandaccommodatesarangeofinteratomicpotentials,including
learndetailedpatternsrelatedtoatomicarrangements,symmetryopera- theEmbeddedAtomMethod(EAM)61,Lennard-Jones(LJ)62,andEffective
tions,andlatticeparametersacrossawidevarietyofcrystalsystems. MediumTheory(EMT)63.Theseenablesimulationsofmetals,alloys,and
WeemploythesmallvariantofCrystaLLM,withtemperaturesetto simplemolecularsystems.Theagentcanalsoperformsimulationsunder
0.8;top-ksamplingwithk=10;randomseedfixedat1337forreproduci- differentthermodynamicensembles–NVE(constantenergy),NVT(con-
bility; executed with bfloat16 in our study. This version consists of 8 stanttemperature),andNPT(constantpressure)–allowinguserstoexplore
transformerlayers,eachwith8attentionheadsandacontextwindowof materialbehaviorundercontrolledconditions.Furtherdetailsareprovided
1,024 tokens. The model has an embedding dimension of 512 and was in the Methods section. By translating natural language input into
trainedfromscratchfor5,000iterations. simulation-ready parameters, the agent simplifies the MD simulation
workflow.
Crystalstructuregenerationagent IntegratingtheMDsimulationtoolswithanLLMagentsignificantly
Atomicstructureisfundamentaltounderstandinginorganiccrystalmate- enhancesitscapabilities.Userscaninteractivelyconfiguresimulations,ana-
rialsandperformingcomputationalsimulations.Whenstructuraldatais lyzeresults,andvisualizeatomictrajectoriesusingnaturallanguagequeries.
availableinexistingdatasets,itcanbedirectlyretrieved.However,ifsuch Unlike traditional standalone MD tools, this agent automates the entire
data is missing, alternative methods are needed to generate the desired workflow–from structure initialization to result interpretation–providing
atomicstructures. actionableoutputssuchasenergyplotsandtrajectorydatawithminimal
Thecrystalgeneratoragentaddressesthisbygeneratingcrystalstructures manualeffort.
based on elemental compositions or alloy systems using CrystaLLM,
a transformer-based language model specifically designed to produce Ethicsandinclusion
CIFs (Crystallographic Information Files) of inorganic crystals8. Upon Thisstudyusesonlypubliclyavailabledataandadherestoethicalresearch
receiving a user query, the agent extracts relevant information and runs standards.Codeandmethodologywillbesharedtopromotetransparency,
CrystaLLMtogenerateplausibleinorganiccrystalstructures.Itcanproduce reproducibility,andcollaboration.
multiple candidate structures for a given composition, enabling material
exploration. Technologyusedisclosure
Unlike general-purpose LLMs, CrystaLLM is tailored to recognize ChatGPT was utilized for grammar and spelling corrections during
complex crystallographic patterns, enabling the generation of physically manuscriptpreparation.Allauthorshavereviewedandverifiedtheaccu-
realisticstructures.Aspartofamulti-agentsystem,thecrystalgenerator racyofthefinalcontent.
agentstreamlinesmaterialsworkflowsbyprovidingimmediateinputfor
downstreamtaskssuchasthermodynamicstabilityanalysis,propertypre- Dataavailability
diction,andMDsimulations. WhileCrystaLLM is presentedhere as an Thecasestudyresultsandreliabilitystudyresultsareprovidedassupple-
examplegenerativemodelforcrystalstructuregenerationbasedoncom- mentarydata.
positionandspacegroupinformationnotethattheframeworkismodular
andcanaccommodateadditionalgenerativemodels,includingthosecap- Codeavailability
ableofproperty-constrainedgeneration,allowingfutureextensionstoward Thenecessarycodeusedinthisstudycanbeaccessedathttps://github.com/
inversematerialsdesignaswell. cakshat/MatSci-LLM-Agents.
Moleculardynamicssimulation Received:5May2025;Accepted:14October2025;
MD simulations were conducted using the Atomic Simulation Environ-
ment(ASE)toinvestigatethestructuralevolutionofatomicsystemsunder
various thermodynamic conditions. The agentic framework enables the References
executionofMDsimulationsinNVE(constantenergy),NVT(constant 1. Pollice,R.etal.Data-drivenstrategiesforacceleratedmaterials
Number,Volume,Temperature),andNPT(constantNumber,Pressure, design.Acc.Chem.Res.54,849–860(2021).
Temperature)ensembles.Thermodynamiccontrolwasachievedusingthe
CommunicationsMaterials| ( 2026) 7:131 14

https://doi.org/10.1038/s43246-025-00994-x Article
2. Kalidindi,S.R.&DeGraef,M.Materialsdatascience:current 26. Chaudhari,A.,Guntuboina,C.,Huang,H.&Farimani,A.B.Alloybert:
statusandfutureoutlook.Annu.Rev.Mater.Res.45,171–193 Alloypropertypredictionwithlargelanguagemodels.Comput.Mater.
(2015). Sci.244,113256(2024).
3. Jain,A.etal.Thematerialsproject:amaterialsgenomeapproachto 27. Yeh,Y.-T.,Ock,J.&Farimani,A.B.Texttobandgap:Pre-trained
acceleratingmaterialsinnovation.APLMater.1,011002(2013). languagemodelsasencodersforsemiconductorbandgap
4. LLC,M.Matweb:OnlineMaterialsInformationResource.http://www. prediction.arXivhttps://arxiv.org/abs/2501.03456(2025).
matweb.com(2020). 28. Pak,P.&Farimani,A.B.Additivellm:Largelanguagemodelspredict
5. Kirklin,S.etal.Theopenquantummaterialsdatabase(oqmd): defectsinadditivemanufacturing.arXivhttps://arxiv.org/abs/2501.
assessingtheaccuracyofDFTformationenergies.npjComput. 17784(2025).
Mater.1,1–15(2015). 29. Lu,C.etal.Theaiscientist:Towardsfullyautomatedopen-ended
6. Hellenbrandt,M.Theinorganiccrystalstructuredatabase(ICSD)- scientificdiscovery.arXivhttps://arxiv.org/abs/2408.06292(2024).
presentandfuture.Crystallogr.Rev.10,17–22(2004). 30. Ock,J.,Vinchurkar,T.,Jadhav,Y.&Farimani,A.B.Adsorb-agent:
7. Tanaka,I.,Rajan,K.&Wolverton,C.Data-centricscienceformaterials Autonomousidentificationofstableadsorptionconfigurationsvialarge
innovation.MRSBull.43,659–663(2018). languagemodelagent.arXivhttps://arxiv.org/abs/2410.16658(2024).
8. Antunes,L.M.,Butler,K.T.&Grau-Crespo,R.Crystalstructure 31. Boiko,D.A.,MacKnight,R.,Kline,B.&Gomes,G.Autonomous
generationwithautoregressivelargelanguagemodeling.Nat. chemicalresearchwithlargelanguagemodels.Nature624,570–578
Commun.15,10570(2024). (2023).
9. Xie,T.,Fu,X.,Ganea,O.-E.,Barzilay,R.&Jaakkola,T.Crystal 32. Bran,A.M.etal.Augmentinglargelanguagemodelswithchemistry
diffusionvariationalautoencoderforperiodicmaterialgeneration. tools.Nat.Mach.Intell.6,525–535(2024).
arXivhttps://arxiv.org/abs/2110.06197(2022). 33. Jadhav,Y.,Pak,P.&Farimani,A.B.LLM-3Dprint:Largelanguage
10. Zeni,C.etal.Agenerativemodelforinorganicmaterialsdesign. modelstomonitorandcontrol3dprinting.arXivhttps://arxiv.org/abs/
Nature639,624–632(2025). 2408.14307(2024).
11. Himanen,L.,Geurts,A.,Foster,A.S.&Rinke,P.Data-drivenmaterials 34. Jadhav,Y.&Farimani,A.B.Largelanguagemodelagentasa
science:status,challenges,andperspectives.Adv.Sci.6,1900808 mechanicaldesigner.arXivhttps://arxiv.org/abs/2404.17525(2024).
(2019). 35. Huang,L.etal.Asurveyonhallucinationinlargelanguagemodels:
12. Vaswani,A.etal.Attentionisallyouneed.InGuyon,I.etal.(eds.) Principles,taxonomy,challenges,andopenquestions.arXivhttps://
AdvancesinNeuralInformationProcessingSystems,vol.30(Curran doi.org/10.1145/3703155(2024).
Associates,Inc.,2017). 36. Perković,G.,Drobnjak,A.&Botički,I.Hallucinationsinllms:
13. Brown,T.etal.Languagemodelsarefew-shotlearners.Adv.neural Understandingandaddressingchallenges.In202447thMIPROICT
Inf.Process.Syst.33,1877–1901(2020). andElectronicsConvention(MIPRO)2084–2088(IEEE,2024).
14. Achiam,J.etal.Gpt-4TechnicalReport.https://cdn.openai.com/ 37. Liu,F.etal.ExploringandevaluatinghallucinationsinLLM-powered
papers/gpt-4.pdf(2023). codegeneration.arXivhttps://arxiv.org/abs/2404.00971(2024).
15. Touvron,H.etal.Llama:Openandefficientfoundationlanguage 38. Birhane,A.,Kasirzadeh,A.,Leslie,D.&Wachter,S.Scienceintheage
models.arXivhttps://arxiv.org/abs/2302.13971(2024). oflargelanguagemodels.Nat.Rev.Phys.5,277–280(2023).
16. Anthropic.Claude3.7Sonnet.https://www.anthropic.com(2025). 39. Johnson,S.&Hyland-Wood,D.Aprimeronlargelanguagemodels
17. Tshitoyan,V.etal.Unsupervisedwordembeddingscapturelatent andtheirlimitations.arXivhttps://arxiv.org/abs/2412.04503(2024).
knowledgefrommaterialsscienceliterature.Nature571,95–98 40. Chiang,Y.,Hsieh,E.,Chou,C.-H.&Riebesell,J.Llamp:Large
(2019). languagemodelmadepowerfulforhigh-fidelitymaterialsknowledge
18. Ock,J.,Guntuboina,C.&BaratiFarimani,A.Catalystenergy retrievalanddistillation.arXivhttps://arxiv.org/abs/2401.17244
predictionwithCatBERTA:unveilingfeatureexplorationstrategies (2024).
throughlargelanguagemodels.ACSCatal.13,16032–16044 41. Zhang,H.,Song,Y.,Hou,Z.,Miret,S.&Liu,B.Honeycomb:Aflexible
(2023). LLM-basedagentsystemformaterialsscience.arXivhttps://arxiv.
19. Ock,J.,Badrinarayanan,S.,Magar,R.,Antony,A.&BaratiFarimani, org/abs/2409.00135(2024).
A.Multimodallanguageandgraphlearningofadsorption 42. Ghafarollahi,A.&Buehler,M.J.Atomagents:Alloydesignand
configurationincatalysis.Nat.Mach.Intell.6,1501–1511(2024). discoverythroughphysics-awaremulti-modalmulti-agentartificial
20. Cao,Z.,Magar,R.,Wang,Y.&BaratiFarimani,A.Moformer:Self- intelligence.arXivhttps://arxiv.org/abs/2407.10022(2024).
supervisedtransformermodelformetal-organicframeworkproperty 43. Radford,A.&Narasimhan,K.ImprovingLanguageUnderstandingby
prediction.J.Am.Chem.Soc.145,2958–2967(2023). GenerativePre-training.https://api.semanticscholar.org/CorpusID:
21. Xu,C.,Wang,Y.&BaratiFarimani,A.Transpolymer:atransformer- 49313245(2018).
basedlanguagemodelforpolymerpropertypredictions.npjComput. 44. Vaswani,A.Attentionisallyouneed.In31stConferenceonNeural
Mater.9,64(2023). InformationProcessingSystems.(NIPS,2017).
22. Kim,S.,Mollaei,P.,Antony,A.,Magar,R.&BaratiFarimani,A.Gpcr- 45. Chase,H.Langchain.https://github.com/langchain-ai/langchain
bert:Interpretingsequentialdesignofgprotein-coupledreceptors (2022).
usingproteinlanguagemodels.J.Chem.Inf.Modeling64,1134–1144 46. Ling,C.etal.Domainspecializationasthekeytomakelargelanguage
(2024). modelsdisruptive:acomprehensivesurvey.arXivhttps://arxiv.org/
23. Mollaei,P.,Sadasivam,D.,Guntuboina,C.&BaratiFarimani,A. abs/2305.18703(2024).
Idp-bert:Predictingpropertiesofintrinsicallydisorderedproteins 47. Li,H.etal.Blade:Enhancingblack-boxlargelanguagemodelswith
usinglargelanguagemodels.J.Phys.Chem.B128,12030–12037 smalldomain-specificmodelsarXivhttps://arxiv.org/abs/2403.18365
(2024). (2024).
24. Badrinarayanan,S.,Guntuboina,C.,Mollaei,P.&BaratiFarimani,A. 48. Mittelstadt,B.,Wachter,S.&Russell,C.Toprotectscience,wemust
Multi-peptide:Multimodalityleveragedlanguage-graphlearningof useLLMsaszero-shottranslators.Nat.Hum.Behav.7,1830–1832
peptideproperties.J.Chem.Inf.Model.65,83–91(2025). (2023).
25. Meda,R.S.&Farimani,A.B.Bapulm:Bindingaffinitypredictionusing 49. Fanfoni,M.&Tomellini,M.TheJohnson-Mehl-Avrami-Khokhlov
languagemodels.arXivhttps://arxiv.org/abs/2411.04150(2024). model:abriefreview.IlNuovoCim.D.20,1171–1182(1998).
CommunicationsMaterials| ( 2026) 7:131 15

https://doi.org/10.1038/s43246-025-00994-x Article
50. Kinoshita,M.,Okamoto,Y.&Hirata,F.First-principledeterminationof wrotetheoriginaldraft.J.O.contributedtomethodology,validation,
peptideconformationsinsolvents:CombinationofMonteCarlo investigation,datacuration,andwritingandediting.A.B.F.supervisedthe
simulatedannealingandRISMtheory.J.Am.Chem.Soc.120, project,contributedtoconceptualization,projectadministration,funding
1855–1863(1998). acquisition,andwritingandediting.
51. Wolfram,S.Statisticalmechanicsofcellularautomata.Rev.Mod.
Phys.55,601(1983). Competinginterests
52. Wolfram,S.Cellularautomataasmodelsofcomplexity.Nature311, Theauthorsdeclarenocompetinginterests.
419–424(1984).
53. Metropolis,N.&Ulam,S.TheMonteCarlomethod.J.Am.Stat. Additionalinformation
Assoc.44,335–341(1949). SupplementaryinformationTheonlineversioncontains
54. Saito,Y.&Enomoto,M.MonteCarlosimulationofgraingrowth.ISIJ supplementarymaterialavailableat
Int.32,267–274(1992). https://doi.org/10.1038/s43246-025-00994-x.
55. Radford,A.etal.LanguageModelsareUnsupervisedMultitask
Learners.https://api.semanticscholar.org/CorpusID:160025533 Correspondenceandrequestsformaterialsshouldbeaddressedto
(2019). JanghoonOckorAmirBaratiFarimani.
56. Karpathy,A.NanoGPT.https://github.com/karpathy/nanoGPT
(2022). PeerreviewinformationCommunicationsMaterialsthanksFederico
57. Nomad:Adistributedweb-basedplatformformanagingmaterials Ottomanoandtheother,anonymous,reviewer(s)fortheircontributiontothe
scienceresearchdata.J.OpenSourceSoftw.8,5388(2023). peerreviewofthiswork.Apeerreviewfileisavailable.
58. Mavromaras,A.etal.Computationalmaterialsengineering:
capabilitiesofatomic-scalepredictionofmechanical,thermal,and Reprintsandpermissionsinformationisavailableat
electricalpropertiesofmicroelectronicmaterials.In201011th http://www.nature.com/reprints
InternationalThermal,Mechanical&Multi-PhysicsSimulation,and
ExperimentsinMicroelectronicsandMicrosystems(EuroSimE), Publisher’snoteSpringerNatureremainsneutralwithregardto
Bordeaux,1–10(IEEE,2010). jurisdictionalclaimsinpublishedmapsandinstitutionalaffiliations.
59. Eyert,V.etal.Atomisticsimulationsofmicroelectronicmaterials:
predictionofmechanical,thermal,andelectricalproperties.In OpenAccessThisarticleislicensedunderaCreativeCommons
MolecularModelingandMultiscalingIssuesforElectronicMaterial Attribution-NonCommercial-NoDerivatives4.0InternationalLicense,
Applications.(eds.Iwamoto,N.,Yuen,M.,Fan,H.)(Springer,2012). whichpermitsanynon-commercialuse,sharing,distributionand
60. Larsen,A.H.etal.Theatomicsimulationenvironment-aPythonlibrary reproductioninanymediumorformat,aslongasyougiveappropriate
forworkingwithatoms.J.Phys.Condens.Matter29,273002(2017). credittotheoriginalauthor(s)andthesource,providealinktotheCreative
61. Foiles,S.,Baskes,M.&Daw,M.S.Embedded-atom-method Commonslicence,andindicateifyoumodifiedthelicensedmaterial.You
functionsforthefccmetalsCu,Ag,Au,Ni,Pd,Pt,andtheiralloys. donothavepermissionunderthislicencetoshareadaptedmaterial
Phys.Rev.B33,7983(1986). derivedfromthisarticleorpartsofit.Theimagesorotherthirdparty
62. Lennard-Jones,J.E.Ontheforcesbetweenatomsandions.Proc.A materialinthisarticleareincludedinthearticle’sCreativeCommons
109,584–597(1925). licence,unlessindicatedotherwiseinacreditlinetothematerial.Ifmaterial
63. Choy,T.C.EffectiveMediumTheory:PrinciplesandApplications2nd isnotincludedinthearticle’sCreativeCommonslicenceandyourintended
edn,Vol.256(OxfordUniversityPress,2015). useisnotpermittedbystatutoryregulationorexceedsthepermitteduse,
youwillneedtoobtainpermissiondirectlyfromthecopyrightholder.To
Acknowledgements viewacopyofthislicence,visithttp://creativecommons.org/licenses/by-
TheauthorsgratefullyacknowledgesupportfromtheH.RobertSharbaugh nc-nd/4.0/.
PresidentialFellowship.
©TheAuthor(s)2026
Authorcontributions
A.C.conceivedthestudy,developedthemethodology,implementedthe
software,curateddata,performedanalysis,preparedvisualizations,and
CommunicationsMaterials| ( 2026) 7:131 16