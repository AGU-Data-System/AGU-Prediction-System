package aguPredictionSystem.server.http.models

/**
 * Represents the input model for the training endpoint.
 *
 * @param temperatures The temperatures.
 * @param consumptions The consumptions.
 */
class TrainingInputModel(
	val temperatures: String,
	val consumptions: String
)