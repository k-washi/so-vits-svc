from pathlib import Path
import subprocess

def deepfilter_in_dir(input_dir, output_dir):
    input_dir = Path(input_dir)
    audio_files = sorted(list(input_dir.glob("*")))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = f"deep-filter-py"
    for audio_file in audio_files:
        cmd += f" {str(audio_file)}"
    
    cmd += f" -o {str(output_dir)}"
    subprocess.run(cmd, shell=True)
        
        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    
    args = parser.parse_args()
    deepfilter_in_dir(args.input_dir, args.output_dir)
    
    