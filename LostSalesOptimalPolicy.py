"""
    
    Optimal Policy calculation for Zipkin (2008) lost sales model.
    
    This is the optimal policy for a lead time of L=1
    Assume c=0
    Assume zero salvage value, so terminal cost is 0
"""

import scipy.stats as sp


class OptimalPolicy():


    def __init__(self, periods, holding_cost, penalty_cost, discount_factor, demand_rate, demand_truncation, state_truncation):

        self.T = periods
        self.h = holding_cost
        self.p = penalty_cost
        self.gamma = discount_factor
        self.lam = demand_rate
        self.max_d = demand_truncation
        self.max_x = state_truncation

        self.max_q = demand_truncation # Cap the decision space by the maximum demand faced (if we think about it this makes sense)

        self.demand_val, self.demand_pmf = self.gen_demand()

        self.optimal_pol  = []
        self.V = []

        ###
        # Pre-processing
        ###

        # Generate the state space
        self.state_space = [x for x in range(self.max_x)]
        self.state_space_size = len(self.state_space) # size of the state space

        self.G = {}

        for idx,x in enumerate(self.state_space):        
            print('Pre-calculating Cost Function: {}/{}'.format(idx+1,self.state_space_size), end='\r')
            self.G[x] = self.calculate_period_cost(x)
        print('\n')

        # Append terminal states
        for idx,x in enumerate(self.state_space):        
            print('Appending Terminal States: {}/{}'.format(idx+1,self.state_space_size), end='\r')
            self.V.append((x, 0))
        print('\n')
        print('Done!')

    

    def gen_demand(self):
        vals = [i for i in range(self.max_d)]
        pmf = [sp.poisson(self.lam).pmf(v) for v in vals]

        return vals, pmf
    
    def calculate_period_cost(self,x):

        # Keep track of the expectation (period cost)
        Exp = 0

        # Discretise the expectation 
        for (d,d_pmf) in zip(self.demand_val, self.demand_pmf):
            Exp += d_pmf*(self.h*max(x-d,0)+self.p*max(d-x,0))
        
        return Exp
    
    def calculate_future_costs(self,x,q,V_t_plus_1):
        fut_cost = 0
        for (d,d_pmf) in zip(self.demand_val, self.demand_pmf):
            x_t_plus_1 = max((x-d),0)+q
            fut_cost += d_pmf*V_t_plus_1[x_t_plus_1]
        return fut_cost
    
    def run_dp_algo(self):

        # Iterate backwards recursively through all periods
        for period in range(self.T,0,-1):
            # print('Period: {}'.format(period))
            # Retrieve one step ahead optimal cost
            V_t_plus_1 = {val_func[0]:val_func[1] for val_func in self.V}

            # Reset value function for this period
            self.V = []
            for idx, x in enumerate(self.state_space):
                # print('Calculating {}/{}'.format(idx+1, self.state_space_size),end='\r')
                total_cost = {} # Keep track of total cost of each action in the state
                
                # Recall a decision doesn't come into place until the next period so this is independent of the decision 
                # So we can calculate the immediate cost here before iterating over actions
                im_cost = self.G[x]

                # Go over every ordering decision
                # We need to make sure the q is not larger than what we have available in our state space
                max_q = self.max_x-x

                for q in range(max_q):
                    fut_cost = self.gamma*self.calculate_future_costs(x,q,V_t_plus_1)
                    total_cost[q]= im_cost+fut_cost

                opt = min(total_cost, key=total_cost.get)
                self.V.append((x,total_cost[opt]))
                self.optimal_pol.append((period,x,opt))


