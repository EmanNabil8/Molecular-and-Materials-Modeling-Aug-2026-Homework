Part II: Materials Modeling
==========================

Challenge 2.1 
--------------
	Calculate Total Energy (QE and ASE) using Quantum ESPRESSO --> Modify the "ecutwfc" in the input file and check, how it changes the total energy.

(a) QE
------

::Input Files::
	cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/1_Energy_Calculation/Si.in .

::Run::
	mpirun -np 4 pw.x < Si.in > Si.out
			Successfully ended. 
	Increase "ecutwfc" to 60
	mpirun -np 4 pw.x < Si_60-ecutwfc.in > Si_60-ecutwfc.in.out
			Successfully ended.

::Conclusion::

| "ecutwfc" | Total energy (Ry) | Fermi energy (eV) |

| --------: | ----------------: | ----------------: |

|     30 Ry |      -22.65169249 |            6.7973 |

|     60 Ry |      -22.65193261 |            6.7962 |

(b) ASE
-------

::Input Files::
	cp ~/Molecular-and-Materials-Modeling-2026-August/materials-modeling/1_Energy_Calculation/si_ase.py .

::Run::
	python si_ase.py > si_ase.py.out
			Error due to wrong QE path and mismatched name/location of Si PP file
			
	Update Calculator configuration: 
	python si_ase-upd.py > si_ase-upd.py.out
			Running SCF calculation...
			Total energy: -308.191950 eV
			Fermi level: 6.797300 eV

	Increase "ecutwfc" to 60
	python si_ase-upd60.py > si_ase-upd60.py.out
			Running SCF calculation...
			Total energy: -308.195217 eV
			Fermi level: 6.796200 eV

::Conclusion::

| `ecutwfc` (Ry) | Total Energy (Ry) | Total Energy (eV) | Fermi Level (eV) |

| -------------: | ----------------: | ----------------: | ---------------: |

|             30 |      -22.65169249 |       -308.191950 |         6.797300 |

|             60 |      -22.65193261 |       -308.195217 |         6.796200 |
