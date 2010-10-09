# Auto-generated by EclipseNSIS Script Wizard
# 06-oct-2010 22:26:27

Name Esquipulas

# General Symbol Definitions
!define REGKEY "SOFTWARE\$(^Name)"
!define VERSION 1.0
!define COMPANY "Cusuco Soft"
!define URL ""

# MultiUser Symbol Definitions
!define MULTIUSER_EXECUTIONLEVEL Highest
!define MULTIUSER_MUI
!define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_KEY "${REGKEY}"
!define MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_VALUENAME MultiUserInstallMode
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!define MULTIUSER_INSTALLMODE_INSTDIR Esquipulas
!define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_KEY "${REGKEY}"
!define MULTIUSER_INSTALLMODE_INSTDIR_REGISTRY_VALUE "Path"

# MUI Symbol Definitions
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_STARTMENUPAGE_REGISTRY_ROOT HKLM
!define MUI_STARTMENUPAGE_REGISTRY_KEY ${REGKEY}
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULTFOLDER Esquipulas
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

# Included files
!include MultiUser.nsh
!include Sections.nsh
!include MUI2.nsh

# Variables
Var StartMenuGroup

# Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ..\esquipulaspy\LICENSE
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MULTIUSER_PAGE_INSTALLMODE
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuGroup
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Installer languages
!insertmacro MUI_LANGUAGE SpanishInternational

# Installer attributes
OutFile setup.exe
InstallDir Esquipulas
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion 1.0.0.0
VIAddVersionKey ProductName Esquipulas
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey FileVersion "${VERSION}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show

# Installer sections
Section -Main SEC0000
    SetOutPath $INSTDIR
    SetOverwrite on
    File ..\esquipulaspy\dist\_hashlib.pyd
    File ..\esquipulaspy\dist\bz2.pyd
    File ..\esquipulaspy\dist\esquipulas.exe
    File ..\esquipulaspy\dist\libgcc_s_dw2-1.dll
    File ..\esquipulaspy\dist\libmySQL.dll
    File ..\esquipulaspy\dist\mingwm10.dll
    File ..\esquipulaspy\dist\phonon4.dll
    File ..\esquipulaspy\dist\PyQt4.QtCore.pyd
    File ..\esquipulaspy\dist\PyQt4.QtGui.pyd
    File ..\esquipulaspy\dist\PyQt4.QtNetwork.pyd
    File ..\esquipulaspy\dist\PyQt4.QtSql.pyd
    File ..\esquipulaspy\dist\PyQt4.QtWebKit.pyd
    File ..\esquipulaspy\dist\python26.dll
    File ..\esquipulaspy\dist\QtCore4.dll
    File ..\esquipulaspy\dist\QtGui4.dll
    File ..\esquipulaspy\dist\QtHelp4.dll
    File ..\esquipulaspy\dist\QtNetwork4.dll
    File ..\esquipulaspy\dist\QtSql4.dll
    File ..\esquipulaspy\dist\QtWebKit4.dll
    File ..\esquipulaspy\dist\select.pyd
    File ..\esquipulaspy\dist\sip.pyd
    File ..\esquipulaspy\dist\unicodedata.pyd
    File ..\esquipulaspy\dist\w9xpopen.exe
    File ..\esquipulaspy\dist\logo.ico
    File /r ..\esquipulaspy\dist\sqldrivers
    File /r ..\esquipulaspy\dist\translations
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

Section Contabilidad SEC0001
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    createShortCut $SMPROGRAMS\$StartMenuGroup\contabilidad.lnk $INSTDIR\esquipulas.exe --contabilidad
    WriteRegStr HKLM "${REGKEY}\Components" Contabilidad 1
SectionEnd

Section "Compras e Inventario" SEC0002
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    createShortCut $SMPROGRAMS\$StartMenuGroup\inventario.lnk $INSTDIR\esquipulas.exe --inventario
    WriteRegStr HKLM "${REGKEY}\Components" "Compras e Inventario" 1
SectionEnd

Section Caja SEC0003
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    createShortCut $SMPROGRAMS\$StartMenuGroup\caja.lnk $INSTDIR\esquipulas.exe --caja
    WriteRegStr HKLM "${REGKEY}\Components" Caja 1
SectionEnd

Section Ayuda SEC0004
    SetOutPath $INSTDIR
    SetOverwrite on
    File ..\esquipulaspy\dist\assistant.exe
    File ..\esquipulaspy\dist\doc.qch
    File ..\esquipulaspy\dist\esquipulashelpcollection.qhc
    File ..\esquipulaspy\dist\qt.conf
    File ..\esquipulaspy\dist\QtAssistantClient4.dll
    File ..\esquipulaspy\dist\QtCLucene4.dll
    File ..\esquipulaspy\dist\QtXml4.dll
    File ..\esquipulaspy\dist\QtXmlPatterns4.dll
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    createShortCut "$SMPROGRAMS\$StartMenuGroup\Ayuda.lnk" "$INSTDIR\assistant.exe" "-collectionFile '$INSTDIR\esquipulashelpcollection.qhc'" $INSTDIR\logo.ico
    WriteRegStr HKLM "${REGKEY}\Components" Ayuda 1
SectionEnd

Section -post SEC0005
    WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
    SetOutPath $INSTDIR
    WriteUninstaller $INSTDIR\uninstall.exe
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    CreateShortcut "$SMPROGRAMS\$StartMenuGroup\Uninstall $(^Name).lnk" $INSTDIR\uninstall.exe
    !insertmacro MUI_STARTMENU_WRITE_END
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayName "$(^Name)"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayVersion "${VERSION}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" Publisher "${COMPANY}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayIcon $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" UninstallString $INSTDIR\uninstall.exe
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoModify 1
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoRepair 1
SectionEnd

# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

# Uninstaller sections
!macro DELETE_SMGROUP_SHORTCUT NAME
    Push "${NAME}"
    Call un.DeleteSMGroupShortcut
!macroend

Section /o -un.Ayuda UNSEC0004
    !insertmacro DELETE_SMGROUP_SHORTCUT Ayuda
    Delete /REBOOTOK $INSTDIR\QtXmlPatterns4.dll
    Delete /REBOOTOK $INSTDIR\QtXml4.dll
    Delete /REBOOTOK $INSTDIR\QtCLucene4.dll
    Delete /REBOOTOK $INSTDIR\QtAssistantClient4.dll
    Delete /REBOOTOK $INSTDIR\qt.conf
    Delete /REBOOTOK $INSTDIR\esquipulashelpcollection.qhc
    Delete /REBOOTOK $INSTDIR\doc.qch
    Delete /REBOOTOK $INSTDIR\assistant.exe
    Delete /REBOOTOK $INSTDIR\assistant.bat
    DeleteRegValue HKLM "${REGKEY}\Components" Ayuda
SectionEnd

Section /o -un.Caja UNSEC0003
    !insertmacro DELETE_SMGROUP_SHORTCUT Caja
    DeleteRegValue HKLM "${REGKEY}\Components" Caja
SectionEnd

Section /o "-un.Compras e Inventario" UNSEC0002
    !insertmacro DELETE_SMGROUP_SHORTCUT Inventario
    DeleteRegValue HKLM "${REGKEY}\Components" "Compras e Inventario"
SectionEnd

Section /o -un.Contabilidad UNSEC0001
    !insertmacro DELETE_SMGROUP_SHORTCUT Contabilidad
    DeleteRegValue HKLM "${REGKEY}\Components" Contabilidad
SectionEnd

Section /o -un.Main UNSEC0000
    RmDir /r /REBOOTOK $INSTDIR
    RmDir /r /REBOOTOK $INSTDIR
    Delete /REBOOTOK $INSTDIR\w9xpopen.exe
    Delete /REBOOTOK $INSTDIR\unicodedata.pyd
    Delete /REBOOTOK $INSTDIR\sip.pyd
    Delete /REBOOTOK $INSTDIR\select.pyd
    Delete /REBOOTOK $INSTDIR\QtWebKit4.dll
    Delete /REBOOTOK $INSTDIR\QtSql4.dll
    Delete /REBOOTOK $INSTDIR\QtNetwork4.dll
    Delete /REBOOTOK $INSTDIR\QtHelp4.dll
    Delete /REBOOTOK $INSTDIR\QtGui4.dll
    Delete /REBOOTOK $INSTDIR\QtCore4.dll
    Delete /REBOOTOK $INSTDIR\python26.dll
    Delete /REBOOTOK $INSTDIR\PyQt4.QtWebKit.pyd
    Delete /REBOOTOK $INSTDIR\PyQt4.QtSql.pyd
    Delete /REBOOTOK $INSTDIR\PyQt4.QtNetwork.pyd
    Delete /REBOOTOK $INSTDIR\PyQt4.QtGui.pyd
    Delete /REBOOTOK $INSTDIR\PyQt4.QtCore.pyd
    Delete /REBOOTOK $INSTDIR\phonon4.dll
    Delete /REBOOTOK $INSTDIR\mingwm10.dll
    Delete /REBOOTOK $INSTDIR\library.zip
    Delete /REBOOTOK $INSTDIR\libmySQL.dll
    Delete /REBOOTOK $INSTDIR\libgcc_s_dw2-1.dll
    Delete /REBOOTOK $INSTDIR\esquipulas.exe
    Delete /REBOOTOK $INSTDIR\bz2.pyd
    Delete /REBOOTOK $INSTDIR\_hashlib.pyd
    DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd

Section -un.post UNSEC0005
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\Uninstall $(^Name).lnk"
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue HKLM "${REGKEY}" StartMenuGroup
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
    DeleteRegKey /IfEmpty HKLM "${REGKEY}"
    RmDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RmDir /REBOOTOK $INSTDIR
    Push $R0
    StrCpy $R0 $StartMenuGroup 1
    StrCmp $R0 ">" no_smgroup
no_smgroup:
    Pop $R0
SectionEnd

# Installer functions
Function .onInit
    InitPluginsDir
    !insertmacro MULTIUSER_INIT
FunctionEnd


# Uninstaller functions
Function un.onInit
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuGroup
    !insertmacro MULTIUSER_UNINIT
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
    !insertmacro SELECT_UNSECTION Contabilidad ${UNSEC0001}
    !insertmacro SELECT_UNSECTION "Compras e Inventario" ${UNSEC0002}
    !insertmacro SELECT_UNSECTION Caja ${UNSEC0003}
    !insertmacro SELECT_UNSECTION Ayuda ${UNSEC0004}
FunctionEnd

Function un.DeleteSMGroupShortcut
    Exch $R1 ;NAME
    Push $R2
    StrCpy $R2 $StartMenuGroup 1
    StrCmp $R2 ">" no_smgroup
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\$R1.lnk"
no_smgroup:
    Pop $R2
    Pop $R1
FunctionEnd
