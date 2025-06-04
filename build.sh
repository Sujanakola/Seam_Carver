#!/usr/bin/env bash
# Install Java
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 17.0.9-tem

# Compile Java files
javac Picture.java SeamCarver.java

# Create necessary directories
mkdir -p uploads
mkdir -p static/img 