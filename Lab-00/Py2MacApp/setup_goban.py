import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        './src/goban/goban.py',
        '--onefile',
        '--windowed',
        '--icon=./src/goban/goban.ico'
    ]
)
