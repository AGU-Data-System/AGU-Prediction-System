package aguPredictionSystem.server.utils

import aguPredictionSystem.server.Environment
import java.io.BufferedReader
import java.io.InputStreamReader
import org.slf4j.LoggerFactory

object InvokeScripts {

	private const val PYTHON_COMMAND = "python"
	private val BASE_SCRIPTS_PATH = Environment.getPythonScriptPath()
	private val logger = LoggerFactory.getLogger(InvokeScripts::class.java)

	/**
	 * Invokes the training algorithm.
	 *
	 * @param temperatures The temperatures.
	 * @param consumptions The consumptions.
	 * @return The result of the training algorithm.
	 */
	fun invokeTrainingAlgorithm(temperatures: String, consumptions: String): String {
		return invokeAlgorithm("$BASE_SCRIPTS_PATH/TrainingModule.py", temperatures, consumptions)
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
		val coefficientsString = coefficients.joinToString(",")
		return invokeAlgorithm(
			"$BASE_SCRIPTS_PATH/PredictionModule.py",
			temperatures,
			consumptions,
			coefficientsString,
			intercept.toString()
		)
	}

	/**
	 * Invokes the algorithm.
	 *
	 * @param path The path to the script.
	 * @param args The arguments.
	 * @return The result of the algorithm.
	 */
	private fun invokeAlgorithm(path: String, vararg args: String): String {
		val processBuilder = ProcessBuilder(PYTHON_COMMAND, path, *args)

		processBuilder.redirectErrorStream(true)
		val process = processBuilder.start()

		val reader = BufferedReader(InputStreamReader(process.inputStream))
		var line: String?
		var lastLine: String? = null
		while (reader.readLine().also { line = it } != null) {
			lastLine = line
		}

		val exitCode = process.waitFor()
		return if (exitCode == 0) {
			logger.info("Python training script executed successfully.")
			val result = lastLine ?: "ERROR"
			if (result.split(",", " ", "{", ":").contains("\"date\"") || result.split(",", " ")
					.contains("\"coefficients\":")
			)
				result
			else
				"ERROR"
		} else {
			logger.error("Python training script encountered an error. Exit code: {}", exitCode)
			"ERROR"
		}
	}
}
