__author__ = 'Helena Russello'

__all__ = ['CSPProblem', 'AllDifferentConstraint', 'BacktrackingSolver']

from copy import deepcopy

"""
Implementation of the CSP problem
"""
class CSPProblem:

    #Constructor
    def __init__(self):
        self._variables = {}
        self._constraints = []
        self._solver = BacktrackingSolver()
        self._assignments = {}

    #Add variable
    def add_variable(self, variable, domain):
        self._variables[variable] = domain

    #Add a constraint
    def add_constraint(self, constraint, variables):
        self._constraints.append((constraint, variables))
        return self._constraints

    #Returns a variable
    def get_variable(self, value):
        return self._variables[value]

    #Assign a value to a variable
    def assign_variable(self, variable, value):
        self._domain_assignment(variable, value)
        self._assignments[variable] = value

    #Prunes the domain of the assigned variable to the given value
    #Private function
    def _domain_assignment(self, variable, value):
        domain = [value]
        self._variables[variable] = domain

    #Private method for solving the problem
    #Parameters : do_forwardchecking (boolean), do_mrv(boolean)
    #must be set to True for performing the Forward check and/or MRV, respectively
    def _solve(self, do_forwardchecking, do_mrv):
        domains, constraints, vconstraints = self._get_attr_for_solving()

        if not domains:
            return {}

        self._assignments = self._solver.solve(domains, constraints, vconstraints, deepcopy(self._assignments), do_forwardchecking, do_mrv)

        for var in self._assignments:
            value = self._assignments[var]
            self._domain_assignment(var, value)

        return self._assignments

    def solve(self):
        return self._solve(False, False)

    def solve_fwc(self):
        return self._solve(True, False)

    def solve_mrv(self):
        return self._solve(False, True)

    def solve_all(self):
        return self._solve(True, True)

    #Private function called before solving the problem
    #Performs some pre-processing such as domain pruning
    #and mapping variables with their constraints
    def _get_attr_for_solving(self):
        domains = deepcopy(self._variables)
        variables = domains.keys()
        constraints = []

        for constraint, c_variables in self._constraints:
            if not c_variables:
                c_variables=variables
            constraints.append((constraint, c_variables))

        v_constraints = {}
        for variable in domains:
            v_constraints[variable] = []
        for constraint, c_variables in constraints:
            for c_var in c_variables:
                v_constraints[c_var].append((constraint, c_variables))

        for constraint, variables in constraints:
            constraint.domain_pruning(domains, variables, self._assignments)

        for domain in domains.values():
            if not domain:
                return None, None, None

        return domains, constraints, v_constraints

#End class CSPProblem

"""
Implementation of the Constraint class (all variables must have a different assigned value)
"""
class AllDifferentConstraint:

    def domain_pruning(self, domains, c_variables, assignments):
        #For each variable of the constraint:
        for variable in c_variables:
            domain = domains[variable]
            #If a variable has a domain of length 1
            if len(domain) == 1:
                value = domain[0]

                #For each other variable of the constraint
                for c_var in c_variables:
                    if c_var != variable:
                        #if not self.satisfied(domains, {c_var:value}, False):
                        c_var_domain = domains[c_var]
                        if len(c_var_domain) > 1:
                            try:
                                c_var_domain.remove(value)
                                if len(c_var_domain) == 1:
                                    assignments[variable] = value
                            except ValueError:
                                pass

    #returns True if the assignments satisfy the constraint, False otherwise
    #do_forwardcheck is a boolean parameter which must be set to True if forward checking is wanted
    def satisfied(self, domains, c_variables, assignments, do_forwardcheck):

        seen = {}
        # return False If the value has been seen more than once
        # in the constraint's assigned variables
        for variable in c_variables:
            assignment = assignments.get(variable)
            if assignment is not None:
                if assignment in seen:
                    return False
                seen[assignment] = True

        if do_forwardcheck:

            #for each variable of the constraint
            for variable in c_variables:
                domain = domains.get(variable)
                assignment = assignments.get(variable)

                #if the variable hasn't been assigned yet:
                if assignment is None:

                    for value in seen:
                        #remove the value from the domain if we saw it already
                        try:
                            domain.remove(value)

                            if len(domain) == 1:
                                assignments[variable] = domain[0]
                                break
                            if len(domain) == 0:
                                #print "False"
                                return False
                        except ValueError:
                            pass

        return True

#End class AllDifferentConstraint

"""
Implementation of the Solver class.
It is a recursive backtracking solver
"""
class BacktrackingSolver:
    #Constructor
    def __init__(self):
        self._recursive_counter=0
        self._domains_stack = []


    def solve(self, domains, constraints, v_constraints, assignments, do_forwardchecking, do_mrv):
        #print "in solve"
        self._recursive_counter=0
        solution = {}
        solution = self._simple_backtracking(solution, domains, constraints, v_constraints, assignments, do_forwardchecking, do_mrv)
        #print str(solution)
        #print self._recursive_counter
        return solution

    def _simple_backtracking(self, solution, domains, constraints, v_constraints, assignments, do_forwardchecking, do_mrv):
        self._recursive_counter = self._recursive_counter +1

        #Look for an unassigned variable
        #Minimum Remaining Value
        happy = False
        if do_mrv:

            #variables sorted from the smallest to the biggest domain
            list = [(len(domains[variable]), variable) for variable in domains]
            list.sort()

            for order, var in list:
                if var not in assignments:
                    break
            else:
                happy = True

            variable = var

        #No heuristic
        else:
            #print "dom:"+str(domains)
            for var in domains:
                if var not in assignments:
                    variable = var
                    break
            #No more unassigned variables ==> solution found
            else:
                #HAPPY
                happy = True

        if happy:
            solution=deepcopy(assignments)
            return solution

        assignments[variable] = None

        for value in domains[variable]:
            assignments[variable] = value
            if do_forwardchecking:
                self._domains_stack.append(deepcopy(domains))

            for constraint, vars in v_constraints[variable]:
                if not constraint.satisfied(domains, vars, assignments, do_forwardchecking):
                    #Assignment doesn't satisfy the constraint
                    break

            #Assignment is ok, next
            else:
                solution = self._simple_backtracking(solution, domains, constraints, v_constraints, assignments, do_forwardchecking, do_mrv)

                if len(solution) > 0:
                    #new_assignments = deepcopy(assignments)
                    return solution

            #Assignment doesn't satisfy the constraint
            if do_forwardchecking:
                domains = self._domains_stack.pop()

        del assignments[variable]
        #new_assignments = deepcopy(assignments)
        return solution

#End of the class BacktrackingSolver