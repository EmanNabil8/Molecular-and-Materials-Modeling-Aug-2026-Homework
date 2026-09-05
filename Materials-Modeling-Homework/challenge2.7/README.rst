Part II: Materials Modeling
==========================

Challenge 2.7 
--------------
	Redo of calculations for the planar average potential and work function for graphene using ASE 

::Input::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/7_Work_Function/work_function.py .
cp /usr/share/espresso/pseudo/C.pbe-n-kjpaw_psl.1.0.0.UPF ./C.upf

Edited Script for bin PATH and np:
qe_bin = "/home/compchemisteman/miniforge3/envs/molmatmodel/bin"
pw_command = f'mpirun -np 4 {qe_bin}/pw.x'

::Run 1::
	python work_function.py > work_function.py.out 
			Successfully ended--> potential_plot1.png >> this figure corresponds to the case where # 'assume_isolated': '2D' is commented out, so the calculation was run without the 2D isolated-system correction.

::Run 2::
	python work_function_2D.py > work_function_2D.py.out 
			Successfully ended--> potential_plot1.png >> 2D isolated-system correction produces a clear boundary artifacts at the two cell boundaries (0 & 15 Angstrom)
