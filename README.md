# Introduction
  The focus for project is to study the effects of altering the parameter size used in an inference. The Dynamic Model used in this experiment is capable of altering the size of its parameter during an inference in exchange for a faster processing time and lesser energy consumption. 
  
# Software and Environment set-up installations
  Please refer to [this](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#installation) for a detailed walkthrough of all necessary installations. The project was carried out using a Windows 11 operating system, and installed **Ubuntu** for a virtual Linux environment. The main IDE used is the provided **Eclipse**. 

# Training the AI Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a smaller yet similar trained model. It would then undergo the training process such that its weights would be trained while retaining some resemblance of the previous model. The figure below illustrates the training process.
  
## Data Loader Design
  A Data Loader is required during training and has different designs for different datasets. It handles data preperation, like preprocessing or normalizing, and ensures that the data is fit for training. The MAX78000 directory provides many Data Loader designs for many datasets, like MNIST and Cifar100. For datasets that are not provided, please refer to [this](https://www.analog.com/en/resources/app-notes/data-loader-design-for-max78000-model-training.html) for steps to designing a data loader. 
## Model Design
  The MAX78000 uses the **"ai8x.py"** library 
## Training the model
## Quantisation Aware Training (QAT)
## train_altered.py

# Converting the python script into C
## Quantasizing the Model
## Network Description file (.yaml)
## ai8xer.py

# Data Streaming and Testing
## Data Normalizing
## UART Initialisation and UART Transaction

# Future Works
