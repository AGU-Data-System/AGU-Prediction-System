package aguPredictionSystem.server.http.models

/**
 * Represents the input model for the prediction endpoint.
 *
 * @param temperatures The temperatures.
 * @param previousConsumptions The previous consumptions.
 * @param coefficients The coefficients.
 * @param intercept The intercept.
 */
data class PredictionInputModel(
	val temperatures: String,
	val previousConsumptions: String,
	val coefficients: List<Double>,
	val intercept: Double
)