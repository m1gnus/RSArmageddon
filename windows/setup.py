from cx_Freeze import setup, Executable

setup(
    name="rsarmageddon",
    version="2.0.1",
    description="RSA cryptography and cryptoanalysis toolkit",
    options={
        "build_exe": {
            "excludes": ["tkinter", "test"],
            "packages": ["rsarmageddon", "colorama"]
        }
    },
    executables=[
        Executable("entrypoint.py", target_name="rsarmageddon")
    ])
