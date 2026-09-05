Part II: Materials Modeling
==========================

Challenge 2.2 
--------------

(a) Run Convergence ASE python script after editing QE bin path and name/location of Si PP file:
	python convergence_New-test_si.py > convergence_New-test_si.py.out

------------------------------------------------------------
>>> K-points CONVERGED at (15, 15, 15) (ΔE < 0.01 meV/atom)
------------------------------------------------------------
============================================================
Convergence summary:
- ecutwfc: 60
- k-points: (15, 15, 15)
============================================================

(b)
	Run a final QE SCF calculation with your converged ecutwfc and kpoints (60,15), along with tstress = .true. and tprnfor = .true. in the input file (under &CONTROL) to compute stress and atomic forces and inspect the output. /path/to/qebin/pw.x < Si_force_stress.in > Si_force_stress.out

::Input Files::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/2_Convergence_Test/Si_force_stress.in .
cp /usr/share/espresso/pseudo/Si.pbe-n-rrkjus_psl.1.0.0.UPF .
mv Si.pbe-n-rrkjus_psl.1.0.0.UPF Si.upf

::Run::
	mpirun -np 4 pw.x < Si_force_stress.in > Si_force_stress.out

::RESULTS::

grep "!" Si_force_stress.out
!    total energy              =     -22.83981831 Ry

grep -A5 "Forces acting on atoms" Si_force_stress.out
     Forces acting on atoms (cartesian axes, Ry/au):

     atom    1 type  1   force =     0.00000000    0.00000000   -0.00000000
     atom    2 type  1   force =     0.00000000    0.00000000    0.00000000

     Total force =     0.000000     Total SCF correction =     0.000000
	 
grep -A4 "total   stress" Si_force_stress.out
          total   stress  (Ry/bohr**3)                   (kbar)     P=       20.32
   0.00013813   0.00000000  -0.00000000           20.32        0.00       -0.00
   0.00000000   0.00013813  -0.00000000            0.00       20.32       -0.00
  -0.00000000  -0.00000000   0.00013813           -0.00       -0.00       20.32

(c) 
	Find different pseudopotentials from http://pseudopotentials.quantum-espresso.org/legacy_tables or other resources. Update the convergence Test (ASE) python code, and run the convergence test for each. Make a table of energy and k point cut offs of various pseudopotentials using Si as an example.

	I will skip the pseudopotential comparison challenge because each convergence test takes more than an hour.



