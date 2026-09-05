Part II: Materials Modeling
==========================

Challenge 2.8 
--------------
	Adsorption on the surface using ASE: Hydrogen or Mercury atom on a piece of graphene, C8 atom on a C18 piece of graphene: Modify the Python script to perform the relaxation of the C8 slab and calculate the new adsorption energy. Likewise, increase the ecutwfc parameter to see if this improves the binding energy of H on C8.

(a) Relax the clean C8 slab and compare new binding energy:

::Input::
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/7_Work_Function/relaxation.py . 
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/8_Adsorption/energy_h.py .
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/8_Adsorption/c.vasp .
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/8_Adsorption/ch.vasp .
cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/8_Adsorption/h.vasp .
cp /usr/share/espresso/pseudo/C.pbe-n-kjpaw_psl.1.0.0.UPF ./C.upf
cp /usr/share/espresso/pseudo/H.pbe-kjpaw.UPF ./H.upf

Edited Script:
C.upf, nat = 8, ntyp = 1, c.vasp, and removed nspin = 2.
qe_bin = "/home/compchemisteman/miniforge3/envs/molmatmodel/bin"
pw_command = f'mpirun -np 4 {qe_bin}/pw.x'

::Run 1::
	export OMP_NUM_THREADS=1

	python relaxation_c8.py > relaxation_c8.py.out 
			Successfully ended-->  Total Energy : -1999.821951 eV

	python relaxation.py > relaxation.py.out 
			Successfully ended-->  Total Energy : -2015.256373 eV

	python energy_h.py > energy_h.py.out 
			Successfully ended-->  Total Energy : -12.564796 eV

Binding energy = E(C8) + E(H) - E(H@C8) 
               = -1999.821951 -12.564796 -(-2015.256373) eV Binding energy = 2.87 eV

Since Binding Energy reported by using unrelaxed C8 slab = 2.8639 eV, then difference ≈ 0.0057 eV
	So relaxing the C8 slab has almost no effect on the adsorption energy.



(b) Recalculating adsorption-energy at a higher ecutwfc:

::Input::
Same files for task (a) with only 'ecutwfc': 100, edit

::Run 2::
	export OMP_NUM_THREADS=1

	python relaxation_c8.py > relaxation_c8.py.out 
			Successfully ended-->  Total Energy : -1999.824422 eV

	python relaxation.py > relaxation.py.out 
			Successfully ended-->  Total Energy : -2015.258861 eV

	python energy_h.py > energy_h.py.out 
			Successfully ended-->  Total Energy : -12.564892 eV

Binding energy = E(C8) + E(H) - E(H@C8) 
               = -1999.824422 -12.564892 -(-2015.258861) eV Binding energy = 2.87 eV

	So  increasing the ecutwfc parameter from 80 Ry to 100 Ry --> a difference of only 0.000079 eV
