#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

B9_OUT=${B9_OUT:?set B9_OUT to the completed Phase B9 receipt}
OUT=${OUT:?set OUT to a stage-specific receipt directory}
REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
RUNNER="$REPO/experiments/glibc/selected-obsidian-closure/recipe/run-explicit-generation-cpu-validation.sh"

mkdir -p "$OUT"

cat >"$OUT/interaction-contract.tsv" <<'EOF'
field	value
mode	PASSIVE_NO_GUI_INPUT
operator_action	OBSERVE_ONLY
forbidden_action	DO_NOT_CLICK_OPEN_VAULT_OR_ANY_GUI_CONTROL
claim	IDLE_STARTUP_SURVIVAL_AND_MAPS_ONLY
interactive_file_chooser_capability	OUT_OF_SCOPE
EOF

printf '\n===== passive Obsidian explicit-generation CPU validation =====\n'
printf 'Do not click Open vault, Create vault, or any other GUI control.\n'
printf 'Observe the initial window only until the capture finishes.\n\n'

exec env \
    B9_OUT="$B9_OUT" \
    OUT="$OUT" \
    bash "$RUNNER"
