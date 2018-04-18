# -*-coding:utf-8-*-

arr1 = [1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,45,33,45]
count = len(arr1)
for x in range(0, count):
    for y in range(x + 1, count):
        if arr1[x] < arr1[y]:
            arr1[x], arr1[y] = arr1[y], arr1[x]
print "top1 = %d, top2 = %d" % (arr1[0], arr1[1])

arr2 = [1,2,3,2,12,3,1,3,21,2,2,3,4111,22,3333,444,111,4,5,777,65555,45,33,45]
fir = 0
sec = 0
for x in arr2:
	if x > fir:
		fir = x
for x in arr2:
	if x > sec and x < fir:
		sec = x
print "top1 = %d, top2 = %d" % (fir, sec)
