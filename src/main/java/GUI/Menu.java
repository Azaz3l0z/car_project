/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JFrame.java to edit this template
 */
package GUI;

import java.util.List;
import java.util.Arrays;
import java.util.Iterator;
import java.util.ListIterator;  

import java.io.File;
import modules.JSONReader;
import modules.ScrapPython;

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
    public Menu() {
        initComponents();
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
        download = new javax.swing.JButton();
        table_panel = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTable1 = new javax.swing.JTable();

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

        download.setText("Download");
        download.setFocusable(false);
        download.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        download.setVerticalTextPosition(javax.swing.SwingConstants.BOTTOM);
        download.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                downloadActionPerformed(evt);
            }
        });
        toolbar_panel.add(download);

        getContentPane().add(toolbar_panel);

        table_panel.setBackground(new java.awt.Color(255, 0, 0));
        table_panel.setMinimumSize(new java.awt.Dimension(100, 100));
        table_panel.setPreferredSize(new java.awt.Dimension(100, 100));
        table_panel.setLayout(new java.awt.BorderLayout());

        jTable1.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "Title 1", "Title 2", "Title 3", "Title 4"
            }
        ));
        jScrollPane1.setViewportView(jTable1);

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
        Long valStart = Long.parseLong(currentStart);
        Long valEnd = Long.parseLong(currentEnd);

        if (valEnd < valStart){
            int index = 0;
            for (int k = 0; k < jsonKey_Time.size(); k++){
                if (jsonKey_Time.get(k).equals(valStart)){
                    index = k;
                    break;
                }            
            }

            String[] yearendMenu = new String[jsonKey_Time.size() - index];

            for (int k = index; k < jsonKey_Time.size(); k++){
                String year = String.valueOf(jsonKey_Time.get(k));
                yearendMenu[k - index] = year;
            }

            yearend.setModel(new javax.swing.DefaultComboBoxModel<>(yearendMenu));  
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
    	
    	ScrapPython scraper = 
    			new ScrapPython(currentWebpage, currentTrademark, 
    					currentModel, currentYearStart, currentYearEnd,
    					currentChange, currentKm);
        
    }//GEN-LAST:event_downloadActionPerformed
    private JSONObject json_file;
    private JSONObject jsonKey_Models;
    private JSONArray jsonKey_Time;
    private String kmText;
    
    private void setAll(){
        JSONReader reader = new JSONReader();
        String current_val = String.valueOf(webpage.getSelectedItem());
        File f = new File("src/main/java/files/"+current_val+".json");
        
        json_file = reader.read(f.getAbsolutePath());
        kmText = km.getText();
        setTrademarkMenu();
        setTimeMenu();
    }
    
    private void setTrademarkMenu(){
        jsonKey_Models = (JSONObject)json_file.get("models");
        String[] trademarkMenu = new String[jsonKey_Models.size()];
        Iterator itr = jsonKey_Models.keySet().iterator();
        int k = 0;
        while (itr.hasNext()){
            String key = (String)itr.next();
            trademarkMenu[k] = key;
            k++;
        }
        
        Arrays.sort(trademarkMenu);
        trademark.setModel(new javax.swing.DefaultComboBoxModel<>(trademarkMenu));
        
        setModelMenu(trademarkMenu[0]);
                
    }
    
    private void setModelMenu(String key){
        JSONObject modelsDict = (JSONObject)jsonKey_Models.get(key);
        modelsDict = (JSONObject)modelsDict.get("models");
        
        Iterator itr = modelsDict.keySet().iterator();
        String[] modelMenu = new String[modelsDict.size()];
        int k = 0;
        while (itr.hasNext()){
            key = (String)itr.next();
            modelMenu[k] = key;
            k++;
        }
        Arrays.sort(modelMenu);
        model.setModel(new javax.swing.DefaultComboBoxModel<>(modelMenu));

    }
    
    private void setTimeMenu(){
        jsonKey_Time = (JSONArray)json_file.get("time");
        String[] timeMenu = new String[jsonKey_Time.size()];
        for (int k = 0; k < jsonKey_Time.size(); k++){
            timeMenu[k] = String.valueOf(jsonKey_Time.get(k));
        }
        
        yearstart.setModel(new javax.swing.DefaultComboBoxModel<>(timeMenu));
        yearend.setModel(new javax.swing.DefaultComboBoxModel<>(timeMenu));
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
    private javax.swing.JButton download;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JTable jTable1;
    private javax.swing.JTextField km;
    private javax.swing.JComboBox<String> model;
    private javax.swing.JPanel table_panel;
    private javax.swing.JPanel toolbar_panel;
    private javax.swing.JComboBox<String> trademark;
    private javax.swing.JComboBox<String> webpage;
    private javax.swing.JComboBox<String> yearend;
    private javax.swing.JComboBox<String> yearstart;
    // End of variables declaration//GEN-END:variables
}
