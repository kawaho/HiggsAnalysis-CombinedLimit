combineCards.py Name1=datacard_ggcat0.txt Name2=datacard_ggcat1.txt Name3=datacard_ggcat2.txt Name4=datacard_ggcat3.txt Name5=datacard_vbf.txt Name6=datacard_ggcat4.txt > datacard_comb.txt

combine -M AsymptoticLimits -m 125 datacard_ggcat0.txt --run blind #--freezeParameters pdfindex_ggcat0_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.ggcat0.mH125.root

combine -M AsymptoticLimits -m 125 datacard_ggcat1.txt --run blind #--freezeParameters pdfindex_ggcat1_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.ggcat1.mH125.root

combine -M AsymptoticLimits -m 125 datacard_ggcat2.txt --run blind #--freezeParameters pdfindex_ggcat2_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.ggcat2.mH125.root

combine -M AsymptoticLimits -m 125 datacard_ggcat3.txt --run blind #--freezeParameters pdfindex_ggcat1_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.ggcat3.mH125.root

combine -M AsymptoticLimits -m 125 datacard_ggcat4.txt --run blind #--freezeParameters pdfindex_ggcat3_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.ggcat4.mH125.root

combine -M AsymptoticLimits -m 125 datacard_vbf.txt --run blind #--freezeParameters pdfindex_vbf_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.vbf.mH125.root

combine -M AsymptoticLimits -m 125 datacard_comb.txt --run blind #--freezeParameters pdfindex_ggcat0_13TeV,pdfindex_ggcat1_13TeV,pdfindex_ggcat2_13TeV,pdfindex_ggcat3_13TeV,pdfindex_vbf_13TeV
mv higgsCombineTest.AsymptoticLimits.mH125.root higgsCombineTest.AsymptoticLimits.Comb.mH125.root
