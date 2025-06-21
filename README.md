DetectablePrecedencesExperiment

This repository contains the run script "script.sh" with a model file 
"jobshop5.mzn". The instances and the model file were copied from https://github.com/MiniZinc/minizinc-benchmarks/tree/master/jobshop
The .dzn files are present in the "instances" folder directory

script.sh can be used in the following way: 
./script.sh <output-dir> 

In order to compare the output of multiple benchmark runs, add the output directories 
of multiple benchmark runs to the same directory like in /output2 and /output3.
Then replace /output3 in compare.py with your new directory.
Then execute compare.py:
python3 compare.py
This outputs the statistics of all approaches on the common lower objective to 
a separate .csv file.

data.ipynb and data2.ipynb were used for the data analysis

