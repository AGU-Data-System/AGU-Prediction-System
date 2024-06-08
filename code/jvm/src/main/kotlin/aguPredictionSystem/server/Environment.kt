package aguPredictionSystem.server

/**
 * Environment variables.
 */
object Environment {

	private const val KEY_PYTHON_SCRIPT_PATH = "PYTHON_SCRIPT_PATH"

	/**
	 * Gets the Python script path from the environment variables.
	 */
	fun getPythonScriptPath(): String? =
		System.getenv(KEY_PYTHON_SCRIPT_PATH) //?: throw Exception("Missing env var $KEY_PYTHON_SCRIPT_PATH")

}