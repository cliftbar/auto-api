import os
import sys


platform = sys.platform


def generate():
    os.system(f"conda list --export > conda_requirements_{platform}.txt")
    os.system(f"conda list --explicit > conda_requirements_explicit_{platform}.txt")
    os.system(f"pip freeze > requirements.txt")
    os.system(f"conda env export --name {os.environ['CONDA_DEFAULT_ENV']} --file conda_environment_{platform}.yml")


def install():
    os.system(f"conda install -y --file conda_requirements_{platform}.txt")


def install_explicit():
    os.system(f"conda install -y --file conda_requirements_explicit_{platform}.txt")


def install_environment():
    os.system(f"conda env create --file conda_environment_{platform}.yml")


def install_pip():
    os.system(f"pip install -r requirements.txt")


def print_help():
    print("Usage:")
    print("\t$ python generate_requirements.py [option]")
    print("Options:")
    print("\tgenerate")
    print("\tinstall")
    print("\tinstall-explicit")
    print("\tinstall-pip")
    print("\tinstall-environment (preferred)")


def main():
    task = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"task is {task}")
    if task == "generate":
        generate()
    elif task == "install":
        install()
    elif task == "install-explicit":
        install_explicit()
    elif task == "install-environment":
        install_environment()
    elif task == "install-pip":
        install_pip()
    else:
        print_help()


main()
