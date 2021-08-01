@echo off
set /p ch="MGU>1, IDC>2: "

IF %ch%==1 ( 
    set /A ip = 131
    set pass=mgu22
    ) 
IF %ch%==2 (
    set /A ip = 50  
    set pass=MGU22
    )

C:\\WINDOWS\\system32\\net.exe use \\10.12.81.%ip%\TAL /user:MGU22 %pass%
copy OSIS_DIAG.skr \\10.12.81.%ip%\TAL
C:\\WINDOWS\\system32\\net.exe use \\10.12.81.%ip%\TAL /delete