import time

begin=time.time()
answer = 1
while(True):
    test=answer
    for i in range(1,10):
        test=test/2-1
    if test==1:
        break
    else:
        answer+=1
print(answer)
print(time.time()-begin)