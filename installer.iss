[Setup]
AppName=Simulador Lotofacil Pro
AppVersion=12.0
DefaultDirName={autopf}\LotofacilPro
DefaultGroupName=Lotofacil Pro
UninstallDisplayIcon={app}\Simulador Lotofacil Pro.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Release
OutputBaseFilename=LotofacilPro_Installer
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Files]
Source: "dist\Simulador Lotofacil Pro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Simulador Lotofacil Pro"; Filename: "{app}\Simulador Lotofacil Pro.exe"
Name: "{autodesktop}\Simulador Lotofacil Pro"; Filename: "{app}\Simulador Lotofacil Pro.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na Área de Trabalho"; GroupDescription: "Atalhos Adicionais:"

[Run]
Filename: "{app}\Simulador Lotofacil Pro.exe"; Description: "Iniciar o Simulador Lotofacil Pro agora"; Flags: nowait postinstall skipifsilent
