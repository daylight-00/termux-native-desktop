case $- in
    *i*) ;;
    *) return ;;
esac

for f in \
    "$HOME/.config/bash/interactive.sh" \
    "$HOME/.config/bash/prompt.sh" \
    "$HOME/.config/bash/aliases.sh"; do
    [ -r "$f" ] && . "$f"
done

for f in "$HOME/.config/bash/conf.d/"*.sh; do
    [ -r "$f" ] && . "$f"
done

unset f
