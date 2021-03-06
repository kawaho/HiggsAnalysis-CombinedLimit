import ROOT
import os
from datetime import datetime
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so");
ROOT.gROOT.SetBatch(True)
cat = 'ggcat4'
order = [1,1,1,1]

def run(cmd):
  print "%s\n\n"%cmd
  os.system(cmd)

bkgfile = ROOT.TFile('CMS_Hemu_13TeV_multipdf.root')
bkgWS = bkgfile.Get('multipdf')
multipdf = bkgWS.pdf('CMS_hemu_'+cat+'_13TeV_bkgshape')
numofpdfcat = multipdf.getNumPdfs()
for i in range(numofpdfcat):
  pdfname = multipdf.getPdf(i).GetName()
  split_string = pdfname.split("_")
  if 'bern' in pdfname and not 'bern%i'%order[0] in pdfname: continue
  if 'exp' in pdfname and not 'exp%i'%order[1] in pdfname: continue
  if 'lau' in pdfname and not 'lau%i'%order[2] in pdfname: continue
  if 'pow' in pdfname and not 'pow%i'%order[3] in pdfname: continue
  Gen = "combine datacard_" + cat + "_NoSys.txt -M GenerateOnly --setParameters pdfindex_" + cat + "_13TeV="+str(i)+" --toysNoSystematics -t 10000 --expectSignal 1 --saveToys -m 125 --freezeParameters pdfindex_" + cat + "_13TeV --name "+split_string[3]
  run(Gen)
  for j in range(numofpdfcat):
    pdfname2 = multipdf.getPdf(j).GetName()
    split_string2 = pdfname2.split("_")
    Fit = "combineTool.py --job-mode condor --sub-opts=\'+JobFlavour=\"espresso\"\' --task-name Gen"+split_string[3]+"Fit"+split_string2[3] + " datacard_" + cat + "_NoSys.txt -M FitDiagnostics --setParameters pdfindex_" + cat +"_13TeV="+str(j)+" --toysFile higgsCombine"+split_string[3]+".GenerateOnly.mH125.123456.root  -t 10000 -m 125 --rMin -5 --rMax 5 --freezeParameters pdfindex_" + cat + "_13TeV --cminDefaultMinimizerStrategy=0 -v 3 --name Gen"+split_string[3]+"Fit"+split_string2[3]
    run(Fit) 
