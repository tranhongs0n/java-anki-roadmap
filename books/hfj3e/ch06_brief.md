# Chapter 6: Chapter 6: Using the Java Library

pages 163-204

the wheel if you know how to find what you need in the Java library, known as the Java API. You’ve got better things to do. If you’re going to write code, you might as well write only the parts that are truly custom for your application. You know those programmers who walk out the door each night at 5 PM? The ones who don’t even show up until 10 AM? They use the Java API. And about eight pages from now, so will you. The core Java library is a giant pile of

classes just waiting for you to use like building blocks, to assemble your own program out of largely prebuilt code. The Ready-Bake Java we use in this book is code you don’t have to create from scratch, but you still have to type it. The Java API is full of code you don’t even have to type. All you need to do is learn to use it. Using the Java Library So it’s true? We don’t have to build it ourselves?

```java
enter a number 1
miss
enter a number 2
miss
enter a number 3
miss
enter a number 4
hit
enter a number 5
hit
enter a number 6
kill
You took 6 guesses
```

```java
enter a number 2
hit
enter a number 2
hit
enter a number 2
kill
You took 3 guesses
```

## So what happened? <!--p165-->

```java
public String checkYourself(int guess) {
String result = "miss";
for (int cell : locationCells) {
if (guess == cell) {
result = "hit";
numOfHits++;
break;
} // end if
} // end for
if (numOfHits == locationCells.length) {
result = "kill";
} // end if
System.out.println(result);
return result;
} // end method
```

## How do we fix it? <!--p166-->

## Option one is too clunky <!--p167-->

## Option three <!--p168-->

## Wake up and smell the library <!--p170-->

## Some things you can do with ArrayList <!--p171-->

```java
myList.add(egg1);
```

```java
myList.add(egg2);
```

```java
ArrayList<String> myList = new
ArrayList<String>();
```

```java
myList.add(a);
```

```java
myList.add(b);
int theSize = myList.size();
String str = myList.get(1);
myList.remove(1);
boolean isIn = myList.contains(b);
```

object from the array. It’s still there. But I can just set its reference to null, I guess. ArrayList: But I’m a first-class object, so I have methods, and I can actually, you know, do things like remove the Dog’s reference from myself, not just set it to null. And I can change my size, dynamically (look it up). Just try to get an array to do that! HeadFirst: Gee, hate to bring this up, but the rumor is that you’re nothing more than a glorified but less-efficient array. That in fact you’re just a wrapper for an array, adding extra methods for things like resizing that I would have had to write myself. And while we’re at it, you can’t even hold primitives! Isn’t that a big limitation?

array might be just a tad, I repeat, tad bit faster for certain things. But is it worth the miniscule performance gain to give up all this power? Still, look at all this flexibility. And as for the primitives, of course you can put a primitive in an ArrayList, as long as it’s wrapped in a primitive wrapper class (you’ll see a lot more on that in Chapter 10). And if you’re using Java 5 or above, that wrapping (and unwrapping when you take the primitive out again) happens automatically. And alright, I’ll acknowledge that yes, if you’re using an ArrayList of primitives, it probably is faster with an array, because of all the wrapping and unwrapping, but still...who really uses primitives these days?

```java
ArrayList<String> myList = new
ArrayList<String>();
String [] myList = new String[2];
String a = "whoohoo";
String a = "whoohoo";
myList.add(a);
myList[0] = a;
String b = "Frog";
String b = "Frog";
myList.add(b);
myList[1] = b;
int theSize = myList.size();
int theSize = myList.length;
String str = myList.get(1);
String str = myList[1];
myList.remove(1);
myList[1] = null;
boolean isIn = myList.contains(b);
boolean isIn = false;
for (String item : myList) {
if (b.equals(item)) {
isIn = true;
break;
}
}
```

```java
myList[1] = b;
```

```java
myList.add(b);
```

```java
myList[1]
new String[2]
new ArrayList<String>()
```

## Comparing ArrayList to a regular array <!--p175-->

```java
ArrayList<String>
```

## Let’s fix the Startup code <!--p176-->

```java
class Startup {
private int[] locationCells;
private int numOfHits = 0;
public void setLocationCells(int[] locs) {
locationCells = locs;
}
public String checkYourself(int guess) {
String result = "miss";
for (int cell : locationCells) {
if (guess == cell) {
result = "hit";
numOfHits++;
break;
}
} // end for
if (numOfHits == locationCells.length) {
result = "kill";
} // end if
System.out.println(result);
return result;
} // end method
} // close class
```

```java
import java.util.ArrayList;
public class Startup {
private ArrayList<String> locationCells;
// private int numOfHits;
// don't need to track this now
public void setLocationCells(ArrayList<String> locs) {
locationCells = locs;
}
public String checkYourself(String userInput) {
String result = "miss";
int index = locationCells.indexOf(userInput);
if (index >= 0) {
locationCells.remove(index);
if (locationCells.isEmpty()) {
result = "kill";
} else {
result = "hit";
} // end if
} // end outer if
return result;
} // end method
} // close class
```

## New and improved Startup class <!--p177-->

```java
Enter a guess A3
miss
Enter a guess B2
miss
Enter a guess C4
miss
Enter a guess D2
hit
Enter a guess D3
hit
Enter a guess D4
Ouch! You sunk poniez : (
kill
Enter a guess G3
hit
Enter a guess G4
hit
Enter a guess G5
Ouch! You sunk hacqi : (
All Startups are dead! Your stock
is now worthless
Took you long enough. 62 guesses.
```

## What needs to change? <!--p179-->

DECLARE and instantiate an ArrayList to hold the list of Startups (initially three) Call it startups. DECLARE an int variable to hold the number of user guesses (so that we can give the user a score at the end of the game). Name it numOfGuesses and set it to 0. DECLARE a setUpGame() method to create and initialize the Startup objects with names and locations. Display brief instructions to the user.

location for this Startup (three cells, vertically or horizontally aligned, on a 7 X 7 grid). SET the location for each Startup based on the result of the placeStartup() call. END REPEAT END METHOD StartupBust The StartupBust class has three main jobs: set up the game, play the game until the Startups are dead, and end the game. Although we could map those three jobs directly into three methods, we split the middle job (play the game) into two methods to keep the granularity smaller. Smaller methods (meaning smaller chunks of func­ tionality) help us test, debug, and modify the code more easily.

## Prep code for the real StartupBust class <!--p182-->

SET the local result variable (a String) to “miss”, assuming that the user’s guess will be a miss. REPEAT with each of the Startup objects in the startups List. EVALUATE the user’s guess by calling the Startup object’s checkYourself() method. SET the result variable to “hit” or “kill” if appropriate. IF the result is “kill”, REMOVE the Startup from the startups List. END REPEAT DISPLAY the result value to the user.

```java
import java.util.ArrayList;
public class StartupBust {
private GameHelper helper = new GameHelper();
private ArrayList<Startup> startups = new ArrayList<Startup>();
private int numOfGuesses = 0;
private void setUpGame() {
// first make some Startups and give them locations
Startup one = new Startup();
one.setName("poniez");
Startup two = new Startup();
two.setName("hacqi");
Startup three = new Startup();
three.setName("cabista");
startups.add(one);
startups.add(two);
startups.add(three);
System.out.println("Your goal is to sink three Startups.");
System.out.println("poniez, hacqi, cabista");
System.out.println("Try to sink them all in the fewest number of guesses");
for (Startup startup : startups) {
ArrayList<String> newLocation = helper.placeStartup(3);
startup.setLocationCells(newLocation);
} // close for loop
} // close setUpGame method
private void startPlaying() {
while (!startups.isEmpty()) {
String userGuess = helper.getUserInput("Enter a guess");
checkUserGuess(userGuess);
} // close while
finishGame();
} // close startPlaying method
```

```java
private void checkUserGuess(String userGuess) {
numOfGuesses++;
String result = "miss";
for (Startup startupToTest : startups) {
result = startupToTest.checkYourself(userGuess);
if (result.equals("hit")) {
break;
}
if (result.equals("kill")) {
startups.remove(startupToTest);
break;
}
} // close for
System.out.println(result);
} // close method
private void finishGame() {
System.out.println("All Startups are dead! Your stock is now worthless");
if (numOfGuesses <= 18) {
System.out.println("It only took you " + numOfGuesses + " guesses.");
System.out.println("You got out before your options sank.");
} else {
System.out.println("Took you long enough. " + numOfGuesses + " guesses.");
System.out.println("Fish are dancing with your options");
}
} // close method
public static void main(String[] args) {
StartupBust game = new StartupBust();
game.setUpGame();
game.startPlaying();
} // close method
}
```

```java
import java.util.ArrayList;
public class StartupBust {
private GameHelper helper = new GameHelper();
private ArrayList<Startup> startups = new ArrayList<Startup>();
private int numOfGuesses = 0;
private void setUpGame() {
// first make some Startups and give them locations
Startup one = new Startup();
one.setName("poniez");
Startup two = new Startup();
two.setName("hacqi");
Startup three = new Startup();
three.setName("cabista");
startups.add(one);
startups.add(two);
startups.add(three);
System.out.println("Your goal is to sink three Startups.");
System.out.println("poniez, hacqi, cabista");
System.out.println("Try to sink them all in the fewest number of guesses");
for (Startup startup : startups) {
ArrayList<String> newLocation = helper.placeStartup(3);
startup.setLocationCells(newLocation);
} // close for loop
} // close setUpGame method
private void startPlaying() {
while (!startups.isEmpty()) {
String userGuess = helper.getUserInput("Enter a guess");
checkUserGuess(userGuess);
} // close while
finishGame();
} // close startPlaying method
```

```java
private void checkUserGuess(String userGuess) {
numOfGuesses++;
String result = "miss";
for (Startup startupToTest : startups) {
result = startupToTest.checkYourself(userGuess);
if (result.equals("hit")) {
break;
}
if (result.equals("kill")) {
startups.remove(startupToTest);
break;
}
} // close for
System.out.println(result);
} // close method
private void finishGame() {
System.out.println("All Startups are dead! Your stock is now worthless");
if (numOfGuesses <= 18) {
System.out.println("It only took you " + numOfGuesses + " guesses.");
System.out.println("You got out before your options sank.");
} else {
System.out.println("Took you long enough. " + numOfGuesses + " guesses.");
System.out.println("Fish are dancing with your options");
}
} // close method
public static void main(String[] args) {
StartupBust game = new StartupBust();
game.setUpGame();
game.startPlaying();
} // close method
}
```

```java
import java.util.ArrayList;
public class Startup {
private ArrayList<String> locationCells;
private String name;
public void setLocationCells(ArrayList<String> loc) {
locationCells = loc;
}
public void setName(String n) {
name = n;
}
public String checkYourself(String userInput) {
String result = "miss";
int index = locationCells.indexOf(userInput);
if (index >= 0) {
locationCells.remove(index);
if (locationCells.isEmpty()) {
result = "kill";
System.out.println("Ouch! You sunk " + name + " : ( ");
} else {
result = "hit";
} // end if
} // end outer if
return result;
} // end method
} // close class
```

## Super powerful Boolean expressions <!--p189-->

```java
if (price >= 300 && price < 400) {
camera = "X";
}
```

```java
if (brand.equals("A") || brand.equals("B")) {
// do stuff for only brand A or brand B
}
```

```java
if ((zoomType.equals("optical") &&
(zoomDegree >= 3 && zoomDegree <= 8)) ||
(zoomType.equals("digital") &&
(zoomDegree >= 5 && zoomDegree <= 12))) {
// do appropriate zoom stuff
}
```

```java
if (model != 2000) {
// do non-model 2000 stuff
}
```

```java
if (!brand.equals("X")) {
// do non-brand X stuff
}
```

```java
if (refVar != null &&
refVar.isValidType()) {
// do ‘got a valid type’ stuff
}
```

```java
import java.util.*;
public class GameHelper {
private static final String ALPHABET = "abcdefg";
private static final int GRID_LENGTH = 7;
private static final int GRID_SIZE = 49;
private static final int MAX_ATTEMPTS = 200;
static final int HORIZONTAL_INCREMENT = 1; // A better way to represent these two
static final int VERTICAL_INCREMENT = GRID_LENGTH; // things is an enum (see Appendix B)
private final int[] grid = new int[GRID_SIZE];
private final Random random = new Random();
private int startupCount = 0;
public String getUserInput(String prompt) {
System.out.print(prompt + ": ");
Scanner scanner = new Scanner(System.in);
return scanner.nextLine().toLowerCase();
} //end getUserInput
public ArrayList<String> placeStartup(int startupSize) {
// holds index to grid (0 - 48)
int[] startupCoords = new int[startupSize]; // current candidate co-ordinates
int attempts = 0; // current attempts counter
boolean success = false; // flag = found a good location?
startupCount++; // nth Startup to place
int increment = getIncrement(); // alternate vert & horiz alignment
while (!success & attempts++ < MAX_ATTEMPTS) { // main search loop
int location = random.nextInt(GRID_SIZE); // get random starting point
for (int i = 0; i < startupCoords.length; i++) { // create array of proposed coords
startupCoords[i] = location; // put current location in array
location += increment; // calculate the next location
}
// System.out.println("Trying: " + Arrays.toString(startupCoords));
if (startupFits(startupCoords, increment)) { // startup fits on the grid?
success = coordsAvailable(startupCoords); // ...and locations aren't taken?
} // end loop
} // end while
savePositionToGrid(startupCoords); // coords passed checks, save
ArrayList<String> alphaCells = convertCoordsToAlphaFormat(startupCoords);
// System.out.println("Placed at: "+ alphaCells);
return alphaCells;
} //end placeStartup
```

```java
private boolean startupFits(int[] startupCoords, int increment) {
int finalLocation = startupCoords[startupCoords.length - 1];
if (increment == HORIZONTAL_INCREMENT) {
// check end is on same row as start
return calcRowFromIndex(startupCoords[0]) == calcRowFromIndex(finalLocation);
} else {
return finalLocation < GRID_SIZE; // check end isn't off the bottom
}
} //end startupFits
private boolean coordsAvailable(int[] startupCoords) {
for (int coord : startupCoords) { // check all potential positions
if (grid[coord] != 0) { // this position already taken
// System.out.println("position: " + coord + " already taken.");
return false; // NO success
}
}
return true; // there were no clashes, yay!
} //end coordsAvailable
private void savePositionToGrid(int[] startupCoords) {
for (int index : startupCoords) {
grid[index] = 1; // mark grid position as 'used'
}
} //end savePositionToGrid
private ArrayList<String> convertCoordsToAlphaFormat(int[] startupCoords) {
ArrayList<String> alphaCells = new ArrayList<String>();
for (int index : startupCoords) { // for each grid coordinate
String alphaCoords = getAlphaCoordsFromIndex(index); // turn it into an "a0" style
alphaCells.add(alphaCoords); // add to a list
}
return alphaCells; // return the "a0"-style coords
} // end convertCoordsToAlphaFormat
private String getAlphaCoordsFromIndex(int index) {
int row = calcRowFromIndex(index); // get row value
int column = index % GRID_LENGTH; // get numeric column value
String letter = ALPHABET.substring(column, column + 1); // convert to letter
return letter + row;
} // end getAlphaCoordsFromIndex
private int calcRowFromIndex(int index) {
return index / GRID_LENGTH;
} // end calcRowFromIndex
private int getIncrement() {
if (startupCount % 2 == 0) { // if EVEN Startup
return HORIZONTAL_INCREMENT; // place horizontally
} else { // else ODD
return VERTICAL_INCREMENT; // place vertically
}
} //end getIncrement
} //end class
```

## Using the Library (the Java API) <!--p192-->

```java
import java.util.ArrayList;
public class MyClass {... }
```

```java
java.util.ArrayList
```

```java
java.util.ArrayList<Dog> list = new java.util.ArrayList<Dog>();
```

```java
public void go(java.util.ArrayList<Dog> list) { }
```

```java
public java.util.ArrayList<Dog> foo() {...}
```

## How to discover the API <!--p196-->

Java comes with a fabulous set of online docs called, strangely, the Java API. You (or your IDE) can also download the docs to have on your hard drive just in case your internet connection fails at the Worst Possible Moment. The API docs are the best reference for getting more details about what’s in a package, and what the classes and interfaces in the package provide (e.g., in terms of methods and functionality).

Java 9 introduced the Java Module System, which we’re not going to cover in this book. What you do need to know to understand the docs is that the JDK is now split into modules. These modules group together related packages. This can make it easier to find the classes that interest you, because they’re grouped by function. All of the classes we’ve covered in this book so far are in the java.base module; this contains core Java packages like java.lang and java.util.

## Using the class documentation <!--p200-->

Whichever version of the Java docs you’re using, they all have a similar layout for showing information about a specific class. This is where the juicy details are. Let’s say you were browsing through the reference book and found a class called ArrayList, in java.util. The book tells you a little about it, enough to know that this is indeed what you want to use, but you still need to know more about the methods. In the reference book, you’ll find the method indexOf(). But if all you knew is that there is a method called indexOf() that takes an object and returns the index (an int) of that object, you still need to know one crucial thing: what happens if the object is not in the ArrayList? Looking at the method signature alone won’t tell you how that works. But the API docs will (most of the time, anyway). The API docs tell you that the indexOf() method returns a -1 if the object parameter is not in the ArrayList. So now we know we can use it both as a way to check if an object is even in the ArrayList, and to get its index at the same time, if the object was there. But without the API docs, we might have thought that the indexOf() method would blow up if the object wasn’t in the ArrayList.

```java
if (a.contains("three")) {
a.add("four");
}
import java.util.ArrayList;
public class ArrayListMagnet {
ArrayList<String> a = new ArrayList<String>();
public static void main (String[] args) {
a.add(0, "zero");
a.add(1, "one");
a.add(3, "three");
printList(a);
a.remove(2);
if (a.indexOf("four") != 4) {
a.add(4, "4.2");
}
if (a.contains("two")) {
a.add("2.2");
}
public static void printList(ArrayList<String> list) {
for (String element : list) {
System.out.print(element + " ");
}
System.out.println();
}
}
}
printList(a);
printList(a);
printList(a);
```

```java
% java ArrayListMagnet
zero one two three
zero one three four
zero one three four 4.2
zero one three four 4.2
a.add(2, "two");
```

```java
% java ArrayListMagnet
zero one two three
zero one three four
zero one three four 4.2
zero one three four 4.2
import java.util.ArrayList;
public class ArrayListMagnet {
public static void main(String[] args) {
ArrayList<String> a = new ArrayList<String>();
a.add(0, "zero");
a.add(1, "one");
a.add(2, "two");
a.add(3, "three");
printList(a);
if (a.contains("three")) {
a.add("four");
}
a.remove(2);
printList(a);
if (a.indexOf("four") != 4) {
a.add(4, "4.2");
}
printList(a);
if (a.contains("two")) {
a.add("2.2");
}
printList(a);
}
public static void printList(ArrayList<String> list) {
for (String element : list) {
System.out.print(element + " ");
}
System.out.println();
}
}
```