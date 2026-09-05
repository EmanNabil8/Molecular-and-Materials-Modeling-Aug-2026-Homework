from ase import Atoms
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from mace.calculators import mace_mp
import numpy as np

# ============================================
# Experimental reference data
# ============================================
# Each entry: symbol, initial bond length (Å), experimental bond length (Å), experimental atomization energy (eV)
molecules_data = {
    'H2': {'symbol': 'H', 'd0': 0.74, 'd_exp': 0.741, 'E_exp': 4.52},
    'N2': {'symbol': 'N', 'd0': 1.10, 'd_exp': 1.098, 'E_exp': 9.76},
    'O2': {'symbol': 'O', 'd0': 1.21, 'd_exp': 1.208, 'E_exp': 5.12},
    'F2': {'symbol': 'F', 'd0': 1.42, 'd_exp': 1.412, 'E_exp': 1.60},
}

# ============================================
# MACE calculator (CPU only, float64)
# ============================================
calc_mace = mace_mp(model="medium", device="cpu", default_dtype="float64")

# ============================================
# Helper function to run optimization and return results
# ============================================
def compute_diatomic(symbol, d0, calculator, label):
    """Compute atom energy, molecule energy, and optimized bond length for a diatomic."""
    # Single atom energy
    atom = Atoms(symbol, calculator=calculator)
    e_atom = atom.get_potential_energy()

    # Molecule with initial guess
    molecule = Atoms(f'{symbol}2', positions=[(0, 0, 0), (0, 0, d0)], calculator=calculator)

    # Optimize
    opt = BFGS(molecule, trajectory=f"{label}_opt.traj")
    opt.run(fmax=0.01)   # silent (no per‑step output)

    # Results
    d_opt = molecule.get_distance(0, 1)
    e_molecule = molecule.get_potential_energy()
    e_atomization = 2 * e_atom - e_molecule

    return e_atom, e_molecule, d_opt, e_atomization, opt.nsteps

# ============================================
# Main loop
# ============================================
print("=" * 80)
print("DIATOMIC MOLECULE ATOMIZATION ENERGIES: EMT vs MACE (CPU)")
print("=" * 80)

# Store results for summary table
results = []

for name, data in molecules_data.items():
    symbol = data['symbol']
    d0 = data['d0']
    d_exp = data['d_exp']
    E_exp = data['E_exp']

    print(f"\n{'='*80}")
    print(f"Molecule: {name} (diatomic {symbol}₂)")
    print(f"Experimental: bond length = {d_exp:.4f} Å, atomization energy = {E_exp:.2f} eV")
    print(f"{'='*80}")

    # ---------- EMT ----------
    emt_ok = False
    print("\n--- EMT Calculation ---")
    try:
        e_atom_emt, e_mol_emt, d_emt, e_atomiz_emt, n_steps_emt = compute_diatomic(
            symbol, d0, EMT(), f"{name}_emt"
        )
        emt_ok = True
        print(f"  Optimized bond length: {d_emt:.4f} Å")
        print(f"  Atom energy:           {e_atom_emt:.4f} eV")
        print(f"  Molecule energy:       {e_mol_emt:.4f} eV")
        print(f"  Atomization energy:    {e_atomiz_emt:.4f} eV")
        print(f"  Optimization steps:    {n_steps_emt}")
    except NotImplementedError as e:
        print(f"  EMT not available for {symbol}: {e}")

    # ---------- MACE ----------
    print("\n--- MACE Calculation (CPU) ---")
    try:
        e_atom_mace, e_mol_mace, d_mace, e_atomiz_mace, n_steps_mace = compute_diatomic(
            symbol, d0, calc_mace, f"{name}_mace"
        )
        print(f"  Optimized bond length: {d_mace:.4f} Å")
        print(f"  Atom energy:           {e_atom_mace:.4f} eV")
        print(f"  Molecule energy:       {e_mol_mace:.4f} eV")
        print(f"  Atomization energy:    {e_atomiz_mace:.4f} eV")
        print(f"  Optimization steps:    {n_steps_mace}")
    except Exception as e:
        print(f"  MACE calculation failed: {e}")
        e_atom_mace = e_mol_mace = d_mace = e_atomiz_mace = n_steps_mace = None

    # ---------- Comparison ----------
    print("\n--- Comparison with Experiment ---")
    # Bond length
    if emt_ok:
        err_emt_d = abs(d_emt - d_exp) / d_exp * 100
        print(f"  EMT bond length:  {d_emt:.4f} Å  (Δ = {d_emt - d_exp:+.4f} Å, {err_emt_d:.2f}%)")
    else:
        print("  EMT: not available")
    if d_mace is not None:
        err_mace_d = abs(d_mace - d_exp) / d_exp * 100
        print(f"  MACE bond length: {d_mace:.4f} Å  (Δ = {d_mace - d_exp:+.4f} Å, {err_mace_d:.2f}%)")
    # Atomization energy
    if emt_ok:
        err_emt_E = abs(e_atomiz_emt - E_exp) / E_exp * 100
        print(f"  EMT atomization:  {e_atomiz_emt:.4f} eV (Δ = {e_atomiz_emt - E_exp:+.4f} eV, {err_emt_E:.2f}%)")
    else:
        print("  EMT: not available")
    if e_atomiz_mace is not None:
        err_mace_E = abs(e_atomiz_mace - E_exp) / E_exp * 100
        print(f"  MACE atomization: {e_atomiz_mace:.4f} eV (Δ = {e_atomiz_mace - E_exp:+.4f} eV, {err_mace_E:.2f}%)")

    # Store for summary
    results.append({
        'name': name,
        'symbol': symbol,
        'd_exp': d_exp,
        'E_exp': E_exp,
        'emt': {'d': d_emt if emt_ok else None, 'E': e_atomiz_emt if emt_ok else None, 'steps': n_steps_emt if emt_ok else None},
        'mace': {'d': d_mace, 'E': e_atomiz_mace, 'steps': n_steps_mace}
    })

# ============================================
# Summary table
# ============================================
print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)

header = f"{'Molecule':<10} {'Exp d (Å)':<10} {'Exp E (eV)':<12} | "
header += f"{'EMT d (Å)':<10} {'EMT E (eV)':<12} {'EMT st':<8} | "
header += f"{'MACE d (Å)':<10} {'MACE E (eV)':<12} {'MACE st':<8}"
print(header)
print("-" * len(header))

for r in results:
    emt = r['emt']
    mace = r['mace']
    line = f"{r['name']:<10} {r['d_exp']:<10.4f} {r['E_exp']:<12.2f} | "
    if emt['d'] is not None:
        line += f"{emt['d']:<10.4f} {emt['E']:<12.4f} {emt['steps']:<8} | "
    else:
        line += f"{'N/A':<10} {'N/A':<12} {'N/A':<8} | "
    if mace['d'] is not None:
        line += f"{mace['d']:<10.4f} {mace['E']:<12.4f} {mace['steps']:<8}"
    else:
        line += f"{'N/A':<10} {'N/A':<12} {'N/A':<8}"
    print(line)

print("\nNote: 'steps' = number of BFGS optimization steps.")
print("EMT does not support all elements (e.g., F). MACE supports all listed diatomics.")

# ============================================
# Overall analysis
# ============================================
print("\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)

# For molecules where EMT is available, compare average errors
emt_available = [r for r in results if r['emt']['d'] is not None]
mace_available = [r for r in results if r['mace']['d'] is not None]

if emt_available:
    avg_emt_d_err = np.mean([abs(r['emt']['d'] - r['d_exp']) / r['d_exp'] * 100 for r in emt_available])
    avg_emt_E_err = np.mean([abs(r['emt']['E'] - r['E_exp']) / r['E_exp'] * 100 for r in emt_available])
    print(f"EMT (only supported molecules): avg bond length error = {avg_emt_d_err:.2f}%, avg atomization error = {avg_emt_E_err:.2f}%")

if mace_available:
    avg_mace_d_err = np.mean([abs(r['mace']['d'] - r['d_exp']) / r['d_exp'] * 100 for r in mace_available])
    avg_mace_E_err = np.mean([abs(r['mace']['E'] - r['E_exp']) / r['E_exp'] * 100 for r in mace_available])
    print(f"MACE (all molecules): avg bond length error = {avg_mace_d_err:.2f}%, avg atomization error = {avg_mace_E_err:.2f}%")

print("\nDone. Trajectory files saved for each molecule and method.")
