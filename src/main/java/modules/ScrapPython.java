/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package modules;

import java.io.File;
import java.lang.Process;
import java.lang.Runtime;
import javax.swing.table.DefaultTableModel;

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
    public String download_dir;
    
    public DefaultTableModel tableModel;
    public int id;

    public ScrapPython(String webpage, String trademark, String model, 
                    String yearstart, String yearend, String change, 
                    String km, DefaultTableModel tableModel, int id,
                    String download_dir){
        this.webpage = webpage;
        this.trademark = trademark;
        this.model = model;
        this.yearstart = yearstart;
        this.yearend = yearend;
        this.change = change;
        this.km = km.replace(" ", "");
        this.setDaemon(true);
        this.tableModel = tableModel;
        this.id = id;
        this.download_dir = download_dir;
    }

    public String get_command(){
    	String OS = CheckOS.get_OS();
    	String ext = "";
    	if (OS == "windows") {
    		ext = ".exe";
    	} else if (OS == "linux") {
    		ext = ".sh";
    	}
    		
        String env_path = String.join(File.separator, 
            System.getProperty("user.dir"), "resources", "python");

        String[] args = new String[]{download_dir, webpage, trademark, 
            model, yearstart, yearend, change, km};

        for (int k = 0; k < args.length; k++){
            args[k] = args[k].replace(" ", "_");
        }

        String command = 
            String.join(File.separator, env_path, "run"+ext)
            + " " + String.join(" ", args)
            ;
        return command;
    }
    
    public void run() {
        try {
            String command = get_command();
            System.out.println(command);
            Process process = Runtime.getRuntime().exec(command);
            while (process.isAlive()){

            }
            
            tableModel.setValueAt("Si", id, 7);
            

        } catch (Exception e) {
        }
    }
}


