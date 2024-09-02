# Introduction
  The focus for project is to study the effects of altering the parameter size used in an inference. The Dynamic Model used in this experiment is capable of altering the size of its parameter during an inference in exchange for a faster processing time and lesser energy consumption. 
  
# Software and Environment set-up installations
  A detailed walkthrough of all the necessary installations can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#installation). The project was carried out using a Windows 11 operating system, and installed **Ubuntu** for a virtual Linux environment. The main IDE used is the provided **Eclipse**. 

# Training the AI Dynamic Model
  Before describing the Dynamic approach, here are some important information to take note of which governs the way training should be done for the most part of the project. The Dynamic approach strictly follows these steps, but diverges in [train.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#trainpy) as the software does not support Dynamic training.
  
## Data Loader Design and Model Design
### Data Loader
  A Data Loader is required during training and has different designs for different datasets. It handles data preperation, like preprocessing or normalizing, and ensures that the data is fit for training. The MAX78000 directory provides many Data Loader designs for many datasets, like MNIST and Cifar100, and are readily available for use in training. For datasets that are not provided, please refer to the [steps on designing a data loader](https://www.analog.com/en/resources/app-notes/data-loader-design-for-max78000-model-training.html).

### Model Design
  The MAX78000 uses the **"ai8x.py"** library and its predefined modules to describe the model design. The list of predefined modules can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#list-of-predefined-modules). All model designs have to use the predefined modules to be compatible with the MAX78000, and pre-existing models can be adapted for compatibility by following [steps listed here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#adapting-pre-existing-models). 
  
## Model Training
### train.py
  The MAX78000 provides a training software **"train.py"** which should be used when training any models for the board. It can be activated through the shell script (Ubuntu 22.04.03), coupled with other arguments that can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#command-line-arguments). However, this software does restricts Dynamic Model training. Thus it was modified in [train_altered.py]() to support Dynamic Model training. More information would be provided there.
### Quantisation Aware Training (QAT)

## Training the Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a smaller yet similar trained model. It would then undergo the training process such that its weights would be trained while retaining some resemblance of the previous model. The figure below illustrates the training process.
### train_altered.py
### Optimizing the Dynamic Model Accuracy

# Synthesising and Modification of the code for Dynamic Model
## Synthesising and ai8xer.py
## Weights and Processor modification for Dynamic Model

# Data Streaming and Testing
## Data Normalizing and Loading of Data (HCW)
## UART Initialisation and UART Transaction

# Future Works
