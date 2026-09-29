communications materials
Article
ANaturePortfoliojournal
https://doi.org/10.1038/s43246-026-01167-0
GENIUS: an agentic AI framework for
autonomous design and execution of
simulation protocols
Checkforupdates
MohammadSoleymanibrojeni1,RolandAydin2,DiegoGuedes-Sobrinho3,AlexandreC.Dias 4,
MaurícioJ.Piotrowski 5,WolfgangWenzel 6&CelsoRicardoCaldeiraRêgo 6
Predictiveatomisticsimulationshavepropelledmaterialsdiscovery,yetroutinesetupanddebugging
stilldemandcomputerspecialists.Thisknow-howgaplimitstheuseofIntegratedComputational
MaterialsEngineering(ICME),wherestate-of-the-artcodesexistbutremaincumbersomefornon-
experts.WeaddressthisbottleneckwithGENIUS,anAI-agenticworkflowthatfusesasmartQuantum
ESPRESSOknowledgegraphwithatieredhierarchyoflargelanguagemodelssupervisedbyafinite-
stateerror-recoverymachine.HereweshowthatGENIUStranslatesfree-formhuman-generated
promptsintoQuantumESPRESSOinputfilesthatpassearlyexecutionvalidationfor ≈80%of295
diversebenchmarks.Zero-shotgenerationsucceedsfor14.2%ofallprompts,andamongcasesthat
donotsucceedinitially,76.3%areautonomouslyrecoveredbytheautomatederror-handlingloop,
withtheattempt-wisesuccessratedecayingexponentiallytowarda7%baseline.Comparedwith
LLM-onlybaselines,GENIUSincreasesinferenceandcomputationalefficiencyandvirtually
eliminateshallucinations.Theframeworkdemocratizeselectronic-structureDFTsimulationsby
intelligentlyautomatingprotocolgeneration,validation,andrepair,enablinglarge-scalescreeningand
acceleratingICMEdesignloopsworldwideacrossacademiaandindustry.
Computational simulations have revolutionized materials design, accel- experimental data, simulations, and theoretical models across multiple
eratinginnovationbyenablingresearcherstoexplorematerialproperties scales.ICMEaimstostreamlinethetransitionfromlaboratorydiscoveryto
andbehaviorvirtuallybeforeexperimentalvalidation1–5.Thisshifthasledto industrial application through predictive modeling15,16. However, its full
significantbreakthroughsthatrangefromenergystorage6,7topharmaceu- potentialremainsconstrainedbywhatimplementationsciencedescribesas
ticaldevelopment8,9.However,apersistentchallengetothispotentialisthe theknow-dogap,thedisparitybetweenavailablecomputationaltoolsand
technicalbarriers to effective simulationsetup,which disproportionately theirpracticalapplicationbythebroaderscientificcommunity.Thisgap
burdenresearchers,particularlythosewhoseexpertiseliesinexperimental persists despite the availability of a wide range of these tools. The open
ratherthancomputationaldomains.Whenscientistsidentifyapromising source community has made remarkable progress in the accuracy and
newcompound,understandingitsfundamentalpropertiesoftenrequires consistencyofcomputationalcodes.Recentcommunity-widebenchmarks
computationalvalidation.Yetevenseeminglystraightforwardsimulations demonstratethatmodernDFTcodesandpseudopotentialsnowyieldnear-
oftenposelengthytechnicalchallenges.Evenexperiencedcomputational identicalequationsofstateforelementalcrystals,approachingtheprecision
scientists (physicists, chemists, engineers) find themselves diverted from ofexperiments17,18.Thistechnicalconvergencesuggeststhatthetoolsare
scientific inquiry toward navigating complex programming challenges, mature,yetthehumaninterfaceremainsasignificantbottleneck.Thetime
engaging in trial-and-error attempts, and struggling with computational spent on technical implementation, rather than on scientific thinking,
setupdetailsratherthanfocusingonthescientificquestions10–14. dramaticallyslowsthepaceofdiscovery.
Integratedcomputationalmaterialsengineering(ICME)hasemerged Ascurrentapproachestocreatingsimulationprotocolsrelyonpre-
asarobustframeworkforacceleratingmaterialsdevelopmentbyintegrating definedorrigidparametersettingsacrossseveralprograms19–21,integrating
1InstituteofMaterialSystemsModeling,Helmholtz-ZentrumHereon,Geesthacht,Germany.2SaarlandUniversityandGermanResearchCenterforArtificial
Intelligence(DFKI),Saarbrücken,Germany.3DepartmentofChemistry,FederalUniversityofParaná,Curitiba,Brazil.4InstituteofPhysicsandInternationalCenter
ofPhysics,UniversityofBrasília,Brasília,Brazil.5DepartmentofPhysics,FederalUniversityofPelotas,Pelotas,Brazil.6InstituteofNanotechnology,Karlsruhe
InstituteofTechnology,Karlsruhe,Germany. e-mail:celso.rego@kit.edu
CommunicationsMaterials| ( 2026) 7:115 1
;,:)(0987654321 ;,:)(0987654321

https://doi.org/10.1038/s43246-026-01167-0 Article
differentcomputationaltoolsremainschallenging.Creatingandvalidating GENIUS reshapes who can participate in computational materials
theseprotocolsrequiresthattheusermanuallyinteractwiththedatabasesto researchbybridgingtechnicalcomputationaltaskswiththenatureofthe
collectrelevantdata.Furthermore,usersmustmasterthesyntaxofseveral materials.WeintegratepreviouslydiscretemanualtasksintoasingleAI
computationaltoolsandpossessdeepexpertiseinallofthem,effectively systembyevaluatingtheresearcher’srequest,generatingcompliantsimu-
becoming experts in their documentation through debugging protocols lationprotocols,validatingthem,andautomaticallyhandlingerrors.This
whenerrorsoccur.Althoughstate-of-the-art(SOTA)electronic-structure integrationimprovesthereproducibility,reusability,andtransferabilityof
codes are accurate, open, and widely accessible, their routine use still simulationprotocols4,10,32whilemakingadvancedsimulationsaccessibleto
demandstechnicalexpertisethatmanydomainscientistsfindchallenging. researchers regardless of their computational background. Our work
This expertise barrier narrows the pool of researchers who can exploit advancesbothinICMEandintheimplementationofscienceobjectives:we
computationalmaterialsscience.Itcreatesbarriersthatdraintimeanddelay enhance the ICME paradigm by making its computational tools more
criticaldiscoveries,therebyslowingthetranslationoftheoryintoconcrete accessible,whileapplyingimplementationscienceprinciplestoovercome
advancesinbatteries,catalysts,andstructuralalloys.Implementationsci- adoption barriers in computational materials research. By allowing
enceprinciples22,23,thefieldthatstudieshowevidence-basedpracticesmove researchers to focus on scientific questions rather than technical imple-
fromthelaboratoryintoeverydayuse,offerapathforward.Bydiagnosing mentation,GENIUSdeliversincrementalefficiencygainswhileenablinga
anddismantlingtheeducational,cultural,andinfrastructuralobstaclesthat fundamental shift in how—and by whom—materials discovery can be
restricttheadoptionofevidence-basedtools,thisprinciplecanshrinkthe conducted33.Inthefollowingsections,wedetailthecreationofthesmartQE
know-dogapseparatingmaturecomputationalcapabilitiesfromtheneeds KG and explain the framework’s architecture, including its specialized
ofworkingmaterialscientists.Thegoalisnottoinventanothermethodbut agentsandsubsystems,suchasrecommendation,protocolgeneration,and
todemocratizeexistingpowerfulmethods,freeingresearcherstofocuson automatederrorhandling.Wepresentbenchmarksassessingtheframe-
scientific questions rather than on software configuration and workflow work’sperformanceacrossseveralcomputationaltasks.
maintenance.Indoingso,wecanacceleratethetranslationofcomputa-
tionalinsightsintoreal-worldmaterialsinnovations,whichmightotherwise Results
transformindustriesandaddressglobalchallenges. We tested GENIUS with multiple LLMs to evaluate our approach, each
Toaddressthiscriticalinterfacebottleneckandbridgetheknow-do exhibiting incremental capabilities, to obtain more comprehensive diag-
gap, this paper introduces GENIUS, an AI-driven agentic framework nosticinsightsintotheworkflow’sperformance.Bygatheringalargedataset
combininglargelanguagemodels(LLMs)24withasmartknowledgegraph ofhuman-generatedpromptsforDFTcalculationsusingQEandthecor-
(KG)25employingreinforcementlearningwithverifiablerewards26–28,that respondingworkflowlogs(seeFig.4),weanalyzedthenumberofattempts
inourcaseinterpretstheschema,enforcesconstraints,reformulatesques- required to successfully complete each prompt. These prompts were
tions,andsurfacesonlyconsistentanswers.Thisframeworkservesasan authoredbychemistsandphysicistswhoroutinelyperformDFTsimula-
intelligentinterfacetocomputationaltools,specificallydesignedtogenerate tionswithelectronic-structurepackagesotherthanQuantumESPRESSO,
andautomaticallydebugsimulationprotocolsbasedondensityfunctional ensuringthatthebenchmarkreflectsrealisticexpertusagewhileremaining
theory (DFT), and to validate our approach, we use the Quantum unbiasedtowardQE-specificsyntax.
ESPRESSO (QE)program29. A schematic overview of this framework is Tounderstandthediversityofthepromptsdataset,weconvertedthe
presented in Fig. 1. The mechanisms of the smart KG with LLMs infer 295 prompts into 3072-dimensional embedding vectors with OpenAI’s
relevantparametersbyunderstandingbothexplicitandimplicitconditions text-embedding-3-large model. A 10 × 10 self-organizing map
intheuser’srequest,andthencriticallyevaluatetheretrievedinformationto (SOM)34wasthentrainedtovisualizetheirsemanticlandscape.TheSOMis
ensure its suitability and context. This process provides the LLM with anunsupervisedneuralnetworkfordimensionalityreductionandcluster-
accurate, structured knowledge, mitigating limitations, such as ingbyprojectinghigh-dimensionalinputdataontoalower-dimensional
hallucinations30,31andenablingreliableprotocolgenerationtailoredtouser grid (here, 2-dimensional) while preserving topological relationships
requirements, including material-specific details from curated databases. betweentheinputdata.Eachofthe100SOMneuronswasinitializedwitha
Furthermore,theframeworkincorporatesrobustautomatederrorhandling randomweightvectorofequaldimensionality,andtrainingproceededfor
thatcandebugandvalidateprotocolswheninitialattemptsfail,thereby 50,000iterationsinmini-batchesof50samples.Duringeachiteration,the
overcoming a significant hurdle in generating protocols for practical neuronscompetetobestrepresenttheinputpattern.Thealgorithmiden-
simulation workflows. This integrated approach addresses the inherent tifiesthebestmatchingunit(BMU)foreachinputvector,whichisdefinedas
limitationsofcurrentAImodelswhenappliedtoprecisescientifictasks. theneuronwhoseweightvectorhasthesmallestEuclideandistancetothe
Fig.1|GENIUSframeworkforautonomous
QuantumESPRESSOsimulations.Thisschematic
illustrationdepictstheend-to-endworkflowofthe
GENIUSframework,designedtoovercometechni-
calbarriersinDFTsimulations.Users'naturallan-
guagepromptsareinterpretedbya
recommendationsystempoweredbyasmart
knowledgegraphthatencodesQuantum
ESPRESSOparameterdetailsandconstraints.Large
languagemodelsthengeneratethecorresponding
simulationprotocols.Theframeworkincludes
automatedvalidationandanautomatederror
handling(AEH(error1anderror2)loopthatutilizes
aknowledgegraphandlargelanguagemodelsto
diagnoseandcorrectfailedrunsiteratively.This
integratedprocessautonomouslytranslatesuser
intentintovalidatedQuantumESPRESSOinput
files,readyforsubmissiontotheavailablecompu-
tationalresources.
CommunicationsMaterials| ( 2026) 7:115 2

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.2|Self-organizingmap(SOM)analysisofuserinputpromptembeddings. count)showingthedistributionofpromptsacrosstheneurongrid.Fivedistinct
aU-matrixvisualizationoftheSOMtrainedonuserpromptembeddings,where high-activationandlow-activationregionsarescatteredinbetween,suggestinga
regionswithmoredistanceindicateclusterboundariesandregionswithlower balancebetweensemanticclustersanddiverserequesttypesintheinputdata.
distancedenotedenseclustersofsimilarprompts.bSOMhitmap(BMUactivation
inputvector.Afterward,theBMUanditsneighboringneuronsareupdated, significantlytosemanticdistinctionsandhelpingidentifycorrelatedcom-
withtheadjustmentmagnitudedecreasingasafunctionofdistancefromthe ponentsthatformmeaningfulsemanticfeatures.Thesevisualizationsare
BMU,accordingtoaGaussianneighborhoodfunction.Thisneighborhood availableintheproject’sGitHubrepository.Thefigureshowsfiveneurons
influence, combined with a linearly decreasing learning rate, allows the withthehighestactivationcounts,includingtheirrespectiveBMUs.These
SOMtoformatopologicallyorderedmapoftheinputspace.Thecon- neuronsarewell-separatedontheSOMgrid,indicatingthatthecalculation
vergenceandqualityoftheresultingmapwerequantitativelyvalidatedby promptscanbegroupedprimarilyintofivesemanticclusters,withaddi-
calculatingstandardSOMmetrics:thequantizationerror,representingthe tional residual prompts that share similarities with the core concepts.
averagedistancebetweeninputdatavectorsandtheirbestmatchingunit’s Overall,theSOMgridshowsthatthepromptcollectionisdispersed,pro-
weightvector,andthetopologicalerror(TE),measuringtheproportionof viding a good balance between semantic cohesion within the identified
datapointsforwhichthefirstandsecondBMUsarenotadjacentonthe clustersandconceptualdiversityacrossthem.Uponmanualinspectionof
mapgrid. prompts,itwasfoundthatthepromptsaremainlydividedintotwomajor
TheSOMandBMUanalysesprovideinformationontheprompts’ categories,namelystructuralrelaxationandavarietyofsingle-shotDFT
degreeofcomplexityandsemanticsimilarity.Thescore-basedmetriceva- calculations,usingdifferentmethodologiesavailableintheQEcode,which
luationshowsthatthepromptscomprise44.3%basic,48.5%standard,and isfurtherconfirmedbyasimplerk-meansanalysis(SeeGitHubrepository).
7.2%complexprompts.ThisevaluationisperformedbyanLLM,which Discussing these findings highlights the framework’s sensitivityto input
assignsanumericalvaluetotextdata35.TheSOManalysiscreatesaself- quality and type, potentially informing future improvements to user
organizingmapgridofhexagonallypackedneurons,Fig.2,trainedonthe interactionorpromptpre-processing.Thisanalysisuncoverslatentstruc-
embeddingsoftheprompts,whicharethenclusteredintodifferentgroups. turesintheuser-requestspacethataredirectlyrelevanttothedevelopment
The SOM preserves topological identitywhile showingthe clusters.The ofautomatedprotocol-generationmechanisms.
qualityoftheSOMrepresentationreinforcesthereliabilityoftheobserved InFig.3,theuser’sprompt(classifiedasstandard)isshownatthetop,
promptdistribution(Fig.2).ThelowTE(0.0373)confirmsexcellentpre- specifying a geometry optimization for a 2D PdS structure using the
2
servationoftheoriginaldata’sneighborhoodstructure.Thequantization B3LYP functional, whereas the bottom portion highlights the valid QE
error(0.4970)indicatesgoodrepresentationalfidelity;giventhattheinput inputfilegeneratedbytheGENIUSframework.InFig.4,weillustratethe
vectors were unit-normalized (maximum pairwise distance of 2.0), the completetimelinelogforthesameprompt,emphasizingthesequenceof
averagedistancebetweendatapointsandtheirmaprepresentativesislow, events,asindicatedbycolor-codedstatuses(PENDING,SUCCESS,RETRY,
especially given the significant dimensionality reduction. The U-matrix andERROR),asthesystemprogressesfromtheinterfaceagentphasetothe
(unifieddistancematrix)inFig.2ashowsthedistancesbetweenneurons;the finalsolutiongeneration.AsevidencedinFig.4,theextendedtimerequired
hexagonal structure captures six equidistant neighbors, compared to a toevaluateinputparametersisasecondaryconstraintimposedbyLLMAPI
square grid with only four. To analyze the learned representations, two providers,whichaself-hostservicecouldmitigate;withoutsuchlimitations,
complementaryvisualizationsweregenerated.TheU-matrixvisualizesthe parameters could be processed in parallel, reducing overall latency. The
average distance between neighboring neurons, with higher values indi- stepwiseentriesinthelogfiguredemonstratetheframework’sresilience,
cating cluster boundaries and lower values indicating dense regions of including how QE crashes (red dots) can result from hallucinations or
similarinputs.TheBMUactivationcountplot(hitmap)inFig.2bshows confabulations. Our framework automatically detects and resolves these
how frequently each neuron was selected as a BMU, revealing the dis- failures,iterativelyrefiningandvalidatingtheinputparametersuntilthe
tribution of input assignments across the SOMgrid. Neurons with zero finalQEcalculationiscompleted.It’simportanttonotethatthewall-clock
activationsindicatetheyserveasboundaryregionsorrepresentsemantic performanceillustratedinFig.4reflectsthespecificbenchmarksetupused
areasnotcoveredbythecurrentdataset.Theseemptyneuronsarecrucialfor in this research. In this setup, considering only the QE attempt has a
preserving topology, helping maintain proper inter-cluster distance maximumvalidationperiodof60s.Asaresult,theoverallworkflowrun-
relationships. timeisprimarilyinfluencedbyorchestrationfactors,suchasmodelinfer-
AsimilarSOMrepresentationcanbegeneratedforeachcomponentof enceandretrymechanisms,ratherthanthetimerequiredtocompleteafull
the embedding vectors, revealing which dimensions contribute most productionDFTcalculation.
CommunicationsMaterials| ( 2026) 7:115 3

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.3|RealsimulationprotocolexampleofQuantumEspressogeneratedby specifies20%exact-exchange,aplane-wavebasisset,smearingforoccupation,a
GENIUS.Theuser’spromptrequestisdisplayedatthetop,instructingtheQEcode mixingparameterfortheSCFcycle,anda7×7×2k-pointsmesh.Additionally,the
toperformageometryoptimizationfor2DPdS intheP21/cspacegroup,using fileincludesdetailedcontrolparametersforgeometryrelaxation(viaBFGS),
2
QuantumESPRESSOwiththeB3LYPexchange-correlationfunctional.Thegen- pseudopotentialsforPdandS,andtherequiredsettings,includingecutwfc,ecutrho,
eratedprotocolisprovidedintwocolumnsforcompactness.Theframeworkparses occupations,andspinpolarization,asshownintheoutput.
theseinstructionsandautomaticallygeneratesthevalidQEinput.Theprotocol
Anoverviewoftheoutcomesforthe295testpromptsispresentedin zero-shotsuccesscorrespondstocasesinwhichthefirstoutputgeneratedby
Fig.5,whichdepictsthedistributionbetweensuccessfulandfailedruns,the Model1isvalidanddoesnotrequireanyfurthercorrection.Withinthe
pathtosuccess,zero-shotorviaspecificmodelsintheAEHsystem,aswellas GENIUSframework,Model1proceedswiththefirstcycleofautomated
abreakdownaccordingtotheinitialpromptcomplexity.Additionally,when error-handlingretriesifthisinitialattemptfails.
prompts are evaluatedusing only base LLMs, without the GENIUS fra- InFig.5,wepresentthedistributionofsuccessfulrunsthatreachedthe
mework,theyyieldnegligiblecontributionstogeneratingvalidQEinput FINISHEDstateintheworkflowafteragivennumberofattempts.The
filesthatcontainthecorrectcardsandmutuallyconsistentparametersfora success in zero-shot cases indicates scenarios in which a request was
givengeometricstructure,regardlessoftheirnominalreasoningenhance- FINISHEDusingonlytheworkflow’srecommendationsystem,without
ments.Thislimitationlikelyarisesbecausethemodelsdonotembedexplicit invokingtheautomatederror-handlingsystem.Thisscenarioaccountsfor
crystallographicinformationandcannotinferthesubtleinterdependencies 17.9%,comprising9.4%forbasicprompts,7.2%forstandardprompts,and
amonggeometry,namelistkeywords,andthecardsyntaxrequiredbyQE. 1.3%forcomplexprompts.Asimilardistributionpatterncanbeobserved
WereiteratethatModel1,thefirstcomponentintheprotocolgeneration for subsequent attempts. If the initial execution fails, the GENIUS AEH
hierarchy, produces the initial simulation protocol version. Therefore, a systemistriggered.Eachretrywithinanattemptcycleusesthesamemodel
CommunicationsMaterials| ( 2026) 7:115 4

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.4|Livetimelineofaself-healing(AEH)GENIUSjob.Eachdotmarksalog finite-stateloopappliesasingleretry(gray)withintheAEH,resolvestheissue,and
event(y-axis,newestattop)plottedagainstwall-clocktime(x-axis),colorsdenote thesimulationreachessteadyexecutionandcompletion(green)in≈3min.The
status:PENDING(orange),SUCCESS(green),RETRY(gray),ERROR(red).The timelineexposesfullprovenanceandillustrateshowGENIUSautonomously
workflowfirstparsestheuserprompt,harvestsdocumentation,buildsaparameter recoversfromruntimefailureswhilestreamingreal-timestatusupdates.
graph,andgeneratesaQEinputtemplate.Afterlaunch,QEcrashesonce(red);the
that generated the initial protocol. After three attempts per model, the theprecedingstages.ThisdemonstratesthattheGENIUSframeworkcanbe
processswitchestothenextmodelinthehierarchyifnosolutionisfound. usedwithanymodel(itismodel-agnostic)andthatitsoverallperformance
Based on the user’s calculation prompt, the workflow resets from the isattributabletoitsarchitectureintelligence,notjusttheunderlyinglan-
recommendationsystem’soutput,whichservesasatemplateforgenerating guagemodel’scapabilities.Theoppositescenariowouldmanifestasalackof
asimulationprotocol.Previouschangelogattemptsarenotprovidedtothe abaseline,withanincreaseinsuccessfulattempts.Specificallyindicating
newmodelduringeachmodelexchange.Themodelreceivesonlytheerror thatsuccessreliedprimarilyonthemoreperformativemodelratherthan
message,therelevantdocumentation,thelatestversionofthesimulation theframework’sarchitecturaldesign.
protocol,andtheoriginalusercalculationprompt. Fromourtotaldatasetof295calculationrequestsanalyzed,235suc-
Ourresultsdemonstratethatsuccessfulcasesacrossattemptscomprise cessfullyproducedavalidsimulationprotocol,with42ofthesesucceeding
a mixture of basic, standard, and complex calculation prompts. This inthezero-shotscenario,whichisdefinedhereastheframeworkconverging
observationshowsthatpromptcomplexity(basic,standard,orcomplex)is toacorrectprotocolonitsveryfirstattempt,withoutinvokinganyauto-
not inherently problematic for the framework’s performance. Complex matederror-handlingloops.Thisyieldsanoverallsystemsuccessratioof
promptscancontainmoredistinctiveinstructions,enhancingtheframe- PðSÞ¼235(cid:2)0:7966, a zero-shot, (ZS), success ratio of
295
work’sabilitytogeneratevalidprotocols.Thegeneraltrendrevealsthatafter PðZSÞ¼ 42 (cid:2)0:1424, and a ratio of success through automated error
295
theinitialattemptswithModel1,thenumberofsuccessfulattemptssta- handling (given zero-shot fails) of PðAEHjnotZSÞ¼193(cid:2)0:7628. To
253
bilizes at a baseline level. This initial high success rate is followed by a characterizehowthesuccessrateevolveswithsuccessiveattempts,wefitted
plateau,whichresemblesanexponentialdecaybehaviorinthenumberof anexponentialdecaymodeltotheobservedsuccessrates(S)acrossmultiple
casesrequiringsuccessiveattempts.Forthemodelselectionhierarchy,we attempts,wherexdenotestheattemptnumber.Thefunctiontakestheform,
assumeaperformanceorderingofModel1<Model2<referee.Thiscanbe Eq.1:
donewithanysetoflanguagemodels,butthepredefinedordercharacterizes
theframework’sbehavior,wheretherefereemodelwaschosenastheSOTA SðxÞ¼Ae (cid:3)bxþC;RMSE¼1:9%; ð1Þ
model.Therefereemodelisusedtoestablishtheperformancebaseline.This
outcomeindicatesthattheframeworkitself,ratherthanjustthepowerofthe obtainingA=11.1%±1.0,b=0.46(1/attempt)±0.1,andC=7.0%±0.70.In
strongestmodel,isresponsibleforhandlingmostcases,astherefereemodel thisparametrization,theinitialamplitude,A(%),representsthemaximum
isnotdisproportionatelyutilized,whichwouldotherwisesuggestafailurein influenceofthezero-shotattempt;thedecayrate,b(1/attempt),determines
CommunicationsMaterials| ( 2026) 7:115 5

| https://doi.org/10.1038/s43246-026-01167-0 |     |     |     |     |     |     |     |     |     |     |     |     |     | Article |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
Fig.5|GENIUSperformancebenchmarkon295testedprompts.Thestackedbar samemodel.Withineverybar,coloredsegmentsdisaggregatethetotalsuccessrate
chartreportsthepercentageofsuccessfulruns(y-axis)forthezero-shotpass bypromptcomplexity:basic,standard,andcomplex.Thecumulativesolvedper-
(GENIUSwithoutAEH)andGENIUSusingAEHcombinedwithModel1,Model2, centage(righty-axis)isoverlaidindarkblue,showingthetotalproportionof
andrefereemodels.Shadedverticalpanelsgroupthebarsforsystemsassessedbythe promptssolvedaftereachsuccessiveattempt.
howquicklythisinitialadvantagedecreasesoversuccessiveattempts,and To estimate the system’s performance in the absence of Rec, we
thebaseline,C(%)istheasymptoticsuccessprobabilityreachedaftermany introducethescalingfactorsαandβ,whichquantifyhowmuchRecmul-
tipliesthezero-shotandAEHsuccessprobabilities,respectively,assumingα,
retries.
β≥1.UsingEq.2thehypotheticalQ-onlysuccessprobabilitiesarethen,
Figure6delineatesthreedistinctoperationalregimeswithinGENIUS:
workflow
| recommendation-system, |     | maximum |     |     | utilization, | and | shallow |     |     |        |         |     |         |        |     |
| ---------------------- | --- | ------- | --- | --- | ------------ | --- | ------- | --- | --- | ------ | ------- | --- | ------- | ------ | --- |
|                        |     |         |     |     |              |     |         |     |     | 0:1424 | (cid:1) |     | (cid:3) | 0:7628 |     |
workflowutilization.Theopeningrecommendation-systemregimecoincides
|     |     |     |     |     |     |     |     | PðZSjQ(cid:3)onlyÞ¼ |     |     | ; P AEHj:ZS;Q(cid:3)only |     | ¼   |     | ; ð3Þ |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ------------------------ | --- | --- | --- | ----- |
withthezero-shotpass,highlightingtheframework’sabilitytosuccessfully α β
generateprotocolsindependentlyofmodelswitchingorfallbackmechan-
isms.Immediatelythereafter,thecurveplungesintothemaximumwork-
sothat
flow
| utilization | regime: | each | early retry | unlocks | deeper | cross-model |     |     |     |     |        |        |        |     |     |
| ----------- | ------- | ---- | ----------- | ------- | ------ | ----------- | --- | --- | --- | --- | ------ | ------ | ------ | --- | --- |
|             |         |      |             |         |        |             |     |     |     |     | 0:1424 | 0:7628 | 0:1086 |     |     |
synergies,yieldingrapidlydiminishingbutstillsubstantivegains.Oncethe
processreachesroughlysixattempts,thetrajectoryflattensintotheshallow PðSjQ(cid:3)onlyÞ¼ þ (cid:3) : ð4Þ
|          |             |               |     |             |                |     |      |     |     |     | α   | β   | αβ  |     |     |
| -------- | ----------- | ------------- | --- | ----------- | -------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| workflow | utilization | regime, where | the | performance | asymptotically |     | con- |     |     |     |     |     |     |     |     |
vergestowardthebaselinevalueof C≈7%.Withinthisregime,further Settingα=β=γgives
| retries contribute | marginal | benefit; | success | is governed |     | primarily | by the |     |     |     |     |     |     |     |     |
| ------------------ | -------- | -------- | ------- | ----------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
workflow’s inherent competenceratherthan by additionalcomputation. 0:9052 0:1086
|     |     |     |     | fitted |     |     |     |     |     | PðSjQ(cid:3)onlyÞ¼ |     | (cid:3) | :   |     | ð5Þ |
| --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | ------------------ | --- | ------- | --- | --- | --- |
The slight oscillations superimposed on the curve stem from the γ γ2
designchoicetoresetthecontextaftereverythirdattemptandswitchthe
influence
| model. Inter-block |     | is  | shortened | because | each | reset isolates | the |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --------- | ------- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Thisdependencyofthesuccessprobabilityontheeffectivenessofthe
| subsequent  | block of | attempts.           | Allowing | more  | consecutive | attempts          | per |                |     |        |                   |     |            |                |     |
| ----------- | -------- | ------------------- | -------- | ----- | ----------- | ----------------- | --- | -------------- | --- | ------ | ----------------- | --- | ---------- | -------------- | --- |
|             |          |                     |          |       |             |                   |     | recommendation |     | system | can be considered |     | with a few | representative |     |
| model would | amplify  | these oscillations, |          | which | could       | be quantitatively |     |                |     |        |                   |     |            |                |     |
examples:Inthelimitingcasewheretherecommendationsystemhasno
capturedbyextendingthefittingfunctiontoincludeanexplicitperiodic
effect(γ=1),thesuccessprobabilityis0.7966,whichisthesameasthe
component,therebyrequiringfiner-grainedmodeling.
overallsuccessprobabilitywiththerecommendationsystem.Acasewhere
The recommendation system (Rec) includes the smart knowledge the recommendation system has an effectiveness reduction of 50% (i.e.,
graph,extractsboundaryconditions,andevaluateskeyparametersforeach γ=1.50),thesuccessratewithouttherecommendationsystemdropsto
userquery(Q).Theworkflowiscompleteifthecalculationrequestissuc-
(γ
|     |     |     |     |     |     |     |     | 0.56.In | thecase | of doubleeffectiveness |     | =2),thesuccess |     | rate | further |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ---------------------- | --- | -------------- | --- | ---- | ------- |
cessfullyresolvedinazero-shotscenario.Otherwise,therequestproceedsto
declinesto0.43.Thesensitivityofthesuccessrateconcerningvariationsin
the AEH subsystem, which can be a successful case. Given an effective therecommendationsystem’seffectivenessisshowninthefollowingEq.6:
recommendationsystem,wecandecomposeSasinEq.2:
|                                                 |                                       |     |     |     |     |     |     |     | d   |                           | 0:9052 | 0:2172 |       |      |     |
| ----------------------------------------------- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------- | ------ | ------ | ----- | ---- | --- |
|                                                 |                                       |     |     |     |     |     |     |     |     | PðSjQ(cid:3)onlyÞ¼(cid:3) |        | þ      | ; for | γ>1: | ð6Þ |
|                                                 | PðSÞ¼PðZSÞþð1(cid:3)PðZSÞÞPðAEHj:ZSÞ: |     |     |     |     |     | ð2Þ |     | dγ  |                           |        | γ2 γ3  |       |      |     |
| CommunicationsMaterials|  (        2026) 7:115  |                                       |     |     |     |     |     |     |     |     |                           |        |        |       |      | 6   |

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.6|Exponentialdecayfit(redcurve)appliedtotheobservedfractionof rapidlydiminishingbutstillsubstantivegains,andthelong-tailshallowworkflow
successfulrunsperattemptnumber(blackpoints).Asingle-parameterexpo- utilizationzoneinwhichperformanceplateausatthe7%baseline.Thefitconfirms
nential,S(x)=11.1e−0.46x+7.0%(redline),capturesthetrend.Shadedbandsspecify thatmostrecoverableerrorsarecorrectedwithinthefirstthreeattempts,afterwhich
thethreeoperatingregimes:theopeningrecommendationsystemzone(zero- additionalcomputationyieldsmarginalreturns.
shotwins),thesteepmaximumworkflowutilizationzonewhereearlyretriesyield
Thisderivativeindicatesthatthereductioninsuccessrate(whenthe 247parametersand330dependencyedges,theKGsuppliestheLLMswith
recommendationsystemisremoved)ismostsensitivewhenitseffectiveness grounded,constraint-awarefacts,reducinghallucinationsandimproving
factor(γ)iscloseto1.Theseresultsimplythattherecommendationsystem syntactic and physical consistency. Model hierarchy: lightweight models
significantlyboostssystemperformance.Asγincreases(implyingthatthe address most queries, while larger models are invoked only when the
recommendationsystemisevenslightlyeffective),thesuccessprobabilityin workflowstalls,improvingcost-performancetrade-offswithoutsacrificing
theQ-onlyregimediminishessharply.Thederivativeanalysisconfirmsthat robustness. Finite-state error recovery: a transparent finite-state machine
the decrease in success probability is steepest when γ is near 1. Small monitorseveryrun,restartsfromacleantemplateafterthreefailedfixes,and
enhancementsduetotherecommendationsystemcanleadtosubstantial escalatesonlywhentheevidencejustifiestheadditionalexpense.
differencesinoverallperformance.Thebenchmarkreportedhereevaluates Together,theseelementshelpnarrowtheknow-dogapthatseparates
protocolexecutabilityusingthecontrolledvalidationproceduredescribed matureelectronic-structurecodesfrommoreroutine,accessibleuse.This
in the “Methods” section. Accordingly, a successful case indicates that reducestheneedforuserstoengagedirectlywitharcaneinputsyntax,while
GENIUSgeneratedaQEprotocolthatpassedparsingandearlyruntime allowingcomputationalspecialiststoredirectmoreeffortfromboilerplate
validationwithinthebenchmarkwindow.Thismetricdoesnotbyitself scriptingtowardscientificexploration.InthecontextofICME,GENIUS
establishthattheresultingworkflowisscientificallyoptimal,thatitisthe addressesanimportantimplementationbarrier,helpingpredictivesimu-
uniqueprotocolanexpertuserwouldhavechosen,orthatitimprovesend- lation integrate more effectively into design loops and high-throughput
user productivity relative to manual practice. These questions require campaigns. By automating protocol generation, validation, and repair,
dedicatedcomparativestudieswithhumanusersandarethereforeleftfor GENIUS can broaden access to advanced simulation tools for groups
futurework. without deep computational expertise, thereby supporting wider partici-
pationinmaterialsdiscovery.Itstransparentlogsalsosupportreproduci-
Conclusion bility,aprerequisiteforFAIRdatapractices.
Our study demonstrates that the GENIUS framework has successfully ThepresentKGcoversonlypw.x;extendingittootherQuantum
automatedprotocolgeneration,earlyvalidation,andfailurerecoveryfora ESPRESSOmodulesandtocodesbeyondQEwillbroadenGENIUS’sreach.
substantialfractionofQE-basedDFTrequestsunderthebenchmarkcon- TheGENIUSarchitectureis,inprinciple,transferabletoothersimulation
ditionsstudiedhere.Byintegratingadomain-specificknowledgegraphwith codesprovidedthatfourkeyelementsarepresent:(i)acuratedparameter
atieredstackoflargelanguagemodelsandanintelligent,automatederror- representationencodingsyntax,dependencies,andconditionallogic;(ii)a
handlingloop,theframeworkconvertstextuserrequestsintoQuantum retrieval layer that maps user prompts to this representation; (iii) an
ESPRESSOsimulationprotocolinputsthatpassearly-executionvalidation executablevalidatorthatexposesmachine-interpretableerrors;and(iv)a
forapproximately80%ofthebenchmarkcases.Whentheinitialattempt backendadapterforsubmission,monitoring,andprovenancecapture.In
fails,theagenticlooprepairs>76%ofcrashes,andtheattempt-wisesuccess thissense,thecoredesignofGENIUSiscode-agnosticatthesystemslevel.
curvefollowsafastexponentialdecaytowardastable7%baseline,indicating However, its practical performance in a new domain will depend sig-
thatmost recoverableerrorsareneutralizedinthe earliestretries.These nificantlyonthequalityofthedocumentation,theinformativenessofthe
claimsareconsistentwiththeroleofQEinthisstudyasanexecution-level targetcode’serrormessages,andthematurityofthecuratedknowledge
validator,inwhichmalformedorinconsistentinputstypicallyfailimme- representation.Community-drivencontributionscouldincludeadditional
diatelyduringinputreadingoratearlyruntimestages.Threearchitectural simulationcodes,refinededgeconditions,andenrichedmanuallycurated
choicesunderpinthisperformance.Smartknowledgegraph:encapsulating metadata.
CommunicationsMaterials| ( 2026) 7:115 7

https://doi.org/10.1038/s43246-026-01167-0 Article
Finally, incorporating physics-informed validators (e.g., symmetry validation), and (iv) terminal states: indicating either success (valid
checks,chargecounting)andadaptivehyperparametertuningmayfurther protocolgeneration)orfailure(unresolvederror).Theoverallframework
improvefirst-shotaccuracy.Forhigh-costproductionworkloads,wedonot isillustratedinFig.7.GENIUSkeepsreasoningandexecutionseparateby
viewfullyautomaticsubmissionastheonlyappropriateoperatingmode.A preventing the language model from directly accessing the execution
human-in-the-loop checkpoint between protocol drafting and scheduler system.Instead,itcreatesastructuredprotocolobjectthatissenttoa
submissionisbothtechnicallystraightforwardinthecurrentarchitecture reliableexecutionlayer,whichthenmanagesthenecessaryinputfilesand
and scientifically desirable when modeling choices remain ambiguous. handlesthesubmissionlocally.Thisseparationensuresthatusersand
GENIUSshowsthatasubstantialpartofthelong-standingtechnicaldragon sitesretaincontroloverkeysettings,includingpermissions,jobqueues,
computational materials science can be reduced when factual domain timelimits,filestorage,andaccountingrules.Inpractice,thissystemalso
knowledge,strategicmodelselection,anddisciplinedworkflowcontrolare allowsahumanreviewstepbeforeanylong-runningtasksaresenttothe
fusedintoasingleagenticsystem. scheduler. This design also supports a human-in-the-loop operating
modeforexpensiveproductioncalculations.Inthismode,thestructured
Methods protocol draft can be presented to the user for confirmation or clar-
WedevelopedGENIUStoaddresstechnicalchallengesincomputational ification of ambiguous choices, for example, the exchange-correlation
materialsscienceandtomakeQE-basedsimulationmethodsmoreacces- functional, spin treatment, boundary conditions, k-point density, or
sible to researchers in the domain. Although we focus here on QE as a relaxation strategy, before the calculation is released to the scheduler.
representativecase,thisapproachcaneasilybeextendedtoanyatomistic This interactive checkpoint was not activated in the present
simulationcode,includingmoleculardynamics.Thisframeworkcombines benchmark because all QE executions were intentionally limited to a
LLMswithasmartKG,servingasanintelligentinterfacebetweenusersand shortvalidationwindow.
QE to automate the generation, validation, and debugging of complex
simulationprotocols.Oursystemarchitecturecomprisesthreemaincom- Smartknowledgegraph
ponents,whichare:(i)arecommendationsystem,(ii)aprotocolgeneration Theuserinterfaceswiththeoriginaldocumentation,asprovided,viaour
module,and(iii)anautomatederrorhandlingsystem(denotedaserror1 developed smart KG, as shown in Fig. 8a, which displays the QE KG
anderror2)asshowninFig.1.Thesecomponentsaredesignedtohandle structure.Theusercansearchfornodesandexaminetheirconnectivity.
specificaspectsoftheworkflow,fromuserinputtothegenerationofthe Althoughweperformedsomemanualrefinement,theparameterdescrip-
finalprotocol.Theframeworkprioritizesreproducibility,accuracy,anduser tionsremainfaithfulto the originaldocumentation.The KG is thecore
adaptability,aligningwithbestpracticesandscientificstandardsincom- componentoftherecommendationsystem,comprising247nodesand330
putational materials research. Therefore, references to computational edges,providingstructured,connectedinformationextractedfromtheQE
resources,modelnames,serviceproviders,orotherentitiesaremadeby programdocumentation.ThedatasourcefortheQEknowledgegraphisthe
name,astheseareconsideredcommonknowledgewithintherelevantfields. online documentation for the QE pw.x code at https://www.quantum-
espresso.org/Doc/INPUT_PW.html. Initially, the documentation was
Systemarchitectureoverview convertedintoaplain.txtversion,asQEusesparametersorganizedinto
InGENIUS,ourthree-tierQEsimulationprotocolgenerationarchitecture namelesssectionsandcards,eachwithdistinctsyntaxandpurposes,
isbasedonasetofsequentialpropositions.(i)Recommendationsystem:this whichmadethisformateasiertomanagethantheoriginalHTMLformat.As
interfaceconnectstheusertotheprotocolgenerationpipeline.Itcomprises aresult,informationwasextractedseparatelyforeachtype.Thecurated
submodulesthatcollectmaterial-specificinformation,retrieverelevantQE documentationwasthentransformedintoakey-valuepairformatusing
simulationparameters,andevaluatethem.Thisinformationisformulated anthropic/claude-3.5-sonnet36 language model, followed by
into a template recommended to the protocol generation system. The manual verification and adjustments. For a complete description of the
templateincludesacollectionofparameterswithsuggestedvaluesanddata resultingkey-valueschema(includingallnamelistandcardentries,their
types (CHARACTER, REAL, INTEGER, and LOGICAL), followed by connectionsandconditionskeys,andillustrativeJSONexamples,
material-specific information, such as atomic positions and appropriate such as the parameter nspin and card ATOMIC_SPECIES given in
element-specificpseudopotentials.(ii)Protocolgenerationsystem:itgen- Fig.8b,c),pleaserefertoourGitHubrepositoryathttps://github.com/KIT-
erates the simulation protocol based on the template provided by the Workflows/agentic-workflow-framework/blob/main/knowledge_graph_
recommendationsystem.Thesystemmaynotuseallsuggestedparameters, schema.md.Giventhespecializedexpertiserequired,improvingtheKG,
asthefinalselectionoccursduringprotocolgeneration,takingintoaccount particularlytheconnectionsandconditions,remainsanareaforfuturework
theuser’spromptandadditionalcontextprovidedtotheLLM.Thegen- andpotentialcommunitycontributions.Werefertothisobjectassmart
eratedinputissyntacticallyvalidatedbyrunningtheQEprogram.Upon whenwenameitassmartknowledgegraphtodistinguishitfromaplain.
successfulvalidation,theworkflowconcludes.Ifvalidationfails,theauto- The nodes are retrieved from the KG using two complementary
matederror-handlingmoduleisinvoked.(iii)Automatederrorhandling approaches:(i)directkeywordmatchingand(ii)context-awareretrieval
system:itreceivesthecurrentsimulationprotocolanderrormessagesfrom basedongraphrelationshipsandinferredlogicalconditions.Athresholdof
theQEprogramandextractsrelevantdocumentationfromthesemessages. top70%cosinesimilarity37isusedasthecutoffforretrieval,increasingthe
Usingthecurrentlygeneratedprotocolandextracteddocumentation,the numberofnodesevaluatedandrequiringmorecomputationalresources.A
errorcanberesolvedandtheprotocolrevalidated.EachLLMisallocateda hashingvectorizerisemployedfornodeembeddingbecauseitisrobust,
specificnumberofattemptstoresolvetheerror.Iftheerrorpersists,the reliable, fast, and effective for large corpora. Due to the domain-specific
systemswitchestothenext,presumablymorecapableLLMinapredefined nature of calculation requests, keyword- and condition-based retrieval
hierarchy.Ifallattemptsfail,theprocessterminateswithafailuremessage. proved highly effective and efficient compared to denser embedding
representations.Additionally,implicit conditions were inferred from the
Systemcomponentsintegration.Theframeworkemploysafinite-state user’s input request. For example, when a calculation mentions the Cu
machine (FSM) architecture to manage component interactions and surface,bulk,orelementalsystem,themetallicsystemsconditionis
workflowprogression.EachcomponentoperatesasadistinctFSMstate automaticallyinvoked.Weextracted162conditionsunderninedifferent
node,withwell-definedtransitionconditionsthatdependonthestateof categoriestofacilitateknowledgeretrieval.Theseninecategoriesare:cal-
theexecutingprocess.TheFSMimplementationhasan(i)entrynode:to culationtype,functionalandmethod,cellandmaterialproperties,pseu-
initialize theframework andvalidateuserinputs, (ii)state transitions: dopotential,magnetism(andspin),isolatedsystems(byimposingboundary
definedbythesuccessorfailureconditionsateachprocessingstep,(iii) conditions),k-pointsettings,electric-fieldconditions,andoccupationtypes.
errorrecoverystates:implementingretrymechanisms(forI/O,network, User input requests are processed under these nine categories, and the
CommunicationsMaterials| ( 2026) 7:115 8

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.7|StatediagramoftheAI-drivenframeworkforgeneratingQEsimulation (“QeInputGeneration”).“ExecutionValidation”runsthesimulation(“QeRun”),
protocols.Thediagramisorganizedintofourcompositestates(dashedboxes): transitioningto`Finished'onsuccess.“AutomatedErrorHandling”detectsfailures
RecommendationSystemparsestheuser’snatural-languagerequest(“inter- (“FailureDetected” →“CheckRetries”)andeitherretriesexecution(“Attempt-
face“→“InitializeWorkflow”),retrievesmaterialsdata(“MaterialsDb”)andsimu- Correction”),switchestoanalternativemodel(“SwitchModel”),orterminatesat
lationparameters(via“DocumentCollection”→“ConditionExtraction”→ “failure”ifalloptionsareexhausted.Solidarrowsshowtransitionslabeledwiththe
“RetrieveCandidateParameters”),andevaluatesthem(“EvaluateParameters”)to triggeringactionorcondition;colorandclassstylingdifferentiatedatasources,main
produceastructuredinputtemplate.“ProtocolGeneration”usesthattemplate processes,anderror-handlingloops;moredetailscanbefoundintheGitHub
(“PrepareInputTemplate”)togeneratetheactualQEinputfile repository.
explicitandimplicitrelevantconditionsareextracted.Eachconditionserves explainthecurrentcontextandthenexpanduponit,makingareasoned
asanaccesskeytonodesintheKG.Thisinferenceofimplicitconditions conclusionbasedonincrementallyacquiredin-contextknowledge.Sucha
enablestheKGtoproviderelevantinformationevenwhennotexplicitly techniquewascrucialforerrorhandlingandresolution,butlesscriticalfor
requested, thereby significantly enhancing the contextual understanding tasks like keyword extraction. The second strategy, aimed at structured
presentedtotheuserorusedindownstreamtasks. informationextraction,employedexplicitschemadefinitionswithexpected
keys and data types, supported by few-shot examples, ensuring that the
Largelanguagemodelintegration outputwasavalidJSONobject.TheLLM’srawoutputwasextractedusing
We employed LLMs to perform various tasks, including user-prompt regular expressions and parsed into a Python dictionary. This method
interfacingformaterialinformation,keywordextractionforKGretrieval, helpedtosecuredownstreamintegrationforAPIcallsandsystemupdates.
evaluationofQEparameters,andprocessingofQEerrormessages.Users AsdisplayedinpanelFig.9a,usercalculationpromptsareparsedto
choose the LLM based on accuracy, cost, context window length, and extractkeywordsandcalculationconditions.Thisstructuredoutputfacil-
runtimeavailability.Forinitialinterfacing,conditionextraction,andpara- itatesaccesstothreepartsoftheKGnodes.(i)Therequirednodescorre-
meter evaluation, we used mistralai/mixtral-8 × 22b- spondingtoessentialQEparametersforanycalculationareincluded.(ii)A
instruct38. For error keyword extraction, databricks/dbrx- keyword search is performed using the extracted keywords against the
instruct39 was employed. Our core protocol generation involved a knowledge graph’s raw text. Thetop70%of nodes rankedbyrelevance
hierarchical model structure with two worker models (databricks/ (cosinesimilarity)areselected.Thistextsearchutilizesahashingvectorizer
dbrx-instruct,meta-llama/llama-3.1-405b-instruct)40 (scikit-learnimplementation)with217featurestovectorizetheraw
and one referee model anthropic/claude-3.5-sonnet36. Addi- text in the knowledge graph and the query keywords. (iii) QE-specific
tionally, google/gemini-2.0-flash-00141 was used for pre- conditionsareextractedfromtheuser’sprompt.Weidentified164unique
processinguserpromptstoextractscoringmetrics.Thisframeworkvali- conditionsacrossninecategorieswithintheQEdocumentation.Theuser’s
datestheeffectivenessoftheknowledgegraphandtheautomatederror- promptisparsedtoidentifyapplicableconditionswithinthesecategories.
handlingsystem,providinginsightsintoLLMcapabilities. EachmatchedconditionactivatesrelevantKGnodes.Thenodesconnected
Weimplementedtwomainpromptengineeringstrategies.Thefirst tothecollectednodesareaddedtothefinalset.Thenodesfromthesethree
aimedtoprovidecontextualscaffoldingtotheLLM,andthesecondstrategy parts are concatenated and sent for evaluation. Each selected node (QE
focusedonextractingstructuredinformation.Thefirstisusedassubsequent parameter)isassessedbasedontheuser’spromptandcalculationcondi-
LLM inputs and for further processing, or to initiate other framework tionstodetermineanappropriatevalue.Ifaparameterisevaluatedasnon-
components.Whengeneratingtextualresponses,theLLMwasguidedto relevant,itgetsnoneasavalueandisexcluded.
CommunicationsMaterials| ( 2026) 7:115 9

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.8|ThethreepanelsillustratethestructureandinterfaceoftheQEknowledge bExampleJSONstructureforanamelistparameternode“nspin”intheknowl-
graphandhowindividualQEinputparametersareformalizedasmachine- edgegraph,showingitsattributesandinter-parameterrelationships.cExample
readablenodesandexposedthroughaninteractivegraphthatmakestheir JSONstructureforacardnode“ATOMIC_SPECIES”,illustratingitscomplex
dependenciesexplicit.aScreenshotoftheQuantumESPRESSOknowledgegraph’s syntaxandconditionaloptions.
webinterface,enablinginteractiveexplorationofnodesandtheirrelationships.
Promptdatasetandcomplexitymapping 5–8,and9ormorewerelabeledbasic,standard,andcomplex,respectively.
AsshowninFig.9b,theframeworkprovidesawebinterfaceforusersto Thecompletescoringscriptsandpromptdatasetareavailableinourpublic
submit free-form calculation prompts. Moreover, because material- repository44formoredetails.
structuregeometriescanbeinconsistentwhendirectlyextractedfromdif-
ferentmodels,weemployanagenttoretrieveandstandardizeallstructural Automatederrorhandling(AEH)
datafromthespecifieddatabasetoensurereproducibilityoftheDFTcal- Theframeworkincorporatesanautomatederror-handling(AEH)systemto
culations.Uponsubmission,thesystemparsesthetext,extractsthematerial mitigatethecriticalchallengeoftime-consumingmanualdebuggingwhen
formulaorstructure,andautomaticallyroutestherequesttotheappropriate simulationsfail.Aftergeneratingthesimulationprotocol,theQEprogramis
MaterialsClouddatabase(MC2DorMC3D)basedonwhetherthetarget executed. If the execution fails,QEgenerates a CRASH file containing a
compoundistwo-orthree-dimensional42,43.Tobenchmarktheinterface descriptiveerrormessage.AnLLMprocessesthismessagetoextractrele-
under realistic conditions, we compiled more than 400 prompts from vantkeywords,whicharethenusedtoquerythesmartKGforrelevant
independent researchers with no prior knowledge of the framework’s information. The retrieved nodes provide contextual information to the
internaldesign.Afterverifyingthateachrequestedmaterialwasavailablein LLM,whichthenattemptstoformulateasolutiontotheencounterederror.
MC2DorMC3D,weselected295promptsfortestingtheframework.We Each LLM within the hierarchical architecture is allocated a predefined
quantifiedpromptcomplexityusingascore-basedrubricinspiredbyBrown number of retries. Logs from previous unsuccessful attempts within the
et al.35. Using the google/gemini-2.0-flash-001 model, we samemodel’sretrycycleareomittedfromtheLLMinputduetotheirlength
extractedtenlinguisticanddomain-specificfeaturesfromeveryprompt; andpotentiallackofimmediateusefulness.IfanLLMusesallitsretries
eachfeaturepresentassigned+1tothetotalscore.Promptsscoring0–4, withoutresolvingtheerror,itswitchestothenextmodelinthehierarchy.
CommunicationsMaterials| ( 2026) 7:115 10

https://doi.org/10.1038/s43246-026-01167-0 Article
Fig.9|ComparisonoftheworkflowserviceJSONpayloadandthewebinterface. dashboardwrapsthesameparametersinapoint-and-clickinterface:userspastean
aSchematicoftheminimalJSONpayloadacceptedbythePOST/workflow/REST APIkey,entertheircalculationprompt,selectamodelhierarchy,andlaunchor
endpoint.Theobjectdefinesthefree-textcalculation_prompt,theordered aborttherun.Alivelogpanestreamsserver-senteventsforreal-timemonitoring.
gen_model_hierarchy,per-taskmodel_config,optionalinterface-agent Thetwoviewsillustrateparitybetweenprogrammaticandinteractivecontrolofthe
kwargs,thetargetLLMAPI,andanoptionalprojectconfiguration.bThebrowser GENIUSworkflowservice.
The subsequent model restarts the error resolution process from the Fig.9b.TheseapproachesfacilitateprogrammaticintegrationwithotherAI-
beginning,usingtheinitialoutputfromtherecommendationmoduleasits drivenapplicationswhilesupportinginteractivehumanuserexperiences.
starting point. The overall effectiveness of the AEH system is thus sig-
nificantlydependentontheclarityandinformationalcontentoftheCRASH Dataavailability
filecombinedwiththeKG,operatingwithinaself-consistentfeedbackloop. The authors confirm that the data supporting the study’s findings are
In this study, we used the QE PWSCF v.7.2package45 to validate the available in the article GitHub repository https://github.com/KIT-
simulationprotocolswedeveloped.It’simportanttonotethatthebench- Workflows/agentic-workflow-framework.
mark we set up focused on generating protocols and performing initial
validation,ratherthanafull-fledgedproductionrun.EachgeneratedQE Codeavailability
protocolwasexecutedwithinastrict60-stimelimit.Weconsideredacase Thecodesupportingthisstudy’sfindingsisavailableathttps://github.com/
successfulifthegeneratedinputcouldbeparsedandvalidatedduringthis KIT-Workflows/agentic-workflow-framework.
time without causing any crashes. This benchmark helps us determine
whether GENIUS can generate executable, coherent QE protocols from Received:30May2025;Accepted:15April2026;
open-endedprompts,ratherthanwhethereachcalculationwasfullycarried
outtoyieldscientificresults.
Logs were collected from executing the 295 curated calculation References
prompts to track the framework’s evolution. Each log file records the 1. Hafner,J.,Wolverton,C.&Ceder,G.Towardcomputationalmaterials
workflow’s terminal status (success or failure) and, for successful runs, design:theimpactofdensityfunctionaltheoryonmaterialsresearch.
includes the number of attempts and any model switches that occurred MRSBull.31,659–668(2006).
during the automated error-handling phase. The primary metric for 2. Shen,S.C.etal.Computationaldesignandmanufacturingof
assessingtheefficiencyofprotocolgenerationisthenumberofattemptsand sustainablematerialsthroughfirst-principlesandmateriomics.Chem.
model switches required to achieve a successful outcome. A zero value Rev.123,2242–2275(2023).
indicateszero-shotgeneration:theinitialprotocolgeneratedbyModel1, 3. Bock,F.E.etal.Areviewoftheapplicationofmachinelearningand
usingtherecommendationsystem’soutput,succeededonthefirstattempt dataminingapproachesincontinuummaterialsmechanics.Front.
without requiring any intervention from the AEH system. The primary Mater.6,110(2019).
requirementsarethecapabilitytointeractwithLLMproviderAPIsandto 4. CaldeiraRego,C.R.etal.SimStack:anintuitiveworkflowframework.
executetheQEprogramforprotocolvalidation.Sometools,suchasthe Front.Mater.9,877597(2022).
atomic simulation environment (ASE), scikit-learn, and net- 5. Guedes-Sobrinho,D.etal.Revealingtheimpactoforganicspacers
workx, were also used. Additional dependencies are standard Python andcavitycationsonquasi-2Dperovskitesviacomputational
libraries.TheworkflowAPIisaRESTfuldesignwritteninFastAPI, simulations.Sci.Rep.13,4446(2023).
managingtheworkflowthroughstandardizedHTTPendpoints.Oncethe 6. Yu,Z.,Singh,B.,Yu,Y.&Nazar,L.F.Suppressingargyrodite
workflowserverisinitialized,itsprimaryendpointPOST"/workflow/" oxidationbytuningthehoststructureforhigh-areal-capacityall-solid-
acceptsJSONpayloadsthatspecifycalculationparameters,modelconfig- statelithium-sulfurbatteries.Nat.Mater.24,1082–1090(2025).
urations, and optional project settings, as shown in Fig. 9a. The service 7. Lin,X.etal.Afamilyofdual-anion-basedsodiumsuperionic
providesadditionalworkflow managementthroughotherendpoints for: conductorsforall-solid-statesodium-ionbatteries.Nat.Mater.24,
Status monitoring (GET "/workflow-status/{workflow_id}"), 83–91(2024).
Resultretrieval(GET"/results/{workflow_id}"),andvisualization 8. Han,X.etal.Fastandfacilesynthesisofamidine-incorporated
access(GET"/timeline/{workflow_id}").Real-timemonitoringis degradablelipidsforversatileMRNAdeliveryinvivo.Nat.Chem.16,
enabledviaserver-sentevents(SSE)atthe/logsendpoint,asillustratedin 1687–1697(2024).
CommunicationsMaterials| ( 2026) 7:115 11

https://doi.org/10.1038/s43246-026-01167-0 Article
9. King,A.Fourwaystopower-upAIfordrugdiscovery.Nature,https:// FoundationandLargeLanguageModels(FLLM),330–338(IEEE,
doi.org/10.1038/d41586-025-00602-5(2025). 2024).
10. Schaarschmidt,J.etal.Workflowengineeringinmaterialsdesign 31. Ledger,G.&Mancinni,R.DetectingLLMhallucinationsusingMonte
withinthebattery2030+project.Adv.EnergyMater.12,2102638 Carlosimulationsontokenprobabilities.Preprintathttps://doi.org/
(2021). 10.36227/techrxiv.171822396.61518693/v1(2024).
11. Bekemeier,S.etal.Advancingdigitaltransformationinmaterial 32. Gundersen,O.E.Thefundamentalprinciplesofreproducibility.
science:theroleofworkflowswithinthematerialdigitalinitiative.Adv. Philos.Trans.R.Soc.A379,20200210(2021).
Eng.Mater.https://doi.org/10.1002/adem.202402149(2025). 33. Holbrook,J.B.Openscience,openaccess,andthedemocratization
12. Dalmedico,J.F.etal.Tuningelectronicandstructuralpropertiesof ofknowledge.IssuesSci.Technol.35,26–28(2019).
lead-freemetalhalideperovskites:acomparativestudyof2D 34. Kohonen,T.Theself-organizingmap.Proc.IEEE78,1464–1480
Ruddlesden-Popperand3Dcompositions.Chemphyschem25, (1990).
e202400118(2024). 35. Brown,T.etal.Languagemodelsarefew-shotlearners.Adv.Neural
13. Bastos,C.M.dO.etal.First-principlesstatisticalinvestigationof Inf.Process.Syst.33,1877–1901(2020).
thermodynamicbehaviorwithexcitoniceffectsinmo 1−x W x Se 2 alloys 36. Claude3.5sonnet.https://www.anthropic.com/news/claude-3-5-
throughadata-drivenworkflowapproach.J.Mater.Chem.AMater. sonnet(2024).Accessed:February,2025.
EnergySustain.13,39053–39064(2025). 37. Steck,H.,Ekanadham,C.&Kallus,N.Iscosine-similarityof
14. Mieller,B.,Valavi,M.&CaldeiraRêgo,C.R.Anautomatized embeddingsreallyaboutsimilarity?Preprintathttps://doi.org/10.
simulationworkflowforpowderpressingsimulationsusingSimStack. 48550/ARXIV.2403.05440(2024).
Adv.Eng.Mater.27,2400872(2025). 38. MistralAI.Mixtral-8×22binstruct.https://mistral.ai/news/mixtral-
15. Allison,J.,Backman,D.&Christodoulou,L.Integratedcomputational 8x22b(2024).Accessed:February,2025.
materialsengineering:anewparadigmfortheglobalmaterials 39. Databricks,I.dbrx.https://www.databricks.com/blog/introducing-
profession.Jom58,25–27(2006). dbrx-new-state-art-open-llm(2024).Accessed:February,2025.
16. Taylor,C.D.,Lu,P.,Saal,J.,Frankel,G.&Scully,J.Integrated 40. AI,M.Metallama3.1.https://ai.meta.com/blog/meta-llama-3-1/
computationalmaterialsengineeringofcorrosionresistantalloys. (2024).Accessed:February,2025.
NPJMater.Degrad.2,6(2018). 41. GoogleAI.Gemini2.0flash.https://blog.google/technology/google-
17. Lejaeghere,K.etal.Reproducibilityindensityfunctionaltheory deepmind/google-gemini-ai-update-december-2024/(2024).
calculationsofsolids.Science351,aad3000(2016). Accessed:February,2025.
18. Huber,S.P.etal.Commonworkflowsforcomputingmaterial 42. Huber,S.etal.MaterialsCloudThree-dimensionalCrystalsDatabase
propertiesusingdifferentquantumengines.NPJComput.Mater.7, (mc3d).MaterialsCloudArchive2022.38https://doi.org/10.24435/
136(2021). materialscloud:rw-t0(2022).
19. deAraujo,L.O.etal.Automatedworkflowforanalyzing 43. Campi,D.,Mounet,N.,Gibertini,M.,Pizzi,G.&Marzari,N.Expansion
thermodynamicstabilityinpolymorphicperovskitealloys.NPJ ofthematerialscloud2Ddatabase.ACSNano17,11268–11278
Comput.Mater.10,146(2024). (2023).
20. Bonacci,M.etal.Towardshigh-throughputmany-bodyperturbation 44. Soleymanibrojeni,M.&CaldeiraRego,C.R.Agentic-workflow-
theory:efficientalgorithmsandautomatedworkflows.NPJComput. framework:AI-drivenagenticframeworkforautonomoussimulation
Mater.9,74(2023). protocolgenerationandexecution.https://github.com/KIT-
21. Soleymanibrojeni,M.,CaldeiraRego,C.R.,Esmaeilpour,M.& Workflows/agentic-workflow-framework(2025).
Wenzel,W.Anactivelearningapproachtomodelsolid-electrolyte 45. QuantumESPRESSOGroup.User’sGuideforQuantumESPRESSO
interphaseformationinLi-ionbatteries.J.Mater.Chem.A12, (pw.x).QuantumESPRESSOFoundationhttps://www.quantum-
2249–2266(2024). espresso.org/Doc/pw_user_guide/(2023).Accessed:February,(2025).
22. Luke,D.A.,Powell,B.J.&Paniagua-Avila,A.Bridgesand
mechanisms:integratingsystemssciencethinkinginto Acknowledgements
implementationresearch.Annu.Rev.PublicHealth45,7–25(2024). WeacknowledgesupportbytheKITPublicationFundoftheKarlsruhe
23. Toner-Rodgers,A.Artificialintelligence,scientificdiscovery,and InstituteofTechnology.Theauthorsarealsothankfulforfinancial
productinnovation.Preprintathttps://doi.org/10.48550/arXiv.2412. supportfromtheNationalCouncilforScientificandTechnological
17866(2024). Development(CNPq,grantnumbers444431/2024-1,and444069/2024-0).
24. Jablonka,K.M.etal.14examplesofhowLLMscantransform W.W.,C.R.C.R.thanktheGermanFederalMinistryofEducationand
materialsscienceandchemistry:areflectiononalargelanguage Research(BMBF)forfinancialsupportoftheprojectInnovation-Platform
modelhackathon.Digit.Discov.2,1233–1250(2023). MaterialDigital(www.materialdigital.de)throughprojectfundingFKZ
25. Wang,Q.,Mao,Z.,Wang,B.&Guo,L.Knowledgegraphembedding: number13XP5094A.Theproject(HGFZT-I-PF-5-261GENIUS)
asurveyofapproachesandapplications.IEEETrans.Knowl.Data underlyingthispublicationis/wasfundedbytheInitiativeandNetworking
Eng.29,2724–2743(2017). FundoftheHelmholtzAssociationintheframeworkoftheHelmholtzAI
26. Lambert,N.etal.Tulu3:pushingfrontiersinopenlanguagemodel projectcall.
post-training.Preprintathttps://doi.org/10.48550/ARXIV.2411.
15124(2024). Authorcontributions
27. Guo,D.etal.DeepSeek-R1incentivizesreasoninginLLMsthrough M.S.,C.R.C.R.conceptualizedthestudy,ledthedataanalysis,preparedthe
reinforcementlearning.Nature645,633–638(2025). figures,curatedthedata,anddraftedthemanuscript.M.J.P.,A.C.D.,and
28. KimiTeametal.Kimik1.5:scalingreinforcementlearningwithLLMs. D.G.S.developedandrefinedthepromptsusedinGENIUS.C.R.C.R.,W.W.,
Preprintathttps://doi.org/10.48550/ARXIV.2501.12599(2025). andR.A.contributedtofundingacquisition,projectdesign,andscientific
29. Giannozzi,P.etal.Quantumespresso:amodularandopen-source supervision.Allauthorscontributedtothewriting,review,andrevisionofthe
softwareprojectforquantumsimulationsofmaterials.J.Phys. manuscript.
Condens.Matter21,395502(2009).
30. Michelutti,C.,Eckert,J.,Monecke,M.,Klein,J.&Glesner,S.A Funding
systematicstudyonthepotentialsandlimitationsofLLM-assisted OpenAccessfundingenabledandorganizedbyProjektDEAL.
softwaredevelopment.InProc.20242ndInternationalConferenceon
CommunicationsMaterials| ( 2026) 7:115 12

https://doi.org/10.1038/s43246-026-01167-0 Article
Competinginterests OpenAccessThisarticleislicensedunderaCreativeCommons
Theauthorsdeclarenocompetinginterests. Attribution4.0InternationalLicense,whichpermitsuse,sharing,
adaptation,distributionandreproductioninanymediumorformat,aslong
asyougiveappropriatecredittotheoriginalauthor(s)andthesource,
Additionalinformation
providealinktotheCreativeCommonslicence,andindicateifchanges
Correspondenceandrequestsformaterialsshouldbeaddressedto weremade.Theimagesorotherthirdpartymaterialinthisarticleare
CelsoRicardoCaldeiraRêgo. includedinthearticle’sCreativeCommonslicence,unlessindicated
otherwiseinacreditlinetothematerial.Ifmaterialisnotincludedinthe
PeerreviewinformationCommunicationsMaterialsthanksMassimiliano article’sCreativeCommonslicenceandyourintendeduseisnotpermitted
LupoPasini,SandraDiaz-Pierandtheotheranonymousreviewer(s)fortheir bystatutoryregulationorexceedsthepermitteduse,youwillneedto
contributiontothepeerreviewofthiswork.Apeerreviewfileisavailable. obtainpermissiondirectlyfromthecopyrightholder.Toviewacopyofthis
licence,visithttp://creativecommons.org/licenses/by/4.0/.
Reprintsandpermissionsinformationisavailableat
http://www.nature.com/reprints ©TheAuthor(s)2026
Publisher’snoteSpringerNatureremainsneutralwithregardtojurisdictional
claimsinpublishedmapsandinstitutionalaffiliations.
CommunicationsMaterials| ( 2026) 7:115 13