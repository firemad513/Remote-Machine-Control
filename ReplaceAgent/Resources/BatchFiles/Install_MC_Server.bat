echo off
setlocal enabledelayedexpansion

rem (1) checked current machine whether preinstalled MC Server, if yes, then uninstall MC Server first
IF EXIST "C:\Program Files\Mobile Center Server\installation\Change Mobile Center Server Installation.exe" (
	echo Now trying to uninstall MC Server on this machine first...
	"C:\Program Files\Mobile Center Server\installation\Change Mobile Center Server Installation.exe" -i silent -DUSER_INPUT_RESULT_UNINSTALL_POSTGRES_YES=1
)  ELSE (
	echo "there is no old Server installation "
)

rem (2) Install 7zip and extracting the installer
if EXIST "C:\Program Files\7-Zip" (
	echo no need to silent install 7-zip...
)  ELSE (
	echo not found 7-zip silent install package...
	start /wait 7z1900-x64.exe /S
)
rem (3) unzip the zip installer to the current folder
if EXIST ".\install*.exe" (
       echo zip already been unzip...
)  ELSE (
       echo start to unzip the installer
       "C:\Program Files\7-Zip\7z.exe" x *.zip -o.
)

rem (4) Deploy MC Server to local machine
echo start to deploy MC Server now...

set installExeFileName=
for /f "delims=" %%i in ('dir .\install*.exe /b') do (
	set installExeFileName=%installExeFileName%%%i
)

echo %installExeFileName%-i silent -DUSER_INPUT_SERVER_IP=%1 -DUSER_INPUT_SERVER_PORT=8443 -DUSER_INPUT_POSTGRES_SERVER_PORT=5432 -DUSER_INPUT_POSTGRES_SUPERUSER_PASSWORD=Password1 -DUSER_INPUT_POSTGRES_HPMCADMIN_USER=hpmcadmin -DUSER_INPUT_POSTGRES_HPMCADMIN_PASSWORD=Password1 -DUSER_INPUT_NEW_ADMIN_PASSWORD=password -DUSER_INPUT_INSTALL_TEST_MODE=1 -Dhpmc.param.HPMC_DEV=true -DUSER_INPUT_USE_SSL=1 -DUSER_INPUT_HPMC_PRIVATE_PORT=8888

%installExeFileName% -i silent -DUSER_INPUT_SERVER_IP=%1 -DUSER_INPUT_SERVER_PORT=8443 -DUSER_INPUT_POSTGRES_SERVER_PORT=5432 -DUSER_INPUT_POSTGRES_SUPERUSER_PASSWORD=Password1 -DUSER_INPUT_POSTGRES_HPMCADMIN_USER=hpmcadmin -DUSER_INPUT_POSTGRES_HPMCADMIN_PASSWORD=Password1 -DUSER_INPUT_NEW_ADMIN_PASSWORD=password -DUSER_INPUT_INSTALL_TEST_MODE=1 -Dhpmc.param.HPMC_DEV=true -DUSER_INPUT_USE_SSL=1 -DUSER_INPUT_HPMC_PRIVATE_PORT=8888

echo MC deployment finished
cd ..

