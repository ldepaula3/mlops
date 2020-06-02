from petshop_model import *

#res = scoreModel("Adult", "Dog", "Gold Fur", "Normal", "No", "Winter", "Male", "Sterilized at Intake", "Public Assist", 3)
res = scoreModel("Adult", "Dog", "Gold Fur", "Normal", "No", "Winter", "Male", "Sterilized at Intake", "Public Assist")
    
if res not in [0.0, 1.0]:
    raise Exception('Error executing program')
else:
    print(" The probability is: " + str(res))
