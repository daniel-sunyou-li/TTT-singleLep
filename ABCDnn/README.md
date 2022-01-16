# ABCDnn
`ABCDnn` is a data-driven background estimation method that transforms a background Monte Carlo sample variable distribution to resemble that of data for a defined 2D-phase space region. The regions are defined by two discrete control variables (nJ and nB) and the `ABCDnn` method allows for 6 regions to be defined, 5 being control regions used in the training, and 1 signal region which is used for any subsequent analysis.  `ABCDnn` is capable of transforming multiple variables for a given sample, and as an example, in the search for pp to three tops, we would be interested in two variables: the scalar transverse momentum of jets, HT, and the DNN discriminator produced in step 3.

The `ABCDnn` method is intended to be run following the production of step3 samples where the DNN discriminator is added to the output `ntuples`.  Because it is only intended for use on ttbar samples, this step is run exclusively on the ttbar samples and the output ntuples will still be denoted as `step3_ABCDnn` to indicate that there is also the transformed distributions available.

## Quick-Start Instructions
### Google Colab (interactive)

### FNAL LPC
    cd nobackup/
    
    export SCRAM_ARCH=slc7_amd64
    
    pip install --user "tensorflow-probability<0.9"
    
    source /cvmfs/cms.cern.ch/cmsset_default.csh
    cmsenv
    source /cvmfs/sft.cern.ch/lcg/views/LCG_98/x86_64-centos7-gcc8-opt/setup.csh
    
## About Neural Autoregressive Flows

Each of the terms in 'Neural Autoregressive Flows' refers to:
* __Flow__: _flow_ refers to generative models built on a series of invertible transformations with the goal of learning a sampled distribution (i.e. data)
> * These are in contrast to two other types of generative models: Generative Adversarial Networks (GANs) and Variational Autoencoders (VAE)
> * The _flow_ in 'Neural Autoregressive Flows' implicity refers to _normalizing flows_ (NF) which are intended to transform simple distributions into complex ones using a series of invertible transformation functions where each individual transformation function is specifically the flow
> * In particular, the flow used in `ABCDnn` applies an affine transformation which can both scale ("multiply") and shift ("add") the source values  
* __Autoregressive__: _autoregrssive_ means that the output of the NF is dependent only on the preceding inputs, but not subsequent outputs
> *  An _autoregressive flow_ is a flow in which each transformations vector variable is conditioned on the previous flow's vector variable
> * For autoregressive flows, each flow can be thought of as predicting the conditional probability, and the normalizaing flow is the product of each of the individual autoregrssive flows  
* __Neural__: _neural_ refers to the use of neural networks to learn the invertible bijective transformations, which are an improvement upon upon the affine transformation, being able to learn more complex transformations
> * One of the reasons NAF are an improvement upon affine transformations is that the transformation can have inflection points allowing unimodal distributions to be transformed to multimodal distributions
> * The NAF transformation can be understood as a cumulative distribution function

The Neural Autoregressive Flow (NAF) is a two-component process which has an autoregressive conditioner and an invertible transformer combined to transform a source distribution into a target distribution. The autoregressive conditioner outputs parameters for the transformer at each training step as a function of the preceding step's output. Any neural architecture satisfying the autoregressive property can be used as the conditioner. The invertible transformer can be any invertible function.  

### Transformers

In using neural networks as both the conditioner and invertible transformer, the choice of activation function is important in achieving the desired functionality. In particular, the activation function of the transformer should be monotonic and the weights positive for the entire normalizing flow to be monotonic. A good candidate is the sigmoid function since it is both monotonic and has an inflection point. 

To avoid restricting the range of the transformation, the inverse sigmoid (i.e. "logit") is applied at the output layer and the outputs of final layer are combined using a softmax-weighted sum. Alternatives to the sigmoid function could be leaky ReLU or ELUs. In the case of using leaky ReLU, because it is a bijection, it would not require softmax-weighted summation. There are also two ways to apply neural networks as the transformations: the first is to use a single node representing the transformation, and the second is to use a dense layer with multiple nodes. For the sigmoidal activation function, the first case is referred to as Deep Sigmoidal Flows (DSF), and the second case is referred to as Deep Dense Sigmoidal Flows (DDSF).
