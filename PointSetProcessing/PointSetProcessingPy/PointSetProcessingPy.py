import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

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

class PointSetProcessingPyWidget(ScriptedLoadableModuleWidget):
  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    poissonCollapsibleButton = ctk.ctkCollapsibleButton()
    poissonCollapsibleButton.text = "Poisson Surface Reconstruction"
    self.layout.addWidget(poissonCollapsibleButton)
    poissonFormLayout = qt.QFormLayout(poissonCollapsibleButton)

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
    poissonFormLayout.addRow("Input Model: ", self.inputSelector)

    self.parametersOutputGroupBox = ctk.ctkCollapsibleGroupBox()
    self.parametersOutputGroupBox.setTitle("Parameters")
    parametersOutputFormLayout = qt.QFormLayout(self.parametersOutputGroupBox)
    poissonFormLayout.addRow(self.parametersOutputGroupBox)
    
    self.depthSlider = ctk.ctkSliderWidget()
    self.depthSlider.setDecimals(0)
    self.depthSlider.singleStep = 1
    self.depthSlider.minimum = 1
    self.depthSlider.maximum = 20
    self.depthSlider.value = 10
    parametersOutputFormLayout.addRow('Depth: ', self.depthSlider)

    self.knnSlider = ctk.ctkSliderWidget()
    self.knnSlider.setDecimals(0)
    self.knnSlider.singleStep = 1
    self.knnSlider.minimum = 1
    self.knnSlider.maximum = 20
    self.knnSlider.value = 3
    parametersOutputFormLayout.addRow('Nearest Neighbors: ', self.knnSlider)
    
    self.graphTypeComboBox = qt.QComboBox()
    self.graphTypeComboBox.addItem('KNN')
    self.graphTypeComboBox.addItem('Riemann')        
    parametersOutputFormLayout.addRow('Graph Type: ', self.graphTypeComboBox)
    
        # Runtime
    self.runtimeGroupBox = ctk.ctkCollapsibleGroupBox()
    self.runtimeGroupBox.setTitle("Runtime")
    runtimeFormLayout = qt.QFormLayout(self.runtimeGroupBox)
    poissonFormLayout.addRow(self.runtimeGroupBox)
    
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
    
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    self.applyButton.checkable = True
    poissonFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh selector
    self.onSelect()
    
  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode()

  def onApplyButton(self):
    if self.applyButton.checked:
      logic = PointSetProcessingPyLogic()
      logic.apply(self.inputSelector.currentNode(), self.knnSlider.value, self.depthSlider.value, self.graphTypeComboBox.currentText, self.runtimeLabel)
      self.applyButton.checked = False   

class PointSetProcessingPyLogic(ScriptedLoadableModuleLogic):

  def apply(self, inputModelNode, kNearestNeighbors, depth, graphTypeText, runtimeLabel = None):
    outputModelNode = slicer.util.getNode('PointSetProcessingOutput')
    if not outputModelNode:
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
    if graphTypeText == 'Riemann':
      graphType = 0
    elif graphTypeText == 'KNN':
      graphType = 1
    runtime = slicer.modules.pointsetprocessingcpp.logic().PointSetProcessingConnector(inputModelNode, outputModelNode, int(kNearestNeighbors), int(depth), graphType)
    if runtimeLabel:
      runtimeLabel.setText('%.2f' % runtime + ' s.')