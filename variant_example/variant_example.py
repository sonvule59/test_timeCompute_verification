import subprocess
import os
os.environ["PATH"] = "/opt/homebrew/opt/llvm/bin:" + os.environ.get("PATH", "")
# Compile all variants
print("Compiling variants...")
subprocess.run(["bash", "compile_variants.sh"], check=True)

# Run variants and capture output
print("Running variants and scoring...")
result = subprocess.run(["bash", "run_variants.sh"], capture_output=True, text=True)
print(result.stdout)

# Parse summary from the run script output
scores = {}
summary_found = False
for line in result.stdout.splitlines():
    if "----- Summary" in line:
        summary_found = True
        continue
    if summary_found and ":" in line:
        name, score = line.split(": Score =")
        name = name.strip()
        score = float(score.strip())
        scores[name] = score

if scores:
    # Pick the best variant
    best = max(scores, key=scores.get)
    print(f"\nBest OpenMP variant: {best} (Score: {scores[best]:.1f})")
else:
    print("No valid scores found. Please check output above for errors.")

import csv
with open("variant_scores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["variant", "score"])
    for k, v in scores.items():
        writer.writerow([k, v])

print("Scores saved to variant_scores.csv.")
