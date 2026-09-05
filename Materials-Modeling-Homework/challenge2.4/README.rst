Part II: Materials Modeling
==========================

Challenge 2.4 
--------------
	Electronic properties: Si (Charge and DOS, ASE); Modify the input file parameters in Si ASE script and test the effects of different values of Gaussian broadening (degauss).

::Input::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/4_Electronic_Properties_Si/electronic_properties_si.py .

cp ~/Molecular-and-Materials-Modeling-2026-Homework/Materials-Modeling-Homework/challenge2.3/ASE-QE/Si.upf .

Edited Script for bin PATH and np:
qe_bin = "/home/compchemisteman/miniforge3/envs/molmatmodel/bin"
pw_command = f'mpirun -np 4 {qe_bin}/pw.x'
set 'degauss': 0.005,

::Run::
	python electronic_properties_si_new.py > electronic_properties_si_new.py.out
			Successfully ended.

::RESULTS::

=== Electronic Structure Analysis Complete ===

Generated files:

- Charge density (from SCF): charge_density.cube

- Löwdin Charges (from SCF): lowdin.out

- Total DOS (from NSCF): total_dos.dat --> Fermi enrgy was shifted to zero & visualized using python script by ChatGPT.

- PDOS files (from NSCF): pdos_results/ --> Fermi enrgy was shifted to zero & visualized using python script by ChatGPT.

