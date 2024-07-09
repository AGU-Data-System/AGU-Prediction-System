package aguPredictionSystem.server.http

/**
 * Contains the URIs for the API
 */
object URIs {
	const val PREFIX = "/api"

	/**
	 * Contains the URIs for the train endpoints
	 */
	object Train {
		const val ROOT = "$PREFIX/train"
	}

	/**
	 * Contains the URIs for the prediction endpoints
	 */
	object Prediction {
		const val ROOT = "$PREFIX/predict"
	}
}
