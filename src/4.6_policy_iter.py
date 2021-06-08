import numpy as np

def draw(iteration):
    for i in range(1,11):
        for j in range(1,11):
            if (A[i][j])==0:
                print("↑",end='  ')
            elif (A[i][j])==1:
                print("↓",end='  ')
            elif (A[i][j])==2:
                print("←",end='  ')
            elif (A[i][j])==3:
                print("→",end='  ')
        print()
    for i in range(1,11):
        for j in range(1,11):
            if U[iteration][i][j]>=0 and U[iteration][i][j]<10:
                print(format(U[iteration][i][j], '.3f'),end='  ')
            elif U[iteration][i][j]>=10 or U[iteration][i][j]<0 and U[iteration][i][j]>-10:
                print(format(U[iteration][i][j], '.2f'),end='  ')
            elif U[iteration][i][j]<=10:
                print(format(U[iteration][i][j], '.1f'),end='  ')
        print()
    print()

max_iteration = 50
U=np.array([[0.0]*144*(max_iteration+1)]).reshape(max_iteration+1,12,12)

def evaluate(A,gamma):
    iteration = 0
    while iteration < max_iteration:
        k = iteration
        for statex in range(1,11):
            for statey in range(1,11):
                if (statex==8 and statey==9) or (statex==3 and statey==8):
                    U[k+1][statex][statey]=R[statex][statey][0]
                    continue
                Q=np.array([])
                action = A[statex][statey]
                if action==0: # up
                    sum=0.7*U[k][statex-1][statey]+0.1*U[k][statex+1][statey]+0.1*U[k][statex][statey+1]+0.1*U[k][statex][statey-1]
                elif action==1: # down
                    sum=0.7*U[k][statex+1][statey]+0.1*U[k][statex-1][statey]+0.1*U[k][statex][statey+1]+0.1*U[k][statex][statey-1]
                elif action==2: # left
                    sum=0.7*U[k][statex][statey-1]+0.1*U[k][statex+1][statey]+0.1*U[k][statex-1][statey]+0.1*U[k][statex][statey+1]
                elif action==3: # right
                    sum=0.7*U[k][statex][statey+1]+0.1*U[k][statex+1][statey]+0.1*U[k][statex-1][statey]+0.1*U[k][statex][statey-1]
                U[k+1][statex][statey]=R[statex][statey][action]+gamma*sum
        for x in range(1,11):
            U[k+1][0][x]=U[k+1][1][x]
            U[k+1][11][x]=U[k+1][10][x]
            U[k+1][x][0]=U[k+1][x][1]
            U[k+1][x][11]=U[k+1][x][10]
        iteration+=1
    return U[-1],iteration

def policy_iter(gamma):
    k=0
    max_iteration = 50
    A=np.array([[0]*144*(max_iteration+1)]).reshape(max_iteration+1,12,12)
    while k<max_iteration:
        U,iteration=evaluate(A[k],gamma)
        for statex in range(1,11):
            for statey in range(1,11):
                Q=np.array([])
                for action in range(4):
                    if action==0: # up
                        sum=0.7*U[statex-1][statey]+0.1*U[statex+1][statey]+0.1*U[statex][statey+1]+0.1*U[statex][statey-1]
                    elif action==1: # down
                        sum=0.7*U[statex+1][statey]+0.1*U[statex-1][statey]+0.1*U[statex][statey+1]+0.1*U[statex][statey-1]
                    elif action==2: # left
                        sum=0.7*U[statex][statey-1]+0.1*U[statex+1][statey]+0.1*U[statex-1][statey]+0.1*U[statex][statey+1]
                    elif action==3: # right
                        sum=0.7*U[statex][statey+1]+0.1*U[statex+1][statey]+0.1*U[statex-1][statey]+0.1*U[statex][statey-1]
                    Q=np.append(Q,R[statex][statey][action]+gamma*sum)
                A[k+1][statex][statey]=Q.argmax()
        k+=1
        if (A[k]-A[k-1]).sum()==0:
            break
    print('total number of iterations: '+str(k))
    return A[k-1],iteration
    
if __name__ == '__main__':
    gamma=0.9
    R=np.array([0.0]*144*4).reshape(12,12,4)
    R[1][1][0]=R[1][1][2]=R[1][10][0]=R[1][10][3]=R[10][1][1]=R[10][1][2]=R[10][10][1]=R[10][10][3]=-0.8
    R[1][1][1]=R[1][1][3]=R[1][10][1]=R[1][10][2]=R[10][1][0]=R[10][1][3]=R[10][10][0]=R[10][10][2]=-0.2
    for i in range(2,10):
        R[1][i][0]=R[i][10][3]=R[i][1][2]=R[10][i][1]=-0.7
        R[1][i][1]=R[1][i][2]=R[1][i][3]=R[i][10][1]=R[i][10][2]=R[i][10][0]=R[i][1][1]=R[i][1][0]=R[i][1][3]=R[10][i][0]=R[10][i][2]=R[10][i][3]=-0.1
    for i in range(4):
        R[5][4][i]=-5
        R[8][4][i]=-10
        R[8][9][i]=10
        R[3][8][i]=3
    A,iteration=policy_iter(gamma)
    draw(iteration)