#include "simd_transform.h"

#if PG_ENABLE_ARM_NEON
// sse2neon.h is from here: https://github.com/DLTcollab/sse2neon
#include "include/sse2neon.h"
#endif /* PG_ENABLE_ARM_NEON */

/* This returns 1 when sse2 is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_sse2_at_runtime_but_uncompiled()
{
    if (SDL_HasSSE2()) {
#ifdef __SSE2__
        return 0;
#else
        return 1;
#endif /* __SSE2__ */
    }
    return 0;
}

/* This returns 1 when neon is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_neon_at_runtime_but_uncompiled()
{
    if (SDL_HasNEON()) {
#if PG_ENABLE_ARM_NEON
        return 0;
#else
        return 1;
#endif /* PG_ENABLE_ARM_NEON */
    }
    return 0;
}

#if (defined(__SSE2__) || defined(PG_ENABLE_ARM_NEON))

void
filter_shrink_X_SSE2_multi(Uint8 *srcpix, Uint8 *dstpix, int height,
                           int srcpitch, int dstpitch, int srcwidth,
                           int dstwidth)
{
    // FIXME TODO: assumes height is multiple of 2

    int srcdiff = srcpitch - (srcwidth * 4) + srcpitch;
    int dstdiff = dstpitch - (dstwidth * 4) + dstpitch;
    int x, y;

    __m128i src, src2, dst, dst2, accumulate, mm_xcounter, mm_xfrac;

    Uint8 *srcpix2 = srcpix + srcpitch;
    Uint8 *dstpix2 = dstpix + dstpitch;

    int xspace = 0x04000 * srcwidth / dstwidth; /* must be > 1 */

    __m128i xrecip = _mm_set1_epi16((Uint16)(0x40000000 / xspace));

    for (y = 0; y < height; y += 2) {
        accumulate = _mm_setzero_si128();
        int xcounter = xspace;
        for (x = 0; x < srcwidth; x++) {
            if (xcounter > 0x04000) {
                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());

                src2 = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix2),
                                         _mm_setzero_si128());
                src2 = _mm_slli_si128(src2, 8);  // replace with
                src = _mm_add_epi16(src, src2);  // _mm_unpacklo_epi64?

                accumulate = _mm_add_epi16(accumulate, src);
                srcpix += 4;
                srcpix2 += 4;
                xcounter -= 0x04000;
            }
            else {
                int xfrac = 0x04000 - xcounter;
                /* write out a destination pixel */

                mm_xcounter = _mm_set1_epi16(xcounter);
                mm_xfrac = _mm_set1_epi16(xfrac);

                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());

                src2 = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix2),
                                         _mm_setzero_si128());
                src2 = _mm_slli_si128(src2, 8);  // replace with
                src = _mm_add_epi16(src, src2);  // _mm_unpacklo_epi64?

                src = _mm_slli_epi16(src, 2);
                dst = _mm_mulhi_epu16(src, mm_xcounter);
                dst = _mm_add_epi16(dst, accumulate);
                accumulate = _mm_mulhi_epu16(src, mm_xfrac);

                dst = _mm_mulhi_epu16(dst, xrecip);
                dst = _mm_packus_epi16(dst, _mm_setzero_si128());
                _mm_storeu_si32(dstpix, dst);

                _mm_storeu_si32(dstpix2, _mm_srli_si128(dst, 4));

                dstpix += 4;
                dstpix2 += 4;
                srcpix += 4;
                srcpix2 += 4;
                xcounter = xspace - xfrac;
            }
        }
        srcpix += srcdiff;
        srcpix2 += srcdiff;
        dstpix += dstdiff;
        dstpix2 += dstdiff;
    }
}

void
filter_shrink_X_SSE2(Uint8 *srcpix, Uint8 *dstpix, int height, int srcpitch,
                     int dstpitch, int srcwidth, int dstwidth)
{
    int srcdiff = srcpitch - (srcwidth * 4);
    int dstdiff = dstpitch - (dstwidth * 4);
    int x, y;
    __m128i src, dst, accumulate, mm_xcounter, mm_xfrac;

    int xspace = 0x04000 * srcwidth / dstwidth; /* must be > 1 */
    __m128i xrecip = _mm_set1_epi16(0x40000000 / xspace);

    for (y = 0; y < height; y++) {
        accumulate = _mm_setzero_si128();
        int xcounter = xspace;
        for (x = 0; x < srcwidth; x++) {
            if (xcounter > 0x04000) {
                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());

                accumulate = _mm_add_epi16(accumulate, src);
                srcpix += 4;
                xcounter -= 0x04000;
            }
            else {
                int xfrac = 0x04000 - xcounter;
                /* write out a destination pixel */

                mm_xcounter = _mm_set1_epi16(xcounter);
                mm_xfrac = _mm_set1_epi16(xfrac);

                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());

                src = _mm_slli_epi16(src, 2);
                dst = _mm_mulhi_epu16(src, mm_xcounter);
                dst = _mm_add_epi16(dst, accumulate);
                accumulate = _mm_mulhi_epu16(src, mm_xfrac);

                dst = _mm_mulhi_epu16(dst, xrecip);
                dst = _mm_packus_epi16(dst, _mm_setzero_si128());
                _mm_storeu_si32(dstpix, dst);

                dstpix += 4;
                srcpix += 4;

                xcounter = xspace - xfrac;
            }
        }
        srcpix += srcdiff;
        dstpix += dstdiff;
    }
}

void
filter_shrink_Y_SSE2(Uint8 *srcpix, Uint8 *dstpix, int width, int srcpitch,
                     int dstpitch, int srcheight, int dstheight)
{
    int srcdiff = srcpitch - (width * 4);
    int dstdiff = dstpitch - (width * 4);
    int x, y;
    __m128i src, dst, mm_acc, mm_yfrac, mm_ycounter;

    int yspace = 0x04000 * srcheight / dstheight; /* must be > 1 */
    __m128i yrecip = _mm_set1_epi16(0x40000000 / yspace);
    int ycounter = yspace;

    Uint16 *templine;
    // TODO replace malloc+memset with calloc?
    /* allocate and clear a memory area for storing the accumulator line */
    templine = (Uint16 *)malloc(dstpitch * 2);
    if (templine == NULL)
        return;
    memset(templine, 0, dstpitch * 2);

    for (y = 0; y < srcheight; y++) {
        Uint16 *accumulate = templine;
        if (ycounter > 0x04000) {
            // TODO could iterate multipixel at a time
            for (x = 0; x < width; x++) {
                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());
                _mm_storeu_si64(
                    accumulate,
                    _mm_add_epi16(_mm_loadu_si64(accumulate), src));
                accumulate += 4;  // 4 Uint16s, so 8 bytes
                srcpix += 4;
            }
            ycounter -= 0x04000;
        }
        else {
            int yfrac = 0x04000 - ycounter;
            /* write out a destination line */
            // TODO could iterate multipixel at a time
            for (x = 0; x < width; x++) {
                src = _mm_unpacklo_epi8(_mm_loadu_si32(srcpix),
                                        _mm_setzero_si128());
                srcpix += 4;

                mm_acc = _mm_loadu_si64(accumulate);

                mm_yfrac = _mm_set1_epi16(yfrac);
                mm_ycounter = _mm_set1_epi16(ycounter);

                src = _mm_slli_epi16(src, 2);
                dst = _mm_mulhi_epu16(src, mm_yfrac);
                src = _mm_mulhi_epu16(src, mm_ycounter);

                _mm_storeu_si64(accumulate, dst);
                accumulate += 4;  // 4 Uint16s, so 8 bytes

                dst = _mm_add_epi16(src, mm_acc);
                dst = _mm_mulhi_epu16(dst, yrecip);
                dst = _mm_packus_epi16(dst, _mm_setzero_si128());
                _mm_storeu_si32(dstpix, dst);
                dstpix += 4;
            }
            dstpix += dstdiff;
            ycounter = yspace - yfrac;
        }
        srcpix += srcdiff;
    } /* for (int y = 0; y < srcheight; y++) */

    /* free the temporary memory */
    free(templine);
}

void
filter_expand_X_SSE2(Uint8 *srcpix, Uint8 *dstpix, int height, int srcpitch,
                     int dstpitch, int srcwidth, int dstwidth)
{
    int dstdiff = dstpitch - (dstwidth * 4);
    int *xidx0, *xmult_combined;
    int x, y;
    const int factorwidth = 8;

#ifdef _MSC_VER
    /* Make MSVC static analyzer happy by assuring dstwidth >= 2 to suppress
     * a false analyzer report */
    __analysis_assume(dstwidth >= 2);
#endif

    /* Allocate memory for factors */
    xidx0 = malloc(dstwidth * 4);
    if (xidx0 == 0)
        return;
    xmult_combined = (int *)malloc(dstwidth * factorwidth);
    if (xmult_combined == 0) {
        free(xidx0);
        return;
    }

    /* Create multiplier factors and starting indices and put them in arrays */
    for (x = 0; x < dstwidth; x++) {
        // Could it be worth it to reduce the fixed point there to fit
        // inside 16 bits (0xFF), and then pack xidx0 in with mult factors?
        int xm1 = 0x100 * ((x * (srcwidth - 1)) % dstwidth) / dstwidth;
        int xm0 = 0x100 - xm1;
        xidx0[x] = x * (srcwidth - 1) / dstwidth;

        // packs xm0 and xm1 scaling factors into a combined array, for easy
        // loading
        xmult_combined[x * 2] = xm0 | (xm0 << 16);
        xmult_combined[x * 2 + 1] = xm1 | (xm1 << 16);
    }

    __m128i src, mmxid, mult0, mult1, multcombined, dst;

    /* Do the scaling in raster order so we don't trash the cache */
    for (y = 0; y < height; y++) {
        Uint8 *srcrow0 = srcpix + y * srcpitch;
        for (x = 0; x < dstwidth; x++) {
            Uint8 *src_p =
                srcrow0 + xidx0[x] * 4;  // *8 now because of factorwidth?

            src =
                _mm_unpacklo_epi8(_mm_loadu_si64(src_p), _mm_setzero_si128());

            // uses combined multipliers against 2 src pixels
            // xm0 against src[0-3] (1 px), and xm1 against xrc[4-7] (1 px)
            multcombined = _mm_shuffle_epi32(
                _mm_loadu_si64(xmult_combined + x * 2), 0b01010000);

            src = _mm_mullo_epi16(src, multcombined);

            dst = _mm_bsrli_si128(src, 8);
            dst = _mm_add_epi16(src, dst);
            dst = _mm_srli_epi16(dst, 8);
            dst = _mm_packus_epi16(dst, _mm_setzero_si128());
            _mm_storeu_si32(dstpix, dst);

            dstpix += 4;
        }
        dstpix += dstdiff;
    }

    /* free memory */
    free(xidx0);
    free(xmult_combined);
}

void
filter_expand_Y_SSE2(Uint8 *srcpix, Uint8 *dstpix, int width, int srcpitch,
                     int dstpitch, int srcheight, int dstheight)
{
    int x, y;

    __m128i src0, src1, dst, ymult0_mm, ymult1_mm;

    for (y = 0; y < dstheight; y++) {
        int yidx0 = y * (srcheight - 1) / dstheight;
        Uint8 *srcrow0 = srcpix + yidx0 * srcpitch;
        Uint8 *srcrow1 = srcrow0 + srcpitch;
        int ymult1 = 0x0100 * ((y * (srcheight - 1)) % dstheight) / dstheight;
        int ymult0 = 0x0100 - ymult1;

        ymult0_mm = _mm_set1_epi16(ymult0);
        ymult1_mm = _mm_set1_epi16(ymult1);

        for (x = 0; x < width; x++) {
            src0 = _mm_unpacklo_epi8(_mm_loadu_si32(srcrow0),
                                     _mm_setzero_si128());
            src1 = _mm_unpacklo_epi8(_mm_loadu_si32(srcrow1),
                                     _mm_setzero_si128());

            src0 = _mm_mullo_epi16(src0, ymult0_mm);
            src1 = _mm_mullo_epi16(src1, ymult1_mm);

            dst = _mm_add_epi16(src0, src1);
            dst = _mm_srli_epi16(dst, 8);
            dst = _mm_packus_epi16(dst, _mm_setzero_si128());
            _mm_storeu_si32(dstpix, dst);

            srcrow0 += 4;
            srcrow1 += 4;
            dstpix += 4;
        }
        Uint8 *dstrow = dstpix + y * dstpitch;
    }
}

#endif /* __SSE2__ || PG_ENABLE_ARM_NEON*/
