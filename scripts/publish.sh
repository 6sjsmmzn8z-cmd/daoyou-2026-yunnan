#!/usr/bin/env bash
# Create a new private repository and publish downloadable Release assets.
set -euo pipefail
repo_name="${1:-daoyou-2026-yunnan}"
if [[ ! "$repo_name" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo 'Repository name must contain only letters, digits, dots, underscores or hyphens.' >&2
  exit 1
fi
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
command -v gh >/dev/null || { echo 'Install GitHub CLI first.' >&2; exit 1; }
gh api user --jq '.login' >/dev/null
python3 scripts/build_downloads.py
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo 'Initialize and commit this repository before publishing.' >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo 'Commit all intended repository changes before publishing.' >&2
  exit 1
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo 'origin already exists. Inspect the remote before pushing; this script will not overwrite it.' >&2
  exit 1
fi
# Fails if a repository of the same name already exists; does not adopt or overwrite it.
gh repo create "$repo_name" --private --source . --remote origin --push
notes_file="$(mktemp)"
trap 'rm -f "$notes_file"' EXIT
cat > "$notes_file" <<'EOF'
2026全国导游资格考试资料库，云南昆明中文类。资料截点2026-11-14。

完整包包含全部归档资料与原创复习材料；核心包为考前精选。另附32页PDF复习册、可编辑DOCX与来源CSV。

来源去重后229份文件，含104份PDF。课程网页不是离线视频，公开样章不是整本商业教材。预测是复习优先级和原创练习，不保证命中。
EOF
gh release create v2026.11.14 \
  downloads/guide-all.zip downloads/guide-core.zip \
  study.pdf study.docx 资源总表.csv \
  --title '2026导游资格考试资料 · 云南昆明中文' --notes-file "$notes_file"
gh repo view --json url --jq '.url'
