package modules;

import java.io.File;

public class Updater {
	public static void update(){
    	String OS = CheckOS.get_OS();
    	String ext = "";
    	if (OS == "windows") {
    		ext = ".exe";
    	} else if (OS == "linux") {
    		ext = "";
    	}
    		
        String command = String.join(File.separator, 
            System.getProperty("user.dir"), "resources", 
            	"updater", "updater"+ext);
        
        try {
        	Process process = Runtime.getRuntime().exec(command);
        } catch (Exception e) {
        	System.out.println("No updater");
        }
    }
}
