from torch import nn

import ai8x
#Use checkpoint path to realise scalable model

class MNIST_25(nn.Module):

    def __init__(self, num_classes=10, num_channels=1, dimensions=(28, 28),
                 planes=16, pool=2, fc_inputs=12, bias=False, **kwargs):
                 
        super().__init__();
       
        dim = dimensions[0];
        
        self.conv1 = ai8x.FusedConv2dReLU(num_channels, planes, 3, 
                                        padding=0, bias=bias);

        self.conv2 = ai8x.FusedConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias);

        self.conv3 = ai8x.FusedMaxPoolConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias)
                                        
        self.conv4 =  ai8x.FusedMaxPoolConv2dReLU(planes, fc_inputs, 1, 
                                        padding=0, bias=bias)
                                        
        self.fc = ai8x.Linear(fc_inputs * (5**2), num_classes, bias = bias);
        
        
    def forward(self, x):
        x = self.conv1(x)
        
        x = self.conv2(x)
        
        x = self.conv3(x)

        x = self.conv4(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)

        return x;
        
        
def mnist_25(pretrained=False, **kwargs):
    """
    Constructs a AI85Net5 model.
    """
    assert not pretrained
    return MNIST_25(**kwargs)
    
    
class MNIST_50(nn.Module):

    def __init__(self, num_classes=10, num_channels=1, dimensions=(28, 28),
                 planes=32, pool=2, fc_inputs=12, bias=False, **kwargs):
                 
        super().__init__();
       
        dim = dimensions[0];
        
        self.conv1 = ai8x.FusedConv2dReLU(num_channels, planes, 3, 
                                        padding=0, bias=bias);

        self.conv2 = ai8x.FusedConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias);

        self.conv3 = ai8x.FusedMaxPoolConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias)
                                        
        self.conv4 =  ai8x.FusedMaxPoolConv2dReLU(planes, fc_inputs, 1, 
                                        padding=0, bias=bias)
                                        
        self.fc = ai8x.Linear(fc_inputs * (5**2), num_classes, bias = bias);
        
        
    def forward(self, x):
        x = self.conv1(x)
        
        x = self.conv2(x)
        
        x = self.conv3(x)

        x = self.conv4(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)

        return x;
        
        
def mnist_50(pretrained=False, **kwargs):
    """
    Constructs a AI85Net5 model.
    """
    assert not pretrained
    return MNIST_50(**kwargs)
    
class MNIST_75(nn.Module):

    def __init__(self, num_classes=10, num_channels=1, dimensions=(28, 28),
                 planes=48, pool=2, fc_inputs=12, bias=False, **kwargs):
                 
        super().__init__();
       
        dim = dimensions[0];
        
        self.conv1 = ai8x.FusedConv2dReLU(num_channels, planes, 3, 
                                        padding=0, bias=bias);

        self.conv2 = ai8x.FusedConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias);

        self.conv3 = ai8x.FusedMaxPoolConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias)
                                        
        self.conv4 =  ai8x.FusedMaxPoolConv2dReLU(planes, fc_inputs, 1, 
                                        padding=0, bias=bias)
                                        
        self.fc = ai8x.Linear(fc_inputs * (5**2), num_classes, bias = bias);
        
        
    def forward(self, x):
        x = self.conv1(x)
        
        x = self.conv2(x)
        
        x = self.conv3(x)

        x = self.conv4(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)

        return x;
        
        
def mnist_75(pretrained=False, **kwargs):
    """
    Constructs a AI85Net5 model.
    """
    assert not pretrained
    return MNIST_75(**kwargs)
    
class MNIST_100(nn.Module):

    def __init__(self, num_classes=10, num_channels=1, dimensions=(28, 28),
                 planes=64, pool=2, fc_inputs=12, bias=False, **kwargs):
                 
        super().__init__();
       
        dim = dimensions[0];
        
        self.conv1 = ai8x.FusedConv2dReLU(num_channels, planes, 3, 
                                        padding=0, bias=bias);

        self.conv2 = ai8x.FusedConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias);

        self.conv3 = ai8x.FusedMaxPoolConv2dReLU(planes, planes, 3, 
                                        padding=0, bias=bias)
                                        
        self.conv4 =  ai8x.FusedMaxPoolConv2dReLU(planes, fc_inputs, 1, 
                                        padding=0, bias=bias)
                                        
        self.fc = ai8x.Linear(fc_inputs * (5**2), num_classes, bias = bias);
        
        
    def forward(self, x):
        x = self.conv1(x)
        
        x = self.conv2(x)
        
        x = self.conv3(x)

        x = self.conv4(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)

        return x;
        
        
def mnist_100(pretrained=False, **kwargs):
    """
    Constructs a AI85Net5 model.
    """
    assert not pretrained
    return MNIST_100(**kwargs)
    
models = [
    {
        'name': 'mnist_25',
        'min_input': 1,
        'dim': 2,
    },
    {
        'name': 'mnist_50',
        'min_input': 1,
        'dim': 2,
    },
    {
        'name': 'mnist_75',
        'min_input': 1,
        'dim': 2,
    },
    {
        'name': 'mnist_100',
        'min_input': 1,
        'dim': 2,
    }
]
