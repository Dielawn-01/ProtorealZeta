//! # zProto Trainer — Spectral Perception
//!
//! Trains the zProto agent on random matrix eigenvalue datasets.
//!
//! The goal is to see if the agent's internal state (chi, conic, metric)
//! stabilizes differently for GUE, GOE, and GSE ensembles.

use zproto::agent::ZProtoAgent;
use zproto::fiber::fiber_project;
use zproto::graph::{ObservationGraph, euler_perception};
use serde::Deserialize;
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::path::Path;

#[derive(Debug, Deserialize)]
struct EigenvalueRow {
    ensemble: String,
    matrix_size: usize,
    sample: usize,
    index: usize,
    eigenvalue: f64,
}

fn main() -> Result<(), Box<dyn Error>> {
    println!("============================================================");
    println!("  zProto Agent Training: Spectral Perception");
    println!("============================================================");

    let ensembles = vec!["gue", "goe", "gse"];
    let data_dir = Path::new("zProto/data/random_matrix");

    for ensemble in ensembles {
        let file_path = data_dir.join(format!("{}_eigenvalues.csv", ensemble));
        if !file_path.exists() {
            println!("  [!] Skipping {}: File not found", ensemble);
            continue;
        }

        println!("\n▸ Processing {} ensemble...", ensemble.to_uppercase());
        
        let mut rdr = csv::Reader::from_reader(File::open(file_path)?);
        
        // Group by sample
        let mut samples: HashMap<(usize, usize), Vec<f64>> = HashMap::new();
        for result in rdr.deserialize() {
            let row: EigenvalueRow = result?;
            samples.entry((row.matrix_size, row.sample)).or_default().push(row.eigenvalue);
        }

        // Stats tracking
        let mut total_metric = 0.0;
        let mut chi_counts: HashMap<i64, usize> = HashMap::new();
        let mut conic_counts: HashMap<String, usize> = HashMap::new();
        let mut active_counts: HashMap<usize, usize> = HashMap::new();
        let mut sample_count = 0;

        for ((_size, _sample_id), eigs) in &samples {
            let mut agent = ZProtoAgent::origin();
            let mut last_result = None;
            let mut last_intuition = None;

            for eig in eigs {
                let input = fiber_project(eig.abs().max(1e-6));
                let step_res = agent.step(input);
                last_result = Some(step_res);
                last_intuition = Some(agent.frame.intuition());
            }

            if let Some(result) = last_result {
                total_metric += result.metric;
                
                // Perceive the INTUITION graph
                let intuition_graph = ObservationGraph::active_subgraph(&last_intuition.unwrap());
                let intuition_chi = euler_perception(&intuition_graph);
                
                *chi_counts.entry(intuition_chi).or_default() += 1;
                *conic_counts.entry(format!("{:?}", result.conic)).or_default() += 1;
                
                // Debug: what components are active?
                let active_count = (result.state.a.abs() > 1e-12) as usize
                    + (result.state.b.abs() > 1e-12) as usize
                    + (result.state.m.abs() > 1e-12) as usize
                    + (result.state.e.abs() > 1e-12) as usize
                    + (result.state.l.abs() > 1e-12) as usize;
                *active_counts.entry(active_count).or_default() += 1;
            }
            sample_count += 1;
        }

        println!("  Total samples: {}", sample_count);
        println!("  Avg Convergence Metric: {:.6}", total_metric / sample_count as f64);
        println!("  Active Components Distribution:");
        for (count, freq) in active_counts {
            println!("    {} components: {}%", count, (freq * 100) / sample_count);
        }
        println!("  Euler Perception (χ) Distribution:");
        for (chi, count) in chi_counts {
            println!("    χ = {}: {}%", chi, (count * 100) / sample_count);
        }
        println!("  Conic Distribution:");
        for (conic, count) in conic_counts {
            println!("    {}: {}%", conic, (count * 100) / sample_count);
        }
    }

    println!("\n============================================================");
    println!("  Training Complete!");
    println!("============================================================");

    Ok(())
}
