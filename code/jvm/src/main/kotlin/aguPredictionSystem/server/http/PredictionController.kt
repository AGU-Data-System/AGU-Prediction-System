package aguPredictionSystem.server.http

import aguPredictionSystem.server.InvokeScripts.invokePredictionAlgorithm
import aguPredictionSystem.server.http.models.PredictionInputModel
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

/**
 * Controller for the prediction endpoint.
 */
@RestController(URIs.PREDICT)
class PredictionController {

	/**
	 * Generates a prediction for the given AGU.
	 */
	@PostMapping(URIs.BY_ID)
	fun generatePrediction(
		@PathVariable aguCui: String,
		@RequestBody predictionInputModel: PredictionInputModel
	): ResponseEntity<*> {
		val result = invokePredictionAlgorithm(
			predictionInputModel.temperatures,
			predictionInputModel.previousConsumptions,
			predictionInputModel.coefficients,
			predictionInputModel.intercept
		)
		return ResponseEntity.ok(result)
	}
}
