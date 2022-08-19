ln -s ../../../BIN/calc_stericHindrance.py .
ln -s ../../../BIN/gen_popkinsForChains.py .
ln -s ../../../BIN/util_fullBindingSitesParser.py .

cp ../../../BIN/calc_stericHindrance.sh .
cp ../../../BIN/gen_popkinsForChains.sh .

helpf=HELP.TXT
rm -f $helpf
tou $helpf
echo "Thank you for calling for help." >> $helpf
echo "Now that you've executed setup.sh, make sure you complete the following tasks:" >> $helpf
echo " * update gen_popkinsForChains.sh" >> $helpf
echo " * update calc_stericHindrance.sh" >> $helpf
