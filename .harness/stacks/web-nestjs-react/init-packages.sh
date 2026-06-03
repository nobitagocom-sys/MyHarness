#!/usr/bin/env bash
# Run once after scaffolding to install latest compatible packages.
# Usage: bash init-packages.sh [project-root]
# Default project-root: current directory

set -euo pipefail

ROOT="${1:-.}"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_INSTRUCTIONS_PATH=".harness/stacks/web-nestjs-react/instructions"

check_dir() {
  if [[ ! -d "$1" ]]; then
    echo "ERROR: directory not found: $1"
    echo "Run this script from the project root, or pass the path as an argument."
    exit 1
  fi
}

check_dir "$BACKEND"
check_dir "$FRONTEND"

echo ""
echo "=== COPY AGENT INSTRUCTIONS ==="
DEST="$ROOT/.github/agents"
mkdir -p "$DEST"

# Copy file, rewrite links: instructions/ -> ../../.harness/stacks/web-nestjs-react/instructions/
# Source links use relative path from harness (instructions/xx.md)
# Destination is .github/agents/copilot-instructions.md
# So the correct relative path from dest back to harness instructions is: ../../.harness/stacks/web-nestjs-react/instructions/
sed 's|(instructions/|(../../'"$HARNESS_INSTRUCTIONS_PATH"'/|g' \
  "$SCRIPT_DIR/copilot-instructions.md" > "$DEST/copilot-instructions.md"

echo "Copied .github/agents/copilot-instructions.md (links rewritten)"

echo ""
echo "=== BACKEND: installing packages ==="
cd "$BACKEND"

# ── Runtime dependencies ───────────────────────────────────────────────────────
npm install \
  @nestjs/common@latest \
  @nestjs/core@latest \
  @nestjs/platform-express@latest \
  @nestjs/jwt@latest \
  @nestjs/config@latest \
  @nestjs/swagger@latest \
  @nestjs/throttler@latest \
  nestjs-pino@latest \
  pino-http@latest \
  prisma@latest \
  @prisma/client@latest \
  bcrypt@latest \
  class-validator@latest \
  class-transformer@latest \
  mysql2@latest \
  reflect-metadata@latest \
  rxjs@latest

# ── Dev dependencies ───────────────────────────────────────────────────────────
npm install --save-dev \
  @nestjs/testing@latest \
  @nestjs/cli@latest \
  @types/bcrypt@latest \
  @types/node@latest \
  @types/express@latest \
  typescript@latest \
  ts-node@latest \
  ts-jest@latest \
  jest@latest \
  @types/jest@latest \
  supertest@latest \
  @types/supertest@latest \
  source-map-support@latest

echo ""
echo "=== FRONTEND: installing packages ==="
cd "$ROOT/frontend"

# ── Runtime dependencies ───────────────────────────────────────────────────────
npm install \
  react@latest \
  react-dom@latest \
  react-router-dom@latest \
  @tanstack/react-query@latest \
  axios@latest \
  react-hook-form@latest \
  zod@latest

# ── Dev dependencies ───────────────────────────────────────────────────────────
npm install --save-dev \
  vite@latest \
  @vitejs/plugin-react@latest \
  tailwindcss@^3 \
  autoprefixer@latest \
  postcss@latest \
  typescript@latest \
  @types/react@latest \
  @types/react-dom@latest \
  @types/node@latest \
  vitest@latest \
  @testing-library/react@latest \
  @testing-library/user-event@latest \
  @testing-library/jest-dom@latest

echo ""
echo "=== DONE ==="
echo ""
echo "Installed versions:"
echo ""
echo "--- backend ---"
cd "$ROOT/backend"
node -e "
  const pkg = require('./package.json');
  const all = { ...pkg.dependencies, ...pkg.devDependencies };
  const keys = [
    '@nestjs/common','@nestjs/core','@nestjs/platform-express',
    '@nestjs/jwt','@nestjs/config','@nestjs/swagger','@nestjs/throttler',
    'nestjs-pino','pino-http','prisma','@prisma/client',
    'bcrypt','class-validator','class-transformer','mysql2',
    'reflect-metadata','rxjs','typescript','jest','ts-jest'
  ];
  keys.forEach(k => console.log(k.padEnd(36) + (all[k] || '-')));
"

echo ""
echo "--- frontend ---"
cd "$ROOT/frontend"
node -e "
  const pkg = require('./package.json');
  const all = { ...pkg.dependencies, ...pkg.devDependencies };
  const keys = [
    'react','react-dom','react-router-dom','@tanstack/react-query',
    'axios','react-hook-form','zod','vite','@vitejs/plugin-react',
    'tailwindcss','typescript'
  ];
  keys.forEach(k => console.log(k.padEnd(36) + (all[k] || '-')));
"

echo ""
echo "Next steps:"
echo "  cd backend && npx prisma generate"
echo "  docker-compose up --build"
