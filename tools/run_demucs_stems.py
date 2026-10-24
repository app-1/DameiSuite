"""
Damei AI Stem Separation Pipeline
File: run_demucs_stems.py
Description: Separates your mix audio and reference track into identical 24-bit WAV stem quads
             (Vocals, Drums, Bass, Other) using Meta AI's HTDemucs v4 Fine-Tuned (htdemucs_ft)
             ready for REAPER side-by-side shootout analysis.
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

DEFAULT_MODEL = "htdemucs_ft"

STEM_MAP = {
    "vocals": "Vocals",
    "drums": "Drums",
    "bass": "Bass",
    "other": "Other"
}

def run_demucs(input_file: Path, out_dir: Path, model: str = DEFAULT_MODEL, device: str = None) -> Path:
    """Run demucs CLI separation on a single audio file."""
    print(f"\n[Damei Demucs] Processing: {input_file.name}")
    print(f"[Damei Demucs] Model: {model} | Target: 24-bit PCM WAV")
    
    cmd = [
        sys.executable, "-m", "demucs.separate",
        "-n", model,
        "--int24",
        "--clip-mode", "clamp",
        "-o", str(out_dir),
        str(input_file)
    ]
    if device:
        cmd.extend(["-d", device])
        
    res = subprocess.run(cmd)
    if res.returncode != 0:
        raise RuntimeError(f"Demucs separation failed for {input_file} (exit code {res.returncode})")
        
    # Result folder is out_dir / model / input_stem_name
    track_name = input_file.stem
    result_dir = out_dir / model / track_name
    if not result_dir.exists():
        # Fallback to direct name match
        matches = list(out_dir.glob(f"**/{track_name}"))
        if matches:
            result_dir = matches[0]
        else:
            raise FileNotFoundError(f"Could not locate separated stems folder in {out_dir}")
            
    return result_dir

def organize_stems(stem_dir: Path, target_dir: Path, prefix: str):
    """
    Standardize stem filenames to:
    {prefix}_Vocals.wav, {prefix}_Drums.wav, {prefix}_Bass.wav, {prefix}_Other.wav
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    created = []
    
    for raw_name, clean_name in STEM_MAP.items():
        candidates = list(stem_dir.glob(f"*{raw_name}*.wav"))
        if candidates:
            src = candidates[0]
            dst_name = f"{prefix}_{clean_name}.wav"
            dst = target_dir / dst_name
            shutil.copy2(src, dst)
            print(f"  ✓ Exported: {dst.name}")
            created.append(dst)
        else:
            print(f"  ⚠ Warning: Could not find '{raw_name}' in {stem_dir}")
            
    return created

def main():
    parser = argparse.ArgumentParser(description="Damei AI Stem Separation Pipeline (HTDemucs v4)")
    parser.add_argument("--mix", type=str, help="Path to your mix bounce WAV file")
    parser.add_argument("--ref", type=str, help="Path to professional reference track WAV/MP3")
    parser.add_argument("--out", type=str, default="./StemShootout", help="Output directory for organized stems")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Demucs model checkpoint (default: htdemucs_ft)")
    parser.add_argument("--device", type=str, default=None, help="Device to use ('cuda', 'cpu')")
    
    args = parser.parse_args()
    
    if not args.mix and not args.ref:
        print("Usage: python run_demucs_stems.py --mix <MyMix.wav> --ref <Reference.wav> [--out <dest_folder>]")
        sys.exit(1)
        
    out_path = Path(args.out).resolve()
    temp_dir = out_path / "_raw_demucs"
    out_path.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print(" 🚀 DAMEI AI STEM SEPARATION PIPELINE (HTDemucs v4)")
    print("=" * 70)
    print(f"Output Directory: {out_path}")
    
    mix_stems = []
    ref_stems = []
    
    if args.mix:
        mix_file = Path(args.mix).resolve()
        if not mix_file.exists():
            print(f"Error: Mix file not found: {mix_file}")
            sys.exit(1)
        stems_dir = run_demucs(mix_file, temp_dir, args.model, args.device)
        print(f"\n[Damei Demucs] Organizing Mix Stems...")
        mix_stems = organize_stems(stems_dir, out_path, prefix="My")
        
    if args.ref:
        ref_file = Path(args.ref).resolve()
        if not ref_file.exists():
            print(f"Error: Reference file not found: {ref_file}")
            sys.exit(1)
        stems_dir = run_demucs(ref_file, temp_dir, args.model, args.device)
        print(f"\n[Damei Demucs] Organizing Reference Stems...")
        ref_stems = organize_stems(stems_dir, out_path, prefix="Ref")
        
    # Clean up raw subfolder
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass
        
    print("\n" + "=" * 70)
    print(" ✨ SEPARATION COMPLETE!")
    print("=" * 70)
    print(f"All stems time-aligned & organized in: {out_path}")
    print("\nFiles ready for REAPER:")
    if mix_stems:
        print("  [MY MIX]:")
        for s in mix_stems:
            print(f"    - {s.name}")
    if ref_stems:
        print("  [REFERENCE MIX]:")
        for s in ref_stems:
            print(f"    - {s.name}")
            
    print("\nNext: Run 'Damei_Setup_Stem_Shootout.lua' in REAPER and drop these stems into their tracks!")

if __name__ == "__main__":
    main()
