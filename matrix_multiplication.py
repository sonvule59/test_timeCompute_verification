import torch
import os
import time

# Configuration
variants = [1, 2, 4]  # Thread counts simulating OpenMP parallel strategies
small_size = 500  # Small matrix for profiling
large_size = 2000  # Large matrix for final application
num_trials = 5  # Average over multiple runs for stable timing
tolerance = 1e-3  # Floating-point tolerance for correctness

# Generate input matrices
A_small = torch.randn(small_size, small_size)
B_small = torch.randn(small_size, small_size)
A_large = torch.randn(large_size, large_size)
B_large = torch.randn(large_size, large_size)

# Step 1: Profile and verify variants on small input
times = {}
checksums = {}
print("Profiling variants on small input ({}x{} matrix):".format(small_size, small_size))
for v in variants:
    torch.set_num_threads(v)
    # Note: OMP_NUM_THREADS omitted as PyTorch uses its own threading
    total_time = 0
    for _ in range(num_trials):
        start = time.time()
        C = torch.mm(A_small, B_small)
        total_time += time.time() - start
    times[v] = total_time / num_trials
    checksums[v] = C.sum().item()
    print(f"Threads: {v}, Avg Time: {times[v]:.4f}s, Checksum: {checksums[v]:.4f}")

# Step 2: Correctness verification (compare to single-threaded)
ref_checksum = checksums[1]
correct_variants = [
    v for v in variants
    if abs(checksums[v] - ref_checksum) <= tolerance * abs(ref_checksum)
]
print("\nCorrect variants (within tolerance):", correct_variants)

# Step 3: Select best variant
if not correct_variants:
    print("Error: No correct variants found.")
    exit(1)
best_variant = min(correct_variants, key=lambda v: times[v])
print(f"Selected best variant: {best_variant} threads (Time: {times[best_variant]:.4f}s)")

# Step 4: Apply to large input and compare to single-threaded
print("\nApplying to large input ({}x{} matrix):".format(large_size, large_size))
torch.set_num_threads(best_variant)
total_time_best = 0
for _ in range(num_trials):
    start = time.time()
    torch.mm(A_large, B_large)
    total_time_best += time.time() - start
avg_time_best = total_time_best / num_trials
print(f"Best variant ({best_variant} threads): {avg_time_best:.4f}s")

torch.set_num_threads(1)
total_time_seq = 0
for _ in range(num_trials):
    start = time.time()
    torch.mm(A_large, B_large)
    total_time_seq += time.time() - start
avg_time_seq = total_time_seq / num_trials
print(f"Single-threaded: {avg_time_seq:.4f}s")

# Step 5: Report benefit
benefit = (avg_time_seq - avg_time_best) / avg_time_seq * 100
print(f"Performance benefit: {benefit:.2f}% faster than single-threaded")