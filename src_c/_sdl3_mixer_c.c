#include <SDL3_mixer/SDL_mixer.h>
#include "pygame.h"
#include "pgcompat.h"
#include "_base_audio.h"

// Useful heap type example @
// https://github.com/python/cpython/blob/main/Modules/xxlimited.c

// ***************************************************************************
// OVERALL DEFINITIONS
// ***************************************************************************

typedef struct {
    bool mixer_initialized;
    PyObject *mixer_obj_type;
    PyObject *audio_obj_type;
    PyObject *track_obj_type;
} _mixer_state;

#define GET_STATE(x) (_mixer_state *)PyModule_GetState(x)

typedef struct {
    PyObject_HEAD MIX_Mixer *mixer;
} PGMixerObject;

typedef struct {
    PyObject_HEAD MIX_Audio *audio;
} PGAudioObject;

typedef struct {
    PyObject_HEAD MIX_Track *track;
    PyObject *mixer_obj;
    PyObject *source_obj;
} PGTrackObject;

// ***************************************************************************
// GLOBAL HELPER FUNCTIONS
// ***************************************************************************

#define SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(props, property, value, \
                                              default, success)       \
    if (value != default) {                                           \
        success &= SDL_SetNumberProperty(props, property, value);     \
    }

static bool
pg_populate_play_props(SDL_PropertiesID options, int64_t loops,
                       int64_t max_frame, int64_t max_ms, int64_t start_frame,
                       int64_t start_ms, int64_t loop_start_frame,
                       int64_t loop_start_ms, int64_t fadein_frames,
                       int64_t fadein_ms, int64_t append_silence_frames,
                       int64_t append_silence_ms)
{
    bool success = true;

    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(options, MIX_PROP_PLAY_LOOPS_NUMBER,
                                          loops, 0, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_MAX_FRAME_NUMBER, max_frame, -1, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_MAX_MILLISECONDS_NUMBER, max_ms, -1, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_START_FRAME_NUMBER, start_frame, 0, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_START_MILLISECOND_NUMBER, start_ms, 0, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_LOOP_START_FRAME_NUMBER, loop_start_frame, 0,
        success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_LOOP_START_MILLISECOND_NUMBER, loop_start_ms, 0,
        success);

    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(options,
                                          MIX_PROP_PLAY_FADE_IN_FRAMES_NUMBER,
                                          fadein_frames, 0, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_FADE_IN_MILLISECONDS_NUMBER, fadein_ms, 0,
        success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_APPEND_SILENCE_FRAMES_NUMBER,
        append_silence_frames, 0, success);
    SET_NUM_PROPERTY_IFNOTDEFAULT_ANDFLAG(
        options, MIX_PROP_PLAY_APPEND_SILENCE_MILLISECONDS_NUMBER,
        append_silence_ms, 0, success);

    return success;
}

// ***************************************************************************
// MIXER.MIXER CLASS
// ***************************************************************************

static PyObject *
pg_mixer_obj_play_audio(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    PGAudioObject *audio;
    char *keywords[] = {"audio", NULL};
    PyObject *audio_type =
        PyObject_GetAttrString((PyObject *)self, "_audio_type");

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O!", keywords, audio_type,
                                     &audio)) {
        Py_DECREF(audio_type);
        return NULL;
    }
    Py_DECREF(audio_type);

    if (!MIX_PlayAudio(self->mixer, audio->audio)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_play_tag(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    int64_t loops = 0;
    int64_t max_ms = -1;
    int64_t start_ms = 0, loop_start_ms = 0;
    int64_t fadein_ms = 0, append_silence_ms = 0;
    char *keywords[] = {"tag",
                        "loops",
                        "max_ms",
                        "start_ms",
                        "loop_start_ms",
                        "fadein_ms",
                        "append_silence_ms",
                        NULL};

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs, "s|LLLLLL", keywords, &tag, &loops, &max_ms,
            &start_ms, &loop_start_ms, &fadein_ms, &append_silence_ms)) {
        return NULL;
    }

    SDL_PropertiesID options = SDL_CreateProperties();
    if (options == 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    // Since frames can be not meaningful between tracks with different sample
    // rates, the frames arguments are not passed through here or exposed to
    // Python, unlike in Track.play().
    bool success = pg_populate_play_props(options, loops, -1, max_ms, 0,
                                          start_ms, 0, loop_start_ms, 0,
                                          fadein_ms, 0, append_silence_ms);

    if (!success || !MIX_PlayTag(self->mixer, tag, options)) {
        SDL_DestroyProperties(options);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    SDL_DestroyProperties(options);
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_stop_tag(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    int64_t fade_out_ms = 0;
    char *keywords[] = {"tag", "fade_out_ms", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|L", keywords, &tag,
                                     &fade_out_ms)) {
        return NULL;
    }

    if (!MIX_StopTag(self->mixer, tag, fade_out_ms)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_pause_tag(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    char *keywords[] = {"tag", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", keywords, &tag)) {
        return NULL;
    }

    if (!MIX_PauseTag(self->mixer, tag)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_resume_tag(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    char *keywords[] = {"tag", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", keywords, &tag)) {
        return NULL;
    }

    if (!MIX_ResumeTag(self->mixer, tag)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_set_tag_gain(PGMixerObject *self, PyObject *args,
                          PyObject *kwargs)
{
    char *tag;
    float gain;
    char *keywords[] = {"tag", "gain", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "sf", keywords, &tag,
                                     &gain)) {
        return NULL;
    }

    if (!MIX_SetTagGain(self->mixer, tag, gain)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_stop_all_tracks(PGMixerObject *self, PyObject *args,
                             PyObject *kwargs)
{
    int64_t fade_out_ms = 0;
    char *keywords[] = {"fade_out_ms", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|L", keywords,
                                     &fade_out_ms)) {
        return NULL;
    }

    if (!MIX_StopAllTracks(self->mixer, fade_out_ms)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_pause_all_tracks(PGMixerObject *self, PyObject *_null)
{
    if (!MIX_PauseAllTracks(self->mixer)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_resume_all_tracks(PGMixerObject *self, PyObject *_null)
{
    if (!MIX_ResumeAllTracks(self->mixer)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_obj_get_spec(PGMixerObject *self, PyObject *_null)
{
    SDL_AudioSpec spec;
    if (!MIX_GetMixerFormat(self->mixer, &spec)) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return NULL;
    }

    return Py_BuildValue("iii", spec.format, spec.channels, spec.freq);
}

static int
pg_mixer_obj_init(PGMixerObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *device_obj;
    PyObject *spec_obj = Py_None;

    char *keywords[] = {"device", "spec", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", keywords,
                                     &device_obj, &spec_obj)) {
        return -1;
    }

    SDL_AudioSpec *spec_p = NULL;
    SDL_AudioSpec spec;
    // if the passed in spec obj is not None, we assume it is a correctly laid
    // out tuple of elements created by the Python layer for us.
    if (spec_obj != Py_None) {
        spec.format = PyLong_AsInt(PyTuple_GetItem(spec_obj, 0));
        spec.channels = PyLong_AsInt(PyTuple_GetItem(spec_obj, 1));
        spec.freq = PyLong_AsInt(PyTuple_GetItem(spec_obj, 2));

        // Check that they all succeeded
        if (spec.format == -1 || spec.channels == -1 || spec.freq == -1) {
            if (PyErr_Occurred()) {
                return -1;
            }
        }

        spec_p = &spec;
    }

    self->mixer = MIX_CreateMixerDevice(
        ((PGAudioDeviceStateObject *)device_obj)->devid, spec_p);
    if (self->mixer == NULL) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }

    return 0;
}

static void
pg_mixer_obj_dealloc(PGMixerObject *self)
{
    MIX_DestroyMixer(self->mixer);
    self->mixer = NULL;
    PyObject_GC_UnTrack(self);
    PyTypeObject *tp = Py_TYPE(self);
    freefunc free = PyType_GetSlot(tp, Py_tp_free);
    free(self);
    Py_DECREF(tp);
}

static PyObject *
pg_mixer_obj_get_gain(PGMixerObject *self, void *_null)
{
    return PyFloat_FromDouble(MIX_GetMixerGain(self->mixer));
}

static int
pg_mixer_obj_set_gain(PGMixerObject *self, PyObject *value, void *_null)
{
    double gain = PyFloat_AsDouble(value);
    if (gain == -1.0 && PyErr_Occurred()) {
        return -1;
    }
    if (!MIX_SetMixerGain(self->mixer, (float)gain)) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    return 0;
}

// The documentation says heap types need to support GC, so we're implementing
// traverse even though the object has no explicit references.
static int
pg_mixer_obj_traverse(PyObject *op, visitproc visit, void *arg)
{
    // Visit the type
    Py_VISIT(Py_TYPE(op));
    return 0;
}

static PyGetSetDef mixer_obj_getsets[] = {
    {"gain", (getter)pg_mixer_obj_get_gain, (setter)pg_mixer_obj_set_gain,
     "TODO", NULL},
    {NULL, NULL, NULL, NULL, NULL}};

static PyMethodDef mixer_obj_methods[] = {
    {"play_tag", (PyCFunction)pg_mixer_obj_play_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"stop_tag", (PyCFunction)pg_mixer_obj_stop_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"pause_tag", (PyCFunction)pg_mixer_obj_pause_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"resume_tag", (PyCFunction)pg_mixer_obj_resume_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"set_tag_gain", (PyCFunction)pg_mixer_obj_set_tag_gain,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"play_audio", (PyCFunction)pg_mixer_obj_play_audio,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"stop_all_tracks", (PyCFunction)pg_mixer_obj_stop_all_tracks,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"pause_all_tracks", (PyCFunction)pg_mixer_obj_pause_all_tracks,
     METH_NOARGS, "TODO"},
    {"resume_all_tracks", (PyCFunction)pg_mixer_obj_resume_all_tracks,
     METH_NOARGS, "TODO"},
    {"_get_spec", (PyCFunction)pg_mixer_obj_get_spec, METH_NOARGS, "TODO"},
    {NULL, NULL, 0, NULL}};

static PyType_Slot mixer_slots[] = {{Py_tp_methods, mixer_obj_methods},
                                    {Py_tp_init, pg_mixer_obj_init},
                                    {Py_tp_getset, mixer_obj_getsets},
                                    {Py_tp_dealloc, pg_mixer_obj_dealloc},
                                    {Py_tp_traverse, pg_mixer_obj_traverse},
                                    {0, NULL}};

static PyType_Spec mixer_spec = {
    .name = "Mixer",
    .basicsize = sizeof(PGMixerObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
    .slots = mixer_slots};

// ***************************************************************************
// MIXER.AUDIO CLASS
// ***************************************************************************

static int
pg_audio_obj_init(PGAudioObject *self, PyObject *args, PyObject *kwargs)
{
    int predecode = 0;
    PyObject *file = NULL;
    PyObject *mixer_or_none = Py_None;
    char *keywords[] = {"file", "predecode", "preferred_mixer", NULL};
    PyObject *mixer_type =
        PyObject_GetAttrString((PyObject *)self, "_mixer_type");

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|pO", keywords, &file,
                                     &predecode, &mixer_or_none)) {
        Py_DECREF(mixer_type);
        return -1;
    }

    MIX_Mixer *mixer = NULL;
    if (PyObject_IsInstance(mixer_or_none, mixer_type)) {
        mixer = ((PGMixerObject *)mixer_or_none)->mixer;
    }
    else if (!Py_IsNone(mixer_or_none)) {  // not mixer, not none
        Py_DECREF(mixer_type);
        PyErr_SetString(PyExc_TypeError, "argument 3 must be Mixer or None");
        return -1;
    }
    Py_DECREF(mixer_type);

    SDL_IOStream *io = pgRWops_FromObject(file, NULL);
    if (io == NULL) {
        return -1;
    }

    self->audio = MIX_LoadAudio_IO(mixer, io, predecode, true);
    if (self->audio == NULL) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }

    return 0;
}

static void
pg_audio_obj_dealloc(PGAudioObject *self)
{
    MIX_DestroyAudio(self->audio);
    self->audio = NULL;
    PyObject_GC_UnTrack(self);
    PyTypeObject *tp = Py_TYPE(self);
    freefunc free = PyType_GetSlot(tp, Py_tp_free);
    free(self);
    Py_DECREF(tp);
}

static PyObject *
pg_audio_obj_get_duration_frames(PGAudioObject *self, void *_null)
{
    int64_t duration_frames = MIX_GetAudioDuration(self->audio);
    if (duration_frames < 0) {
        Py_RETURN_NONE;  // infinite / unknown
    }
    return PyLong_FromInt64(duration_frames);
}

static PyObject *
pg_audio_obj_get_duration_ms(PGAudioObject *self, void *_null)
{
    int64_t duration_frames = MIX_GetAudioDuration(self->audio);
    if (duration_frames < 0) {
        Py_RETURN_NONE;  // infinite / unknown
    }
    int64_t duration_ms = MIX_AudioFramesToMS(self->audio, duration_frames);
    return PyLong_FromInt64(duration_ms);
}

static PyObject *
pg_audio_obj_get_duration_infinite(PGAudioObject *self, void *_null)
{
    int64_t duration_frames = MIX_GetAudioDuration(self->audio);
    if (duration_frames == MIX_DURATION_INFINITE) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;  // not infinite / unknown
}

static PyObject *
pg_audio_obj_from_raw(PyTypeObject *cls, PyObject *args, PyObject *kwargs)
{
    PyObject *buffer, *spec_obj;
    PyObject *mixer_or_none = Py_None;
    char *keywords[] = {"buffer", "spec", "preferred_mixer", NULL};
    PyObject *mixer_type =
        PyObject_GetAttrString((PyObject *)cls, "_mixer_type");

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO|O", keywords, &buffer,
                                     &spec_obj, &mixer_or_none)) {
        Py_DECREF(mixer_type);
        return NULL;
    }

    // We assume the passed spec obj is a 3-tuple of AudioSpec values
    // this is validated by the Python layer.
    SDL_AudioSpec spec;
    spec.format = PyLong_AsInt(PyTuple_GetItem(spec_obj, 0));
    spec.channels = PyLong_AsInt(PyTuple_GetItem(spec_obj, 1));
    spec.freq = PyLong_AsInt(PyTuple_GetItem(spec_obj, 2));

    // Check that they all succeeded
    if (spec.format == -1 || spec.channels == -1 || spec.freq == -1) {
        if (PyErr_Occurred()) {
            Py_DECREF(mixer_type);
            return NULL;
        }
    }

    MIX_Mixer *mixer = NULL;
    if (PyObject_IsInstance(mixer_or_none, mixer_type)) {
        mixer = ((PGMixerObject *)mixer_or_none)->mixer;
    }
    else if (!Py_IsNone(mixer_or_none)) {  // not mixer, not none
        Py_DECREF(mixer_type);
        return RAISE(PyExc_TypeError, "argument 3 must be Mixer or None");
    }
    Py_DECREF(mixer_type);

    PyObject *bytes = PyBytes_FromObject(buffer);
    if (bytes == NULL) {
        return NULL;
    }

    void *buf;
    Py_ssize_t len;
    if (PyBytes_AsStringAndSize(bytes, (char **)&buf, &len) != 0) {
        Py_DECREF(bytes);
        return NULL;
    }

    PGAudioObject *self = (PGAudioObject *)cls->tp_alloc(cls, 0);
    if (self == NULL) {
        Py_DECREF(bytes);
        return NULL;
    }

    MIX_Audio *raw_audio = MIX_LoadRawAudio(mixer, buf, (size_t)len, &spec);
    if (raw_audio == NULL) {
        Py_DECREF(bytes);
        Py_DECREF(self);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    self->audio = raw_audio;

    Py_DECREF(bytes);
    return (PyObject *)self;
}

static PyObject *
pg_audio_obj_from_sine_wave(PyTypeObject *cls, PyObject *args,
                            PyObject *kwargs)
{
    int hz, ms = -1;
    float amplitude;
    PyObject *mixer_or_none = Py_None;
    char *keywords[] = {"hz", "amplitude", "preferred_mixer", "ms", NULL};
    PyObject *mixer_type =
        PyObject_GetAttrString((PyObject *)cls, "_mixer_type");

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "if|Oi", keywords, &hz,
                                     &amplitude, &mixer_or_none, &ms)) {
        Py_DECREF(mixer_type);
        return NULL;
    }

    MIX_Mixer *mixer = NULL;
    if (PyObject_IsInstance(mixer_or_none, mixer_type)) {
        mixer = ((PGMixerObject *)mixer_or_none)->mixer;
    }
    else if (!Py_IsNone(mixer_or_none)) {  // not mixer, not none
        Py_DECREF(mixer_type);
        return RAISE(PyExc_TypeError, "argument 3 must be Mixer or None");
    }
    Py_DECREF(mixer_type);

    PGAudioObject *self = (PGAudioObject *)cls->tp_alloc(cls, 0);
    if (self == NULL) {
        return NULL;
    }

    // MIX_CreateSineWaveAudio is bugged right now (2025-10-04),
    // complains about invalid context parameter.
    MIX_Audio *sine_wave_audio =
        MIX_CreateSineWaveAudio(mixer, hz, amplitude, ms);
    if (sine_wave_audio == NULL) {
        Py_DECREF(self);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    self->audio = sine_wave_audio;
    return (PyObject *)self;
}

static PyObject *
pg_audio_obj_ms_to_frames(PGAudioObject *self, PyObject *args,
                          PyObject *kwargs)
{
    int64_t ms;
    char *keywords[] = {"ms", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "L", keywords, &ms)) {
        return NULL;
    }

    int64_t frames = MIX_AudioMSToFrames(self->audio, ms);
    if (frames == -1 && ms >= 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromInt64(frames);
}

static PyObject *
pg_audio_obj_frames_to_ms(PGAudioObject *self, PyObject *args,
                          PyObject *kwargs)
{
    int64_t frames;
    char *keywords[] = {"frames", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "L", keywords, &frames)) {
        return NULL;
    }

    int64_t ms = MIX_AudioFramesToMS(self->audio, frames);
    if (ms == -1 && frames >= 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromInt64(ms);
}

static PyObject *
pg_audio_obj_get_metadata(PGAudioObject *self, PyObject *_null)
{
    SDL_PropertiesID props = MIX_GetAudioProperties(self->audio);
    if (props == 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    // Lock properties for a bit while transferring data out, for safety
    if (!SDL_LockProperties(props)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    const char *title =
        SDL_GetStringProperty(props, MIX_PROP_METADATA_TITLE_STRING, NULL);
    const char *artist =
        SDL_GetStringProperty(props, MIX_PROP_METADATA_ARTIST_STRING, NULL);
    const char *album =
        SDL_GetStringProperty(props, MIX_PROP_METADATA_ALBUM_STRING, NULL);
    const char *copyright =
        SDL_GetStringProperty(props, MIX_PROP_METADATA_COPYRIGHT_STRING, NULL);

    PyObject *track_obj;
    if (SDL_GetPropertyType(props, MIX_PROP_METADATA_TRACK_NUMBER) ==
        SDL_PROPERTY_TYPE_NUMBER) {
        int64_t track_no =
            SDL_GetNumberProperty(props, MIX_PROP_METADATA_TRACK_NUMBER, 0);
        track_obj = PyLong_FromInt64(track_no);
    }
    else {
        track_obj = Py_NewRef(Py_None);
    }

    PyObject *total_track_obj;
    if (SDL_GetPropertyType(props, MIX_PROP_METADATA_TOTAL_TRACKS_NUMBER) ==
        SDL_PROPERTY_TYPE_NUMBER) {
        int64_t track_no = SDL_GetNumberProperty(
            props, MIX_PROP_METADATA_TOTAL_TRACKS_NUMBER, 0);
        total_track_obj = PyLong_FromInt64(track_no);
    }
    else {
        total_track_obj = Py_NewRef(Py_None);
    }

    PyObject *meta_dict =
        Py_BuildValue("{sz sz sz sz sN sN}", "title", title, "artist", artist,
                      "album", album, "copyright", copyright, "track_num",
                      track_obj, "total_tracks", total_track_obj);

    SDL_UnlockProperties(props);

    return meta_dict;
}

static PyObject *
pg_audio_obj_get_spec(PGAudioObject *self, PyObject *_null)
{
    SDL_AudioSpec spec;
    if (!MIX_GetAudioFormat(self->audio, &spec)) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return NULL;
    }

    return Py_BuildValue("iii", spec.format, spec.channels, spec.freq);
}

static int
pg_audio_obj_traverse(PyObject *op, visitproc visit, void *arg)
{
    // Visit the type
    Py_VISIT(Py_TYPE(op));
    return 0;
}

static PyGetSetDef audio_obj_getsets[] = {
    {"duration_frames", (getter)pg_audio_obj_get_duration_frames, NULL, "TODO",
     NULL},
    {"duration_ms", (getter)pg_audio_obj_get_duration_ms, NULL, "TODO", NULL},
    {"duration_infinite", (getter)pg_audio_obj_get_duration_infinite, NULL,
     "TODO", NULL},
    {NULL, NULL, NULL, NULL, NULL}};

static PyMethodDef audio_obj_methods[] = {
    {"from_sine_wave", (PyCFunction)pg_audio_obj_from_sine_wave,
     METH_CLASS | METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"from_raw", (PyCFunction)pg_audio_obj_from_raw,
     METH_CLASS | METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"ms_to_frames", (PyCFunction)pg_audio_obj_ms_to_frames,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"frames_to_ms", (PyCFunction)pg_audio_obj_frames_to_ms,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_metadata", (PyCFunction)pg_audio_obj_get_metadata, METH_NOARGS,
     "TODO"},
    {"_get_spec", (PyCFunction)pg_audio_obj_get_spec, METH_NOARGS, "TODO"},
    {NULL, NULL, 0, NULL}};

static PyType_Slot audio_slots[] = {{Py_tp_init, pg_audio_obj_init},
                                    {Py_tp_getset, audio_obj_getsets},
                                    {Py_tp_methods, audio_obj_methods},
                                    {Py_tp_dealloc, pg_audio_obj_dealloc},
                                    {Py_tp_traverse, pg_audio_obj_traverse},
                                    {0, NULL}};

static PyType_Spec audio_spec = {
    .name = "Audio",
    .basicsize = sizeof(PGAudioObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
    .slots = audio_slots};

// ***************************************************************************
// MIXER.TRACK CLASS
// ***************************************************************************

static int
pg_track_obj_init(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    PGMixerObject *mixer = NULL;
    char *keywords[] = {"mixer", NULL};

    // Input object type check handled at the Python level.
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &mixer)) {
        return -1;
    }

    self->track = MIX_CreateTrack(mixer->mixer);
    if (self->track == NULL) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }

    // Mixers own Tracks. When the Mixer is deallocated, the tracks become
    // invalid. So we need to hold a reference to prevent Mixer deallocating
    // before any of the Tracks it owns.
    Py_INCREF(mixer);
    self->mixer_obj = (PyObject *)mixer;

    return 0;
}

static void
pg_track_obj_dealloc(PGTrackObject *self)
{
    MIX_DestroyTrack(self->track);
    self->track = NULL;
    PyObject_GC_UnTrack(self);
    Py_CLEAR(self->mixer_obj);
    Py_CLEAR(self->source_obj);
    PyTypeObject *tp = Py_TYPE(self);
    freefunc free = PyType_GetSlot(tp, Py_tp_free);
    free(self);
    Py_DECREF(tp);
}

static PyObject *
pg_track_obj_get_mixer(PGTrackObject *self, PyObject *_null)
{
    Py_INCREF(self->mixer_obj);
    return self->mixer_obj;
}

static PyObject *
pg_track_obj_get_playing(PGTrackObject *self, PyObject *_null)
{
    return PyBool_FromLong(MIX_TrackPlaying(self->track));
}

static PyObject *
pg_track_obj_get_paused(PGTrackObject *self, PyObject *_null)
{
    return PyBool_FromLong(MIX_TrackPaused(self->track));
}

static PyObject *
pg_track_obj_get_loops(PGTrackObject *self, PyObject *_null)
{
    return PyLong_FromLong(MIX_GetTrackLoops(self->track));
}

static PyObject *
pg_track_obj_get_gain(PGTrackObject *self, PyObject *_null)
{
    return PyFloat_FromDouble(MIX_GetTrackGain(self->track));
}

static int
pg_track_obj_set_gain(PGTrackObject *self, PyObject *value, void *_null)
{
    double gain = PyFloat_AsDouble(value);
    if (gain == -1.0 && PyErr_Occurred()) {
        return -1;
    }
    if (!MIX_SetTrackGain(self->track, (float)gain)) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    return 0;
}

static PyObject *
pg_track_obj_get_freq_ratio(PGTrackObject *self, PyObject *_null)
{
    float ratio = MIX_GetTrackFrequencyRatio(self->track);
    if (ratio == 0.0f) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyFloat_FromDouble((double)ratio);
}

static int
pg_track_obj_set_freq_ratio(PGTrackObject *self, PyObject *value, void *_null)
{
    double ratio = PyFloat_AsDouble(value);
    if (ratio == -1.0 && PyErr_Occurred()) {
        return -1;
    }
    if (!MIX_SetTrackFrequencyRatio(self->track, (float)ratio)) {
        PyErr_SetString(pgExc_SDLError, SDL_GetError());
        return -1;
    }
    return 0;
}

static PyObject *
pg_track_obj_set_audio(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *audio_or_none = NULL;
    char *keywords[] = {"audio", NULL};
    PyObject *audio_type =
        PyObject_GetAttrString((PyObject *)self, "_audio_type");

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords,
                                     &audio_or_none)) {
        Py_DECREF(audio_type);
        return NULL;
    }

    MIX_Audio *audio = NULL;
    if (PyObject_IsInstance(audio_or_none, audio_type)) {  // audio
        audio = ((PGAudioObject *)audio_or_none)->audio;
    }
    else if (!Py_IsNone(audio_or_none)) {  // not audio, not none
        Py_DECREF(audio_type);
        return RAISE(PyExc_TypeError, "argument 1 must be Audio or None");
    }
    Py_DECREF(audio_type);

    if (!MIX_SetTrackAudio(self->track, audio)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    // We've successfully added (or removed) an audio, lets decref anything
    // we were previously holding onto.
    Py_CLEAR(self->source_obj);

    if (audio != NULL) {
        // We've successfully added an audio object, yay!
        Py_INCREF(audio_or_none);
        self->source_obj = audio_or_none;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_get_audio(PGTrackObject *self, PyObject *_null)
{
    if (MIX_GetTrackAudio(self->track) != NULL) {
        // This track object owns an audio, therefore our source object must
        // be non-null, and an audio object.
        Py_INCREF(self->source_obj);
        return self->source_obj;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_set_audiostream(PGTrackObject *self, PyObject *args,
                             PyObject *kwargs)
{
    PyObject *audiostream_or_none = NULL;
    char *keywords[] = {"audiostream", NULL};

    // This function relies on Python level type checking to remove values
    // that are not AudioStream objects or None.
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords,
                                     &audiostream_or_none)) {
        return NULL;
    }

    SDL_AudioStream *stream = NULL;
    if (audiostream_or_none != Py_None) {
        // audiostream._state to get at internals
        PGAudioStreamStateObject *as_state =
            (PGAudioStreamStateObject *)PyObject_GetAttrString(
                audiostream_or_none, "_state");
        if (as_state == NULL) {
            return RAISE(pgExc_SDLError,
                         "Unexpected internal error getting SDL audio stream "
                         "from Python object");
        }
        stream = as_state->stream;
        Py_DECREF(as_state);  // PyObject_GetAttrString gives new ref
    }

    if (!MIX_SetTrackAudioStream(self->track, stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    // We've potentially replaced the track source, so lets get
    // rid of any previous track source reference.
    Py_CLEAR(self->source_obj);

    if (stream != NULL) {
        // We've successfully added an audio object, yay!
        Py_INCREF(audiostream_or_none);
        self->source_obj = audiostream_or_none;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_get_audiostream(PGTrackObject *self, PyObject *_null)
{
    if (MIX_GetTrackAudioStream(self->track) != NULL) {
        // This track object owns an audio, therefore our source object must
        // be non-null, and an audio object.
        Py_INCREF(self->source_obj);
        return self->source_obj;
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_set_filestream(PGTrackObject *self, PyObject *args,
                            PyObject *kwargs)
{
    PyObject *file_obj = NULL;
    char *keywords[] = {"file", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords, &file_obj)) {
        return NULL;
    }

    SDL_IOStream *io = pgRWops_FromObject(file_obj, NULL);
    if (io == NULL) {
        return NULL;
    }

    if (!MIX_SetTrackIOStream(self->track, io, true)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    // We've potentially replaced the track source, so lets get
    // rid of any previous track source reference.
    Py_CLEAR(self->source_obj);

    // Hold onto you! -- is this actually needed?
    // Theoretically this is keeping Python file object (like BytesIO) alive
    // through the stream, but maybe the rwObject subsystem is smart enough
    // to do that.
    Py_INCREF(file_obj);
    self->source_obj = file_obj;

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_play(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    int64_t loops = 0;
    int64_t max_frame = -1, max_ms = -1;
    int64_t start_frame = 0, start_ms = 0;
    int64_t loop_start_frame = 0, loop_start_ms = 0;
    int64_t fadein_frames = 0, fadein_ms = 0;
    int64_t append_silence_frames = 0, append_silence_ms = 0;
    char *keywords[] = {"loops",
                        "max_frame",
                        "max_ms",
                        "start_frame",
                        "start_ms",
                        "loop_start_frame",
                        "loop_start_ms",
                        "fadein_frames",
                        "fadein_ms",
                        "append_silence_frames",
                        "append_silence_ms",
                        NULL};

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs, "|LLLLLLLLLLL", keywords, &loops, &max_frame,
            &max_ms, &start_frame, &start_ms, &loop_start_frame,
            &loop_start_ms, &fadein_frames, &fadein_ms, &append_silence_frames,
            &append_silence_ms)) {
        return NULL;
    }

    SDL_PropertiesID options = SDL_CreateProperties();
    if (options == 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    bool success = pg_populate_play_props(
        options, loops, max_frame, max_ms, start_frame, start_ms,
        loop_start_frame, loop_start_ms, fadein_frames, fadein_ms,
        append_silence_frames, append_silence_ms);

    if (!success || !MIX_PlayTrack(self->track, options)) {
        SDL_DestroyProperties(options);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    SDL_DestroyProperties(options);
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_add_tag(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    char *keywords[] = {"tag", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", keywords, &tag)) {
        return NULL;
    }

    if (!MIX_TagTrack(self->track, tag)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_remove_tag(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    char *tag;
    char *keywords[] = {"tag", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s", keywords, &tag)) {
        return NULL;
    }

    MIX_UntagTrack(self->track, tag);  // no error return!
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_set_playback_position(PGTrackObject *self, PyObject *args,
                                   PyObject *kwargs)
{
    int64_t frame_position;
    char *keywords[] = {"frames", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "L", keywords,
                                     &frame_position)) {
        return NULL;
    }

    if (!MIX_SetTrackPlaybackPosition(self->track, frame_position)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_get_playback_position(PGTrackObject *self, PyObject *null)
{
    int64_t frame_position = MIX_GetTrackPlaybackPosition(self->track);
    if (frame_position == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromInt64(frame_position);
}

static PyObject *
pg_track_obj_get_remaining_frames(PGTrackObject *self, PyObject *null)
{
    int64_t remaining = MIX_GetTrackRemaining(self->track);

    // If unknown, return None
    if (remaining == -1) {
        Py_RETURN_NONE;
    }

    return PyLong_FromInt64(remaining);
}

static PyObject *
pg_track_obj_ms_to_frames(PGTrackObject *self, PyObject *args,
                          PyObject *kwargs)
{
    int64_t ms;
    char *keywords[] = {"ms", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "L", keywords, &ms)) {
        return NULL;
    }

    int64_t frames = MIX_TrackMSToFrames(self->track, ms);
    if (frames == -1 && ms >= 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromInt64(frames);
}

static PyObject *
pg_track_obj_frames_to_ms(PGTrackObject *self, PyObject *args,
                          PyObject *kwargs)
{
    int64_t frames;
    char *keywords[] = {"frames", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "L", keywords, &frames)) {
        return NULL;
    }

    int64_t ms = MIX_TrackFramesToMS(self->track, frames);
    if (ms == -1 && frames >= 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromInt64(ms);
}

static PyObject *
pg_track_obj_stop(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    int64_t fade_out_frames = 0;
    char *keywords[] = {"fade_out_frames", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|L", keywords,
                                     &fade_out_frames)) {
        return NULL;
    }

    if (!MIX_StopTrack(self->track, fade_out_frames)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_pause(PGTrackObject *self, PyObject *null)
{
    if (!MIX_PauseTrack(self->track)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_resume(PGTrackObject *self, PyObject *null)
{
    if (!MIX_ResumeTrack(self->track)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_set_stereo(PGTrackObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *gains_or_none_obj = NULL;
    char *keywords[] = {"gains", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords,
                                     &gains_or_none_obj)) {
        return NULL;
    }

    MIX_StereoGains *gains_p = NULL;
    MIX_StereoGains gains;
    if (gains_or_none_obj != Py_None) {
        if (!pg_TwoFloatsFromObj(gains_or_none_obj, &gains.left,
                                 &gains.right)) {
            return RAISE(PyExc_TypeError,
                         "gains must be a sequence of two numbers");
        }
        gains_p = &gains;
    }

    if (!MIX_SetTrackStereo(self->track, gains_p)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_set_3d_position(PGTrackObject *self, PyObject *args,
                             PyObject *kwargs)
{
    PyObject *position_or_none_obj = NULL;
    char *keywords[] = {"position", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", keywords,
                                     &position_or_none_obj)) {
        return NULL;
    }

    MIX_Point3D *point_p = NULL;
    MIX_Point3D point;
    if (position_or_none_obj != Py_None) {
        // The error message this raises with invalid input not entirely ideal
        if (!PyArg_ParseTuple(position_or_none_obj, "fff", &point.x, &point.y,
                              &point.z)) {
            return NULL;
        }
        point_p = &point;
    }

    if (!MIX_SetTrack3DPosition(self->track, point_p)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_track_obj_get_3d_position(PGTrackObject *self, PyObject *null)
{
    MIX_Point3D point;

    if (!MIX_GetTrack3DPosition(self->track, &point)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return Py_BuildValue("fff", point.x, point.y, point.z);
}

// traverse: Visit all references from an object, including its type
static int
pg_track_obj_traverse(PyObject *op, visitproc visit, void *arg)
{
    // Visit the type
    Py_VISIT(Py_TYPE(op));

    PGTrackObject *self = (PGTrackObject *)op;
    Py_VISIT(self->mixer_obj);
    Py_VISIT(self->source_obj);
    return 0;
}

static int
pg_track_obj_clear(PyObject *op)
{
    PGTrackObject *self = (PGTrackObject *)op;
    Py_CLEAR(self->mixer_obj);
    Py_CLEAR(self->source_obj);
    return 0;
}

static PyGetSetDef track_obj_getsets[] = {
    {"mixer", (getter)pg_track_obj_get_mixer, NULL, "TODO", NULL},
    {"playing", (getter)pg_track_obj_get_playing, NULL, "TODO", NULL},
    {"paused", (getter)pg_track_obj_get_paused, NULL, "TODO", NULL},
    {"loops", (getter)pg_track_obj_get_loops, NULL, "TODO", NULL},
    {"gain", (getter)pg_track_obj_get_gain, (setter)pg_track_obj_set_gain,
     "TODO", NULL},
    {"frequency_ratio", (getter)pg_track_obj_get_freq_ratio,
     (setter)pg_track_obj_set_freq_ratio, "TODO", NULL},
    {NULL, NULL, NULL, NULL, NULL}};

static PyMethodDef track_obj_methods[] = {
    {"set_audio", (PyCFunction)pg_track_obj_set_audio,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_audio", (PyCFunction)pg_track_obj_get_audio, METH_NOARGS, "TODO"},
    {"set_audiostream", (PyCFunction)pg_track_obj_set_audiostream,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_audiostream", (PyCFunction)pg_track_obj_get_audiostream, METH_NOARGS,
     "TODO"},
    {"set_filestream", (PyCFunction)pg_track_obj_set_filestream,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"play", (PyCFunction)pg_track_obj_play, METH_VARARGS | METH_KEYWORDS,
     "TODO"},
    {"add_tag", (PyCFunction)pg_track_obj_add_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"remove_tag", (PyCFunction)pg_track_obj_remove_tag,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"set_playback_position", (PyCFunction)pg_track_obj_set_playback_position,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_playback_position", (PyCFunction)pg_track_obj_get_playback_position,
     METH_NOARGS, "TODO"},
    {"get_remaining_frames", (PyCFunction)pg_track_obj_get_remaining_frames,
     METH_NOARGS, "TODO"},
    {"ms_to_frames", (PyCFunction)pg_track_obj_ms_to_frames,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"frames_to_ms", (PyCFunction)pg_track_obj_frames_to_ms,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"stop", (PyCFunction)pg_track_obj_stop, METH_VARARGS | METH_KEYWORDS,
     "TODO"},
    {"pause", (PyCFunction)pg_track_obj_pause, METH_NOARGS, "TODO"},
    {"resume", (PyCFunction)pg_track_obj_resume, METH_NOARGS, "TODO"},
    {"set_stereo", (PyCFunction)pg_track_obj_set_stereo,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"set_3d_position", (PyCFunction)pg_track_obj_set_3d_position,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_3d_position", (PyCFunction)pg_track_obj_get_3d_position, METH_NOARGS,
     "TODO"},
    {NULL, NULL, 0, NULL}};

static PyType_Slot track_slots[] = {{Py_tp_init, pg_track_obj_init},
                                    {Py_tp_dealloc, pg_track_obj_dealloc},
                                    {Py_tp_getset, track_obj_getsets},
                                    {Py_tp_methods, track_obj_methods},
                                    {Py_tp_traverse, pg_track_obj_traverse},
                                    {Py_tp_clear, pg_track_obj_clear},
                                    {0, NULL}};

static PyType_Spec track_spec = {
    .name = "Track",
    .basicsize = sizeof(PGTrackObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE,
    .slots = track_slots};

// ***************************************************************************
// MODULE METHODS
// ***************************************************************************

static PyObject *
pg_mixer_init(PyObject *module, PyObject *_null)
{
    _mixer_state *state = GET_STATE(module);
    if (!state->mixer_initialized) {
        if (!MIX_Init()) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        state->mixer_initialized = true;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_quit(PyObject *module, PyObject *_null)
{
    _mixer_state *state = GET_STATE(module);
    if (state->mixer_initialized) {
        MIX_Quit();
        state->mixer_initialized = false;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_mixer_get_sdl_mixer_version(PyObject *self, PyObject *args,
                               PyObject *kwargs)
{
    int linked = 1; /* Default is linked version. */
    int version = SDL_MIXER_VERSION;

    char *keywords[] = {"linked", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|p", keywords, &linked)) {
        return NULL; /* Exception already set. */
    }

    if (linked) {
        version = MIX_Version();
    }

    return Py_BuildValue("iii", PG_FIND_VNUM_MAJOR(version),
                         PG_FIND_VNUM_MINOR(version),
                         PG_FIND_VNUM_MICRO(version));
}

static PyObject *
pg_mixer_get_decoders(PyObject *module, PyObject *_null)
{
    _mixer_state *state = GET_STATE(module);
    if (!state->mixer_initialized) {
        return RAISE(pgExc_SDLError, "mixer not initialized");
    }

    int num_decoders = MIX_GetNumAudioDecoders();
    PyObject *decoders = PyList_New(num_decoders);
    if (decoders == NULL) {
        return NULL;  // error already set
    }

    for (int i = 0; i < num_decoders; i++) {
        PyObject *decoder = PyUnicode_FromString(MIX_GetAudioDecoder(i));
        if (decoder == NULL || PyList_SetItem(decoders, i, decoder)) {
            Py_DECREF(decoders);
            return NULL;  // error already set
        }
    }

    return decoders;
}

static PyMethodDef _mixer_methods[] = {
    {"init", (PyCFunction)pg_mixer_init, METH_NOARGS, "DOC_MIXER_INIT"},
    {"quit", (PyCFunction)pg_mixer_quit, METH_NOARGS, "DOC_MIXER_QUIT"},
    {"get_sdl_mixer_version", (PyCFunction)pg_mixer_get_sdl_mixer_version,
     METH_VARARGS | METH_KEYWORDS, "TODO"},
    {"get_decoders", (PyCFunction)pg_mixer_get_decoders, METH_NOARGS, "TODO"},
    {NULL, NULL, 0, NULL}};

// ***************************************************************************
// MODULE SETUP
// ***************************************************************************

int
pg_audio_exec(PyObject *module)
{
    /*imported needed apis*/
    import_pygame_base();
    if (PyErr_Occurred()) {
        return -1;
    }
    import_pygame_rwobject();
    if (PyErr_Occurred()) {
        return -1;
    }

    _mixer_state *state = GET_STATE(module);
    state->mixer_initialized = false;

    // Create types
    state->mixer_obj_type =
        PyType_FromModuleAndSpec(module, &mixer_spec, NULL);
    state->audio_obj_type =
        PyType_FromModuleAndSpec(module, &audio_spec, NULL);
    state->track_obj_type =
        PyType_FromModuleAndSpec(module, &track_spec, NULL);

    // If any NULLs, error
    if (state->mixer_obj_type == NULL || state->audio_obj_type == NULL ||
        state->track_obj_type == NULL) {
        return -1;
    }

    // Add types to module
    if (PyModule_AddType(module, (PyTypeObject *)state->mixer_obj_type) < 0 ||
        PyModule_AddType(module, (PyTypeObject *)state->audio_obj_type) < 0 ||
        PyModule_AddType(module, (PyTypeObject *)state->track_obj_type) < 0) {
        return -1;
    }

    // Add references between types where necessary.
    if (PyObject_SetAttrString(state->mixer_obj_type, "_audio_type",
                               state->audio_obj_type) < 0 ||
        PyObject_SetAttrString(state->track_obj_type, "_audio_type",
                               state->audio_obj_type) < 0 ||
        PyObject_SetAttrString(state->audio_obj_type, "_mixer_type",
                               state->mixer_obj_type) < 0) {
        return -1;
    }

    return 0;
}

static int
pg_mixer_traverse(PyObject *module, visitproc visit, void *arg)
{
    _mixer_state *state = GET_STATE(module);
    Py_VISIT(state->mixer_obj_type);
    Py_VISIT(state->audio_obj_type);
    Py_VISIT(state->track_obj_type);
    return 0;
}

static int
pg_mixer_clear(PyObject *module)
{
    _mixer_state *state = GET_STATE(module);
    Py_CLEAR(state->mixer_obj_type);
    Py_CLEAR(state->audio_obj_type);
    Py_CLEAR(state->track_obj_type);
    return 0;
}

static void
pg_mixer_free(void *module)
{
    // allow pg_audio_exec to omit calling pg_audio_clear on error
    (void)pg_mixer_clear((PyObject *)module);
}

MODINIT_DEFINE(_sdl3_mixer_c)
{
    static PyModuleDef_Slot mixer_slots[] = {
        {Py_mod_exec, &pg_audio_exec},
#if PY_VERSION_HEX >= 0x030c0000
        {Py_mod_multiple_interpreters,
         Py_MOD_MULTIPLE_INTERPRETERS_NOT_SUPPORTED},  // TODO: see if this can
                                                       // be supported later
#endif
#if PY_VERSION_HEX >= 0x030d0000
        {Py_mod_gil, Py_MOD_GIL_USED},  // TODO: support this later
#endif
        {0, NULL}};
    static struct PyModuleDef _module = {PyModuleDef_HEAD_INIT,
                                         .m_name = "_sdl3_mixer_c",
                                         .m_doc = NULL,
                                         .m_size = sizeof(_mixer_state),
                                         .m_methods = _mixer_methods,
                                         .m_slots = mixer_slots,
                                         .m_traverse = pg_mixer_traverse,
                                         .m_clear = pg_mixer_clear,
                                         .m_free = pg_mixer_free};

    return PyModuleDef_Init(&_module);
}
