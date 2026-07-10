#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* Minimal ABI declaration: no development headers are required for the pilot. */
void dbus_get_version(int *major_version, int *minor_version, int *micro_version);

static unsigned parse_hold_seconds(void) {
    const char *value = getenv("DBUS_PROBE_HOLD_SECONDS");
    if (value == NULL || *value == '\0') {
        return 15U;
    }

    errno = 0;
    char *end = NULL;
    unsigned long parsed = strtoul(value, &end, 10);
    if (errno != 0 || end == value || *end != '\0' || parsed > 300UL) {
        fprintf(stderr, "invalid DBUS_PROBE_HOLD_SECONDS: %s\n", value);
        exit(2);
    }

    return (unsigned)parsed;
}

int main(void) {
    int major = 0;
    int minor = 0;
    int micro = 0;

    dbus_get_version(&major, &minor, &micro);
    printf("libdbus runtime version: %d.%d.%d\n", major, minor, micro);
    fflush(stdout);

    unsigned hold_seconds = parse_hold_seconds();
    printf("probe pid: %ld\n", (long)getpid());
    printf("hold seconds: %u\n", hold_seconds);
    fflush(stdout);

    if (hold_seconds > 0U) {
        sleep(hold_seconds);
    }

    return 0;
}
