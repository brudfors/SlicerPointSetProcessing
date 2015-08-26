/*==============================================================================

  Program: 3D Slicer

  Portions (c) Copyright Brigham and Women's Hospital (BWH) All Rights Reserved.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

==============================================================================*/

// PointSetProcessingCpp Logic includes
#include "vtkSlicerPointSetProcessingCppLogic.h"

// MRML includes
#include <vtkMRMLModelNode.h>
#include <vtkMRMLScene.h>

// VTK includes
#include <vtkIntArray.h>
#include <vtkNew.h>
#include <vtkObjectFactory.h>
#include <vtkTimerLog.h>

// STD includes
#include <cassert>

#include <vtkPointSetNormalEstimation.h>
#include <vtkPointSetNormalOrientation.h>
#include <vtkPoissonReconstruction.h>

//----------------------------------------------------------------------------
vtkStandardNewMacro(vtkSlicerPointSetProcessingCppLogic);

//----------------------------------------------------------------------------
vtkSlicerPointSetProcessingCppLogic::vtkSlicerPointSetProcessingCppLogic()
{
}

//----------------------------------------------------------------------------
vtkSlicerPointSetProcessingCppLogic::~vtkSlicerPointSetProcessingCppLogic()
{
}

//----------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::SetMRMLSceneInternal(vtkMRMLScene * newScene)
{
  vtkNew<vtkIntArray> events;
  events->InsertNextValue(vtkMRMLScene::NodeAddedEvent);
  events->InsertNextValue(vtkMRMLScene::NodeRemovedEvent);
  events->InsertNextValue(vtkMRMLScene::EndBatchProcessEvent);
  this->SetAndObserveMRMLSceneEventsInternal(newScene, events.GetPointer());
}

//-----------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::RegisterNodes()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic::UpdateFromMRMLScene()
{
  assert(this->GetMRMLScene() != 0);
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic
::OnMRMLSceneNodeAdded(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
void vtkSlicerPointSetProcessingCppLogic
::OnMRMLSceneNodeRemoved(vtkMRMLNode* vtkNotUsed(node))
{
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::PointSetProcessingConnector(vtkMRMLModelNode* input, 
                              vtkMRMLModelNode* output,
                              int kNearestNeighbors, 
                              int depth, 
                              unsigned int graphType)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::PointSetProcessingConnector");

  vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
  timer->StartTimer();

	vtkPolyData* inputPolyData = input->GetPolyData();
	
  // vtkPointSetNormalEstimation
  vtkSmartPointer<vtkPointSetNormalEstimation> normalEstimation = vtkSmartPointer<vtkPointSetNormalEstimation>::New();
  normalEstimation->SetInputData(inputPolyData);

  // vtkPointSetNormalOrientation
  vtkSmartPointer<vtkPointSetNormalOrientation> normalOrientationFilter = vtkSmartPointer<vtkPointSetNormalOrientation>::New();
  normalOrientationFilter->SetInputConnection(normalEstimation->GetOutputPort()); 
  if (graphType == vtkPointSetNormalOrientation::KNN_GRAPH)
  {
    normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::KNN_GRAPH);
  }
  else if (graphType == vtkPointSetNormalOrientation::RIEMANN_GRAPH)
  {
    normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::RIEMANN_GRAPH);
  }
  else
  {
    vtkWarningMacro("Invalid graphType! Got ' + graphType + ' should be either 0 (RIEMANN_GRAPH) or 1 (KNN_GRAPH).");
    return 0;
  }
  normalOrientationFilter->SetKNearestNeighbors(kNearestNeighbors);

  // vtkPoissonReconstruction
  vtkSmartPointer<vtkPoissonReconstruction> poissonFilter = vtkSmartPointer<vtkPoissonReconstruction>::New();
  poissonFilter->SetDepth(depth);
  poissonFilter->SetInputConnection(normalOrientationFilter->GetOutputPort());
  poissonFilter->Update();	

  output->SetAndObservePolyData(poissonFilter->GetOutput());

  timer->StopTimer();
  float runtime = timer->GetElapsedTime();
  return runtime;
}