import numpy as np
import random
from matplotlib import pyplot as plt

e0= 0.001
sigma0= 1
mass0= 1


velocity0 = np.sqrt((2*e0)/mass0)
t0= sigma0*np.sqrt(mass0/(2*e0))

deltaT = 0.001*t0 #0.001/5
iteration = 5000#int(10/deltaT)

boundary =[0,100*sigma0]

n = 100
# positions = np.zeros((n,2))
int_velocity = np.full((n,2),2*velocity0)



def distance(point1, point2):
    return np.linalg.norm(point1 - point2)


int_positions = []
while len(int_positions) < n:
    new_position = np.random.uniform(boundary[0], boundary[1], size=2)
    valid = True
    for existing_position in int_positions:
        if distance(new_position, existing_position) < sigma0:
            valid = False
            break
    if valid:
        int_positions.append(new_position)

for i in range(n):
    angle = random.random()*2*np.pi
    int_velocity[i][0]= int_velocity[i][0]*np.cos(angle) 
    int_velocity[i][1]= int_velocity[i][1]*np.sin(angle)

int_positions= np.array(int_positions)
print(int_positions[:][0])
plt.xlim(0, boundary[1]) 
plt.ylim(0, boundary[1]) 
plt.quiver(int_positions[:, 0], int_positions[:, 1], int_velocity[:, 0], int_velocity[:, 1])

plt.show()

def distance_between (m):
    d= np.zeros((len(m), len(m)))
    for i in range (len(m)):
        for j in range (len(m)):
            if i!=j:
                d[i,j]= distance(m[i],m[j])
    return d

def force (d):
    v= np.zeros((len(d),len(d)))
    for i in range(int(len(d))):
        for j in range (len(d)):
            if d[i][j]>2**(1/6)*sigma0:
                v[i][j]= 48*e0*(2*(sigma0**12/d[i][j]**13) - (0.5*sigma0**6/d[i][j]**7))
            else:
                v[i][j] =0
    return v
def lennard_jones_force(positions):
    forces = np.zeros_like(positions)
    for i in range(n):
        for j in range(i+1, n):
            r = np.linalg.norm(positions[i] - positions[j])
            direction = (positions[j] - positions[i]) / r
            magnitude = 4 * e0 * ((sigma0**12 / r**13) - (sigma0**6 / r**7))
            forces[i] -= magnitude * direction
            forces[j] += magnitude * direction
    return forces

def potential (d):
    v= np.zeros((len(d),len(d)))
    for i in range(int(len(d))):
        for j in range (len(d)):
            if d[i][j]!=0:
                v[i][j]= 4*e0*((sigma0/d[i][j])**12 - (sigma0/d[i][j])**6)
            else:
                v[i][j] =0
    return v

# print(int_velocity)
# print(int_positions)
dp={}
dv={}

dp[0]= int_positions
dv[0]= int_velocity

positions = int_positions
velocity = int_velocity

final_KE=np.zeros((iteration,1))
final_PE=np.zeros((iteration,1))

final_TE=np.zeros((iteration,1))
int_KE=0
int_PE=0
int_TE=0
time_list=[]
temp_time=0
position_list=[]
for t in range (iteration):
    temp_time= temp_time+deltaT
    time_list.append(temp_time)

    nxt_position = np.zeros((n,2))
    nxt_velocity = np.zeros((n,2))
    middle_step =np.zeros((n,2))
    d = distance_between(positions)
    v = lennard_jones_force(positions)

    temp_KE=0
    temp_PE=0
    temp_TE=0
    for i in range (n):
        # temp_KE+= 0.5*mass0*(np.linalg.norm(velocity[i][0]-velocity[i][1]))**2
        temp_KE+= 0.5*mass0*np.sqrt(velocity[i][0]**2+velocity[i][1]**2)**2
        temp_PE+= 0.5*np.sqrt(v[i][0]**2+v[i][1]**2)**2
    
    temp_TE= temp_PE/2+temp_KE
    final_KE[t]=temp_KE
    final_PE[t]=temp_PE
    final_TE[t]=temp_TE



    for i in range(n):
        middle_step[i] = positions[i] + velocity[i]*deltaT/2
    
    force_middle = lennard_jones_force(middle_step)
    
    d_middle= distance_between(middle_step)
    v_middle= force(d_middle)
    for i in range(n):
        # f= np.zeros(1)
        # for j in range(n):
        #     if i!=j:
        #         f += v_middle[i][j]
        # f=f/2
        nxt_velocity[i] = velocity[i]+ force_middle[i]*deltaT/mass0
        nxt_position[i] = middle_step[i]+ nxt_velocity[i]*deltaT/2

        if nxt_position[i][0]< boundary[0]:
            difference = boundary[0] - nxt_position[i][0]
            nxt_position[i][0]= difference
            nxt_velocity[i][0]= - nxt_velocity[i][0]
        if nxt_position[i][0]> boundary[1]:
            difference = nxt_position[i][0] - boundary[1]  
            nxt_position[i][0]= boundary[1] - difference
            nxt_velocity[i][0] = -nxt_velocity[i][0]
            
        if nxt_position[i][1]< boundary[0]:
            difference = boundary[0] - nxt_position[i][1]
            nxt_position[i][1]= difference
            nxt_velocity[i][1]= - nxt_velocity[i][1]
        if nxt_position[i][1]> boundary[1]:
            difference = nxt_position[i][1] - boundary[1]  
            nxt_position[i][1]= boundary[1] - difference
            nxt_velocity[i][1] = -nxt_velocity[i][1]
    positions = nxt_position
    velocity = nxt_velocity
    position_list.append(positions)
    if t%250==0:
        print('iteration',t)
        print('position', positions[:5])
        print("velocity",velocity[:5])

position_list=np.array(position_list)

for i in range(100):
    x = position_list[:, i, 0] 
    y = position_list[:, i, 1]  
    plt.plot(x, y, label=f"Particle {i+1}")
plt.quiver(positions[:, 0], positions[:, 1], velocity[:, 0], velocity[:, 1], color='r')

plt.show()


    # if t%250 ==0:
    #     for i in range (n):
    #         plt.subplot(131)
    #         plt.scatter(int_positions[i][0],int_positions[i][1],color='r')
    #     plt.title(f'inital position of paticles')

    #     for i in range (n):
    #         plt.subplot(132)
    #         plt.scatter(positions[i][0],positions[i][1],color='r')
    #     plt.title(f'position of patricles after iteration:{t} with time step= {deltaT}')
    #     plt.show()

    #     plt.quiver(int_positions[:, 0], int_positions[:, 1], int_velocity[:, 0], int_velocity[:, 1], color='g', label='intial velocity')
    #     plt.quiver(positions[:, 0], positions[:, 1], velocity[:, 0], velocity[:, 1], color='r', label= f'velocity  after iteration:{t}')
    #     plt.legend()
    #     plt.show()       






#----------------final resutl---- above plot shows resutl after every 100 iteration------
# plt.subplot(141)
# plt.quiver(int_positions[:, 0], int_positions[:, 1], int_velocity[:, 0], int_velocity[:, 1])
# plt.subplot(142)
# plt.quiver(positions[:, 0], positions[:, 1], velocity[:, 0], velocity[:, 1])
# plt.show()


# plt.quiver(int_positions[:, 0], int_positions[:, 1], int_velocity[:, 0], int_velocity[:, 1], color='g', label='intial velocity of particles')
# plt.quiver(positions[:, 0], positions[:, 1], velocity[:, 0], velocity[:, 1], color='r', label= f'velocity of particle at iteration:{t}')
# plt.show()



fig, ax = plt.subplots(3,1)
ax[0].plot(time_list, final_KE)
ax[0].set_title('KE')
ax[1].plot(time_list, final_PE)
ax[1].set_title('PE')
ax[2].plot(time_list, final_TE)
ax[2].set_title('TE')
plt.tight_layout()
plt.show()
# print( "final_KE",final_KE[:50])
# print("final pe", final_PE[:50])
# print("final TE", final_TE[:50])

# print(len(final_KE))