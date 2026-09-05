Part I: Molecular Modeling
==========================

Challenge I.2
-------------

Software Performance Test
=========================

1. MOPAC
--------

MOPAC executable search:
   which -a mopac
Output:
    /opt/mopac/bin/mopac
    /home/compchemisteman/miniforge3/envs/molmatmodel/bin/mopac
    /opt/mopac/bin/mopac

Input 1: molecular-modeling/software_performance/mopac/dna_pm7_threads

Command used:
    bash run_mopac_bash.01 | tee mopac_bash.log

Result:: The MOPAC calculation started successfully and ended normally.

Sun Aug 30 12:42:58 2026  Job: 'dna_pm7_threads' started successfully

          MOPAC Job: "dna_pm7_threads.mop" ended normally on Aug 30, 2026, at 12:50.

 MOPAC run ends on Sun Aug 30 12:50:02 EEST 2026
