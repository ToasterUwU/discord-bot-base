cd .vscode
rename *.json *.save
cd ..
rename config.json config.save
rename _base_config.json _base_config.save

del /s /q bot.spec bot.log source-code.zip windows-installer.exe .\*.json
rmdir /s /q dist\ __pycache__\ build\ cogs\__pycache__ internal_tools\__pycache__

rename config.save config.json
rename _base_config.save _base_config.json
cd .vscode
rename *.save *.json