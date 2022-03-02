/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package modules;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.io.File;

/**
 *
 * @author azazel
 */
public class QueueObserver extends Thread{
    ArrayBlockingQueue<Thread> queue;
    public QueueObserver(ArrayBlockingQueue<Thread> queue){
            this.queue = queue;
            this.setDaemon(true);
    }
    public void run(){
        while (true) {
            System.out.println("OBSERVER");
            System.out.println(queue);
            if (!queue.isEmpty()) {
                Thread thread = queue.peek();
                thread.start();                
                while (thread.isAlive()){

                }
            
                try {
                    queue.take();
                } catch (InterruptedException e){
                    e.printStackTrace();
                }
            } else {
                try {
                    TimeUnit.SECONDS.sleep(5);
                } catch (InterruptedException e){
                    e.printStackTrace();
                }
            }
        }
    }
}
