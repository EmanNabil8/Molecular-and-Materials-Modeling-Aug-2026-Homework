Part II: Materials Modeling
==========================

Challenge 2.3 
--------------

	Modify parameters For the cell relaxation (both QE and ASE-QE), use a custom, tighter values of etot_conv_thr and forc_conv_thr, shift the atoms manually and run the convergence again. Try the same in ASE-driven QE run.

(a) QE:
-------

::Input::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/3_Cell_Relaxation/cell_relaxation_si.in .
cp /usr/share/espresso/pseudo/Si.pbe-n-rrkjus_psl.1.0.0.UPF .
mv Si.pbe-n-rrkjus_psl.1.0.0.UPF Si.upf

Edited input using tighter relaxation thresholds inside &CONTROL:
   etot_conv_thr    = 1.0d-5
   forc_conv_thr    = 5.0d-4
Shifted one Si relative to the other, by +0.05 Å along x
Setting calculation = 'vc-relax'

::Run::
	export OMP_NUM_THREADS=1
	mpirun -np 4 pw.x < cell_relaxation_si_new.in > cell_relaxation_si_new.out
			Successfully ended.

(b) ASE-QE:
-----------

::Input::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/3_Cell_Relaxation/cell_relaxation_si.py .
cp /usr/share/espresso/pseudo/Si.pbe-n-rrkjus_psl.1.0.0.UPF .
mv Si.pbe-n-rrkjus_psl.1.0.0.UPF Si.upf

Edited Script using tighter relaxation thresholds inside &CONTROL:
   etot_conv_thr    = 1.0d-5
   forc_conv_thr    = 5.0d-4
Shifted one Si relative to the other, by +0.05 Å along x:

Edited Script for bin PATH and np:
qe_bin = "/home/compchemisteman/miniforge3/envs/molmatmodel/bin"
pw_command = f'mpirun -np 4 {qe_bin}/pw.x'

::Run::
	python cell_relaxation_si_new.py > cell_relaxation_si_new.py.out
			Successfully ended.


::RESULTS::

  Total Energy (ASE-QE)                 :  -310.757091 eV
  Total Energy (direct QE)              :  −22.84015363 Ry = −310.75612 eV

So the final energiesare are nearly qual.
However, ASE route is much slower (3 min 37 s vs. ~20 min)
