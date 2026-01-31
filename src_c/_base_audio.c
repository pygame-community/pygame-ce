#include "pygame.h"
#include "pgcompat.h"
#include "structmember.h"

// Useful heap type example @
// https://github.com/python/cpython/blob/main/Modules/xxlimited.c

// ***************************************************************************
// OVERALL DEFINITIONS
// ***************************************************************************

typedef struct {
    bool audio_initialized;
    PyObject *audio_device_state_type;
    PyObject *audio_stream_state_type;
} audio_state;

#define GET_STATE(x) (audio_state *)PyModule_GetState(x)

typedef struct {
    PyObject_HEAD SDL_AudioDeviceID devid;
} PGAudioDeviceStateObject;

typedef struct {
    PyObject_HEAD SDL_AudioStream *stream;
} PGAudioStreamStateObject;

#define AUDIO_INIT_CHECK(module)                               \
    if (!(GET_STATE(module))->audio_initialized) {             \
        return RAISE(pgExc_SDLError, "audio not initialized"); \
    }

// ***************************************************************************
// AUDIO.AUDIODEVICE CLASS
// ***************************************************************************

// The documentation says heap types need to support GC, so we're implementing
// traverse even though the object has no explicit references.
static int
adevice_state_traverse(PyObject *op, visitproc visit, void *arg)
{
    // Visit the type
    Py_VISIT(Py_TYPE(op));
    return 0;
}

static void
adevice_state_dealloc(PGAudioDeviceStateObject *self)
{
    // Only close devices that have been opened.
    // (logical devices, not physical)
    if (!SDL_IsAudioDevicePhysical(self->devid)) {
        SDL_CloseAudioDevice(self->devid);
    }
    PyObject_GC_UnTrack(self);
    PyTypeObject *tp = Py_TYPE(self);
    freefunc free = PyType_GetSlot(tp, Py_tp_free);
    free(self);
    Py_DECREF(tp);
}

static PyMemberDef adevice_state_members[] = {
    {"id", Py_T_UINT, offsetof(PGAudioDeviceStateObject, devid), Py_READONLY,
     NULL},
    {NULL} /* Sentinel */
};

static PyType_Slot adevice_state_slots[] = {
    {Py_tp_members, adevice_state_members},
    {Py_tp_traverse, adevice_state_traverse},
    {Py_tp_dealloc, adevice_state_dealloc},
    {0, NULL}};

static PyType_Spec adevice_state_spec = {
    .name = "AudioDeviceState",
    .basicsize = sizeof(PGAudioDeviceStateObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .slots = adevice_state_slots};

static PyObject *
pg_audio_is_audio_device_playback(PyObject *module, PyObject *arg)
{
    // SDL_IsAudioDevicePlayback
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    if (SDL_IsAudioDevicePlayback(devid)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject *
pg_audio_get_audio_device_name(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioDeviceName
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    const char *name = SDL_GetAudioDeviceName(devid);
    if (name == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }
    return PyUnicode_FromString(name);
}

static PyObject *
pg_audio_get_audio_device_channel_map(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioDeviceChannelMap
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;

    int count;
    int *channel_map = SDL_GetAudioDeviceChannelMap(devid, &count);
    if (channel_map == NULL) {
        Py_RETURN_NONE;
    }

    PyObject *channel_map_list = PyList_New(count);
    if (channel_map_list == NULL) {
        SDL_free(channel_map);
        return NULL;
    }
    PyObject *item;
    for (int i = 0; i < count; i++) {
        item = PyLong_FromLong(channel_map[i]);
        if (item == NULL) {
            SDL_free(channel_map);
            Py_DECREF(channel_map_list);
            return NULL;
        }
        if (PyList_SetItem(channel_map_list, i, item) < 0) {
            SDL_free(channel_map);
            Py_DECREF(item);
            Py_DECREF(channel_map_list);
            return NULL;
        }
    }

    SDL_free(channel_map);
    return channel_map_list;
}

static PyObject *
pg_audio_pause_audio_device(PyObject *module, PyObject *arg)
{
    // SDL_PauseAudioDevice
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    if (!SDL_PauseAudioDevice(devid)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_resume_audio_device(PyObject *module, PyObject *arg)
{
    // SDL_ResumeAudioDevice
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    if (!SDL_ResumeAudioDevice(devid)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_audio_device_paused(PyObject *module, PyObject *arg)
{
    // SDL_AudioDevicePaused
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    if (SDL_AudioDevicePaused(devid)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject *
pg_audio_get_audio_device_gain(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioDeviceGain
    // arg: PGAudioDeviceStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)arg)->devid;
    float gain = SDL_GetAudioDeviceGain(devid);
    if (gain == -1.0f) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyFloat_FromDouble((double)gain);
}

static PyObject *
pg_audio_set_audio_device_gain(PyObject *module, PyObject *const *args,
                               Py_ssize_t nargs)
{
    // SDL_SetAudioDeviceGain
    // arg0: PGAudioDeviceStateObject, gain: float

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)args[0])->devid;
    double gain = PyFloat_AsDouble(args[1]);
    if (gain == -1.0 && PyErr_Occurred()) {
        return NULL;
    }

    if (!SDL_SetAudioDeviceGain(devid, (float)gain)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_open_audio_device(PyObject *module, PyObject *const *args,
                           Py_ssize_t nargs)
{
    // SDL_OpenAudioDevice
    // arg0: PGAudioDeviceStateObject, format: int | unset, channels: int |
    // unset, frequency: int | unset

    audio_state *state = GET_STATE(module);
    PyTypeObject *adevice_state_type =
        (PyTypeObject *)state->audio_device_state_type;

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)args[0])->devid;

    SDL_AudioSpec *spec_p = NULL;
    SDL_AudioSpec spec;
    if (nargs != 1) {
        spec.format = PyLong_AsInt(args[1]);
        spec.channels = PyLong_AsInt(args[2]);
        spec.freq = PyLong_AsInt(args[3]);

        // Check that they all succeeded
        if (spec.format == -1 || spec.channels == -1 || spec.freq == -1) {
            if (PyErr_Occurred()) {
                return NULL;
            }
        }

        spec_p = &spec;
    }

    SDL_AudioDeviceID logical_id = SDL_OpenAudioDevice(devid, spec_p);
    if (logical_id == 0) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PGAudioDeviceStateObject *device =
        (PGAudioDeviceStateObject *)adevice_state_type->tp_alloc(
            adevice_state_type, 0);
    if (device == NULL) {
        SDL_CloseAudioDevice(logical_id);
        return NULL;
    }
    device->devid = logical_id;

    return (PyObject *)device;
}

// ***************************************************************************
// AUDIO.AUDIOSTREAM CLASS
// ***************************************************************************

// The documentation says heap types need to support GC, so we're implementing
// traverse even though the object has no explicit references.
static int
astream_state_traverse(PyObject *op, visitproc visit, void *arg)
{
    // Visit the type
    Py_VISIT(Py_TYPE(op));
    return 0;
}

static void
astream_state_dealloc(PGAudioStreamStateObject *self)
{
    SDL_DestroyAudioStream(self->stream);
    PyObject_GC_UnTrack(self);
    PyTypeObject *tp = Py_TYPE(self);
    freefunc free = PyType_GetSlot(tp, Py_tp_free);
    free(self);
    Py_DECREF(tp);
}

static PyType_Slot astream_state_slots[] = {
    {Py_tp_traverse, astream_state_traverse},
    {Py_tp_dealloc, astream_state_dealloc},
    {0, NULL}};

static PyType_Spec astream_state_spec = {
    .name = "AudioStreamState",
    .basicsize = sizeof(PGAudioStreamStateObject),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .slots = astream_state_slots};

static PyObject *
pg_audio_create_audio_stream(PyObject *module, PyObject *const *args,
                             Py_ssize_t nargs)
{
    // SDL_CreateAudioStream
    //  src_format: int, src_channels: int, src_frequency: int,
    //  dst_format: int, dst_channels: int, dst_frequency: int

    audio_state *state = GET_STATE(module);
    PyTypeObject *astream_state_type =
        (PyTypeObject *)state->audio_stream_state_type;

    SDL_AudioSpec src, dst;

    src.format = PyLong_AsInt(args[0]);
    src.channels = PyLong_AsInt(args[1]);
    src.freq = PyLong_AsInt(args[2]);
    dst.format = PyLong_AsInt(args[3]);
    dst.channels = PyLong_AsInt(args[4]);
    dst.freq = PyLong_AsInt(args[5]);

    // Check that they all succeeded
    if (src.format == -1 || src.channels == -1 || src.freq == -1 ||
        dst.format == -1 || dst.channels == -1 || dst.freq == -1) {
        if (PyErr_Occurred()) {
            return NULL;
        }
    }

    SDL_AudioStream *stream = SDL_CreateAudioStream(&src, &dst);
    if (stream == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PGAudioStreamStateObject *stream_state =
        (PGAudioStreamStateObject *)astream_state_type->tp_alloc(
            astream_state_type, 0);

    if (stream_state == NULL) {
        SDL_DestroyAudioStream(stream);
        return NULL;
    }
    stream_state->stream = stream;

    return (PyObject *)stream_state;
}

static PyObject *
pg_audio_bind_audio_stream(PyObject *module, PyObject *const *args,
                           Py_ssize_t nargs)
{
    // SDL_BindAudioStream
    // arg0: PGAudioDeviceStateObject, arg1: PGAudioStreamStateObject

    SDL_AudioDeviceID devid = ((PGAudioDeviceStateObject *)args[0])->devid;
    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[1])->stream;

    if (!SDL_BindAudioStream(devid, stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_unbind_audio_stream(PyObject *module, PyObject *arg)
{
    // SDL_UnbindAudioStream
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    SDL_UnbindAudioStream(stream);
    Py_RETURN_NONE;
}

static PyObject *
pg_audio_clear_audio_stream(PyObject *module, PyObject *arg)
{
    // SDL_ClearAudioStream
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;

    if (!SDL_ClearAudioStream(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_flush_audio_stream(PyObject *module, PyObject *arg)
{
    // SDL_FlushAudioStream
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;

    if (!SDL_FlushAudioStream(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_get_audio_stream_available(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioStreamAvailable
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;

    int available = SDL_GetAudioStreamAvailable(stream);
    if (available == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromLong(available);
}

static PyObject *
pg_audio_get_audio_stream_queued(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioStreamQueued
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;

    int queued = SDL_GetAudioStreamQueued(stream);
    if (queued == -1) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyLong_FromLong(queued);
}

static PyObject *
pg_audio_get_audio_stream_data(PyObject *module, PyObject *const *args,
                               Py_ssize_t nargs)
{
    // SDL_GetAudioStreamData
    // stream_state: PGAudioStreamStateObject, size: int

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[0])->stream;

    int size = PyLong_AsInt(args[1]);
    if (size == -1 && PyErr_Occurred()) {
        return NULL;
    }

    if (size < 0) {
        return RAISE(PyExc_ValueError, "size must be >= 0");
    }

    void *buf = malloc(size);
    if (buf == NULL) {
        return PyErr_NoMemory();
    }

    int bytes_read = SDL_GetAudioStreamData(stream, buf, size);

    if (bytes_read == -1) {
        free(buf);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PyObject *bytes = PyBytes_FromStringAndSize(buf, bytes_read);
    free(buf);
    if (bytes == NULL) {
        return NULL;
    }

    return bytes;
}

static PyObject *
pg_audio_put_audio_stream_data(PyObject *module, PyObject *const *args,
                               Py_ssize_t nargs)
{
    // SDL_PutAudioStreamData
    // stream_state: PGAudioStreamStateObject, data: Buffer

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[0])->stream;

    PyObject *bytes = PyBytes_FromObject(args[1]);
    if (bytes == NULL) {
        return NULL;
    }

    void *buf;
    Py_ssize_t len;

    if (PyBytes_AsStringAndSize(bytes, (char **)&buf, &len) != 0) {
        Py_DECREF(bytes);
        return NULL;
    }

    if (len > INT_MAX) {
        Py_DECREF(bytes);
        return RAISE(pgExc_SDLError, "audio buffer too large");
    }

    if (!SDL_PutAudioStreamData(stream, buf, (int)len)) {
        Py_DECREF(bytes);
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_DECREF(bytes);
    Py_RETURN_NONE;
}

static PyObject *
pg_audio_pause_audio_stream_device(PyObject *module, PyObject *arg)
{
    // SDL_PauseAudioStreamDevice
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    if (!SDL_PauseAudioStreamDevice(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_resume_audio_stream_device(PyObject *module, PyObject *arg)
{
    // SDL_ResumeAudioStreamDevice
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    if (!SDL_ResumeAudioStreamDevice(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_audio_stream_device_paused(PyObject *module, PyObject *arg)
{
    // SDL_AudioStreamDevicePaused
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    if (SDL_AudioStreamDevicePaused(stream)) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}

static PyObject *
pg_audio_get_audio_stream_format(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioStreamFormat
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    SDL_AudioSpec src_spec, dst_spec;

    if (!SDL_GetAudioStreamFormat(stream, &src_spec, &dst_spec)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return Py_BuildValue("iiiiii", src_spec.format, src_spec.channels,
                         src_spec.freq, dst_spec.format, dst_spec.channels,
                         dst_spec.freq);
}

static PyObject *
pg_audio_set_audio_stream_format(PyObject *module, PyObject *const *args,
                                 Py_ssize_t nargs)
{
    // SDL_SetAudioStreamFormat
    // arg0: PGAudioStreamStateObject,
    // src format: (format int, channels int, frequency int) | None
    // dst format: (format int, channels int, frequency int) | None

    SDL_AudioSpec src, dst;
    SDL_AudioSpec *src_p = NULL;
    SDL_AudioSpec *dst_p = NULL;

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[0])->stream;

    if (!Py_IsNone(args[1])) {
        src.format = PyLong_AsInt(PyTuple_GetItem(args[1], 0));
        src.channels = PyLong_AsInt(PyTuple_GetItem(args[1], 1));
        src.freq = PyLong_AsInt(PyTuple_GetItem(args[1], 2));
        src_p = &src;
        if ((src.format == -1 || src.channels == -1 || src.freq == -1) &&
            PyErr_Occurred()) {
            return NULL;
        }
    }
    if (!Py_IsNone(args[2])) {
        dst.format = PyLong_AsInt(PyTuple_GetItem(args[2], 0));
        dst.channels = PyLong_AsInt(PyTuple_GetItem(args[2], 1));
        dst.freq = PyLong_AsInt(PyTuple_GetItem(args[2], 2));
        dst_p = &dst;
        if ((dst.format == -1 || dst.channels == -1 || dst.freq == -1) &&
            PyErr_Occurred()) {
            return NULL;
        }
    }

    if (!SDL_SetAudioStreamFormat(stream, src_p, dst_p)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_get_audio_stream_gain(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioStreamGain
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    float gain = SDL_GetAudioStreamGain(stream);

    if (gain == -1.0f) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyFloat_FromDouble((double)gain);
}

static PyObject *
pg_audio_set_audio_stream_gain(PyObject *module, PyObject *const *args,
                               Py_ssize_t nargs)
{
    // SDL_SetAudioStreamGain
    // arg0: PGAudioStreamStateObject, gain: float

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[0])->stream;

    double gain = PyFloat_AsDouble(args[1]);
    if (gain == -1.0 && PyErr_Occurred()) {
        return NULL;
    }

    if (!SDL_SetAudioStreamGain(stream, (float)gain)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_get_audio_stream_frequency_ratio(PyObject *module, PyObject *arg)
{
    // SDL_GetAudioStreamFrequencyRatio
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    float frequency_ratio = SDL_GetAudioStreamFrequencyRatio(stream);

    if (frequency_ratio == 0.0f) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    return PyFloat_FromDouble((double)frequency_ratio);
}

static PyObject *
pg_audio_set_audio_stream_frequency_ratio(PyObject *module,
                                          PyObject *const *args,
                                          Py_ssize_t nargs)
{
    // SDL_SetAudioStreamFrequencyRatio
    // arg0: PGAudioStreamStateObject, frequency_ratio: float

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)args[0])->stream;

    double frequency_ratio = PyFloat_AsDouble(args[1]);
    if (frequency_ratio == -1.0 && PyErr_Occurred()) {
        return NULL;
    }

    if (!SDL_SetAudioStreamFrequencyRatio(stream, (float)frequency_ratio)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_lock_audio_stream(PyObject *module, PyObject *arg)
{
    // SDL_LockAudioStream
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    if (!SDL_LockAudioStream(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

static PyObject *
pg_audio_unlock_audio_stream(PyObject *module, PyObject *arg)
{
    // SDL_UnlockAudioStream
    // arg: PGAudioStreamStateObject

    SDL_AudioStream *stream = ((PGAudioStreamStateObject *)arg)->stream;
    if (!SDL_UnlockAudioStream(stream)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    Py_RETURN_NONE;
}

// ***************************************************************************
// MODULE METHODS
// ***************************************************************************

static PyObject *
pg_audio_init(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    if (!state->audio_initialized) {
        if (!SDL_InitSubSystem(SDL_INIT_AUDIO)) {
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        state->audio_initialized = true;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_audio_quit(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    if (state->audio_initialized) {
        SDL_QuitSubSystem(SDL_INIT_AUDIO);
        state->audio_initialized = false;
    }
    Py_RETURN_NONE;
}

static PyObject *
pg_audio_get_init(PyObject *module, PyObject *_null)
{
    // Returns whether the subsystem is initialized, not
    // whether _base_audio.init was called!
    // EX: mixer would initialize SDL audio subsystem too.

    if (!SDL_WasInit(SDL_INIT_AUDIO)) {
        Py_RETURN_FALSE;
    }
    Py_RETURN_TRUE;
}

static PyObject *
pg_audio_get_current_driver(PyObject *module, PyObject *_null)
{
    AUDIO_INIT_CHECK(module);

    const char *driver = SDL_GetCurrentAudioDriver();
    if (driver != NULL) {
        return PyUnicode_FromString(driver);
    }
    return RAISE(pgExc_SDLError, SDL_GetError());
}

static PyObject *
pg_audio_get_drivers(PyObject *module, PyObject *_null)
{
    int num_drivers = SDL_GetNumAudioDrivers();

    PyObject *driver_list = PyList_New(num_drivers);
    if (driver_list == NULL) {
        return NULL;
    }
    PyObject *item;
    const char *driver;
    for (int i = 0; i < num_drivers; i++) {
        driver = SDL_GetAudioDriver(i);
        if (driver == NULL) {
            Py_DECREF(driver_list);
            return RAISE(pgExc_SDLError, SDL_GetError());
        }
        item = PyUnicode_FromString(driver);
        if (item == NULL) {
            Py_DECREF(driver_list);
            return NULL;
        }
        if (PyList_SetItem(driver_list, i, item) < 0) {
            Py_DECREF(item);
            Py_DECREF(driver_list);
            return NULL;
        }
    }

    return driver_list;
}

// Returns Python list of DeviceState objects, or NULL with error set.
static PyObject *
_pg_audio_device_array_to_pylist(SDL_AudioDeviceID *devices, int num_devices,
                                 PyTypeObject *adevice_state_type)
{
    if (devices == NULL) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PyObject *device_list = PyList_New(num_devices);
    if (device_list == NULL) {
        return NULL;
    }
    PGAudioDeviceStateObject *device;
    for (int i = 0; i < num_devices; i++) {
        device = (PGAudioDeviceStateObject *)adevice_state_type->tp_alloc(
            adevice_state_type, 0);
        if (device == NULL) {
            Py_DECREF(device_list);
            return NULL;
        }
        device->devid = devices[i];
        if (PyList_SetItem(device_list, i, (PyObject *)device) < 0) {
            Py_DECREF(device);
            Py_DECREF(device_list);
            return NULL;
        }
    }

    return device_list;
}

static PyObject *
pg_audio_get_playback_device_states(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    PyTypeObject *adevice_state_type =
        (PyTypeObject *)state->audio_device_state_type;

    int num_devices;
    SDL_AudioDeviceID *devices = SDL_GetAudioPlaybackDevices(&num_devices);

    PyObject *dev_list = _pg_audio_device_array_to_pylist(devices, num_devices,
                                                          adevice_state_type);
    SDL_free(devices);
    return dev_list;  // Fine if NULL, error already set.
}

static PyObject *
pg_audio_get_recording_device_states(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    PyTypeObject *adevice_state_type =
        (PyTypeObject *)state->audio_device_state_type;

    int num_devices;
    SDL_AudioDeviceID *devices = SDL_GetAudioRecordingDevices(&num_devices);

    PyObject *dev_list = _pg_audio_device_array_to_pylist(devices, num_devices,
                                                          adevice_state_type);
    SDL_free(devices);
    return dev_list;  // Fine if NULL, error already set.
}

static PyObject *
pg_audio_load_wav(PyObject *module, PyObject *arg)
{
    // SDL_LoadWAV_IO
    // arg: FileLike

    SDL_IOStream *src = pgRWops_FromObject(arg, NULL);
    if (src == NULL) {
        return NULL;
    }

    SDL_AudioSpec spec;
    Uint8 *audio_buf;
    Uint32 audio_len;

    if (!SDL_LoadWAV_IO(src, true, &spec, &audio_buf, &audio_len)) {
        return RAISE(pgExc_SDLError, SDL_GetError());
    }

    PyObject *bytes = PyBytes_FromStringAndSize((char *)audio_buf, audio_len);
    SDL_free(audio_buf);
    if (bytes == NULL) {
        return NULL;
    }

    return Py_BuildValue("Niii", bytes, spec.format, spec.channels, spec.freq);
}

static PyObject *
pg_audio_get_default_playback_device_state(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    PyTypeObject *adevice_state_type =
        (PyTypeObject *)state->audio_device_state_type;

    PGAudioDeviceStateObject *device =
        (PGAudioDeviceStateObject *)adevice_state_type->tp_alloc(
            adevice_state_type, 0);
    if (device == NULL) {
        return NULL;
    }
    device->devid = SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK;

    return (PyObject *)device;
}

static PyObject *
pg_audio_get_default_recording_device_state(PyObject *module, PyObject *_null)
{
    audio_state *state = GET_STATE(module);
    PyTypeObject *adevice_state_type =
        (PyTypeObject *)state->audio_device_state_type;

    PGAudioDeviceStateObject *device =
        (PGAudioDeviceStateObject *)adevice_state_type->tp_alloc(
            adevice_state_type, 0);
    if (device == NULL) {
        return NULL;
    }
    device->devid = SDL_AUDIO_DEVICE_DEFAULT_RECORDING;

    return (PyObject *)device;
}

static PyObject *
pg_audio_get_silence_value_for_format(PyObject *module, PyObject *arg)
{
    // SDL_GetSilenceValueForFormat
    // format: int

    int format_num = PyLong_AsInt(arg);
    if (format_num == -1 && PyErr_Occurred()) {
        return NULL;
    }

    int silence_value =
        SDL_GetSilenceValueForFormat((SDL_AudioFormat)format_num);

    return PyBytes_FromFormat("%c", silence_value);
}

static PyMethodDef audio_methods[] = {
    {"init", (PyCFunction)pg_audio_init, METH_NOARGS, NULL},
    {"quit", (PyCFunction)pg_audio_quit, METH_NOARGS, NULL},
    {"get_init", (PyCFunction)pg_audio_get_init, METH_NOARGS, NULL},
    {"get_current_driver", (PyCFunction)pg_audio_get_current_driver,
     METH_NOARGS, NULL},
    {"get_drivers", (PyCFunction)pg_audio_get_drivers, METH_NOARGS, NULL},
    {"get_playback_device_states",
     (PyCFunction)pg_audio_get_playback_device_states, METH_NOARGS, NULL},
    {"get_recording_device_states",
     (PyCFunction)pg_audio_get_recording_device_states, METH_NOARGS, NULL},
    {"load_wav", (PyCFunction)pg_audio_load_wav, METH_O, NULL},
    {"get_default_playback_device_state",
     (PyCFunction)pg_audio_get_default_playback_device_state, METH_NOARGS,
     NULL},
    {"get_default_recording_device_state",
     (PyCFunction)pg_audio_get_default_recording_device_state, METH_NOARGS,
     NULL},

    // format utility (the one)
    {"get_silence_value_for_format",
     (PyCFunction)pg_audio_get_silence_value_for_format, METH_O, NULL},

    // AudioDevice utilities
    {"is_audio_device_playback",
     (PyCFunction)pg_audio_is_audio_device_playback, METH_O, NULL},
    {"get_audio_device_name", (PyCFunction)pg_audio_get_audio_device_name,
     METH_O, NULL},
    {"get_audio_device_channel_map",
     (PyCFunction)pg_audio_get_audio_device_channel_map, METH_O, NULL},
    {"open_audio_device", (PyCFunction)pg_audio_open_audio_device,
     METH_FASTCALL, NULL},
    {"pause_audio_device", (PyCFunction)pg_audio_pause_audio_device, METH_O,
     NULL},
    {"resume_audio_device", (PyCFunction)pg_audio_resume_audio_device, METH_O,
     NULL},
    {"audio_device_paused", (PyCFunction)pg_audio_audio_device_paused, METH_O,
     NULL},
    {"get_audio_device_gain", (PyCFunction)pg_audio_get_audio_device_gain,
     METH_O, NULL},
    {"set_audio_device_gain", (PyCFunction)pg_audio_set_audio_device_gain,
     METH_FASTCALL, NULL},

    // AudioStream utilities
    {"create_audio_stream", (PyCFunction)pg_audio_create_audio_stream,
     METH_FASTCALL, NULL},
    {"bind_audio_stream", (PyCFunction)pg_audio_bind_audio_stream,
     METH_FASTCALL, NULL},
    {"unbind_audio_stream", (PyCFunction)pg_audio_unbind_audio_stream, METH_O,
     NULL},
    {"clear_audio_stream", (PyCFunction)pg_audio_clear_audio_stream, METH_O,
     NULL},
    {"flush_audio_stream", (PyCFunction)pg_audio_flush_audio_stream, METH_O,
     NULL},
    {"get_audio_stream_available",
     (PyCFunction)pg_audio_get_audio_stream_available, METH_O, NULL},
    {"get_audio_stream_queued", (PyCFunction)pg_audio_get_audio_stream_queued,
     METH_O, NULL},
    {"get_audio_stream_data", (PyCFunction)pg_audio_get_audio_stream_data,
     METH_FASTCALL, NULL},
    {"put_audio_stream_data", (PyCFunction)pg_audio_put_audio_stream_data,
     METH_FASTCALL, NULL},
    {"pause_audio_stream_device",
     (PyCFunction)pg_audio_pause_audio_stream_device, METH_O, NULL},
    {"resume_audio_stream_device",
     (PyCFunction)pg_audio_resume_audio_stream_device, METH_O, NULL},
    {"audio_stream_device_paused",
     (PyCFunction)pg_audio_audio_stream_device_paused, METH_O, NULL},
    {"get_audio_stream_format", (PyCFunction)pg_audio_get_audio_stream_format,
     METH_O, NULL},
    {"set_audio_stream_format", (PyCFunction)pg_audio_set_audio_stream_format,
     METH_FASTCALL, NULL},
    {"get_audio_stream_gain", (PyCFunction)pg_audio_get_audio_stream_gain,
     METH_O, NULL},
    {"set_audio_stream_gain", (PyCFunction)pg_audio_set_audio_stream_gain,
     METH_FASTCALL, NULL},
    {"get_audio_stream_frequency_ratio",
     (PyCFunction)pg_audio_get_audio_stream_frequency_ratio, METH_O, NULL},
    {"set_audio_stream_frequency_ratio",
     (PyCFunction)pg_audio_set_audio_stream_frequency_ratio, METH_FASTCALL,
     NULL},
    {"lock_audio_stream", (PyCFunction)pg_audio_lock_audio_stream, METH_O,
     NULL},
    {"unlock_audio_stream", (PyCFunction)pg_audio_unlock_audio_stream, METH_O,
     NULL},

    {NULL, NULL, 0, NULL}};

// ***************************************************************************
// MODULE SETUP
// ***************************************************************************

static int
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

    audio_state *state = GET_STATE(module);
    state->audio_initialized = false;

    state->audio_device_state_type =
        PyType_FromModuleAndSpec(module, &adevice_state_spec, NULL);
    if (state->audio_device_state_type == NULL) {
        return -1;
    }
    if (PyModule_AddType(module,
                         (PyTypeObject *)state->audio_device_state_type) < 0) {
        return -1;
    }

    state->audio_stream_state_type =
        PyType_FromModuleAndSpec(module, &astream_state_spec, NULL);
    if (state->audio_stream_state_type == NULL) {
        return -1;
    }
    if (PyModule_AddType(module,
                         (PyTypeObject *)state->audio_stream_state_type) < 0) {
        return -1;
    }

    return 0;
}

static int
pg_audio_traverse(PyObject *module, visitproc visit, void *arg)
{
    audio_state *state = GET_STATE(module);
    Py_VISIT(state->audio_device_state_type);
    Py_VISIT(state->audio_stream_state_type);
    return 0;
}

static int
pg_audio_clear(PyObject *module)
{
    audio_state *state = GET_STATE(module);
    Py_CLEAR(state->audio_device_state_type);
    Py_CLEAR(state->audio_stream_state_type);
    return 0;
}

static void
pg_audio_free(void *module)
{
    // Maybe not necessary, but lets tell SDL that we no longer depend
    // on the audio subsystem when the module is being deallocated.
    audio_state *state = GET_STATE((PyObject *)module);
    if (state != NULL) {
        if (state->audio_initialized) {
            SDL_QuitSubSystem(SDL_INIT_AUDIO);
            state->audio_initialized = false;
        }
    }

    // allow pg_audio_exec to omit calling pg_audio_clear on error
    (void)pg_audio_clear((PyObject *)module);
}

MODINIT_DEFINE(_base_audio)
{
    static PyModuleDef_Slot audio_slots[] = {
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
    static struct PyModuleDef _module = {
        PyModuleDef_HEAD_INIT, "_base_audio",  NULL,
        sizeof(audio_state),   audio_methods,  audio_slots,
        pg_audio_traverse,     pg_audio_clear, pg_audio_free};

    return PyModuleDef_Init(&_module);
}
