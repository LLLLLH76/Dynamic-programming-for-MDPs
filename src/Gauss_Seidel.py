import numpy as np

def draw():
    for i in range(1,11):
        for j in range(1,11):
            if list(A[i][j])==[1,1,1,1]:
                print("+",end='   ')
            elif list(A[i][j])==[1,0,0,0]:
                print("↑",end='   ')
            elif list(A[i][j])==[0,1,0,0]:
                print("↓",end='   ')
            elif list(A[i][j])==[0,0,1,0]:
                print("←",end='   ')
            elif list(A[i][j])==[0,0,0,1]:
                print("→",end='   ')
            elif list(A[i][j])==[1,1,0,0]:
                print("|",end='   ')
            elif list(A[i][j])==[1,0,1,0]:
                print("┘",end='   ')
            elif list(A[i][j])==[1,0,0,1]:
                print("L",end='   ')
            elif list(A[i][j])==[0,1,1,0]:
                print("┐",end='   ')
            elif list(A[i][j])==[0,1,0,1]:
                print("Γ",end='   ')
            elif list(A[i][j])==[0,0,1,1]:
                print("一",end=' ')
            elif list(A[i][j])==[1,1,1,0]:
                print("⊣",end='   ')
            elif list(A[i][j])==[1,1,0,1]:
                print("⊢",end='   ')
            elif list(A[i][j])==[1,0,1,1]:
                print("⊥",end='   ')
            elif list(A[i][j])==[0,1,1,1]:
                print("T",end='   ')
        print()
    for i in range(1,11):
        for j in range(1,11):
            if U[i][j]>=0 and U[i][j]<10:
                print(format(U[i][j], '.3f'),end='  ')
            elif U[i][j]>=10 or U[i][j]<0 and U[i][j]>-10:
                print(format(U[i][j], '.2f'),end='  ')
            elif U[i][j]<=10:
                print(format(U[i][j], '.1f'),end='  ')
        print()
    print()

if __name__ == '__main__':
    gamma=0.9
    A=np.array([1]*144*4).reshape(12,12,4)
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
    iteration = 0
    max_iteration=100
    U=np.array([[0.0]*144]).reshape(12,12)
    old_U=np.array([[0.0]*144]).reshape(12,12)
    while iteration < max_iteration:
        #print('iteration: '+str(iteration))
        k = iteration
        for statex in range(1,11):
            for statey in range(1,11):
                if (statex==8 and statey==9) or (statex==3 and statey==8):
                    U[statex][statey]=R[statex][statey][0]
                    continue
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
                for action in range(4):
                    A[statex][statey][action]=1 if abs(Q[action]-Q[Q.argmax()])<1e-5 else 0
                U[statex][statey]=Q[Q.argmax()]
        for x in range(1,11):
            U[0][x]=U[1][x]
            U[11][x]=U[10][x]
            U[x][0]=U[x][1]
            U[x][11]=U[x][10]
        # infinite norm
        if max(abs((U.reshape(1,-1)-old_U.reshape(1,-1))[0].max()),abs((U.reshape(1,-1)-old_U.reshape(1,-1))[0].min())) < 1e-5:
            break
        # 避免浅拷贝
        old_U=U.copy()
        iteration+=1
    draw()
    print('total number of iterations: '+str(iteration))
    print()