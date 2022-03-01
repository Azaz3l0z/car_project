/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package modules;

import java.io.*;
import java.lang.Process;
import java.lang.Runtime;
import java.io.File;

/**
 *
 * @author azazel
 */
public class ScrapPython extends Thread {
	public String webpage;
	public String trademark;
	public String model;
	public String yearstart;
	public String yearend;
	public String change;
	public String km;
        
	public ScrapPython(String webpage, String trademark, String model, 
			String yearstart, String yearend, String change, String km){
		this.webpage = webpage;
		this.trademark = trademark;
		this.model = model;
		this.yearstart = yearstart;
		this.yearend = yearend;
		this.change = change;
		this.km = km.replace(" ", "");
	}

	public void run() {
		try {
			String env_path = String.join(File.separator, 
                                System.getProperty("user.dir"), "src", "main", 
                                "java", "scripts");
                        
                        String[] args = new String[]{webpage, trademark, 
                                model, yearstart, yearend, change, km};
                        
                        for (int k = 0; k < args.length; k++){
                            args[k] = args[k].replace(" ", "_");
                        }
                        
			String command = 
                                String.join(File.separator, env_path, "env",
                                        "bin", "python3") 
                                + " "
                                + String.join(File.separator, env_path, "run.py")
                                + " " + String.join(" ", args)
                                ;
			Process process = Runtime.getRuntime().exec(command);
                        System.out.println(command);

		} catch (Exception e) {
		}

	}
}


