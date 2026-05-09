"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              MONTE CARLO ALGORİTMASI - ÖZEL ELEMAN TESPİTİ                   ║
║                                                                              ║
║  Öğrenci No  : 1240505066                                                    ║
║  Algoritma   : Monte Carlo (Son iki hane: 66 → Çift)                         ║
║  Veri Hacmi  : n = 10^6 (Son rakam Y=6, Y≥5)                                 ║
║  Seed        : 1240505066                                                    ║
║  Koşul       : eleman mod 7 == 3                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import time
import math
import statistics

# ============================================================================
#                              SABİTLER
# ============================================================================

STUDENT_ID = 1240505066       # Öğrenci numarası
SEED = STUDENT_ID             # Rastgele sayı üretici tohum değeri
N = 10**6                     # Veri hacmi (1.000.000 eleman)
MODULO = 7                    # Mod değeri
TARGET_REMAINDER = 3          # Hedef kalan
NUM_RUNS = 100                # Algoritma çalıştırma sayısı
EPSILON = 0.01                # Hata toleransı (ε)

# Farklı örneklem boyutları (k değerleri)
K_VALUES = [100, 500, 1000, 5000, 10000, 50000, 100000]

# ============================================================================
#                         VERİ SETİ ÜRETİMİ
# ============================================================================

def generate_dataset(n, seed):
    rng = random.Random(seed)
    return [rng.randint(0, 10**7 - 1) for _ in range(n)]

# ============================================================================
#                      DETERMİNİSTİK SAYIM (GROUND TRUTH)
# ============================================================================

def deterministic_count(data, modulo, target):
    count = 0
    for x in data:
        if x % modulo == target:
            count += 1
    return count

# ============================================================================
#                       MONTE CARLO TAHMİN ALGORİTMASI
# ============================================================================

def monte_carlo_estimate(data, k, modulo, target, rng):
    n = len(data)
    sample_indices = rng.sample(range(n), k)
    
    sample_count = 0
    for i in sample_indices:
        if data[i] % modulo == target:
            sample_count += 1
            
    estimated_proportion = sample_count / k
    estimated_count = estimated_proportion * n
    return estimated_count, estimated_proportion

# ============================================================================
#                    TEORİK HATA OLASILIĞI HESABI
# ============================================================================

def hoeffding_bound(k, epsilon):
    return min(1.0, 2 * math.exp(-2 * k * epsilon**2))

def chebyshev_bound(k, epsilon, p):
    return min(1.0, (p * (1 - p)) / (k * epsilon**2))

# ============================================================================
#                          TEK DENEY ÇALIŞTIRMA
# ============================================================================

def run_single_experiment(data, true_count, k, epsilon, rng):
    n = len(data)
    true_proportion = true_count / n
    
    start_time = time.perf_counter()
    estimated_count, estimated_proportion = monte_carlo_estimate(data, k, MODULO, TARGET_REMAINDER, rng)
    elapsed_time = time.perf_counter() - start_time
    
    absolute_error = abs(estimated_proportion - true_proportion)
    relative_error = abs(estimated_count - true_count) / true_count if true_count > 0 else 0
    is_error = absolute_error > epsilon
    
    return {
        'estimated_count': estimated_count,
        'estimated_proportion': estimated_proportion,
        'absolute_error': absolute_error,
        'relative_error': relative_error,
        'is_error': is_error,
        'time': elapsed_time
    }

# ============================================================================
#                        100 DENEY ÇALIŞTIRMA
# ============================================================================

def run_100_experiments(data, true_count, k, epsilon):
    results = []
    for run_id in range(NUM_RUNS):
        rng = random.Random(SEED + run_id)
        result = run_single_experiment(data, true_count, k, epsilon, rng)
        results.append(result)
    
    errors = [r['absolute_error'] for r in results]
    rel_errors = [r['relative_error'] for r in results]
    times = [r['time'] for r in results]
    error_flags = [r['is_error'] for r in results]
    estimates = [r['estimated_count'] for r in results]
    
    true_proportion = true_count / len(data)
    
    return {
        'avg_error': statistics.mean(errors),
        'std_error': statistics.stdev(errors) if len(errors) > 1 else 0,
        'avg_time': statistics.mean(times),
        'std_time': statistics.stdev(times) if len(times) > 1 else 0,
        'empirical_error_rate': sum(error_flags) / NUM_RUNS,
        'error_count': sum(error_flags),
        'theoretical_hoeffding': hoeffding_bound(k, epsilon),
        'theoretical_chebyshev': chebyshev_bound(k, epsilon, true_proportion),
    }

def print_section(title):
    print("\n" + "─" * 74)
    print(f"  {title}")
    print("─" * 74)

# ============================================================================
#                              ANA PROGRAM
# ============================================================================

def main():
    print("\n╔" + "═" * 72 + "╗")
    print("║" + " MONTE CARLO ALGORİTMASI — ÖZEL ELEMAN TESPİTİ ".center(72) + "║")
    print("╚" + "═" * 72 + "╝")
    
    # ADIM 1: Veri seti üretimi
    print_section("ADIM 1: VERİ SETİ ÜRETİMİ VE GERÇEK DEĞER (GROUND TRUTH)")
    data = generate_dataset(N, SEED)
    true_count = deterministic_count(data, MODULO, TARGET_REMAINDER)
    true_proportion = true_count / N
    
    print(f"  Veri Hacmi       : {N:,} eleman")
    print(f"  Gerçek Sayı      : {true_count:,} eleman")
    print(f"  Gerçek Oran (p)  : {true_proportion:.6f}")
    
    # ADIM 2: Monte Carlo Deneyleri ve Teorik Hata Analizi
    print_section("ADIM 2: MONTE CARLO DENEYLERİ (100 ÇALIŞTIRMA) VE TEORİK HATA (P(error))")
    
    header = (
        f"  {'k':>8} │ {'Deneysel Hata':>13} │ {'Teorik Hoeffding':>16} │ {'Teorik Chebyshev':>16}"
    )
    print(header)
    print("  " + "─" * len(header.strip()))
    
    all_results = {}
    for k in K_VALUES:
        stats = run_100_experiments(data, true_count, k, EPSILON)
        all_results[k] = stats
        print(
            f"  {k:>8,} │ {stats['empirical_error_rate']:>13.4f} │ "
            f"{stats['theoretical_hoeffding']:>16.6f} │ "
            f"{stats['theoretical_chebyshev']:>16.6f}"
        )

    # ADIM 3: Zaman Analizi
    print_section("ADIM 3: ZAMAN ANALİZİ (RASTGELELİĞİN STANDART SAPMAYA ETKİSİ)")
    
    print(f"  {'k':>8} │ {'Ort. Süre (s)':>15} │ {'Süre Std. Sapma (s)':>20} │ {'CV (%)':>10}")
    print("  " + "─" * 60)
    for k in K_VALUES:
        r = all_results[k]
        cv = (r['std_time'] / r['avg_time'] * 100) if r['avg_time'] > 0 else 0
        print(
            f"  {k:>8,} │ {r['avg_time']:>15.6f} │ {r['std_time']:>20.6f} │ {cv:>9.2f}%"
        )
        
    print("\n  Program tamamlandı. Çıkan sonuçları kopyalayıp raporunuza ekleyebilirsiniz.")

if __name__ == "__main__":
    main()
