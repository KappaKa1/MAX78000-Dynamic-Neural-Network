# MNIST Dynamic Neural Network
  idk what to say here yet
# Software and Environment set-up installations
  Before embarking on the project, there are several software and environment set-ups that have to be done. A detailed walkthrough of all the necessary installations can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#installation). 
  Here are the information for the systems involved in the project:
  - The project was carried out using a Windows 11 operating system
  - **Ubuntu 22.04.3 LTS** was used for a virtual Linux environment.
  - The main IDE used is the provided **Eclipse** 
# Training the AI Dynamic Model
  Before describing the Dynamic training approach, here are some important information to take note of that governs the way training is done throughtout the project. The Dynamic approach strictly follow these information, but diverges in [train.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#trainpy) as the provided software does not support Dynamic training. The Dynamic Training approach consist of models inheriting parameters from previous smaller trained models that are predefind sizes of 25%, 50%, 75% and 100% (final model). The final model produced would have parameters resembling that of previous models. This allow the model to alter in size, though discretely, while retaining accpetable accuracy.
  
## Data Loader Design and Model Design
### Data Loader
  A Data Loader is required during training and contains different designs according to different datasets. It handles data preperation, like preprocessing or normalizing, and prepares that the data for training. The MAX78000 directory provides many Data Loader designs for many datasets that are readily available for use in training. For datasets that are not provided, please refer to the [steps on designing a data loader](https://www.analog.com/en/resources/app-notes/data-loader-design-for-max78000-model-training.html). For training purposes, the data loader normalizes the data to values of [-128/128, 127/128] and converts the data type to Tensor.
  
  The Data Loader used in this project is the provided MNIST Data Loader, which has proccessed the MNIST dataset for training. The data loader also manipulates the image data, through image rotation or position offsetting, that prevents overfitted models and enhances the model's robustness.

### Model Design
  The MAX78000 uses the `ai8x.py` library and its predefined modules to describe the design of the model. A list of predefined modules can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#list-of-predefined-modules). All model designs must follow the predefined modules to be synthesizable onto the MAX78000. Pre-existing models can be adapted onto the board by following the [steps listed here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#adapting-pre-existing-models). 

  The Dynamic Model in this project contains 4 seperate models that are labeled 100%, 75%, 50% and 25%. Although the main focus of this project is not on model design, the structure of the Dynamic Model have to be large to produce acceptable accuracy in the 25% model. Each model consists solely of 4 convolutional layer and a final fully connected layer for categorizing the results. The final model (100%) contains 64-channels, and its subsequnt models which are 75%, 50% and 25% contains 48-channels, 32-channels and 16-channels respectively.The code below displays the 25% model of the Dynamic Model.
  ```
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

        return x
```
  
## Model Training
### train.py
  The MAX78000 provides a training software `train.py` that is used in training AI models for the board. It is activated through a shell script environment (Ubuntu 22.04.03), coupled with other arguments which can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#command-line-arguments). This software however does not support Dynamic Model training. It was thus modified in [train_altered.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#train_alteredpy) to support Dynamic Model training. an example script for training MNIST model is shown below.
```
(ai8x-training) $ python train.py --lr 0.1 --optimizer SGD --epochs 25 --deterministic --compress policies/schedule.yaml --model mnist_25 --dataset MNIST --confusion --param-hist --pr-curves --embedding --device MAX78000 --qat-policy policies/KC_policies/MNIST/qat_policy_kc_start.yaml "$@"
```
### Quantisation Aware Training (QAT) policy
  The parameters after training needs to be [quantasized](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#synthesising-and-ai8xerpy) before getting synthesized onto the board. Quantisation converts the parameters of a floating-point value to an 8-bit value, which lowers the accuracy of the model. A QAT policy can be used during training to lower the effects of quantisation through introducing an extra variable. The variable requires some training and the accuracy of the model might decrease when the QAT policy starts. It is enabled by default and is controlled by a policy file ("qat_policy.yaml"). QAT policy file can be specifically designed to improve quantisation effects, and should be done depending on the model.
## Training the Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a smaller yet similar trained model. It would then undergo the training process such that its weights would be trained while retaining some resemblance of the previous model. The figure below illustrates the training process.
  <image>
  The intensity of the Dynamic Model training depends heavily on the Dataset itself and the amount of nested models needed. And the intensity of each training of subsequent models is negatively correlated with the accuracy of the subsequent models. This is shown in the results section of the Dynamic MNIST model where the subsequent models in the Dynamic Model performing worse than its counterpart which did not undergo dynamic training. This is also supported by the explanation that additional training epochs would likely alter the original parameters provided by the previous models.
### train_altered.py
  The provided `train.py` does not provide the neccessary functions to support Dynamic Training. Thus, it has to be altered while at the same time causing minimum inteference to the entire training process. The altered version is called `train_altered.py`, which contains additional code that supports Dynamic Training. The location in which the addtional codes are placed ensures minimal interaction to the training process. The python file of the Dynamic Model have to be imported to `train_altered.py` for linking purposes. It contains 3 variables that have to be changed for each subsequent training, and these are `LOGGER_INFO`, `RATIO` and the 1st argument of `apputils.load_lean_checkpoint()`. The `LOGGER_INFO` selects the trained version of the previous model in which the weights of the current model would be initiallised with. The `RATIO` represents the dimension of the previous model's channel, which is dependant for each layer (though not in this dynamic model). Finally, the 1st argument of `apputils.load_lean_checkpoint()` should be the initiallisation of the previous model. The code below is an example of training the 100% model using the weights of 75% model.
```
    if True:
        LOGGER_INFO = "logs/2024.09.01-121816/qat_best.pth.tar"
        INPUT_NO = 1
        RATIO = int(64 * 0.75)
        fc_inputs = 12
        Prev_Model = apputils.load_lean_checkpoint(mnist_model.mnist_75(), LOGGER_INFO,
                                              model_device=args.device)
        
        with torch.no_grad():
            for name, param in model.named_parameters():
                param_source = dict(Prev_Model.named_parameters())[name]
                
                if "conv" in name and param.dim() == 4:
                    if 'conv1' in name:
                        param.data[0:RATIO, :, :, :] = param_source.clone()
                    elif 'conv2' in name:
                        param.data[0:RATIO, 0:RATIO, :, :] = param_source.clone()

                elif param.shape == param_source.shape:                                         
                    param.data = param_source.clone()    
```
## Optimizing the Dynamic Model Accuracy
  The project measures the accuracy of the Dynamic Model through analysing the accuracy of each subsequent model. Thus, the smallest model's accuracy is just as important as the largest mode's accuracy. During training, the best outcome for a dynamic model is increasing the accuracy of the current model while maintaining the accuracy of the previous model. This sections aims to achieve this outcome. It is important to note that these factors are heavily dependant on the type of dataset used, although it would not be the main area of focus as there is less control over it.
### Number of Epochs
  The number of epochs firstly depends heavily of the type of dataset, but that will not be the area of focus. In the first starting model (base model), the number of epochs should be high to set a good foundation for the subsequent models. This number should be at the stage in which the accuracy of the model stabilizes. For the subsequent models however, each additional epoch would likely mean a decreased accuracy for all previous models before it, especially the base model. The selected epoch number have to therefore balance between increasing the current model's accuracy and maintaining previous models' accuracy. The best approach is through trial and error.

| Model  | Number of Epochs |
| ------------- | ------------- |
| 25% | 25 Epochs  |
| 50% | 5 Epochs  |
| 75% | 5 Epochs  |
| 100% | 5 Epochs  |
  In the project, the number of training epoch for the base model was set to 25 epochs. The number of training epochs for the subsequent models was set to 5 epochs
### Number of subsequent models
  The number of subsequent models affects the number of epochs. With a high number of subsequent models, the starting few models' accuracy would be heavily impeded due to the high dynamic training frequency. Thus, a suitable number of subsequency models have to be chosen to maintain a high accuracy for the base model. 
  The MNIST Dynamic Model uses 4 total models, and are 25%, 50%, 75% and 100%.
### QAT policy
  The QAT policy file dictates the epoch in which QAT begins and how the parameters are quantisised. It is recommended that the selected epoch is at a stage in which the accuracy of the model stabilises, and that there is enough epoch **(after)** for the QAT's parameter to be trained. 
  The project applies QAT policy in every step of the dynamic training, although starting at different epochs. The QAT policy takes effect on the **10th Epoch** for the base model while the QAT policy takes effect on the **2nd Epoch** for the subsequent models.

# Synthesising and Modification of the code for Dynamic Model
  The MAX78000 provides a software `ai8xer.py` that translates the python model code into C language that can be synthesized onto the board. There are 3 main files that are required when using the `ai8xer.py`, and are the quantisised weights file, the network description file and the sample file.
## Quantisised weights file
  The following code produces a quantisised weight file under the directory `ai8x-synthesis/trained/`. Please note to use the weights with [QAT policy](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#quantisation-aware-training-qat-policy) when quantisising.
```
python quantize.py ../ai8x-training/logs/2024.09.01-120027/qat_best.pth.tar  trained/proj-final.pth.tar --device MAX78000 -v "$@"
```
## Network Description file
  The network description file contains high-level codes which describes the network to the board. It can be generated through the python code below, although it only works for simple networks and would produce errors for much complex models. The best approach is to generate the network description file, then correct any mistakes made by the software. Additional descriptions can be added [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#global-configuration)
```
python train.py --device MAX78000 --model ai85net5 --dataset MNIST --epochs 4 --yaml-template mnist_final.yaml
```
## Sample file
  For verification purposes, a sample file is required for KAT (Known-Answer-Test). There are two ways to generate a sample, either by slicing a sample data during training or by generating a random sample. To slice a sample data, include `--save-sample [number]` in the training script. To generate a random sample, use the code below
```
import os
import numpy as np

a = np.random.randint(-128, 127, size=(1, 28, 28), dtype=np.int64)
np.save(os.path.join('tests', 'sample_mnist'), a, allow_pickle=False, fix_imports=False)
```
For slicing a sample data, use the script below.
### ai8xer.py
  Once all 3 files are ready, use the script below to generate C code that can be synthesised into the board.
```
python ai8xize.py --verbose --test-dir demos --prefix example --checkpoint-file trained/example.pth.tar --config-file networks/example.yaml --device MAX78000 --compact-data --softmax --energy --no-kat
```
## Weights and Processor modification for Dynamic Model
  The Dynamic Model in this project alters the size of each model by altering the channel number of each layer. The channel number of the next layer equates to the number of 2x2 weights used during inference. The image below provides an example. This process is replicated on the MAX78000 by altering the max-address register for weight memory (per layer) in each processor. The MAX78000 also contains 64 processors, with each processor having its own **weights memory** and each managing a single channel. Therefore, the processor enable register have to be altered according to the number of active channel to prevent inference of unwanted channels.

  **Note**: In the memory register, bits[3:0] and bits[19:16] should not be altered. In the processor register, bits [31:16] controls the weight counter and bits [15:0] control the processor power. To turn off the first processor entirely, turn off bit[16] and bit[0].
  
# Data Streaming, Testing and Data Collecting
  The Dynamic Model on MAX78000 is validated with the **TEST DATASET** provided in the MNIST Dataset. The data are loaded onto the MAX78000 using a UART from a laptop, and the output of the inference (plus inference time) is outputted from the MAX78000 to the laptop. As for the values of power consumptions, there is a usb port (CN1) that serially outputs the data per inference which can be collected using external device. The values of power consumptions can alternatively be observed through the LED display provided on the MAX78000 EV kit board (which is the primary method for obtaining power data in this project).
## Data Normalizing and Loading of Data (CHW)
  The values of the MNIST dataset comes in the ranges of [0,255], with each data having **784** bytes. The MAX78000 requires all input data to be normalized in the range of [-128,127], and this is done through XOR gate of 128 (^ 128) to the MNSIT dataset. The input data are transmitted and received through UART protocol in bytes. In Transmission, a data is split into groups of 4 bytes and its order inverted (required by the board) before being transmitted. Once received at the board, each 4 bytes of input data are concatenated to a single block of 32-bits data and is stored in the desired address. The selected format in which the MNIST inputs are stored is CHW [(Channel-Height-Width)](https://github.com/analogdevicesinc/ai8x-training#hwc-height-width-channels), which priotises channels. This eases data organisation and makes memory manipulation much less complex, although data processing is slower due to [memory constriction](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#chw-input-data-format-and-consequences-for-weight-memory-layout).
## UART Initialisation and UART Transaction
### MAX78000 UART
  The MAX78000 provides multiple UART ports for communication, with each UART initialisation and transaction register and address being different. A self-defined header and source file, "UART_kc.h" and "UART_kc.c", handles these intialisation and transactions through defined functions. However, the UART ports have to be altered depending on the UART intended to be used for communication.
### External Device UART
  The external device used in this project is a laptop with 2 ports. Python is used for UART communication as it is a high-level language and it provides library that supports serial communication (Pyserial). All data loading and processing are handled by the external device before being transmitted to the MAX78000.
## Data Collection and Analysis
  Once the MAX78000 receives the input data, it undergoes the inference process and produce an output. This output is then transmitted to the external device and would be saved in a excel sheet. This process is repeated until all dataset has been used. Every data in the dataset comes with its label, and the label contains the number in which the data represent. The outputs are checked accordingly using the label to determine if the results is "Correct", "TOP 5" and "Wrong" (It is worth to note that on the finalised excel sheet that "TOP 5" includes "Correct"). "Correct" means that the label value has the highest confidence value in the output **(no repeats)**, "Top 5" means that the label value is within top 5 confidence in the output **(with repeats)** and "Wrong" are the rest.
