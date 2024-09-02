# Introduction
  The focus for project is to study the effects of altering the parameter size used in an inference
  
# Software and Environment set-up installations
  Please refer to [this](https://github.com/analogdevicesinc/ai8x-training) for the detailed walkthrough of all necessary installations. The project was carried out using a Windows 11 operating system, and installed **Ubuntu** for a virtual Linux environment. The main IDE used is the provided **Eclipse**. 

# Training the AI Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The Dynamic Model used in this experiment is capable of altering the size of its parameter during an inference in exchange for a faster processing time and lesser energy consumption. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a similar yet smaller trained model (excluding the smallest model). 
## Dataset and Model
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
