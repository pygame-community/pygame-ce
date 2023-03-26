

int
pg_sse2_at_runtime_but_uncompiled();
int
pg_neon_at_runtime_but_uncompiled();
int
pg_avx2_at_runtime_but_uncompiled();
int
pg_has_avx2();

/* This returns True if either SSE2 or NEON is present at runtime.
 * Relevant because they use the same codepaths. Only the relevant runtime
 * SDL cpu feature check is compiled in.*/
int
pg_HasSSE_NEON();
