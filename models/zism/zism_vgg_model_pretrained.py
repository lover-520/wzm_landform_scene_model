# -*- coding: utf-8 -*-
"""
@author: WZM
@time: 2021/1/4 17:26
@function: 将原文作者的初始网络结构换成VGG网络提取特征图
"""

import torch.nn as nn
import torch
import torchvision.models as models
import torch.utils.model_zoo as model_zoo


class VggModel(nn.Module):

    # Multi-column CNN
    def __init__(self, num_classes=6):
        super(VggModel, self).__init__()
        # pre = torch.load("vgg16-397923af.pth")
        # model = models.vgg16(pretrained=False)
        # model.load_state_dict(pre)
        self.features1 = nn.Sequential(
            # [16, 3, 128, 128]
            nn.Conv2d(3, 64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(64, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(128, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(256, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False)
        )
        self.features2 = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(64, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(128, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(256, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 128, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0,
                         dilation=1, ceil_mode=False)
        )
        self.conv1_fusion = nn.Conv2d(384, 256, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(256)
        self.relu1_fusion = nn.ReLU(inplace=True)

        self.conv2_fusion = nn.Conv2d(256, 128, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(128)
        self.relu2_fusion = nn.ReLU(inplace=True)

        self.downsample = nn.Sequential(
            nn.Conv2d(384, 128, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(128),
        )
        self.conv_fusion = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=1, stride=1, padding=0, bias=False),
            nn.ReLU(inplace=True),
        )

        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(64 * 7 * 7, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes),
        )

    def forward(self, x1, x2, x3, IsUseRGB):
        """
        :param x1: [16, 3, 512, 512]
        :param x2: [16, 1, 512, 512]
        :param x3: [16, 1, 512, 512]
        :param IsUseRGB:
        :return:
        """
        # x1---image ; x2-----dem ; x3 ----slope
        # if IsUseRGB == 1:
        #     x1 = self.features1(x1)
        # else:
        #     x1 = self.features11(x1)
        x1 = self.features1(x1)  # [16, 128, 7, 7]

        x2 = self.features2(x2)
        x3 = self.features2(x3)
        x = torch.cat((x1, x2, x3), 1)

        h = self.conv1_fusion(x)

        h = self.bn1(h)
        h = self.relu1_fusion(h)

        h = self.conv2_fusion(h)
        h = self.bn2(h)

        h += self.downsample(x)

        h = self.relu1_fusion(h)
        h = self.conv_fusion(h)
        # print(h.shape)
        h = h.view(h.size(0), -1)

        h = self.classifier(h)
        return h
