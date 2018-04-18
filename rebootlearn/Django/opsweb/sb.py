class Student(object):
    
    def __init__(self,id,name,sex,age):
        self.id=id
        self.name=name
        self.sex=sex
        self.age=age
    def prin(self):
        print(self.id+self.name+self.sex+self.age)
c=Student(1,2,3,4)
c.prin()
