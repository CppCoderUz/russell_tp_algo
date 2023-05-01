"""
Russel Method for transportation problem
=====
"""

from gui import TransportationSolveGUI
from russel_solution import RussellSolution, point_list

TransportationSolveGUI(solution_class=RussellSolution, point_list=point_list, offer_name="S-room", demand_name="Shop")


