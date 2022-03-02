/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package GUI;

import java.lang.*;
import javax.swing.*;


/**
 *
 * @author azazel
 */
class MyTableCellRenderer extends DefaultTableCellRenderer {

    @Override
    public Color getBackground() {
        return super.getBackground();
    }
    
     public void changeTable(JTable table, int column_index) {
        table.getColumnModel().getColumn(column_index).setCellRenderer(new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus, int row, int column) {
                final Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
                int st_val = Integer.parseInt(table.getValueAt(row, 2).toString());
                int req_val = 2000;
                if (st_val < req_val) {
                    c.setBackground(Color.MAGENTA);
                } else {
                    c.setBackground(Color.GREEN);
                }
                return c;
            }
        });
    }
}