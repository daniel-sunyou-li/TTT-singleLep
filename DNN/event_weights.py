import numpy as np
import ROOT
import config

year = "17"
step2Dir = "FWLJMET106XUL_1lep20{}_3t_deepJetV1_step2".format( year )

event_count = {}

weight_vars = [
  "triggerXSF", "pileupWeight", "lepIdSF", "EGammaGsfSF", "isoSF", "L1NonPrefiringProb_CommonCalc", "MCWeight_MultiLepCalc", "xsecEff", "tthfWeight", "btagDeepJetWeight", "btagDeepJet2DWeight_HTnj"
]

ROOT.gInterpreter.Declare("""
float compute_weight( float triggerXSF, float pileupWeight, float lepIdSF, float isoSF, float L1NonPrefiringProb_CommonCalc, float MCWeight_MultiLepCalc, float xsecEff, float tthfWeight, float btagDeepJetWeight, float btagDeepJet2DWeight_HTnj ){
  return triggerXSF * pileupWeight * lepIdSF * isoSF * L1NonPrefiringProb_CommonCalc * ( MCWeight_MultiLepCalc / abs( MCWeight_MultiLepCalc ) ) * xsecEff * tthfWeight * btagDeepJetWeight * btagDeepJet2DWeight_HTnj;
}
""")

for sample in config.sig_training[ year ] + config.bkg_training[ year ]:
  rDF = ROOT.RDataFrame( "ljmet", "root://cmsxrootd.fnal.gov//store/user/dsunyou/{}/nominal/{}".format( step2Dir, sample ) )
  event_count[ sample ] = { "NORMAL": 0, "WEIGHTED": 0 }
  rDF_filt = rDF.Filter( "isTraining == 1 && DataPastTriggerX == 1 && MCPastTriggerX == 1 && ( isElectron == 1 || isMuon == 1 ) && leptonPt_MultiLepCalc > 20 && NJetsCSV_JetSubCalc >= 2 && NJets_JetSubCalc >= 5 && AK4HT > 350 && corr_met_MultiLepCalc > 30 && minDR_lepJet > 0.4" )
  print( ">> Calculating weights for {} ({}/{} passed events)".format( sample, rDF_filt.Count().GetValue(), rDF.Count().GetValue() ) )
  rDF_weight = rDF_filt.Define( "event_weight", "compute_weight( triggerXSF, pileupWeight, lepIdSF, isoSF, L1NonPrefiringProb_CommonCalc, MCWeight_MultiLepCalc, xsecEff, tthfWeight, btagDeepJetWeight, btagDeepJet2DWeight_HTnj )" )
  event_count[ sample ] = {
    "NORMAL": rDF_weight.Count().GetValue(),
    "WEIGHTED": rDF_weight.Sum( "event_weight" ).GetValue()
  }

min_factor = 1e6
for sample in event_count:
  factor = float( event_count[ sample ][ "NORMAL" ] ) / float( event_count[ sample ][ "WEIGHTED" ] )
  print( "{}: Normal = {}, Weighted = {:.0f}, Factor = {:.2f}".format( sample, event_count[ sample ][ "NORMAL" ], event_count[ sample ][ "WEIGHTED" ], factor ) )
  if factor < min_factor: min_factor = factor

print( ">> Minimum factor is {:.3f}".format( min_factor ) )
