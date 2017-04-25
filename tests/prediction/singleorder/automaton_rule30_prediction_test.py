from collections import deque

import unittest2 as unittest
import automatatron

from nupic.frameworks.opf.model_factory import ModelFactory

import rule_30_model_params


PREDICTED_FIELD = "bit_10"
RULE_NUMBER = 30


class Rule30AutomataPredictionTest(unittest.TestCase):



  def test_rule30_prediction_is_perfect_after_600_iterations(self):
    """
    Generates Rule 30 elementary cellular automaton and passes it through NuPIC.
    Asserts that predictions are perfect after X rows of data.
    """
    iterations = 600
    model = ModelFactory.create(rule_30_model_params.MODEL_PARAMS)
    model.enableInference({"predictedField": PREDICTED_FIELD})
    prediction_history = deque(maxlen=500)
    counter = [0]
    last_prediction = [None]

    def stream_handler(row, _):
      counter[0] += 1
      input_row = {}
      for index, field in enumerate(row):
        input_row["bit_%i" % index] = str(field)

      prediction = last_prediction[0]
      predicted_index = int(PREDICTED_FIELD.split("_").pop())
      value = str(row[predicted_index])
      correct = (value == prediction)
      count = counter[0]

      if correct:
        prediction_history.append(1.0)
      else:
        prediction_history.append(0.0)

      correctness = reduce(lambda x, y: x + y,
                           prediction_history) / len(prediction_history)

      if count == iterations:
        unittest.TestCase.assertEqual(
          self, 1.0, correctness,
          "Predictions should be 100 percent correct after reaching %i "
          "iterations." % iterations
        )

      result = model.run(input_row)

      prediction = result.inferences["multiStepBestPredictions"][1]
      last_prediction[0] = prediction

    automaton = automatatron.Engine(RULE_NUMBER)
    automaton.run(handler=stream_handler, width=21, iterations=iterations)


if __name__ == "__main__":
  unittest.main()
