import ROOT
import os
from datetime import datetime
if not os.path.exists('BiasPlot'):
  os.makedirs('BiasPlot')
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so");
ROOT.gROOT.SetBatch(True)
cats = ['vbf']
order = [1,1,1,1]
outfile = open('BiasStudy.txt','a', buffering=0) 
outfile.write("%s\n"%str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

bkgfile = ROOT.TFile('CMS_Hemu_13TeV_multipdf.root')
bkgWS = bkgfile.Get('multipdf')
#outRoot = ROOT.TFile("hist_bias_study.root","RECREATE")
for cat in cats:
  multipdf = bkgWS.pdf('CMS_hemu_'+cat+'_13TeV_bkgshape')
  numofpdfcat = multipdf.getNumPdfs()
  print "Total number of cats: ", numofpdfcat
  for i in range(numofpdfcat):
    pdfname = multipdf.getPdf(i).GetName()
    split_string = pdfname.split("_")
    if 'bern' in pdfname and not 'bern%i'%order[0] in pdfname: continue
    if 'exp' in pdfname and not 'exp%i'%order[1] in pdfname: continue
    if 'lau' in pdfname and not 'lau%i'%order[2] in pdfname: continue
    if 'pow' in pdfname and not 'pow%i'%order[3] in pdfname: continue
    for j in range(numofpdfcat):
      pdfname2 = multipdf.getPdf(j).GetName()
      split_string2 = pdfname2.split("_")
      print "Scanning fitDiagnosticsGen"+split_string[3]+"Fit"+split_string2[3]+".root"
      file_ = ROOT.TFile("fitDiagnosticsGen"+split_string[3]+"Fit"+split_string2[3]+".root")
      tree = file_.Get("tree_fit_sb")
      if not tree: continue
      tree.Draw("(r-1)/(0.5*(rHiErr+rLoErr))>>h(100,-5,5)")
      h = ROOT.gPad.GetPrimitive("h")
      h.SetTitle(cat+" Gen "+split_string[3]+" - Fit "+split_string2[3]+";Pull;");
      h.SetName('%sGen%sFit%s'%(cat,split_string[3],split_string2[3]))
      ROOT.gPad.SaveAs('BiasPlot/%sGen%sFit%s.png'%(cat,split_string[3],split_string2[3]))
#      h.Write()
#      print "Mean of bias of "+cat+" for pdf "+split_string[3]+" generated with pdf "+split_string2[3], h.GetMean()
#      print "Standard Deviation of bias", h.GetStdDev()
      outfile.write(cat + " " + split_string[3] + " " + split_string2[3] +" "+ str(round(h.GetMean()*100,3)) + " " + str(round(h.GetStdDev(),3)) + "\n")
      file_.Close()
outfile.close()
#outRoot.Close()
