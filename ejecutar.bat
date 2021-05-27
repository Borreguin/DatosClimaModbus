call cd /D "%~dp0" 
call C:\ProgramData\Anaconda3\Scripts\activate.bat 
call C:\ProgramData\Anaconda3\python.exe "%~dp0main.py" 
rem Para motivos de depuración del bat incluya al final: call cmd /k
rem esta instrucción mostrará los resultados del script
rem NOTA: Nunca deje la instrucción "call cmd /k" al final de este archivo
rem ya que dejará abierto este terminal, lo que podría ser indeseable si se ejecuta de manera periódica