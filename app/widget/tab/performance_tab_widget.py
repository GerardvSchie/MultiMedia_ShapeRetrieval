from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.util import color_widget, create_header_label
from app.widget.settings_widget import SettingsWidget
from app.widget.visualization_widget import VisualizationWidget

from src.database.querier import CustomFeatureDatabaseQuerier
from src.object.settings import Settings
from src.object.shape import Shape
from src.pipeline.compute_descriptors import compute_descriptors
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.pipeline.feature_extractor.shape_properties_extractor import ShapePropertyExtractor
from src.pipeline.normalization_pipeline import NormalizationPipeline

from src.util.configs import *


class PerformanceTabWidget(QWidget):
    def __init__(self):
        # super allows PerformanceTabWidget to inherit from QWidget
        super(PerformanceTabWidget, self).__init__()

        # Color of ?
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.pipeline = NormalizationPipeline()

        # We have 2 DatabaseQueriers in querier.py.
        # self.querier = DatabaseQuerier(os.path.join(DATABASE_REFINED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        self.querier = CustomFeatureDatabaseQuerier(
            os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME),
            os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME)
        )

        # Load widget
        self.query_scene_widget = VisualizationWidget(self.settings)
        window = QWindow.fromWinId(self.query_scene_widget.hwnd)
        window_container = self.createWindowContainer(window, self.query_scene_widget)

        #self.query_performance_results_widgets: [QueryResultWidget] = []
        self.query_performance_results_widgets = []

        # performance_results_layout = QGridLayout()
        # for i in range(QueryTabWidget.NR_RESULTS):
        #     query_widget = QueryResultWidget(f'Result {i+1}', self.settings)
        #     self.query_result_widgets.append(query_widget)
        #     performance_results_layout.addWidget(query_widget, int(i / QueryTabWidget.RESULTS_PER_ROW), i % QueryTabWidget.RESULTS_PER_ROW, 1, 1)

        # Connect the settings to the widget
        self.scene_widgets = [self.query_scene_widget] #+ [widget.scene_widget for widget in self.query_result_widgets]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        left_layout = QVBoxLayout()

        # Changes the text above the shape display area.
        left_layout.addWidget(create_header_label("Query item"))

        # The white area where the shape is displayed.
        left_layout.addWidget(window_container)

        # Makes sure that the display area isn't too big?
        # Or also displays the options underneath the area.
        left_layout.addWidget(self.settings_widget)

        # QHBox, when also having the grid_layout, makes sure they both fit in the viewer?
        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)

        # Originally used for the first 5 results of query_tab
        #layout.addLayout(performance_results_layout)
        self.setLayout(layout)


    # Taken from query_tab_widget
    def load_shape_from_path(self, file_path: str):
        # Load + normalize shape
        self.query_scene_widget.load_shape_from_path(file_path)
        normalized_shape = self.pipeline.normalize_shape(file_path)

        # Extract data
        ShapeFeatureExtractor.extract_all_shape_features(normalized_shape)
        compute_descriptors(normalized_shape)
        ShapePropertyExtractor.shape_propertizer(normalized_shape)

        # Compute the top X shapes
        queried_shape_paths, distances = self.querier.calc_distances_row(normalized_shape)

        # self.querier.query_descriptor returns top k paths and distances.
        # CustomFeatureDatabaseQuerier returns regular top k.
        # DatabaseQuerier returns top k using ANN.

        print(f'queried_shape_paths has {len(queried_shape_paths)} elements:\n {np.array(queried_shape_paths)}\n')
        #prin()

        # Now that we have our top k results, we calculate our TP, FP, etc.
        self.calculate_measure_values(normalized_shape.features.true_class, queried_shape_paths)


    def calculate_measure_values(self, queryTrueClass, retrievedShapes):
        truePositives, trueNegatives, falsePositives, falseNegatives = [0, 0, 0, 0]

        #print(f'retrieved Shapes:\n{np.array(retrievedShapes)}')

        # Evaluation must be done per class and over the entire database.

        # TP + FN + FP + TN
        totalNumberOfItems = NR_SHAPES

        # In LabeledDB, we know there are 19 classes, each with 20 Shapes.
        #numberOfShapesPerClass = NR_RESULTS
        numberOfShapesPerClass = NR_ITEMS_PER_CATEGORY

        # The retrieved Shapes are our positives.
        # Any Shapes (of the same class or in entire database?) not returned are our negatives.

        # TP + FP
        # Retrieved items are all our positive guesses, guesses may be incorrect.
        numberOfRetrievedItems = len(retrievedShapes)

        # k from top k should be 20 for evaluation.
        assert(numberOfRetrievedItems == numberOfShapesPerClass)

        # true_class in the query item is what we query for.
        for item in retrievedShapes:
            # We can get the true class from the path as well.
            pathElements = item.split("\\")
            currentClass = pathElements[2]

            #print(f'testList = {np.array(pathElements)}')
            #print(f'currentClass = {currentClass}')

            #print(f'We got a Shape at {item} and with {currentClass} as the true class.')

            # The retrieved Shape has the same class as the query Shape.
            # We have a True Positive
            if (queryTrueClass == currentClass):
                truePositives += 1
                print(f'{queryTrueClass} == {currentClass} --> Found a True Positive')
            # The retrieved Shape has a different class than the query Shape.
            # We have a False Positive.
            else:
                falsePositives += 1
                print(f'{queryTrueClass} != {currentClass} --> Found a False Positive')

        #prin()

        # FN:
        # Size of the class of the query minus the number of true positives A.K.A.
        # The number of shapes in the database having label C(Query) - TP. 
        falseNegatives = numberOfShapesPerClass - truePositives

        # TP + FN
        # Relevant items are all the correct Shapes for the query, correct shapes may be incorrectly labeled.
        numberOfRelevantItems = truePositives + falseNegatives
        
        # TN are all wrong Shapes not returned.
        trueNegatives = totalNumberOfItems - numberOfRetrievedItems - falseNegatives


        accuracy = (truePositives + trueNegatives) / totalNumberOfItems

        precision = truePositives / numberOfRetrievedItems
        recall = truePositives / numberOfRelevantItems

        sensitivity = recall
        specificity = truePositives / (totalNumberOfItems - numberOfRelevantItems)

        print(f'\nResults for {numberOfRetrievedItems} retrieved Shapes:')
        print(f'TP = {truePositives}')
        print(f'FP = {falsePositives}')
        print(f'TN = {trueNegatives}')
        print(f'FN = {falseNegatives}')


        print(f'\naccuracy = {accuracy}')
        print("{:.0%}".format(accuracy))

        print(f'\nprecision = {precision}')
        print("{:.0%}".format(precision))
        print(f'recall = {recall}')
        print("{:.0%}".format(recall))

        print(f'\nsensitivity = {sensitivity}')
        print("{:.0%}".format(sensitivity))
        print(f'specificity = {specificity}')
        print("{:.0%}".format(specificity))

        #prin()

        # TODO
        # Show plots