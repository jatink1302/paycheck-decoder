#!/usr/bin/env bash
# Installs the local pre-commit hook that runs scripts/check_data_dir.py.
# Run once after cloning: bash scripts/install_hooks.sh
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
hook_path="$repo_root/.git/hooks/pre-commit"

cat > "$hook_path" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
python3 "$(git rev-parse --show-toplevel)/scripts/check_data_dir.py"
EOF

chmod +x "$hook_path"
echo "Installed pre-commit hook at $hook_path"
