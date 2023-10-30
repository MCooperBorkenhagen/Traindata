# This line allows us to import the Traindata class from the traindata module 
# without having to specify the file name that the class is located in. 
# For example, we can import the Traindata class like this:
# from traindata import Traindata # (which is how it was before)
# instead of like this:
# from traindata.core import Traindata # (which is how it would need to be with the project structure)
from .core import Traindata
