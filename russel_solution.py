import copy

from utils import Price, Point



point_list = []


class RussellSolution:
    """ Russell metodi yordamida transport muammosini hal qilish """

    def __init__(self, demand: list, offer: list, costs: list) -> None:
        self.demand: list = demand
        self.offer: list = offer
        self.price_matrix: list = []
        if RussellSolution.is_empty_matrix(costs):
            return point_list
        if hasattr(costs[0][0], "arg"):
            self.price_matrix = costs
        else:
            for i in range(len(costs)):
                vc = []
                for j in range(len(costs[0])):
                    vc.append(Price(i, j, costs[i][j]))
                self.price_matrix.append(vc)

    
    def get_required_resourse_row(matrix: list, func) -> list:
        """ row bo'yicha func funksiyasi bo'yicha elementlarni qidiradi """
        vc = []
        for i in matrix:
            new_vc = []
            for j in i:
                new_vc.append(j.arg)
            vc.append(func(new_vc))
        return vc

        
    def is_empty_matrix(matrix: list):
        return (matrix == [])

    def get_required_resourse_column(matrix: list, func):
        transposed = []
        for row in zip(*matrix):
            transposed.append(list(row))
        rotated = []
        for row in transposed:
            rotated.append(row[::-1])
        return RussellSolution.get_required_resourse_row(rotated, func=func)

    def get_in_matrix(matrix: list, func):
        vc = []
        try:
            for i in matrix:
                for j in i:
                    vc.append(j.arg)
            return func(vc)
        except:
            return None

    def delete_row_in_matrix(matrix: list, row_index: int) -> list:
        new_matrix = []
        
        for i in range(len(matrix)):
            new_vc = []
            for j in range(len(matrix[0])):
                if not (i == row_index):
                    new_vc.append(matrix[i][j])
            if not (len(new_vc) == 0):
                new_matrix.append(new_vc)
        return new_matrix
    
    def delete_column_in_matrix(matrix: list, column_index: int) -> list:
        new_matrix = []

        for i in range(len(matrix)):
            new_matrix.append([])
            for j in range(len(matrix[0])):
                if not (j == column_index):
                    new_matrix[i].append(matrix[i][j])
        return new_matrix
    
    def delete_index_in_list(vc: list, index: int) -> list:
        new_vc = []
        for i in range(len(vc)):
            if not (i == index):
                new_vc.append(vc[i])
        return new_vc

    def set_point_list(self, matrix: list, min_element: float) -> list:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j].arg == min_element:
                    if self.demand[j] < self.offer[i]:
                        """ taklif katta bo'lgan holat """
                        point_list.append(Point(self.price_matrix[i][j], self.demand[j]))
                        self.offer[i] -= self.demand[j]
                        self.demand = RussellSolution.delete_index_in_list(self.demand, j)
                        matrix = RussellSolution.delete_column_in_matrix(matrix=matrix, column_index=j)
                        self.price_matrix = RussellSolution.delete_column_in_matrix(self.price_matrix, j)
                    elif self.demand[j] > self.offer[i]:
                        """ talab katta bo'lgan holat """
                        point_list.append(Point(self.price_matrix[i][j], self.offer[i]))
                        self.demand[j] -= self.offer[i]
                        self.offer = RussellSolution.delete_index_in_list(self.offer, i)
                        matrix = RussellSolution.delete_row_in_matrix(matrix, i)
                        self.price_matrix = RussellSolution.delete_row_in_matrix(self.price_matrix, i)
                    else:
                        """ talab va taklif teng bo'lgan holat """
                        point_list.append(Point(self.price_matrix[i][j], self.offer[i]))
                        self.offer = RussellSolution.delete_index_in_list(self.offer, i)
                        self.demand = RussellSolution.delete_index_in_list(self.demand, j)

                        self.price_matrix = RussellSolution.delete_column_in_matrix(self.price_matrix, j)
                        self.price_matrix = RussellSolution.delete_row_in_matrix(self.price_matrix, i)

                        matrix = RussellSolution.delete_column_in_matrix(matrix=matrix, column_index=j)
                        matrix = RussellSolution.delete_row_in_matrix(matrix, i)
                    return matrix
    
    def solve(self):
        max_row = RussellSolution.get_required_resourse_row(matrix=self.price_matrix, func=max)
        max_column = RussellSolution.get_required_resourse_column(matrix=self.price_matrix, func=max)

        new_matrix = copy.deepcopy(self.price_matrix)
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[0])):
                new_matrix[i][j].arg = new_matrix[i][j].arg - max_row[i] - max_column[j]
        min_element = RussellSolution.get_in_matrix(new_matrix, min)


        while True:
            if RussellSolution.is_empty_matrix(self.price_matrix):
                return point_list
            new_matrix = self.set_point_list(new_matrix, min_element)
            if min_element == RussellSolution.get_in_matrix(new_matrix, min):
                pass
            else:
                break

        if RussellSolution.is_empty_matrix(self.price_matrix):
            return point_list
        else:
            return RussellSolution(demand=self.demand, offer=self.offer, costs=self.price_matrix).solve()
