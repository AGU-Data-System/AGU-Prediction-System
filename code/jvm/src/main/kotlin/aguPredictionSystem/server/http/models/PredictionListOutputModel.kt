package aguPredictionSystem.server.http.models

/**
 * Represents the output model for the list of predictions.
 *
 * @property predictionList The list of predictions.
 */
data class PredictionListOutputModel(
	val predictionList: List<PredictionOutputModel>
) {
	constructor(prediction: String) : this(
		predictionList = prediction.filterNot { it in "[]{" }.split("},").map {
			val date = it.split(",")[0].split(":")[1].trim('"')
			val consumption = it.split(",")[1].split(":")[1].trim('"', '}')
			PredictionOutputModel(date = date, consumption = consumption.toDouble())
		}
	)
}