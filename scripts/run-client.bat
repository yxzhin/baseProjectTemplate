@echo off

cd /d "%~dp0"
cd ../src/frontend

pnpm install && pnpm run dev
