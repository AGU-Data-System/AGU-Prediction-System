package aguPredictionSystem.server.http

import aguPredictionSystem.server.InvokeScripts.invokeTrainingAlgorithm
import aguPredictionSystem.server.http.models.TrainingInputModel
import aguPredictionSystem.server.http.models.TrainingOutputModel
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController

/**
 * Controller for the training endpoint.
 */
@RestController
class TrainingController {

	/**
	 * Generates a training for the given AGU.
	 */
	@PostMapping(URIs.Train.BY_ID)
	fun generateTraining(
		@PathVariable aguCui: String,
		@RequestBody trainingInputModel: TrainingInputModel
	): ResponseEntity<*> {
		val result = invokeTrainingAlgorithm(
			trainingInputModel.consumptions,
			trainingInputModel.temperatures
		)

		return ResponseEntity.ok(TrainingOutputModel(result))
	}
}
