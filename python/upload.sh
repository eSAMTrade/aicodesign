#!/usr/bin/env bash

set -euo pipefail

package_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
work_dir="$(mktemp -d)"
dist_dir="${work_dir}/dist"

cleanup() {
    rm -rf -- "${work_dir}"
}
trap cleanup EXIT

if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is required. Install it from https://docs.astral.sh/uv/." >&2
    exit 1
fi

run_packaging_tool() {
    uv run --quiet --no-project --with build --with twine python -m "$@"
}

echo "Building aicodesign..."
run_packaging_tool build --outdir "${dist_dir}" "${package_dir}"

echo "Validating distributions..."
run_packaging_tool twine check "${dist_dir}"/*

echo "Uploading distributions to PyPI..."
export TWINE_USERNAME="${TWINE_USERNAME:-__token__}"
run_packaging_tool twine upload "${dist_dir}"/*

echo "Published successfully."
