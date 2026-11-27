# Chapter 16: Chapter 16: Saving Objects (and Text)

pages 577-624

the class, but state lives within each individual object. So what happens when it’s time to save the state of an object? If you’re writing a game, you’re gonna need a Save/Restore Game feature. If you’re writing an app that creates charts, you’re gonna need a Save/Open File feature. If your program needs to save state, you can do it the hard way, interrogating each object, then painstakingly writing the value of each instance variable

to a file, in a format you create. Or, you can do it the easy OO way—you simply freeze-dry/flatten/persist/ dehydrate the object itself, and reconstitute/inflate/restore/rehydrate it to get it back. But you’ll still have to do it the hard way sometimes, especially when the file your app saves has to be read by some other non-Java application, so we’ll look at both in this chapter. And since all I/O operations are risky, we’ll take a look at how

## Capture the beat <!--p578-->

## Saving state <!--p579-->

## Writing a serialized object to a file <!--p580-->

```java
FileOutputStream fileStream = new FileOutputStream("MyGame.ser");
```

```java
os.writeObject(characterOne);
os.writeObject(characterTwo);
os.writeObject(characterThree);
```

sources such as files or network sockets, and chain streams that work only if chained to other streams. Often, it takes at least two streams hooked together to do something useful—one to represent the connection and another to call methods on. Why two? Because connection streams are usually too low-level. FileOutputStream (a connection stream), for example, has methods for writing bytes. But we don’t want to write bytes! We want to write objects, so we need a higher-level chain stream.

OK, then why not have just a single stream that does exactly what you want? One that lets you write objects but underneath converts them to bytes? Think good OO. Each class does one thing well. FileOutputStreams write bytes to a file. ObjectOutputStreams turn objects into data that can be written to a stream. So we make a FileOutputStream (a connection stream) that lets us write to a file, and we hook an ObjectOutputStream (a chain stream) on the end of it. When we call writeObject() on the ObjectOutputStream, the object gets pumped into the stream and then moves to the FileOutputStream where it ultimately gets written as bytes to a file.

The ability to mix and match different combinations of connection and chain streams gives you tremendous flexibility! If you were forced to use only a single stream class, you’d be at the mercy of the API designers, hoping they’d thought of everything you might ever want to do. But with chaining, you can patch together your own custom chains.

## Data moves in streams from one place to another <!--p581-->

```java
Foo myFoo = new Foo();
myFoo.setWidth(37);
myFoo.setHeight(70);
FileOutputStream fs = new FileOutputStream("foo.ser");
ObjectOutputStream os = new ObjectOutputStream(fs);
os.writeObject(myFoo);
```

```java
objectOutputStream.writeObject(mySquare);
```

```java
import java.io.*;
public class Square implements Serializable {
private int width;
private int height;
public Square(int width, int height) {
this.width = width;
this.height = height;
}
public static void main(String[] args) {
Square mySquare = new Square(50, 20);
try {
FileOutputStream fs = new FileOutputStream("foo.ser");
ObjectOutputStream os = new ObjectOutputStream(fs);
os.writeObject(mySquare);
os.close();
} catch (Exception ex) {
ex.printStackTrace();
}
}
}
```

```java
import java.io.*;
public class Pond implements Serializable {
private Duck duck = new Duck();
public static void main(String[] args) {
Pond myPond = new Pond();
try {
FileOutputStream fs = new FileOutputStream("Pond.ser");
ObjectOutputStream os = new ObjectOutputStream(fs);
os.writeObject(myPond);
os.close();
} catch (Exception ex) {
ex.printStackTrace();
}
}
}
```

```java
public class Duck {
// duck code here
}
```

```java
% java Pond
java.io.NotSerializableException: Duck
at Pond.main(Pond.java:13)
```

```java
import java.net.*;
class Chat implements Serializable {
transient String currentID;
String userName;
// more code
}
```

## Deserialization: restoring an object <!--p589-->

```java
FileInputStream fileStream = new FileInputStream("MyGame.ser");
```

```java
Object one = os.readObject();
Object two = os.readObject();
Object three = os.readObject();
```

```java
GameCharacter elf = (GameCharacter) one;
GameCharacter troll = (GameCharacter) two;
GameCharacter magician = (GameCharacter) three;
```

## What happens during deserialization? <!--p590-->

## Saving and restoring the game characters <!--p592-->

```java
import java.io.*;
public class GameSaverTest {
public static void main(String[] args) {
GameCharacter one = new GameCharacter(50, "Elf",
new String[]{"bow", "sword", "dust"});
GameCharacter two = new GameCharacter(200, "Troll",
new String[]{"bare hands", "big ax"});
GameCharacter three = new GameCharacter(120, "Magician",
new String[]{"spells", "invisibility"});
// imagine code that does things with the characters that changes their state values
try {
ObjectOutputStream os = new ObjectOutputStream(new FileOutputStream("Game.ser"));
os.writeObject(one);
os.writeObject(two);
os.writeObject(three);
os.close();
} catch (IOException ex) {
ex.printStackTrace();
}
try {
ObjectInputStream is = new ObjectInputStream(new FileInputStream("Game.ser"));
GameCharacter oneRestore = (GameCharacter) is.readObject();
GameCharacter twoRestore = (GameCharacter) is.readObject();
GameCharacter threeRestore = (GameCharacter) is.readObject();
System.out.println("One's type: " + oneRestore.getType());
System.out.println("Two's type: " + twoRestore.getType());
System.out.println("Three's type: " + threeRestore.getType());
} catch (Exception ex) {
ex.printStackTrace();
}
}
}
```

```java
One’s type: Elf
Two’s type: Troll
Three’s type: Magician
```

```java
import java.io.*;
import java.util.Arrays;
public class GameCharacter implements Serializable {
private final int power;
private final String type;
private final String[] weapons;
public GameCharacter(int power, String type, String[] weapons) {
this.power = power;
this.type = type;
this.weapons = weapons;
}
public int getPower() {
return power;
}
public String getType() {
return type;
}
public String getWeapons() {
return Arrays.toString(weapons);
}
}
```

## The GameCharacter class <!--p593-->

## Version ID: A big serialization gotcha <!--p594-->

```java
101101
101101
10101000010
1010 10 0
01010 1
1010101
10101010
1001010101
```

```java
101101
101101
101000010
1010 10 0
01010 1
100001 1010
0 00110101
1 0 1 10 10
```

```java
101101
101101
101000010
1010 10 0
01010 1
100001 1010
0 00110101
1 0 1 10 10
```

## Using the serialVersionUID <!--p595-->

```java
Dog: static final long
serialVersionUID =
-5849794470654667210L;
public class Dog {
static final long serialVersionUID =
-5849794470654667210L;
private String name;
private int size;
// method code here
}
```

```java
Dog: static final long
serialVersionUID =
-5849794470654667210L;
```

## Writing a String to a Text File <!--p597-->

```java
objectOutputStream.writeObject(someObject);
```

```java
fileWriter.write("My first String to save");
import java.io.*;
class WriteAFile {
public static void main(String[] args) {
try {
FileWriter writer = new FileWriter("Foo.txt");
writer.write("hello foo!");
writer.close();
} catch (IOException ex) {
ex.printStackTrace();
}
}
}
```

## Text file example: e-Flashcards <!--p598-->

## Quiz Card Builder (code outline) <!--p599-->

```java
public class QuizCardBuilder {
public void go() {
// build and display gui
}
private void nextCard() {
// add the current card to the list
// and clear the text areas
}
private void saveCard() {
// bring up a file dialog box
// let the user name and save the set
}
private void clearCard() {
// clear out the text areas
}
private void saveFile(File file) {
// iterate through the list of cards and write
// each one out to a text file in a parseable way
// (in other words, with clear separations between parts)
}
}
```

The Java API has included I/O features since day one, you know, back in the last millennium. In 2002, Java 1.4 was released, and it included a new approach to I/O called “NIO,” short for non-blocking I/O. In 2011, Java 7 was released, and it included big enhancements to NIO. This yet again newer approach to I/O was dubbed “NIO.2.” Why should you care? When you’re writing new I/O, you should use the latest and greatest features. But you’re almost certainly going to encounter older code that uses the NIO ap­ proach. We want you to be covered for both situations, so in this chapter:

```java
import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.util.ArrayList;
public class QuizCardBuilder {
private ArrayList<QuizCard> cardList = new ArrayList<>();
private JTextArea question;
private JTextArea answer;
private JFrame frame;
public static void main(String[] args) {
new QuizCardBuilder().go();
}
public void go() {
frame = new JFrame("Quiz Card Builder");
JPanel mainPanel = new JPanel();
Font bigFont = new Font("sanserif", Font.BOLD, 24);
question = createTextArea(bigFont);
JScrollPane qScroller = createScroller(question);
answer = createTextArea(bigFont);
JScrollPane aScroller = createScroller(answer);
mainPanel.add(new JLabel("Question:"));
mainPanel.add(qScroller);
mainPanel.add(new JLabel("Answer:"));
mainPanel.add(aScroller);
JButton nextButton = new JButton("Next Card");
nextButton.addActionListener(e -> nextCard());
mainPanel.add(nextButton);
JMenuBar menuBar = new JMenuBar();
JMenu fileMenu = new JMenu("File");
JMenuItem newMenuItem = new JMenuItem("New");
newMenuItem.addActionListener(e -> clearAll());
JMenuItem saveMenuItem = new JMenuItem("Save");
saveMenuItem.addActionListener(e -> saveCard());
fileMenu.add(newMenuItem);
fileMenu.add(saveMenuItem);
menuBar.add(fileMenu);
frame.setJMenuBar(menuBar);
frame.getContentPane().add(BorderLayout.CENTER, mainPanel);
frame.setSize(500, 600);
frame.setVisible(true);
}
```

You'll see more I/O, NIO, and NIO.2 features in Chapter 17, Make a Connection, when we look at network connections. Java I/O to NIO to NIO.2 We make a menu bar, make a File menu, then put ‘New’ and ‘Save’ menu items into the File menu. We add the menu to the menu bar, and then tell the frame to use this menu bar. Menu items can fire an ActionEvent. Quiz Card Builder code This is all GUI code here. Nothing special, although you might want to look at the code for the new GUI components MenuBar, Menu, and MenuItems.

```java
private JScrollPane createScroller(JTextArea textArea) {
JScrollPane scroller = new JScrollPane(textArea);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
return scroller;
}
private JTextArea createTextArea(Font font) {
JTextArea textArea = new JTextArea(6, 20);
textArea.setLineWrap(true);
textArea.setWrapStyleWord(true);
textArea.setFont(font);
return textArea;
}
private void nextCard() {
QuizCard card = new QuizCard(question.getText(), answer.getText());
cardList.add(card);
clearCard();
}
private void saveCard() {
QuizCard card = new QuizCard(question.getText(), answer.getText());
cardList.add(card);
JFileChooser fileSave = new JFileChooser();
fileSave.showSaveDialog(frame);
saveFile(fileSave.getSelectedFile());
}
private void clearAll() {
cardList.clear();
clearCard();
}
private void clearCard() {
question.setText("");
answer.setText("");
question.requestFocus();
}
private void saveFile(File file) {
try {
BufferedWriter writer = new BufferedWriter(new FileWriter(file));
for (QuizCard card : cardList) {
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
}
writer.close();
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
}
}
}
```

## The java.io.File class <!--p602-->

```java
File f = new File("MyCode.txt");
```

```java
File dir = new File("Chapter7");
dir.mkdir();
```

```java
if (dir.isDirectory()) {
String[] dirContents = dir.list();
for (String dirContent : dirContents) {
System.out.println(dirContent);
}
}
```

```java
boolean isDeleted = f.delete();
```

## The beauty of buffers <!--p603-->

BufferedWriter will hold all the stuff you write to it until it’s full. Only when the buffer is fullwill the FileWriter actually be told to write to the file on disk. If you do want to send data before the buffer is full, you do have control. Just Flush It. Calls to writer.flush() say, “send whatever’s in the buffer, now!” Buffers give you a temporary holding place to group things until the holder (like the cart) is full. You get to make far fewer trips when you use a buffer.

```java
BufferedWriter writer = new BufferedWriter(new FileWriter(aFile));
```

## Reading from a text file <!--p604-->

```java
import java.io.*;
class ReadAFile {
public static void main(String[] args) {
try {
File myFile = new File("MyText.txt");
FileReader fileReader = new FileReader(myFile);
BufferedReader reader = new BufferedReader(fileReader);
String line;
while ((line = reader.readLine()) != null) {
System.out.println(line);
}
reader.close();
} catch (IOException e) {
e.printStackTrace();
}
}
}
```

```java
Files.lines(Path.of("MyText.txt"))
.forEach(line -> System.out.println(line));
```

## Quiz Card Player (code outline) <!--p605-->

```java
public class QuizCardPlayer {
public void go() {
// build and display gui
}
private void nextCard() {
// if this is a question, show the answer, otherwise show
// next question set a flag for whether we’re viewing a
// question or answer
}
private void open() {
// bring up a file dialog box
// let the user navigate to and choose a card set to open
}
private void loadFile(File file) {
// must build an ArrayList of cards, by reading them from
// a text file called from the OpenMenuListener event handler,
// reads the file one line at a time and tells the makeCard()
// method to make a new card out of the line (one line in the
// file holds both the question and answer, separated by a “/”)
}
private void makeCard(String lineToParse) {
// called by the loadFile method, takes a line from the text file
// and parses into two pieces—question and answer—and creates a
// new QuizCard and adds it to the ArrayList called CardList
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.util.ArrayList;
public class QuizCardPlayer {
private ArrayList<QuizCard> cardList;
private int currentCardIndex;
private QuizCard currentCard;
private JTextArea display;
private JFrame frame;
private JButton nextButton;
private boolean isShowAnswer;
public static void main(String[] args) {
QuizCardPlayer reader = new QuizCardPlayer();
reader.go();
}
public void go() {
frame = new JFrame("Quiz Card Player");
JPanel mainPanel = new JPanel();
Font bigFont = new Font("sanserif", Font.BOLD, 24);
display = new JTextArea(10, 20);
display.setFont(bigFont);
display.setLineWrap(true);
display.setEditable(false);
JScrollPane scroller = new JScrollPane(display);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
mainPanel.add(scroller);
nextButton = new JButton("Show Question");
nextButton.addActionListener(e -> nextCard());
mainPanel.add(nextButton);
JMenuBar menuBar = new JMenuBar();
JMenu fileMenu = new JMenu("File");
JMenuItem loadMenuItem = new JMenuItem("Load card set");
loadMenuItem.addActionListener(e -> open());
fileMenu.add(loadMenuItem);
menuBar.add(fileMenu);
frame.setJMenuBar(menuBar);
frame.getContentPane().add(BorderLayout.CENTER, mainPanel);
frame.setSize(500, 400);
frame.setVisible(true);
}
```

```java
private void nextCard() {
if (isShowAnswer) {
// show the answer because they’ve seen the question
display.setText(currentCard.getAnswer());
nextButton.setText("Next Card");
isShowAnswer = false;
} else { // show the next question
if (currentCardIndex < cardList.size()) {
showNextCard();
} else {
// there are no more cards!
display.setText("That was last card");
nextButton.setEnabled(false);
}
}
}
private void open() {
JFileChooser fileOpen = new JFileChooser();
fileOpen.showOpenDialog(frame);
loadFile(fileOpen.getSelectedFile());
}
private void loadFile(File file) {
cardList = new ArrayList<>();
currentCardIndex = 0;
try {
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
while ((line = reader.readLine()) != null) {
makeCard(line);
}
reader.close();
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
}
showNextCard();
}
private void makeCard(String lineToParse) {
String[] result = lineToParse.split("/");
QuizCard card = new QuizCard(result[0], result[1]);
cardList.add(card);
System.out.println("made a card");
}
private void showNextCard() {
currentCard = cardList.get(currentCardIndex);
currentCardIndex++;
display.setText(currentCard.getQuestion());
nextButton.setText("Show Answer");
isShowAnswer = true;
}
}
```

## Parsing with String split() <!--p608-->

```java
String toTest = "What is blue + yellow?/green";
String[] result = toTest.split("/");
for (String token : result) {
System.out.println(token);
}
```

## NIO.2 and the java.nio.file package <!--p610-->

```java
java.nio.file
java.nio.file.attribute
```

```java
Path myPath = Paths.get("MyFile.txt");
```

```java
BufferedWriter writer = Files.newBufferedWriter(myPath);
```

```java
import java.nio.file.*;
```

```java
Path myPath = Paths.get("/myApp", "files", "MyFile.txt");
```

In Appendix B, we’ll be discussing how to split your Java app into packages. This includes creating the proper directory structure for all of your app’s files. In most cases you’ll make and move directories and files by hand, using the command line or utilities like the Finder or Windows Explorer. But you can also do it from within your Java code. Warning! Goofing around with directories in a Java program is a real “can of worms” topic. To do it correctly you need to learn about paths, absolute paths, relative paths, OS permissions, file attributes, and on and on. Below is a greatly simplified example of messing around with directories, just to give you a feel for what’s possible.

Suppose you wanted to make an installer program to install your killer app. You start with the directory and files on the left, and want to end up with the directory structure and files on the right.

## Path, Paths, and Files (messing with directories) <!--p611-->

```java
Lorper
iure eugue
tat vero
conse
eugueroLore
do eliquis
do del dip
101101
101101
10101000010
1010 10 0
01010 1
1010101
10101010
1001010101
```

```java
Lorper
iure eugue
tat vero
conse
eugueroLore
do eliquis
do del dip
101101
101101
10101000010
1010 10 0
01010 1
1010101
10101010
1001010101
```

```java
101101
101101
10101000010
1010 10 0
01010 1
1010101
10101010
1001010101
```

```java
import java.nio.file.*;
public class Install {
public static void main(String[] args) {
try {
Path myPath = Paths.get("MyApp");
Path myPath2 = Paths.get("MyApp", "media");
Path myPath3 = Paths.get("MyApp", "source");
Path mySource = Paths.get("MyApp.class");
Path myMedia = Paths.get("MyMedia.jpeg");
Files.createDirectory(myPath);
Files.createDirectory(myPath2);
Files.createDirectory(myPath3);
Files.move(mySource, myPath3.resolve(mySource.getFileName()));
Files.move(myMedia, myPath2.resolve(myMedia.getFileName()));
} catch (Exception e) {
System.out.println("Got an NIO Exception" + e.getMessage());
}
}
}
```

## Finally, a closer look at finally <!--p612-->

```java
private void saveFile(File file) {
try {
BufferedWriter writer = new BufferedWriter(new FileWriter(file));
for (QuizCard card : cardList) {
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
}
writer.close();
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
}
}
```

```java
private void saveFile(File file) {
BufferedWriter writer = null;
try {
writer = new BufferedWriter(new FileWriter(file));
for (QuizCard card : cardList) {
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
}
writer.close();
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
} finally {
try {
writer.close();
} catch (Exception e) {
System.out.println("Couldn't close writer: " + e.getMessage());
}
}
```

## The try-with-resources (TWR), statement <!--p614-->

```java
private void saveFile(File file) {
BufferedWriter writer = null;
try {
writer = new BufferedWriter(new FileWriter(file));
for (QuizCard card : cardList) {
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
}
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
} finally {
try {
writer.close();
} catch (Exception e) {
System.out.println("Couldn't close writer: " + e.getMessage());
}
}
}
```

```java
private void saveFile(File file) {
try (BufferedWriter writer =
new BufferedWriter(new FileWriter(file))) {
for (QuizCard card : cardList) {
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
}
} catch (IOException e) {
System.out.println("Couldn't write the cardList out: " + e.getMessage());
}
}
```

## Autocloseable, the very small catch <!--p615-->

```java
try (BufferedWriter writer =
new BufferedWriter(new FileWriter(file))) {
```

```java
try (BufferedWriter writer =
new BufferedWriter(new FileWriter(file))) {
```

```java
try ( ... ) {
```

```java
writer.write(card.getQuestion() + "/");
writer.write(card.getAnswer() + "\n");
```

```java
try (BufferedWriter writer =
new BufferedWriter(new FileWriter(file));
BufferedReader reader =
new BufferedReader(new FileReader(file))) {
```

## Code Kitchen <!--p616-->

## Saving a BeatBox pattern <!--p617-->

```java
private void writeFile() {
boolean[] checkboxState = new boolean[256];
for (int i = 0; i < 256; i++) {
JCheckBox check = checkboxList.get(i);
if (check.isSelected()) {
checkboxState[i] = true;
}
}
try (ObjectOutputStream os =
new ObjectOutputStream(new FileOutputStream("Checkbox.ser"))) {
os.writeObject(checkboxState);
} catch (IOException e) {
e.printStackTrace();
}
}
```

## Restoring a BeatBox pattern <!--p618-->

```java
private void readFile() {
boolean[] checkboxState = null;
try (ObjectInputStream is =
new ObjectInputStream(new FileInputStream("Checkbox.ser"))) {
checkboxState = (boolean[]) is.readObject();
} catch (Exception e) {
e.printStackTrace();
}
for (int i = 0; i < 256; i++) {
JCheckBox check = checkboxList.get(i);
check.setSelected(checkboxState[i]);
}
sequencer.stop();
buildTrackAndStart();
}
```

```java
FileReader fileReader = new FileReader();
BufferedReader reader = new BufferedReader(fileReader);
FileOutputStream f = new FileOutputStream("Foo.ser");
ObjectOutputStream os = new ObjectOutputStream(f);
BufferedReader reader = new BufferedReader(new FileReader(file));
String line;
while ((line = reader.readLine()) != null) {
makeCard(line);
}
FileOutputStream f = new FileOutputStream("Game.ser");
ObjectInputStream is = new ObjectInputStream(f);
GameCharacter oneAgain = (GameCharacter) is.readObject();
```

9. Only classes that implement AutoCloseable can be used in try-with-resources statements. 10. When an object is deserialized, its constructor does not run. 11. Both serialization and saving to a text file can throw exceptions. 12. BufferedWriters can be chained to FileWriters. 13. File objects represent files, but not directories. 14. You can’t force a buffer to send its data before it’s full. 15. Both file readers and file writers can optionally be buffered.

```java
public static void main(String[] args) {
DungeonGame d = new DungeonGame();
int getX() {
return x;
public int x = 3;
transient long y = 4;
private short z = 5;
```

```java
% java DungeonTest
class DungeonTest {
long getY() {
return y;
short getZ() {
return z;
d = (DungeonGame) ois.readObject();
} catch (Exception e) {
ois.close();
class DungeonGame implements Serializable {
e.printStackTrace();
FileOutputStream fos = new
FileOutputStream("dg.ser");
oos.close();
fos.writeObject(d);
ObjectOutputStream oos = new
ObjectOutputStream(fos);
ObjectInputStream ois = new
ObjectInputStream(fis);
oos.writeObject(d);
try {
System.out.println(d.getX()+d.getY()+d.getZ());
FileInputStream fis = new
FileInputStream("dg.ser");
import java.io.*;
```

9. Only classes that implement AutoCloseable can be used in try-with-resources statements. 10. When an object is deserialized, its constructor does not run. 11. Both serialization and saving to a text file can throw exceptions. 12. BufferedWriters can be chained to FileWriters. 13. File objects represent files, but not directories. 14. You can’t force a buffer to send its data before it’s full. 15. Both file readers and file writers can optionally be buffered.

```java
% java DungeonTest
import java.io.*;
class DungeonGame implements Serializable {
public int x = 3;
transient long y = 4;
private short z = 5;
int getX() {
return x;
}
long getY() {
return y;
}
short getZ() {
return z;
}
}
class DungeonTest {
public static void main(String[] args) {
DungeonGame d = new DungeonGame();
System.out.println(d.getX() + d.getY() + d.getZ());
try {
FileOutputStream fos = new FileOutputStream("dg.ser");
ObjectOutputStream oos = new ObjectOutputStream(fos);
oos.writeObject(d);
oos.close();
FileInputStream fis = new FileInputStream("dg.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
d = (DungeonGame) ois.readObject();
ois.close();
} catch (Exception e) {
e.printStackTrace();
}
System.out.println(d.getX() + d.getY() + d.getZ());
}
}
```