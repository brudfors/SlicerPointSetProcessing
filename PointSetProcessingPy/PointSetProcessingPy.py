import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

import logging

############################################################ PointSetProcessingPy 
class PointSetProcessingPy(ScriptedLoadableModule):
  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PointSetProcessing" 
    self.parent.categories = ["Filtering"]
    self.parent.dependencies = []
    self.parent.contributors = ["Mikael Brudfors (brudfors@gmail.com)"] 
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

############################################################ PointSetProcessingPyWidget 
class PointSetProcessingPyWidget(ScriptedLoadableModuleWidget):
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    pointSetProcessingCollapsibleButton = ctk.ctkCollapsibleButton()
    pointSetProcessingCollapsibleButton.text = "Surface Reconstruction from Unorganized Points"
    self.layout.addWidget(pointSetProcessingCollapsibleButton)
    pointSetProcessingFormLayout = qt.QFormLayout(pointSetProcessingCollapsibleButton)

    # Input
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLModelNode"), "" )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    pointSetProcessingFormLayout.addRow("Input Model: ", self.inputSelector)

    # Runtime
    self.runtimeGroupBox = ctk.ctkCollapsibleGroupBox()
    self.runtimeGroupBox.setTitle("Runtime")
    runtimeFormLayout = qt.QFormLayout(self.runtimeGroupBox)
    pointSetProcessingFormLayout.addRow(self.runtimeGroupBox)
    
    self.runtimeLabel = qt.QLabel()
    self.runtimeLabel.setText("... s.")
    self.runtimeLabel.setWordWrap(True)
    self.runtimeLabel.setStyleSheet("QLabel { background-color : black; \
                                           color : #66FF00; \
                                           height : 60px; \
                                           border-style: outset; \
                                           border-width: 5px; \
                                           border-radius: 10px; \
                                           font: bold 14px; \
                                           padding: 0px;\
                                           font-family : SimSun; \
                                           qproperty-alignment: AlignCenter}")
    runtimeFormLayout.addRow(self.runtimeLabel)
    
    # Normals
    self.normalsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.normalsGroupBox.setTitle("Normals")
    normalsFormLayout = qt.QFormLayout(self.normalsGroupBox)
    pointSetProcessingFormLayout.addRow(self.normalsGroupBox)
    
    self.parametersNormalsOutputGroupBox = qt.QGroupBox()
    self.parametersNormalsOutputGroupBox.setTitle("Parameters")
    parametersNormalsOutputFormLayout = qt.QFormLayout(self.parametersNormalsOutputGroupBox)
    normalsFormLayout.addRow(self.parametersNormalsOutputGroupBox)

    self.modeTypeComboBox = qt.QComboBox()
    self.modeTypeComboBox.addItem('Fixed')  
    self.modeTypeComboBox.addItem('Radius')
    self.modeTypeComboBox.setCurrentIndex(1)
    self.modeTypeComboBox.setToolTip('')    
    parametersNormalsOutputFormLayout.addRow('Mode Type: ', self.modeTypeComboBox)
    
    self.numberOfNeighborsSlider = ctk.ctkSliderWidget()
    self.numberOfNeighborsSlider.setDecimals(0)
    self.numberOfNeighborsSlider.singleStep = 1
    self.numberOfNeighborsSlider.minimum = 1
    self.numberOfNeighborsSlider.maximum = 20
    self.numberOfNeighborsSlider.value = 4
    self.numberOfNeighborsSlider.setToolTip('')
    self.numberOfNeighborsSlider.enabled = False
    parametersNormalsOutputFormLayout.addRow('Fixed Neighbors: ', self.numberOfNeighborsSlider)
    
    self.radiusSlider = ctk.ctkSliderWidget()
    self.radiusSlider.setDecimals(2)
    self.radiusSlider.singleStep = 0.01
    self.radiusSlider.minimum = 1
    self.radiusSlider.maximum = 10
    self.radiusSlider.value = 1.0
    self.radiusSlider.setToolTip('')
    parametersNormalsOutputFormLayout.addRow('Radius: ', self.radiusSlider)
    
    self.graphTypeComboBox = qt.QComboBox()
    self.graphTypeComboBox.addItem('Riemann')  
    self.graphTypeComboBox.addItem('KNN')
    self.graphTypeComboBox.setCurrentIndex(1)
    self.graphTypeComboBox.setToolTip('')    
    parametersNormalsOutputFormLayout.addRow('Graph Type: ', self.graphTypeComboBox)
    
    self.knnSlider = ctk.ctkSliderWidget()
    self.knnSlider.setDecimals(0)
    self.knnSlider.singleStep = 1
    self.knnSlider.minimum = 1
    self.knnSlider.maximum = 20
    self.knnSlider.value = 3
    self.knnSlider.setToolTip('')
    parametersNormalsOutputFormLayout.addRow('Nearest Neighbors: ', self.knnSlider)
           
    self.computeNormalsButton = qt.QPushButton("Compute Normals")
    self.computeNormalsButton.enabled = False
    self.computeNormalsButton.checkable = True
    normalsFormLayout.addRow(self.computeNormalsButton)
    
    # Surface
    self.surfaceGroupBox = ctk.ctkCollapsibleGroupBox()
    self.surfaceGroupBox.setTitle("Surface")
    surfaceFormLayout = qt.QFormLayout(self.surfaceGroupBox)
    pointSetProcessingFormLayout.addRow(self.surfaceGroupBox)
    
    self.parametersPoissonOutputGroupBox = qt.QGroupBox()
    self.parametersPoissonOutputGroupBox.setTitle("Parameters")
    parametersPoissonOutputFormLayout = qt.QFormLayout(self.parametersPoissonOutputGroupBox)
    surfaceFormLayout.addRow(self.parametersPoissonOutputGroupBox)
    
    self.depthSlider = ctk.ctkSliderWidget()
    self.depthSlider.setDecimals(0)
    self.depthSlider.singleStep = 1
    self.depthSlider.minimum = 1
    self.depthSlider.maximum = 20
    self.depthSlider.value = 8
    self.depthSlider.setToolTip('This integer controls the reconstruction depth; the maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a voxel grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound. The default value for this parameter is 8.')
    parametersPoissonOutputFormLayout.addRow('Depth: ', self.depthSlider)
    
    self.scaleSlider = ctk.ctkSliderWidget()
    self.scaleSlider.setDecimals(2)
    self.scaleSlider.singleStep = 0.01
    self.scaleSlider.minimum = 1
    self.scaleSlider.maximum = 10
    self.scaleSlider.value = 1.25
    self.scaleSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube. The default value is 1.25.')
    parametersPoissonOutputFormLayout.addRow('Scale: ', self.scaleSlider)    
    
    self.solverDivideSlider = ctk.ctkSliderWidget()
    self.solverDivideSlider.setDecimals(0)
    self.solverDivideSlider.singleStep = 1
    self.solverDivideSlider.minimum = 1
    self.solverDivideSlider.maximum = 20
    self.solverDivideSlider.value = 8
    self.solverDivideSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube. The default value is 1.25.')
    parametersPoissonOutputFormLayout.addRow('Solver Divide: ', self.solverDivideSlider)   
    
    self.isoDivideSlider = ctk.ctkSliderWidget()
    self.isoDivideSlider.setDecimals(0)
    self.isoDivideSlider.singleStep = 1
    self.isoDivideSlider.minimum = 1
    self.isoDivideSlider.maximum = 20
    self.isoDivideSlider.value = 8
    self.isoDivideSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube. The default value is 1.25.')
    parametersPoissonOutputFormLayout.addRow('Iso Divide: ', self.isoDivideSlider)   
 
    self.samplesPerNodeSlider = ctk.ctkSliderWidget()
    self.samplesPerNodeSlider.setDecimals(2)
    self.samplesPerNodeSlider.singleStep = 0.1
    self.samplesPerNodeSlider.minimum = 1
    self.samplesPerNodeSlider.maximum = 10
    self.samplesPerNodeSlider.value = 1.0
    self.samplesPerNodeSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube. The default value is 1.25.')
    parametersPoissonOutputFormLayout.addRow('Samples per Node: ', self.samplesPerNodeSlider)   
    
    self.confidenceComboBox = qt.QComboBox()
    self.confidenceComboBox.addItem('False')
    self.confidenceComboBox.addItem('True')  
    self.confidenceComboBox.setToolTip('')    
    parametersPoissonOutputFormLayout.addRow('Confidence: ', self.confidenceComboBox)
   
    self.verboseComboBox = qt.QComboBox()
    self.verboseComboBox.addItem('False')
    self.verboseComboBox.addItem('True')  
    self.verboseComboBox.setToolTip('')    
    parametersPoissonOutputFormLayout.addRow('Verbose: ', self.verboseComboBox)
    
    self.computeSurfaceButton = qt.QPushButton("Compute Surface")
    self.computeSurfaceButton.enabled = False
    self.computeSurfaceButton.checkable = True
    surfaceFormLayout.addRow(self.computeSurfaceButton)
    
    # connections
    self.computeNormalsButton.connect('clicked(bool)', self.onComputeNormals)
    self.computeSurfaceButton.connect('clicked(bool)', self.onComputeSurface)
    self.inputSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.graphTypeComboBox.connect('currentIndexChanged(const QString &)', self.onGraphTypeChanged)
    self.modeTypeComboBox.connect('currentIndexChanged(const QString &)', self.onModeTypeChanged)
    
    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh 
    self.onSelect()
        
    lm=slicer.app.layoutManager()
    lm.setLayout(4) # One 3D-view    
    
  def onGraphTypeChanged(self, type):
    if type == 'KNN':
      self.knnSlider.enabled = True
    elif type == 'Riemann':
      self.knnSlider.enabled = False

  def onModeTypeChanged(self, type):
    if type == 'Radius':
      self.radiusSlider.enabled = True
      self.numberOfNeighborsSlider.enabled = False
    elif type == 'Fixed':
      self.radiusSlider.enabled = False
      self.numberOfNeighborsSlider.enabled = True
      
  def onSelect(self):
    logic = PointSetProcessingPyLogic()
    self.computeNormalsButton.enabled = self.inputSelector.currentNode()
    self.computeSurfaceButton.enabled = logic.inputHasNormals(self.inputSelector.currentNode())

  def onComputeNormals(self):
    if self.computeNormalsButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.computeNormals(self.inputSelector.currentNode(), self.modeTypeComboBox.currentIndex, self.numberOfNeighborsSlider.value, self.radiusSlider.value, self.knnSlider.value, self.graphTypeComboBox.currentIndex, self.runtimeLabel)
      self.computeNormalsButton.checked = False   
      self.computeSurfaceButton.enabled = logic.inputHasNormals(self.inputSelector.currentNode())
      
  def onComputeSurface(self):
    if self.computeSurfaceButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.computeSurface(self.inputSelector.currentNode(), self.depthSlider.value, self.scaleSlider.value, self.solverDivideSlider.value, self.isoDivideSlider.value, self.samplesPerNodeSlider.value, self.confidenceComboBox.currentIndex, self.verboseComboBox.currentIndex, self.runtimeLabel)
      self.computeSurfaceButton.checked = False         

############################################################ PointSetProcessingPyLogic 
class PointSetProcessingPyLogic(ScriptedLoadableModuleLogic):

  def computeNormals(self, inputModelNode, modeType, numberOfNeighbors, radius, kNearestNeighbors, graphType, runtimeLabel = None):
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeNormals(inputModelNode, modeType, int(numberOfNeighbors), float(radius), int(kNearestNeighbors), graphType)
    if runtimeLabel:
      runtimeLabel.setText('Normals computed in  %.2f' % runtime + ' s.')
    return True
   
  def computeSurface(self, inputModelNode, depth, scale, solverDivide, isoDivide, samplesPerNode, confidence, verbose, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('PointSetProcessingOutput')
    if not outputModelNode:
      outputModelNode = self.createOutputModelNode()
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeSurface(inputModelNode, outputModelNode, int(depth), float(scale), int(solverDivide), int(isoDivide), float(samplesPerNode), confidence, verbose)
    if runtimeLabel:
      runtimeLabel.setText('Surface computed in %.2f' % runtime + ' s.')
    return True
    
  def inputHasNormals(self, inputModelNode):
    if not inputModelNode:
      logging.info('inputHasNormals(): No input')
      return False
    return slicer.modules.pointsetprocessingcpp.logic().HasPointNormals(inputModelNode)
   
  def createOutputModelNode(self):
    scene = slicer.mrmlScene
    outputModelNode = slicer.vtkMRMLModelNode()
    outputModelNode.SetScene(scene)
    outputModelNode.SetName('PointSetProcessingOutput')
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(1, 0, 0)
    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    outputModelNode.SetAndObserveDisplayNodeID(modelDisplay.GetID())
    scene.AddNode(outputModelNode)  
    return outputModelNode
    
############################################################ PointSetProcessingPyTest    
class PointSetProcessingPyTest(ScriptedLoadableModuleTest):

  def setUp(self):
    slicer.mrmlScene.Clear(0)
    layoutManager = slicer.app.layoutManager()
    layoutManager.setLayout(4)
    
  def runTest(self):
    self.setUp()
    self.test_Module()

  def test_Module(self):
    self.delayDisplay("Testing module")
    pointSetProcessingPyModuleDirectoryPath = slicer.modules.pointsetprocessingpy.path.replace("PointSetProcessingPy.py", "")
    slicer.util.loadModel(pointSetProcessingPyModuleDirectoryPath + '../Data/SpherePoints.vtp', 'SpherePoints')
    inputModelNode = slicer.util.getNode('SpherePoints')
    logic = PointSetProcessingPyLogic()
    self.assertTrue(logic.computeNormals(inputModelNode, 3, 'KNN'))        
    self.assertTrue(logic.computeSurface(inputModelNode, 8))        
    self.delayDisplay('Testing module passed!')    
