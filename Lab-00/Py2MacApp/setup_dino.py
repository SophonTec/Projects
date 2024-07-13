import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        './src/dino/dino_leaderboard.py',
        '--onedir',
        '--windowed',
        '--add-data=./src/dino/Assets:Assets',
        '--icon=./src/dino/dino-icon.icns',
        '--log-level=DEBUG',
        '--name=DinoGame',
    ]
)
