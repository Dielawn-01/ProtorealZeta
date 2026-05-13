//! # zProto Trainer — Spectral Perception
//!
//! Trains the zProto agent on:
//! 1. Random matrix eigenvalues (GUE/GOE/GSE)
//! 2. Planck 2018 CMB power spectrum (TT/TE/EE)

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

// ════════════════════════════════════════════════════
// RANDOM MATRIX TRAINING
// ════════════════════════════════════════════════════

fn train_random_matrix() -> Result<(), Box<dyn Error>> {
    println!("\n  PHASE 1: Random Matrix Eigenvalues");
    println!("  -----------------------------------");

    let ensembles = vec!["gue", "goe", "gse"];
    let data_dir = Path::new("zProto/data/random_matrix");

    for ensemble in ensembles {
        let file_path = data_dir.join(format!("{}_eigenvalues.csv", ensemble));
        if !file_path.exists() {
            println!("  [!] Skipping {}: run generate_random_matrix.py first", ensemble);
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
// CMB TRAINING
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
        println!("\n  ▸ {} spectrum ({} multipoles, ℓ = {}..{})",
            stype, data.len(), data.first().unwrap().0, data.last().unwrap().0);

        let mut agent = ZProtoAgent::origin();
        let mut peak_resonances: Vec<(u32, f64, f64)> = Vec::new();
        let mut total_metric = 0.0;
        let mut step_count = 0;

        for (ell, d_ell, _sm, _sp) in data {
            // Map multipole to manifold:
            // ℓ becomes the "height" (like zeta zero imaginary part)
            // D_ℓ becomes the noise potential (observation magnitude)
            let ell_f = *ell as f64;
            let input = KleinManifold::new(
                0.0,            // a: unbiased
                ell_f,          // b: multipole as thrust
                1.0 / ell_f,    // m: 1/ℓ as anchor (Bridge: b·m = 1)
                d_ell / 1000.0, // e: D_ℓ scaled as noise potential
                0.0,            // l: fresh
            );

            let result = agent.step(input);
            total_metric += result.metric;
            step_count += 1;

            // Track resonance at acoustic peaks
            let resonance = standard_resonance(&result.state);
            if [220, 546, 800, 1120].contains(ell) {
                peak_resonances.push((*ell, resonance, result.metric));
            }
        }

        let avg_metric = total_metric / step_count as f64;
        let final_intuition = agent.frame.intuition();
        let final_graph = ObservationGraph::active_subgraph(&final_intuition);
        let final_chi = euler_perception(&final_graph);

        println!("    Avg Metric: {:.6} | Final χ: {} | Steps: {}",
            avg_metric, final_chi, step_count);

        if !peak_resonances.is_empty() {
            println!("    Acoustic Peak Resonances:");
            for (ell, res, met) in &peak_resonances {
                println!("      ℓ={}: SR={:.4}, metric={:.4}", ell, res, met);
            }
        }
    }

    Ok(())
}

// ════════════════════════════════════════════════════
// MAIN
// ════════════════════════════════════════════════════

fn main() -> Result<(), Box<dyn Error>> {
    println!("============================================================");
    println!("  zProto Agent Training: Spectral Perception");
    println!("============================================================");

    train_random_matrix()?;
    train_cmb()?;

    println!("\n============================================================");
    println!("  Training Complete!");
    println!("============================================================");

    Ok(())
}
