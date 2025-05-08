from time import sleep
from rich import *
import os
import random
import wmi
import winreg
import subprocess
import ctypes
from ctypes import wintypes
import sys

def winact():
    try:
        c = wmi.WMI()
        for os in c.Win32_OperatingSystem():
            if os.Name.startswith("Microsoft Windows"):
                if os.Description == "Windows(R) Operating System" and os.BuildNumber > "9600":
                    return "[blue]Activated[/blue]"
        return "[red]Not activated[/red]"
    except Exception as e:
        pass

def check_defender():
    try:
        result = subprocess.run(['sc', 'query', 'WinDefend'], capture_output=True, text=True)
        if "RUNNING" in result.stdout or "STOPPED" in result.stdout:
            return "[red]Installed[/red]"
        return "[blue]Not installed[/blue]"
    except Exception:
        return "[blue]Not installed[/blue]"

def check_edge():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        try:
            result = subprocess.run([edge_path, '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            return f"[red]Installed (v{version})[/red]"
        except:
            return "[red]Installed[/red]"
    return "[blue]Not installed[/blue]"

Microsoft_edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OneDrive = r"C:\Users\fotokoyo\AppData\Local\Microsoft\OneDrive\OneDrive.exe"

current_file = os.path.realpath(__file__)
script_path = os.path.dirname(current_file)

class OSVERSIONINFOEXW(ctypes.Structure):
    _fields_ = [("dwOSVersionInfoSize", wintypes.DWORD),
                ("dwMajorVersion", wintypes.DWORD),
                ("dwMinorVersion", wintypes.DWORD),
                ("dwBuildNumber", wintypes.DWORD),
                ("dwPlatformId", wintypes.DWORD),
                ("szCSDVersion", wintypes.WCHAR * 128),
                ("wServicePackMajor", wintypes.WORD),
                ("wServicePackMinor", wintypes.WORD),
                ("wSuiteMask", wintypes.WORD),
                ("wProductType", wintypes.BYTE),
                ("wReserved", wintypes.BYTE)]

def get_winvers():
    osvi = OSVERSIONINFOEXW()
    osvi.dwOSVersionInfoSize = ctypes.sizeof(OSVERSIONINFOEXW)
    retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(osvi))
    if retcode == 0:
        major_version = osvi.dwMajorVersion
        minor_version = osvi.dwMinorVersion
        product_type = osvi.wProductType
        if major_version == 10 and product_type == 1:
            return "Windows 10 Pro"
        elif major_version == 11 and product_type == 1:
            return "Windows 11 Home"
        else:
            return f"Windows {major_version}"
    else:
        pass

def check_choco():
    try:
        result = subprocess.run(['where', 'choco'], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_edge_version():
    try:
        result = subprocess.run(['msedge', '--version'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pass

def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    os.system("cls")
    print()
    if check_admin():
        pass
    else:
        print("[red]ЗАПУСТИ ПРОГРАММУ ОТ ИМЕНИ АДМИНИСТРАТОРА[/red]")
        sleep(10)
        sys.exit()
    print("    [green]Windows[/green]: " + get_winvers())
    print("    [green]Windows activation[/green]: " + winact())
    print("    [green]Path[/green]: " + script_path)
    print()
    print('''    [[blue]1[/blue]] - [yellow]Install programm[/yellow]      | [bright_black]Установка программ[/bright_black]''')
    print('''    [[blue]2[/blue]] - [yellow]Optimization windows[/yellow]  | [bright_black]Отключение ненужных служб[/bright_black]''')
    print('''    [[blue]3[/blue]] - [yellow]Activation windows[/yellow]    | [bright_black]Активация Windows[/bright_black]''')
    print()
    print('''    [red]Code by[/red] [purple]conn01sseur[/purple]''')
    print()

    a = input("  --> ")

    if a == "1":
        os.system("cls")
        print()
        if check_choco():
            print("    [green]Choco[/green]: [blue]Installed[/blue]")
            print()
            print('''           [cyan]Communication[/cyan]''')
            print('''    [[blue]1[/blue]]  - [yellow]Discord[/yellow]''')
            print('''    [[blue]2[/blue]]  - [yellow]Telegram[/yellow]''')
            print()
            print('''           [cyan]Games[/cyan]''')
            print('''    [[blue]3[/blue]]  - [yellow]Steam[/yellow]''')
            print('''    [[blue]4[/blue]]  - [yellow]Epic Games[/yellow]''')
            print()
            print('''           [cyan]Browser[/cyan]''')
            print('''    [[blue]5[/blue]]  - [yellow]FireFox[/yellow]''')
            print('''    [[blue]6[/blue]]  - [yellow]Tor Browser[/yellow]''')
            print('''    [[blue]7[/blue]]  - [yellow]Chrome[/yellow]''')
            print('''    [[blue]8[/blue]]  - [yellow]Yandex[/yellow]''')
            print('''    [[blue]9[/blue]]  - [yellow]Opera[/yellow]''')
            print('''    [[blue]10[/blue]] - [yellow]Brave[/yellow]''')
            print('''    [[blue]11[/blue]] - [yellow]Vivaldi[/yellow]''')
            print()
            print('''           [cyan]Utilites[/cyan]''')
            print('''    [[blue]12[/blue]] - [yellow]7-zip[/yellow]''')
            print('''    [[blue]13[/blue]] - [yellow]qBittorrent[/yellow]''')
            print()
            print('''           [cyan]Other[/cyan]''')
            print('''    [[blue]oo[/blue]] - [yellow]Install other program[/yellow]''')
            print()
            print('''    [[red]bb[/red]] - [red]Back to the main menu[/red]''')
            print()
            c = int(input("  --> "))
            if c == "1":
                os.system("choco install Discord")
            elif c == "2":
                os.system("choco install telegram")
            elif c == "3":
                os.system("choco install Steam")
            elif c == "4":
                os.system("choco install epicgameslauncher")
            elif c == "5":
                os.system("choco install FireFox")
            elif c == "6":
                os.system("choco install tor-browser")
            elif c == "7":
                os.system("choco install chrome")
            elif c == "8":
                os.system("choco install yandex")
            elif c == "9":
                os.system("choco install opera")
            elif c == "10":
                os.system("choco install brave")
            elif c == "11":
                os.system("choco install vivaldi")
            elif c == "12":
                os.system("choco install 7zip")
            elif c == "13":
                os.system("choco install qbittorrent")
            elif c == "oo":
                other_program = input("choco install  --> ")
                os.system(f"choco install {other_program}")
            elif c == "bb":
                main()
            main()

        else:
            print("    [green]Choco[/green]: [red]Not installed[/red]")
            install_choco = input("Установить Choco? [Y] or [N]: ")
            if install_choco == "Y" or install_choco == "y":
                try:
                    os.system("powershell Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
                    print()
                    print('''    [[red]Пожалуйста перезагрузи программу[/red]]''')
                except:
                    pass
            else:
                main()

    elif a == "2":
        os.system("cls")
        print()
        if os.path.exists(OneDrive):
            print("    [green]OneDrive[/green]: [red]Installed[/red]")
            print()
        else:
            print("    [green]OneDrive[/green]: [blue]Not installed[/blue]")
            print()

        print("    [green]Windows Defender[/green]: " + check_defender())
        print()
        print("    [green]Microsoft Edge[/green]: " + check_edge())
        print()
        print('''    [[blue]1[/blue]] - Disable services''')
        print('''    [[blue]2[/blue]] - Disable Telemetry''')
        print('''    [[blue]3[/blue]] - Remove All Microsoft APPS''')
        print('''    [[blue]4[/blue]] - Remove OneDrive''')
        print('''    [[blue]5[/blue]] - Remove Windows Defender''')
        print()
        b = int(input("  --> "))

        if b == 1:
            Disable_Services = "Set-Service -Name 'WbioSrvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", Disable_Services], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            Disable_NFC = "Set-Service -Name 'SEMgrSvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", Disable_NFC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            Windup = "Set-Service -Name 'wscsvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", Windup], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            dmwappushservice = "Set-Service -Name 'dmwappushservice' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", dmwappushservice], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            Browsere = "Set-Service -Name 'Browser' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", Browsere], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            WSearch = "Set-Service -Name 'WSearch' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", WSearch], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            KeyIso = "Set-Service -Name 'KeyIso' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", KeyIso], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            SharedAccess = "Set-Service -Name 'SharedAccess' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", SharedAccess], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            workfolderssvc = "Set-Service -Name 'workfolderssvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", workfolderssvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            LanmanServer = "Set-Service -Name 'LanmanServer' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", LanmanServer], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            XboxNetApiSvc = "Set-Service -Name 'XboxNetApiSvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", XboxNetApiSvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            lfsvc = "Set-Service -Name 'lfsvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", lfsvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            SensorDataService = "Set-Service -Name 'SensorDataService' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", SensorDataService], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            SensorService = "Set-Service -Name 'SensorService' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", SensorService], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            stisvc = "Set-Service -Name 'stisvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", stisvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            AJRouter = "Set-Service -Name 'AJRouter' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", AJRouter], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            vmicrdv = "Set-Service -Name 'vmicrdv' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", vmicrdv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()

            SensrSvc = "Set-Service -Name 'SensrSvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", SensrSvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            WPDBusEnum = "Set-Service -Name 'WPDBusEnum' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", WPDBusEnum], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            NetTcpPortSharing = "Set-Service -Name 'NetTcpPortSharing' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", NetTcpPortSharing], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            WerSvc = "Set-Service -Name 'WerSvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", WerSvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            BDESVC = "Set-Service -Name 'BDESVC' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", BDESVC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            RemoteRegistry = "Set-Service -Name 'RemoteRegistry' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", RemoteRegistry], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            Fax = "Set-Service -Name 'Fax' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", Fax], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            PhoneSvc = "Set-Service -Name 'PhoneSvc' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", PhoneSvc], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            TapiSrv = "Set-Service -Name 'TapiSrv' -StartupType Disabled"
            process = subprocess.Popen(["powershell", "-Command", TapiSrv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
        
        elif b == 2:
            os.system("sc delete DiagTrack")
            os.system("sc delete dmwappushservice")
            os.system('echo "" > C:\ProgramData\Microsoft\Diagnosis\ETLLogs\AutoLogger\AutoLogger-Diagtrack-Listener.etl')
            os.system('reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG DWORD /d 0 /f')

        elif b == 3:
            os.system("powershell Get-AppxPackage *people*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *communicationsapps*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *zunevideo*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *3dbuilder*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *skypeapp*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *solitaire*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *officehub*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *xbox*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *photos*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *maps*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *calculator*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *camera*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *alarms*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *onenote*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *bing*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *soundrecorder*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *windowsphone*| Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *getstarted* | Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *zunemusic* | Remove-AppxPackage")
            os.system("powershell Get-AppxPackage *bingfinance* | Remove-AppxPackage")

        elif b == 4:
            try:
                os.system("taskkill /f /im OneDrive.exe")
                os.system("C:\Windows\SysWOW64\OneDriveSetup.exe /uninstall")
            except:
                os.system("powershell Get-AppxPackage-name* OneDrive | Remove-AppxPackage")

        elif b == 5:
            path_reg = r"SOFTWARE\Policies\Microsoft\Windows Defender"
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path_reg)
                winreg.SetValueEx(key, "DisableAntiSpyware", 0, winreg.REG_DWORD, 1)
            except:
                pass
            finally:
                winreg.CloseKey(key)

    elif a == "3":
        if get_winvers() == "Windows 10 Pro":
            try:
                os.system("slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX")
            except:
                os.system("slmgr /ipk 8N67H-M3CY9-QT7C4-2TR7M-TXYCV")
            os.system("slmgr /skms kms.digiboy.ir")
            os.system("slmgr /ato")

        elif get_winvers() == "Windows 10 Home":
            try:
                os.system("slmgr /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99")
            except:
                os.system("slmgr /ipk 7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH")
            os.system("slmgr /skms kms.digiboy.ir")
            os.system("slmgr /ato")

        elif get_winvers() == "Windows 11 Pro":
            try:
                os.system("slmgr /ipk MH37W-N47XK-V7XM9-C7227-GCQG9")
            except:
                os.system("slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX")
            os.system("slmgr /skms kms.digiboy.ir")
            os.system("slmgr /ato")

        elif get_winvers() == "Windows 11 Home":
            print("Пока нету :(")
            sleep(10)

    main()

if __name__ == "__main__":
    main()
