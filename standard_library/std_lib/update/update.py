def update_pip_packages():
    import pkg_resources
    from subprocess import call

    packages = [dist.project_name for dist in pkg_resources.working_set]
    call("pip install --upgrade " + ' '.join(packages), shell=True)
    print("Successfully updated pip packages.")
    call("pip freeze > requirements.txt", shell=True)
    print("Successfully updated requirements.txt")

def update_pip_manager():
    #import pkg_resources
    from subprocess import call

    #packages = [dist.project_name for dist in pkg_resources.working_set]
    call("python -m pip install --upgrade pip", shell=True)
    print("Successfully updated pip.")
