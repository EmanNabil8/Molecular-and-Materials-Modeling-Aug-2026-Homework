Part I: Molecular Modeling
==========================

Challenge I.2 Software Performance Test
=======================================

	3. Quantum ESPRESSO
	--------------------

export OMP_NUM_THREADS=1 
mpirun -np 4 pw.x -in Tl2.so_scf.in > Tl2.so_scf.in_out_OMP1_MPI4 
mpirun -np 8 pw.x -in Tl2.so_scf.in > Tl2.so_scf.in_out_OMP1_MPI8_bltpDesktop


:::Checks:::

which pw.x
	/home/compchemisteman/miniforge3/envs/molmatmodel/bin/pw.x

which mpirun
	/home/compchemisteman/miniforge3/envs/molmatmodel/bin/mpirun

(a) Primitive Input Files: molecular-modeling/software_performance/quantum_espresso/primitive_run/Tl2.so_scf.in

1. Set OpenMP to 1 thread
	export OMP_NUM_THREADS=1

2. Verify:
	echo $OMP_NUM_THREADS

3. Run: 
	mpirun -np 2 pw.x -in Tl2.so_scf.in > Tl2.so_scf_MPI2
	mpirun -np 4 pw.x -in Tl2.so_scf.in > Tl2.so_scf_MPI4

4. Conclusion:
#MPI wall 
2 	1m 0.97s 
4 	 58.69s



(b) Python Input Files: molecular-modeling/software_performance/quantum_espresso/python_run/tl_bulk_scf_04.py

::Checks::
which pw.x
	/home/compchemisteman/miniforge3/envs/molmatmodel/bin/pw.x
			File "pw_configure.txt" was adjusted accordingly

1. Set OpenMP to 1 thread
	export OMP_NUM_THREADS=1

2. Verify:
	echo $OMP_NUM_THREADS

3. Run: 
	python tl_bulk_scf_04.py > tl_bulk_scf_04.py_logfile

4. Conclusion:
================================================================================
BENCHMARK SUMMARY
================================================================================
   MPI    OMP    Wall Time   Efficiency       Status
--------------------------------------------------------------------------------
     1      1        88.80s         0.99x    completed
     2      1        65.64s         0.96x    completed
     4      1        72.50s         0.95x    completed
================================================================================

🏆 Fastest calculation: MPI=2, OMP=1
   Wall Time: 65.64s
   Efficiency: 0.96x

🏆 Best efficiency: MPI=1, OMP=1
   Efficiency: 0.99x
   Wall Time: 88.80s

📊 Speedup relative to serial (1 MPI, 1 OMP): 88.80s
   MPI= 2, OMP= 1:   1.35x speedup,    65.64s
   MPI= 4, OMP= 1:   1.22x speedup,    72.50s
   MPI= 1, OMP= 1:   1.00x speedup,    88.80s
