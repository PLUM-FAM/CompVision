
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;

public class MyPanel extends JPanel
{
 
    int startX, flag, startY, endX, endY;

	int [] freq;
    BufferedImage grid;
    Graphics2D gc;

	public MyPanel()
	{
		startX = startY = 0;
        endX = endY = 100;
 	}
	
	//constructor for drawing histograms.
	public MyPanel(int[] freq)
	{
		startX = startY = 0;
		endX = endY = 100;
		
		this.freq = freq; //initialize global array "freq"		
	}

	
	
    public void clear()
    {
       grid = null;
       repaint();
    }
     
    public void paintComponent(Graphics g)
    {  
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D)g;
        if(grid == null)
        {
            int w = this.getWidth();
            int h = this.getHeight();
            grid = (BufferedImage)(this.createImage(w,h));
            gc = grid.createGraphics();
        }
        g2.drawImage(grid, null, 0, 0);
        this.drawing(freq);
         
         
         
         
    }
    
    public void drawing(int freq[])
    {    	
    	//draw the lines for histogram frequencies
        //255 lines based off of index and frequency value in freq[]
        
        //panel size 305wx600h
        
        //print a line for each frequency in freq
        for (int f = 0; f < 255; f++)
        {
            gc.drawLine(5+f, this.getHeight(), 5+f, this.getHeight()-freq[f]);
        }
        repaint();
    }
   
}
