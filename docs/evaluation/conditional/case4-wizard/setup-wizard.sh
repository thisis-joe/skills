#!/usr/bin/env bash
set +x
set -euo pipefail
umask 077
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
STORE="$SCRIPT_DIR/helpers/env_store.py"
ENV_FILE=${1:-"$SCRIPT_DIR/.env"}
[[ -t 0 && -t 1 ]] || { printf '%s\n' 'Human-operated only: run in a terminal.' >&2; exit 2; }
command -v python3 >/dev/null || { printf '%s\n' 'python3 is required.' >&2; exit 2; }
[[ -d "$(dirname -- "$ENV_FILE")" ]] || { printf '%s\n' 'Destination parent must exist.' >&2; exit 2; }
stage() { printf '\n[%s/3] %s\n' "$1" "$2"; }
confirm() { local answer; IFS= read -r -p "$1 [y/N] " answer </dev/tty; [[ "$answer" == y || "$answer" == Y ]]; }
open_url() {
  local url=$1
  printf 'Open: %s\n' "$url"
  if command -v open >/dev/null; then open "$url"
  elif command -v xdg-open >/dev/null; then xdg-open "$url"
  else confirm 'Open that exact URL manually, then continue?' || exit 1
  fi
}
write_value() { local key=$1 value=$2; printf '%s' "$value" | python3 "$STORE" set "$ENV_FILE" "$key"; }
stage 1 'Capture the approved sending key locally'
if python3 "$STORE" present "$ENV_FILE" RESEND_API_KEY; then
  if confirm 'Replace the locally captured key?'; then replace_key=yes; else replace_key=no; fi
else replace_key=yes; fi
if [[ "$replace_key" == yes ]]; then
  open_url 'https://resend.com/api-keys'
  printf '%s\n' 'Log in and obtain the previously approved key. Key creation/revocation is a separate human choice; this wizard performs neither.'
  confirm 'Ready to capture the approved value locally?' || exit 1
  key_value=''
  IFS= read -r -s -p 'RESEND_API_KEY (hidden): ' key_value </dev/tty
  printf '\n' >/dev/tty
  [[ -n "$key_value" ]] || { printf '%s\n' 'No key captured; prior stages retained.' >&2; exit 1; }
  write_value RESEND_API_KEY "$key_value"
  unset key_value
fi
stage 2 'Record the agreed public application origin'
if python3 "$STORE" present "$ENV_FILE" APP_ORIGIN; then
  printf '%s\n' 'Existing origin retained. To change it, edit the approved inventory and rerun a reviewed wizard.'
else write_value APP_ORIGIN 'https://reports.example.invalid'; fi
stage 3 'Safe readback and manual CI handoff'
python3 "$STORE" present "$ENV_FILE" RESEND_API_KEY
python3 "$STORE" present "$ENV_FILE" APP_ORIGIN
printf '%s\n' 'Local preparation complete. No remote secret/variable was written and no message was sent.'
printf '%s\n' 'Pending human CI setup, if separately authorized: secret RESEND_API_KEY; variable APP_ORIGIN (see supplied workflow references). Never copy a key into logs.'
printf '%s\n' 'Keep this local .env out of version control. Retain it only for intended local use; remove it manually when that use ends. Rerun preserves already captured stages.'
