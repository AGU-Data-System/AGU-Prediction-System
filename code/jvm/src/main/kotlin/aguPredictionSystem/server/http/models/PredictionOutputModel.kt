package aguPredictionSystem.server.http.models

/**
 * Represents the output model for the prediction endpoint.
 * TODO check if we can segregate the prediction model because its a json string
 * @param prediction The prediction.
 */
data class PredictionOutputModel(
	val prediction: String
)