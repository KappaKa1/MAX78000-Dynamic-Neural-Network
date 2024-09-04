# Introduction
  The focus for project is to study the effects of altering the parameter size used in an inference. The Dynamic Model used in this experiment is capable of altering the size of its parameter during an inference in exchange for a faster processing time and lesser energy consumption. 
  
# Software and Environment set-up installations
  Before embarking on the project, there are several software and environment set-ups that have to be done. A detailed walkthrough of all the necessary installations can be found [here](https://github.com/analogdevicesinc/ai8x-training?tab=readme-ov-file#installation). 
  Here are the information for the systems involved in the project:
  - The project was carried out using a Windows 11 operating system
  - **Ubuntu 22.04.3 LTS** was used for a virtual Linux environment.
  - The main IDE used is the provided **Eclipse** 

# Training the AI Dynamic Model
  Before describing the Dynamic training approach, here are some important information to take note of which governs the way training should be done for the most part of the project. The Dynamic approach strictly follow these information, but diverges in [train.py](https://github.com/KappaKa1/MAX78000-Dynamic-Neural-Network/blob/main/README.md#trainpy) as the software does not support Dynamic training. The Dynamic Training consist of models inheriting parameters from previous smaller trained models, and are predefind sizes of 25%, 50%, 75% and 100% (final model). The final model produced, although not entirely similar, would have parameters resembling previous models. This allow the model to alter in size, though in discrete values, while still retaining some accuracy.
  
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
### Quantisation Aware Training (QAT) FINISH THIS
  Before the calculated weights from the training are synthesised onto the board, it has to be quantisized.
## Training the Dynamic Model
  The training stage is crucial for building a Model with dynamic traits. The training method utilized is similar to inheriting, where a model would inherit parts of its initial parameters from a smaller yet similar trained model. It would then undergo the training process such that its weights would be trained while retaining some resemblance of the previous model. The figure below illustrates the training process.
  <image>
  The intensity of the Dynamic Model training depends heavily on the Dataset itself and the amount of nested models needed. And the intensity of each training of subsequent models is negatively correlated with the accuracy of the subsequent models. This is shown in the results section of the Dynamic MNIST model where the subsequent models in the Dynamic Model performing worse than its counterpart which did not undergo dynamic training. This is also supported by the explanation that additional training epochs would likely alter the original parameters provided by the previous models.
### train_altered.py
  The provided "train.py" does not provide the neccessary functions to support Dynamic Training. Thus, it has to be altered while at the same time causing minimum inteference to the entire training process. The altered version is called **"train_altered.py"**, which contains additional code that supports Dynamic Training. The location in which the addtional codes are placed ensures minimal interaction to the training process. The python file of the Dynamic Model have to be imported to **"train_altered.py"** for linking purposes. It contains 3 variables that have to be changed for each subsequent training, and these are "LOGGER_INFO", "RATIO" and the 1st argument of "apputils.load_lean_checkpoint()". The "LOGGER_INFO" selects the trained version of the previous model in which the weights of the current model would be initiallised with. The "RATIO" represents the dimension of the previous model's channel, which is dependant for each layer (though not in this dynamic model). Finally, the 1st argument of "apputils.load_lean_checkpoint()" should be the initiallisation of the previous model. The code below is an example of training the 75% model using the weights of 50% model.
  (image)
## Optimizing the Dynamic Model Accuracy
  The project measures the accuracy of the Dynamic Model through analysing the accuracy of each subsequent model. Thus, the smallest model's accuracy is just as important as the largest mode's accuracy. During training, the best outcome for a dynamic model is increasing the accuracy of the current model while maintaining the accuracy of the previous model. This sections aims to achieve this outcome. It is important to note that these factors are heavily dependant on the type of dataset used, although it would not be the main area of focus as there is less control over it.
### Number of Epochs
  The number of epochs firstly depends heavily of the type of dataset, but that will not be the area of focus. For the first starting model (base model), the number of epochs should be high to set a good foundation for the subsequent models and for its accuracy. The number of epochs should reflect the stage in which the accuracy of the model stabilizes, in the case of MNIST is 25 epochs. For the subsequent models however, each additional epoch would likely mean a decreased accuracy for all previous models before it, especially the base model. The selected epoch number have to therefore balance between increasing the current model's accuracy and maintaining previous models' accuracy. The best approach is using trial and error, and in the case of MNIST is found to be 5 epochs each for subsequent models.
### Number of subsequent models
  The number of seubsequent models affects the number of epochs. With a high number of subsequent models, the starting few models' accuracy would be heavily impeded due to the high dynamic training frequency. Thus, a suitable number of subsequency models have to be chosen to maintain a high accuracy for the base model. The MNIST Dynamic Model uses 4 total models, and are 25%, 50%, 75% and 100%.
### QAT policy


# Synthesising and Modification of the code for Dynamic Model
## Synthesising and ai8xer.py
  The MAX78000 provides a software, **"ai8xer.py"**, that translates the python model code into C language that can be synthesized onto the board. There are 3 main files that are required when using the **"ai8xer.py"**, and are the python model, the network description file and the sample file. Information on the python model found can be found [here]().
### Network Description file and Sample file
  The network description file contains high-level codes which describes inner workings, like processor enables, to the board. It can be generat
## Weights and Processor modification for Dynamic Model

# Data Streaming, Testing and Data Collecting
  The model on MAX78000 have to be validated with the **TEST DATASET** provided in the MNIST Dataset. The data are loaded onto the MAX78000 using a UART from a laptop, and the output of the inference (plus inference time) is outputted from the MAX78000 to the laptop. As for the values of power consumptions, there is a usb port (CN1) that uses UART to output the data per inference and can be collected using a laptop (although this is not done in the project due to the lack of ports). The values of power consumptions can alternatively be observed through the LED display provided on the MAX78000 EV kit board (which is the primary method for obtaining energy data in this project).
## Data Normalizing and Loading of Data (CHW)
  The values of the MNIST dataset comes in the ranges of [0,255], with each data having **784** bytes. The MAX78000 requires all input data to be normalized in the range of [-128,127], and this is done through XOR gate of 128 (^ 128) to the MNSIT dataset. The input data are transmitted and received through UART protocol in bytes. During Transmission, a data is split into groups of 4 bytes, with the order of the 4 bytes inverted (required by the board). Once received at the board, each 4 bytes of input data are concatenated to a single block of 32-bits data and is stored in the desired address. The selected format in which the MNIST inputs are stored is CHW [(Channel-Height-Width)](https://github.com/analogdevicesinc/ai8x-training#hwc-height-width-channels), which priotises channels (less complex for MNIST which only have a single input channel).
## UART Initialisation and UART Transaction
## Push Button
# Future Works
