python -m PyInstaller "Simulador Lotofacil Pro.spec" -y
if ($?) {
    & "C:\Users\berge\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
    if ($?) {
        git add .
        git commit -m "fix(engine): resolve crash do numpy no logger e inclui sklearn no build p/ xgboost"
        git push -f
    }
}
