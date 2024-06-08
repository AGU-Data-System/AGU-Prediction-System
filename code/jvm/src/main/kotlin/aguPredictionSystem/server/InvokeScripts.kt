package aguPredictionSystem.server

import java.io.BufferedReader
import java.io.InputStreamReader

object InvokeScripts {

	private val BASE_SCRIPTS_PATH = Environment.getPythonScriptPath() ?: "/../code/python/scripts"

	/**
	 * Invokes the training algorithm.
	 *
	 * @param temperatures The temperatures.
	 * @param consumptions The consumptions.
	 * @return The result of the training algorithm.
	 */
	fun invokeTrainingAlgorithm(temperatures: String, consumptions: String): String {
		val pythonScript = "$BASE_SCRIPTS_PATH/TrainingModule.py"

		val processBuilder = ProcessBuilder("python", pythonScript, temperatures, consumptions)

		processBuilder.redirectErrorStream(true)
		val process = processBuilder.start()

		val reader = BufferedReader(InputStreamReader(process.inputStream))
		var line: String?
		var lastLine: String? = null
		while (reader.readLine().also { line = it } != null) {
			lastLine = line
		}

		val exitCode = process.waitFor()
		if (exitCode == 0) {
			println("Python script executed successfully.")
		} else {
			println("Python script encountered an error. Exit code: $exitCode")
		}

		return lastLine ?: "{}"
	}

	/**
	 * Invokes the prediction algorithm.
	 *
	 * @param temperatures The temperatures.
	 * @param consumptions The consumptions.
	 * @param coefficients The coefficients.
	 * @param intercept The intercept.
	 * @return The result of the prediction algorithm.
	 */
	fun invokePredictionAlgorithm(
		temperatures: String,
		consumptions: String,
		coefficients: List<Double>,
		intercept: Double
	): String {
		val pythonScript = "$BASE_SCRIPTS_PATH/PredictionResults.py"

		val processBuilder = ProcessBuilder(
			"python",
			pythonScript,
			temperatures,
			consumptions,
			coefficients.toString(),
			intercept.toString()
		)

		processBuilder.redirectErrorStream(true)
		val process = processBuilder.start()

		val reader = BufferedReader(InputStreamReader(process.inputStream))
		var line: String?
		var lastLine: String? = null
		while (reader.readLine().also { line = it } != null) {
			println(line)
			lastLine = line
		}

		val exitCode = process.waitFor()
		if (exitCode == 0) {
			println("Python script executed successfully.")
		} else {
			println("Python script encountered an error. Exit code: $exitCode")
		}

		return lastLine ?: "{}"
	}
}
