Part I: Molecular Modeling
==========================

Challenge I.7 
--------------
	Modify EMT-MACE script (using AI tool) to perform the geometry relaxation of methane or other small molecule

::Input Files::
	cp ~/Molecular-and-Materials-Modeling-2026-August/molecular-modeling/ase_mace/ase_tests/04_quantum_espresso_water/qe_h2o_optimize.py .

::Checks PP Files for C & H::
			ls -lah /usr/share/espresso/pseudo/
total 207M
C.pbe-n-kjpaw_psl.1.0.0.UPF
H.pbe-kjpaw.UPF


::RUN::
	1...python qe_h2o_optimize.py > qe_h2o_optimize.py.log 
			Successfully ended. 

	2...python qe_CH3_optimize_New-AI-1.py > qe_CH3_optimize_New-AI-1.py.log 
			Successfully ended.
