from ase import Atoms
from ase.calculators.emt import EMT
from ase.optimize import BFGS

# Experimental bond lengths (Angstrom) and atomization energies (eV) for comparison
molecules_data = {
    'H2': {'symbol': 'H', 'd0': 0.74, 'E_atom_exp': 4.52},
    'N2': {'symbol': 'N', 'd0': 1.10, 'E_atom_exp': 9.76},
    'O2': {'symbol': 'O', 'd0': 1.21, 'E_atom_exp': 5.12},
    'F2': {'symbol': 'F', 'd0': 1.42, 'E_atom_exp': 1.60},
}

print("Diatomic molecule atomization energies with EMT calculator\n")
print(f"{'Molecule':<10} {'d0 (Å)':<8} {'d_opt (Å)':<10} {'E_atom (eV)':<12} {'E_mol (eV)':<12} {'E_atomiz (eV)':<14} {'Exp. (eV)':<10}")

for name, data in molecules_data.items():
    symbol = data['symbol']
    d0 = data['d0']
    E_exp = data['E_atom_exp']

    # Atom energy
    atom = Atoms(symbol, calculator=EMT())
    e_atom = atom.get_potential_energy()

    # Molecule setup with initial bond length
    molecule = Atoms(f'{symbol}2', positions=[(0, 0, 0), (0, 0, d0)], calculator=EMT())

    # Geometry optimization
    opt = BFGS(molecule)
    opt.run(fmax=0.01)  # silent optimization

    # Optimized bond length
    d_opt = molecule.get_distance(0, 1)

    # Molecule energy
    e_molecule = molecule.get_potential_energy()

    # Atomization energy: 2 * E_atom - E_molecule
    e_atomization = 2 * e_atom - e_molecule

    # Print results
    print(f"{name:<10} {d0:<8.2f} {d_opt:<10.3f} {e_atom:<12.3f} {e_molecule:<12.3f} {e_atomization:<14.3f} {E_exp:<10.2f}")

print("\nNote: EMT is a simple metal potential; results for covalently bonded diatomics are not physically accurate.")
