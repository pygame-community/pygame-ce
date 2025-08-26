#define PYGAMEAPI_RENDERER_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/sdl2_video_doc.h"

static PyTypeObject pgRenderer_Type;

static PyTypeObject pgTexture_Type;

static PyTypeObject pgImage_Type;

#define pgRenderer_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgRenderer_Type))

#define pgTexture_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgTexture_Type))

#define pgImage_Check(x) (PyObject_IsInstance((x), (PyObject *)&pgImage_Type))

#define RENDERER_ERROR_CHECK(x)                       \
    if (x < 0) {                                      \
        return RAISE(pgExc_SDLError, SDL_GetError()); \
    }

#define RENDERER_PROPERTY_ERROR_CHECK(x)       \
    if (x < 0) {                               \
        RAISE(pgExc_SDLError, SDL_GetError()); \
        return -1;                             \
    }

static void
texture_renderer_draw(pgTextureObject *self, PyObject *area, PyObject *dest);

static void
image_renderer_draw(pgImageObject *self, PyObject *area, PyObject *dest);

/* Helper functions */
static inline Uint32
format_from_depth(int depth)
{
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
        RAISE(PyExc_ValueError,
              "no standard masks exist for given bitdepth with alpha");
        return -1;
    }
    return SDL_MasksToPixelFormatEnum(depth, Rmask, Gmask, Bmask, Amask);
}

static inline int
set_texture_blend_mode_helper(SDL_Texture *texture, SDL_BlendMode value)
{
    RENDERER_PROPERTY_ERROR_CHECK(SDL_SetTextureBlendMode(texture, value))
    return 0;
}

static inline int
set_texture_color_helper(SDL_Texture *texture, Uint8 r, Uint8 g, Uint8 b)
{
    RENDERER_PROPERTY_ERROR_CHECK(SDL_SetTextureColorMod(texture, r, g, b))
    return 0;
}

static inline int
set_texture_alpha_helper(SDL_Texture *texture, Uint8 alpha)
{
    RENDERER_PROPERTY_ERROR_CHECK(SDL_SetTextureAlphaMod(texture, alpha));
    return 0;
}

static inline SDL_FRect *
parse_dest_rect(pgTextureObject *texture, PyObject *dstrectobj, SDL_FRect *tmp)
{
    SDL_FRect *dstrectptr = NULL;
    if (!(dstrectptr = pgFRect_FromObject(dstrectobj, tmp))) {
        if (pg_TwoFloatsFromObj(dstrectobj, &dstrectptr->x, &dstrectptr->y)) {
            dstrectptr->w = (float)texture->width;
            dstrectptr->h = (float)texture->height;
        }
    }
    return dstrectptr;
}

/* Renderer implementation */
static PyObject *
from_window(PyTypeObject *cls, PyObject *args, PyObject *kwargs)
{
    PyObject *window;
    static char *keywords[] = {"window", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &window)) {
        return NULL;
    }
    if (pgWindow_Check(window)) {
        pgRendererObject *self =
            (pgRendererObject *)(cls->tp_new(cls, NULL, NULL));
        self->window = (pgWindowObject *)window;
        if (self->window->_is_borrowed) {
            self->_is_borrowed = SDL_TRUE;
        }
        else {
            return RAISE(pgExc_SDLError,
                         "Window is not created from display module");
        }
        self->renderer = SDL_GetRenderer(self->window->_win);
        if (!self->renderer) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        self->target = NULL;
        return (PyObject *)self;
    }
    else {
        return RAISE(PyExc_TypeError, "Invalid window argument");
    }
}

static PyObject *
renderer_draw_point(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *point;
    float x, y;
    static char *keywords[] = {"point", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &point)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(point, &x, &y)) {
        return RAISE(PyExc_TypeError, "invalid point");
    }
    RENDERER_ERROR_CHECK(SDL_RenderDrawPointF(self->renderer, x, y))
    Py_RETURN_NONE;
}

static PyObject *
renderer_draw_line(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *start, *end;
    float startx, starty, endx, endy;
    static char *keywords[] = {"p1", "p2", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &start,
                                     &end)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(start, &startx, &starty)) {
        return RAISE(PyExc_TypeError, "invalid p1 argument");
    }
    if (!pg_TwoFloatsFromObj(end, &endx, &endy)) {
        return RAISE(PyExc_TypeError, "invalid p2 argument");
    }
    RENDERER_ERROR_CHECK(
        SDL_RenderDrawLineF(self->renderer, startx, starty, endx, endy))
    Py_RETURN_NONE;
}

static PyObject *
renderer_draw_rect(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *rectobj;
    SDL_FRect *rect = NULL, temp;
    static char *keywords[] = {"rect", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &rectobj)) {
        return NULL;
    }
    if (!(rect = pgFRect_FromObject(rectobj, &temp))) {
        return RAISE(PyExc_TypeError, "rect argument is invalid");
    }
    RENDERER_ERROR_CHECK(SDL_RenderDrawRectF(self->renderer, rect))
    Py_RETURN_NONE;
}

static PyObject *
renderer_fill_rect(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *rectobj;
    SDL_FRect *rect = NULL, temp;
    static char *keywords[] = {"rect", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &rectobj)) {
        return NULL;
    }
    if (!(rect = pgFRect_FromObject(rectobj, &temp))) {
        return RAISE(PyExc_TypeError, "rect argument is invalid");
    }
    RENDERER_ERROR_CHECK(SDL_RenderFillRectF(self->renderer, rect))
    Py_RETURN_NONE;
}

static PyObject *
renderer_draw_triangle(pgRendererObject *self, PyObject *args,
                       PyObject *kwargs)
{
    PyObject *p1, *p2, *p3;
    float p1x, p1y, p2x, p2y, p3x, p3y;
    SDL_FPoint points[4];
    static char *keywords[] = {"p1", "p2", "p3", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO", keywords, &p1, &p2,
                                     &p3)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(p1, &p1x, &p1y)) {
        return RAISE(PyExc_TypeError, "invalid p1 argument");
    }
    if (!pg_TwoFloatsFromObj(p2, &p2x, &p2y)) {
        return RAISE(PyExc_TypeError, "invalid p2 argument");
    }
    if (!pg_TwoFloatsFromObj(p3, &p3x, &p3y)) {
        return RAISE(PyExc_TypeError, "invalid p3 argument");
    }
    points[0].x = p1x;
    points[0].y = p1y;
    points[1].x = p2x;
    points[1].y = p2y;
    points[2].x = p3x;
    points[2].y = p3y;
    points[3].x = p1x;
    points[3].y = p1y;
    RENDERER_ERROR_CHECK(SDL_RenderDrawLinesF(self->renderer, points, 4))
    Py_RETURN_NONE;
}

static PyObject *
renderer_fill_triangle(pgRendererObject *self, PyObject *args,
                       PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    Uint8 rgba[4];
    PyObject *p1, *p2, *p3;
    float p1x, p1y, p2x, p2y, p3x, p3y;
    SDL_Vertex vertices[3];
    static char *keywords[] = {"p1", "p2", "p3", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO", keywords, &p1, &p2,
                                     &p3)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(p1, &p1x, &p1y)) {
        return RAISE(PyExc_TypeError, "invalid p1 argument");
    }
    if (!pg_TwoFloatsFromObj(p2, &p2x, &p2y)) {
        return RAISE(PyExc_TypeError, "invalid p2 argument");
    }
    if (!pg_TwoFloatsFromObj(p3, &p3x, &p3y)) {
        return RAISE(PyExc_TypeError, "invalid p3 argument");
    }
    RENDERER_ERROR_CHECK(SDL_GetRenderDrawColor(self->renderer, &rgba[0],
                                                &rgba[1], &rgba[2], &rgba[3]))
    vertices[0].position.x = p1x;
    vertices[0].position.y = p1y;
    vertices[0].color.r = rgba[0];
    vertices[0].color.g = rgba[1];
    vertices[0].color.b = rgba[2];
    vertices[0].color.a = rgba[3];
    vertices[1].position.x = p2x;
    vertices[1].position.y = p2y;
    vertices[1].color.r = rgba[0];
    vertices[1].color.g = rgba[1];
    vertices[1].color.b = rgba[2];
    vertices[1].color.a = rgba[3];
    vertices[2].position.x = p3x;
    vertices[2].position.y = p3y;
    vertices[2].color.r = rgba[0];
    vertices[2].color.g = rgba[1];
    vertices[2].color.b = rgba[2];
    vertices[2].color.a = rgba[3];
    RENDERER_ERROR_CHECK(
        SDL_RenderGeometry(self->renderer, NULL, vertices, 3, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "fill_triangle() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
renderer_draw_quad(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *p1, *p2, *p3, *p4;
    float p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y;
    SDL_FPoint points[5];
    static char *keywords[] = {"p1", "p2", "p3", "p4", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO", keywords, &p1, &p2,
                                     &p3, &p4)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(p1, &p1x, &p1y)) {
        return RAISE(PyExc_TypeError, "invalid p1 argument");
    }
    if (!pg_TwoFloatsFromObj(p2, &p2x, &p2y)) {
        return RAISE(PyExc_TypeError, "invalid p2 argument");
    }
    if (!pg_TwoFloatsFromObj(p3, &p3x, &p3y)) {
        return RAISE(PyExc_TypeError, "invalid p3 argument");
    }
    if (!pg_TwoFloatsFromObj(p4, &p4x, &p4y)) {
        return RAISE(PyExc_TypeError, "invalid p4 argument");
    }
    points[0].x = p1x;
    points[0].y = p1y;
    points[1].x = p2x;
    points[1].y = p2y;
    points[2].x = p3x;
    points[2].y = p3y;
    points[3].x = p4x;
    points[3].y = p4y;
    points[4].x = p1x;
    points[4].y = p1y;
    RENDERER_ERROR_CHECK(SDL_RenderDrawLinesF(self->renderer, points, 5))
    Py_RETURN_NONE;
}

static PyObject *
renderer_fill_quad(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    Uint8 rgba[4];
    PyObject *p1, *p2, *p3, *p4;
    float p1x, p1y, p2x, p2y, p3x, p3y, p4x, p4y;
    SDL_Vertex vertices[6];
    static char *keywords[] = {"p1", "p2", "p3", "p4", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO", keywords, &p1, &p2,
                                     &p3, &p4)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(p1, &p1x, &p1y)) {
        return RAISE(PyExc_TypeError, "invalid p1 argument");
    }
    if (!pg_TwoFloatsFromObj(p2, &p2x, &p2y)) {
        return RAISE(PyExc_TypeError, "invalid p2 argument");
    }
    if (!pg_TwoFloatsFromObj(p3, &p3x, &p3y)) {
        return RAISE(PyExc_TypeError, "invalid p3 argument");
    }
    if (!pg_TwoFloatsFromObj(p4, &p4x, &p4y)) {
        return RAISE(PyExc_TypeError, "invalid p4 argument");
    }
    RENDERER_ERROR_CHECK(SDL_GetRenderDrawColor(self->renderer, &rgba[0],
                                                &rgba[1], &rgba[2], &rgba[3]))
    vertices[0].position.x = p1x;
    vertices[0].position.y = p1y;
    vertices[0].color.r = rgba[0];
    vertices[0].color.g = rgba[1];
    vertices[0].color.b = rgba[2];
    vertices[0].color.a = rgba[3];
    vertices[1].position.x = p2x;
    vertices[1].position.y = p2y;
    vertices[1].color.r = rgba[0];
    vertices[1].color.g = rgba[1];
    vertices[1].color.b = rgba[2];
    vertices[1].color.a = rgba[3];
    vertices[2].position.x = p3x;
    vertices[2].position.y = p3y;
    vertices[2].color.r = rgba[0];
    vertices[2].color.g = rgba[1];
    vertices[2].color.b = rgba[2];
    vertices[2].color.a = rgba[3];
    vertices[3].position.x = p3x;
    vertices[3].position.y = p3y;
    vertices[3].color.r = rgba[0];
    vertices[3].color.g = rgba[1];
    vertices[3].color.b = rgba[2];
    vertices[3].color.a = rgba[3];
    vertices[4].position.x = p4x;
    vertices[4].position.y = p4y;
    vertices[4].color.r = rgba[0];
    vertices[4].color.g = rgba[1];
    vertices[4].color.b = rgba[2];
    vertices[4].color.a = rgba[3];
    vertices[5].position.x = p1x;
    vertices[5].position.y = p1y;
    vertices[5].color.r = rgba[0];
    vertices[5].color.g = rgba[1];
    vertices[5].color.b = rgba[2];
    vertices[5].color.a = rgba[3];
    RENDERER_ERROR_CHECK(
        SDL_RenderGeometry(self->renderer, NULL, vertices, 6, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "fill_quad() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
renderer_present(pgRendererObject *self, PyObject *_null)
{
    SDL_RenderPresent(self->renderer);
    Py_RETURN_NONE;
}

static PyObject *
renderer_clear(pgRendererObject *self, PyObject *_null)
{
    RENDERER_ERROR_CHECK(SDL_RenderClear(self->renderer))
    Py_RETURN_NONE;
}

static PyObject *
renderer_get_viewport(pgRendererObject *self, PyObject *_null)
{
    SDL_Rect rect;
    SDL_RenderGetViewport(self->renderer, &rect);
    return pgRect_New(&rect);
}

static PyObject *
renderer_set_viewport(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *rectobj = Py_None;
    SDL_Rect rect;
    static char *keywords[] = {"area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|O", keywords, &rectobj)) {
        return NULL;
    }
    if (rectobj == Py_None) {
        RENDERER_ERROR_CHECK(SDL_RenderSetViewport(self->renderer, NULL))
    }
    else {
        rect = pgRect_AsRect(rectobj);
        RENDERER_ERROR_CHECK(SDL_RenderSetViewport(self->renderer, &rect))
    }
    Py_RETURN_NONE;
}

static PyObject *
compose_custom_blend_mode(PyObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *color_mode, *alpha_mode;
    float mode[6];
    int blend_mode;
    static char *keywords[] = {"color_mode", "alpha_mode", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &color_mode,
                                     &alpha_mode)) {
        return NULL;
    }
    if (!PySequence_Check(color_mode)) {
        return RAISE(PyExc_TypeError, "color_mode has to be sequence");
    }
    if (!PySequence_Check(alpha_mode)) {
        return RAISE(PyExc_TypeError, "alpha_mode has to be sequence");
    }
    if (PySequence_Size(color_mode) != 3) {
        return RAISE(PyExc_TypeError, "color_mode has to have 3 elements");
    }
    if (PySequence_Size(alpha_mode) != 3) {
        return RAISE(PyExc_TypeError, "alpha_mode has to have 3 elements");
    }
    if (!pg_FloatFromObjIndex(color_mode, 0, &mode[0])) {
        return RAISE(PyExc_TypeError,
                     "color_mode first element must be float");
    }
    if (!pg_FloatFromObjIndex(color_mode, 1, &mode[1])) {
        return RAISE(PyExc_TypeError,
                     "color_mode second element must be float");
    }
    if (!pg_FloatFromObjIndex(color_mode, 2, &mode[2])) {
        return RAISE(PyExc_TypeError,
                     "color_mode third element must be float");
    }
    if (!pg_FloatFromObjIndex(alpha_mode, 0, &mode[3])) {
        return RAISE(PyExc_TypeError,
                     "alpha_mode first element must be float");
    }
    if (!pg_FloatFromObjIndex(alpha_mode, 1, &mode[4])) {
        return RAISE(PyExc_TypeError,
                     "alpha_mode second element must be float");
    }
    if (!pg_FloatFromObjIndex(alpha_mode, 2, &mode[5])) {
        return RAISE(PyExc_TypeError,
                     "alpha_mode third element must be float");
    }
    blend_mode = SDL_ComposeCustomBlendMode(mode[0], mode[1], mode[2], mode[3],
                                            mode[4], mode[5]);
    return PyLong_FromLong((long)blend_mode);
}

static PyObject *
renderer_to_surface(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *surfobj = Py_None, *rectobj = Py_None;
    SDL_Surface *surf;
    pgSurfaceObject *surface;
    SDL_Rect viewport, *areaparam, rarea, *rareaptr = &rarea;
    Uint32 format;
    static char *keywords[] = {"surface", "area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OO", keywords, &surfobj,
                                     &rectobj)) {
        return NULL;
    }
    if (!Py_IsNone(rectobj)) {
        if (!(rareaptr = pgRect_FromObject(rectobj, &rarea))) {
            return RAISE(PyExc_TypeError, "area must be None or a rect");
        }
        SDL_RenderGetViewport(self->renderer, &viewport);
        SDL_IntersectRect(rareaptr, &viewport, rareaptr);
        areaparam = rareaptr;
    }
    else {
        SDL_RenderGetViewport(self->renderer, rareaptr);
        areaparam = NULL;
    }
    if (!Py_IsNone(surfobj)) {
        if (!(pgSurface_Check(surfobj))) {
            return RAISE(PyExc_TypeError, "surface must be None or a Surface");
        }
        surface = (pgSurfaceObject *)surfobj;
        Py_INCREF(surface);
        surf = pgSurface_AsSurface(surfobj);
        if (surf->w < rareaptr->w || surf->h < rareaptr->h) {
            return RAISE(PyExc_ValueError, "the surface is too small");
        }
        format = surf->format->format;
    }
    else {
        format = SDL_GetWindowPixelFormat(self->window->_win);
        if (format == SDL_PIXELFORMAT_UNKNOWN) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        surf = SDL_CreateRGBSurfaceWithFormat(
            0, rareaptr->w, rareaptr->h, SDL_BITSPERPIXEL(format), format);
        if (surf == NULL) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        surface = pgSurface_New(surf);
    }
    RENDERER_ERROR_CHECK(SDL_RenderReadPixels(
        self->renderer, areaparam, format, surf->pixels, surf->pitch));
    return (PyObject *)surface;
}

static PyObject *
renderer_blit(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *sourceobj, *destobj = Py_None, *areaobj = Py_None;
    int special_flags = 0;
    static char *keywords[] = {"source", "dest", "area", "special_flags",
                               NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OOi", keywords,
                                     &sourceobj, &destobj, &areaobj,
                                     &special_flags)) {
        return NULL;
    }

    if (pgTexture_Check(sourceobj)) {
        texture_renderer_draw((pgTextureObject *)sourceobj, areaobj, destobj);
    }
    else if (pgImage_Check(sourceobj)) {
        image_renderer_draw((pgImageObject *)sourceobj, areaobj, destobj);
    }
    else if (PyObject_HasAttrString(sourceobj, "draw")) {
        PyObject *draw_method = PyObject_GetAttrString(sourceobj, "draw");
        if (draw_method && PyCallable_Check(draw_method)) {
            PyObject_CallMethodObjArgs(sourceobj, PyUnicode_FromString("draw"),
                                       areaobj, destobj, NULL);
            Py_DECREF(draw_method);
        }
        else {
            return RAISE(PyExc_AttributeError, "source.draw is not callable");
        }
    }
    else {
        return RAISE(PyExc_AttributeError,
                     "source object doesn't have draw method");
    }

    if (Py_IsNone(destobj)) {
        return renderer_get_viewport(self, NULL);
    }
    Py_INCREF(destobj);
    return destobj;
}

static PyObject *
renderer_get_draw_color(pgRendererObject *self, void *closure)
{
    Uint8 rgba[4];
    RENDERER_ERROR_CHECK(SDL_GetRenderDrawColor(self->renderer, &rgba[0],
                                                &rgba[1], &rgba[2], &rgba[3]))
    return pgColor_NewLength(rgba, 4);
}

static int
renderer_set_draw_color(pgRendererObject *self, PyObject *arg, void *closure)
{
    Uint8 color[4];
    if (!pg_RGBAFromObjEx(arg, color, PG_COLOR_HANDLE_ALL)) {
        return -1;
    }
    RENDERER_PROPERTY_ERROR_CHECK(SDL_SetRenderDrawColor(
        self->renderer, color[0], color[1], color[2], color[3]))
    return 0;
}

static PyObject *
renderer_get_draw_blend_mode(pgRendererObject *self, void *closure)
{
    SDL_BlendMode blend_mode;
    RENDERER_ERROR_CHECK(
        SDL_GetRenderDrawBlendMode(self->renderer, &blend_mode))
    return PyLong_FromLong((long)blend_mode);
}

static int
renderer_set_draw_blend_mode(pgRendererObject *self, PyObject *arg,
                             void *closure)
{
    if (!PyLong_Check(arg)) {
        RAISE(PyExc_TypeError, "Draw blend mode must be int");
        return -1;
    }
    RENDERER_PROPERTY_ERROR_CHECK(
        SDL_SetRenderDrawBlendMode(self->renderer, (int)PyLong_AsLong(arg)))
    return 0;
}

static PyObject *
renderer_get_logical_size(pgRendererObject *self, void *closure)
{
    int w, h;
    SDL_RenderGetLogicalSize(self->renderer, &w, &h);
    return pg_tuple_couple_from_values_int(w, h);
}

static int
renderer_set_logical_size(pgRendererObject *self, PyObject *arg, void *closure)
{
    int w, h;
    if (!pg_TwoIntsFromObj(arg, &w, &h)) {
        RAISE(PyExc_TypeError, "invalid logical size");
        return -1;
    }
    RENDERER_PROPERTY_ERROR_CHECK(
        SDL_RenderSetLogicalSize(self->renderer, w, h))
    return 0;
}

static PyObject *
renderer_get_scale(pgRendererObject *self, void *closure)
{
    float x, y;
    SDL_RenderGetScale(self->renderer, &x, &y);
    return pg_tuple_couple_from_values_double(x, y);
}

static int
renderer_set_scale(pgRendererObject *self, PyObject *arg, void *closure)
{
    float x, y;
    if (!pg_TwoFloatsFromObj(arg, &x, &y)) {
        RAISE(PyExc_TypeError, "invalid scale");
        return -1;
    }
    RENDERER_PROPERTY_ERROR_CHECK(SDL_RenderSetScale(self->renderer, x, y))
    return 0;
}

static PyObject *
renderer_get_target(pgRendererObject *self, void *closure)
{
    if (self->target == NULL) {
        Py_RETURN_NONE;
    }
    Py_INCREF(self->target);
    return (PyObject *)self->target;
}

static int
renderer_set_target(pgRendererObject *self, PyObject *arg, void *closure)
{
    if (Py_IsNone(arg)) {
        self->target = NULL;
        RENDERER_PROPERTY_ERROR_CHECK(
            SDL_SetRenderTarget(self->renderer, NULL))
        return 0;
    }
    else if (pgTexture_Check(arg)) {
        self->target = (pgTextureObject *)arg;
        RENDERER_PROPERTY_ERROR_CHECK(
            SDL_SetRenderTarget(self->renderer, self->target->texture))
        return 0;
    }
    else {
        RAISE(PyExc_TypeError, "target must be Texture object or None");
        return -1;
    }
}

static int
renderer_init(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_Renderer *renderer = NULL;
    pgWindowObject *window;
    int index = -1;
    int accelerated = -1;
    int vsync = 0;
    int target_texture = 0;
    Uint32 flags = 0;

    char *keywords[] = {"window", "index",          "accelerated",
                        "vsync",  "target_texture", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|iipp", keywords, &window,
                                     &index, &accelerated, &vsync,
                                     &target_texture)) {
        return -1;
    }
    if (accelerated >= 0) {
        flags |=
            accelerated ? SDL_RENDERER_ACCELERATED : SDL_RENDERER_SOFTWARE;
    }
    if (vsync) {
        flags |= SDL_RENDERER_PRESENTVSYNC;
    }
    if (target_texture) {
        flags |= SDL_RENDERER_TARGETTEXTURE;
    }
    renderer = SDL_CreateRenderer(window->_win, index, flags);
    if (!renderer) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    self->renderer = renderer;
    self->window = window;
    self->target = NULL;
    self->_is_borrowed = SDL_FALSE;
    return 0;
}

static void
renderer_dealloc(pgRendererObject *self, PyObject *_null)
{
    if (!self->_is_borrowed && self->renderer) {
        SDL_DestroyRenderer(self->renderer);
    }
    Py_TYPE(self)->tp_free(self);
}

/* Texture implementation */
static void
texture_renderer_draw(pgTextureObject *self, PyObject *area, PyObject *dest)
{
    SDL_Rect srcrect, *srcrectptr = NULL;
    SDL_FRect dstrect, *dstrectptr = NULL;
    if (!Py_IsNone(area)) {
        if (!(srcrectptr = pgRect_FromObject(area, &srcrect))) {
            RAISE(PyExc_ValueError, "srcrect must be a Rect or None");
        }
    }
    if (!Py_IsNone(dest)) {
        if (!(dstrectptr = parse_dest_rect(self, dest, &dstrect))) {
            RAISE(PyExc_ValueError, "dstrect must be a point, Rect, or None");
        }
    }
    if (SDL_RenderCopyExF(self->renderer->renderer, self->texture, srcrectptr,
                          dstrectptr, 0, NULL, SDL_FLIP_NONE) < 0) {
        RAISE(pgExc_SDLError, SDL_GetError());
    }
}

static PyObject *
from_surface(PyObject *self, PyObject *args, PyObject *kwargs)
{
    pgRendererObject *renderer;
    pgSurfaceObject *surfobj;
    pgTextureObject *new_texture;
    SDL_Surface *surf = NULL;
    static char *keywords[] = {"renderer", "surface", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO!", keywords, &renderer,
                                     &pgSurface_Type, &surfobj)) {
        return NULL; /* Exception already set. */
    }
    new_texture =
        (pgTextureObject *)(&(pgTexture_Type))->tp_alloc(&pgTexture_Type, 0);
    surf = pgSurface_AsSurface(surfobj);
    SURF_INIT_CHECK(surf)
    new_texture->texture =
        SDL_CreateTextureFromSurface(renderer->renderer, surf);
    if (!new_texture->texture) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    new_texture->renderer = renderer;
    new_texture->width = surf->w;
    new_texture->height = surf->h;
    return (PyObject *)new_texture;
}

static PyObject *
texture_get_rect(pgTextureObject *self, PyObject *const *args,
                 Py_ssize_t nargs, PyObject *kwargs)
{
    PyObject *rect = pgRect_New4(0, 0, self->width, self->height);
    return pgObject_getRectHelper(rect, args, nargs, kwargs, "rect");
}

static PyObject *
texture_draw(pgTextureObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *srcrectobj = Py_None, *dstrectobj = Py_None,
             *originobj = Py_None;
    SDL_Rect srcrect, *srcrectptr = NULL;
    SDL_FRect dstrect, *dstrectptr = NULL;
    SDL_FPoint origin, *originptr = NULL;
    int has_origin = 0;
    double angle = 0;
    int flip_x = 0;
    int flip_y = 0;
    SDL_RendererFlip flip = SDL_FLIP_NONE;
    static char *keywords[] = {"srcrect", "dstrect", "angle", "origin",
                               "flip_x",  "flip_y",  NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OOdOpp", keywords,
                                     &srcrectobj, &dstrectobj, &angle,
                                     &originobj, &flip_x, &flip_y)) {
        return NULL; /* Exception already set. */
    }
    if (!Py_IsNone(srcrectobj)) {
        if (!(srcrectptr = pgRect_FromObject(srcrectobj, &srcrect))) {
            return RAISE(PyExc_ValueError, "srcrect must be a Rect or None");
        }
    }
    if (!Py_IsNone(dstrectobj)) {
        if (!(dstrectptr = parse_dest_rect(self, dstrectobj, &dstrect))) {
            return RAISE(PyExc_ValueError,
                         "dstrect must be a point, Rect, or None");
        }
    }
    if (!Py_IsNone(originobj)) {
        if (!pg_TwoFloatsFromObj(originobj, &origin.x, &origin.y)) {
            return RAISE(PyExc_ValueError, "origin must be a point or None");
        }
        originptr = &origin;
    }
    if (flip_x) {
        flip |= SDL_FLIP_HORIZONTAL;
    }
    if (flip_y) {
        flip |= SDL_FLIP_VERTICAL;
    }
    RENDERER_ERROR_CHECK(SDL_RenderCopyExF(self->renderer->renderer,
                                           self->texture, srcrectptr,
                                           dstrectptr, angle, originptr, flip))
    Py_RETURN_NONE;
}

static PyObject *
texture_draw_triangle(pgTextureObject *self, PyObject *args, PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1_xyobj, *p2_xyobj, *p3_xyobj,
        *p1_uvobj = Py_None, *p2_uvobj = Py_None, *p3_uvobj = Py_None,
        *p1_modobj = Py_None, *p2_modobj = Py_None, *p3_modobj = Py_None;
    Uint8 _r_mod, _g_mod, _b_mod, _a_mod;
    float r_mod, g_mod, b_mod, a_mod;
    SDL_Vertex vertices[3];
    float p1_xy[2], p2_xy[2], p3_xy[2],
        p1_uv[] = {0.0, 0.0}, p2_uv[] = {1.0, 1.0}, p3_uv[] = {0.0, 1.0};
    int p1_mod[] = {255, 255, 255, 255}, p2_mod[] = {255, 255, 255, 255},
        p3_mod[] = {255, 255, 255, 255};
    static char *keywords[] = {"p1_xy", "p2_xy",  "p3_xy",  "p1_uv",  "p2_uv",
                               "p3_uv", "p1_mod", "p2_mod", "p3_mod", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|OOOOOO", keywords,
                                     &p1_xyobj, &p2_xyobj, &p3_xyobj,
                                     &p1_uvobj, &p2_uvobj, &p3_uvobj,
                                     &p1_modobj, &p2_modobj, &p3_modobj)) {
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
    if (!Py_IsNone(p1_uvobj) &&
        !pg_TwoFloatsFromObj(p1_uvobj, &p1_uv[0], &p1_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_uv argument");
    }
    if (!Py_IsNone(p2_uvobj) &&
        !pg_TwoFloatsFromObj(p2_uvobj, &p2_uv[0], &p2_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_uv argument");
    }
    if (!Py_IsNone(p3_uvobj) &&
        !pg_TwoFloatsFromObj(p3_uvobj, &p3_uv[0], &p3_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_uv argument");
    }
    if (!Py_IsNone(p1_modobj)) {
        if (!pg_IntFromObjIndex(p1_modobj, 0, &p1_mod[0]) ||
            !pg_IntFromObjIndex(p1_modobj, 1, &p1_mod[1]) ||
            !pg_IntFromObjIndex(p1_modobj, 2, &p1_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p1_mod argument");
        }
        if (PySequence_Size(p1_modobj) == 4) {
            pg_IntFromObjIndex(p1_modobj, 3, &p1_mod[3]);
        }
    }
    if (!Py_IsNone(p2_modobj)) {
        if (!pg_IntFromObjIndex(p2_modobj, 0, &p2_mod[0]) ||
            !pg_IntFromObjIndex(p2_modobj, 1, &p2_mod[1]) ||
            !pg_IntFromObjIndex(p2_modobj, 2, &p2_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p2_mod argument");
        }
        if (PySequence_Size(p2_modobj) == 4) {
            pg_IntFromObjIndex(p2_modobj, 3, &p2_mod[3]);
        }
    }
    if (!Py_IsNone(p3_modobj)) {
        if (!pg_IntFromObjIndex(p3_modobj, 0, &p3_mod[0]) ||
            !pg_IntFromObjIndex(p3_modobj, 1, &p3_mod[1]) ||
            !pg_IntFromObjIndex(p3_modobj, 2, &p3_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p3_mod argument");
        }
        if (PySequence_Size(p3_modobj) == 4) {
            pg_IntFromObjIndex(p3_modobj, 3, &p3_mod[3]);
        }
    }
    RENDERER_ERROR_CHECK(
        SDL_GetTextureColorMod(self->texture, &_r_mod, &_g_mod, &_b_mod));
    RENDERER_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &_a_mod));
    r_mod = _r_mod / (float)255.0;
    g_mod = _g_mod / (float)255.0;
    b_mod = _b_mod / (float)255.0;
    a_mod = _a_mod / (float)255.0;

    vertices[0].position.x = p1_xy[0];
    vertices[0].position.y = p1_xy[1];
    vertices[0].tex_coord.x = p1_uv[0];
    vertices[0].tex_coord.y = p1_uv[1];
    vertices[0].color.r = (int)r_mod * p1_mod[0];
    vertices[0].color.g = (int)g_mod * p1_mod[1];
    vertices[0].color.b = (int)b_mod * p1_mod[2];
    vertices[0].color.a = (int)a_mod * p1_mod[3];
    vertices[1].position.x = p2_xy[0];
    vertices[1].position.y = p2_xy[1];
    vertices[1].tex_coord.x = p2_uv[0];
    vertices[1].tex_coord.y = p2_uv[1];
    vertices[1].color.r = (int)r_mod * p2_mod[0];
    vertices[1].color.g = (int)g_mod * p2_mod[1];
    vertices[1].color.b = (int)b_mod * p2_mod[2];
    vertices[1].color.a = (int)a_mod * p2_mod[3];
    vertices[2].position.x = p3_xy[0];
    vertices[2].position.y = p3_xy[1];
    vertices[2].tex_coord.x = p3_uv[0];
    vertices[2].tex_coord.y = p3_uv[1];
    vertices[2].color.r = (int)r_mod * p3_mod[0];
    vertices[2].color.g = (int)g_mod * p3_mod[1];
    vertices[2].color.b = (int)b_mod * p3_mod[2];
    vertices[2].color.a = (int)a_mod * p3_mod[3];
    RENDERER_ERROR_CHECK(SDL_RenderGeometry(
        self->renderer->renderer, self->texture, vertices, 3, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "draw_triangle() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
texture_draw_quad(pgTextureObject *self, PyObject *args, PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1_xyobj, *p2_xyobj, *p3_xyobj, *p4_xyobj,
        *p1_uvobj = Py_None, *p2_uvobj = Py_None, *p3_uvobj = Py_None,
        *p4_uvobj = Py_None, *p1_modobj = Py_None, *p2_modobj = Py_None,
        *p3_modobj = Py_None, *p4_modobj = Py_None;
    Uint8 _r_mod, _g_mod, _b_mod, _a_mod;
    float r_mod, g_mod, b_mod, a_mod;
    SDL_Vertex vertices[6];
    float p1_xy[2], p2_xy[2], p3_xy[2], p4_xy[2],
        p1_uv[] = {0.0, 0.0}, p2_uv[] = {1.0, 0.0}, p3_uv[] = {1.0, 1.0},
        p4_uv[] = {0.0, 1.0};
    int p1_mod[] = {255, 255, 255, 255}, p2_mod[] = {255, 255, 255, 255},
        p3_mod[] = {255, 255, 255, 255}, p4_mod[] = {255, 255, 255, 255};
    static char *keywords[] = {"p1_xy",  "p2_xy",  "p3_xy", "p4_xy",  "p1_uv",
                               "p2_uv",  "p3_uv",  "p4_uv", "p1_mod", "p2_mod",
                               "p3_mod", "p4_mod", NULL};
    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs, "OOOO|OOOOOOOO", keywords, &p1_xyobj, &p2_xyobj,
            &p3_xyobj, &p4_xyobj, &p1_uvobj, &p2_uvobj, &p3_uvobj, &p4_uvobj,
            &p1_modobj, &p2_modobj, &p3_modobj, &p4_modobj)) {
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
    if (!Py_IsNone(p1_uvobj) &&
        !pg_TwoFloatsFromObj(p1_uvobj, &p1_uv[0], &p1_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p1_uv argument");
    }
    if (!Py_IsNone(p2_uvobj) &&
        !pg_TwoFloatsFromObj(p2_uvobj, &p2_uv[0], &p2_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p2_uv argument");
    }
    if (!Py_IsNone(p3_uvobj) &&
        !pg_TwoFloatsFromObj(p3_uvobj, &p3_uv[0], &p3_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p3_uv argument");
    }
    if (!Py_IsNone(p4_uvobj) &&
        !pg_TwoFloatsFromObj(p3_uvobj, &p4_uv[0], &p4_uv[1])) {
        return RAISE(PyExc_TypeError, "invalid p4_uv argument");
    }
    if (!Py_IsNone(p1_modobj)) {
        if (!pg_IntFromObjIndex(p1_modobj, 0, &p1_mod[0]) ||
            !pg_IntFromObjIndex(p1_modobj, 1, &p1_mod[1]) ||
            !pg_IntFromObjIndex(p1_modobj, 2, &p1_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p1_mod argument");
        }
        if (PySequence_Size(p1_modobj) == 4) {
            pg_IntFromObjIndex(p1_modobj, 3, &p1_mod[3]);
        }
    }
    if (!Py_IsNone(p2_modobj)) {
        if (!pg_IntFromObjIndex(p2_modobj, 0, &p2_mod[0]) ||
            !pg_IntFromObjIndex(p2_modobj, 1, &p2_mod[1]) ||
            !pg_IntFromObjIndex(p2_modobj, 2, &p2_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p2_mod argument");
        }
        if (PySequence_Size(p2_modobj) == 4) {
            pg_IntFromObjIndex(p2_modobj, 3, &p2_mod[3]);
        }
    }
    if (!Py_IsNone(p3_modobj)) {
        if (!pg_IntFromObjIndex(p3_modobj, 0, &p3_mod[0]) ||
            !pg_IntFromObjIndex(p3_modobj, 1, &p3_mod[1]) ||
            !pg_IntFromObjIndex(p3_modobj, 2, &p3_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p3_mod argument");
        }
        if (PySequence_Size(p3_modobj) == 4) {
            pg_IntFromObjIndex(p3_modobj, 3, &p3_mod[3]);
        }
    }
    if (!Py_IsNone(p4_modobj)) {
        if (!pg_IntFromObjIndex(p4_modobj, 0, &p4_mod[0]) ||
            !pg_IntFromObjIndex(p4_modobj, 1, &p4_mod[1]) ||
            !pg_IntFromObjIndex(p4_modobj, 2, &p4_mod[2])) {
            return RAISE(PyExc_TypeError, "invalid p4_mod argument");
        }
        if (PySequence_Size(p4_modobj) == 4) {
            pg_IntFromObjIndex(p4_modobj, 3, &p4_mod[3]);
        }
    }
    RENDERER_ERROR_CHECK(
        SDL_GetTextureColorMod(self->texture, &_r_mod, &_g_mod, &_b_mod));
    RENDERER_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &_a_mod));

    r_mod = _r_mod / (float)255.0;
    g_mod = _g_mod / (float)255.0;
    b_mod = _b_mod / (float)255.0;
    a_mod = _a_mod / (float)255.0;

    vertices[0].position.x = p1_xy[0];
    vertices[0].position.y = p1_xy[1];
    vertices[0].tex_coord.x = p1_uv[0];
    vertices[0].tex_coord.y = p1_uv[1];
    vertices[0].color.r = (int)r_mod * p1_mod[0];
    vertices[0].color.g = (int)g_mod * p1_mod[1];
    vertices[0].color.b = (int)b_mod * p1_mod[2];
    vertices[0].color.a = (int)a_mod * p1_mod[3];
    vertices[1].position.x = p2_xy[0];
    vertices[1].position.y = p2_xy[1];
    vertices[1].tex_coord.x = p2_uv[0];
    vertices[1].tex_coord.y = p2_uv[1];
    vertices[1].color.r = (int)r_mod * p2_mod[0];
    vertices[1].color.g = (int)g_mod * p2_mod[1];
    vertices[1].color.b = (int)b_mod * p2_mod[2];
    vertices[1].color.a = (int)a_mod * p2_mod[3];
    vertices[2].position.x = p3_xy[0];
    vertices[2].position.y = p3_xy[1];
    vertices[2].tex_coord.x = p3_uv[0];
    vertices[2].tex_coord.y = p3_uv[1];
    vertices[2].color.r = (int)r_mod * p3_mod[0];
    vertices[2].color.g = (int)g_mod * p3_mod[1];
    vertices[2].color.b = (int)b_mod * p3_mod[2];
    vertices[2].color.a = (int)a_mod * p3_mod[3];
    vertices[3].position.x = p3_xy[0];
    vertices[3].position.y = p3_xy[1];
    vertices[3].tex_coord.x = p3_uv[0];
    vertices[3].tex_coord.y = p3_uv[1];
    vertices[3].color.r = (int)r_mod * p3_mod[0];
    vertices[3].color.g = (int)g_mod * p3_mod[1];
    vertices[3].color.b = (int)b_mod * p3_mod[2];
    vertices[3].color.a = (int)a_mod * p3_mod[3];
    vertices[4].position.x = p4_xy[0];
    vertices[4].position.y = p4_xy[1];
    vertices[4].tex_coord.x = p4_uv[0];
    vertices[4].tex_coord.y = p4_uv[1];
    vertices[4].color.r = (int)r_mod * p4_mod[0];
    vertices[4].color.g = (int)g_mod * p4_mod[1];
    vertices[4].color.b = (int)b_mod * p4_mod[2];
    vertices[4].color.a = (int)a_mod * p4_mod[3];
    vertices[5].position.x = p1_xy[0];
    vertices[5].position.y = p1_xy[1];
    vertices[5].tex_coord.x = p1_uv[0];
    vertices[5].tex_coord.y = p1_uv[1];
    vertices[5].color.r = (int)r_mod * p1_mod[0];
    vertices[5].color.g = (int)g_mod * p1_mod[1];
    vertices[5].color.b = (int)b_mod * p1_mod[2];
    vertices[5].color.a = (int)a_mod * p1_mod[3];
    RENDERER_ERROR_CHECK(SDL_RenderGeometry(
        self->renderer->renderer, self->texture, vertices, 6, NULL, 0))
    Py_RETURN_NONE;
#else
    RAISE(PyExc_TypeError, "draw_triangle() requires SDL 2.0.18 or newer");
    Py_RETURN_NONE;
#endif
}

static PyObject *
texture_update(pgTextureObject *self, PyObject *args, PyObject *kwargs)
{
    pgSurfaceObject *surfobj;
    PyObject *rectobj = Py_None;
    SDL_Surface *surf = NULL;
    SDL_Rect area, *areaptr = NULL;
    SDL_Surface *converted_surf = NULL;
    SDL_PixelFormat *pixel_format = NULL;
    SDL_BlendMode blend;
    Uint32 format;
    int res;
    int dst_width, dst_height;
    static char *keywords[] = {"surface", "area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|O", keywords,
                                     &pgSurface_Type, &surfobj, &rectobj)) {
        return NULL; /* Exception already set. */
    }
    surf = pgSurface_AsSurface(surfobj);
    SURF_INIT_CHECK(surf)
    area.x = 0;
    area.y = 0;
    if (!Py_IsNone(rectobj)) {
        if (!(areaptr = pgRect_FromObject(rectobj, &area))) {
            return RAISE(PyExc_ValueError, "area must be a rectangle or None");
        }
    }
    if (areaptr == NULL) {
        dst_width = self->width;
        dst_height = self->height;
    }
    else {
        dst_width = areaptr->w;
        dst_height = areaptr->h;
    }
    if (dst_width > surf->w || dst_height > surf->h) {
        areaptr = &area;
        areaptr->w = surf->w;
        areaptr->h = surf->h;
    }
    RENDERER_ERROR_CHECK(
        SDL_QueryTexture(self->texture, &format, NULL, NULL, NULL))
    if (format != surf->format->format) {
        RENDERER_ERROR_CHECK(SDL_GetSurfaceBlendMode(surf, &blend))
        pixel_format = SDL_AllocFormat(format);
        if (pixel_format == NULL) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        converted_surf = SDL_ConvertSurface(surf, pixel_format, 0);
        if (SDL_SetSurfaceBlendMode(converted_surf, blend) < 0) {
            SDL_FreeSurface(converted_surf);
            SDL_FreeFormat(pixel_format);
            return RAISE(pgExc_SDLError, SDL_GetError());
        }

        res = SDL_UpdateTexture(self->texture, areaptr, converted_surf->pixels,
                                converted_surf->pitch);
        SDL_FreeSurface(converted_surf);
        SDL_FreeFormat(pixel_format);
    }
    else {
        res = SDL_UpdateTexture(self->texture, areaptr, surf->pixels,
                                surf->pitch);
    }
    if (res < 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
texture_get_renderer(pgTextureObject *self, void *closure)
{
    Py_INCREF(self->renderer);
    return (PyObject *)self->renderer;
}

static PyObject *
texture_get_width(pgTextureObject *self, void *closure)
{
    return PyLong_FromLong(self->width);
}

static PyObject *
texture_get_height(pgTextureObject *self, void *closure)
{
    return PyLong_FromLong(self->height);
}

static PyObject *
texture_get_alpha(pgTextureObject *self, void *closure)
{
    Uint8 alpha;
    RENDERER_ERROR_CHECK(SDL_GetTextureAlphaMod(self->texture, &alpha));
    return PyLong_FromLong(alpha);
}

static int
texture_set_alpha(pgTextureObject *self, PyObject *arg, void *closure)
{
    if (PyLong_Check(arg)) {
        unsigned long ulongval = PyLong_AsUnsignedLong(arg);
        return set_texture_alpha_helper(self->texture, (Uint8)ulongval);
    }
    return -1;
}

static PyObject *
texture_get_blend_mode(pgTextureObject *self, void *closure)
{
    SDL_BlendMode blend_mode;
    RENDERER_ERROR_CHECK(SDL_GetTextureBlendMode(self->texture, &blend_mode));
    return PyLong_FromLong((long)blend_mode);
}

static int
texture_set_blend_mode(pgTextureObject *self, PyObject *arg, void *closure)
{
    if (PyLong_Check(arg)) {
        long longval = PyLong_AsLong(arg);
        return set_texture_blend_mode_helper(self->texture,
                                             (SDL_BlendMode)longval);
    }
    return 1;
}

static PyObject *
texture_get_color(pgTextureObject *self, void *closure)
{
    Uint8 color[4];
    RENDERER_ERROR_CHECK(SDL_GetTextureColorMod(self->texture, &color[0],
                                                &color[1], &color[2]));
    color[3] = 255;
    return pgColor_NewLength(color, 4);
}

static int
texture_set_color(pgTextureObject *self, PyObject *arg, void *closure)
{
    Uint8 color[4];
    if (!pg_RGBAFromObjEx(arg, color, PG_COLOR_HANDLE_ALL)) {
        return -1;
    }
    return set_texture_color_helper(self->texture, color[0], color[1],
                                    color[2]);
}

static int
texture_init(pgTextureObject *self, PyObject *args, PyObject *kwargs)
{
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

    char *keywords[] = {"renderer",  "size",   "depth",         "static",
                        "streaming", "target", "scale_quality", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|ipppi", keywords,
                                     &renderer, &sizeobj, &depth, &staticc,
                                     &streaming, &target, &scale_quality)) {
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
            RAISE(PyExc_ValueError,
                  "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_STATIC;
    }
    else if (streaming) {
        if (staticc || target) {
            RAISE(PyExc_ValueError,
                  "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_STREAMING;
    }
    else if (target) {
        if (staticc || streaming) {
            RAISE(PyExc_ValueError,
                  "only one of static, streaming, or target can be true");
            return -1;
        }
        access = SDL_TEXTUREACCESS_TARGET;
    }
    self->renderer = renderer;
    self->texture =
        SDL_CreateTexture(renderer->renderer, format, access, width, height);
    if (!self->texture) {
        RAISE(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    if (scale_quality != -1) {
        RENDERER_PROPERTY_ERROR_CHECK(
            SDL_SetTextureScaleMode(self->texture, scale_quality) < 0);
    }
    self->width = width;
    self->height = height;
    return 0;
}

static void
texture_dealloc(pgTextureObject *self, PyObject *_null)
{
    if (self->texture) {
        SDL_DestroyTexture(self->texture);
    }
    Py_TYPE(self)->tp_free(self);
}

/* Image implementation */
static void
image_renderer_draw(pgImageObject *self, PyObject *area, PyObject *dest)
{
    SDL_Rect tmp, *srcrectptr = NULL;
    SDL_FRect ftmp, *dstrectptr = NULL;
    SDL_FPoint *originptr = (self->has_origin) ? &self->origin : NULL;
    SDL_RendererFlip flip = SDL_FLIP_NONE;
    if (!Py_IsNone(area)) {
        if (!(srcrectptr = pgRect_FromObject(area, &tmp))) {
            RAISE(PyExc_ValueError, "srcrect must be a Rect or None");
        }
    }
    else {
        srcrectptr = &self->srcrect->r;
    }
    if (!Py_IsNone(dest)) {
        if (!(dstrectptr = parse_dest_rect(self->texture, dest, &ftmp))) {
            RAISE(PyExc_ValueError, "dstrect must be a point, Rect, or None");
        }
    }
    if (self->flip_x) {
        flip |= SDL_FLIP_HORIZONTAL;
    }
    if (self->flip_y) {
        flip |= SDL_FLIP_VERTICAL;
    }
    set_texture_color_helper(self->texture->texture, self->color->data[0],
                             self->color->data[1], self->color->data[2]);
    set_texture_alpha_helper(self->texture->texture, (Uint8)self->alpha);
    set_texture_blend_mode_helper(self->texture->texture, self->blend_mode);
    if (SDL_RenderCopyExF(self->texture->renderer->renderer,
                          self->texture->texture, srcrectptr, dstrectptr,
                          self->angle, originptr, flip) < 0) {
        RAISE(pgExc_SDLError, SDL_GetError());
    }
}

static PyObject *
image_get_rect(pgImageObject *self, PyObject *const *args, Py_ssize_t nargs,
               PyObject *kwargs)
{
    return pgRect_New(&(self->srcrect->r));
}

static PyObject *
image_draw(pgImageObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *srcrectobj = Py_None, *dstrectobj = Py_None;
    SDL_Rect tmp, *srcrectptr = NULL;
    SDL_FRect ftmp, *dstrectptr = NULL;
    SDL_FPoint *originptr = (self->has_origin) ? &self->origin : NULL;
    SDL_RendererFlip flip = SDL_FLIP_NONE;
    static char *keywords[] = {"srcrect", "dstrect", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OO", keywords,
                                     &srcrectobj, &dstrectobj)) {
        return NULL;
    }
    if (!Py_IsNone(srcrectobj)) {
        if (!(srcrectptr = pgRect_FromObject(srcrectobj, &tmp))) {
            return RAISE(PyExc_ValueError, "srcrect must be a Rect or None");
        }
    }
    else {
        srcrectptr = &self->srcrect->r;
    }
    if (!Py_IsNone(dstrectobj)) {
        if (!(dstrectptr =
                  parse_dest_rect(self->texture, dstrectobj, &ftmp))) {
            RAISE(PyExc_ValueError, "dstrect must be a point, Rect, or None");
        }
    }
    if (self->flip_x) {
        flip |= SDL_FLIP_HORIZONTAL;
    }
    if (self->flip_y) {
        flip |= SDL_FLIP_VERTICAL;
    }
    set_texture_color_helper(self->texture->texture, self->color->data[0],
                             self->color->data[1], self->color->data[2]);
    set_texture_alpha_helper(self->texture->texture, (Uint8)self->alpha);
    set_texture_blend_mode_helper(self->texture->texture, self->blend_mode);
    RENDERER_ERROR_CHECK(SDL_RenderCopyExF(
        self->texture->renderer->renderer, self->texture->texture, srcrectptr,
        dstrectptr, self->angle, originptr, flip));
    Py_RETURN_NONE;
}

static PyObject *
image_get_alpha(pgImageObject *self, void *closure)
{
    return PyFloat_FromDouble((double)self->alpha);
}

static int
image_set_alpha(pgImageObject *self, PyObject *arg, void *closure)
{
    if (!PyNumber_Check(arg)) {
        RAISE(PyExc_TypeError, "alpha must be real number");
        return -1;
    }
    self->alpha = (float)PyFloat_AsDouble(arg);
    return 0;
}

static PyObject *
image_get_angle(pgImageObject *self, void *closure)
{
    return PyFloat_FromDouble((double)self->angle);
}

static int
image_set_angle(pgImageObject *self, PyObject *arg, void *closure)
{
    if (!PyNumber_Check(arg)) {
        RAISE(PyExc_TypeError, "angle must be real number");
        return -1;
    }
    self->angle = (float)PyFloat_AsDouble(arg);
    return 0;
}

static PyObject *
image_get_blend_mode(pgImageObject *self, void *closure)
{
    return PyLong_FromLong((long)self->blend_mode);
}

static int
image_set_blend_mode(pgImageObject *self, PyObject *arg, void *closure)
{
    if (!PyLong_Check(arg)) {
        RAISE(PyExc_TypeError, "Blend mode must be an integer");
        return -1;
    }
    self->blend_mode = (SDL_BlendMode)(PyLong_AsLong(arg));
    return 0;
}

static PyObject *
image_get_color(pgImageObject *self, void *closure)
{
    Py_INCREF(self->color);
    return (PyObject *)self->color;
}

static int
image_set_color(pgImageObject *self, PyObject *arg, void *closure)
{
    Uint8 color[4];
    if (!pg_RGBAFromObjEx(arg, color, PG_COLOR_HANDLE_ALL)) {
        RAISE(PyExc_TypeError, "Unable to convert argument to Color");
        return -1;
    }
    for (int i = 0; i < 3; i++) {
        self->color->data[i] = color[i];
    }
    return 0;
}

static PyObject *
image_get_flip_x(pgImageObject *self, void *closure)
{
    return PyBool_FromLong(self->flip_x);
}

static int
image_set_flip_x(pgImageObject *self, PyObject *arg, void *closure)
{
    int value = PyObject_IsTrue(arg);
    if (value == -1) {
        RAISE(PyExc_TypeError, "flip_x must be boolean value");
        return -1;
    }
    self->flip_x = (SDL_bool)value;
    return 0;
}

static PyObject *
image_get_flip_y(pgImageObject *self, void *closure)
{
    return PyBool_FromLong(self->flip_y);
}

static int
image_set_flip_y(pgImageObject *self, PyObject *arg, void *closure)
{
    int value = PyObject_IsTrue(arg);
    if (value == -1) {
        RAISE(PyExc_TypeError, "flip_y must be boolean value");
        return -1;
    }
    self->flip_y = (SDL_bool)value;
    return 0;
}

static PyObject *
image_get_origin(pgImageObject *self, void *closure)
{
    if (!self->has_origin) {
        Py_RETURN_NONE;
    }
    return pg_tuple_couple_from_values_double(self->origin.x, self->origin.y);
}

static int
image_set_origin(pgImageObject *self, PyObject *arg, void *closure)
{
    if (!Py_IsNone(arg)) {
        if (!pg_TwoFloatsFromObj(arg, &self->origin.x, &self->origin.y)) {
            RAISE(PyExc_TypeError, "origin must be pair of floats");
            return -1;
        }
        self->has_origin = SDL_TRUE;
    }
    else {
        self->has_origin = SDL_FALSE;
    }
    return 0;
}

static PyObject *
image_get_srcrect(pgImageObject *self, void *closure)
{
    Py_INCREF(self->srcrect);
    return (PyObject *)self->srcrect;
}

static int
image_set_srcrect(pgImageObject *self, PyObject *arg, void *closure)
{
    SDL_Rect *rect, temp;
    if (!(rect = pgRect_FromObject(arg, &temp))) {
        RAISE(PyExc_TypeError, "srcrect must be a rectangle");
        return -1;
    }
    self->srcrect = (pgRectObject *)pgRect_New(rect);
    return 0;
}

static PyObject *
image_get_texture(pgImageObject *self, void *closure)
{
    Py_INCREF(self->texture);
    return (PyObject *)self->texture;
}

static int
image_set_texture(pgImageObject *self, PyObject *arg, void *closure)
{
    if (!pgTexture_Check(arg)) {
        RAISE(PyExc_TypeError, "texture must be a Texture");
        return -1;
    }
    self->texture = (pgTextureObject *)arg;
    return 0;
}

static int
image_init(pgImageObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *texture_or_imageobj, *srcrectobj = Py_None;
    pgTextureObject *textureprt;
    SDL_Rect *rect, temp, old_srcrect;
    SDL_BlendMode blend_mode;
    Uint8 rgba[4] = {255, 255, 255, 255};
    char *keywords[] = {"texture_or_image", "srcrect", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", keywords,
                                     &texture_or_imageobj, &srcrectobj)) {
        return -1;
    }
    if (pgTexture_Check(texture_or_imageobj)) {
        textureprt = (pgTextureObject *)texture_or_imageobj;
        temp = (SDL_Rect){0, 0, textureprt->width, textureprt->height};
    }
    else if (pgImage_Check(texture_or_imageobj)) {
        textureprt = ((pgImageObject *)texture_or_imageobj)->texture;
        temp = ((pgImageObject *)texture_or_imageobj)->srcrect->r;
    }
    else {
        RAISE(PyExc_AttributeError,
              "First argument must be either Texture or Image object");
        return -1;
    }
    self->texture = textureprt;
    Py_INCREF(self->texture);
    if (Py_IsNone(srcrectobj)) {
        self->srcrect = (pgRectObject *)pgRect_New(&temp);
    }
    else {
        old_srcrect = temp;
        if (!(rect = pgRect_FromObject(srcrectobj, &temp))) {
            RAISE(PyExc_TypeError, "srcrect must be a rectangle or None");
            return -1;
        }
        if (rect->x < 0 || rect->y < 0 || rect->w < 0 || rect->h < 0 ||
            rect->x + rect->w > old_srcrect.w ||
            rect->y + rect->h > old_srcrect.h) {
            RAISE(PyExc_ValueError, "srcrect values are out of range");
            return -1;
        }
        rect->x += old_srcrect.x;
        rect->y += old_srcrect.y;
        self->srcrect = (pgRectObject *)pgRect_New(rect);
    }
    RENDERER_PROPERTY_ERROR_CHECK(
        SDL_GetTextureBlendMode(self->texture->texture, &blend_mode));
    self->angle = 0;
    self->blend_mode = blend_mode;
    self->origin.x = 0;
    self->origin.y = 0;
    self->has_origin = SDL_FALSE;
    self->flip_x = SDL_FALSE;
    self->flip_y = SDL_FALSE;
    self->alpha = 255;
    self->color = (pgColorObject *)pgColor_NewLength(rgba, 4);
    return 0;
}

static void
image_dealloc(pgTextureObject *self, PyObject *_null)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

/* Module definition */
static PyMethodDef renderer_methods[] = {
    {"draw_point", (PyCFunction)renderer_draw_point,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_DRAWPOINT},
    {"draw_line", (PyCFunction)renderer_draw_line,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_DRAWLINE},
    {"draw_rect", (PyCFunction)renderer_draw_rect,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_DRAWRECT},
    {"draw_triangle", (PyCFunction)renderer_draw_triangle,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_DRAWTRIANGLE},
    {"draw_quad", (PyCFunction)renderer_draw_quad,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_DRAWQUAD},
    {"fill_rect", (PyCFunction)renderer_fill_rect,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_FILLRECT},
    {"fill_triangle", (PyCFunction)renderer_fill_triangle,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_FILLTRIANGLE},
    {"fill_quad", (PyCFunction)renderer_fill_quad,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_FILLQUAD},
    {"present", (PyCFunction)renderer_present, METH_NOARGS,
     DOC_SDL2_VIDEO_RENDERER_PRESENT},
    {"clear", (PyCFunction)renderer_clear, METH_NOARGS,
     DOC_SDL2_VIDEO_RENDERER_CLEAR},
    {"set_viewport", (PyCFunction)renderer_set_viewport,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_SETVIEWPORT},
    {"get_viewport", (PyCFunction)renderer_get_viewport, METH_NOARGS,
     DOC_SDL2_VIDEO_RENDERER_GETVIEWPORT},
    {"compose_custom_blend_mode", (PyCFunction)compose_custom_blend_mode,
     METH_VARARGS | METH_KEYWORDS | METH_CLASS,
     DOC_SDL2_VIDEO_RENDERER_COMPOSECUSTOMBLENDMODE},
    {"from_window", (PyCFunction)from_window,
     METH_CLASS | METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_GETGRABBEDWINDOW},
    {"to_surface", (PyCFunction)renderer_to_surface,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_RENDERER_TOSURFACE},
    {"blit", (PyCFunction)renderer_blit, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_RENDERER_SETVIEWPORT},
    {NULL, NULL, 0, NULL}};

static PyGetSetDef renderer_getset[] = {
    {"draw_color", (getter)renderer_get_draw_color,
     (setter)renderer_set_draw_color, DOC_SDL2_VIDEO_RENDERER_DRAWCOLOR, NULL},
    {"draw_blend_mode", (getter)renderer_get_draw_blend_mode,
     (setter)renderer_set_draw_blend_mode, DOC_SDL2_VIDEO_RENDERER_DRAWCOLOR,
     NULL},
    {"logical_size", (getter)renderer_get_logical_size,
     (setter)renderer_set_logical_size, DOC_SDL2_VIDEO_RENDERER_LOGICALSIZE,
     NULL},
    {"scale", (getter)renderer_get_scale, (setter)renderer_set_scale,
     DOC_SDL2_VIDEO_RENDERER_SCALE, NULL},
    {"target", (getter)renderer_get_target, (setter)renderer_set_target,
     DOC_SDL2_VIDEO_RENDERER_TARGET, NULL},
    {NULL, 0, NULL, NULL, NULL}};

static PyMethodDef texture_methods[] = {
    {"get_rect", (PyCFunction)texture_get_rect, METH_FASTCALL | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_GETRECT},
    {"draw", (PyCFunction)texture_draw, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_DRAW},
    {"draw_triangle", (PyCFunction)texture_draw_triangle,
     METH_VARARGS | METH_KEYWORDS, DOC_SDL2_VIDEO_TEXTURE_DRAWTRIANGLE},
    {"draw_quad", (PyCFunction)texture_draw_quad, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_DRAWQUAD},
    {"update", (PyCFunction)texture_update, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_TEXTURE_UPDATE},
    {"from_surface", (PyCFunction)from_surface,
     METH_VARARGS | METH_KEYWORDS | METH_CLASS,
     DOC_SDL2_VIDEO_TEXTURE_FROMSURFACE},
    {NULL, NULL, 0, NULL}};

static PyGetSetDef texture_getset[] = {
    {"renderer", (getter)texture_get_renderer, (setter)NULL,
     DOC_SDL2_VIDEO_TEXTURE_RENDERER, NULL},
    {"width", (getter)texture_get_width, (setter)NULL,
     DOC_SDL2_VIDEO_TEXTURE_WIDTH, NULL},
    {"height", (getter)texture_get_height, (setter)NULL,
     DOC_SDL2_VIDEO_TEXTURE_HEIGHT, NULL},
    {"alpha", (getter)texture_get_alpha, (setter)texture_set_alpha,
     DOC_SDL2_VIDEO_TEXTURE_ALPHA, NULL},
    {"blend_mode", (getter)texture_get_blend_mode,
     (setter)texture_set_blend_mode, DOC_SDL2_VIDEO_TEXTURE_BLENDMODE, NULL},
    {"color", (getter)texture_get_color, (setter)texture_set_color,
     DOC_SDL2_VIDEO_TEXTURE_COLOR, NULL},
    {NULL, 0, NULL, NULL, NULL}};

static PyMethodDef image_methods[] = {
    {"get_rect", (PyCFunction)image_get_rect, METH_NOARGS,
     DOC_SDL2_VIDEO_IMAGE_GETRECT},
    {"draw", (PyCFunction)image_draw, METH_VARARGS | METH_KEYWORDS,
     DOC_SDL2_VIDEO_IMAGE_DRAW},
    {NULL, NULL, 0, NULL}};

static PyGetSetDef image_getset[] = {
    {"alpha", (getter)image_get_alpha, (setter)image_set_alpha,
     DOC_SDL2_VIDEO_IMAGE_ALPHA, NULL},
    {"angle", (getter)image_get_angle, (setter)image_set_angle,
     DOC_SDL2_VIDEO_IMAGE_ANGLE, NULL},
    {"blend_mode", (getter)image_get_blend_mode, (setter)image_set_blend_mode,
     DOC_SDL2_VIDEO_IMAGE_BLENDMODE, NULL},
    {"color", (getter)image_get_color, (setter)image_set_color,
     DOC_SDL2_VIDEO_IMAGE_COLOR, NULL},
    {"flip_x", (getter)image_get_flip_x, (setter)image_set_flip_x,
     DOC_SDL2_VIDEO_IMAGE_FLIPX, NULL},
    {"flip_y", (getter)image_get_flip_y, (setter)image_set_flip_y,
     DOC_SDL2_VIDEO_IMAGE_FLIPY, NULL},
    {"origin", (getter)image_get_origin, (setter)image_set_origin,
     DOC_SDL2_VIDEO_IMAGE_ORIGIN, NULL},
    {"srcrect", (getter)image_get_srcrect, (setter)image_set_srcrect,
     DOC_SDL2_VIDEO_IMAGE_SRCRECT, NULL},
    {"texture", (getter)image_get_texture, (setter)image_set_texture,
     DOC_SDL2_VIDEO_IMAGE_TEXTURE, NULL},
    {NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgRenderer_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Renderer",
    .tp_basicsize = sizeof(pgRendererObject),
    .tp_dealloc = (destructor)renderer_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_RENDERER,
    .tp_methods = renderer_methods,
    .tp_init = (initproc)renderer_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = renderer_getset};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    .tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE,
    .tp_methods = texture_methods,
    .tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = texture_getset};

static PyTypeObject pgImage_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._renderer.Image",
    .tp_basicsize = sizeof(pgImageObject),
    .tp_dealloc = (destructor)image_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_IMAGE,
    .tp_methods = image_methods,
    .tp_init = (initproc)image_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = image_getset};

static PyMethodDef _renderer_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_renderer)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RENDERER_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_renderer",
                                         "docs_needed",
                                         -1,
                                         _renderer_methods,
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

    if (PyType_Ready(&pgRenderer_Type) < 0) {
        return NULL;
    }

    if (PyType_Ready(&pgTexture_Type) < 0) {
        return NULL;
    }

    if (PyType_Ready(&pgImage_Type) < 0) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (module == 0) {
        return NULL;
    }

    Py_INCREF(&pgRenderer_Type);
    if (PyModule_AddObject(module, "Renderer", (PyObject *)&pgRenderer_Type)) {
        Py_DECREF(&pgRenderer_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgTexture_Type);
    if (PyModule_AddObject(module, "Texture", (PyObject *)&pgTexture_Type)) {
        Py_DECREF(&pgTexture_Type);
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&pgImage_Type);
    if (PyModule_AddObject(module, "Image", (PyObject *)&pgImage_Type)) {
        Py_DECREF(&pgImage_Type);
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgRenderer_Type;
    c_api[1] = &pgTexture_Type;
    c_api[2] = &pgImage_Type;
    apiobj = encapsulate_api(c_api, "_renderer");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
