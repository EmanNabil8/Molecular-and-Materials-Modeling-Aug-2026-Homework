from ase import Atoms
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from mace.calculators import mace_mp
import numpy as np

# Experimental/reference values
EXP_BOND_LENGTH = 1.098       # Å
EXP_FREQUENCY = 2358.57       # cm^-1
EXP_DISSOCIATION_ENERGY = 9.76  # eV

print("=" * 70)
print("NITROGEN MOLECULE (N₂) - MACE CALCULATION")
print("=" * 70)

# ------------------------------------------------
# 1. MACE calculator
# ------------------------------------------------
calc_mace = mace_mp(
    model="medium",
    device="cpu",
    default_dtype="float64"
)

# ------------------------------------------------
# 2. Isolated N atom
# ------------------------------------------------
atom_mace = Atoms("N")
atom_mace.calc = calc_mace

e_atom_mace = atom_mace.get_potential_energy()

# ------------------------------------------------
# 3. N₂ geometry optimization
# ------------------------------------------------
d_init = 1.1

molecule_mace = Atoms(
    "N2",
    positions=[(0., 0., 0.), (0., 0., d_init)]
)

molecule_mace.calc = calc_mace

opt_mace = BFGS(
    molecule_mace,
    trajectory="N2_opt_mace.traj"
)

print(f"\nOptimizing N₂ with MACE")
print(f"Initial N-N distance: {d_init:.4f} Å")

opt_mace.run(fmax=0.01)

d_mace = molecule_mace.get_distance(0, 1)
e_molecule_mace = molecule_mace.get_potential_energy()

# Dissociation/atomization energy
e_dissociation_mace = 2 * e_atom_mace - e_molecule_mace

print("\nMACE Results:")
print(f"  Optimized N-N bond length: {d_mace:.4f} Å")
print(f"  N atom energy:              {e_atom_mace:.4f} eV")
print(f"  N₂ molecule energy:         {e_molecule_mace:.4f} eV")
print(f"  Dissociation energy:        {e_dissociation_mace:.4f} eV")

# ------------------------------------------------
# 4. Vibrational frequency
# ------------------------------------------------
print("\n" + "=" * 70)
print("MACE VIBRATIONAL ANALYSIS")
print("=" * 70)

vib_molecule = molecule_mace.copy()
vib_molecule.calc = calc_mace

vib = Vibrations(
    vib_molecule,
    name="N2_vib_mace"
)

vib.run()

freqs = vib.get_frequencies()

print("\nMACE vibrational frequencies:")
for i, freq in enumerate(freqs, 1):
    print(f"  Mode {i}: {freq}")

# Select positive real vibrational frequency
real_freqs = np.real(freqs)
positive_freqs = real_freqs[real_freqs > 1.0]

if len(positive_freqs) == 1:
    vib_freq_mace = positive_freqs[0]
else:
    vib_freq_mace = positive_freqs.max()
    print("\nWarning: unexpected number of positive frequencies.")

print(f"\nN-N stretching frequency: {vib_freq_mace:.2f} cm⁻¹")

# ------------------------------------------------
# 5. Comparison with reference
# ------------------------------------------------
print("\n" + "=" * 70)
print("COMPARISON WITH REFERENCE")
print("=" * 70)

bond_error = abs(d_mace - EXP_BOND_LENGTH)
freq_error = abs(vib_freq_mace - EXP_FREQUENCY)
energy_error = abs(e_dissociation_mace - EXP_DISSOCIATION_ENERGY)

print("\nN-N Bond Length:")
print(f"  Reference: {EXP_BOND_LENGTH:.4f} Å")
print(f"  MACE:      {d_mace:.4f} Å")
print(f"  Error:     {bond_error:.4f} Å "
      f"({bond_error / EXP_BOND_LENGTH * 100:.2f}%)")

print("\nDissociation Energy:")
print(f"  Reference: {EXP_DISSOCIATION_ENERGY:.2f} eV")
print(f"  MACE:      {e_dissociation_mace:.4f} eV")
print(f"  Error:     {energy_error:.4f} eV "
      f"({energy_error / EXP_DISSOCIATION_ENERGY * 100:.2f}%)")

print("\nN-N Stretching Frequency:")
print(f"  Reference: {EXP_FREQUENCY:.2f} cm⁻¹")
print(f"  MACE:      {vib_freq_mace:.2f} cm⁻¹")
print(f"  Error:     {freq_error:.2f} cm⁻¹ "
      f"({freq_error / EXP_FREQUENCY * 100:.2f}%)")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"{'Property':<30} {'Reference':<15} {'MACE':<15}")
print("-" * 60)
print(f"{'N-N Bond Length (Å)':<30} "
      f"{EXP_BOND_LENGTH:<15.4f} {d_mace:<15.4f}")
print(f"{'Dissociation Energy (eV)':<30} "
      f"{EXP_DISSOCIATION_ENERGY:<15.2f} {e_dissociation_mace:<15.4f}")
print(f"{'N-N Frequency (cm⁻¹)':<30} "
      f"{EXP_FREQUENCY:<15.2f} {vib_freq_mace:<15.2f}")

print("\nOptimization and vibrational analysis complete.")
print("Files:")
print("  - N2_opt_mace.traj")
print("  - N2_vib_mace.*")
