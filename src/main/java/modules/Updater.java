package modules;

import java.io.File;

public class Updater {
	public static void update(){
    	String OS = CheckOS.get_OS();
    	String ext = "";
    	if (OS == "windows") {
    		ext = ".exe";
    	} else if (OS == "linux") {
    		ext = ".sh";
    	}
    		
        String command = String.join(File.separator, 
            System.getProperty("user.dir"), "resources", 
            	"updater", "updater"+ext);
        
        try {
        	System.out.println(command);
        	Process process = Runtime.getRuntime().exec(command);
        } catch (Exception e) {
        	System.out.println("No updater");
        }
    }
}
