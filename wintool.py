from time import sleep
from rich import *
import os
import winreg
import subprocess
import ctypes
from ctypes import wintypes
import sys

import ctypes
import subprocess

def set_cmd_window_size(width=120, height=30, buffer_height=9001):
    try:
        kernel32 = ctypes.windll.kernel32
        h_console = kernel32.GetStdHandle(-11)

        class CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("dwSize", ctypes.c_ushort * 2),
                ("dwCursorPosition", ctypes.c_ushort * 2),
                ("wAttributes", ctypes.c_ushort),
                ("srWindow", ctypes.c_short * 4),
                ("dwMaximumWindowSize", ctypes.c_ushort * 2),
                ("wPopupAttributes", ctypes.c_ushort),
                ("bFullscreenSupported", ctypes.c_bool),
                ("ColorTable", ctypes.c_ulong * 16)
            ]

        csbi = CONSOLE_SCREEN_BUFFER_INFOEX()
        csbi.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)

        if kernel32.GetConsoleScreenBufferInfoEx(h_console, ctypes.byref(csbi)):
            csbi.dwSize = (width, buffer_height)
            csbi.srWindow = (0, 0, width - 1, height - 1)
            
            kernel32.SetConsoleScreenBufferInfoEx(h_console, ctypes.byref(csbi))
            print(f"Размер окна: {width}x{height}, буфер: {buffer_height} строк")
        else:
            print("Ошибка: Не удалось изменить размер консоли")
    except Exception as e:
        print(f"Ошибка: {e}")

def winact():
    try:
        result = subprocess.run(['cscript', '//Nologo', os.path.expandvars('%windir%\\system32\\slmgr.vbs'), '/dli'], 
                              capture_output=True, text=True)
        output = result.stdout.lower()
        
        if "licensed" in output or "активирована" in output:
            return "[blue]Activated[/blue]"
        elif "license status: licensed" in output:
            return "[blue]Activated[/blue]"
        else:
            return "[red]Not activated[/red]"
    except Exception as e:
        print(f"Activation check error: {e}")
        return "[red]Error checking activation[/red]"

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
    
    if retcode != 0:
        return "Unknown Windows Version"
    
    major = osvi.dwMajorVersion
    minor = osvi.dwMinorVersion
    product_type = osvi.wProductType

    try:
        reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            edition_id = winreg.QueryValueEx(key, "EditionID")[0] if "EditionID" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else ""
            display_version = winreg.QueryValueEx(key, "DisplayVersion")[0] if "DisplayVersion" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else ""
    except:
        product_name = ""
        edition_id = ""
        display_version = ""

    version_map = {
        (10, 0): "Windows 10" if major == 10 and minor == 0 else "",
        (6, 3): "Windows 8.1",
        (6, 2): "Windows 8",
        (6, 1): "Windows 7",
        (6, 0): "Windows Vista",
        (5, 2): "Windows Server 2003" if product_type == 1 else "Windows XP x64",
        (5, 1): "Windows XP",
        (5, 0): "Windows 2000"
    }

    base_version = version_map.get((major, minor), f"Windows {major}.{minor}")

    if major == 10 and minor == 0:
        if "Pro" in product_name:
            base_version = "Windows 10 Pro"
        elif "Home" in product_name:
            base_version = "Windows 10 Home"
        elif "Enterprise" in product_name:
            base_version = "Windows 10 Enterprise"
        elif "Education" in product_name:
            base_version = "Windows 10 Education"
        elif "LTSC" in product_name:
            base_version = "Windows 10 LTSC"

    if major == 10 and minor >= 0 and osvi.dwBuildNumber >= 22000:
        base_version = base_version.replace("10", "11")
        if "Pro" in product_name:
            base_version = "Windows 11 Pro"
        elif "Home" in product_name:
            base_version = "Windows 11 Home"
        elif "Enterprise" in product_name:
            base_version = "Windows 11 Enterprise"
        elif "Education" in product_name:
            base_version = "Windows 11 Education"

    build_info = f" (Build {osvi.dwBuildNumber}"
    if display_version:
        build_info += f", {display_version}"
    build_info += ")"
    
    if edition_id and edition_id not in base_version:
        base_version += f" {edition_id}"
    
    return base_version + build_info

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
                try:
                    os.system("choco install Discord")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "2":
                try:
                    os.system("choco install telegram")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "3":
                try:
                    os.system("choco install Steam")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "4":
                try:
                    os.system("choco install epicgameslauncher")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "5":
                try:
                    os.system("choco install FireFox")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "6":
                try:
                    os.system("choco install tor-browser")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "7":
                try:
                    os.system("choco install chrome")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "8":
                try:
                    os.system("choco install yandex")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "9":
                try:
                    os.system("choco install opera")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "10":
                try:
                    os.system("choco install brave")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "11":
                try:
                    os.system("choco install vivaldi")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "12":
                try:
                    os.system("choco install 7zip")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "13":
                try:
                    os.system("choco install qbittorrent")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
            elif c == "oo":
                try:
                    other_program = input("choco install  --> ")
                    print('''   [green]Choco already install this program[/green]''')
                    os.system(f"choco install {other_program}")
                except:
                    print('''    [red]ОШИБКА ПРИ УСТАНОВКЕ[/red]''')
                    main()
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
        os.system("cls")
        print()
        if check_admin():
            pass
        else:
            print("[red]ЗАПУСТИ ПРОГРАММУ ОТ ИМЕНИ АДМИНИСТРАТОРА[/red]")
            sleep(10)
            sys.exit()
        print()
        print('''    [yellow]Choose your Window[brown]s(hit)[/brown] version[/yellow]''')
        print()
        print('''    [[blue]1[/blue]] - [yellow]Windows 10 Pro[/yellow]''')
        print('''    [[blue]2[/blue]] - [yellow]Windows 10 Home[/yellow]''')
        print('''    [[blue]3[/blue]] - [yellow]Windows 11 Pro[/yellow]''')
        print('''    [[blue]4[/blue]] - [yellow]Windows 11 Home[/yellow]''')
        print()
        windows_activation = int(input("  --> "))
        if windows_activation == "1":
            try:
                os.system("slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX")
            except:
                os.system("slmgr /ipk 8N67H-M3CY9-QT7C4-2TR7M-TXYCV")
            try:
                os.system("slmgr /skms kms.digiboy.ir")
            except:
                os.system("slmgr /skms zh.us.to")
            os.system("slmgr /ato")

        elif windows_activation == "2":
            try:
                os.system("slmgr /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99")
            except:
                os.system("slmgr /ipk 7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH")
            try:
                os.system("slmgr /skms kms.digiboy.ir")
            except:
                os.system("slmgr /skms zh.us.to")
            os.system("slmgr /ato")

        elif windows_activation == "3":
            try:
                os.system("slmgr /ipk VK7JG-NPHTM-C97JM-9MPGT-3V66T")
            except:
                os.system("slmgr /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX")
            try:
                os.system("slmgr /skms kms.digiboy.ir")
            except:
                os.system("slmgr /skms zh.us.to")
            os.system("slmgr /ato")

        elif windows_activation == "4":
            try:
                os.system("slmgr /ipk YTMG3-N6DKC-DKB77-7M9GH-8HVX7")
            except:
                os.system("slmgr /ipk TX9XD-98N7V-6WMQ6-BX7FG-H8Q99")
            try:
                os.system("slmgr /skms kms.digiboy.ir")
            except:
                os.system("slmgr /skms zh.us.to")
            os.system("slmgr /ato")

            sleep(10)
    main()

if __name__ == "__main__":
    set_cmd_window_size(70, 25, 5000)
    main()
