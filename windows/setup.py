from cx_Freeze import setup, Executable
import rsarmageddon

setup(
    name="rsarmageddon",
    version=rsarmageddon.__version__,
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
