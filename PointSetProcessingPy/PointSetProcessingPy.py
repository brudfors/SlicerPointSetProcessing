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
    This module reconstructs a surface from unorganized points. For more information see: https://github.com/brudfors/SlicerPointSetProcessing
    """
    self.parent.acknowledgementText = """
    Supported by projects IPT-2012-0401-300000, TEC2013-48251-C2-1-R, DTS14/00192 and FEDER funds. 
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
    
    # Compute Normals
    self.normalsGroupBox = ctk.ctkCollapsibleGroupBox()
    self.normalsGroupBox.setTitle("Compute Normals")
    normalsFormLayout = qt.QFormLayout(self.normalsGroupBox)
    pointSetProcessingFormLayout.addRow(self.normalsGroupBox)
    
    self.normalsTabWidget = qt.QTabWidget()
    normalsFormLayout.addRow(self.normalsTabWidget)

    # vtkPointSetNormal
    self.vtkPointSetNormalWidget = qt.QWidget()
    vtkPointSetNormalFormLayout = qt.QFormLayout(self.vtkPointSetNormalWidget)
    normalsFormLayout.addRow(self.vtkPointSetNormalWidget)
    self.normalsTabWidget.addTab(self.vtkPointSetNormalWidget, "vtkPointSetNormal")    
        
    self.modeTypeComboBox = qt.QComboBox()
    self.modeTypeComboBox.addItem('Fixed')  
    self.modeTypeComboBox.addItem('Radius')
    self.modeTypeComboBox.setCurrentIndex(1)
    self.modeTypeComboBox.setToolTip('')    
    vtkPointSetNormalFormLayout.addRow('Mode Type: ', self.modeTypeComboBox)
    
    self.numberOfNeighborsSlider = ctk.ctkSliderWidget()
    self.numberOfNeighborsSlider.setDecimals(0)
    self.numberOfNeighborsSlider.singleStep = 1
    self.numberOfNeighborsSlider.minimum = 1
    self.numberOfNeighborsSlider.maximum = 20
    self.numberOfNeighborsSlider.value = 4
    self.numberOfNeighborsSlider.setToolTip('')
    self.numberOfNeighborsSlider.enabled = False
    vtkPointSetNormalFormLayout.addRow('Fixed Neighbors: ', self.numberOfNeighborsSlider)
    
    self.radiusSlider = ctk.ctkSliderWidget()
    self.radiusSlider.setDecimals(2)
    self.radiusSlider.singleStep = 0.01
    self.radiusSlider.minimum = 1
    self.radiusSlider.maximum = 10
    self.radiusSlider.value = 1.0
    self.radiusSlider.setToolTip('')
    vtkPointSetNormalFormLayout.addRow('Radius: ', self.radiusSlider)
    
    self.graphTypeComboBox = qt.QComboBox()
    self.graphTypeComboBox.addItem('Riemann')  
    self.graphTypeComboBox.addItem('KNN')
    self.graphTypeComboBox.setCurrentIndex(1)
    self.graphTypeComboBox.setToolTip('')    
    vtkPointSetNormalFormLayout.addRow('Graph Type: ', self.graphTypeComboBox)
    
    self.knnSlider = ctk.ctkSliderWidget()
    self.knnSlider.setDecimals(0)
    self.knnSlider.singleStep = 1
    self.knnSlider.minimum = 1
    self.knnSlider.maximum = 20
    self.knnSlider.value = 5
    self.knnSlider.setToolTip('')
    vtkPointSetNormalFormLayout.addRow('K-Nearest Neighbors: ', self.knnSlider)
    
    self.vtkPointSetNormalButton = qt.QPushButton("Apply")
    self.vtkPointSetNormalButton.enabled = False
    self.vtkPointSetNormalButton.checkable = True
    vtkPointSetNormalFormLayout.addRow(self.vtkPointSetNormalButton)    

    # vtkPolyDataNormals
    self.vtkPolyDataNormalsWidget = qt.QWidget()
    vtkPolyDataNormalsFormLayout = qt.QFormLayout(self.vtkPolyDataNormalsWidget)
    normalsFormLayout.addRow(self.vtkPolyDataNormalsWidget)
    self.normalsTabWidget.addTab(self.vtkPolyDataNormalsWidget, "vtkPolyDataNormals") 
    
    self.normalsVisibleCheckBox = qt.QCheckBox('Normals Visibility: ')
    self.normalsVisibleCheckBox.checked = True
    self.normalsVisibleCheckBox.enabled = True
    self.normalsVisibleCheckBox.setLayoutDirection(1)
    normalsFormLayout.addRow(self.normalsVisibleCheckBox)
    
    # Compute Surface
    self.surfaceGroupBox = ctk.ctkCollapsibleGroupBox()
    self.surfaceGroupBox.setTitle("Compute Surface")
    surfaceFormLayout = qt.QFormLayout(self.surfaceGroupBox)
    pointSetProcessingFormLayout.addRow(self.surfaceGroupBox)

    self.surfaceTabWidget = qt.QTabWidget()
    surfaceFormLayout.addRow(self.surfaceTabWidget)
    
    # vtkPoissionReconstruction    
    self.vtkPoissionReconstructionWidget = qt.QWidget()
    vtkPoissionReconstructionFormLayout = qt.QFormLayout(self.vtkPoissionReconstructionWidget)
    surfaceFormLayout.addRow(self.vtkPoissionReconstructionWidget)
    self.surfaceTabWidget.addTab(self.vtkPoissionReconstructionWidget, "vtkPoissionReconstruction")   
    
    self.depthSlider = ctk.ctkSliderWidget()
    self.depthSlider.setDecimals(0)
    self.depthSlider.singleStep = 1
    self.depthSlider.minimum = 1
    self.depthSlider.maximum = 20
    self.depthSlider.value = 8
    self.depthSlider.setToolTip('This integer controls the reconstruction depth; the maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a voxel grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound.')
    vtkPoissionReconstructionFormLayout.addRow('Depth: ', self.depthSlider)
    
    self.scaleSlider = ctk.ctkSliderWidget()
    self.scaleSlider.setDecimals(2)
    self.scaleSlider.singleStep = 0.01
    self.scaleSlider.minimum = 1
    self.scaleSlider.maximum = 10
    self.scaleSlider.value = 1.25
    self.scaleSlider.setToolTip('This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples bounding cube.')
    vtkPoissionReconstructionFormLayout.addRow('Scale: ', self.scaleSlider)    
    
    self.solverDivideSlider = ctk.ctkSliderWidget()
    self.solverDivideSlider.setDecimals(0)
    self.solverDivideSlider.singleStep = 1
    self.solverDivideSlider.minimum = 1
    self.solverDivideSlider.maximum = 20
    self.solverDivideSlider.value = 8
    self.solverDivideSlider.setToolTip('Solver subdivision depth; This integer argument specifies the depth at which a block Gauss-Seidel solver is used to solve the Laplacian equation. Using this parameter helps reduce the memory overhead at the cost of a small increase in reconstruction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)')
    vtkPoissionReconstructionFormLayout.addRow('Solver Divide: ', self.solverDivideSlider)   
    
    self.isoDivideSlider = ctk.ctkSliderWidget()
    self.isoDivideSlider.setDecimals(0)
    self.isoDivideSlider.singleStep = 1
    self.isoDivideSlider.minimum = 1
    self.isoDivideSlider.maximum = 20
    self.isoDivideSlider.value = 8
    self.isoDivideSlider.setToolTip('Iso-surface extraction subdivision depth; This integer argument specifies the depth at which a block isosurface extractor should be used to extract the iso-surface. Using this parameter helps reduce the memory overhead at the cost of a small increase in extraction time. (In practice, we have found that for reconstructions of depth 9 or higher a subdivide depth of 7 or 8 can greatly reduce the memory usage.)')
    vtkPoissionReconstructionFormLayout.addRow('Iso Divide: ', self.isoDivideSlider)   
 
    self.samplesPerNodeSlider = ctk.ctkSliderWidget()
    self.samplesPerNodeSlider.setDecimals(2)
    self.samplesPerNodeSlider.singleStep = 0.1
    self.samplesPerNodeSlider.minimum = 1
    self.samplesPerNodeSlider.maximum = 30
    self.samplesPerNodeSlider.value = 1.0
    self.samplesPerNodeSlider.setToolTip('Minimum number of samples; This floating point value specifies the minimum number of sample points that should fall within an octree node as the octree construction is adapted to sampling density. For noise-free samples, small values in the range [1.0 - 5.0] can be used. For more noisy samples, larger values in the range [15.0 - 20.0] may be needed to provide a smoother, noise-reduced, reconstruction.')
    vtkPoissionReconstructionFormLayout.addRow('Samples per Node: ', self.samplesPerNodeSlider)   
    
    self.confidenceComboBox = qt.QComboBox()
    self.confidenceComboBox.addItem('False')
    self.confidenceComboBox.addItem('True')  
    self.confidenceComboBox.setToolTip('Enabling tells the reconstructor to use the size of the normals as confidence information. When the flag is not enabled, all normals are normalized to have unit-length prior to reconstruction.')    
    vtkPoissionReconstructionFormLayout.addRow('Confidence: ', self.confidenceComboBox)
   
    self.verboseComboBox = qt.QComboBox()
    self.verboseComboBox.addItem('False')
    self.verboseComboBox.addItem('True')  
    self.verboseComboBox.setToolTip('Enabling this flag provides a more verbose description of the running times and memory usages of individual components of the surface reconstructor.')    
    vtkPoissionReconstructionFormLayout.addRow('Verbose: ', self.verboseComboBox)
    
    self.vtkPoissionReconstructionButton = qt.QPushButton("Apply")
    self.vtkPoissionReconstructionButton.enabled = False
    self.vtkPoissionReconstructionButton.checkable = True
    vtkPoissionReconstructionFormLayout.addRow(self.vtkPoissionReconstructionButton)    

    # vtkDelaunay3D
    self.vtkDelaunay3DWidget = qt.QWidget()
    vtkPolyDataNormalsFormLayout = qt.QFormLayout(self.vtkDelaunay3DWidget)
    surfaceFormLayout.addRow(self.vtkDelaunay3DWidget)
    self.surfaceTabWidget.addTab(self.vtkDelaunay3DWidget, "vtkDelaunay3D") 
    
    self.surfaceVisibleCheckBox = qt.QCheckBox('Surface Visibility: ')
    self.surfaceVisibleCheckBox.checked = True
    self.surfaceVisibleCheckBox.enabled = True
    self.surfaceVisibleCheckBox.setLayoutDirection(1)
    surfaceFormLayout.addRow(self.surfaceVisibleCheckBox)
    
    # connections
    self.vtkPointSetNormalButton.connect('clicked(bool)', self.vtkPointSetNormalButtonClicked)
    self.vtkPoissionReconstructionButton.connect('clicked(bool)', self.vtkPoissionReconstructionClicked)
    self.inputSelector.connect('currentNodeChanged(vtkMRMLNode*)', self.onSelect)
    self.graphTypeComboBox.connect('currentIndexChanged(const QString &)', self.onGraphTypeChanged)
    self.modeTypeComboBox.connect('currentIndexChanged(const QString &)', self.onModeChanged)
    self.surfaceVisibleCheckBox.connect('stateChanged(int)', self.onSurfaceVisible)
    self.normalsVisibleCheckBox.connect('stateChanged(int)', self.onNormalsVisible)
            
    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh 
    self.onSelect()
        
    lm=slicer.app.layoutManager()
    lm.setLayout(4) # One 3D-view    

  def onSurfaceVisible(self, state):
    logic = PointSetProcessingPyLogic()
    logic.setModelVisibility('ComputedSurface', self.surfaceVisibleCheckBox.checked)
 
  def onNormalsVisible(self, state):
    logic = PointSetProcessingPyLogic()
    logic.setModelVisibility('ComputedNormals', self.normalsVisibleCheckBox.checked)
    
  def onGraphTypeChanged(self, type):
    if type == 'KNN':
      self.knnSlider.enabled = True
    elif type == 'Riemann':
      self.knnSlider.enabled = False

  def onModeChanged(self, type):
    if type == 'Radius':
      self.radiusSlider.enabled = True
      self.numberOfNeighborsSlider.enabled = False
    elif type == 'Fixed':
      self.radiusSlider.enabled = False
      self.numberOfNeighborsSlider.enabled = True
      
  def onSelect(self):
    self.vtkPointSetNormalButton.enabled = self.inputSelector.currentNode()
    self.vtkPoissionReconstructionButton.enabled = self.inputSelector.currentNode()

  def vtkPointSetNormalButtonClicked(self):
    if self.vtkPointSetNormalButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.vtkPointSetNormal(self.inputSelector.currentNode(), self.modeTypeComboBox.currentIndex, self.numberOfNeighborsSlider.value, self.radiusSlider.value, self.knnSlider.value, self.graphTypeComboBox.currentIndex, self.runtimeLabel)        
      self.vtkPointSetNormalButton.checked = False   
      
  def vtkPoissionReconstructionClicked(self):
    if self.vtkPoissionReconstructionButton.checked:
      logic = PointSetProcessingPyLogic()  
      logic.vtkPoissionReconstruction(self.inputSelector.currentNode(), self.depthSlider.value, self.scaleSlider.value, self.solverDivideSlider.value, self.isoDivideSlider.value, self.samplesPerNodeSlider.value, self.confidenceComboBox.currentIndex, self.verboseComboBox.currentIndex, self.runtimeLabel)
      self.vtkPoissionReconstructionButton.checked = False         

############################################################ PointSetProcessingPyLogic 
class PointSetProcessingPyLogic(ScriptedLoadableModuleLogic):

  def vtkPointSetNormal(self, inputModelNode, mode = 1, numberOfNeighbors = 4, radius = 1.0, kNearestNeighbors = 5, graphType = 1, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('ComputedNormals')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedNormals', [0, 1, 0])  
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeNormalsPointSetNormal(inputModelNode, outputModelNode, int(mode), int(numberOfNeighbors), float(radius), int(kNearestNeighbors), int(graphType), True, True)
    if runtimeLabel:
      runtimeLabel.setText('vtkPointSetNormal computed in  %.2f' % runtime + ' s.')
    return True
   
  def computeNormalsPolyDataNormals(self, inputModelNode, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('ComputedNormals')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedNormals', [0, 1, 0])  
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeNormalsPolyDataNormals(inputModelNode, outputModelNode)
    if runtimeLabel:
      runtimeLabel.setText('vtkPolyDataNormals computed in  %.2f' % runtime + ' s.')
    return True
   
  def computeSurfaceDelaunay3D(self, inputModelNode, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('ComputedSurface')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedSurface', [1, 0, 0])
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeSurfaceDelaunay3D(inputModelNode, outputModelNode)
    if runtimeLabel:
      runtimeLabel.setText('vtkDelaunay3D computed in %.2f' % runtime + ' s.')
    return True

  def vtkPoissionReconstruction(self, inputModelNode, depth = 8, scale = 1.25, solverDivide = 8, isoDivide = 8, samplesPerNode = 1.0, confidence = 0, verbose = 0, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('ComputedSurface')
    if not outputModelNode:
      outputModelNode = self.createModelNode('ComputedSurface', [1, 0, 0])
    runtime = slicer.modules.pointsetprocessingcpp.logic().ComputeSurfacePoissionReconstruction(inputModelNode, outputModelNode, int(depth), float(scale), int(solverDivide), int(isoDivide), float(samplesPerNode), int(confidence), int(verbose), True)
    if runtimeLabel:
      runtimeLabel.setText('vtkPoissionReconstruction computed in %.2f' % runtime + ' s.')
    return True
    
  def setModelVisibility(self, name, visible):
    modelNode = slicer.util.getNode(name)
    if modelNode:  
      modelNode.SetDisplayVisibility(visible)
    
  def createModelNode(self, name, color):
    scene = slicer.mrmlScene
    modelNode = slicer.vtkMRMLModelNode()
    modelNode.SetScene(scene)
    modelNode.SetName(name)
    modelDisplay = slicer.vtkMRMLModelDisplayNode()
    modelDisplay.SetColor(color)
    modelDisplay.SetScene(scene)
    scene.AddNode(modelDisplay)
    modelNode.SetAndObserveDisplayNodeID(modelDisplay.GetID())
    scene.AddNode(modelNode)  
    return modelNode
    
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
    self.assertTrue(logic.computeNormals(inputModelNode))        
    self.assertTrue(logic.computeSurface(inputModelNode))        
    self.delayDisplay('Testing module passed!')    
