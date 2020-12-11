combineTool.py -M T2W -i ../../datacard_$cat.txt -o datacard_$cat.root --parallel 4 -m 125
combineTool.py -M Impacts -d ../../datacard_$cat.root -m 125 --doInitialFit --robustFit 1 -P r --expectSignal=0 --rMin=-.5 --rMax=.5 -t -1
combineTool.py -M Impacts -d ../../datacard_$cat.root -m 125 --robustFit 1 --doFits --rMin=-.5 --rMax=.5 -t -1 --parallel 4
combineTool.py -M Impacts -d ../../datacard_$cat.root -m 125 -o impacts.json -t -1
plotImpacts.py -i impacts.json -o impacts_$cat
