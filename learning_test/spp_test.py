# -*- coding: utf-8 -*-
"""
@author: WZM
@time: 2021/2/2 17:53
@function:  用于测试SPPNet的文件
"""

from math import floor, ceil
import torch
import torch.nn as nn
import torch.nn.functional as F


class SpatialPyramidPooling2d(nn.Module):
    r"""apply spatial pyramid pooling over a 4d input(a mini-batch of 2d inputs
    with additional channel dimension) as described in the paper
    'Spatial Pyramid Pooling in deep convolutional Networks for visual recognition'
    Args:
        num_level:
        pool_type: max_pool, avg_pool, Default:max_pool
    By the way, the target output size is num_grid:
        num_grid = 0
        for i in range num_level:
            num_grid += (i + 1) * (i + 1)
        num_grid = num_grid * channels # channels is the channel dimension of input data
    examples:
        input = torch.randn((1,3,32,32), dtype=torch.float32)
        net = torch.nn.Sequential(nn.Conv2d(in_channels=3,out_channels=32,kernel_size=3,stride=1),\
                                      nn.ReLU(),\
                                      SpatialPyramidPooling2d(num_level=2,pool_type='avg_pool'),\
                                      nn.Linear(32 * (1*1 + 2*2), 10))
        output = net(input)
    """

    def __init__(self, num_level, pool_type='max_pool'):
        super(SpatialPyramidPooling2d, self).__init__()
        self.num_level = num_level
        self.pool_type = pool_type

    def forward(self, x):
        N, C, H, W = x.size()
        for i in range(self.num_level):
            level = i + 1
            kernel_size = (ceil(H / level), ceil(W / level))
            stride = (ceil(H / level), ceil(W / level))
            padding = (floor((kernel_size[0] * level - H + 1) / 2), floor((kernel_size[1] * level - W + 1) / 2))

            if self.pool_type == 'max_pool':
                tensor = (F.max_pool2d(x, kernel_size=kernel_size, stride=stride, padding=padding)).view(N, -1)
            else:
                tensor = (F.avg_pool2d(x, kernel_size=kernel_size, stride=stride, padding=padding)).view(N, -1)

            if i == 0:
                res = tensor
            else:
                res = torch.cat((res, tensor), 1)
        return res

    def __repr__(self):
        return self.__class__.__name__ + '(' \
               + 'num_level = ' + str(self.num_level) \
               + ', pool_type = ' + str(self.pool_type) + ')'


class SPPNet(nn.Module):
    def __init__(self, num_level=3, pool_type='max_pool'):
        super(SPPNet, self).__init__()
        self.feature = nn.Sequential(nn.Conv2d(3, 64, 3),
                                     nn.ReLU(),
                                     nn.MaxPool2d(2),
                                     nn.Conv2d(64, 64, 3),
                                     nn.ReLU())
        self.num_level = num_level
        self.pool_type = pool_type
        self.num_grid = self._cal_num_grids(num_level)
        self.spp_layer = SpatialPyramidPooling2d(num_level)
        self.linear = nn.Sequential(nn.Linear(self.num_grid * 64, 512),
                                    nn.Linear(512, 10))

    def _cal_num_grids(self, level):
        count = 0
        for i in range(level):
            count += (i + 1) * (i + 1)
        return count

    def forward(self, x):
        x = self.feature(x)
        x = self.spp_layer(x)
        x = self.linear(x)
        return x


if __name__ == '__main__':
    a = torch.rand((1, 3, 224, 224))
    net = SPPNet()
    output = net(a)
    print(output.shape)
