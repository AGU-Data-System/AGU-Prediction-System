package aguPredictionSystem.server.http

object URIs {
	const val PREFIX = "/api"

	object Train {
		private const val ROOT = "$PREFIX/train"
		const val BY_ID = "$ROOT/{aguCui}"
	}

	object Predict {
		const val ROOT = "$PREFIX/predict"
		const val BY_ID = "$ROOT/{aguCui}"
	}
}