#!/usr/bin/env python3
"""
Train zProto on Planck 2018 CMB Power Spectrum.

Maps each multipole ℓ to a KleinManifold state via fiber_project(ℓ),
then feeds the power spectrum D_ℓ as the observation magnitude.

The acoustic peaks at ℓ ≈ 220, 546, 800 should produce distinctive
convergence signatures in the agent's perception.
"""

import subprocess
import struct
import os
import sys

DATA_DIR = "/home/phrxmaz/Singularity/cmb/planck_2018"
ZPROTO_DIR = "/home/phrxmaz/Documents/Protoreal_Zeta/zProto"

def parse_planck_spectrum(filename):
    """Parse Planck power spectrum text file.
    Returns list of (ell, D_ell, sigma_minus, sigma_plus)."""
    data = []
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 4:
                try:
                    ell = float(parts[0])
                    d_ell = float(parts[1])
                    sigma_m = float(parts[2])
                    sigma_p = float(parts[3])
                    data.append((ell, d_ell, sigma_m, sigma_p))
                except ValueError:
                    continue
    return data

def write_csv(data, output_path, spectrum_type):
    """Write parsed spectrum to CSV for Rust consumption."""
    with open(output_path, 'w') as f:
        f.write("ell,d_ell,sigma_minus,sigma_plus,spectrum\n")
        for ell, d_ell, sigma_m, sigma_p in data:
            f.write(f"{int(ell)},{d_ell},{sigma_m},{sigma_p},{spectrum_type}\n")
    print(f"  Wrote {len(data)} multipoles to {output_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("  Planck 2018 CMB → zProto Training Preparation")
    print("=" * 60)

    spectra = {
        "TT": "COM_PowerSpect_CMB-TT-full_R3.01.txt",
        "TE": "COM_PowerSpect_CMB-TE-full_R3.01.txt",
        "EE": "COM_PowerSpect_CMB-EE-full_R3.01.txt",
    }

    all_data = []
    for stype, fname in spectra.items():
        print(f"\n▸ Parsing {stype} spectrum...")
        data = parse_planck_spectrum(fname)
        print(f"  Found {len(data)} multipoles (ℓ = {int(data[0][0])} to {int(data[-1][0])})")

        # Key peaks
        if stype == "TT":
            peaks = [(220, "1st acoustic"), (546, "2nd acoustic"), (800, "3rd acoustic")]
            for peak_ell, name in peaks:
                closest = min(data, key=lambda x: abs(x[0] - peak_ell))
                print(f"  Peak at ℓ≈{peak_ell} ({name}): D_ℓ = {closest[1]:.1f} μK²")

        all_data.extend([(d[0], d[1], d[2], d[3], stype) for d in data])

    # Write combined CSV
    output = os.path.join(DATA_DIR, "planck_2018_combined.csv")
    with open(output, 'w') as f:
        f.write("ell,d_ell,sigma_minus,sigma_plus,spectrum\n")
        for ell, d_ell, sm, sp, stype in all_data:
            f.write(f"{int(ell)},{d_ell},{sm},{sp},{stype}\n")
    print(f"\n  Combined: {len(all_data)} total observations → {output}")

    print("\n" + "=" * 60)
    print("  Data ready for zProto training")
    print("=" * 60)
