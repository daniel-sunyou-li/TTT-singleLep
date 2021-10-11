

class ABCDnn(object):
  def __init__( self, inputdim_categorical_list, inputdim, ndense, minibatch, nafdim, depth, lr, gap, conddim, beta1, beta2, lamb, retrain, savedir, savefile, seedd, permute, verbose ):
  self.inputdim_categorical_list = inputdim_categorical_list
  self.inputdim = inputdim
  self.ndense = ndense
  self.inputdimcat = int( np.sum( inputdim_categorical_list ) )
  self.inputdimreal = inputdim - self.inputdimcat
  self.minibatch = minibatch
  self.nafdim = nafdim
  self.depth = depth
  self.lr = lr
  self.gap = gap
  self.conddim = conddim
  self.beta1 = beta1
  self.beta2 = beta2
  self.lamb = lamb
  self.retrain = retrain
  self.savedir = savedir
  self.savefile = savefile
  self.global_step = tf.Variable( 0, name = "global_step" )
  self.monitor_record = []
  self.seed = seedd
  self.permute = permute
  self.verbose = verbose
  self.setup()

def setup( self ):
  np.random.seed( self.seed )
  tf.random.set_seed( self.seed )
  self.createmodel()
  self.checkpoint = tf.train.Checkpoint( global_step, model = self.model, optimizer = self.optimizer )
  self.checkpointmgr = tf.train.CheckpointManager( self.checkpoint, directory = self.savedir, max_to_keep = 10 )
  if ( not self.retrain ) and os.path.exists( self.savedir ):
    status = self.checkpoint.restore( self.checkpointmgr.latest_checkpoint )
    status.assert_existing_objects_matched()
    print( ">> Loaded model from checkpoint" )
    if os.path.exists( os.path.join( self.savedir, self.savefile ) ):
      print( ">> Reading monitor file" )
      self.load_training_monitor()
    print( ">> Resuming from step", self.global_step )
  elif not os.path.exists( self.savedir ):
    os.mkdir( self.savedir )
  pass  



   
