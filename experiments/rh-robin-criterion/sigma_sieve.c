/* Segmented exact sum-of-divisors sieve with conservative Robin flagging.
 *
 * For each segment [L, R) it computes sigma(n) exactly in uint64 via the
 * divisor-pair enumeration  sigma(n) = sum_{d | n, d*d <= n} (d + n/d),
 * counting d exactly once when d*d = n.  All arithmetic on sigma is integer
 * and exact; doubles appear ONLY in the flagging filter, which uses a
 * per-segment threshold T (read from a table certified in Python) with a
 * 1e-9 relative safety margin, so it can over-flag but never miss a true
 * violation.  Flagged n are re-decided rigorously in Python.
 *
 * Usage: sigma_sieve THRESHOLD_TABLE OUT_SEGMENTS OUT_CANDIDATES [DUMP_FILE]
 *   THRESHOLD_TABLE: lines "L R T_hexfloat" (contiguous segments, L >= 5041)
 *   OUT_SEGMENTS:    per-segment checkpoint CSV (appended as we go):
 *                    L,R,argmax_n,sigma(argmax_n),sigma_sum_mod2^64,n_flagged
 *   OUT_CANDIDATES:  one line "n sigma" per flagged n
 *   DUMP_FILE:       optional; if given, every "n sigma" of the FIRST segment
 *                    is dumped there (for cross-validation) and we exit.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s table out_seg out_cand [dump]\n", argv[0]); return 2; }
    FILE *tab = fopen(argv[1], "r");
    if (!tab) { perror("table"); return 2; }
    FILE *oseg = fopen(argv[2], "a");
    FILE *ocand = fopen(argv[3], "a");
    FILE *dump = (argc > 4) ? fopen(argv[4], "w") : NULL;
    if (!oseg || !ocand) { perror("out"); return 2; }

    uint64_t *sig = NULL; size_t cap = 0;
    uint64_t L, R; double T;
    clock_t t0 = clock();
    while (fscanf(tab, "%llu %llu %la", (unsigned long long*)&L,
                  (unsigned long long*)&R, &T) == 3) {
        uint64_t S = R - L;
        if (S > cap) { free(sig); sig = malloc(S * sizeof *sig); cap = S; if (!sig) { perror("malloc"); return 2; } }
        memset(sig, 0, S * sizeof *sig);
        uint64_t dmax = (uint64_t)sqrt((double)(R - 1)) + 2;
        while (dmax * dmax > R - 1) dmax--;      /* exact integer sqrt of R-1 */
        for (uint64_t d = 1; d <= dmax; d++) {
            uint64_t m = (L + d - 1) / d * d;    /* first multiple of d >= L */
            if (m < d * d) m = d * d;            /* enforce d <= sqrt(m)     */
            for (; m < R; m += d) {
                uint64_t q = m / d;
                sig[m - L] += (q == d) ? d : d + q;
            }
        }
        if (dump) {
            for (uint64_t n = L; n < R; n++)
                fprintf(dump, "%llu %llu\n", (unsigned long long)n,
                        (unsigned long long)sig[n - L]);
            fclose(dump);
            return 0;
        }
        /* scan: exact checksum, argmax of sigma(n)/n, conservative flagging */
        uint64_t sum = 0, best_n = L, best_sig = 0, nflag = 0;
        double best_ratio = -1.0;
        for (uint64_t n = L; n < R; n++) {
            uint64_t s = sig[n - L];
            sum += s;                             /* mod 2^64 by design */
            double r = (double)s / (double)n;
            if (r > best_ratio) { best_ratio = r; best_n = n; best_sig = s; }
            if ((double)s >= T * (double)n) {     /* conservative filter */
                fprintf(ocand, "%llu %llu\n", (unsigned long long)n,
                        (unsigned long long)s);
                nflag++;
            }
        }
        fprintf(oseg, "%llu,%llu,%llu,%llu,%llu,%llu\n",
                (unsigned long long)L, (unsigned long long)R,
                (unsigned long long)best_n, (unsigned long long)best_sig,
                (unsigned long long)sum, (unsigned long long)nflag);
        fflush(oseg); fflush(ocand);              /* checkpoint per segment */
    }
    fprintf(stderr, "done in %.1fs\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    free(sig);
    return 0;
}
