#
# ASE driven Quantum ESPRESSO geometry optimization of methane (CH4)
#
import os
from ase import Atoms
from ase.build import molecule
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import BFGS
from ase.units import Ry, Bohr

os.environ['OMP_NUM_THREADS'] = '1'

# Set the path to your pseudopotential directory (update to your actual path)
PSEUDO_DIR = '/usr/share/espresso/pseudo/'

# 1. Create the initial methane molecule structure
ch4 = molecule('CH4')
ch4.set_cell([12, 12, 12])  # Vacuum box
ch4.center()               # Center the molecule in the box

# 2. Configure the Quantum ESPRESSO Calculator
pseudopotentials = {
    'C': 'C.pbe-n-kjpaw_psl.1.0.0.UPF',
    'H': 'H.pbe-kjpaw.UPF'
}

input_data = {
    'control': {
        'calculation': 'scf', 
        'prefix': 'ch4',
        'outdir': './outdir',
        'verbosity': 'low',
        'tstress': True,
        'tprnfor': True
    },
    'system': {
        'ecutwfc': 46.0,    # Plane wave cutoff (Ry)
        'ibrav': 0,         # Use 0 for ASE to handle cell parameters
        'nosym': True,      # No symmetry for molecules
        'noinv': True,
        'occupations': 'smearing',  # Smearing for better convergence
        'smearing': 'gaussian',
        'degauss': 0.02,
    },
    'electrons': {
        'conv_thr': 1e-8,
        'mixing_beta': 0.7,
        'diagonalization': 'david'
    }
}

command = 'mpirun -np 4 pw.x'
profile = EspressoProfile(command, pseudo_dir=PSEUDO_DIR)

calc = Espresso(profile=profile, 
                pseudopotentials=pseudopotentials,
                input_data=input_data,
                kpts=(1, 1, 1))  # Gamma-point only for molecules

ch4.calc = calc

# 3. Run the Geometry Optimization
dyn = BFGS(ch4, trajectory='ch4_opt.traj', logfile='ch4_opt.log')
dyn.run(fmax=0.01)

# 4. Print optimized geometry
print("\nOptimized methane geometry:")
print("C-H bond lengths (Å):")
for i in range(1, 5):
    print(f"  C-H{i}: {ch4.get_distance(0, i):.4f}")
avg_bond = sum(ch4.get_distance(0, i) for i in range(1,5)) / 4
print(f"  Average C-H bond length: {avg_bond:.4f} Å")

print("\nH-C-H angles (degrees):")
# There are 6 H-C-H angles in CH4
h_indices = [1, 2, 3, 4]
for idx, i in enumerate(h_indices):
    for j in h_indices[idx+1:]:
        angle = ch4.get_angle(i, 0, j)
        print(f"  H{i}-C-H{j}: {angle:.2f}")

print(f"\nFinal total energy: {ch4.get_total_energy():.6f} eV")
