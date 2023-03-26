#include "simd_blitters.h"

#if defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H)
#include <immintrin.h>
#endif /* defined(HAVE_IMMINTRIN_H) && !defined(SDL_DISABLE_IMMINTRIN_H) */

#define BAD_AVX2_FUNCTION_CALL                                               \
    printf(                                                                  \
        "Fatal Error: Attempted calling an AVX2 function when both compile " \
        "time and runtime support is missing. If you are seeing this "       \
        "message, you have stumbled across a pygame bug, please report it "  \
        "to the devs!");                                                     \
    PG_EXIT(1)

/* helper function that does a runtime check for AVX2. It has the added
 * functionality of also returning 0 if compile time support is missing */
int
pg_has_avx2()
{
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
    return SDL_HasAVX2();
#else
    return 0;
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
}

/* This returns 1 when avx2 is available at runtime but support for it isn't
 * compiled in, 0 in all other cases */
int
pg_avx2_at_runtime_but_uncompiled()
{
    if (SDL_HasAVX2()) {
#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
        return 0;
#else
        return 1;
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
    }
    return 0;
}

/* just prints the first/lower 128 bits, in two chunks */
// static void
//_debug_print256_num(__m256i var, const char *msg)
//{
//    printf("%s\n", msg);
//    Uint64 *z = (Uint64 *)&var;
//    printf("l: %llX\n", *z);
//    printf("h: %llX\n", *(z + 1));
//}

/* Setup for RUN_AVX2_BLITTER */
#define SETUP_AVX2_BLITTER                                                \
    int width = info->width;                                              \
    int height = info->height;                                            \
                                                                          \
    Uint32 *srcp = (Uint32 *)info->s_pixels;                              \
    int srcskip = info->s_skip >> 2;                                      \
    int srcpxskip = info->s_pxskip >> 2;                                  \
                                                                          \
    Uint32 *dstp = (Uint32 *)info->d_pixels;                              \
    int dstskip = info->d_skip >> 2;                                      \
    int dstpxskip = info->d_pxskip >> 2;                                  \
                                                                          \
    int pre_8_width = width % 8;                                          \
    int post_8_width = width / 8;                                         \
                                                                          \
    __m256i *srcp256 = (__m256i *)info->s_pixels;                         \
    __m256i *dstp256 = (__m256i *)info->d_pixels;                         \
                                                                          \
    /* Since this operates on 8 pixels at a time, it needs to mask out */ \
    /* 0-7 pixels for partial loads/stores at periphery of blit area */   \
    __m256i _partial8_mask =                                              \
        _mm256_set_epi32(0x00, (pre_8_width > 6) ? 0x80000000 : 0x00,     \
                         (pre_8_width > 5) ? 0x80000000 : 0x00,           \
                         (pre_8_width > 4) ? 0x80000000 : 0x00,           \
                         (pre_8_width > 3) ? 0x80000000 : 0x00,           \
                         (pre_8_width > 2) ? 0x80000000 : 0x00,           \
                         (pre_8_width > 1) ? 0x80000000 : 0x00,           \
                         (pre_8_width > 0) ? 0x80000000 : 0x00);          \
                                                                          \
    __m256i pixels_src, pixels_dst;

/* Interface definition
 * Definitions needed: MACRO(SETUP_AVX2_BLITTER)
 * Input variables: None
 * Output variables: pixels_src, pixels_dst (containing raw pixel data)
 *
 * Operation: BLITTER_CODE takes pixels_src and pixels_dst and puts processed
 * results into pixels_dst
 */
#define RUN_AVX2_BLITTER(BLITTER_CODE)                                       \
    while (height--) {                                                       \
        for (int i = post_8_width; i > 0; i--) {                             \
            /* ==== load 8 pixels into AVX registers ==== */                 \
            pixels_src = _mm256_loadu_si256(srcp256);                        \
            pixels_dst = _mm256_loadu_si256(dstp256);                        \
                                                                             \
            {BLITTER_CODE}                                                   \
                                                                             \
            /* ==== store 8 pixels from AVX registers ==== */                \
            _mm256_storeu_si256(dstp256, pixels_dst);                        \
                                                                             \
            srcp256++;                                                       \
            dstp256++;                                                       \
        }                                                                    \
        srcp = (Uint32 *)srcp256;                                            \
        dstp = (Uint32 *)dstp256;                                            \
        if (pre_8_width > 0) {                                               \
            pixels_src = _mm256_maskload_epi32((int *)srcp, _partial8_mask); \
            pixels_dst = _mm256_maskload_epi32((int *)dstp, _partial8_mask); \
                                                                             \
            {BLITTER_CODE}                                                   \
                                                                             \
            /* ==== store 1-7 pixels from AVX registers ==== */              \
            _mm256_maskstore_epi32((int *)dstp, _partial8_mask, pixels_dst); \
                                                                             \
            srcp += srcpxskip * pre_8_width;                                 \
            dstp += dstpxskip * pre_8_width;                                 \
        }                                                                    \
                                                                             \
        srcp256 = (__m256i *)(srcp + srcskip);                               \
        dstp256 = (__m256i *)(dstp + dstskip);                               \
    }

/* Setup for RUN_16BIT_SHUFFLE_OUT */
#define SETUP_16BIT_SHUFFLE_OUT                                               \
    __m256i shuff_out_A =                                                     \
        _mm256_set_epi8(0x80, 23, 0x80, 22, 0x80, 21, 0x80, 20, 0x80, 19,     \
                        0x80, 18, 0x80, 17, 0x80, 16, 0x80, 7, 0x80, 6, 0x80, \
                        5, 0x80, 4, 0x80, 3, 0x80, 2, 0x80, 1, 0x80, 0);      \
                                                                              \
    __m256i shuff_out_B = _mm256_set_epi8(                                    \
        0x80, 31, 0x80, 30, 0x80, 29, 0x80, 28, 0x80, 27, 0x80, 26, 0x80, 25, \
        0x80, 24, 0x80, 15, 0x80, 14, 0x80, 13, 0x80, 12, 0x80, 11, 0x80, 10, \
        0x80, 9, 0x80, 8);                                                    \
                                                                              \
    __m256i shuff_src, shuff_dst, _shuff16_temp;

/* Interface definition
 * Definitions needed: MACRO(SETUP_16BIT_SHUFFLE_OUT)
 * Input variables: pixels_src, pixels_dst (containing raw pixel data)
 * Output variables: pixels_dst (containing processed and repacked pixel data)
 *
 * Operation: BLITTER_CODE takes shuff_src and shuff_dst and puts resulting
 * pixel data in shuff_dst
 */
#define RUN_16BIT_SHUFFLE_OUT(BLITTER_CODE)                    \
    /* ==== shuffle pixels out into two registers each, src */ \
    /* and dst set up for 16 bit math, like 0A0R0G0B ==== */   \
    shuff_src = _mm256_shuffle_epi8(pixels_src, shuff_out_A);  \
    shuff_dst = _mm256_shuffle_epi8(pixels_dst, shuff_out_A);  \
                                                               \
    {BLITTER_CODE}                                             \
                                                               \
    _shuff16_temp = shuff_dst;                                 \
                                                               \
    shuff_src = _mm256_shuffle_epi8(pixels_src, shuff_out_B);  \
    shuff_dst = _mm256_shuffle_epi8(pixels_dst, shuff_out_B);  \
                                                               \
    {BLITTER_CODE}                                             \
                                                               \
    /* ==== recombine A and B pixels ==== */                   \
    pixels_dst = _mm256_packus_epi16(_shuff16_temp, shuff_dst);

/* Interface definition
 * Input variables: "info" SDL_BlitInfo object
 * Output variables: `shuff_out_alpha` shuffle control mask.
 *
 * Takes a pixel in AVX2 registers like             [0][A][0][R][0][G][0][B]
 * (or however RGBA are aligned) and turns it into  [0][A][0][A][0][A][0][A]
 * */
#define ADD_SHUFFLE_OUT_ALPHA_CONTROL                                     \
    int _a_off = info->src->Ashift >> 2;                                  \
                                                                          \
    __m256i shuff_out_alpha = _mm256_set_epi8(                            \
        0x80, 8 + _a_off, 0x80, 8 + _a_off, 0x80, 8 + _a_off, 0x80,       \
        8 + _a_off, 0x80, 0 + _a_off, 0x80, 0 + _a_off, 0x80, 0 + _a_off, \
        0x80, 0 + _a_off, 0x80, 8 + _a_off, 0x80, 8 + _a_off, 0x80,       \
        8 + _a_off, 0x80, 8 + _a_off, 0x80, 0 + _a_off, 0x80, 0 + _a_off, \
        0x80, 0 + _a_off, 0x80, 0 + _a_off);

/* Divides each element in input mm256i by 255
 * See: https://stackoverflow.com/a/35286833/13816541 */
#define DO_AVX2_DIV255_U16(MM256I) \
    _mm256_srli_epi16(             \
        _mm256_mulhi_epu16(MM256I, _mm256_set1_epi16((short)0x8081)), 7);

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
alphablit_alpha_avx2_argb_no_surf_alpha_opaque_dst(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT
    ADD_SHUFFLE_OUT_ALPHA_CONTROL

    __m256i src_alpha, temp;

    /* The location of the destination's missing alpha channel can be masked
     * out by composing all the other channels' masks. */
    __m256i mask_out_alpha = _mm256_set1_epi32(
        (info->dst->Rmask | info->dst->Gmask | info->dst->Bmask));

    /* Original 'Straight Alpha' blending equation:
        --------------------------------------------
        dstRGB = (srcRGB * srcA) + (dstRGB * (1-srcA))
            dstA = srcA + (dstA * (1-srcA))

        We use something slightly different to simulate
        SDL1, as follows:
        dstRGB = (((dstRGB << 8) + (srcRGB - dstRGB) * srcA + srcRGB) >> 8)
            dstA = srcA + dstA - ((srcA * dstA) / 255);
    */

    /* Alpha blend procedure in this blitter:
        --------------------------------------
        srcRGBA = 16 bit interspersed source pixels
            i.e. [0][A][0][R][0][G][0][B]
        srcA = 16 bit interspersed alpha channel
            i.e. [0][A][0][A][0][A][0][A]
        As you can see, each pixel is moved out into 64 bits of register
        for processing. This blitter loads in 8 pixels at once, but
        processes 4 at a time (4x64=256 bits).

        * In this blitter, the interspersed RGBA layout is not determined,
        because the only thing that matters is alpha location, and a mask
        is provided to select alpha out of the registers. This way the blitter
        can easily support different pixel arrangements
        (RGBA, BGRA, ARGB, ABGR)

        Order of operations:
            temp = srcRGBA - dstRGBA
            temp *= srcA
            dstRGBA <<= 8
            dstRGBA += temp
            dstRGBA += srcRGBA
            dstRGBA >>= 8
        */

    RUN_AVX2_BLITTER(
        RUN_16BIT_SHUFFLE_OUT(
            src_alpha = _mm256_shuffle_epi8(shuff_src, shuff_out_alpha);
            temp = _mm256_sub_epi16(shuff_src, shuff_dst);
            temp = _mm256_mullo_epi16(temp, src_alpha);
            shuff_dst = _mm256_slli_epi16(shuff_dst, 8);
            shuff_dst = _mm256_add_epi16(shuff_dst, temp);
            shuff_dst = _mm256_add_epi16(shuff_dst, shuff_src);
            shuff_dst = _mm256_srli_epi16(shuff_dst, 8););

        /* It seems like the destination pixel alpha shouldn't matter, since
         * it is RGBX, but it has to be zero. I suspect this is a weak spot
         * in the other blitting routines, that they need alpha 0 from these
         * surfaces. */
        pixels_dst = _mm256_and_si256(pixels_dst, mask_out_alpha);)
}
#else
void
alphablit_alpha_avx2_argb_no_surf_alpha_opaque_dst(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
alphablit_alpha_avx2_argb_no_surf_alpha(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT
    ADD_SHUFFLE_OUT_ALPHA_CONTROL

    // Used to choose which byte to use when pulling from the RGBX buffer and
    // the dst alpha buffer. Chooses the RGBX buffer most of the time, chooses
    // A when on the low byte of the X 16 bit region.
    // RGB buffer looks like: [0][R][0][G][0][B][0][X]
    // Dst alpha looks like:  [0][A][0][A][0][A][0][A]
    // We want:               [0][R][0][G][0][B][0][A]
    // *ofc real memory layout differs based on pixelformat.
    __m256i combine_rgba_mask =
        _mm256_set1_epi64x(1LL << (((info->src->Ashift) * 2) + 7));

    __m256i src_alpha, temp, dst_alpha, new_dst_alpha;

    /*
     dstRGB = (((dstRGB << 8) + (srcRGB - dstRGB) * srcA + srcRGB) >> 8)
     dstA = srcA + dstA - ((srcA * dstA) / 255);
     */

    RUN_AVX2_BLITTER(RUN_16BIT_SHUFFLE_OUT(
        src_alpha = _mm256_shuffle_epi8(shuff_src, shuff_out_alpha);
        dst_alpha = _mm256_shuffle_epi8(shuff_dst, shuff_out_alpha);

        // figure out alpha
        temp = _mm256_mullo_epi16(src_alpha, dst_alpha);
        temp = DO_AVX2_DIV255_U16(temp);
        new_dst_alpha = _mm256_sub_epi16(dst_alpha, temp);
        new_dst_alpha = _mm256_add_epi16(src_alpha, new_dst_alpha);

        // if preexisting dst alpha is 0, src alpha should be set to 255
        // enforces that dest alpha 0 means "copy source RGB"
        // happens after real src alpha values used to calculate dst alpha
        // compares each 16 bit block to zeroes, yielding 0xFFFF or 0x0000--
        // shifts out bottom 8 bits to get to 0x00FF or 0x0000.
        dst_alpha = _mm256_cmpeq_epi16(dst_alpha, _mm256_setzero_si256());
        dst_alpha = _mm256_srli_epi16(dst_alpha, 8);
        src_alpha = _mm256_max_epu8(dst_alpha, src_alpha);

        // figure out RGB
        temp = _mm256_sub_epi16(shuff_src, shuff_dst);
        temp = _mm256_mullo_epi16(temp, src_alpha);
        temp = _mm256_add_epi16(temp, shuff_src);
        shuff_dst = _mm256_slli_epi16(shuff_dst, 8);
        shuff_dst = _mm256_add_epi16(shuff_dst, temp);
        shuff_dst = _mm256_srli_epi16(shuff_dst, 8);

        // blend together dstRGB and dstA
        shuff_dst =
            _mm256_blendv_epi8(shuff_dst, new_dst_alpha, combine_rgba_mask);))
}
#else
void
alphablit_alpha_avx2_argb_no_surf_alpha(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
alphablit_alpha_avx2_argb_surf_alpha(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT
    ADD_SHUFFLE_OUT_ALPHA_CONTROL

    // Used to choose which byte to use when pulling from the RGBX buffer and
    // the dst alpha buffer. Chooses the RGBX buffer most of the time, chooses
    // A when on the low byte of the X 16 bit region.
    // RGB buffer looks like: [0][R][0][G][0][B][0][X]
    // Dst alpha looks like:  [0][A][0][A][0][A][0][A]
    // We want:               [0][R][0][G][0][B][0][A]
    // *ofc real memory layout differs based on pixelformat.
    __m256i combine_rgba_mask =
        _mm256_set1_epi64x(1LL << (((info->src->Ashift) * 2) + 7));

    __m256i src_alpha, temp, dst_alpha, new_dst_alpha;

    int dst_alpha_offset = (info->dst->Amask ? 0 : 255);

    __m256i modulate_alpha = _mm256_set1_epi16(info->src_blanket_alpha);

    /*
     dstRGB = (((dstRGB << 8) + (srcRGB - dstRGB) * srcA + srcRGB) >> 8)
     dstA = srcA + dstA - ((srcA * dstA) / 255);
     */

    RUN_AVX2_BLITTER(RUN_16BIT_SHUFFLE_OUT(
        src_alpha = _mm256_shuffle_epi8(shuff_src, shuff_out_alpha);

        // src_alpha = src_alpha * module_alpha / 255
        src_alpha = _mm256_mullo_epi16(src_alpha, modulate_alpha);
        src_alpha = _mm256_srli_epi16(
            _mm256_mulhi_epu16(src_alpha, _mm256_set1_epi16((short)0x8081)),
            7);

        dst_alpha = _mm256_shuffle_epi8(shuff_dst, shuff_out_alpha);
        // if the destination is opaque, it takes the max of each alpha
        // with 255 otherwise it takes with the max with 0. This is
        // equivalent to if opaque: alpha = 255
        dst_alpha =
            _mm256_max_epi16(dst_alpha, _mm256_set1_epi16(dst_alpha_offset));

        // figure out alpha
        temp = _mm256_mullo_epi16(src_alpha, dst_alpha);
        temp = DO_AVX2_DIV255_U16(temp);
        new_dst_alpha = _mm256_sub_epi16(dst_alpha, temp);
        new_dst_alpha = _mm256_add_epi16(src_alpha, new_dst_alpha);

        // if preexisting dst alpha is 0, src alpha should be set to 255
        // enforces that dest alpha 0 means "copy source RGB"
        // happens after real src alpha values used to calculate dst alpha
        // compares each 16 bit block to zeroes, yielding 0xFFFF or
        // 0x0000-- shifts out bottom 8 bits to get to 0x00FF or 0x0000.
        dst_alpha = _mm256_cmpeq_epi16(dst_alpha, _mm256_setzero_si256());
        dst_alpha = _mm256_srli_epi16(dst_alpha, 8);
        src_alpha = _mm256_max_epu8(dst_alpha, src_alpha);

        // figure out RGB
        temp = _mm256_sub_epi16(shuff_src, shuff_dst);
        temp = _mm256_mullo_epi16(temp, src_alpha);
        temp = _mm256_add_epi16(temp, shuff_src);
        shuff_dst = _mm256_slli_epi16(shuff_dst, 8);
        shuff_dst = _mm256_add_epi16(shuff_dst, temp);
        shuff_dst = _mm256_srli_epi16(shuff_dst, 8);

        // blend together dstRGB and dstA
        shuff_dst =
            _mm256_blendv_epi8(shuff_dst, new_dst_alpha, combine_rgba_mask);))
}
#else
void
alphablit_alpha_avx2_argb_surf_alpha(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgba_mul_avx2(SDL_BlitInfo *info)
{
    __m256i mm256_two_five_fives = _mm256_set1_epi16(0x00FF);

    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT

    RUN_AVX2_BLITTER(RUN_16BIT_SHUFFLE_OUT(
        shuff_dst = _mm256_mullo_epi16(shuff_src, shuff_dst);
        shuff_dst = _mm256_add_epi16(shuff_dst, mm256_two_five_fives);
        shuff_dst = _mm256_srli_epi16(shuff_dst, 8);))
}
#else
void
blit_blend_rgba_mul_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgb_mul_avx2(SDL_BlitInfo *info)
{
    /* if either surface has a non-zero alpha mask use that as our mask */
    Uint32 amask = info->src->Amask | info->dst->Amask;

    __m256i mm256_alpha_mask = _mm256_set1_epi32(amask);

    __m256i mm256_two_five_fives = _mm256_set1_epi16(0x00FF);

    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT

    RUN_AVX2_BLITTER(
        pixels_src = _mm256_or_si256(pixels_src, mm256_alpha_mask);
        RUN_16BIT_SHUFFLE_OUT(
            shuff_dst = _mm256_mullo_epi16(shuff_src, shuff_dst);
            shuff_dst = _mm256_add_epi16(shuff_dst, mm256_two_five_fives);
            shuff_dst = _mm256_srli_epi16(shuff_dst, 8);))
}
#else
void
blit_blend_rgb_mul_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgba_add_avx2(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_dst = _mm256_adds_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgba_add_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgb_add_avx2(SDL_BlitInfo *info)
{
    /* if either surface has a non-zero alpha mask use that as our mask */
    Uint32 amask = info->src->Amask | info->dst->Amask;

    __m256i mm256_alpha_mask = _mm256_set1_epi32(amask);

    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_src =
                         _mm256_subs_epu8(pixels_src, mm256_alpha_mask);
                     pixels_dst = _mm256_adds_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgb_add_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgba_sub_avx2(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_dst = _mm256_subs_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgba_sub_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgb_sub_avx2(SDL_BlitInfo *info)
{
    /* if either surface has a non-zero alpha mask use that as our mask */
    Uint32 amask = info->src->Amask | info->dst->Amask;

    __m256i mm256_alpha_mask = _mm256_set1_epi32(amask);

    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_src =
                         _mm256_subs_epu8(pixels_src, mm256_alpha_mask);
                     pixels_dst = _mm256_subs_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgb_sub_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgba_max_avx2(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_dst = _mm256_max_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgba_max_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgb_max_avx2(SDL_BlitInfo *info)
{
    /* if either surface has a non-zero alpha mask use that as our mask */
    Uint32 amask = info->src->Amask | info->dst->Amask;

    __m256i mm256_alpha_mask = _mm256_set1_epi32(amask);

    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_src =
                         _mm256_subs_epu8(pixels_src, mm256_alpha_mask);
                     pixels_dst = _mm256_max_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgb_max_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgba_min_avx2(SDL_BlitInfo *info)
{
    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_dst = _mm256_min_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgba_min_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_rgb_min_avx2(SDL_BlitInfo *info)
{
    /* if either surface has a non-zero alpha mask use that as our mask */
    Uint32 amask = info->src->Amask | info->dst->Amask;

    __m256i mm256_alpha_mask = _mm256_set1_epi32(amask);

    SETUP_AVX2_BLITTER

    RUN_AVX2_BLITTER(pixels_src =
                         _mm256_adds_epu8(pixels_src, mm256_alpha_mask);
                     pixels_dst = _mm256_min_epu8(pixels_dst, pixels_src);)
}
#else
void
blit_blend_rgb_min_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */

#if defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
    !defined(SDL_DISABLE_IMMINTRIN_H)
void
blit_blend_premultiplied_avx2(SDL_BlitInfo *info)
{
    /*
     * Overall target blend (with colours and alpha represented
     * as values between 0 and 1) is:
     *
     * result = source.RGB + (dest.RGB * (1 - source.A))
     *
     * Optimised and rearranged for values between 0 and 255
     * the blend formula for a single colour channel is:
     *
     * (sC + dC - ((dC + 1) * sA >> 8))
     */

    __m256i src_alpha;
    __m256i mm256_ones = _mm256_set1_epi16(0x0001);

    SETUP_AVX2_BLITTER
    SETUP_16BIT_SHUFFLE_OUT
    ADD_SHUFFLE_OUT_ALPHA_CONTROL

    RUN_AVX2_BLITTER(RUN_16BIT_SHUFFLE_OUT(
        src_alpha = _mm256_shuffle_epi8(shuff_src, shuff_out_alpha);

        /* Source channels + Destination channels */
        shuff_src = _mm256_add_epi16(shuff_src, shuff_dst);

        /* Destination channels plus one */
        shuff_dst = _mm256_add_epi16(shuff_dst, mm256_ones);

        /* Each of the Destination channels plus one
         * multiplied by the Source Alpha channels. */
        shuff_dst = _mm256_mullo_epi16(src_alpha, shuff_dst);

        /* Right shift by 8bits on the result of the last two operations.
         * It is, combined with the addition of the ones above, effectively
         * a division operation by 255 for each channel putting us back in
         * the 8bit, 0 - 255 range (but still with 00) padding taking us up
         * to 16bit for now) */
        shuff_dst = _mm256_srli_epi16(shuff_dst, 8);

        /* Final subtraction completing the original olour channel blend
         * formula. We now have blended channel values sitting in the same
         * 16 bit, 00 padded arrangement of pixels as we did prior to the
         * blend. */
        shuff_dst = _mm256_sub_epi16(shuff_src, shuff_dst);))
}
#else
void
blit_blend_premultiplied_avx2(SDL_BlitInfo *info)
{
    BAD_AVX2_FUNCTION_CALL;
}
#endif /* defined(__AVX2__) && defined(HAVE_IMMINTRIN_H) && \
          !defined(SDL_DISABLE_IMMINTRIN_H) */
