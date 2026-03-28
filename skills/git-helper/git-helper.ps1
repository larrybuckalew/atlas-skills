#!/usr/bin/env pwsh
# Git Helper - Status
# Shows working tree status

param(
    [string]$Path = "."
)

Write-Host "=== Git Status ===" -ForegroundColor Cyan
git -C $Path status
