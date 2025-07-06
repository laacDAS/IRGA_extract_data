Set objShell = CreateObject("Wscript.Shell")
' Caminho absoluto do Python (ajuste se necessário)
pythonExe = "pythonw.exe"
' Caminho absoluto do main.py
scriptPath = WScript.ScriptFullName
scriptDir = Left(scriptPath, InStrRev(scriptPath, "\") - 1)
mainPy = scriptDir & "\main.py"

' Executa o main.py sem abrir terminal
objShell.Run pythonExe & " """ & mainPy & """", 0, False
