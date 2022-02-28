/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package modules;

import java.io.File;
import java.io.FileReader;
import java.io.FileNotFoundException;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JSONReader {
    public JSONObject json_file;
    public JSONObject read(String path) {
            File f = new File(path);
            try {
                    JSONParser parser = new JSONParser();
                    Object obj  = parser.parse(new FileReader(f.getAbsolutePath()));
                    json_file =  (JSONObject) obj;


            } catch (FileNotFoundException e) {
                    e.printStackTrace();

            } catch (Exception e) {
                    e.printStackTrace();
            }	

            return json_file;
    }
}


