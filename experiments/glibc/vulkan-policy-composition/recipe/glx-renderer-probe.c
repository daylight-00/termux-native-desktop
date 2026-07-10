#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct _XDisplay Display;
typedef unsigned long XID;
typedef XID GLXDrawable;
typedef XID GLXPbuffer;
typedef struct __GLXFBConfigRec *GLXFBConfig;
typedef struct __GLXcontextRec *GLXContext;

enum {
    GLX_DRAWABLE_TYPE = 0x8010,
    GLX_RENDER_TYPE = 0x8011,
    GLX_PBUFFER_BIT = 0x00000004,
    GLX_RGBA_BIT = 0x00000001,
    GLX_RGBA_TYPE = 0x8014,
    GLX_PBUFFER_HEIGHT = 0x8040,
    GLX_PBUFFER_WIDTH = 0x8041,
    GL_VENDOR = 0x1F00,
    GL_RENDERER = 0x1F01,
    GL_VERSION = 0x1F02
};

typedef Display *(*PFN_XOpenDisplay)(const char *);
typedef int (*PFN_XDefaultScreen)(Display *);
typedef int (*PFN_XCloseDisplay)(Display *);
typedef int (*PFN_XFree)(void *);

typedef int (*PFN_glXQueryVersion)(Display *, int *, int *);
typedef GLXFBConfig *(*PFN_glXChooseFBConfig)(Display *, int, const int *, int *);
typedef GLXContext (*PFN_glXCreateNewContext)(Display *, GLXFBConfig, int, GLXContext, int);
typedef GLXPbuffer (*PFN_glXCreatePbuffer)(Display *, GLXFBConfig, const int *);
typedef int (*PFN_glXMakeContextCurrent)(Display *, GLXDrawable, GLXDrawable, GLXContext);
typedef void (*PFN_glXDestroyPbuffer)(Display *, GLXPbuffer);
typedef void (*PFN_glXDestroyContext)(Display *, GLXContext);
typedef const unsigned char *(*PFN_glGetString)(unsigned int);

static void *open_library(const char *name) {
    void *handle = dlopen(name, RTLD_NOW | RTLD_LOCAL);
    if (handle == NULL) {
        fprintf(stderr, "dlopen failed for %s: %s\n", name, dlerror());
        exit(2);
    }
    return handle;
}

static void *load_symbol(void *handle, const char *name) {
    dlerror();
    void *symbol = dlsym(handle, name);
    const char *error = dlerror();
    if (error != NULL || symbol == NULL) {
        fprintf(stderr, "dlsym failed for %s: %s\n", name, error != NULL ? error : "symbol is null");
        exit(3);
    }
    return symbol;
}

static unsigned int hold_seconds_from_env(void) {
    const char *value = getenv("PROBE_HOLD_SECONDS");
    if (value == NULL || *value == '\0') {
        return 0;
    }

    char *end = NULL;
    long parsed = strtol(value, &end, 10);
    if (end == value || *end != '\0' || parsed < 0 || parsed > 600) {
        fprintf(stderr, "invalid PROBE_HOLD_SECONDS: %s\n", value);
        exit(11);
    }

    return (unsigned int)parsed;
}

int main(void) {
    void *x11 = open_library("libX11.so.6");
    void *gl = open_library("libGL.so.1");

    PFN_XOpenDisplay XOpenDisplay_fn = (PFN_XOpenDisplay)load_symbol(x11, "XOpenDisplay");
    PFN_XDefaultScreen XDefaultScreen_fn = (PFN_XDefaultScreen)load_symbol(x11, "XDefaultScreen");
    PFN_XCloseDisplay XCloseDisplay_fn = (PFN_XCloseDisplay)load_symbol(x11, "XCloseDisplay");
    PFN_XFree XFree_fn = (PFN_XFree)load_symbol(x11, "XFree");

    PFN_glXQueryVersion glXQueryVersion_fn = (PFN_glXQueryVersion)load_symbol(gl, "glXQueryVersion");
    PFN_glXChooseFBConfig glXChooseFBConfig_fn = (PFN_glXChooseFBConfig)load_symbol(gl, "glXChooseFBConfig");
    PFN_glXCreateNewContext glXCreateNewContext_fn = (PFN_glXCreateNewContext)load_symbol(gl, "glXCreateNewContext");
    PFN_glXCreatePbuffer glXCreatePbuffer_fn = (PFN_glXCreatePbuffer)load_symbol(gl, "glXCreatePbuffer");
    PFN_glXMakeContextCurrent glXMakeContextCurrent_fn = (PFN_glXMakeContextCurrent)load_symbol(gl, "glXMakeContextCurrent");
    PFN_glXDestroyPbuffer glXDestroyPbuffer_fn = (PFN_glXDestroyPbuffer)load_symbol(gl, "glXDestroyPbuffer");
    PFN_glXDestroyContext glXDestroyContext_fn = (PFN_glXDestroyContext)load_symbol(gl, "glXDestroyContext");
    PFN_glGetString glGetString_fn = (PFN_glGetString)load_symbol(gl, "glGetString");

    Display *display = XOpenDisplay_fn(NULL);
    if (display == NULL) {
        fprintf(stderr, "XOpenDisplay failed; DISPLAY=%s\n", getenv("DISPLAY") != NULL ? getenv("DISPLAY") : "<unset>");
        return 4;
    }

    int glx_major = 0;
    int glx_minor = 0;
    if (!glXQueryVersion_fn(display, &glx_major, &glx_minor)) {
        fprintf(stderr, "glXQueryVersion failed\n");
        XCloseDisplay_fn(display);
        return 5;
    }

    int screen = XDefaultScreen_fn(display);
    const int fb_attrs[] = {
        GLX_DRAWABLE_TYPE, GLX_PBUFFER_BIT,
        GLX_RENDER_TYPE, GLX_RGBA_BIT,
        0
    };

    int config_count = 0;
    GLXFBConfig *configs = glXChooseFBConfig_fn(display, screen, fb_attrs, &config_count);
    if (configs == NULL || config_count < 1) {
        fprintf(stderr, "glXChooseFBConfig found no pbuffer-capable RGBA config\n");
        XCloseDisplay_fn(display);
        return 6;
    }

    GLXContext context = glXCreateNewContext_fn(display, configs[0], GLX_RGBA_TYPE, NULL, 1);
    if (context == NULL) {
        fprintf(stderr, "glXCreateNewContext failed\n");
        XFree_fn(configs);
        XCloseDisplay_fn(display);
        return 7;
    }

    const int pbuffer_attrs[] = {
        GLX_PBUFFER_WIDTH, 1,
        GLX_PBUFFER_HEIGHT, 1,
        0
    };

    GLXPbuffer pbuffer = glXCreatePbuffer_fn(display, configs[0], pbuffer_attrs);
    XFree_fn(configs);
    if (pbuffer == 0) {
        fprintf(stderr, "glXCreatePbuffer failed\n");
        glXDestroyContext_fn(display, context);
        XCloseDisplay_fn(display);
        return 8;
    }

    if (!glXMakeContextCurrent_fn(display, pbuffer, pbuffer, context)) {
        fprintf(stderr, "glXMakeContextCurrent failed\n");
        glXDestroyPbuffer_fn(display, pbuffer);
        glXDestroyContext_fn(display, context);
        XCloseDisplay_fn(display);
        return 9;
    }

    const unsigned char *vendor = glGetString_fn(GL_VENDOR);
    const unsigned char *renderer = glGetString_fn(GL_RENDERER);
    const unsigned char *version = glGetString_fn(GL_VERSION);

    if (vendor == NULL || renderer == NULL || version == NULL) {
        fprintf(stderr, "glGetString returned null identity field\n");
        glXMakeContextCurrent_fn(display, 0, 0, NULL);
        glXDestroyPbuffer_fn(display, pbuffer);
        glXDestroyContext_fn(display, context);
        XCloseDisplay_fn(display);
        return 10;
    }

    printf("GLX_VERSION=%d.%d\n", glx_major, glx_minor);
    printf("GL_VENDOR=%s\n", vendor);
    printf("GL_RENDERER=%s\n", renderer);
    printf("GL_VERSION=%s\n", version);
    fflush(stdout);

    unsigned int hold_seconds = hold_seconds_from_env();
    if (hold_seconds > 0) {
        fprintf(stderr, "probe hold seconds: %u\n", hold_seconds);
        sleep(hold_seconds);
    }

    glXMakeContextCurrent_fn(display, 0, 0, NULL);
    glXDestroyPbuffer_fn(display, pbuffer);
    glXDestroyContext_fn(display, context);
    XCloseDisplay_fn(display);
    dlclose(gl);
    dlclose(x11);

    return 0;
}
