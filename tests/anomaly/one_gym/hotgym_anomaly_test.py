import datetime
import unittest2 as unittest
import csv
from nupic.frameworks.opf.model_factory import ModelFactory
import rec_center_hourly_model_params


CSV_DATA = "tests/anomaly/one_gym/rec-center-hourly.csv"
DATE_FORMAT = "%m/%d/%y %H:%M"
START_AT_ROW = 110
ANOMALY_THRESHOLD = 0.5



class AnomalyTest(unittest.TestCase):



  def test_hotgym_anomalyScore_stays_below_50_perc_after_110_rows(self):
    """
    Tests that the hotgym anomalyScore values stays below 50% after feeding in
    110 rows of data.
    """
    model = ModelFactory.create(rec_center_hourly_model_params.MODEL_PARAMS)
    model.enableInference({"predictedField": "kw_energy_consumption"})
    inputFile = open(CSV_DATA, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()

    rowCount = 0

    for row in csvReader:
      rowCount += 1
      timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
      consumption = float(row[1])
      result = model.run({
        "timestamp": timestamp,
        "kw_energy_consumption": consumption
      })
      anomalyScore = result.inferences["anomalyScore"]
      print "row %i: %f" % (rowCount, anomalyScore)
      if rowCount >= START_AT_ROW:
        unittest.TestCase.assertGreater(self, ANOMALY_THRESHOLD, anomalyScore,
            "Anomaly score exceeded threshold of %f after %i rows of data." % (
            ANOMALY_THRESHOLD, rowCount))
        break

    inputFile.close()



if __name__ == "__main__":
  unittest.main()
