/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JFrame.java to edit this template
 */
package GUI;

import java.awt.Color;
import java.awt.Component;
import java.awt.Image;
import java.util.Arrays;
import java.util.Iterator;
import java.util.concurrent.ArrayBlockingQueue;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableCellRenderer;
import javax.swing.JComponent;
import javax.swing.border.*;
import javax.swing.ImageIcon;
import javax.swing.JFileChooser;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import modules.JSONReader;
import modules.ScrapPython;
import modules.QueueObserver;

import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

/**
 *
 * @author azazel
 */
public class Menu extends javax.swing.JFrame {

	/**
	 * Creates new form Menu
	 */
	int cap = 100;
	ArrayBlockingQueue<Thread> queue;
	QueueObserver observer;

	public Menu() {
		initComponents();
		setLocationRelativeTo(null);
		ImageIcon imageIcon = new ImageIcon("resources/icons/car.png"); // load the image to a imageIcon
		Image image = imageIcon.getImage(); // transform it 
		setIconImage(image);
		queue = new ArrayBlockingQueue<>(cap);
		observer = new QueueObserver(queue);
		observer.start();
		setDownloadDir();
		setAll();
	}

	/**
	 * This method is called from within the constructor to initialize the form.
	 * WARNING: Do NOT modify this code. The content of this method is always
	 * regenerated by the Form Editor.
	 */
	@SuppressWarnings("unchecked")
	// <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
	private void initComponents() {

		toolbar_panel = new javax.swing.JPanel();
		webpage = new javax.swing.JComboBox<>();
		trademark = new javax.swing.JComboBox<>();
		model = new javax.swing.JComboBox<>();
		yearstart = new javax.swing.JComboBox<>();
		yearend = new javax.swing.JComboBox<>();
		change = new javax.swing.JComboBox<>();
		km = new javax.swing.JTextField();
		jPanel1 = new javax.swing.JPanel();
		download = new javax.swing.JButton();
		config = new javax.swing.JButton();
		table_panel = new javax.swing.JPanel();
		jScrollPane1 = new javax.swing.JScrollPane();
		table = new javax.swing.JTable() {
			@Override
			public Component prepareRenderer(TableCellRenderer renderer, int row, int col) {
				Component comp = super.prepareRenderer(renderer, row, col);
				JComponent jc = (JComponent)comp;
				Object value = getModel().getValueAt(row, col);

				Border outside = new MatteBorder(1, 0, 1, 0, Color.BLACK);
				Border inside = new EmptyBorder(0, 1, 0, 1);
				Border highlight = new CompoundBorder(outside, inside);

				if (isRowSelected(row)) {
					jc.setForeground(Color.black);
					jc.setBackground(Color.white);
					jc.setBorder(highlight);
				} else {
					jc.setForeground(Color.black);
					jc.setBackground(Color.white);
				}

				if (value.equals("No")) {
					jc.setBackground(Color.red);
				} else if (value.equals("Si")) {
					jc.setBackground(Color.green);
				}

				return comp;
			}
		};

		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		setTitle("CarScraper");
		setBackground(new java.awt.Color(255, 255, 255));
		setMinimumSize(new java.awt.Dimension(1000, 400));
		getContentPane().setLayout(new javax.swing.BoxLayout(getContentPane(), javax.swing.BoxLayout.Y_AXIS));

		toolbar_panel.setForeground(new java.awt.Color(0, 255, 0));
		toolbar_panel.setMaximumSize(new java.awt.Dimension(2147483647, 40));
		toolbar_panel.setMinimumSize(new java.awt.Dimension(100, 40));
		toolbar_panel.setName(""); // NOI18N
		toolbar_panel.setPreferredSize(new java.awt.Dimension(100, 40));
		toolbar_panel.setLayout(new java.awt.GridLayout(1, 0));

		webpage.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "cochesnet", "milanuncios", "autoscout24" }));
		webpage.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				webpageActionPerformed(evt);
			}
		});
		toolbar_panel.add(webpage);

		trademark.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				trademarkActionPerformed(evt);
			}
		});
		toolbar_panel.add(trademark);

		toolbar_panel.add(model);

		yearstart.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				yearstartActionPerformed(evt);
			}
		});
		toolbar_panel.add(yearstart);

		toolbar_panel.add(yearend);

		change.setModel(new javax.swing.DefaultComboBoxModel<>(new String[] { "Manual", "Automatico" }));
		toolbar_panel.add(change);

		km.setText("Hasta x km");
		km.setToolTipText("");
		km.setOpaque(true);
		km.addFocusListener(new java.awt.event.FocusAdapter() {
			public void focusGained(java.awt.event.FocusEvent evt) {
				kmFocusGained(evt);
			}
			public void focusLost(java.awt.event.FocusEvent evt) {
				kmFocusLost(evt);
			}
		});
		toolbar_panel.add(km);

		jPanel1.setLayout(new java.awt.GridLayout());

		download.setText("");
		download.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				downloadActionPerformed(evt);
			}
		});
		try {        	
			ImageIcon imageIcon = new ImageIcon("resources/icons/download.png"); // load the image to a imageIcon
			Image image = imageIcon.getImage(); // transform it 
			Image newimg = image.getScaledInstance(40, 40,  java.awt.Image.SCALE_SMOOTH); // scale it the smooth way  
			imageIcon = new ImageIcon(newimg);  // transform it back

			download.setIcon(imageIcon);
		} catch (Exception ex) {
			System.out.println(ex.getStackTrace());
		}
		jPanel1.add(download);

		config.setText("");
		config.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				configActionPerformed(evt);
			}
		});
		try {
			ImageIcon imageIcon = new ImageIcon("resources/icons/config.png"); // load the image to a imageIcon
			Image image = imageIcon.getImage(); // transform it 
			Image newimg = image.getScaledInstance(40, 35,  java.awt.Image.SCALE_SMOOTH); // scale it the smooth way  
			imageIcon = new ImageIcon(newimg);  // transform it back

			config.setIcon(imageIcon);
		} catch (Exception ex) {
			System.out.println(ex.getStackTrace());
		}
		jPanel1.add(config);

		toolbar_panel.add(jPanel1);

		getContentPane().add(toolbar_panel);

		table_panel.setBackground(new java.awt.Color(255, 0, 0));
		table_panel.setMinimumSize(new java.awt.Dimension(100, 100));
		table_panel.setPreferredSize(new java.awt.Dimension(100, 100));
		table_panel.setLayout(new java.awt.BorderLayout());

		table.setModel(new javax.swing.table.DefaultTableModel(
				new Object [][] {

				},
				new String [] {
						"Página", "Marca", "Modelo", "Desde", "Hasta", "Cambio", "Km", "Descargado"
				}
				) {
			boolean[] canEdit = new boolean [] {
					false, false, false, false, false, false, false, false
			};

			public boolean isCellEditable(int rowIndex, int columnIndex) {
				return canEdit [columnIndex];
			}
		});
		jScrollPane1.setViewportView(table);

		table_panel.add(jScrollPane1, java.awt.BorderLayout.CENTER);

		getContentPane().add(table_panel);

		pack();
	}// </editor-fold>//GEN-END:initComponents

	private void webpageActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_webpageActionPerformed
		setAll();
	}//GEN-LAST:event_webpageActionPerformed

	private void trademarkActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_trademarkActionPerformed
		String key = String.valueOf(trademark.getSelectedItem());
		setModelMenu(key);
	}//GEN-LAST:event_trademarkActionPerformed

	private void yearstartActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_yearstartActionPerformed
		String currentStart = (String)yearstart.getSelectedItem();
		String currentEnd = (String)yearend.getSelectedItem();

		if (currentEnd.equals("Hasta")){
			currentEnd = "0";
		}
		Long valStart = Long.parseLong(currentStart);
		Long valEnd = Long.parseLong(currentEnd);
		int index = 0;
		for (int k = 0; k < jsonKey_Time.size(); k++){
			if (jsonKey_Time.get(k).equals(valStart)){
				index = k;
				break;
			}            
		}

		String[] yearendMenu = new String[jsonKey_Time.size() - index + 1];
		yearendMenu[0] = "Hasta";
		for (int k = index; k < jsonKey_Time.size(); k++){
			String year = String.valueOf(jsonKey_Time.get(k));
			yearendMenu[k - index + 1] = year;
		}

		yearend.setModel(new javax.swing.DefaultComboBoxModel<>(yearendMenu));  
		if (valStart <= valEnd){
			yearend.setSelectedItem(currentEnd);
		}

	}//GEN-LAST:event_yearstartActionPerformed

	private void kmFocusGained(java.awt.event.FocusEvent evt) {//GEN-FIRST:event_kmFocusGained
		if (km.getText().equals(kmText)){
			km.setText("");
		}
	}//GEN-LAST:event_kmFocusGained

	private void kmFocusLost(java.awt.event.FocusEvent evt) {//GEN-FIRST:event_kmFocusLost
		if (km.getText().equals("")){
			km.setText(kmText);
		}
	}//GEN-LAST:event_kmFocusLost

	private void downloadActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_downloadActionPerformed
		String currentWebpage = String.valueOf(webpage.getSelectedItem());
		String currentTrademark = String.valueOf(trademark.getSelectedItem());
		String currentModel = String.valueOf(model.getSelectedItem());
		String currentYearStart = String.valueOf(yearstart.getSelectedItem());
		String currentYearEnd = String.valueOf(yearend.getSelectedItem());
		String currentChange = String.valueOf(change.getSelectedItem());
		String currentKm = String.valueOf(km.getText());

		String dispTrademark = String.valueOf(trademark.getSelectedItem());
		String dispModel = String.valueOf(model.getSelectedItem());
		String dispYearStart = String.valueOf(yearstart.getSelectedItem());
		String dispYearEnd = String.valueOf(yearend.getSelectedItem());
		String dispChange = String.valueOf(change.getSelectedItem());


		if (currentTrademark == "Marca"){
			dispTrademark = "";
		}

		if (currentModel == "Modelo"){
			dispModel = "";
		} 

		if (currentYearStart == "Desde"){
			dispYearStart = "";
		}

		if (currentYearEnd == "Hasta"){
			dispYearEnd = "";
		}

		if (currentChange == "Cambio"){
			dispChange = "";
		}

		DefaultTableModel tableModel = (DefaultTableModel) table.getModel();
		String[] newRow = {currentWebpage, dispTrademark,
				dispModel, dispYearStart, dispYearEnd, dispChange,
				currentKm, "No"};

		tableModel.addRow(newRow);
		int id = 0;
		boolean cond = false ;
		for (int k = 0; k < tableModel.getRowCount(); k++){
			for (String s : newRow){
				if(tableModel.getDataVector().get(k).contains(s)){
					cond = true;
				} else{
					cond = false;
				}
			}
			if (cond){
				id = k;
			}
		}
		ScrapPython pyprocess = 
				new ScrapPython(currentWebpage, currentTrademark,
						currentModel, currentYearStart, currentYearEnd,
						currentChange, currentKm, tableModel, id, download_dir);

		queue.add(pyprocess);
	}//GEN-LAST:event_downloadActionPerformed

	private void configActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_configActionPerformed
		JFileChooser chooser = new JFileChooser(); 
		chooser.setCurrentDirectory(new File(download_dir));
		chooser.setDialogTitle("Carpeta de descargas");
		chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		//
		// disable the "All files" option.
		//
		chooser.setAcceptAllFileFilterUsed(false);
		//    
		if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
			download_dir = chooser.getSelectedFile().getAbsolutePath();

			// We rewrite the settings file
			File settings = new File(String.join(File.separator, "resources", "settings.json"));
			JSONReader reader = new JSONReader();	
			JSONObject settings_json = reader.read(settings.getAbsolutePath());
			settings_json.put("downloads_path", download_dir);
			try {
				FileWriter myWriter = new FileWriter(settings.getAbsoluteFile());
				myWriter.write(settings_json.toString());
				myWriter.close();
			} catch (IOException e) {
				System.out.println("Wrong path");
			}

		}	else {
			System.out.println("No Selection ");
		}
	}

	private JSONObject json_file;
	private JSONObject jsonKey_Models;
	private JSONArray jsonKey_Time;
	private String kmText;
	private String download_dir;

	private void setDownloadDir() {
		File settings = new File(String.join(File.separator, "resources", "settings.json"));

		if (settings.isFile()) {
			JSONReader reader = new JSONReader();	
			JSONObject settings_json = reader.read(settings.getAbsolutePath());
			download_dir = (String)settings_json.get("downloads_path");

		} else {
			download_dir = System.getProperty("user.home");
			if (new File(String.join(File.separator, download_dir, "Descargas")).isDirectory()) {
				download_dir = String.join(File.separator, download_dir, "Descargas");
			} else if (new File(String.join(File.separator, download_dir, "Downloads")).isDirectory()) {
				download_dir = String.join(File.separator, download_dir, "Downloads");
			}

			JSONObject settings_json = new JSONObject();
			settings_json.put("downloads_path", download_dir);
			try {
				FileWriter myWriter = new FileWriter(settings.getAbsoluteFile());
				myWriter.write(settings_json.toString());
				myWriter.close();
			} catch (Exception e) {
				System.out.println("Wrong path");
			}

		}

	}

	private void setAll(){
		JSONReader reader = new JSONReader();
		String current_val = String.valueOf(webpage.getSelectedItem());
		File f = new File(String.join(File.separator, "resources", "json", current_val+".json"));

		json_file = reader.read(f.getAbsolutePath());
		kmText = km.getText();
		setTrademarkMenu();
		setTimeMenu();
		setChangeMenu();
	}

	private void setTrademarkMenu(){
		jsonKey_Models = (JSONObject)json_file.get("models");
		String[] trademarkMenu = new String[jsonKey_Models.size() + 1];
		trademarkMenu[0] = "Marca";
		Iterator itr = jsonKey_Models.keySet().iterator();
		int k = 0;
		while (itr.hasNext()){
			String key = (String)itr.next();
			trademarkMenu[k + 1] = key;
			k++;
		}

		Arrays.sort(trademarkMenu, 1, trademarkMenu.length);
		trademark.setModel(new javax.swing.DefaultComboBoxModel<>(trademarkMenu));
		setModelMenu(trademarkMenu[0]);

	}

	private void setModelMenu(String key){
		if (!key.equals("Marca")){
			JSONObject modelsDict = (JSONObject)jsonKey_Models.get(key);
			modelsDict = (JSONObject)modelsDict.get("models");
			String[] modelMenu = new String[modelsDict.size() + 1];
			modelMenu[0] = "Modelo";
			Iterator itr = modelsDict.keySet().iterator();

			int k = 0;
			while (itr.hasNext()){
				key = (String)itr.next();
				modelMenu[k + 1] = key;
				k++;
			}
			Arrays.sort(modelMenu, 1, modelMenu.length);
			model.setModel(new javax.swing.DefaultComboBoxModel<>(modelMenu));
		} else{
			String[] modelMenu = new String[]{"Modelo"};
			model.setModel(new javax.swing.DefaultComboBoxModel<>(modelMenu));
		}
	}

	private void setTimeMenu(){
		jsonKey_Time = (JSONArray)json_file.get("time");
		String[] timeMenu = new String[jsonKey_Time.size() + 1];
		timeMenu[0] = "Desde";  
		for (int k = 0; k < jsonKey_Time.size(); k++){
			timeMenu[k + 1] = String.valueOf(jsonKey_Time.get(k));
		}

		yearstart.setModel(new javax.swing.DefaultComboBoxModel<>(timeMenu));
		timeMenu[0] = "Hasta";  
		yearend.setModel(new javax.swing.DefaultComboBoxModel<>(timeMenu));
	}

	private void setChangeMenu(){
		String[] changeMenu = new String[]{"Cambio", "Manual", "Automatico"};
		change.setModel(new javax.swing.DefaultComboBoxModel<>(changeMenu));
	}

	/**
	 * @param args the command line arguments
	 */
	public static void main(String args[]) {
		/* Set the Nimbus look and feel */
		//<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
		/* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
		 * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
		 */
		try {
			for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
				if ("Nimbus".equals(info.getName())) {
					javax.swing.UIManager.setLookAndFeel(info.getClassName());
					break;
				}
			}
		} catch (ClassNotFoundException ex) {
			java.util.logging.Logger.getLogger(Menu.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (InstantiationException ex) {
			java.util.logging.Logger.getLogger(Menu.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (IllegalAccessException ex) {
			java.util.logging.Logger.getLogger(Menu.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		} catch (javax.swing.UnsupportedLookAndFeelException ex) {
			java.util.logging.Logger.getLogger(Menu.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
		}
		//</editor-fold>

		/* Create and display the form */
		java.awt.EventQueue.invokeLater(new Runnable() {
			public void run() {
				new Menu().setVisible(true);
			}
		});
	}

	// Variables declaration - do not modify//GEN-BEGIN:variables
	private javax.swing.JComboBox<String> change;
	private javax.swing.JButton config;
	private javax.swing.JButton download;
	private javax.swing.JPanel jPanel1;
	private javax.swing.JScrollPane jScrollPane1;
	private javax.swing.JTextField km;
	private javax.swing.JComboBox<String> model;
	private javax.swing.JTable table;
	private javax.swing.JPanel table_panel;
	private javax.swing.JPanel toolbar_panel;
	private javax.swing.JComboBox<String> trademark;
	private javax.swing.JComboBox<String> webpage;
	private javax.swing.JComboBox<String> yearend;
	private javax.swing.JComboBox<String> yearstart;
	// End of variables declaration//GEN-END:variables
}
