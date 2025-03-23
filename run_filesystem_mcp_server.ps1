# PowerShell script to run the filesystem MCP server
# This script will start the MCP server and keep it running until you close the window

Write-Host "Starting Filesystem MCP Server..." -ForegroundColor Green
Write-Host "Allowed directory: d:/AI_play/AI_Code/browser-use" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

# Run the server
npx -y @modelcontextprotocol/server-filesystem "d:/AI_play/AI_Code/browser-use"
