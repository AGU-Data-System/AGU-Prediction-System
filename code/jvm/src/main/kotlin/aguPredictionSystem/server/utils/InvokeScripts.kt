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
		val pythonScript = "$BASE_SCRIPTS_PATH/TrainingModule.py"

		val processBuilder = ProcessBuilder(PYTHON_COMMAND, pythonScript, temperatures, consumptions)

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
			logger.info("Python training script executed successfully.")
		} else {
			logger.error("Python training script encountered an error. Exit code: {}", exitCode)
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
			PYTHON_COMMAND,
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
			logger.info("Python prediction script executed successfully.")
		} else {
			logger.error("Python prediction script encountered an error. Exit code: {}", exitCode)
		}

		return lastLine ?: "{}"
	}
}
