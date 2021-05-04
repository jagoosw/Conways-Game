import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time, multiprocessing, pickle
import matplotlib.animation as animation

n=128*10
lim=.8
t_end=10
record=False
num_cpu=16

if num_cpu<1 or num_cpu%2!=0:
    raise RuntimeError('Number of CPUs must be at least 4 and must be even')

if n%2!=0:
    raise RuntimeError('n must be even because I am lazy')

if n%(num_cpu**.5)!=0:
    raise RuntimeError('n must be a muiltiple of num_cpu%.5 because I am lazy')
    
def check_cell(i,j,array):
    neigs=sum(np.array([[1 if 0<=i+di<n and 0<=j+dj<n and (i+di,j+dj)!=(i,j) and array[i+di][j+dj]==True else 0 for di in [-1,0,1]] for dj in [-1,0,1]]).flatten())
    if array[i][j]==True and 1<neigs<4:
        ret=1
    elif array[i][j]==False and neigs==3:
        ret=1
    else:
        ret=0
    return ret

def check_segment(*kwargs):#i_range,j_range,array
    kwargs=kwargs[0]
    i_range=kwargs['i_range']
    j_range=kwargs['j_range']
    seg_results=[[0 for j in j_range] for i in i_range]
    for ind_i,i in enumerate(i_range):
        for ind_j,j in enumerate(j_range):
            seg_results[ind_i][ind_j]=check_cell(i,j,kwargs['array'])
    return kwargs['i_range'],kwargs['j_range'],seg_results


array=[[1 if np.random.random()>lim else 0 for j in range(0,n)] for i in range(0,n)]
history=[array]

fig, ax_lst = plt.subplots()
im = ax_lst.imshow(array)
plt.pause(1)
times=[]

if __name__=='__main__':
    pool = multiprocessing.Pool() 
    for t in range(0,t_end):
        ts=time.time()
        result=[]
        i_range=range(0,n)
        j_range=range(0,n)
        for i_sel in range(0,int(num_cpu**.5)):
            for j_sel in range(0,int(num_cpu**.5)):
                i_seg=i_range[int(i_sel*len(i_range)/(num_cpu**.5)):int((i_sel+1)*len(i_range)/(num_cpu**.5))]
                j_seg=j_range[int(j_sel*len(j_range)/(num_cpu**.5)):int((j_sel+1)*len(j_range)/(num_cpu**.5))]
                args={'i_range':i_seg,'j_range':j_seg,'array':array}
                result.append(pool.map_async(check_segment,(args,)))
        result=[res.get()[0] for res in result]
        c=0
        array=[[0 for j in range(0,n)] for i in range(0,n)]
        for res in result:
            for ind_i,i in enumerate(res[0]):
                for ind_j,j in enumerate(res[1]):
                    array[i][j]=res[2][ind_i][ind_j]
        times.append(time.time()-ts)
        im.set_data(array) 
        plt.pause(.1)

        if record==True:
            history.append(array)
        print(t)

    print(np.mean(times),np.std(times))

if record == True:
    with open('%s_%s.obj'%(n,time.time()), 'wb') as f:
        pickle.dump(history,f)