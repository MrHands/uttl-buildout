             ___   _____        __  __    __       
     /\ /\  / _ \ /__   \/\  /\/__\/__\  /__\      
    / / \ \/ /_)/   / /\/ /_/ /_\ / \// /_\        
    \ \_/ / ___/   / / / __  //__/ _  \//__        
     \___/\/       \/  \/ /_/\__/\/ \_/\__/        
                                                   
     _____        __          __    ___         __ 
    /__   \/\  /\/__\/\_/\   / /   /___\/\   /\/__\
      / /\/ /_/ /_\  \_ _/  / /   //  //\ \ / /_\  
     / / / __  //__   / \  / /___/ \_//  \ V //__  
     \/  \/ /_/\__/   \_/  \____/\___/    \_/\__/  

Buildout utilities developed for *Up There They Love*.

# Building from source

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg:

    python setup.py install

Create egg and install manually:

    python setup.py bdist_egg
    python -m easy_install -a dist\uttl_buildout-1.0.0-py3.9.egg
