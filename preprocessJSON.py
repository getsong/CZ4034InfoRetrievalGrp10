import json
from preprocess import Preprocessor


class PreprocessJSON:
    def preprocess(self, inputPath, outputPath):
        with open(inputPath, 'r') as inFile:
            records = json.load(inFile)

        processedRecords = []
