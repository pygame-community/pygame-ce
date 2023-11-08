#define PYGAMEAPI_TEXTURE_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgTexture_Type;

#define TEXTURE_ERROR_CHECK(x)                       \
    if (x < 0) {                                      \
        return RAISE(pgExc_SDLError, SDL_GetError()); \
    }                                                 \

#define pgTexture_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgTexture_Type))

static Uint32
format_from_depth(int depth) {
    Uint32 Rmask, Gmask, Bmask, Amask;
    if (depth == 0 || depth == 32) {
        Rmask = 0xFF << 16;
        Gmask = 0xFF << 8;
        Bmask = 0xFF;
        Amask = 0xFF << 24;
    }
    else if (depth == 16) {
        Rmask = 0xF << 8;
        Gmask = 0xF << 4;
        Bmask = 0xF;
        Amask = 0xF << 12;
    }
    else {
        RAISE(PyExc_ValueError, "no standard masks exist for given bitdepth with alpha");
        return -1;
    }
    return SDL_MasksToPixelFormatEnum(depth, Rmask, Gmask, Bmask, Amask);
}

// From surface.c
static inline PyObject *
_get_rect_helper(PyObject *rect, PyObject *const *args, Py_ssize_t nargs,
                 PyObject *kwnames)
{
    if (nargs > 0) {
        Py_DECREF(rect);
        return PyErr_Format(PyExc_TypeError,
                            "get_rect only accepts keyword arguments");
    }
    if (rect && kwnames) {
        Py_ssize_t i, sequence_len;
        PyObject **sequence_items;
        sequence_items = PySequence_Fast_ITEMS(kwnames);
        sequence_len = PyTuple_GET_SIZE(kwnames);
        
        for (i = 0; i < sequence_len; ++i) {
            if ((PyObject_SetAttr(rect, sequence_items[i], args[i]) == -1)) {
                Py_DECREF(rect);
                return NULL;
            }
        }
    }
    return rect;
}

static PyObject *
texture_get_alpha(pgTextureObject *self, void *closure) {
    Uint8 alpha;
    TEXTURE_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &alpha));
    return PyLong_FromLong(alpha);
}

static int
texture_set_alpha(pgTextureObject *self, PyObject *arg, void *closure) {
    if (PyLong_Check(arg)) {
        unsigned long longval = PyLong_AsUnsignedLong(arg);
        TEXTURE_ERROR_CHECK(SDL_SetTextureAlphaMod(self->texture, (Uint8)longval))
        return 0;
    }
    return -1;
}

static PyObject *
texture_get_blend_mode(pgTextureObject *self, void *closure) {
    SDL_BlendMode blend_mode;
    TEXTURE_ERROR_CHECK(SDL_GetTextureBlendMode(self->texture, &blend_mode));
    return PyLong_FromLong((long) blend_mode);
}

static int
texture_set_blend_mode(pgTextureObject *self, PyObject *arg, void *closure) {
    TEXTURE_ERROR_CHECK(SDL_SetTextureBlendMode(self->texture, (int) PyLong_AsLong(arg)))
    return 0;
}

static PyObject *
texture_get_color(pgTextureObject *self, void *closure) {
    Uint8 color[4];
    TEXTURE_ERROR_CHECK(SDL_GetTextureColorMod(self->texture, &color[0], &color[1], &color[2]));
    color[3] = 255;
    return pgColor_NewLength(color, 4);
}

static int
texture_set_color(pgTextureObject *self, PyObject *arg, void *closure) {
    Uint8 color[4];
    if (!pg_RGBAFromObjEx(arg, color, PG_COLOR_HANDLE_ALL)) {
        return -1;
    }
    TEXTURE_ERROR_CHECK(SDL_SetTextureColorMod(self->texture, color[0], color[1], color[2]))
    return 0;
}

static PyObject *
texture_get_rect(pgTextureObject *self, PyObject *const *args, Py_ssize_t nargs, PyObject *kwargs) {
    PyObject *rect = pgRect_New4(0, 0, self->width, self->height);
    return _get_rect_helper(rect, args, nargs, kwargs);
}

static PyObject *
texture_draw(pgTextureObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *srcrectobj = Py_None, *dstrectobj = Py_None, *originobj = Py_None;
    SDL_Rect srcrect, *srcrectptr = NULL;
    SDL_Rect dstrect, *dstrectptr = NULL;
    SDL_Point origin, *originptr = NULL;
    double angle = 0;
    int flip_x = 0;
    int flip_y = 0;
    SDL_RendererFlip flip = SDL_FLIP_NONE;
    static char *keywords[] = {"srcrect", "dstrect", "angle", "origin", "flip_x", "flip_y", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OOdOpp", keywords,
                                     &srcrectobj, &dstrectobj, &angle, &originobj, &flip_x, &flip_y)) {
        return NULL; /* Exception already set. */
    }
    if (srcrectobj != Py_None) {
        if (!pgRect_Check(srcrectobj)) {
            return RAISE(PyExc_ValueError, "srcrectobj must be a rect, or None");
        }
        srcrectptr = pgRect_FromObject(srcrectobj, &srcrect);
        //srcrect = pgRect_AsRect(srcrectobj);
    }
    if (dstrectobj != Py_None) {
        dstrectptr = pgRect_FromObject(dstrectobj, &dstrect);
        if (dstrectptr == NULL) {
            if (PySequence_Check(dstrectobj) && PySequence_Length(dstrectobj) == 2) {
                if ((!pg_IntFromObjIndex(dstrectobj, 0, &dstrect.x)) ||
                    (!pg_IntFromObjIndex(dstrectobj, 1, &dstrect.y))) {
                    return RAISE(PyExc_ValueError, "dstrect must be a position, rect, or None");
                }
                dstrect.w = self->width;
                dstrect.h = self->height;
            }
        }
    }
    if (originobj != Py_None) {
        if (PySequence_Check(originobj) && PySequence_Length(originobj) == 2) {
            if ((!pg_IntFromObjIndex(originobj, 0, &origin.x)) ||
                (!pg_IntFromObjIndex(originobj, 1, &origin.y))) {
                return RAISE(PyExc_ValueError, "origin must be a point or None");
            }
            originptr = &origin;
        }
    }
    if (flip_x) flip |= SDL_FLIP_HORIZONTAL;
    if (flip_y) flip |= SDL_FLIP_VERTICAL;
    TEXTURE_ERROR_CHECK(SDL_RenderCopyEx(self->renderer->renderer, self->texture, srcrectptr, dstrectptr, angle, originptr, flip))
    Py_RETURN_NONE;
}

static PyObject *
texture_draw_triangle(pgTextureObject *self, PyObject *args, PyObject *kwargs) {
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1_xyobj, *p2_xyobj, *p3_xyobj, *p1_uvobj = Py_None, *p2_uvobj = Py_None, *p3_uvobj = Py_None, *p1_modobj = Py_None, *p2_modobj = Py_None, *p3_modobj = Py_None;
    Uint8 _r_mod, _g_mod, _b_mod, _a_mod;
    float r_mod, g_mod, b_mod, a_mod;
    SDL_Vertex vertices[3];
    float p1_xy[2], p2_xy[2], p3_xy[2], p1_uv[] = {0.0, 0.0}, p2_uv[] = {1.0, 1.0}, p3_uv[] = {0.0, 1.0};
    int p1_mod[] = {255, 255, 255, 255}, p2_mod[] = {255, 255, 255, 255}, p3_mod[] = {255, 255, 255, 255};
    static char *keywords[] = {"p1_xy", "p2_xy", "p3_xy", "p1_uv", "p2_uv", "p3_uv", "p1_mod", "p2_mod", "p3_mod", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|OOOOOO", keywords,
                                     &p1_xyobj, &p2_xyobj, &p3_xyobj, &p1_uvobj, &p2_uvobj, &p3_uvobj, &p1_modobj, &p2_modobj, &p3_modobj)) {
        return NULL; /* Exception already set. */
    }
    if (!pg_TwoFloatsFromObj(p1_xyobj, &p1_xy[0], &p1_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_xy argument");
    }
    if (!pg_TwoFloatsFromObj(p2_xyobj, &p2_xy[0], &p2_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_xy argument");
    }
    if (!pg_TwoFloatsFromObj(p3_xyobj, &p3_xy[0], &p3_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_xy argument");
    }
    if (p1_uvobj != Py_None && !pg_TwoFloatsFromObj(p1_uvobj, &p1_uv[0], &p1_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_uv argument");
    }
    if (p2_uvobj != Py_None && !pg_TwoFloatsFromObj(p2_uvobj, &p2_uv[0], &p2_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_uv argument");
    }
    if (p3_uvobj != Py_None && !pg_TwoFloatsFromObj(p3_uvobj, &p3_uv[0], &p3_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_uv argument");
    }
    if (p1_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p1_modobj, 0, &p1_mod[0]) || !pg_IntFromObjIndex(p1_modobj, 1, &p1_mod[1]) || 
            !pg_IntFromObjIndex(p1_modobj, 2, &p1_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p1_mod argument");
        }
        if (PySequence_Size(p1_modobj) == 4) pg_IntFromObjIndex(p1_modobj, 3, &p1_mod[3]);
    }
    if (p2_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p2_modobj, 0, &p2_mod[0]) || !pg_IntFromObjIndex(p2_modobj, 1, &p2_mod[1]) || 
            !pg_IntFromObjIndex(p2_modobj, 2, &p2_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p2_mod argument");
        }
        if (PySequence_Size(p2_modobj) == 4) pg_IntFromObjIndex(p2_modobj, 3, &p2_mod[3]);
    }
    if (p3_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p3_modobj, 0, &p3_mod[0]) || !pg_IntFromObjIndex(p3_modobj, 1, &p3_mod[1]) || 
            !pg_IntFromObjIndex(p3_modobj, 2, &p3_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p3_mod argument");
        }
        if (PySequence_Size(p3_modobj) == 4) pg_IntFromObjIndex(p3_modobj, 3, &p3_mod[3]);
    }
    TEXTURE_ERROR_CHECK(SDL_GetTextureColorMod(self->texture, &_r_mod, &_g_mod, &_b_mod));
    TEXTURE_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &_a_mod));
    r_mod = _r_mod / (float)255.0;
    g_mod = _g_mod / (float)255.0;
    b_mod = _b_mod / (float)255.0;
    a_mod = _a_mod / (float)255.0;

    vertices[0].position.x = p1_xy[0]; vertices[0].position.y = p1_xy[1]; vertices[0].tex_coord.x = p1_uv[0]; vertices[0].tex_coord.y = p1_uv[1];
    vertices[0].color.r = (int)r_mod * p1_mod[0]; vertices[0].color.g = (int)g_mod * p1_mod[1]; vertices[0].color.b = (int)b_mod * p1_mod[2]; vertices[0].color.a = (int)a_mod * p1_mod[3];
    vertices[1].position.x = p2_xy[0]; vertices[1].position.y = p2_xy[1]; vertices[1].tex_coord.x = p2_uv[0]; vertices[1].tex_coord.y = p2_uv[1];
    vertices[1].color.r = (int)r_mod * p2_mod[0]; vertices[1].color.g = (int)g_mod * p2_mod[1]; vertices[1].color.b = (int)b_mod * p2_mod[2]; vertices[1].color.a = (int)a_mod * p2_mod[3];
    vertices[2].position.x = p3_xy[0]; vertices[2].position.y = p3_xy[1]; vertices[2].tex_coord.x = p3_uv[0]; vertices[2].tex_coord.y = p3_uv[1];
    vertices[2].color.r = (int)r_mod * p3_mod[0]; vertices[2].color.g = (int)g_mod * p3_mod[1]; vertices[2].color.b = (int)b_mod * p3_mod[2]; vertices[2].color.a = (int)a_mod * p3_mod[3];
    TEXTURE_ERROR_CHECK(SDL_RenderGeometry(self->renderer->renderer, self->texture, vertices, 3, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "draw_triangle() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
texture_draw_quad(pgTextureObject *self, PyObject *args, PyObject *kwargs) {
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1_xyobj, *p2_xyobj, *p3_xyobj, *p4_xyobj, *p1_uvobj = Py_None, *p2_uvobj = Py_None, *p3_uvobj = Py_None, *p4_uvobj = Py_None, *p1_modobj = Py_None, *p2_modobj = Py_None, *p3_modobj = Py_None, *p4_modobj = Py_None;
    Uint8 _r_mod, _g_mod, _b_mod, _a_mod;
    float r_mod, g_mod, b_mod, a_mod;
    SDL_Vertex vertices[6];
    float p1_xy[2], p2_xy[2], p3_xy[2], p4_xy[2], p1_uv[] = {0.0, 0.0}, p2_uv[] = {1.0, 0.0}, p3_uv[] = {1.0, 1.0}, p4_uv[] = {0.0, 1.0};
    int p1_mod[] = {255, 255, 255, 255}, p2_mod[] = {255, 255, 255, 255}, p3_mod[] = {255, 255, 255, 255}, p4_mod[] = {255, 255, 255, 255};
    static char *keywords[] = {"p1_xy", "p2_xy", "p3_xy", "p4_xy", "p1_uv", "p2_uv", "p3_uv", "p4_uv", "p1_mod", "p2_mod", "p3_mod", "p4_mod", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO|OOOOOOOO", keywords,
                                     &p1_xyobj, &p2_xyobj, &p3_xyobj, &p4_xyobj, &p1_uvobj, &p2_uvobj, &p3_uvobj, &p4_uvobj, &p1_modobj, &p2_modobj, &p3_modobj, &p4_modobj)) {
        return NULL; /* Exception already set. */
    }
    if (!pg_TwoFloatsFromObj(p1_xyobj, &p1_xy[0], &p1_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_xy argument");
    }
    if (!pg_TwoFloatsFromObj(p2_xyobj, &p2_xy[0], &p2_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_xy argument");
    }
    if (!pg_TwoFloatsFromObj(p3_xyobj, &p3_xy[0], &p3_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_xy argument");
    }
    if (!pg_TwoFloatsFromObj(p4_xyobj, &p4_xy[0], &p4_xy[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_xy argument");
    }
    if (p1_uvobj != Py_None && !pg_TwoFloatsFromObj(p1_uvobj, &p1_uv[0], &p1_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_uv argument");
    }
    if (p2_uvobj != Py_None && !pg_TwoFloatsFromObj(p2_uvobj, &p2_uv[0], &p2_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_uv argument");
    }
    if (p3_uvobj != Py_None && !pg_TwoFloatsFromObj(p3_uvobj, &p3_uv[0], &p3_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_uv argument");
    }
    if (p4_uvobj != Py_None && !pg_TwoFloatsFromObj(p3_uvobj, &p4_uv[0], &p4_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_uv argument");
    }
    if (p1_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p1_modobj, 0, &p1_mod[0]) || !pg_IntFromObjIndex(p1_modobj, 1, &p1_mod[1]) || 
            !pg_IntFromObjIndex(p1_modobj, 2, &p1_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p1_mod argument");
        }
        if (PySequence_Size(p1_modobj) == 4) pg_IntFromObjIndex(p1_modobj, 3, &p1_mod[3]);
    }
    if (p2_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p2_modobj, 0, &p2_mod[0]) || !pg_IntFromObjIndex(p2_modobj, 1, &p2_mod[1]) || 
            !pg_IntFromObjIndex(p2_modobj, 2, &p2_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p2_mod argument");
        }
        if (PySequence_Size(p2_modobj) == 4) pg_IntFromObjIndex(p2_modobj, 3, &p2_mod[3]);
    }
    if (p3_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p3_modobj, 0, &p3_mod[0]) || !pg_IntFromObjIndex(p3_modobj, 1, &p3_mod[1]) || 
            !pg_IntFromObjIndex(p3_modobj, 2, &p3_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p3_mod argument");
        }
        if (PySequence_Size(p3_modobj) == 4) pg_IntFromObjIndex(p3_modobj, 3, &p3_mod[3]);
    }
    if (p4_modobj != Py_None) {
        if (!pg_IntFromObjIndex(p4_modobj, 0, &p4_mod[0]) || !pg_IntFromObjIndex(p4_modobj, 1, &p4_mod[1]) || 
            !pg_IntFromObjIndex(p4_modobj, 2, &p4_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p4_mod argument");
        }
        if (PySequence_Size(p4_modobj) == 4) pg_IntFromObjIndex(p4_modobj, 3, &p4_mod[3]);
    }
    TEXTURE_ERROR_CHECK(SDL_GetTextureColorMod(self->texture, &_r_mod, &_g_mod, &_b_mod));
    TEXTURE_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &_a_mod));

    r_mod = _r_mod / (float)255.0;
    g_mod = _g_mod / (float)255.0;
    b_mod = _b_mod / (float)255.0;
    a_mod = _a_mod / (float)255.0;

    vertices[0].position.x = p1_xy[0]; vertices[0].position.y = p1_xy[1]; vertices[0].tex_coord.x = p1_uv[0]; vertices[0].tex_coord.y = p1_uv[1];
    vertices[0].color.r = (int)r_mod * p1_mod[0]; vertices[0].color.g = (int)g_mod * p1_mod[1]; vertices[0].color.b = (int)b_mod * p1_mod[2]; vertices[0].color.a = (int)a_mod * p1_mod[3];
    vertices[1].position.x = p2_xy[0]; vertices[1].position.y = p2_xy[1]; vertices[1].tex_coord.x = p2_uv[0]; vertices[1].tex_coord.y = p2_uv[1];
    vertices[1].color.r = (int)r_mod * p2_mod[0]; vertices[1].color.g = (int)g_mod * p2_mod[1]; vertices[1].color.b = (int)b_mod * p2_mod[2]; vertices[1].color.a = (int)a_mod * p2_mod[3];
    vertices[2].position.x = p3_xy[0]; vertices[2].position.y = p3_xy[1]; vertices[2].tex_coord.x = p3_uv[0]; vertices[2].tex_coord.y = p3_uv[1];
    vertices[2].color.r = (int)r_mod * p3_mod[0]; vertices[2].color.g = (int)g_mod * p3_mod[1]; vertices[2].color.b = (int)b_mod * p3_mod[2]; vertices[2].color.a = (int)a_mod * p3_mod[3];
    vertices[3].position.x = p3_xy[0]; vertices[3].position.y = p3_xy[1]; vertices[3].tex_coord.x = p3_uv[0]; vertices[3].tex_coord.y = p3_uv[1];
    vertices[3].color.r = (int)r_mod * p3_mod[0]; vertices[3].color.g = (int)g_mod * p3_mod[1]; vertices[3].color.b = (int)b_mod * p3_mod[2]; vertices[3].color.a = (int)a_mod * p3_mod[3];
    vertices[4].position.x = p4_xy[0]; vertices[4].position.y = p4_xy[1]; vertices[4].tex_coord.x = p4_uv[0]; vertices[4].tex_coord.y = p4_uv[1];
    vertices[4].color.r = (int)r_mod * p4_mod[0]; vertices[4].color.g = (int)g_mod * p4_mod[1]; vertices[4].color.b = (int)b_mod * p4_mod[2]; vertices[4].color.a = (int)a_mod * p4_mod[3];
    vertices[5].position.x = p1_xy[0]; vertices[5].position.y = p1_xy[1]; vertices[5].tex_coord.x = p1_uv[0]; vertices[5].tex_coord.y = p1_uv[1];
    vertices[5].color.r = (int)r_mod * p1_mod[0]; vertices[5].color.g = (int)g_mod * p1_mod[1]; vertices[5].color.b = (int)b_mod * p1_mod[2]; vertices[5].color.a = (int)a_mod * p1_mod[3];
    TEXTURE_ERROR_CHECK(SDL_RenderGeometry(self->renderer->renderer, self->texture, vertices, 6, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "draw_triangle() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
texture_update(pgTextureObject *self, PyObject *args, PyObject *kwargs) {
    pgSurfaceObject *surfobj;
    PyObject *rectobj = Py_None;
    SDL_Surface *surf = NULL;
    SDL_Rect area, *areaptr = NULL;
    SDL_Surface *converted_surf = NULL;
    SDL_PixelFormat *pixel_format = NULL;
    SDL_BlendMode blend = SDL_BLENDMODE_NONE;
    Uint32 format;
    int res;
    static char *keywords[] = {"surface", "area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|O", keywords,
                                     &pgSurface_Type, &surfobj, &rectobj)) {
        return NULL; /* Exception already set. */
    }
    surf = pgSurface_AsSurface(surfobj);
    SURF_INIT_CHECK(surf)
    if (rectobj != Py_None) {
        if (!pgRect_Check(rectobj)) {
            return RAISE(PyExc_ValueError, "area must be a rectangle or None");
        }
        areaptr = pgRect_FromObject(rectobj, &area);
    }
    TEXTURE_ERROR_CHECK(SDL_QueryTexture(self->texture, &format, NULL, NULL, NULL))
    if (format != surf->format->format) {
        TEXTURE_ERROR_CHECK(SDL_GetSurfaceBlendMode(surf, &blend))
        pixel_format = SDL_AllocFormat(format);
        if (pixel_format == NULL) return RAISE(pgExc_SDLError, SDL_GetError());
        converted_surf = SDL_ConvertSurface(surf, pixel_format, 0);
        if (SDL_SetSurfaceBlendMode(converted_surf, blend) < 0) {
            SDL_FreeSurface(converted_surf);
            SDL_FreeFormat(pixel_format);
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        
        res = SDL_UpdateTexture(self->texture, areaptr, converted_surf->pixels, converted_surf->pitch);
        SDL_FreeSurface(converted_surf);
        SDL_FreeFormat(pixel_format);
    }
    else {
        
        res = SDL_UpdateTexture(self->texture, areaptr, surf->pixels, surf->pitch);
    }
    if (res < 0) return RAISE(pgExc_SDLError, SDL_GetError());
    Py_RETURN_NONE;
}

static PyObject *
from_surface(PyObject *self, PyObject *args, PyObject *kwargs) {
    pgRendererObject *renderer;
    pgSurfaceObject *surfobj;
    pgTextureObject *new_texture;
    SDL_Surface *surf = NULL;
    static char *keywords[] = {"renderer", "surface", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO!", keywords,
                                     &renderer, &pgSurface_Type, &surfobj)) {
        return NULL; /* Exception already set. */
    }
    new_texture = (pgTextureObject *)(&(pgTexture_Type))->tp_alloc(&pgTexture_Type, 0);
    surf = pgSurface_AsSurface(surfobj);
    SURF_INIT_CHECK(surf)
    new_texture->texture = SDL_CreateTextureFromSurface(renderer->renderer, surf);
    if (!new_texture->texture) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    new_texture->renderer = renderer;
    new_texture->width = surf->w;
    new_texture->height = surf->h;
    return (PyObject *)new_texture;
}

static int
texture_init(pgTextureObject *self, PyObject *args, PyObject *kwargs) {
    SDL_Texture *texture = NULL;
    pgRendererObject *renderer;
    PyObject *sizeobj;
    int width;
    int height;
    int depth = 0;
    int staticc = 0;
    int streaming = 0;
    int target = 0;
    int scale_quality = -1;
    int access = SDL_TEXTUREACCESS_STATIC;
    Uint32 format;

    char *keywords[] = {"renderer", "size", "depth", "static", "streaming", "target", "scale_quality", NULL};   
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|ipppi", keywords, &renderer, &sizeobj, &depth, &staticc, &streaming, &target, &scale_quality)) {
        return -1;
    }
    format = format_from_depth(depth);
    if (!pg_TwoIntsFromObj(sizeobj, &width, &height)) {
        RAISE(PyExc_TypeError, "invalid size argument");
        return -1;
    }
    if (width <= 0 || height <= 0) {
        RAISE(PyExc_ValueError, "size must contain two positive values");
        return -1;
    }
    if (staticc) {
        if (streaming || target) {
            RAISE(PyExc_ValueError, "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_STATIC;
    }
    if (streaming) {
        if (staticc || target) {
            RAISE(PyExc_ValueError, "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_STREAMING;
    }
    if (target) {
        if (staticc || streaming) {
            RAISE(PyExc_ValueError, "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_TARGET;
    }
    self->renderer = renderer;
    self->texture = SDL_CreateTexture(renderer->renderer, format, access, width, height);
    if (!self->texture) {
        RAISE(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    if (scale_quality != -1) {
#if SDL_VERSION_ATLEAST(2,0,12)
        if (SDL_SetTextureScaleMode(self->texture, scale_quality) < 0) {
            RAISE(pgExc_SDLError, SDL_GetError());
            return -1;
        }
#else
        switch (scale_quality) {
            case 0:
                SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "nearest"); break;
            case 1:
                SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "linear"); break;
            case 2:
                SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "best"); break;
        }
#endif
    }
    self->width = width;
    self->height = height;
    return 0;
}

static void
texture_dealloc(pgTextureObject *self, PyObject *_null) {
    if (self->texture) {
        SDL_DestroyTexture(self->texture);
    }
    Py_TYPE(self)->tp_free(self);
}

static PyMethodDef texture_methods[] = {
    {"get_rect", (PyCFunction)texture_get_rect, METH_FASTCALL | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_GETRECT},
    {"draw", (PyCFunction)texture_draw, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_DRAW},
    {"draw_triangle", (PyCFunction)texture_draw_triangle, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_DRAWTRIANGLE},
    {"draw_quad", (PyCFunction)texture_draw_quad, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_DRAWQUAD},
    {"update", (PyCFunction)texture_update, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_UPDATE},    
    {"from_surface", (PyCFunction)from_surface, METH_VARARGS | METH_KEYWORDS | METH_CLASS,
     DOC_SDL2_VIDEO_TEXTURE_FROMSURFACE},
    {NULL, NULL, 0, NULL}
};

static PyGetSetDef texture_getset[] = {
    {"alpha", (getter)texture_get_alpha, (setter)texture_set_alpha,
     DOC_SDL2_VIDEO_TEXTURE_ALPHA, NULL},
    {"blend_mode", (getter)texture_get_blend_mode, (setter)texture_set_blend_mode,
     DOC_SDL2_VIDEO_TEXTURE_BLENDMODE, NULL},
    {"color", (getter)texture_get_color, (setter)texture_set_color,
     DOC_SDL2_VIDEO_TEXTURE_COLOR, NULL},
    {NULL, 0, NULL, NULL, NULL}
};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._texture.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    .tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE,
    .tp_methods = texture_methods,
    .tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = texture_getset};

static PyMethodDef _texture_methods[] = {
    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_texture)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_TEXTURE_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_texture",
                                         "docs_needed",
                                         -1,
                                         _texture_methods,
                                         NULL,
                                         NULL,
                                         NULL,
                                         NULL};
    
    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    import_pygame_surface();
    if (PyErr_Occurred()) {
        return NULL;
    }

    import_pygame_rect();
    if (PyErr_Occurred()) {
        return NULL;
    }


    import_pygame_color();
    if (PyErr_Occurred()) {
        return NULL;
    }

    if (PyType_Ready(&pgTexture_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgTexture_Type);
    if (PyModule_AddObject(module, "Texture", (PyObject *)&pgTexture_Type)) {
        Py_DECREF(&pgTexture_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgTexture_Type;
    apiobj = encapsulate_api(c_api, "_texture");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
