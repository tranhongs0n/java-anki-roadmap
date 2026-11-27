# Chapter 15: Chapter 15: Work on Your Swing

pages 547-576

looks easy, but then you compile it, run it, look at it, and think, “hey, that’s not supposed to go there.” The thing that makes it easy to code is the thing that makes it hard to control—the Layout Manager. Layout Manager objects control the size and location of the widgets in a Java GUI. They do a ton of work on your behalf, but you won’t always like the results. You want two buttons to be the same size, but they aren’t. You want the text field to be three inches

long, but it’s nine. Or one. And under the label instead of next to it. But with a little work, you can get layout managers to submit to your will. Learning a little Swing will give you a head start for most GUI programming you’ll ever do. Wanna write an Android app? Working through this chapter will give you a head start. Work on Your Swing Why won’t the ball go where I want it to go (like, smack in Suzy Smith’s

## Swing components <!--p548-->

```java
JButton button = new JButton("click me");
frame.getContentPane().add(BorderLayout.EAST, button);
```

```java
frame.setSize(300,300);
frame.setVisible(true);
```

## Layout Managers <!--p549-->

```java
myPanel.add(button);
```

```java
JPanel panelA = new JPanel();
JPanel panelB = new JPanel();
panelB.add(new JButton("button 1"));
panelB.add(new JButton("button 2"));
panelB.add(new JButton("button 3"));
panelA.add(panelB);
```

## How does the layout manager decide? <!--p550-->

## Layout Managers <!--p549-->

```java
import javax.swing.*;
import java.awt.*;
public class Button1 {
public static void main(String[] args) {
Button1 gui = new Button1();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
JButton button = new JButton("click me");
frame.getContentPane().add(BorderLayout.EAST, button);
frame.setSize(200, 200);
frame.setVisible(true);
}
}
```

```java
public void go() {
JFrame frame = new JFrame();
JButton button = new JButton("click like you mean it");
frame.getContentPane().add(BorderLayout.EAST, button);
frame.setSize(200, 200);
frame.setVisible(true);
}
```

```java
public void go() {
JFrame frame = new JFrame();
JButton button = new JButton("There is no spoon...");
frame.getContentPane().add(BorderLayout.NORTH, button);
frame.setSize(200, 200);
frame.setVisible(true);
}
```

```java
public void go() {
JFrame frame = new JFrame();
JButton button = new JButton("Click This!");
Font bigFont = new Font("serif", Font.BOLD, 28);
button.setFont(bigFont);
frame.getContentPane().add(BorderLayout.NORTH, button);
frame.setSize(200, 200);
frame.setVisible(true);
}
```

```java
public void go() {
JFrame frame = new JFrame();
JButton east = new JButton("East");
JButton west = new JButton("West");
JButton north = new JButton("North");
JButton south = new JButton("South");
JButton center = new JButton("Center");
frame.getContentPane().add(BorderLayout.EAST, east);
frame.getContentPane().add(BorderLayout.WEST, west);
frame.getContentPane().add(BorderLayout.NORTH, north);
frame.getContentPane().add(BorderLayout.SOUTH, south);
frame.getContentPane().add(BorderLayout.CENTER, center);
frame.setSize(300, 300);
frame.setVisible(true);
}
```

```java
import javax.swing.*;
import java.awt.*;
public class Panel1 {
public static void main(String[] args) {
Panel1 gui = new Panel1();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
frame.getContentPane().add(BorderLayout.EAST, panel);
frame.setSize(200, 200);
frame.setVisible(true);
}
}
```

```java
public void go() {
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("shock me");
panel.add(button);
frame.getContentPane().add(BorderLayout.EAST, panel);
frame.setSize(200, 200);
frame.setVisible(true);
}
```

```java
public void go() {
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("shock me");
JButton buttonTwo = new JButton("bliss");
panel.add(button);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.EAST, panel);
frame.setSize(250, 200);
frame.setVisible(true);
}
```

```java
JButton button = new JButton("shock me");
JButton buttonTwo = new JButton("bliss");
JButton buttonThree = new JButton("huh?");
panel.add(button);
panel.add(buttonTwo);
panel.add(buttonThree);
```

## BoxLayout to the rescue! <!--p559-->

```java
public void go() {
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
JButton button = new JButton("shock me");
JButton buttonTwo = new JButton("bliss");
panel.add(button);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.EAST, panel);
frame.setSize(250,200);
frame.setVisible(true);
}
```

## Layout Managers <!--p549-->

## Playing with Swing components <!--p561-->

```java
JTextField field = new JTextField(20);
```

```java
System.out.println(field.getText());
```

```java
field.setText("whatever");
field.setText("");
```

```java
field.addActionListener(myActionListener);
```

you the whole darn API for each of these, just a few highlights to get you started. If you do want to find out more, read Java Swing by Dave Wood, Marc Loy, and Robert Eckstein. JTextField Constructors How to use it Get text out of it Put text in it Get an ActionEvent when the user presses return or enter You can also register for key events if you really want to hear about it every time the user presses a key.

```java
JTextField field = new JTextField("Your name");
```

```java
field.selectAll();
```

```java
field.requestFocus();
```

```java
JTextArea text = new JTextArea(10, 20);
```

```java
JScrollPane scroller = new JScrollPane(text);
text.setLineWrap(true);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
panel.add(scroller);
```

```java
text.setText("Not all who are lost are wandering");
```

```java
text.selectAll();
```

```java
text.requestFocus();
```

```java
text.append("button clicked");
```

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
public class TextArea1 {
public static void main(String[] args) {
TextArea1 gui = new TextArea1();
gui.go();
}
public void go() {
JFrame frame = new JFrame();
JPanel panel = new JPanel();
JButton button = new JButton("Just Click It");
JTextArea text = new JTextArea(10, 20);
text.setLineWrap(true);
button.addActionListener(e -> text.append("button clicked \n"));
JScrollPane scroller = new JScrollPane(text);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
panel.add(scroller);
frame.getContentPane().add(BorderLayout.CENTER, panel);
frame.getContentPane().add(BorderLayout.SOUTH, button);
frame.setSize(350, 300);
frame.setVisible(true);
}
}
```

```java
JCheckBox check = new JCheckBox("Goes to 11");
```

```java
check.addItemListener(this);
```

```java
public void itemStateChanged(ItemEvent e) {
String onOrOff = "off";
if (check.isSelected()) {
onOrOff = "on";
}
System.out.println("Check box is " + onOrOff);
}
```

```java
check.setSelected(true);
check.setSelected(false);
```

```java
String[] listEntries = {"alpha", "beta", "gamma", "delta",
"epsilon", "zeta", "eta", "theta "};
JList<String> list = new JList<>(listEntries);
```

```java
JScrollPane scroller = new JScrollPane(list);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
panel.add(scroller);
```

```java
list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
```

```java
list.addListSelectionListener(this);
```

```java
public void valueChanged(ListSelectionEvent e) {
if (!e.getValueIsAdjusting()) {
String selection = list.getSelectedValue();
System.out.println(selection);
}
}
```

```java
list.setVisibleRowCount(4);
```

## Code Kitchen <!--p566-->

## Making the BeatBox <!--p567-->

```java
import javax.sound.midi.*;
import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import static javax.sound.midi.ShortMessage.*;
public class BeatBox {
private ArrayList<JCheckBox> checkboxList;
private Sequencer sequencer;
private Sequence sequence;
private Track track;
String[] instrumentNames = {"Bass Drum", "Closed Hi-Hat",
"Open Hi-Hat", "Acoustic Snare", "Crash Cymbal", "Hand Clap",
"High Tom", "Hi Bongo", "Maracas", "Whistle", "Low Conga",
"Cowbell", "Vibraslap", "Low-mid Tom", "High Agogo",
"Open Hi Conga"};
int[] instruments = {35, 42, 46, 38, 49, 39, 50, 60, 70, 72, 64, 56, 58, 47, 67, 63};
public static void main(String[] args) {
new BeatBox().buildGUI();
}
public void buildGUI() {
JFrame frame = new JFrame("Cyber BeatBox");
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
BorderLayout layout = new BorderLayout();
JPanel background = new JPanel(layout);
background.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
Box buttonBox = new Box(BoxLayout.Y_AXIS);
JButton start = new JButton("Start");
start.addActionListener(e -> buildTrackAndStart());
buttonBox.add(start);
JButton stop = new JButton("Stop");
stop.addActionListener(e -> sequencer.stop());
buttonBox.add(stop);
JButton upTempo = new JButton("Tempo Up");
upTempo.addActionListener(e -> changeTempo(1.03f));
buttonBox.add(upTempo);
JButton downTempo = new JButton("Tempo Down");
downTempo.addActionListener(e -> changeTempo(0.97f));
buttonBox.add(downTempo);
```

```java
Box nameBox = new Box(BoxLayout.Y_AXIS);
for (String instrumentName : instrumentNames) {
JLabel instrumentLabel = new JLabel(instrumentName);
instrumentLabel.setBorder(BorderFactory.createEmptyBorder(4, 1, 4, 1));
nameBox.add(instrumentLabel);
}
background.add(BorderLayout.EAST, buttonBox);
background.add(BorderLayout.WEST, nameBox);
frame.getContentPane().add(background);
GridLayout grid = new GridLayout(16, 16);
grid.setVgap(1);
grid.setHgap(2);
JPanel mainPanel = new JPanel(grid);
background.add(BorderLayout.CENTER, mainPanel);
checkboxList = new ArrayList<>();
for (int i = 0; i < 256; i++) {
JCheckBox c = new JCheckBox();
c.setSelected(false);
checkboxList.add(c);
mainPanel.add(c);
}
setUpMidi();
frame.setBounds(50, 50, 300, 300);
frame.pack();
frame.setVisible(true);
}
private void setUpMidi() {
try {
sequencer = MidiSystem.getSequencer();
sequencer.open();
sequence = new Sequence(Sequence.PPQ, 4);
track = sequence.createTrack();
sequencer.setTempoInBPM(120);
} catch (Exception e) {
e.printStackTrace();
}
}
```

```java
private void buildTrackAndStart() {
int[] trackList;
sequence.deleteTrack(track);
track = sequence.createTrack();
for (int i = 0; i < 16; i++) {
trackList = new int[16];
int key = instruments[i];
for (int j = 0; j < 16; j++) {
JCheckBox jc = checkboxList.get(j + 16 * i);
if (jc.isSelected()) {
trackList[j] = key;
} else {
trackList[j] = 0;
}
}
makeTracks(trackList);
track.add(makeEvent(CONTROL_CHANGE, 1, 127, 0, 16));
}
track.add(makeEvent(PROGRAM_CHANGE, 9, 1, 0, 15));
try {
sequencer.setSequence(sequence);
sequencer.setLoopCount(sequencer.LOOP_CONTINUOUSLY);
sequencer.setTempoInBPM(120);
sequencer.start();
} catch (Exception e) {
e.printStackTrace();
}
}
private void changeTempo(float tempoMultiplier) {
float tempoFactor = sequencer.getTempoFactor();
sequencer.setTempoFactor(tempoFactor * tempoMultiplier);
}
```

```java
private void makeTracks(int[] list) {
for (int i = 0; i < 16; i++) {
int key = list[i];
if (key != 0) {
track.add(makeEvent(NOTE_ON, 9, key, 100, i));
track.add(makeEvent(NOTE_OFF, 9, key, 100, i + 1));
}
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
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
frame.getContentPane().add(BorderLayout.NORTH, panel);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
frame.getContentPane().add(BorderLayout.EAST, panel);
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(button);
frame.getContentPane().add(BorderLayout.NORTH, buttonTwo);
frame.getContentPane().add(BorderLayout.EAST, panel);
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
frame.getContentPane().add(BorderLayout.SOUTH, panel);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.NORTH, button);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
frame.getContentPane().add(BorderLayout.EAST, panel);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
panel.add(button);
frame.getContentPane().add(BorderLayout.NORTH, buttonTwo);
frame.getContentPane().add(BorderLayout.EAST, panel);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
frame.getContentPane().add(BorderLayout.SOUTH, panel);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.NORTH, button);
```

```java
JFrame frame = new JFrame();
JPanel panel = new JPanel();
panel.setBackground(Color.darkGray);
JButton button = new JButton("tesuji");
JButton buttonTwo = new JButton("watari");
frame.getContentPane().add(BorderLayout.NORTH, panel);
panel.add(buttonTwo);
frame.getContentPane().add(BorderLayout.CENTER, button);
```