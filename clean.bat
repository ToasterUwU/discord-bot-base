cd .vscode
rename *.json *.save
cd ..
rename config.json config.save

del /s /q bot.spec bot.log source-code.zip windows-installer.exe .\*.json
rmdir /s /q dist\ __pycache__\ build\ cogs\__pycache__

rename config.save config.json
cd .vscode
rename *.save *.json