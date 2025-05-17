#define PYGAMEAPI_RENDER_INTERNAL

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

#define RENDERER_PROPERTY_ERROR_CHECK(x)                 \
    if (x < 0) {                                         \
        RAISERETURN(pgExc_SDLError, SDL_GetError(), -1); \
    }

#define PARSE_POINT(obj, x, y, name)                                 \
    if (!pg_TwoFloatsFromObj(obj, &x, &y)) {                         \
        return RAISE(PyExc_TypeError, "invalid " #name " argument"); \
    }

static void
texture_renderer_draw(pgTextureObject *self, PyObject *area, PyObject *dest);

static void
image_renderer_draw(pgImageObject *self, PyObject *area, PyObject *dest);

/* Renderer implementation */
static PyObject *
renderer_from_window(PyTypeObject *cls, PyObject *args, PyObject *kwargs)
{
    PyObject *window;
    static char *keywords[] = {"window", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", keywords,
                                     &pgWindow_Type, &window)) {
        return NULL;
    }
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
    Py_INCREF(self);
    return (PyObject *)self;
}

static PyObject *
renderer_draw_point(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *point;
    SDL_FPoint pos;
    static char *keywords[] = {"point", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &point)) {
        return NULL;
    }
    if (!pg_TwoFloatsFromObj(point, &pos.x, &pos.y)) {
        return RAISE(PyExc_TypeError, "invalid argument");
    }
    RENDERER_ERROR_CHECK(SDL_RenderDrawPointF(self->renderer, pos.x, pos.y))
    Py_RETURN_NONE;
}

static PyObject *
renderer_draw_line(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *start, *end;
    SDL_FPoint start_pos, end_pos;
    static char *keywords[] = {"p1", "p2", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO", keywords, &start,
                                     &end)) {
        return NULL;
    }
    PARSE_POINT(start, start_pos.x, start_pos.y, "p1")
    PARSE_POINT(end, end_pos.x, end_pos.y, "p2")
    RENDERER_ERROR_CHECK(SDL_RenderDrawLineF(
        self->renderer, start_pos.x, start_pos.y, end_pos.x, end_pos.y))
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
    SDL_FPoint points[4];
    static char *keywords[] = {"p1", "p2", "p3", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO", keywords, &p1, &p2,
                                     &p3)) {
        return NULL;
    }
    PARSE_POINT(p1, points[0].x, points[0].y, "p1")
    PARSE_POINT(p2, points[1].x, points[1].y, "p2")
    PARSE_POINT(p3, points[2].x, points[2].y, "p3")
    points[3] = points[0];
    RENDERER_ERROR_CHECK(SDL_RenderDrawLinesF(self->renderer, points, 4))
    Py_RETURN_NONE;
}

static PyObject *
renderer_fill_triangle(pgRendererObject *self, PyObject *args,
                       PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1, *p2, *p3;
    SDL_Vertex vertices[3];
    static char *keywords[] = {"p1", "p2", "p3", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO", keywords, &p1, &p2,
                                     &p3)) {
        return NULL;
    }
    PARSE_POINT(p1, vertices[0].position.x, vertices[0].position.y, "p1")
    PARSE_POINT(p2, vertices[1].position.x, vertices[1].position.y, "p2")
    PARSE_POINT(p3, vertices[2].position.x, vertices[2].position.y, "p3")
    RENDERER_ERROR_CHECK(SDL_GetRenderDrawColor(
        self->renderer, &vertices[0].color.r, &vertices[0].color.g,
        &vertices[0].color.b, &vertices[0].color.a))
    vertices[1].color = vertices[0].color;
    vertices[2].color = vertices[0].color;
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
    SDL_FPoint points[5];
    static char *keywords[] = {"p1", "p2", "p3", "p4", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO", keywords, &p1, &p2,
                                     &p3, &p4)) {
        return NULL;
    }
    PARSE_POINT(p1, points[0].x, points[0].y, "p1")
    PARSE_POINT(p2, points[1].x, points[1].y, "p2")
    PARSE_POINT(p3, points[2].x, points[2].y, "p3")
    PARSE_POINT(p4, points[3].x, points[3].y, "p4")
    points[4] = points[0];
    RENDERER_ERROR_CHECK(SDL_RenderDrawLinesF(self->renderer, points, 5))
    Py_RETURN_NONE;
}

static PyObject *
renderer_fill_quad(pgRendererObject *self, PyObject *args, PyObject *kwargs)
{
#if SDL_VERSION_ATLEAST(2, 0, 18)
    PyObject *p1, *p2, *p3, *p4;
    SDL_Vertex vertices[4];
    static char *keywords[] = {"p1", "p2", "p3", "p4", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOOO", keywords, &p1, &p2,
                                     &p3, &p4)) {
        return NULL;
    }
    PARSE_POINT(p1, vertices[0].position.x, vertices[0].position.y, "p1")
    PARSE_POINT(p2, vertices[1].position.x, vertices[1].position.y, "p2")
    PARSE_POINT(p3, vertices[2].position.x, vertices[2].position.y, "p3")
    PARSE_POINT(p4, vertices[3].position.x, vertices[3].position.y, "p4")
    RENDERER_ERROR_CHECK(SDL_GetRenderDrawColor(
        self->renderer, &vertices[0].color.r, &vertices[0].color.g,
        &vertices[0].color.b, &vertices[0].color.a))
    for (int i = 1; i < 4; i++) {
        vertices[i].color = vertices[0].color;
    }
    const int indices[] = {0, 1, 2, 2, 3, 0};
    RENDERER_ERROR_CHECK(
        SDL_RenderGeometry(self->renderer, NULL, vertices, 4, indices, 6))
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
    PyObject *rectobj;
    SDL_Rect *rect = NULL, temp;
    static char *keywords[] = {"area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &rectobj)) {
        return NULL;
    }
    if (rectobj == Py_None) {
        RENDERER_ERROR_CHECK(SDL_RenderSetViewport(self->renderer, NULL))
    }
    else {
        if (!(rect = pgRect_FromObject(rectobj, &temp))) {
            return RAISE(PyExc_TypeError, "area must be rectangle or None");
        }
        RENDERER_ERROR_CHECK(SDL_RenderSetViewport(self->renderer, rect))
    }
    Py_RETURN_NONE;
}

static PyObject *
renderer_compose_custom_blend_mode(PyObject *self, PyObject *args,
                                   PyObject *kwargs)
{
    int mode[6];
    SDL_BlendMode blend_mode;
    static char *keywords[] = {"color_mode", "alpha_mode", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "(iii)(iii)", keywords,
                                     &mode[0], &mode[1], &mode[2], &mode[3],
                                     &mode[4], &mode[5])) {
        return NULL;
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
    SDL_Rect viewport, *areaparam, temp, *rect = &temp;
    Uint32 format;
    static char *keywords[] = {"surface", "area", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|OO", keywords, &surfobj,
                                     &rectobj)) {
        return NULL;
    }
    if (!Py_IsNone(rectobj)) {
        if (!(rect = pgRect_FromObject(rectobj, &temp))) {
            return RAISE(PyExc_TypeError, "area must be None or a rect");
        }
        SDL_RenderGetViewport(self->renderer, &viewport);
        SDL_IntersectRect(rect, &viewport, rect);
        areaparam = rect;
    }
    else {
        SDL_RenderGetViewport(self->renderer, rect);
        areaparam = NULL;
    }
    if (!Py_IsNone(surfobj)) {
        if (!(pgSurface_Check(surfobj))) {
            return RAISE(PyExc_TypeError, "surface must be None or a Surface");
        }
        surface = (pgSurfaceObject *)surfobj;
        Py_INCREF(surface);
        surf = surface->surf;
        if (surf->w < rect->w || surf->h < rect->h) {
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
            0, rect->w, rect->h, SDL_BITSPERPIXEL(format), format);
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
    else {
        if (!PyObject_CallFunctionObjArgs(
                PyObject_GetAttrString(sourceobj, "draw"), areaobj, destobj,
                NULL)) {
            return NULL;
        }
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
        RAISERETURN(PyExc_TypeError, "Draw blend mode must be int", -1);
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
        RAISERETURN(PyExc_TypeError, "invalid logical size", -1);
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
        RAISERETURN(PyExc_TypeError, "invalid scale", -1);
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
        RAISERETURN(PyExc_TypeError, "target must be Texture object or None",
                    -1);
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
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!|iipp", keywords,
                                     &pgWindow_Type, &window, &index,
                                     &accelerated, &vsync, &target_texture)) {
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
    return;
}

/* Image implementation */
static void
image_renderer_draw(pgImageObject *self, PyObject *area, PyObject *dest)
{
    return;
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
    {"compose_custom_blend_mode",
     (PyCFunction)renderer_compose_custom_blend_mode,
     METH_VARARGS | METH_KEYWORDS | METH_CLASS,
     DOC_SDL2_VIDEO_RENDERER_COMPOSECUSTOMBLENDMODE},
    {"from_window", (PyCFunction)renderer_from_window,
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

static PyMethodDef texture_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef texture_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyMethodDef image_methods[] = {{NULL, NULL, 0, NULL}};

static PyGetSetDef image_getset[] = {{NULL, 0, NULL, NULL, NULL}};

static PyTypeObject pgRenderer_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Renderer",
    .tp_basicsize = sizeof(pgRendererObject),
    .tp_dealloc = (destructor)renderer_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_RENDERER,
    .tp_methods = renderer_methods,
    .tp_init = (initproc)renderer_init,
    .tp_new = PyType_GenericNew,
    .tp_getset = renderer_getset};

static PyTypeObject pgTexture_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Texture",
    .tp_basicsize = sizeof(pgTextureObject),
    //.tp_dealloc = (destructor)texture_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_TEXTURE, .tp_methods = texture_methods,
    //.tp_init = (initproc)texture_init,
    .tp_new = PyType_GenericNew, .tp_getset = texture_getset};

static PyTypeObject pgImage_Type = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pygame._render.Image",
    .tp_basicsize = sizeof(pgImageObject),
    //.tp_dealloc = (destructor)image_dealloc,
    .tp_doc = DOC_SDL2_VIDEO_IMAGE, .tp_methods = image_methods,
    //.tp_init = (initproc)image_init,
    .tp_new = PyType_GenericNew, .tp_getset = image_getset};

static PyMethodDef _render_methods[] = {{NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_render)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_RENDER_NUMSLOTS];

    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         "_render",
                                         "docs_needed",
                                         -1,
                                         _render_methods,
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

    import_pygame_window();
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

    if (PyModule_AddObjectRef(module, "Renderer",
                              (PyObject *)&pgRenderer_Type)) {
        Py_DECREF(module);
        return NULL;
    }

    if (PyModule_AddObjectRef(module, "Texture",
                              (PyObject *)&pgTexture_Type)) {
        Py_DECREF(module);
        return NULL;
    }

    if (PyModule_AddObjectRef(module, "Image", (PyObject *)&pgImage_Type)) {
        Py_DECREF(module);
        return NULL;
    }

    c_api[0] = &pgRenderer_Type;
    c_api[1] = &pgTexture_Type;
    c_api[2] = &pgImage_Type;
    apiobj = encapsulate_api(c_api, "_render");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
