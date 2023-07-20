import numpy as np
import pandas as pd

class Simulation():
    """
        A simulation of a lost sales inventory management system. Replicates the inventory system of Zipkin (2008).
        Slight differences in that we asssume a time horizon of t=0,...,T-1 with terminal time T. In Zipkin (2008)
        the time horizon is t=1,...,T with terminal time T+1.
        

        Attributes
        ----------
        T : int
            Time horizon
        L : int
            Lead time
        cu : float
            underage cost (cost of stocking out per unit)
        co : float
            overage cost (cost of holding excess inventory per unit)
        c : float
            order cost per unit
        init_inv : List[int]
            Initial inventory
        x : ndarray
            state of inventory system over time. x[t] logs the inventory at time t.
        log : DataFrame
            Pandas DataFrame with comprehensive logging the events in the sytem
        period_cost : ndarray
            The period cost of the ststem over the simulation

        Methods
        -------
        order(t,x)
            Given a time and state of inventory, determine an ordering decision
        reset()
            Reset the simulation from scratch so a new one can be ran without the need to reinitialise the class
        run(demand)
            run a simulation over the time horizon given some demand.


    """
    def __init__(self, T, lead_time, underage, overage, salvage, initial_inventory, order_rule, log_data=True):
        
        self.T = T
        self.L = lead_time # How long it takes for orders to arrive
        self.cu = underage # also known as per unit penalty cost
        self.co = overage # also known as per unit holding cost
        self.c = salvage  # also known as procurement
        self.init_inv = initial_inventory
        
        self.order_rule = order_rule
        
        self.x = np.zeros((self.T+1, self.L+1))
        self.x[0] = self.init_inv
        self.log_data = log_data
        
        # If logging the data, create a dictionary to store updates
        if (self.log_data):
            self.log = {'StartingInv': [], 'Order': [], 'PostOrder': [], 'Demand': [],'PostDemand': [], 'PostDeliveryMovements': [],'PeriodCost': []}
        
    def order(self,t,x):
        """
            Here we define the various ordering policies, given the current period and state of the system.
            These are currenlty left blank and should be filled in with the new methods.
            We should return from this an order quantity, this can be:
            * Constant.
            * Depending on time.
            * Depending on a fixed order up to level.
            * Depending on both time and the current inventory level
        """
        
        # Order up to, constant base-stock policy
        if (self.order_rule == 'CBS'):
            # Insert ordering policy here and remove this temp example
            order_q = 5 if t<5 else 6
        
        # Order-up-to, state-dependent base-stock policy
        if (self.order_rule == 'SDBS'):
            # Insert ordering policy here and remove this temp example
            order_q = 5 if x[0]<5 else 6      
        
        # Fixed Order quantity, constant (i.e. Newsvendor)
        if (self.order_rule == 'FQ'):
           # Insert ordering policy here and remove this temp example
            order_q = 5  
        
        # Order quantity, state dependent (i.e. Optimal)
        # Uncomment if we look at a tractable optimal policy
#         if (self.order_rule == 'OPT'):
#             # Insert ordering policy here and remove this temp example
#             break
            
        return order_q
    
    def reset(self):
        """
            Reset the inventory simulation to run again
        """
        self.x = np.zeros((self.T+1, self.L+1))
        self.x[0] = self.init_inv
        self.period_cost = []
        if (self.log_data):
            self.log = {'StartingInv': [], 'Order': [], 'PostOrder': [], 'Demand': [],'PostDemand': [], 'PostDeliveryMovements': [],'PeriodCost': []}
        
        
        
    def run(self,demand):
        
        # Log period costs
        self.period_cost = []
        
        for t in range(self.T):
            
            if (self.log_data):
                self.log['StartingInv'].append(self.x[t].copy())
            
            # Step 1. Get stocking decision
            # could use an order-up-to policy OR fixed quantity. 
            # Pass the current inventory state if the former, as well as the time period
            Q = self.order(t, self.x[t])

            # Step 2. Add stocking decision to end of pipeline
            self.x[t][-1] = Q
            
            if (self.log_data):
                self.log['PostOrder'].append(self.x[t].copy())
                
            # Step 3. Demand in each channel is realised
            # Allow this to be negative for now so we know the lost sales penalty
            # But later we fix this to pass no negative inventory over.
            self.x[t][0] -= demand[t]
            
            # Step 4. Calculate period costs
            # if shortage: charge underage (lost sales penalty cost)
            # else if surplus: charge overage (holding cost)
            self.period_cost.append(np.abs(self.x[t][0]*self.cu) if self.x[t][0]<=0 else self.x[t][0]*self.co)
            
            # Step 5. Apply lost sales policy and carry move inventory through pipeline
            self.x[t+1][0] = max(self.x[t][0],0)
            for i in range(1,self.L+1):
                self.x[t+1][i-1]+=self.x[t][i]
                self.x[t+1][i] = 0
            
            if (self.log_data):
                self.log['Order'].append(Q)
                self.log['Demand'].append(demand[t])
                self.log['PostDemand'].append(self.x[t][0])
                self.log['PostDeliveryMovements'].append(self.x[t+1].copy())
                self.log['PeriodCost'].append(self.period_cost[t])
        
            
        # Salvage remaining inventory:
        # Here we will incur a overage cost from periods (T:T+L) for stock on-hand
        # and then salvage any remaining inventory at a unit cost c in time period T+L+1.
        # Common to just set this value to 0
        terminal_holding_costs = self.co*np.sum([self.x[self.T][i]*(self.L-i) for i in range(self.L)])
        self.period_cost.append(terminal_holding_costs-self.c*np.sum(self.x[self.T]))
        
        if (self.log_data):
            self.log['StartingInv'].append(self.x[self.T])
            self.log['PostOrder'].append(0)
            self.log['Order'].append(0)
            self.log['Demand'].append(0)
            self.log['PostDemand'].append(0)
            self.log['PostDeliveryMovements'].append(0)
            self.log['PeriodCost'].append(self.period_cost[self.T])
            
            # Export log to dataframe
            self.log = pd.DataFrame(self.log)
            self.log.index +=1
            self.log.index.name = 'Period'    
            