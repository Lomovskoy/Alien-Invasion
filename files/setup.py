from cx_Freeze import setup, Executable

setup(
    name = "alien_invasion",
    version = "1.0",
    description = "Alien Invasion",
    executables = [Executable("alien_invasion.py")]
)
