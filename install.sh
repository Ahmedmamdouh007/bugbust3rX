#!/bin/bash

echo "========== bugbust3rX Installer =========="

PROJECT_PATH=$(pwd)

echo
echo "[+] Project detected at:"
echo "$PROJECT_PATH"

sed "s|__PROJECT_PATH__|$PROJECT_PATH|g" bugbust3rX > bugbust3rX.tmp

mv bugbust3rX.tmp bugbust3rX

chmod +x bugbust3rX

sudo cp bugbust3rX /usr/local/bin/

echo
echo "[+] Installation completed successfully!"
echo
echo "You can now run:"
echo
echo "    bugbust3rX"
echo
