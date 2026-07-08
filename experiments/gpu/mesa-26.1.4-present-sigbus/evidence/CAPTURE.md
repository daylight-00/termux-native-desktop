# Evidence capture (run on device)

Strace captures from the diagnosis, if still present:

    cp ~/.cache/vkcube.strace         evidence/vkcube-patched-round1.strace  2>/dev/null
    cp ~/.cache/vkcube-vanilla.strace evidence/vkcube-vanilla.strace         2>/dev/null
    cp ~/.cache/vkcube-tx.strace      evidence/vkcube-0007-0014.strace       2>/dev/null

Regenerable proofs (current builds):

    for v in 26.1.4 26.1.4-turnip 26.1.4-full; do
      readelf -d ~/gl/opt/mesa-glibc-$v/lib/libvulkan_freedreno.so \
        > evidence/needed-$v.txt 2>/dev/null
    done
    readelf -d ~/opt/mesa-26-glibc/lib/libvulkan_freedreno.so \
      > evidence/needed-26.0.6-backup.txt
    readelf -d $PREFIX/lib/libvulkan_freedreno.so \
      > evidence/needed-bionic.txt

The bisect logs themselves live in the session transcript (git bisect was
reset); round outcomes are recorded in the README.
