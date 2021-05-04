import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import matplotlib.animation as animation

n=128*10
lim=0.8
t_end=10
record=False

def check_cell(i,j,array):
    neigs=sum(np.array([[1 if 0<=i+di<n and 0<=j+dj<n and (i+di,j+dj)!=(i,j) and array[i+di][j+dj]==True else 0 for di in [-1,0,1]] for dj in [-1,0,1]]).flatten())
    if array[i][j]==True and 1<neigs<4:
        ret=1
    elif array[i][j]==False and neigs==3:
        ret=1
    else:
        ret=0
    return ret

array=[[1 if np.random.random()>lim else 0 for j in range(0,n)] for i in range(0,n)]
history=[array]

fig, ax_lst = plt.subplots()
im = ax_lst.imshow(array)
plt.pause(1)
times=[]

if __name__=='__main__':
    for t in range(0,t_end):
        ts=time.time()
        result=[]
        for i in range(0,n):
            for j in range(0,n):
                result.append(check_cell(i,j,array))
                #next_vals.append(check_cell(i,j,array))
        next_vals=[res for res in result]
        c=0
        array=[[0 for j in range(0,n)] for i in range(0,n)]
        for i in range(0,n):
            for j in range(0,n):
                array[i][j]=next_vals[c]
                c+=1
        times.append(time.time()-ts)
        im.set_data(array) 
        plt.pause(.2)

        if record==True:
            history.append(array)
        print(t)

    print(np.mean(times),np.std(times))

