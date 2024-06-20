package aguPredictionSystem.server.http.models

/**
 * Represents the output model for the training endpoint.
 * TODO check if we can segregate the training model because its a json string
 * @param training The training.
 */
data class TrainingOutputModel(
	val training : String
)
