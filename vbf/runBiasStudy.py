import ROOT
import os
from datetime import datetime
if not os.path.exists('BiasPlot'):
  os.makedirs('BiasPlot')
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so");
ROOT.gROOT.SetBatch(True)
cats = ['vbf']
order = {
'ggcat0':[1,1,2,1],
'ggcat1EC':[2,1,2,1],
'ggcat2EC':[1,1,1,1],
'ggcat1B':[2,1,2,1],
'ggcat2B':[1,1,1,1],
'ggcat3':[1,1,1,1],
'vbf':[1,1,1,1]
}
outfile = open('BiasStudy.txt','a', buffering=0) 
outfile.write("%s\n"%str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def run(cmd):
  print "%s\n\n"%cmd
  os.system(cmd)

bkgfile = ROOT.TFile('CMS_Hemu_13TeV_multipdf.root')
bkgWS = bkgfile.Get('multipdf')
outRoot = ROOT.TFile("hist_bias_study.root","RECREATE")
for cat in cats:
  multipdf = bkgWS.pdf('CMS_hemu_'+cat+'_13TeV_bkgshape')
  numofpdfcat = multipdf.getNumPdfs()
  print "Total number of cats: ", numofpdfcat
  goodpdf = [True]*numofpdfcat
  for i in range(numofpdfcat):
    pdfname = multipdf.getPdf(i).GetName()
    split_string = pdfname.split("_")
    if 'bern' in pdfname and not 'bern%i'%order[cat][0] in pdfname: continue
    if 'exp' in pdfname and not 'exp%i'%order[cat][1] in pdfname: continue
    if 'lau' in pdfname and not 'lau%i'%order[cat][2] in pdfname: continue
    if 'pow' in pdfname and not 'pow%i'%order[cat][3] in pdfname: continue
    Gen = "combine datacard_" + cat + "_NoSys.txt -M GenerateOnly --setParameters pdfindex_" + cat + "_13TeV="+str(i)+" --toysNoSystematics -t 10000 --expectSignal 1 --saveToys -m 125 --freezeParameters pdfindex_" + cat + "_13TeV"
    print "Generating MC for "+cat+" with %s"%(split_string[3])
    run(Gen)
    for j in range(numofpdfcat):
      if goodpdf[j] == False: continue
      pdfname2 = multipdf.getPdf(j).GetName()
      split_string2 = pdfname2.split("_")
      Fit = "combine datacard_" + cat + "_NoSys.txt -M FitDiagnostics --setParameters pdfindex_" + cat +"_13TeV="+str(j)+" --toysFile higgsCombineTest.GenerateOnly.mH125.123456.root  -t 10000 -m 125 --rMin -5 --rMax 5 --freezeParameters pdfindex_" + cat + "_13TeV --cminDefaultMinimizerStrategy=0 -v 3"
      print "Fitting MC generated with pdf "+ split_string[3] +" for "+cat+" with pdf "+ split_string2[3] +"....."
      run(Fit) 
      file_ = ROOT.TFile("fitDiagnostics.root")
      tree = file_.Get("tree_fit_sb")
      tree.Draw("(r-1)/(0.5*(rHiErr+rLoErr))>>h(100,-5,5)")
      h = ROOT.gPad.GetPrimitive("h")
      h.SetTitle(cat+" Gen "+split_string[3]+" - Fit "+split_string2[3]+";Pull;");
      h.SetName('%sGen%sFit%s'%(cat,split_string[3],split_string2[3]))
      ROOT.gPad.SaveAs('BiasPlot/%sGen%sFit%s.png'%(cat,split_string[3],split_string2[3]))
      h.Write()
      print "Mean of bias of "+cat+" for pdf "+split_string[3]+" generated with pdf "+split_string2[3], h.GetMean()
      print "Standard Deviation of bias", h.GetStdDev()
      outfile.write(cat + " " + split_string[3] + " " + split_string2[3] +" "+ str(round(h.GetMean()*100,3)) + " " + str(round(h.GetStdDev(),3)) + "\n")
      if abs(h.GetMean()*100) > 14:
        goodpdf[j] = False
outfile.close()
outRoot.Close()
