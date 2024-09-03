# Introduction
  The focus for project is to study the effects of altering the parameter size used in an inference. The Dynamic Model used in this experiment is capable of altering the size of its parameter during an inference in exchange for a faster processing time and lesser energy consumption. 
  
# Software and Environment set-up installations
  A detailed walkthrough of all the necessary installations can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#installation). The project was carried out using a Windows 11 operating system, and installed **Ubuntu** for a virtual Linux environment. The main IDE used is the provided **Eclipse**. 

# Training the AI Dynamic Model
  Before describing the Dynamic approach, here are some important information to take note of which governs the way training should be done for the most part of the project. The Dynamic approach strictly follow these information, but diverges in [train.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#trainpy) as the software does not support Dynamic training. The Dynamic Training consist of models inheriting parameters from previous smaller models, which are predefind sizes of 25%, 50%, 75% and 100% (final model). The final model produced, although not entirely similar, would have parameters resembling previous models. This allow the model to alter in size, though in discrete values, while still retaining some accuracy.
  
## Data Loader Design and Model Design
### Data Loader
  A Data Loader is required during training and has different designs for different datasets. It handles data preperation, like preprocessing or normalizing, and ensures that the data is fit for training. The MAX78000 directory provides many Data Loader designs for many datasets, like MNIST and Cifar100, and are readily available for use in training. For datasets that are not provided, please refer to the [steps on designing a data loader](https://www.analog.com/en/resources/app-notes/data-loader-design-for-max78000-model-training.html). For training purposes, the data loader normalizes the data to values of [-128/128, 127/128] and converts the data type to Tensor.
  
  The Data Loader used in the training of MNIST Dynamic MNIST Model is the provided MNIST Data Loader, which has already process the MNIST dataset in such a way that it is suitable for training. The data loader also morphs the image data (rotating the picture or offsetting the image position) which prevents overfitting and enhances robustness of the model.

### Model Design
  The MAX78000 uses the **"ai8x.py"** library and its predefined modules to describe the model design. The list of predefined modules can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#list-of-predefined-modules). All model designs have to use the predefined modules to be compatible with the MAX78000, and pre-existing models can be adapted for compatibility by following [steps listed here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#adapting-pre-existing-models).

  The Dynamic Model contains 4 seperate models and are labeled 100%, 75%, 50% and 25%. Although the main focus of this project is not the model design, the base Dynamic Model design have to be large and accurate enough to ensure usability for the 25% model. Due to the simplistic nature of the MNIST dataset, the Dynamic Model design consists solely of 2D convolution with 2D pooling and a final fully connected layer for categorizing the results. The final model (100%) contains 64-channels, and its subsequnt models which are 75%, 50% and 25% contains 48-channels, 32-channels and 16-channels respectively.
  
## Model Training
### train.py
  The MAX78000 provides a training software **"train.py"** which should be used when training any models for the board. It can be activated through the shell script (Ubuntu 22.04.03), coupled with other arguments that can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#command-line-arguments). However, this software does restricts Dynamic Model training. Thus it was modified in [train_altered.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#train_alteredpy) to support Dynamic Model training. More information is provided there.
### Quantisation Aware Training (QAT)
  During 
## Training the Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a smaller yet similar trained model. It would then undergo the training process such that its weights would be trained while retaining some resemblance of the previous model. The figure below illustrates the training process.
  <image>
  The intensity of the Dynamic Model training depends heavily on the Dataset itself and the amount of nested models needed. And the intensity of each training of subsequent models is negatively correlated with the accuracy of the subsequent models. This is shown in the results section of the Dynamic MNIST model where the subsequent models in the Dynamic Model performing worse than its counterpart which did not undergo dynamic training. This is also supported by the explanation that additional training epochs would likely alter the original parameters provided by the previous models.
### train_altered.py
  In order to support Dynamic Training, the original **"train.py"** has to be altered; while at the same time causing minimum inteference to the entire training process. 
## Optimizing the Dynamic Model Accuracy
### Epochs
### Training Schedule policy
### QAT policy

# Synthesising and Modification of the code for Dynamic Model
## Synthesising and ai8xer.py
  The MAX78000 provides a software, **"ai8xer.py"**, that translates the python model code into C language that can be synthesized onto the board. There are 3 main files that are required when using the **"ai8xer.py"**, and are the python model, the network description file and the sample file. Information on the python model found can be found [here]().
### Network Description file and Sample file
  The network description file contains high-level codes which describes inner workings, like processor enables, to the board. It can be generat
## Weights and Processor modification for Dynamic Model

# Data Streaming and Testing
## Data Normalizing and Loading of Data (HCW)
## UART Initialisation and UART Transaction

# Future Works
