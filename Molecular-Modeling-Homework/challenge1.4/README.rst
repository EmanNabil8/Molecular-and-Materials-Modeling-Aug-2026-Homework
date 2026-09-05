Part I: Molecular Modeling
==========================

Challenge I.4 
--------------
	Run Scripts of Testing MACE Installation.

(a) Testing:

::Input Files::
cp ~/Molecular-and-Materials-Modeling-2026-August/molecular-modeling/ase_mace/mace/tests/
	[check_mace_ml_installation.py, mace_calc.py, mace_config.txt, model_analyzer.py, model_element_detector.py, quick_test.py]

::RUN::
	1...python check_mace_ml_installation.py > check_mace_ml_installation.py_New.log 
			Successfully ended.
	2...python mace_calc.py > mace_calc.py_New.log
			First Error: 
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
✗ Model not found: /home/compchemisteman/.cache/mace/macempa0mediummodel
			Second: ls -lh ~/.cache/mace/
total 43M
-rw-r--r-- 1 compchemisteman compchemisteman 43M Aug 31 10:36 20231203mace128L1_epoch199model
			Third: python mace_calc.py H2O ~/.cache/mace/20231203mace128L1_epoch199model --device cpu > mace_calc.py_New.log
			Successfully ended.
	3...python model_analyzer.py > model_analyzer.py_New.log
			Successfully completed 
	4...python model_element_detector.py > model_element_detector.py_New.log
			Successfully ended.
	5...python quick_test.py > quick_test.py_New.log
			First Error:
Couldn't find MACE model files: /home/compchemisteman/.cache/mace/macempa0mediummodel
			Second: Editting quick_test.py 
model = Path.home() / '.cache' / 'mace' / 'macempa0mediummodel'
Replaced by:
model = Path.home() / '.cache' / 'mace' / '20231203mace128L1_epoch199model'
			Tird: python quick_test.py > quick_test.py_New-2.log
			Successfully ended.
---------------------------------------------------------------------------

(b) Simple:
-----------

::Input Files::

cp ~/Molecular-and-Materials-Modeling-2026-August/molecular-modeling/ase_mace/mace/simple/
	[water_mace.py & water_mace_emt_01.py]

::RUN::
	1...python water_mace.py > water_mace.py_New.log 
			Successfully ended.
	2...python water_mace_emt_01.py > water_mace_emt_01.py_New.log 
			Successfully ended.


