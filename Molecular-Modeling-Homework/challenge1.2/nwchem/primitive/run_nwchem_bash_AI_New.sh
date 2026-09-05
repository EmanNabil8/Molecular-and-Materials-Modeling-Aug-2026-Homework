#!/bin/bash

# ------------------------------------------------------------
# NWChem Job Submission Script (Optimized for WSL2)
# Detects physical cores, checks environment, and runs MPI jobs.
# ------------------------------------------------------------

# Exit immediately if any command fails (safety net)
set -e

echo -e "\n\n==========================================="
echo "NWChem job started \c"; date
echo -e "Hostname is \c "; hostname
echo -e "User name is \c "; whoami

# --- Check Conda Environment (Warning only) ---
if [ -z "$CONDA_DEFAULT_ENV" ]; then
  echo -e "\n⚠️  WARNING: No Conda environment is active!"
  echo "   Please run: conda activate molmatmodel"
elif [ "$CONDA_DEFAULT_ENV" != "molmatmodel" ]; then
  echo -e "\n⚠️  WARNING: Current Conda env is '$CONDA_DEFAULT_ENV'"
  echo "   Consider switching to 'molmatmodel'"
else
  echo -e "\n✅ Conda environment '$CONDA_DEFAULT_ENV' is active."
fi

# --- CPU / Core Detection ---
echo -e "\nThe host CPU \c"; cat /proc/cpuinfo | grep 'model name' | uniq

NPROCS=$(cat /proc/cpuinfo | grep processor | wc -l)
string=$(cat /proc/cpuinfo | grep 'cpu cores')
number_string=$(echo "$string" | grep -o -E '[0-9]+(\.[0-9]+)?')
MAXTHREADS=$(echo "$number_string" | grep -oE '[0-9]+' | sort | uniq -c | awk '$1 > 1 {print $2}')

# Fallback if detection fails (set to 2)
if [ -z "$MAXTHREADS" ]; then
    MAXTHREADS=2
fi

echo -e "\n🔹 Detected physical cores (MAXTHREADS) = $MAXTHREADS"
echo -e "🔹 Logical processors available = $NPROCS (hyperthreading disabled for MPI)."

# --- Process Command-Line Arguments ---
if [[ $# -gt 0 ]]; then
    first_arg=$1
    echo -e "\n🔹 First argument provided: $first_arg"

    if [[ $first_arg =~ ^[0-9]+$ ]]; then
        if [[ $first_arg -gt 0 && $first_arg -le $MAXTHREADS ]]; then
            echo "   ✅ $first_arg is in the valid range (1 - $MAXTHREADS)."
            NTHREADS=$first_arg
        else
            echo "   ❌ $first_arg is OUT of range (1 - $MAXTHREADS). Defaulting to 2."
            NTHREADS=2
        fi
    else
        echo "   ❌ Argument is not a number. Defaulting to 2."
        NTHREADS=2
    fi
else
    echo -e "\n🔹 No arguments provided. Defaulting NTHREADS=2"
    NTHREADS=2
fi

# --- Set Up NWChem Environment ---
export NWCHEM_EXECUTABLE=nwchem
echo -e "\n🔹 NWCHEM_EXECUTABLE=$NWCHEM_EXECUTABLE"

# Check if the executable actually exists
if ! command -v $NWCHEM_EXECUTABLE &> /dev/null; then
    echo -e "\n❌ ERROR: 'nwchem' not found in PATH!"
    echo "   Please ensure 'nwchem' is installed and the Conda env is active."
    exit 1
fi

# Check shared libraries (ignore errors if ldd fails)
ldd $NWCHEM_EXECUTABLE 2>/dev/null || echo "   (ldd check skipped or not available)"

# --- Check Input File Existence ---
proj=ch3_zora_b3lyp_prop
THISDIR=$PWD

if [ ! -f "$THISDIR/$proj.nw" ]; then
    echo -e "\n❌ FATAL ERROR: Input file '$proj.nw' not found in $THISDIR!"
    echo "   Please place the .nw file in the current directory before running."
    exit 1
else
    echo -e "\n✅ Input file '$proj.nw' found."
fi

# --- Create Unique Scratch Directory ---
randstr=$(openssl rand -hex 6)
export TMPDIR=/tmp/$USER/nwchem_run.$randstr

echo -e "\n🔹 Scratch directory: TMPDIR=$TMPDIR"
echo -e "🔹 Size of /tmp:"
df -h /tmp

echo -e "\n🔹 Creating scratch dir..."
mkdir -p "$TMPDIR"
cd "$TMPDIR"
echo -e "   ✅ Now in: $(pwd)"

# --- MPI Environment Check ---
echo -e "\n🔹 MPI Location: $(which mpirun)"
mpirun --version 2>/dev/null || echo "   (mpirun version check skipped)"

# --- Launch NWChem with MPI Binding Optimization ---
echo -e "\n==========================================="
echo "🚀 Launching NWChem project '$proj'"
echo "   MPI Threads: $NTHREADS (physical cores)"
echo "   Command: mpirun --map-by core --bind-to core -np $NTHREADS ..."
echo "==========================================="

# +++ UPDATED OUTPUT FILENAME +++
# Changed from ${proj}.outN${NTHREADS} to nwchem_bash_AI_New.outN${NTHREADS}
mpirun --map-by core --bind-to core -np $NTHREADS \
    $NWCHEM_EXECUTABLE "$THISDIR/$proj.nw" > "$THISDIR/nwchem_bash_AI_New.outN${NTHREADS}"

# --- Cleanup Scratch Directory ---
echo -e "\n🔹 Contents of scratch dir ($TMPDIR):"
ls -lt "$TMPDIR"
du -h -s "$TMPDIR"

cd "$THISDIR"
echo -e "\n🔹 Returning to $THISDIR"

echo -e "\n🔹 Deleting scratch directory $TMPDIR..."
/bin/rm -rf "$TMPDIR"

# --- Final Job Status ---
echo -e "\n==========================================="
echo "✅ NWChem job completed successfully!"

# +++ UPDATED FINAL MESSAGE +++
echo -e "   Output saved to: ${THISDIR}/nwchem_bash_AI_New.outN${NTHREADS}"
echo -e "   Job finished at \c"; date
echo "==========================================="

exit 0
