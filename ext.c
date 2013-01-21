#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include "fermi/fermi.h"
#include "fermi/kstring.h"
#include "fermi/mag.h"

void fm6_ext_unitig(int unitig_k, int64_t l, int do_clean, 
                    char *seq, char *qual, void **tmp) {
  mag_t *g;
  g = fm6_api_unitig(unitig_k, l, seq);
  if (do_clean) {
    magopt_t *opt = mag_init_opt();
    opt->flag |= MOG_F_AGGRESSIVE | MOG_F_CLEAN;
    mag_g_clean(g, opt);
    free(opt);
  }
  *tmp = (void *) g;
}

void fm6_ext_unitig_write(void **tmp, char **unitigs) {
  int i;
  kstring_t out, all;
  mag_t *g = (mag_t *) *tmp;
  // write FASTQ results to kstring buffer
  out.l = out.m = 0; out.s = 0;
  all.l = all.m = 0; all.s = 0;
  for (i = 0; i < g->v.n; ++i) {
    if (g->v.a[i].len < 0) continue;
    mag_v_write(&g->v.a[i], &out);
    kputsn(out.s, out.l, &all);
  }
  free(out.s);
  free(*unitigs);
  mag_g_destroy(g);
  *unitigs = all.s;
}

void fm6_ext_exportseq(int64_t l, char *seq, char *qual, char **seqs) {
  kstring_t s, q, out;
  int64_t i;
  out.l = out.m = 0; out.s = 0;
  s.l = s.m = q.l = q.m = 0; s.s = q.s = 0;
  for (i = 0; i < l; ++i) {
    int c = seq[i];
    if (c == 0) {
      ksprintf(&out, "@%ld\n%s\n+\n%s\n", (long)i, s.s, q.s);
      s.l = q.l = 0;
    } else {
      if (c < 6) c = "$ACGTN"[c];
      kputc(c, &s);
      kputc(qual[i], &q);
    }
  }
  *seqs = out.s;
  free(s.s); free(q.s);
}

void free_pchar(char *tmp) {
  /* A simple wrapper to free *char. kstring_t allocates memory we may
     need to explicitly free from Python */
  free(tmp);
}
