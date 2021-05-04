using PyCall,Statistics,Dates
@pyimport matplotlib.pyplot as plt

function check_cell(i,j,array)
    total=0
    for di in -1:1
        for dj in -1:1
            if (0<i+di<=n && 0<j+dj<=n && (i+di,j+dj)!=(i,j))
                total+=array[i+di,j+dj]
            end
        end
    end
    if array[i,j]==1 && 1<total<4
        live=1
    elseif array[i,j]==0 && total==3
        live=1
    else
        live=0
    end
    return live
end

n=128*100
lim=0.8
t_end=2

array=rand(Float64, (n,n))

#I'm sure this isn't the correct way todo this
Threads.@threads for i in 1:n
    Threads.@threads for j in 1:n
        array[i,j]=round(array[i,j])
    end
end

fig, ax_lst = plt.subplots()
im = ax_lst.imshow(array)
plt.pause(0.0001)

times=[]

for t in 1:t_end
    new_array=Array{Int, 2}(undef, n, n)
    ts=Dates.value(Dates.now())
    Threads.@threads for i in 1:n
        Threads.@threads for j in 1:n
            #tried just multithreading the outer loop and it made no difference 
            #(i.e. not being slowed down by the dispatch like in python)
            #deminishing returns are seen e.g. 0.24s for n=128 and threads=16 but only 0.25s for n=128 and threads=4
            new_array[i,j]=check_cell(i,j,array)
        end
    end
    push!(times,Dates.value(Dates.now())-ts)
    global array=new_array
    im.set_data(array) 
    plt.pause(.0001)
    println(t)
end
println(mean(times)/1000,",",std(times)/1000)