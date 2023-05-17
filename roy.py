# -*- coding: cp1251 -*-
import numpy as np


def PSO(func, dim, swarm_size, max_iter, bounds):
    # func - ������� �������
    # dim - ����������� ������������ �������
    # swarm_size - ���������� ������ � ���
    # max_iter - ������������ ����� ��������
    # bounds - ������� ������������ ������

    # �������������
    swarm = np.random.uniform(bounds[0], bounds[1], (swarm_size, dim))
    velocity = np.zeros((swarm_size, dim))
    pbest_pos = swarm.copy()
    pbest_value = np.array([np.inf] * swarm_size)
    gbest_pos = np.zeros(dim)
    gbest_value = np.inf

    # ���� �� ���������
    for i in range(max_iter):
        # ���������� �������� ������� ��� ������ �������
        f = np.array([func(x) for x in swarm])

        # ���������� ������ ������� ��� ������ �������
        mask = f < pbest_value
        pbest_value[mask] = f[mask]
        pbest_pos[mask] = swarm[mask]

        # ���������� ������ ������� ��� ����� ���
        mask = pbest_value < gbest_value
        if np.any(mask):
            gbest_value = np.min(pbest_value)
            gbest_pos = pbest_pos[np.argmin(pbest_value)]

        # ���������� �������� � ������� ������ �������
        w = 0.7  # ����������� ���
        c1 = c2 = 1.4  # ������������ ���������
        r1 = np.random.rand(swarm_size, dim)
        r2 = np.random.rand(swarm_size, dim)
        velocity = w * velocity + c1 * r1 * (pbest_pos - swarm) + c2 * r2 * (gbest_pos - swarm)
        swarm = swarm + velocity

         # �������� �������� ������� ������ �� ������ ������������ ������
        swarm = np.clip(swarm, bounds[0], bounds[1])

        # �������� ��������, ����������� �� ���������, �� ��������������� ��������� ��������
        swarm = np.where(swarm < bounds[0], bounds[0], swarm)
        swarm = np.where(swarm > bounds[1], bounds[1], swarm)

    return gbest_pos.round(6), gbest_value.round(6)


def sphere(x):
    return (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2

dim = 2
swarm_size = 20
max_iter = 50
bounds = np.array([[-20] * dim, [20] * dim])

result = PSO(sphere, dim, swarm_size, max_iter, bounds)
print("Minimum value:", result[1])
print("Minimum position:", result[0])
