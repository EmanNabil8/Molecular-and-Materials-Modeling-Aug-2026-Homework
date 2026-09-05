Part I: Molecular Modeling
==========================

Challenge I.2
-------------

Software Performance Test
=========================

2. NWChem
---------
Primitive Input Files:: molecular-modeling > software_performance > nwchem > primitive

1. Run using bash script:
./run_nwchem_bash.01 4
Results::	Total times  cpu:       28.5s     wall:       28.5s

2. To create & run new AI-assissted bash script:
nano run_nwchem_bash_AI_New.sh
chmod u+x run_nwchem_bash_AI_New.sh
./run_nwchem_bash_AI_New.sh 4
Results::	Total times  cpu:       30.1s     wall:       30.1s

Python Input Files:: molecular-modeling > software_performance > nwchem > python-driven

3. Run using python script:
python run_nwchem.py | tee run_nwchem_py.log

Results::
============================================================
PERFORMANCE SUMMARY
============================================================
NPROC      Wall Time (s)   Speedup      Efficiency   Status
------------------------------------------------------------
2          24.50           1.00         50.0       % SUCCESS
4          25.30           0.97         24.2       % SUCCESS
============================================================
