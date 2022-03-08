import collections

def ini():
    capacity = (8,5,3)
    water = (8,0,0)
    
def objetivo(dicc, i):
    if dicc[i] == [4, 4, 0]:
        return True
    else:
        return False
   
def bfs(dicc, root):
    i = 1
    solucion = {}
   # queue = collections.deque([root])
    
    solucion.update({dicc[i]})
    while objetivo == False:
        i+=i
    if objetivo == True:
        for v in solucion.values():
            print (v)
        
    #while queue:
     #   vertex= queue.popleft()
      #  solucion.add(vertex)
    #for i in dicc[vertex]:
     #   if i not in solucion:
      #      queue.append(i)
    
if __name__=='__main__':  
    dicc = {1: [8, 0, 0], 2 : [3, 5, 0], 3 : [3, 2, 3],
           4: [6, 2, 0], 5 : [6, 0, 2], 6 : [1, 5, 2],
           7: [1, 4, 3], 8 : [4, 4, 0]}
    bfs(dicc, 1)


