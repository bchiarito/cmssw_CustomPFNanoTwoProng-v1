import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy
from PhysicsTools.NanoAOD.common_cff import *
from math import ceil,log

from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy
from Configuration.Eras.Modifier_run2_nanoAOD_94XMiniAODv1_cff import run2_nanoAOD_94XMiniAODv1
from Configuration.Eras.Modifier_run2_nanoAOD_94XMiniAODv2_cff import run2_nanoAOD_94XMiniAODv2
from Configuration.Eras.Modifier_run2_nanoAOD_94X2016_cff import run2_nanoAOD_94X2016
from Configuration.Eras.Modifier_run2_nanoAOD_102Xv1_cff import run2_nanoAOD_102Xv1

photon_id_modules_WorkingPoints_nanoAOD = cms.PSet(
    modules = cms.vstring(
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V1_TrueVtx_cff',
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Fall17_94X_V2_cff',
        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V1p1_cff',
        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Fall17_94X_V2_cff',
   ),
   WorkingPoints = cms.vstring(
    "egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-loose",
    "egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-medium",
    "egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-tight",
   )
)
run2_miniAOD_80XLegacy.toModify(photon_id_modules_WorkingPoints_nanoAOD,
    modules = cms.vstring(
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff',
        'RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_Spring16_nonTrig_V1_cff',
   ),
   WorkingPoints = cms.vstring(
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose",
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium",
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight",
   )
)
run2_nanoAOD_94X2016.toModify(photon_id_modules_WorkingPoints_nanoAOD,
    modules = cms.vstring(
        'RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff',
   ),
   WorkingPoints = cms.vstring(
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose",
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium",
    "egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight",
   )
)


_bitmapVIDForPho_docstring = ''
for modname in photon_id_modules_WorkingPoints_nanoAOD.modules:
    ids= __import__(modname, globals(), locals(), ['idName','cutFlow'])
    for name in dir(ids):
        _id = getattr(ids,name)
        if hasattr(_id,'idName') and hasattr(_id,'cutFlow'):
            if (len(photon_id_modules_WorkingPoints_nanoAOD.WorkingPoints)>0 and _id.idName==photon_id_modules_WorkingPoints_nanoAOD.WorkingPoints[0].split(':')[-1]):
                _bitmapVIDForPho_docstring = 'VID compressed bitmap (%s), %d bits per cut'%(','.join([cut.cutName.value() for cut in _id.cutFlow]),int(ceil(log(len(photon_id_modules_WorkingPoints_nanoAOD.WorkingPoints)+1,2))))

bitmapVIDForPho = cms.EDProducer("PhoVIDNestedWPBitmapProducer",
    src = cms.InputTag("slimmedPhotons"),
    WorkingPoints = photon_id_modules_WorkingPoints_nanoAOD.WorkingPoints,
)

isoForPho = cms.EDProducer("PhoIsoValueMapProducer",
    src = cms.InputTag("slimmedPhotons"),
    relative = cms.bool(False),
    rho_PFIso = cms.InputTag("fixedGridRhoFastjetAll"),
    mapIsoChg = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
    mapIsoNeu = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
    mapIsoPho = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
    EAFile_PFIso_Chg = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfChargedHadrons_90percentBased_V2.txt"),
    EAFile_PFIso_Neu = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfNeutralHadrons_90percentBased_V2.txt"),
    EAFile_PFIso_Pho = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Fall17/effAreaPhotons_cone03_pfPhotons_90percentBased_V2.txt"),
)
for modifier in run2_miniAOD_80XLegacy, run2_nanoAOD_94X2016:
    modifier.toModify(isoForPho,
        EAFile_PFIso_Chg = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfChargedHadrons_90percentBased.txt"),
        EAFile_PFIso_Neu = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfNeutralHadrons_90percentBased.txt"),
        EAFile_PFIso_Pho = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring16/effAreaPhotons_cone03_pfPhotons_90percentBased.txt"),
    )

seedGainPho = cms.EDProducer("PhotonSeedGainProducer", src = cms.InputTag("slimmedPhotons"))

import RecoEgamma.EgammaTools.calibratedEgammas_cff
calibratedPatPhotons102Xv1 = RecoEgamma.EgammaTools.calibratedEgammas_cff.calibratedPatPhotons.clone(
    produceCalibratedObjs = False,
    correctionFile = cms.string("EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2018_Step2Closure_CoarseEtaR9Gain_v2")
)

calibratedPatPhotons94Xv1 = RecoEgamma.EgammaTools.calibratedEgammas_cff.calibratedPatPhotons.clone(
    produceCalibratedObjs = False,
    correctionFile = cms.string("EgammaAnalysis/ElectronTools/data/ScalesSmearings/Run2017_17Nov2017_v1_ele_unc")
)

calibratedPatPhotons80XLegacy = RecoEgamma.EgammaTools.calibratedEgammas_cff.calibratedPatPhotons.clone(
    produceCalibratedObjs = False,
    correctionFile = cms.string("EgammaAnalysis/ElectronTools/data/ScalesSmearings/Legacy2016_07Aug2017_FineEtaR9_v3_ele_unc"),
)

slimmedPhotonsWithUserData = cms.EDProducer("PATPhotonUserDataEmbedder",
    src = cms.InputTag("slimmedPhotons"),
    userFloats = cms.PSet(
        mvaID = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v2Values"),
        mvaIDV1 = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v1p1Values"),
        PFIsoChg = cms.InputTag("isoForPho:PFIsoChg"),
        PFIsoAll = cms.InputTag("isoForPho:PFIsoAll"),
    ),
    userIntFromBools = cms.PSet(
        cutbasedID_loose = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-loose"),
        cutbasedID_medium = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-medium"),
        cutbasedID_tight = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V2-tight"),
        mvaID_WP90 = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v2-wp90"),
        mvaID_WP80 = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v2-wp80"),
        cutbasedIDV1_loose = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-loose"),
        cutbasedIDV1_medium = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-medium"),
        cutbasedIDV1_tight = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Fall17-94X-V1-tight"),
        mvaIDV1_WP90 = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v1p1-wp90"),
        mvaIDV1_WP80 = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v1p1-wp80"),
    ),
    userInts = cms.PSet(
        VIDNestedWPBitmap = cms.InputTag("bitmapVIDForPho"),
        seedGain = cms.InputTag("seedGainPho"),
    ),
)
run2_miniAOD_80XLegacy.toModify(slimmedPhotonsWithUserData.userFloats,
    mvaID = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRun2Spring16NonTrigV1Values"),
    mvaIDV1 = None,
)
run2_miniAOD_80XLegacy.toModify(slimmedPhotonsWithUserData.userIntFromBools,
    cutbasedID_loose = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose"),
    cutbasedID_medium = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium"),
    cutbasedID_tight = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight"),
    mvaID_WP90 = cms.InputTag("egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp90"),
    mvaID_WP80 = cms.InputTag("egmPhotonIDs:mvaPhoID-Spring16-nonTrig-V1-wp80"),
    cutbasedIDV1_loose = None,
    cutbasedIDV1_medium = None,
    cutbasedIDV1_tight = None,
    mvaIDV1_WP90 = None,
    mvaIDV1_WP80 = None,
)
run2_nanoAOD_94X2016.toModify(slimmedPhotonsWithUserData.userFloats,
    mvaID = None,
    mvaIDV1 = None,
)
run2_nanoAOD_94X2016.toModify(slimmedPhotonsWithUserData.userIntFromBools,
    cutbasedID_loose = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose"),
    cutbasedID_medium = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium"),
    cutbasedID_tight = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight"),
    mvaID_WP90 = None,
    mvaID_WP80 = None,
    cutbasedIDV1_loose = None,
    cutbasedIDV1_medium = None,
    cutbasedIDV1_tight = None,
    mvaIDV1_WP90 = None,
    mvaIDV1_WP80 = None,
)

run2_miniAOD_80XLegacy.toModify(slimmedPhotonsWithUserData.userFloats,
    ecalEnergyErrPostCorrNew = cms.InputTag("calibratedPatPhotons80XLegacy","ecalEnergyErrPostCorr"),
    ecalEnergyPreCorrNew     = cms.InputTag("calibratedPatPhotons80XLegacy","ecalEnergyPreCorr"),
    ecalEnergyPostCorrNew    = cms.InputTag("calibratedPatPhotons80XLegacy","ecalEnergyPostCorr"),
)
run2_nanoAOD_94XMiniAODv1.toModify(slimmedPhotonsWithUserData.userFloats,
    ecalEnergyErrPostCorrNew = cms.InputTag("calibratedPatPhotons94Xv1","ecalEnergyErrPostCorr"),
    ecalEnergyPreCorrNew     = cms.InputTag("calibratedPatPhotons94Xv1","ecalEnergyPreCorr"),
    ecalEnergyPostCorrNew    = cms.InputTag("calibratedPatPhotons94Xv1","ecalEnergyPostCorr"),
)
run2_nanoAOD_102Xv1.toModify(slimmedPhotonsWithUserData.userFloats,
    ecalEnergyErrPostCorrNew = cms.InputTag("calibratedPatPhotons102Xv1","ecalEnergyErrPostCorr"),
    ecalEnergyPreCorrNew     = cms.InputTag("calibratedPatPhotons102Xv1","ecalEnergyPreCorr"),
    ecalEnergyPostCorrNew    = cms.InputTag("calibratedPatPhotons102Xv1","ecalEnergyPostCorr"),
)

finalPhotons = cms.EDFilter("PATPhotonRefSelector",
    src = cms.InputTag("slimmedPhotonsWithUserData"),
    cut = cms.string("pt > 5 ")
)

photonTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("linkedObjects","photons"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name= cms.string("Photon"),
    doc = cms.string("slimmedPhotons after basic selection (" + finalPhotons.cut.value()+")"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the photons
    variables = cms.PSet(CandVars,
        jetIdx = Var("?hasUserCand('jet')?userCand('jet').key():-1", int, doc="index of the associated jet (-1 if none)"),
        electronIdx = Var("?hasUserCand('electron')?userCand('electron').key():-1", int, doc="index of the associated electron (-1 if none)"),
        energyErr = Var("getCorrectedEnergyError('regression2')",float,doc="energy error of the cluster from regression",precision=6),
        r9 = Var("full5x5_r9()",float,doc="R9 of the supercluster, calculated with full 5x5 region",precision=10),
        sieie = Var("full5x5_sigmaIetaIeta()",float,doc="sigma_IetaIeta of the supercluster, calculated with full 5x5 region",precision=10),
        cutBasedBitmap = Var("userInt('cutbasedID_loose')+2*userInt('cutbasedID_medium')+4*userInt('cutbasedID_tight')",int,doc="cut-based ID bitmap, 2^(0:loose, 1:medium, 2:tight)"),
        cutBasedV1Bitmap = Var("userInt('cutbasedIDV1_loose')+2*userInt('cutbasedIDV1_medium')+4*userInt('cutbasedIDV1_tight')",int,doc="cut-based ID bitmap, Fall17 V1, 2^(0:loose, 1:medium, 2:tight)"),
        vidNestedWPBitmap = Var("userInt('VIDNestedWPBitmap')",int,doc=_bitmapVIDForPho_docstring),
        electronVeto = Var("passElectronVeto()",bool,doc="pass electron veto"),
        pixelSeed = Var("hasPixelSeed()",bool,doc="has pixel seed"),
        mvaID = Var("userFloat('mvaID')",float,doc="MVA ID score",precision=10),
        mvaIDV1 = Var("userFloat('mvaIDV1')",float,doc="MVA ID score, Fall17 V1p1",precision=10),
        mvaID_WP90 = Var("userInt('mvaID_WP90')",bool,doc="MVA ID WP90"),
        mvaID_WP80 = Var("userInt('mvaID_WP80')",bool,doc="MVA ID WP80"),
        pfRelIso03_chg = Var("userFloat('PFIsoChg')/pt",float,doc="PF relative isolation dR=0.3, charged component (with rho*EA PU corrections)"),
        pfRelIso03_all = Var("userFloat('PFIsoAll')/pt",float,doc="PF relative isolation dR=0.3, total (with rho*EA PU corrections)"),
        hoe = Var("hadronicOverEm()",float,doc="H over E",precision=8),
        isScEtaEB = Var("abs(superCluster().eta()) < 1.4442",bool,doc="is supercluster eta within barrel acceptance"),
        isScEtaEE = Var("abs(superCluster().eta()) > 1.566 && abs(superCluster().eta()) < 2.5",bool,doc="is supercluster eta within endcap acceptance"),
        seedGain = Var("userInt('seedGain')","uint8",doc="Gain of the seed crystal"),
        ### ADDED ###
        hadTowOverEm = Var("hadTowOverEm()",float,doc="hadTowOverEm()"),
        chargedHadronIso = Var("chargedHadronIso()",float,doc="chargedHadronIso()"),
        photonIso = Var("photonIso()",float,doc="photonIso()"),
        scEta = Var("superCluster().eta()",float,doc="superCluster()->eta()"),
        #############
    )
)

#these eras have the energy correction in the mini
for modifier in run2_nanoAOD_94XMiniAODv2, run2_nanoAOD_94X2016:
    modifier.toModify(photonTable.variables,
        pt = Var("pt*userFloat('ecalEnergyPostCorr')/userFloat('ecalEnergyPreCorr')", float, precision=-1, doc="p_{T}"),
        energyErr = Var("userFloat('ecalEnergyErrPostCorr')",float,doc="energy error of the cluster from regression",precision=6),
        eCorr = Var("userFloat('ecalEnergyPostCorr')/userFloat('ecalEnergyPreCorr')",float,doc="ratio of the calibrated energy/miniaod energy"),
    )

#these eras need to make the energy correction, hence the "New"
for modifier in run2_nanoAOD_94XMiniAODv1, run2_miniAOD_80XLegacy, run2_nanoAOD_102Xv1:
    modifier.toModify(photonTable.variables,
        pt = Var("pt*userFloat('ecalEnergyPostCorrNew')/userFloat('ecalEnergyPreCorrNew')", float, precision=-1, doc="p_{T}"),
        energyErr = Var("userFloat('ecalEnergyErrPostCorrNew')",float,doc="energy error of the cluster from regression",precision=6),
        eCorr = Var("userFloat('ecalEnergyPostCorrNew')/userFloat('ecalEnergyPreCorrNew')",float,doc="ratio of the calibrated energy/miniaod energy"),
    )


run2_nanoAOD_94X2016.toModify(photonTable.variables,
    cutBasedBitmap = None,
    cutBasedV1Bitmap = None,
    cutBased = Var("userInt('cutbasedID_loose')+userInt('cutbasedID_medium')+userInt('cutbasedID_tight')",int,doc="cut-based Spring16-V2p2 ID (0:fail, 1::loose, 2:medium, 3:tight)"),
    cutBased17Bitmap = Var("photonID('cutBasedPhotonID-Fall17-94X-V1-loose')+2*photonID('cutBasedPhotonID-Fall17-94X-V1-medium')+4*photonID('cutBasedPhotonID-Fall17-94X-V1-tight')",int,doc="cut-based Fall17-94X-V1 ID bitmap, 2^(0:loose, 1:medium, 2:tight)"),
    mvaID = Var("userFloat('PhotonMVAEstimatorRun2Spring16NonTrigV1Values')",float,doc="MVA Spring16NonTrigV1 ID score",precision=10),
    mvaIDV1 = None,
    mvaID17 = Var("userFloat('PhotonMVAEstimatorRunIIFall17v1p1Values')",float,doc="MVA Fall17v1p1 ID score",precision=10),
    mvaID_WP90 = Var("photonID('mvaPhoID-Spring16-nonTrig-V1-wp80')",bool,doc="MVA Spring16NonTrigV1 ID WP90"),
    mvaID_WP80 = Var("photonID('mvaPhoID-Spring16-nonTrig-V1-wp90')",bool,doc="MVA Spring16NonTrigV1 ID WP80"),
    mvaID17_WP90 = Var("photonID('mvaPhoID-RunIIFall17-v1p1-wp90')",bool,doc="MVA Fall17v1p1 ID WP90"),
    mvaID17_WP80 = Var("photonID('mvaPhoID-RunIIFall17-v1p1-wp80')",bool,doc="MVA Fall17v1p1 ID WP80"),
)
run2_miniAOD_80XLegacy.toModify(photonTable.variables,
    cutBasedBitmap = None,
    cutBasedV1Bitmap = None,
    mvaIDV1 = None,
    cutBased = Var("userInt('cutbasedID_loose')+userInt('cutbasedID_medium')+userInt('cutbasedID_tight')",int,doc="cut-based ID (0:fail, 1::loose, 2:medium, 3:tight)"),
)


photonsMCMatchForTable = cms.EDProducer("MCMatcher",  # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src         = photonTable.src,                 # final reco collection
    matched     = cms.InputTag("finalGenParticles"), # final mc-truth particle collection
    mcPdgId     = cms.vint32(11,22),                 # one or more PDG ID (11 = el, 22 = pho); absolute values (see below)
    checkCharge = cms.bool(False),              # True = require RECO and MC objects to have the same charge
    mcStatus    = cms.vint32(1),                # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
    maxDeltaR   = cms.double(0.3),              # Minimum deltaR for the match
    maxDPtRel   = cms.double(0.5),              # Minimum deltaPt/Pt for the match
    resolveAmbiguities    = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True),    # False = just match input in order; True = pick lowest deltaR pair first
)

photonMCTable = cms.EDProducer("CandMCMatchTableProducer",
    src     = photonTable.src,
    mcMap   = cms.InputTag("photonsMCMatchForTable"),
    objName = photonTable.name,
    objType = photonTable.name, #cms.string("Photon"),
    branchName = cms.string("genPart"),
    docString = cms.string("MC matching to status==1 photons or electrons"),
)

from RecoEgamma.EgammaTools.egammaObjectModificationsInMiniAOD_cff import egamma8XObjectUpdateModifier,egamma9X105XUpdateModifier,prependEgamma8XObjectUpdateModifier
#we have dataformat changes to 106X so to read older releases we use egamma updators
slimmedPhotonsTo106X = cms.EDProducer("ModifiedPhotonProducer",
    src = cms.InputTag("slimmedPhotons"),
    modifierConfig = cms.PSet( modifications = cms.VPSet(egamma9X105XUpdateModifier) )
)
#might as well fix 80X while we're at it although the differences are not so relavent for nano
run2_miniAOD_80XLegacy.toModify( slimmedPhotonsTo106X.modifierConfig.modifications, prependEgamma8XObjectUpdateModifier )

for modifier in run2_miniAOD_80XLegacy,run2_nanoAOD_94XMiniAODv1,run2_nanoAOD_94XMiniAODv2,run2_nanoAOD_94X2016 ,run2_nanoAOD_102Xv1:
    modifier.toModify(bitmapVIDForPho, src = "slimmedPhotonsTo106X")
    modifier.toModify(isoForPho, src = "slimmedPhotonsTo106X")
    modifier.toModify(calibratedPatPhotons102Xv1, src = "slimmedPhotonsTo106X")
    modifier.toModify(calibratedPatPhotons94Xv1, src = "slimmedPhotonsTo106X")
    modifier.toModify(calibratedPatPhotons80XLegacy, src = "slimmedPhotonsTo106X")
    modifier.toModify(slimmedPhotonsWithUserData, src = "slimmedPhotonsTo106X")
    modifier.toModify(seedGainPho, src = "slimmedPhotonsTo106X")



photonSequence = cms.Sequence(bitmapVIDForPho + isoForPho + seedGainPho + slimmedPhotonsWithUserData + finalPhotons)

photonTables = cms.Sequence ( photonTable)
photonMC = cms.Sequence(photonsMCMatchForTable + photonMCTable)

from RecoEgamma.EgammaIsolationAlgos.egmPhotonIsolationMiniAOD_cff import egmPhotonIsolation
from RecoEgamma.PhotonIdentification.photonIDValueMapProducer_cff import photonIDValueMapProducer
_updatePhoTo106X_sequence =cms.Sequence(egmPhotonIsolation + photonIDValueMapProducer + slimmedPhotonsTo106X)
_withUpdatePho_sequence = photonSequence.copy()
_withUpdatePho_sequence.insert(0,_updatePhoTo106X_sequence)
for modifier in run2_nanoAOD_94XMiniAODv2,run2_nanoAOD_94X2016 ,run2_nanoAOD_102Xv1:
    modifier.toReplaceWith(photonSequence, _withUpdatePho_sequence)

_with80XScale_sequence = _withUpdatePho_sequence.copy()
_with80XScale_sequence.replace(slimmedPhotonsWithUserData, calibratedPatPhotons80XLegacy  + slimmedPhotonsWithUserData)
run2_miniAOD_80XLegacy.toReplaceWith(photonSequence, _with80XScale_sequence)

_with94Xv1Scale_sequence = _withUpdatePho_sequence.copy()
_with94Xv1Scale_sequence.replace(slimmedPhotonsWithUserData, calibratedPatPhotons94Xv1 + slimmedPhotonsWithUserData)
run2_nanoAOD_94XMiniAODv1.toReplaceWith(photonSequence, _with94Xv1Scale_sequence)

_with102Xv1Scale_sequence = photonSequence.copy()
_with102Xv1Scale_sequence.replace(slimmedPhotonsWithUserData, calibratedPatPhotons102Xv1 + slimmedPhotonsWithUserData)
run2_nanoAOD_102Xv1.toReplaceWith(photonSequence, _with102Xv1Scale_sequence)
