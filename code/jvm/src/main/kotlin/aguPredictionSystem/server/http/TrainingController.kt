package aguPredictionSystem.server.http

import aguPredictionSystem.server.http.models.TrainingInputModel
import aguPredictionSystem.server.http.models.TrainingOutputModel
import aguPredictionSystem.server.utils.InvokeScripts.invokeTrainingAlgorithm
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

/**
 * Controller for the training endpoint.
 */
@RestController("Training")
@RequestMapping(URIs.Train.ROOT)
class TrainingController {

	/**
	 * Generates a training for the given AGU.
	 */
	@PostMapping
	fun generateTraining(
		@RequestBody trainingInputModel: TrainingInputModel
	): ResponseEntity<*> {
		return when (val result = invokeTrainingAlgorithm(
			trainingInputModel.temperatures.replace("\"", "\\\""),
			trainingInputModel.consumptions.replace("\"", "\\\"")
		)) {
			ERROR_IDENTITY -> ResponseEntity.badRequest().body(ERROR_MESSAGE)
			else -> ResponseEntity.ok(TrainingOutputModel(result))
		}
	}

	companion object {
		private const val ERROR_IDENTITY = "ERROR"
		private const val ERROR_MESSAGE = "Error while training the model"
	}
}
