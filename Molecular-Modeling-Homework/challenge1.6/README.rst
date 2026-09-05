Part I: Molecular Modeling
==========================

Challenge I.6 
--------------
	Modify EMT-MACE script (using AI tool) to compute the C-H bond energy in methane

::Input Files::
cp ~/Molecular-and-Materials-Modeling-2026-August/molecular-modeling/ase_mace/ase_tests/03_ethane_C-C_bond_energy/ethane_CC_bond_en_EMT_MACE_01.py .

::RUN::
	1...python methane_CH_bond_en_EMT_MACE.py > methane_CH_bond_en_EMT_MACE.py_NEW-AI.py.log 
			Successfully ended. BUT with Error: NameError: name 'Atoms' is not defined

	2...python methane_CH_bond_en_EMT_MACE-2.py > methane_CH_bond_en_EMT_MACE.py_NEW-AI-2.py.log
			Successfull run and reasonable results. 

::Summary of Results::
Property		EMT			MACE		Experiment
C–H bond length	1.1515 Å	1.0931 Å	1.0870 Å

::Conclusion::
MACE is superior for both bond length and bond energy.
