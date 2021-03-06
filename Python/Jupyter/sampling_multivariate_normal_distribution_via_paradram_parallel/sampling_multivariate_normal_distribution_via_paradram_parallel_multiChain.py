
import numpy as np

NDIM = 4                                # number of dimensions of the domain of the MVN PDF
MEAN =  np.double([-10, 15., 20., 0.0]) # This is the mean of the MVN PDF.
COVMAT = np.double( [ [1.0,.45,-.3,0.0] # This is the covariance matrix of the MVN PDF.
                    , [.45,1.0,0.3,-.2]
                    , [-.3,0.3,1.0,0.6]
                    , [0.0,-.2,0.6,1.0]
                    ] )

INVCOV = np.linalg.inv(COVMAT) # This is the inverse of the covariance matrix of the MVN distribution.

# The following is the log of the coefficient used in the definition of the MVN.

MVN_COEF = NDIM * np.log( 1. / np.sqrt(2.*np.pi) ) + np.log( np.sqrt(np.linalg.det(INVCOV)) )

# the logarithm of objective function: log(MVN)

def getLogFunc(point):
    '''
    Return the logarithm of the MVN PDF.
    '''
    normedPoint = MEAN - point
    return MVN_COEF - 0.5 * ( np.dot(normedPoint,np.matmul(INVCOV,normedPoint)) )

import paramonte as pm

pmpd = pm.ParaDRAM() # define a ParaMonte sampler instance

pmpd.mpiEnabled = True # This is essential as it enables the invocation of the MPI-parallelized ParaDRAM routines.

pmpd.spec.overwriteRequested = True # overwrite existing output files if needed
pmpd.spec.randomSeed = 3751 # initialize the random seed to generate reproducible results.
pmpd.spec.outputFileName = "./out/mvn_parallel_multiChain"
pmpd.spec.progressReportPeriod = 20000
pmpd.spec.chainSize = 30000 # the default 100,000 unique points is too large for this simple example, so set it to 30000.

# set up a random initial starting point for each of the independent MCMC chains,
# by defining the domain of the random start points. The following defines the 
# boundaries of the NDIM(=four)-dimensional hypercube from within which the 
# random initial start points will be drawn by the sampler,

pmpd.spec.randomStartPointRequested = True # This is essential, otherwise, random initialization won't happen
pmpd.spec.randomStartPointDomainLowerLimitVec = NDIM * [-25]
pmpd.spec.randomStartPointDomainUpperLimitVec = NDIM * [+25]

# set the parallelization model to multichain

pmpd.spec.parallelizationModel = "multi chain" # the value is case and white-space insensitive

# call the ParaDRAM sampler

pmpd.runSampler ( ndim = 4
                , getLogFunc = getLogFunc
                )
