import json

class Annotator():

    def __init__(self, url, userPin):
        # Database Structure: annotationDB ->
        #self.dbClient = MongoClient('localhost', 27017)
        #self.userData = dbClient.userData #decide what I need to take in off the Database from Pre-Survey
            #most likely just political leaning score... in order to determine whether they get a liberal or conservative context author

        self.url = url
        self.userPin = userPin
        self.studyGroup = self._determineStudyGroup()
        self.materialFile = self._determineMaterial()
        self.sourceFile = self._determineSource()

    def getDataObject(self):
        #switch on studyGroup
        #GROUPS:
        # CONTROL -- no extension downloaded
        # FACTUAL -- "n_political_left_factual.JSON, n_political_right_factual.JSON, n_technical_factual.JSON"
        #           "s_political_left_factual.JSON, s_political_right_factual.JSON, s_technical_factual.JSON"
        # CONTEXT -- "n_political_left_context.JSON, n_political_right_context.JSON, n_technical_context.JSON"
        #           "s_political_left_context.JSON, s_political_right_context.JSON, s_technical_context.JSON"
        # SOURCE -- "factual_source.JSON, auto_source.JSON, expert_source.JSON, political_left_source.JSON,
        #           politcal_right_source.JSON, peer_source.JSON"

        #make sure that the "source" is dynamically passed into the CONTEXT GROUP.

        #outputs dictionary in this format
        #source: info about the source... comes as a separate JSON object
        #material: the annotations... structure tbd

        #(n -> news; s -> social media)
        materialFileNames = [   "annotations/n_political_left_factual.JSON",
                                "annotations/s_political_left_factual.JSON",
                                "annotations/n_political_right_factual.JSON",
                                "annotations/s_political_right_factual.JSON",
                                "annotations/n_technical_factual.JSON",
                                "annotations/s_technical_factual.JSON",
                                "annotations/n_political_left_context.JSON",
                                "annotations/s_political_left_context.JSON",
                                "annotations/n_political_right_context.JSON",
                                "annotations/s_political_right_context.JSON",
                                "annotations/n_technical_context.JSON",
                                "annotations/s_technical_context.JSON",
                                "annotations/sample_annotations.JSON"]

        sourceFileNames = [     "annotations/factual_source.JSON",
                                "annotations/auto_source.JSON",
                                "annotations/expert_source.JSON",
                                "annotations/political_left_source.JSON",
                                "annotations/political_right_source.JSON",
                                "annotations/peer_source.JSON",
                                "annotations/sample_source.JSON"]

        #SWITCH ON urL AND STUDY PIN
        openMaterial = materialFileNames[self.materialFile]
        openSource = sourceFileNames[self.sourceFile]
        with open(openMaterial, 'r') as material_file:
            materialObject = json.load(material_file)
        with open(openSource, 'r') as source_file:
            sourceObject = json.load(source_file)

        returnObject = {
            "annotations": materialObject,
            "source": sourceObject
        }

        return returnObject

    def _determineSource(self):
        if self.studyGroup == "testing":
            return 6
        else:
            return -1

    def _determineMaterial(self):
        if self.studyGroup == "testing":
            return 12
        else:
            return -1

    def _determineStudyGroup(self):
        if self.userPin == "12874":
            return "testing"
        else:
            return "error"
