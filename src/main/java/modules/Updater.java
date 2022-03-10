package modules;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class Updater {
	public void update(){
		String OS = CheckOS.get_OS();
		String ext = "";
		if (OS == "windows") {
			ext = ".exe";
		} else if (OS == "linux") {
			ext = ".sh";
		}
		System.out.println(System.getProperty("user.dir"));
		String command = String.join(File.separator, 
				System.getProperty("user.dir"), "resources", 
				"updater", "updater"+ext);

		ProcessBuilder processBuilder = new ProcessBuilder();

		processBuilder.command(command);


		try {

			Process process = processBuilder.start();

			StringBuilder output = new StringBuilder();

			BufferedReader reader = new BufferedReader(
					new InputStreamReader(process.getInputStream()));

			String line;
			while ((line = reader.readLine()) != null) {
				output.append(line + "\n");
			}

			int exitVal = process.waitFor();
			if (exitVal == 0) {
				System.out.println("Success!");
				System.out.println(output);
			} else {
				//abnormal...
			}

		} catch (Exception e) {
			e.getStackTrace();
		}

	}
}
