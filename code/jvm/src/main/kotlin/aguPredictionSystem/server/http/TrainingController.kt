package aguPredictionSystem.server.http

import aguPredictionSystem.server.utils.InvokeScripts.invokeTrainingAlgorithm
import aguPredictionSystem.server.http.models.TrainingInputModel
import aguPredictionSystem.server.http.models.TrainingOutputModel
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

/**
 * Controller for the training endpoint.
 */
@RestController(URIs.Train.ROOT)
class TrainingController {

	/**
	 * Generates a training for the given AGU.
	 */
	@PostMapping
	fun generateTraining(
		@RequestBody trainingInputModel: TrainingInputModel
	): ResponseEntity<*> {
		val result = invokeTrainingAlgorithm(
			trainingInputModel.consumptions,
			trainingInputModel.temperatures
		)

		return ResponseEntity.ok(TrainingOutputModel(result))
	}
}
