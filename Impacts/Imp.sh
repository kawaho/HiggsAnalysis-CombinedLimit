declare -a arr=("ggcat0" "ggcat1" "ggcat2" "ggcat3" "ggcat4" "vbf")
for i in "${arr[@]}"
do
  echo $i
  export cat=$i
  cd $i
  source Impacts.sh
  cd ../
done
find . -type f -name "*.pdf" -exec cp {} ./results/ \
