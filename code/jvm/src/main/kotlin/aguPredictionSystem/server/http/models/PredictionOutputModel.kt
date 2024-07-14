package aguPredictionSystem.server.http.models

/**
 * Represents the output model for a prediction.
 *
 * @property date The date of the prediction.
 * @property consumption The consumption of the prediction.
 */
data class PredictionOutputModel(
	val date: String,
	val consumption: Double
)