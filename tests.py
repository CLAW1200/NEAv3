#create a list bigger then 32bit int
object = 1
limitTest = 2**32
objectList = [object] * limitTest

print(objectList)