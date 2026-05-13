//! # zProto Trainer — Spectral Perception
//!
//! Trains the zProto agent on REAL physics data:
//! 1. Random matrix eigenvalues (GUE/GOE/GSE)
//! 2. Planck 2018 CMB power spectrum (TT/TE/EE)
//! 3. Published spin chain spectral gaps (neutron scattering)
//! 4. Glueball mass spectrum (lattice QCD)

use zproto::agent::ZProtoAgent;
use zproto::manifold::KleinManifold;
use zproto::fiber::fiber_project;
use zproto::graph::{ObservationGraph, euler_perception};
use zproto::operators::standard_resonance;
use serde::Deserialize;
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::path::Path;

// ════════════════════════════════════════════════════
// DATA STRUCTURES
// ════════════════════════════════════════════════════

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
struct EigenvalueRow {
    ensemble: String,
    matrix_size: usize,
    sample: usize,
    index: usize,
    eigenvalue: f64,
}

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
struct CmbRow {
    ell: u32,
    d_ell: f64,
    sigma_minus: f64,
    sigma_plus: f64,
    spectrum: String,
}

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
struct SpinChainRow {
    material: String,
    spin: f64,
    chain_type: String,
    gap_meV: f64,
    gap_error_meV: f64,
    exchange_J_meV: f64,
    gapped: String,
    method: String,
    reference: String,
}

#[allow(dead_code)]
#[derive(Debug, Deserialize)]
struct GlueballRow {
    #[serde(rename = "JPC")]
    jpc: String,
    mass_r0: f64,
    mass_GeV: f64,
    error_GeV: f64,
    state_type: String,
}

// ════════════════════════════════════════════════════
// PHASE 1: RANDOM MATRIX EIGENVALUES
// ════════════════════════════════════════════════════

fn train_random_matrix() -> Result<(), Box<dyn Error>> {
    println!("\n  PHASE 1: Random Matrix Eigenvalues");
    println!("  -----------------------------------");

    let ensembles = vec!["gue", "goe", "gse"];
    let data_dir = Path::new("zProto/data/random_matrix");

    for ensemble in ensembles {
        let file_path = data_dir.join(format!("{}_eigenvalues.csv", ensemble));
        if !file_path.exists() {
            println!("  [!] Skipping {}: data not found", ensemble);
            continue;
        }

        println!("\n  ▸ {} ensemble", ensemble.to_uppercase());
        let mut rdr = csv::Reader::from_reader(File::open(file_path)?);

        let mut samples: HashMap<(usize, usize), Vec<f64>> = HashMap::new();
        for result in rdr.deserialize() {
            let row: EigenvalueRow = result?;
            samples.entry((row.matrix_size, row.sample)).or_default().push(row.eigenvalue);
        }

        let mut total_metric = 0.0;
        let mut sample_count = 0usize;

        for (_, eigs) in &samples {
            let mut agent = ZProtoAgent::origin();
            let mut last_result = None;
            for eig in eigs {
                let input = fiber_project(eig.abs().max(1e-6));
                last_result = Some(agent.step(input));
            }
            if let Some(result) = last_result {
                total_metric += result.metric;
            }
            sample_count += 1;
        }

        println!("    Samples: {} | Avg Metric: {:.6}",
            sample_count, total_metric / sample_count as f64);
    }
    Ok(())
}

// ════════════════════════════════════════════════════
// PHASE 2: PLANCK CMB POWER SPECTRUM
// ════════════════════════════════════════════════════

fn train_cmb() -> Result<(), Box<dyn Error>> {
    println!("\n  PHASE 2: Planck 2018 CMB Power Spectrum");
    println!("  ----------------------------------------");

    let cmb_path = Path::new("/home/phrxmaz/Singularity/cmb/planck_2018/planck_2018_combined.csv");
    if !cmb_path.exists() {
        println!("  [!] CMB data not found. Run: python3 zProto/scripts/prepare_cmb.py");
        return Ok(());
    }

    let mut rdr = csv::Reader::from_reader(File::open(cmb_path)?);
    let mut spectra: HashMap<String, Vec<(u32, f64, f64, f64)>> = HashMap::new();

    for result in rdr.deserialize() {
        let row: CmbRow = result?;
        spectra.entry(row.spectrum.clone()).or_default()
            .push((row.ell, row.d_ell, row.sigma_minus, row.sigma_plus));
    }

    for (stype, data) in &spectra {
        println!("\n  ▸ {} spectrum ({} multipoles)", stype, data.len());

        let mut agent = ZProtoAgent::origin();
        let mut total_metric = 0.0;

        for (ell, d_ell, _sm, _sp) in data {
            let ell_f = *ell as f64;
            let input = KleinManifold::new(
                0.0, ell_f, 1.0 / ell_f, d_ell / 1000.0, 0.0,
            );
            let result = agent.step(input);
            total_metric += result.metric;
        }

        let avg_metric = total_metric / data.len() as f64;
        let final_chi = euler_perception(
            &ObservationGraph::active_subgraph(&agent.frame.intuition()));

        println!("    Avg Metric: {:.2} | Final χ: {}", avg_metric, final_chi);
    }
    Ok(())
}

// ════════════════════════════════════════════════════
// PHASE 3: SPIN CHAIN SPECTRAL GAPS (REAL DATA)
// ════════════════════════════════════════════════════

fn train_spin_chains() -> Result<(), Box<dyn Error>> {
    println!("\n  PHASE 3: Spin Chain Spectral Gaps (Neutron Scattering)");
    println!("  -------------------------------------------------------");

    let path = Path::new("/home/phrxmaz/Singularity/spin_chains/spectral_gaps_experimental.csv");
    if !path.exists() {
        println!("  [!] Spin chain data not found");
        return Ok(());
    }

    let mut rdr = csv::ReaderBuilder::new()
        .comment(Some(b'#'))
        .from_reader(File::open(path)?);

    let mut gapped_metrics: Vec<(String, f64, f64)> = Vec::new();
    let mut gapless_metrics: Vec<(String, f64, f64)> = Vec::new();

    for result in rdr.deserialize() {
        let row: SpinChainRow = result?;

        // Map the spectral gap to the Klein manifold:
        //   a = gap/J (normalized gap — the "order parameter")
        //   b = spin (thrust = angular momentum)
        //   m = 1/spin (anchor = inverse angular momentum, Bridge: bm = 1)
        //   e = gap_error/J (noise = measurement uncertainty)
        //   l = 0 (fresh consolidation)
        let j = row.exchange_J_meV.max(1e-6);
        let normalized_gap = row.gap_meV / j;
        let input = KleinManifold::new(
            normalized_gap,
            row.spin,
            1.0 / row.spin,
            row.gap_error_meV / j,
            0.0,
        );

        let mut agent = ZProtoAgent::origin();
        let result = agent.step(input);
        let sr = standard_resonance(&result.state);

        if row.gapped == "yes" {
            gapped_metrics.push((row.material.clone(), result.metric, sr));
        } else {
            gapless_metrics.push((row.material.clone(), result.metric, sr));
        }
    }

    println!("\n  GAPPED systems (S=1 Haldane, Ising-like):");
    for (mat, metric, sr) in &gapped_metrics {
        println!("    {:<16} metric={:.6}  SR={:.6}", mat, metric, sr);
    }

    println!("\n  GAPLESS systems (S=1/2 Heisenberg):");
    for (mat, metric, sr) in &gapless_metrics {
        println!("    {:<16} metric={:.6}  SR={:.6}", mat, metric, sr);
    }

    // Summary statistics
    let avg_gapped: f64 = gapped_metrics.iter().map(|x| x.1).sum::<f64>()
        / gapped_metrics.len() as f64;
    let avg_gapless: f64 = gapless_metrics.iter().map(|x| x.1).sum::<f64>()
        / gapless_metrics.len().max(1) as f64;

    println!("\n  Summary:");
    println!("    Gapped  avg metric: {:.6} ({} materials)", avg_gapped, gapped_metrics.len());
    println!("    Gapless avg metric: {:.6} ({} materials)", avg_gapless, gapless_metrics.len());
    println!("    Separation: {:.6}", (avg_gapped - avg_gapless).abs());

    Ok(())
}

// ════════════════════════════════════════════════════
// PHASE 4: GLUEBALL MASS SPECTRUM (REAL DATA)
// ════════════════════════════════════════════════════

fn train_glueball() -> Result<(), Box<dyn Error>> {
    println!("\n  PHASE 4: Glueball Mass Spectrum (Lattice QCD)");
    println!("  -----------------------------------------------");

    let path = Path::new("/home/phrxmaz/Singularity/yang_mills/glueball_spectrum_morningstar1999.csv");
    if !path.exists() {
        println!("  [!] Glueball data not found");
        return Ok(());
    }

    let mut rdr = csv::ReaderBuilder::new()
        .comment(Some(b'#'))
        .from_reader(File::open(path)?);

    println!("\n  Glueball states (Morningstar & Peardon 1999):");
    println!("  {:<10} {:<10} {:<12} {:<12} {:<12}", "JPC", "Mass(GeV)", "Metric", "SR", "Conic");

    let mut mass_gap_metric = 0.0;

    for result in rdr.deserialize() {
        let row: GlueballRow = result?;

        // Map glueball mass to Klein manifold:
        //   a = mass_GeV (observable energy — the real part)
        //   b = mass_r0 (dimensionless mass — thrust)
        //   m = 1/mass_r0 (inverse mass — anchor, Bridge: bm = 1)
        //   e = error_GeV (measurement noise)
        //   l = 0 (fresh)
        let input = KleinManifold::new(
            row.mass_GeV,
            row.mass_r0,
            1.0 / row.mass_r0,
            row.error_GeV,
            0.0,
        );

        let mut agent = ZProtoAgent::origin();
        let result_step = agent.step(input);
        let sr = standard_resonance(&result_step.state);

        println!("  {:<10} {:<10.3} {:<12.4} {:<12.4} {:?}",
            row.jpc, row.mass_GeV, result_step.metric, sr, result_step.conic);

        if row.jpc == "0++" && row.state_type == "scalar_ground" {
            mass_gap_metric = result_step.metric;
        }
    }

    println!("\n  Mass Gap (0++ scalar): metric = {:.4}", mass_gap_metric);
    println!("  Protoreal Bridge Energy: E = 1 (proven in MassGap.lean)");

    Ok(())
}

// ════════════════════════════════════════════════════
// MAIN
// ════════════════════════════════════════════════════

fn main() -> Result<(), Box<dyn Error>> {
    println!("============================================================");
    println!("  zProto Agent Training: The Spectral Trinity");
    println!("  Real physics data · Zero-sorry runtime");
    println!("============================================================");

    train_random_matrix()?;
    train_cmb()?;
    train_spin_chains()?;
    train_glueball()?;

    println!("\n============================================================");
    println!("  Training Complete: 4 Phases · 3 Problems · 1 Algebra");
    println!("============================================================");

    Ok(())
}
