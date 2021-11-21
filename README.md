# Project Proposal
Final project for genomics class, Fall 2021 (ECBME4060, Columbia University)

**Group Members**: Richmon Lin (rl3245), Sandra Pereira (sm5150), David Gerard (dg3234), Mikhail Morgan (mm5947)

**Kaggle Project**: https://www.kaggle.com/c/lish-moa
 
**Scientific Background**<br>
In the United States, classic drugs such as acetaminophen (Tylenol) have been used clinically well before their specific biological mechanisms were fully understood. Current drug development methods utilize a more targeted approach that focuses on designing specific molecules to target proteins associated with the function/processes of a disease. Understanding the mechanisms of action (MoA) of a drug is critical for evaluating safety and determining dosage.<br>
A common approach to determining the MoA of a drug is to algorithmically analyze the drug's interactions with a variety of human cell types. These interactions are compared with large pre-existing databases of gene expression and cell viability patterns for drugs with known MoAs. By comparing patterns with existing drugs, scientists can infer the MoA of new drugs. In many cases these drugs have multiple different biological mechanisms. In this project, we hope to create a multiple-label classification model that can identify the MoA of a drug based on a set of 100 different cell type tests. Our model will be trained and validated on a 5,000 MoA-labeled drug dataset. Solutions are evaluated based on the average value of the logarithmic loss function applied to each MoA pair. We seek to use cellular structure to predict the MoA of new drug compounds to enable scientists in the process of drug discovery.
 
**Proposed Methods**<br>
* Dimensionality reduction technique (PCA, t-SNE, U-MAP) and how it affects the different models
* Run an optimized deep neural network on reduced dimension data<br>

We plan to test different neural network architectures. We plan to use the same parameters as Zrimec et al. (Reference 2) In that paper, they tested combinations of: <br>
1. 1 to 4 convolutional neural network (CNN) layers
2. 1 to 2 bidirectional recurrent neural network (RNN) layers
3. 1 to 2 fully connected (FC) layers, in a global architecture layout CNN-RNN-FC<br>

Batch normalization and weight dropout will potentially be applied after all layers and max-pooling after CNN layers. <br>
The Adam optimizer with mean squared error (MSE) loss function and ReLU activation function with uniform weight initialization will be tested. <br>
In addition to what was done in the paper, we plan on trying non-deep learning models with auto gluon on this problem to see what kind of results we can get. 


**References**:
* https://www.kaggle.com/c/lish-moa/overview
* Zrimec, J., Börlin, C.S., Buric, F. et al. Deep learning suggests that gene expression is encoded in all parts of a co-evolving interacting gene regulatory structure. Nat Commun 11, 6141 (2020). https://doi.org/10.1038/s41467-020-19921-4
