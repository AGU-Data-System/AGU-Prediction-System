package aguPredictionSystem.server.http

import aguPredictionSystem.server.http.models.PredictionInputModel
import aguPredictionSystem.server.http.models.PredictionOutputModel
import aguPredictionSystem.server.utils.InvokeScripts.invokePredictionAlgorithm
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

/**
 * Controller for the prediction endpoint.
 */
@RestController("Prediction")
@RequestMapping(URIs.Prediction.ROOT)
class PredictionController {

	/**
	 * Generates a prediction for the given AGU.
	 */
	@PostMapping
	fun generatePrediction(
		@RequestBody predictionInputModel: PredictionInputModel
	): ResponseEntity<*> {
		return when (val result = invokePredictionAlgorithm(
			predictionInputModel.temperatures,
			predictionInputModel.previousConsumptions,
			predictionInputModel.coefficients,
			predictionInputModel.intercept
		)) {
			ERROR_IDENTITY -> ResponseEntity.badRequest().body(ERROR_MESSAGE)
			else -> ResponseEntity.ok(PredictionOutputModel(result))
		}
	}

	companion object {
		private const val ERROR_IDENTITY = "ERROR"
		private const val ERROR_MESSAGE = "Error while predicting the consumption"
	}
}
