; ──────────────────────────────────────────────────────────────────────────────
;  PrayerTime Scheduler — Inno Setup Installer Script
;  Publisher: Kesb Tech
; ──────────────────────────────────────────────────────────────────────────────
;  Prerequisites:
;    1. Build the exe first:
;       py -m PyInstaller --onefile --windowed --icon=assets/icon.ico
;           --name="PrayerTimeScheduler" --add-data="assets;assets" main.py
;    2. Install Inno Setup from https://jrsoftware.org/isinfo.php
;    3. Open this .iss file in Inno Setup Compiler and click "Compile".
;       Output will be in installer_output/PrayerTimeScheduler_Setup.exe
; ──────────────────────────────────────────────────────────────────────────────

#define AppName      "PrayerTime Scheduler"
#define AppVersion   "1.0.0"
#define AppPublisher "Kesb Tech"
#define AppURL       "https://kesbtech.com"
#define AppExeName   "PrayerTimeScheduler.exe"

[Setup]
AppId={{B7E8F2A4-3C1D-4A5F-9E6B-8D7C0F2A1B3E}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=PrayerTimeScheduler_Setup_v{#AppVersion}
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";    Description: "Create a &desktop shortcut";    GroupDescription: "Additional shortcuts:"; Flags: unchecked
Name: "startupentry";   Description: "Launch at Windows &startup";    GroupDescription: "System integration:";   Flags: unchecked

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\icon.ico";    DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\icon.png";    DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\assets\icon.ico"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

; Desktop (optional)
Name: "{commondesktop}\{#AppName}";   Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon

[Registry]
; Auto-start (optional)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueType: string; ValueName: "{#AppName}"; \
    ValueData: """{app}\{#AppExeName}"""; Flags: uninsdeletevalue; Tasks: startupentry

[Run]
Filename: "{app}\{#AppExeName}"; \
    Description: "Launch {#AppName}"; \
    Flags: nowait postinstall skipifsilent

[UninstallRun]
; Make sure the app is closed before uninstalling
Filename: "taskkill"; Parameters: "/F /IM {#AppExeName}"; Flags: runhidden

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
