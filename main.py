# Importing the pulp library
import pulp
import math

# -* - coding : utf - 8 -* -
"""
Created on Tue Aug 23  15: 43 : 28 2022
@author : Kelvin Osei Poku
"""
# Solving the Nurse Scheduling Problem
# Number of nurses
n = 30
# A list for number of shifts
jj = [1, 2]  # Index of shifts
kk = [1, 2, 3, 4, 5, 6, 7]  # index of days
ii = [nurses for nurses in range(n)]
# The optimal number of nurses need are calculated here
off_nurses = math.ceil(n / 7)  # Round value up for whole numbers
total_working_nurses = n - off_nurses
a1 = math.ceil(
    total_working_nurses / 2)  # Divide available working days into two   Number of nurses required for day shift each day
a2 = total_working_nurses - a1  # Number of nurses required for night shift each day
# FOR 7 -> 282.0, 0.01 seconds. 14-> 564 0.01s  35-> 1410 0.02s 100-> 30-> 1175
# Matrix for nurse i preferences for a shift j on day k
f = [1, 0, 1, 1, 1, 5, 9, 9]

# Creating the Lp Problem with title ; " Nurse Scheduling Problem "
model = pulp.LpProblem("Nurse_Scheduling_Problem", sense=pulp.LpMaximize)
# Defining variables
# Which is 1 when nurse i is assigned to shift j on day k , 0 otherwise
x = pulp.LpVariable.dicts("x", [(i, j, k) for i in ii for j in jj for k in kk], 0, 1, 'Binary')
# objective function
# Our objective is to maximize the nurse ’s preferences for a shift j on
# a day k
model += pulp.lpSum(f[k] * x[(i, j, k)]
                    for k in kk
                    for j in jj
                    for i in ii
                    )
# Constraint 1
# Each nurse must be scheduled for at most one shift each day
for i in ii:
    for k in kk:
        model += pulp.lpSum(x[(i, j, k)] for j in jj) <= 1
# Constraint 2
# No nurse may be scheduled to work a night shift followed immediately by a day shift
for k in range(1, len(kk)):
    for i in ii:
        model += x[(i, 2, k)] + x[(i, 1, k + 1)] <= 1
# Constraint 3
# Each nurse must have at most one day - off in the week
for i in ii:
    model += pulp.lpSum(x[(i, j, k)] for j in jj for k in kk) <= 6
# ................................................
# Constraint 4
# Nurses assigned each morning should be equal to the number of nurses
# needed for day
# shifts each day which we assume to be constant for all the days
for k in kk:
    model += pulp.lpSum(x[(i, 1, k)] for i in ii) == a1
# Constraint 5
# Nurses assigned each night should be EQUAL  to the number of
# nurses needed for a night
for k in kk:
    model += pulp.lpSum(x[(i, 2, k)] for i in ii) == a2

# Solution
solution = model.solve()

# Generating the status of the solution
print(" The solution has a status of ", solution)
print(" This implies that it is ", pulp.LpStatus[model.status])
print('')
if solution != 1:
    raise Exception('Optimization not feasible. Adjust parameters')
f = open("./schedule.txt", "a+")
# Printing the values for each decision variable
print(" The values of the decision variables are : ")
for var in x:
    var_value = x[var].varValue
    print(x[var], " = ", var_value)
    result = str(x[var]) + " = " + str(var_value)
    f.write(str(result) + "\n")
    # Printing the value of the objective
    obj = model.objective.value()
# Printing the value of the objective
obj = model.objective.value()
print('The cost of the scheduling is', obj)
f.close()

if __name__ == '__main__':
    pass
