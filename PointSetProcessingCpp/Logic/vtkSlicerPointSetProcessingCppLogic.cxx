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
#include <vtkCellData.h>
#include <vtkDoubleArray.h>
#include <vtkFloatArray.h>
#include <vtkIntArray.h>
#include <vtkNew.h>
#include <vtkObjectFactory.h>
#include <vtkPointData.h>
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
::ComputeNormals(vtkMRMLModelNode* input, unsigned int mode, unsigned int numberOfNeighbors, float radius, int kNearestNeighbors, unsigned int graphType)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::ComputeNormals");

  vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
  timer->StartTimer();
	
  // vtkPointSetNormalEstimation
  vtkSmartPointer<vtkPointSetNormalEstimation> normalEstimation = vtkSmartPointer<vtkPointSetNormalEstimation>::New();
  normalEstimation->SetInputData(input->GetPolyData());
  if (mode == vtkPointSetNormalEstimation::FIXED_NUMBER)
  {
    normalEstimation->SetModeToFixedNumber();
    normalEstimation->SetNumberOfNeighbors(numberOfNeighbors);
  }
  else if (mode == vtkPointSetNormalEstimation::RADIUS)
  {
    normalEstimation->SetModeToRadius();
    normalEstimation->SetRadius(radius);
  }
  else
  {
    vtkWarningMacro("Invalid mode! Should be either 0 (FIXED_NUMBER) or 1 (RADIUS).");
    return 0;
  }

  // vtkPointSetNormalOrientation
  vtkSmartPointer<vtkPointSetNormalOrientation> normalOrientationFilter = vtkSmartPointer<vtkPointSetNormalOrientation>::New();
  normalOrientationFilter->SetInputConnection(normalEstimation->GetOutputPort()); 
  if (graphType == vtkPointSetNormalOrientation::KNN_GRAPH)
  {
    normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::KNN_GRAPH);
    normalOrientationFilter->SetKNearestNeighbors(kNearestNeighbors);
  }
  else if (graphType == vtkPointSetNormalOrientation::RIEMANN_GRAPH)
  {
    normalOrientationFilter->SetGraphFilterType(vtkPointSetNormalOrientation::RIEMANN_GRAPH);
  }
  else
  {
    vtkWarningMacro("Invalid graphType! Should be either 0 (RIEMANN_GRAPH) or 1 (KNN_GRAPH).");
    return 0;
  }

  normalOrientationFilter->Update();	

  input->SetAndObservePolyData(normalOrientationFilter->GetOutput());

  timer->StopTimer();
  float runtime = timer->GetElapsedTime();
  return runtime;
}

//---------------------------------------------------------------------------
float vtkSlicerPointSetProcessingCppLogic
::ComputeSurface(vtkMRMLModelNode* input, vtkMRMLModelNode* output, int depth, float scale, int solverDivide, int isoDivide, float samplesPerNode, int confidence, int verbose)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::ComputeSurface");

  vtkSmartPointer<vtkTimerLog> timer = vtkSmartPointer<vtkTimerLog>::New();
  timer->StartTimer();

  // vtkPoissonReconstruction
  vtkSmartPointer<vtkPoissonReconstruction> poissonFilter = vtkSmartPointer<vtkPoissonReconstruction>::New();
  poissonFilter->SetInputData(input->GetPolyData());
  poissonFilter->SetDepth(depth);
  poissonFilter->SetScale(scale);
  poissonFilter->SetSolverDivide(solverDivide); 
  poissonFilter->SetIsoDivide(isoDivide); 
  poissonFilter->SetSamplesPerNode(samplesPerNode);
  poissonFilter->SetConfidence(confidence); 
  poissonFilter->SetVerbose(verbose);   
  poissonFilter->Update();	

  output->SetAndObservePolyData(poissonFilter->GetOutput());

  timer->StopTimer();
  float runtime = timer->GetElapsedTime();
  return runtime;
}

//---------------------------------------------------------------------------
// From: http://www.paraview.org/Wiki/VTK/Examples/Cxx/PolyData/PolyDataExtractNormals
bool vtkSlicerPointSetProcessingCppLogic
::HasPointNormals(vtkMRMLModelNode* input)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::HasPointNormals");

	vtkPolyData* polydata = input->GetPolyData();

  std::cout << "In GetPointNormals: " << polydata->GetNumberOfPoints() << std::endl;
  std::cout << "Looking for point normals..." << std::endl;
 
  // Count points
  vtkIdType numPoints = polydata->GetNumberOfPoints();
  std::cout << "There are " << numPoints << " points." << std::endl;
 
  // Count triangles
  vtkIdType numPolys = polydata->GetNumberOfPolys();
  std::cout << "There are " << numPolys << " polys." << std::endl;
 
  ////////////////////////////////////////////////////////////////
  // Double normals in an array
  vtkDoubleArray* normalDataDouble = vtkDoubleArray::SafeDownCast(polydata->GetPointData()->GetArray("Normals"));
 
  if(normalDataDouble)
  {
    int nc = normalDataDouble->GetNumberOfTuples();
    std::cout << "There are " << nc << " components in normalDataDouble" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Double normals in an array
  vtkFloatArray* normalDataFloat = vtkFloatArray::SafeDownCast(polydata->GetPointData()->GetArray("Normals"));
 
  if(normalDataFloat)
  {
    int nc = normalDataFloat->GetNumberOfTuples();
    std::cout << "There are " << nc << " components in normalDataFloat" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Point normals
  vtkDoubleArray* normalsDouble = vtkDoubleArray::SafeDownCast(polydata->GetPointData()->GetNormals());
 
  if(normalsDouble)
  {
    std::cout << "There are " << normalsDouble->GetNumberOfComponents() << " components in normalsDouble" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Point normals
  vtkFloatArray* normalsFloat = vtkFloatArray::SafeDownCast(polydata->GetPointData()->GetNormals());
 
  if(normalsFloat)
  {
    std::cout << "There are " << normalsFloat->GetNumberOfComponents() << " components in normalsFloat" << std::endl;
    return true;
  }
 
  /////////////////////////////////////////////////////////////////////
  // Generic type point normals
  vtkDataArray* normalsGeneric = polydata->GetPointData()->GetNormals(); 
  if(normalsGeneric)
  {
    std::cout << "There are " << normalsGeneric->GetNumberOfTuples() << " normals in normalsGeneric" << std::endl;
 
    double testDouble[3];
    normalsGeneric->GetTuple(0, testDouble);
 
    std::cout << "Double: " << testDouble[0] << " " << testDouble[1] << " " << testDouble[2] << std::endl;
    return true;
  }
 
 
  // If the function has not yet quit, there were none of these types of normals
  std::cout << "Normals not found!" << std::endl;
  return false;
}

//---------------------------------------------------------------------------
// From: http://www.paraview.org/Wiki/VTK/Examples/Cxx/PolyData/PolyDataExtractNormals
bool vtkSlicerPointSetProcessingCppLogic
::HasCellNormals(vtkMRMLModelNode* input)
{
  vtkInfoMacro("vtkSlicerPointSetProcessingCppLogic::HasCellNormals");

	vtkPolyData* polydata = input->GetPolyData();

  std::cout << "Looking for cell normals..." << std::endl;
 
  // Count points
  vtkIdType numCells = polydata->GetNumberOfCells();
  std::cout << "There are " << numCells << " cells." << std::endl;
 
  // Count triangles
  vtkIdType numPolys = polydata->GetNumberOfPolys();
  std::cout << "There are " << numPolys << " polys." << std::endl;
 
  ////////////////////////////////////////////////////////////////
  // Double normals in an array
  vtkDoubleArray* normalDataDouble = vtkDoubleArray::SafeDownCast(polydata->GetCellData()->GetArray("Normals"));
 
  if(normalDataDouble)
  {
    int nc = normalDataDouble->GetNumberOfTuples();
    std::cout << "There are " << nc << " components in normalDataDouble" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Double normals in an array
  vtkFloatArray* normalDataFloat = vtkFloatArray::SafeDownCast(polydata->GetCellData()->GetArray("Normals"));
 
  if(normalDataFloat)
  {
    int nc = normalDataFloat->GetNumberOfTuples();
    std::cout << "There are " << nc << " components in normalDataFloat" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Point normals
  vtkDoubleArray* normalsDouble = vtkDoubleArray::SafeDownCast(polydata->GetCellData()->GetNormals());
 
  if(normalsDouble)
  {
    std::cout << "There are " << normalsDouble->GetNumberOfComponents() << " components in normalsDouble" << std::endl;
    return true;
  }
 
  ////////////////////////////////////////////////////////////////
  // Point normals
  vtkFloatArray* normalsFloat = vtkFloatArray::SafeDownCast(polydata->GetCellData()->GetNormals());
 
  if(normalsFloat)
  {
    std::cout << "There are " << normalsFloat->GetNumberOfComponents() << " components in normalsFloat" << std::endl;
    return true;
  }
 
  /////////////////////////////////////////////////////////////////////
  // Generic type point normals
  vtkDataArray* normalsGeneric = polydata->GetCellData()->GetNormals();
  if(normalsGeneric)
  {
    std::cout << "There are " << normalsGeneric->GetNumberOfTuples()
              << " normals in normalsGeneric" << std::endl;
 
    double testDouble[3];
    normalsGeneric->GetTuple(0, testDouble);
 
    std::cout << "Double: " << testDouble[0] << " " << testDouble[1] << " " << testDouble[2] << std::endl;

    return true;
  }

  // If the function has not yet quit, there were none of these types of normals
  std::cout << "Normals not found!" << std::endl;
  return false;
}