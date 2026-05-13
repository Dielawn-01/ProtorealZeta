import argparse
import sys
import os
from goait.agent import GoaitAgent
import json

def main():
    parser = argparse.ArgumentParser(description="GOAIT: Generative Observatory for Adelic Intelligence & Topology")
    parser.add_argument("command", choices=["query", "geom", "forecast", "status"], help="Command to execute")
    parser.add_argument("--t", type=float, help="Spectral height for query")
    parser.add_argument("--points", type=str, help="JSON string of points for geom (e.g. '[[0,0], [1,1]]')")
    
    args = parser.parse_args()
    
    agent = GoaitAgent()
    
    if args.command == "query":
        if args.t is None:
            print("Error: --t is required for query")
            return
        result = agent.query_resonance(args.t)
        print(f"--- Spectral Resonance Report (t={args.t}) ---")
        print(json.dumps(result, indent=2))
        
    elif args.command == "geom":
        if args.points is None:
            print("Error: --points is required for geom")
            return
        points = json.loads(args.points)
        facts = agent.solve_geometric_construction(points)
        print(f"--- ZetaSpace Geometric Inference ---")
        for fact in facts:
            print(f" - {fact}")
            
    elif args.command == "status":
        print("--- GOAIT Node Status ---")
        print("Library: Goait (Rust Engine)")
        print("Agent: GoaitAgent (Trained on 2M Zeros)")
        print("Subnet: Potential GOAIT Subnet (UID: 1)")
        print("Local Hardware: Optimized")

if __name__ == "__main__":
    main()
