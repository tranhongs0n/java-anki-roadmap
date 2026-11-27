# Chapter 14: Chapter 14: A Very Graphic Story

pages 499-546

are going to use, you need a graphical interface. If you’re building programs for yourself, you want a graphical interface. Even if you believe that the rest of your natural life will be spent writing server-side code, where the client user interface is a web page, sooner or later you’ll need to write tools, and you’ll want a graphical interface. Sure, command-line apps are retro, but not in a good way. They’re weak, inflexible, and unfriendly. We’ll spend two chapters

Handling and Inner Classes and lambdas. In this chapter, we’ll put a button on the screen, and make it do something when you click it. We’ll paint on the screen, we’ll display a JPEG image, and we’ll even do some (crude) animation. I heard your ex could only cook command-line meals. You don’t add things to the frame directly. Think of the frame as the trim around the window, and you add things to the window pane.

## It all starts with a window

```java
JFrame frame = new JFrame();
```

```java
JButton button = new JButton("click me");
frame.getContentPane().add(button);
```

```java
frame.setSize(300,300);
frame.setVisible(true);
```

```java
import javax.swing.*;
public class SimpleGui1 {
public static void main(String[] args) {
JFrame frame = new JFrame();
JButton button = new JButton("click me");
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.getContentPane().add(button);
frame.setSize(300, 300);
frame.setVisible(true);
}
}
```

## Your first GUI: a button on a frame

## But nothing happens when I click it...

## Getting a user event

```java
public void changeIt() {
button.setText("I’ve been clicked!");
}
```

```java
import javax.swing.*;
import java.awt.event.*;
public class SimpleGui2 implements ActionListener {
private JButton button;
public static void main(String[] args) {
SimpleGui2 gui = new SimpleGui2();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
button = new JButton("click me");
button.addActionListener(this);
frame.getContentPane().add(button);
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.setSize(300, 300);
frame.setVisible(true);
}
public void actionPerformed(ActionEvent event) {
button.setText("I've been clicked!");
}
}
```

## Getting a button’s ActionEvent

## Listeners, Sources, and Events

```java
addKeyListener(KeyListener k)
```

## Getting back to graphics...

```java
frame.getContentPane().add(myButton);
```

```java
graphics.drawImage(myPic,10,10,this);
```

```java
graphics.fillOval(70,70,100,100);
```

## Make your own drawing widget

```java
import javax.swing.*;
import java.awt.*;
class MyDrawPanel extends JPanel {
public void paintComponent(Graphics g) {
g.setColor(Color.orange);
g.fillRect(20, 50, 100, 100);
}
}
```

## Fun things to do in paintComponent()

```java
public void paintComponent(Graphics g) {
Image image = new ImageIcon("catzilla.jpg").getImage();
g.drawImage(image, 3, 4, this);
}
public void paintComponent(Graphics g) {
g.fillRect(0, 0, this.getWidth(), this.getHeight());
Random random = new Random();
int red = random.nextInt(256);
int green = random.nextInt(256);
int blue = random.nextInt(256);
Color randomColor = new Color(red, green, blue);
g.setColor(randomColor);
g.fillOval(70, 70, 100, 100);
}
```

```java
Animal a = new Dog();
```

```java
a.bark();
```

```java
Dog d = (Dog) a;
d.bark();
```

```java
Graphics2D g2d = (Graphics2D) g;
```

```java
Graphics2D g2d = (Graphics2D) g;
```

```java
public void paintComponent(Graphics g) {
Graphics2D g2d = (Graphics2D) g;
GradientPaint gradient = new GradientPaint(70, 70, Color.blue, 150, 150, Color.orange);
g2d.setPaint(gradient);
g2d.fillOval(70, 70, 100, 100);
}
```

```java
public void paintComponent(Graphics g) {
Graphics2D g2d = (Graphics2D) g;
Random random = new Random();
int red = random.nextInt(256);
int green = random.nextInt(256);
int blue = random.nextInt(256);
Color startColor = new Color(red, green, blue);
red = random.nextInt(256);
green = random.nextInt(256);
blue = random.nextInt(256);
Color endColor = new Color(red, green, blue);
GradientPaint gradient = new GradientPaint(70, 70, startColor, 150, 150, endColor);
g2d.setPaint(gradient);
g2d.fillOval(70, 70, 100, 100);
}
```

```java
frame.getContentPane().add(button);
```

```java
frame.getContentPane().add(BorderLayout.CENTER, button);
```

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
public class SimpleGui3 implements ActionListener {
private JFrame frame;
public static void main(String[] args) {
SimpleGui3 gui = new SimpleGui3();
gui.go();
}
public void go() {
frame = new JFrame();
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
JButton button = new JButton("Change colors");
button.addActionListener(this);
MyDrawPanel drawPanel = new MyDrawPanel();
frame.getContentPane().add(BorderLayout.SOUTH, button);
frame.getContentPane().add(BorderLayout.CENTER, drawPanel);
frame.setSize(300, 300);
frame.setVisible(true);
}
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
}
class MyDrawPanel extends JPanel {
public void paintComponent(Graphics g) {
// Code to fill the oval with a random color
// See page 365 for the code
}
}
```

## Let’s try it with TWO buttons

```java
class MyGui implements ActionListener {
// lots of code here and then:
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
public void actionPerformed(ActionEvent event) {
label.setText("That hurt!");
}
}
```

Flaw: You can’t! You can’t implement the same method twice in a Java class. It won’t compile. And even if you could, how would the event source know which of the two methods to call? 2Option Two Register the same listener with both buttons. Flaw: this does work, but in most cases it’s not very OO. One event handler doing many different things means that you have a single method doing many different things. If you need to change how one source is handled, you have to mess with everybody’s event handler. Sometimes it is a good solution, but usually it hurts maintainability and extensibility.

```java
class MyGui implements ActionListener {
// declare a bunch of instance variables here
public void go() {
// build gui
colorButton = new JButton();
labelButton = new JButton();
colorButton.addActionListener(this);
labelButton.addActionListener(this);
// more gui code here ...
}
public void actionPerformed(ActionEvent event) {
if (event.getSource() == colorButton) {
frame.repaint();
} else {
label.setText("That hurt!");
}
}
}
```

the listener classes a reference to the main GUI class, so that inside the actionPerformed() methods the listener could use the GUI class reference to access the variables of the GUI class. But that’s breaking encapsulation, so we’d probably need to make getter methods for the GUI widgets (getFrame(), getLabel(), etc.). And you’d probably need to add a constructor to the listener class so that you can pass the GUI reference to the listener at the time the listener is instantiated. And, well, it gets messier and more complicated.

```java
class MyGui {
private JFrame frame;
private JLabel label;
void gui() {
// code to instantiate the two listeners and register one
// with the color button and the other with the label button
}
}
class ColorButtonListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
}
class LabelButtonListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
label.setText("That hurt!");
}
}
```

## Inner class to the rescue!

```java
class MyOuterClass {
class MyInnerClass {
void go() {
}
}
}
```

```java
class MyOuterClass {
private int x;
class MyInnerClass {
void go() {
x = 42;
}
} // close inner class
} // close outer class
```

```java
class MyOuter {
private int x;
MyInner inner = new MyInner();
public void doStuff() {
inner.go();
}
class MyInner {
void go() {
x = 42;
}
} // close inner class
} // close outer class
```

* There’s an exception to this, for a very special case—an inner class defined within a static method. But we’re not going there, and you might go your entire Java life without ever encountering one of these. The outer class has a private instance variable “x.” Make an instance of the inner class. The method in the inner class uses the outer class instance variable “x,” as if “x” belonged to the inner class.

## How to make an instance of an inner class

```java
class Foo {
public static void main (String[] args) {
MyOuter outerObj = new MyOuter();
MyOuter.MyInner innerObj = outerObj.new MyInner();
}
}
```

```java
public class TwoButtons {
private JFrame frame;
private JLabel label;
public static void main(String[] args) {
TwoButtons gui = new TwoButtons();
gui.go();
}
public void go() {
frame = new JFrame();
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
JButton labelButton = new JButton("Change Label");
labelButton.addActionListener(new LabelListener());
JButton colorButton = new JButton("Change Circle");
colorButton.addActionListener(new ColorListener());
label = new JLabel("I’m a label");
MyDrawPanel drawPanel = new MyDrawPanel();
frame.getContentPane().add(BorderLayout.SOUTH, colorButton);
frame.getContentPane().add(BorderLayout.CENTER, drawPanel);
frame.getContentPane().add(BorderLayout.EAST, labelButton);
frame.getContentPane().add(BorderLayout.WEST, label);
frame.setSize(500, 400);
frame.setVisible(true);
}
class LabelListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
label.setText("Ouch!");
}
}
class ColorListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
}
}
```

have to use a special syntax. Chances are you’ll go through your entire Java life and never need to make an inner class from outside, but just in case you’re interested... inner class instances Sidebar Call a method on the inner class. getting gui Much better: the main GUI class doesn’t implement ActionListener now. Instead of passing (this) to the button’s listener registration method, pass a new instance of

```java
...
public void go() {
frame = new JFrame();
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
JButton labelButton = new JButton("Change Label");
labelButton.addActionListener(new LabelListener());
JButton colorButton = new JButton("Change Circle");
colorButton.addActionListener(new ColorListener());
label = new JLabel("I’m a label");
MyDrawPanel drawPanel = new MyDrawPanel();
// code to add widgets, here
frame.setSize(500, 400);
frame.setVisible(true);
}
class LabelListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
label.setText("Ouch!");
}
}
class ColorListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
}
```

Since ActionListener is a functional interface, you can replace the inner classes we saw on the previous page with lambda expressions.

## ActionListener is a Functional Interface

```java
...
public void go() {
frame = new JFrame();
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
JButton labelButton = new JButton("Change Label");
labelButton.addActionListener(event -> label.setText("Ouch!"));
JButton colorButton = new JButton("Change Circle");
colorButton.addActionListener(event -> frame.repaint());
label = new JLabel("I’m a label");
MyDrawPanel drawPanel = new MyDrawPanel();
// code to add widgets, here
frame.setSize(500, 400);
frame.setVisible(true);
}
class LabelListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
label.setText("Ouch!");
}
}
class ColorListener implements ActionListener {
public void actionPerformed(ActionEvent event) {
frame.repaint();
}
}
```

## Using an inner class for animation

```java
g.fillOval(20,50,100,100);
```

```java
g.fillOval(25,55,100,100);
```

```java
class MyDrawPanel extends JPanel {
public void paintComponent(Graphics g) {
g.setColor(Color.orange);
g.fillOval(x, y, 100, 100);
}
}
```

See if you can design a simple solution to get the ball to animate from the top left of the drawing panel down to the bottom right. Our answer is on the next page, so don’t turn this page until you’re done! Big Huge Hint: make the drawing panel an inner class. Another Hint: don’t put any kind of repeat loop in the paintComponent() method. Write your ideas (or the code) here: Remember! The system invokes the

```java
import javax.swing.*;
import java.awt.*;
import java.util.concurrent.TimeUnit;
public class SimpleAnimation {
private int xPos = 70;
private int yPos = 70;
public static void main(String[] args) {
SimpleAnimation gui = new SimpleAnimation();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
MyDrawPanel drawPanel = new MyDrawPanel();
frame.getContentPane().add(drawPanel);
frame.setSize(300, 300);
frame.setVisible(true);
for (int i = 0; i < 130; i++) {
xPos++;
yPos++;
drawPanel.repaint();
try {
TimeUnit.MILLISECONDS.sleep(50);
} catch (Exception e) {
e.printStackTrace();
}
}
}
class MyDrawPanel extends JPanel {
public void paintComponent(Graphics g) {
g.setColor(Color.green);
g.fillOval(xPos, yPos, 40, 40);
}
}
}
```

## The complete simple animation code

```java
public void paintComponent(Graphics g) {
g.setColor(Color.white);
g.fillRect(0, 0, this.getWidth(), this.getHeight());
g.setColor(Color.green);
g.fillOval(x, y, 40, 40);
}
```

## Code Kitchen

## Code Kitchen

## Listening for a non-GUI event

```java
ShortMessage msg1 = new ShortMessage();
msg1.setMessage(NOTE_ON, 1, 44, 100);
MidiEvent noteOn = new MidiEvent(msg1, 1);
track.add(noteOn);
ShortMessage msg2 = new ShortMessage();
msg2.setMessage(NOTE_OFF, 1, 44, 100);
MidiEvent noteOff = new MidiEvent(msg2, 16);
track.add(noteOff);
```

```java
ShortMessage msg = new ShortMessage();
```

```java
msg.setMessage(NOTE_ON, 1, instrument, 0);
```

```java
MidiEvent noteOn = new MidiEvent(msg, 1);
```

```java
track.add(noteOn);
public static MidiEvent makeEvent(int command, int channel, int one, int two, int tick) {
MidiEvent event = null;
try {
ShortMessage msg = new ShortMessage();
msg.setMessage(command, channel, one, two);
event = new MidiEvent(msg, tick);
} catch (Exception e) {
e.printStackTrace();
}
return event;
}
```

```java
import javax.sound.midi.*;
import static javax.sound.midi.ShortMessage.*;
public class MiniMusicPlayer1 {
public static void main(String[] args) {
try {
Sequencer sequencer = MidiSystem.getSequencer();
sequencer.open();
Sequence seq = new Sequence(Sequence.PPQ, 4);
Track track = seq.createTrack();
for (int i = 5; i < 61; i += 4) {
track.add(makeEvent(NOTE_ON, 1, i, 100, i));
track.add(makeEvent(NOTE_OFF, 1, i, 100, i + 2));
}
sequencer.setSequence(seq);
sequencer.setTempoInBPM(220);
sequencer.start();
} catch (Exception ex) {
ex.printStackTrace();
}
}
public static MidiEvent makeEvent(int cmd, int chnl, int one, int two, int tick) {
MidiEvent event = null;
try {
ShortMessage msg = new ShortMessage();
msg.setMessage(cmd, chnl, one, two);
event = new MidiEvent(msg, tick);
} catch (Exception e) {
e.printStackTrace();
}
return event;
}
}
```

```java
import javax.sound.midi.*;
import static javax.sound.midi.ShortMessage.*;
public class MiniMusicPlayer2 {
public static void main(String[] args) {
MiniMusicPlayer2 mini = new MiniMusicPlayer2();
mini.go();
}
public void go() {
try {
Sequencer sequencer = MidiSystem.getSequencer();
sequencer.open();
int[] eventsIWant = {127};
sequencer.addControllerEventListener(event -> System.out.println("la"), eventsIWant);
Sequence seq = new Sequence(Sequence.PPQ, 4);
Track track = seq.createTrack();
for (int i = 5; i < 60; i += 4) {
track.add(makeEvent(NOTE_ON, 1, i, 100, i));
track.add(makeEvent(CONTROL_CHANGE, 1, 127, 0, i));
track.add(makeEvent(NOTE_OFF, 1, i, 100, i + 2));
}
sequencer.setSequence(seq);
sequencer.setTempoInBPM(220);
sequencer.start();
} catch (Exception ex) {
ex.printStackTrace();
}
}
public static MidiEvent makeEvent(int cmd, int chnl, int one, int two, int tick) {
MidiEvent event = null;
try {
ShortMessage msg = new ShortMessage();
msg.setMessage(cmd, chnl, one, two);
event = new MidiEvent(msg, tick);
} catch (Exception e) {
e.printStackTrace();
}
return event;
}
}
```

## Version Two: registering and getting ControllerEvents

## Version Three: drawing graphics in time with the music

```java
class MyDrawPanel extends JPanel implements ControllerEventListener {
private boolean msg = false;
public void controlChange(ShortMessage event) {
msg = true;
repaint();
}
public void paintComponent(Graphics g) {
if (msg) {
int r = random.nextInt(250);
int gr = random.nextInt(250);
int b = random.nextInt(250);
g.setColor(new Color(r, gr, b));
int height = random.nextInt(120) + 10;
int width = random.nextInt(120) + 10;
int xPos = random.nextInt(40) + 10;
int yPos = random.nextInt(40) + 10;
g.fillRect(xPos, yPos, width, height);
msg = false;
}
}
}
```

```java
import javax.sound.midi.*;
import javax.swing.*;
import java.awt.*;
import java.util.Random;
import static javax.sound.midi.ShortMessage.*;
public class MiniMusicPlayer3 {
private MyDrawPanel panel;
private Random random = new Random();
public static void main(String[] args) {
MiniMusicPlayer3 mini = new MiniMusicPlayer3();
mini.go();
}
public void setUpGui() {
JFrame frame = new JFrame("My First Music Video");
panel = new MyDrawPanel();
frame.setContentPane(panel);
frame.setBounds(30, 30, 300, 300);
frame.setVisible(true);
}
public void go() {
setUpGui();
try {
Sequencer sequencer = MidiSystem.getSequencer();
sequencer.open();
sequencer.addControllerEventListener(panel, new int[]{127});
Sequence seq = new Sequence(Sequence.PPQ, 4);
Track track = seq.createTrack();
int note;
for (int i = 0; i < 60; i += 4) {
note = random.nextInt(50) + 1;
track.add(makeEvent(NOTE_ON, 1, note, 100, i));
track.add(makeEvent(CONTROL_CHANGE, 1, 127, 0, i));
track.add(makeEvent(NOTE_OFF, 1, note, 100, i + 2));
}
sequencer.setSequence(seq);
sequencer.start();
sequencer.setTempoInBPM(120);
} catch (Exception ex) {
ex.printStackTrace();
}
}
```

```java
public static MidiEvent makeEvent(int cmd, int chnl, int one, int two, int tick) {
MidiEvent event = null;
try {
ShortMessage msg = new ShortMessage();
msg.setMessage(cmd, chnl, one, two);
event = new MidiEvent(msg, tick);
} catch (Exception e) {
e.printStackTrace();
}
return event;
}
class MyDrawPanel extends JPanel implements ControllerEventListener {
private boolean msg = false;
public void controlChange(ShortMessage event) {
msg = true;
repaint();
}
public void paintComponent(Graphics g) {
if (msg) {
int r = random.nextInt(250);
int gr = random.nextInt(250);
int b = random.nextInt(250);
g.setColor(new Color(r, gr, b));
int height = random.nextInt(120) + 10;
int width = random.nextInt(120) + 10;
int xPos = random.nextInt(40) + 10;
int yPos = random.nextInt(40) + 10;
g.fillRect(xPos, yPos, width, height);
msg = false;
}
}
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
class InnerButton {
private JButton button;
public static void main(String[] args)
{
InnerButton gui = new InnerButton();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
frame.setDefaultCloseOperation(
JFrame.EXIT_ON_CLOSE);
button = new JButton("A");
button.addActionListener();
frame.getContentPane().add(
BorderLayout.SOUTH, button);
frame.setSize(200, 100);
frame.setVisible(true);
}
class ButtonListener extends ActionListener {
public void actionPerformed(ActionEvent e) {
if (button.getText().equals("A")) {
button.setText("B");
} else {
button.setText("A");
}
}
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.util.concurrent.TimeUnit;
public class Animate {
int x = 1;
int y = 1;
public static void main(String[] args) {
Animate gui = new Animate ();
gui.go();
}
public void go() {
JFrame _________ = new JFrame();
frame.setDefaultCloseOperation(
JFrame.EXIT_ON_CLOSE);
______________________________________;
_________.getContentPane().add(drawP);
__________________________;
_________.setVisible(true);
for (int i=0; i<124; _______________) {
_____________________;
_____________________;
try {
TimeUnit.MILLISECONDS.sleep(50);
} catch(Exception ex) { }
}
}
class MyDrawP extends JPanel {
public void paintComponent (Graphics
_________) {
__________________________________;
__________________________________;
__________________________________;
__________________________________;
}
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
class InnerButton {
private JButton button;
public static void main(String[] args) {
InnerButton gui = new InnerButton();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
frame.setDefaultCloseOperation(
JFrame.EXIT_ON_CLOSE);
```

```java
frame.getContentPane().add(
BorderLayout.SOUTH, button);
frame.setSize(200, 100);
frame.setVisible(true);
}
public void actionPerformed(ActionEvent e) {
if (button.getText().equals("A")) {
button.setText("B");
} else {
button.setText("A");
}
}
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.util.concurrent.TimeUnit;
public class Animate {
int x = 1;
int y = 1;
public static void main(String[] args) {
Animate gui = new Animate ();
gui.go();
}
public void go() {
```

```java
frame.setDefaultCloseOperation(
JFrame.EXIT_ON_CLOSE);
```

```java
try {
TimeUnit.MILLISECONDS.sleep(50);
} catch(Exception ex) { }
}
}
class MyDrawP extends JPanel {
```

```java
}
}
}
```