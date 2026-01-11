#!/bin/bash

set -e

VERSION="0.1.0-local"
echo "🚀 Building version: $VERSION..."

rm -rf dist/ dist-packages/ build/
mkdir -p dist-packages

echo "🔨 Building Binary..."
pyinstaller --onefile --name gitw src/gitw/main.py

echo "📦 Packaging DEB..."
fpm -s dir -t deb \
  -n git-wizard \
  -v $VERSION \
  --architecture amd64 \
  --maintainer "Noufal <noufalkakdlr@gmail.com>" \
  --description "A simple CLI tool to automate Git setup" \
  -d "git" \
  -p dist-packages/git-wizard_${VERSION}_amd64.deb \
  dist/gitw=/usr/bin/gitw

echo "📦 Packaging RPM..."
fpm -s dir -t rpm \
  -n git-wizard \
  -v $VERSION \
  --architecture x86_64 \
  --maintainer "Noufal <noufalkakdlr@gmail.com>" \
  --description "A simple CLI tool to automate Git setup" \
  -d "git" \
  -p dist-packages/git-wizard-${VERSION}-1.x86_64.rpm \
  dist/gitw=/usr/bin/gitw

echo "✅ Build Complete! Check the 'dist-packages' folder."
ls -l dist-packages/
