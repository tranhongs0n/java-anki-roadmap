# Chapter 5: Chapter 5: Extra-Strength Methods

pages 133-162

that too. And why don’t we learn it all by building something real, to see what it’s like to write (and test) a program from scratch. Maybe a game, like Battleships. That’s a heavy-lifting task, so it’ll take two chapters to finish. We’ll build a simple version in this chapter and then build a more powerful deluxe version in Chapter 6, Using the Java Library. Extra-Strength Methods I can lift heavy objects.

```java
%java StartupBust
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

## First, a high-level design <!--p135-->

```java
enter a number 2
hit
enter a number 3
hit
enter a number 4
miss
enter a number 1
kill
You took 4 guesses
```

## Developing a Class <!--p137-->

DECLARE a checkYourself() method that takes a int for the user’s guess (1, 3, etc.), checks it, and returns a result representing a “hit,” “miss,” or “kill.” DECLARE a setLocationCells() setter method that takes an int array (which has the three cell locations as ints (2, 3, 4, etc.)). METHOD: String checkYourself(int userGuess) GET the user guess as an int parameter REPEAT with each of the location cells in the int array

## Writing test code for the SimpleStartup class <!--p140-->

```java
public class SimpleStartupTestDrive {
public static void main(String[] args) {
SimpleStartup dot = new SimpleStartup();
int[] locations = {2, 3, 4};
dot.setLocationCells(locations);
int userGuess = 2;
String result = dot.checkYourself(userGuess);
String testResult = "failed";
if (result.equals("hit")) {
testResult = "passed";
}
System.out.println(testResult);
}
}
```

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

## The checkYourself() method <!--p142-->

## Just the new stuff <!--p143-->

```java
for (int i = 0; i < 10; i++)
{
// do something 10 times
}
```

```java
countdown = i--;
```

## Final code for SimpleStartup and SimpleStartupTestDrive <!--p144-->

```java
public class SimpleStartupTestDrive {
public static void main(String[] args) {
SimpleStartup dot = new SimpleStartup();
int[] locations = {2, 3, 4};
dot.setLocationCells(locations);
int userGuess = 2;
String result = dot.checkYourself(userGuess);
String testResult = "failed";
if (result.equals("hit")) {
testResult = "passed";
}
System.out.println(testResult);
}
}
class SimpleStartup {
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
} // end if
} // end for
if (numOfHits ==
locationCells.length) {
result = "kill";
} // end if
System.out.println(result);
return result;
} // end method
} // close class
```

```java
% java SimpleStartupTestDrive
hit
passed
```

```java
enter a number 2
hit
enter a number 3
hit
enter a number 4
miss
enter a number 1
kill
You took 4 guesses
```

DECLARE an int variable to hold the number of user guesses, named numOfGuesses, and set it to 0 MAKE a new SimpleStartup instance COMPUTE a random number between 0 and 4 that will be the starting location cell position MAKE an int array with 3 ints using the randomly generated number, that number incremented by 1, and that number incremented by 2 (example: 3,4,5) INVOKE the setLocationCells() method on the SimpleStartup instance

DECLARE a boolean variable representing the state of the game, named isAlive.SET it to true WHILE the Startup is still alive (isAlive == true): GET user input from the command line // CHECK the user guess INVOKE the checkYourself() method on the SimpleStartup instance INCREMENT numOfGuesses variable // CHECK for Startup death IF result is “kill” SET isAlive to false (which means we won’t enter the loop again)

## Prep code for the SimpleStartupGame class <!--p146-->

```java
public static void main(String[] args) {
int numOfGuesses = 0;
GameHelper helper = new GameHelper();
SimpleStartup theStartup = new SimpleStartup();
int randomNum = (int) (Math.random() * 5);
int[] locations = {randomNum, randomNum + 1, randomNum + 2};
theStartup.setLocationCells(locations);
boolean isAlive = true;
while (isAlive) {
int guess = helper.getUserInput("enter a number");
String result = theStartup.checkYourself(guess);
numOfGuesses++;
if (result.equals("kill")) {
isAlive = false;
System.out.println("You took " + numOfGuesses + " guesses");
} // close if
} // close while
```

the test code phase for this class, we don’t need a test class for the game. It has only one method, so what would you do in your test code? Make a separate class that would call main() on this class? We didn’t bother, we’ll just run this to test it.

## The game’s main() method <!--p148-->

## random() and getUserInput() <!--p149-->

## One last class: GameHelper <!--p150-->

```java
import java.util.Scanner;
public class GameHelper {
public int getUserInput(String prompt) {
System.out.print(prompt + ": ");
Scanner scanner = new Scanner(System.in);
return scanner.nextInt();
}
}
```

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

## Let’s play <!--p151-->

```java
enter a number 1
hit
enter a number 1
hit
enter a number 1
kill
You took 3 guesses
```

## More about for loops <!--p152-->

```java
x++;
```

```java
x = x + 1;
```

```java
x = x - 1;
```

```java
int x = 0; int z = ++x;
```

```java
int x = 0; int z = x++;
```

## Trips through a loop <!--p153-->

```java
for (int i = 0; i < 8; i++) {
System.out.println(i);
}
System.out.println("done");
```

```java
%java Test
done
```

```java
int i = 0;
while (i < 8) {
System.out.println(i);
i++;
}
System.out.println("done");
```

iteration of the loop, this variable will hold a different element from the collection. The type of this variable must be compatible with the elements in the array! For example, you can’t declare an int iteration variable to use with a String[] array. Part Two: the actual collection This must be a reference to an array or other collection. Again, don’t worry about the other non-array kinds of collections yet—you’ll see them in the next chapter.

## The enhanced for loop <!--p154-->

collections (you’ll learn about other collections in the next chapter). That’s really all that the enhanced for gives you—a simpler way to walk through all the elements in the collection. We’ll see the enhanced for loop in the next chapter too, when we talk about collections that aren’t arrays. The code to repeat goes here (the body). enhanced for The collection of elements that you want to iterate over.

```java
long y = 42;
int x = y; // won’t compile
```

In Chapter 3, Know Your Variables, we talked about the sizes of the various primitives and how you can’t shove a big thing directly into a small thing: A long is bigger than an int, and the compiler can’t be sure where that long has been. It might have been out partying with the other longs, and taking on really big values. To force the compiler to jam the value of a bigger primitive variable into a smaller one, you can use the cast operator. It looks like this:

```java
long y = 42; // so far so good
int x = (int) y; // x = 42 cool!
```

```java
long y = 40002; // 40002 exceeds the 16-bit limit of a short
short x = (short) y; // x now equals -25534!
```

Putting in the cast tells the compiler to take the value of y, chop it down to int size, and set x equal to whatever is left. If the value of y was bigger than the maximum value of x, then what’s left will be a weird (but calculable*) number: Still, the point is that the compiler lets you do it. And let’s say you have a floating-point number and you just want to get at the whole number (int) part of it:

```java
float f = 3.14f;
int x = (int) f; // x will equal 3
```

## Casting primitives <!--p155-->

```java
class Output {
public static void main(String[] args) {
Output output = new Output();
output.go();
}
void go() {
int value = 7;
for (int i = 1; i < 8; i++) {
value++;
if (i > 4) {
System.out.print(++value + " ");
}
if (value > 14) {
System.out.println(" i = " + i);
break;
}
}
}
}
```

```java
% java TestArrays
island = Fiji
island = Cozumel
island = Bermuda
island = Azores
```

```java
% java Output
13 15 x = 6
```

```java
% java Output
12 14
```

```java
% java Output
12 14 x = 6
```

we had to cast the result to an int. Casting one numeric type to another can change the value itself. It's important to understand the rules so you’re not surprised by this. and determine what would be the output when the program runs. File Edit Window Help Sleep File Edit Window Help Believe File Edit Window Help OM File Edit Window Help Incense -or- -or- Answers on page 122. writing a program A working Java program is all scrambled up on the fridge. Can you reconstruct the code snippets to make a working Java program that produces the output listed below? Some of the curly braces fell on the floor and they were too small to pick up, so feel free to add as many of those as you need!

```java
i++;
public static void main(String[] args) {
System.out.println(i + " " + j);
```

```java
% java MultiFor
0 4
0 3
1 4
1 3
3 4
3 3
class MultiFor {
for(int j = 4; j > 2; j--) {
if (i == 1) {
for(int i = 0; i < 4; i++) {
```

```java
public static void main(String[] args) {
int x = 0;
int y = 30;
for (int outer = 0; outer < 3; outer++) {
for (int inner = 4; inner > 1; inner--) {
y = y - 2;
if (x == 6) {
break;
}
x = x + 3;
}
y = y - 2;
}
System.out.println(x + " " + y);
}
```

```java
x = x + 3;
x = x + 6;
x = x + 2;
x++;
x--;
x = x + 0;
45 6
36 6
54 6
60 10
18 6
6 14
12 14
```

```java
class MultiFor {
public static void main(String[] args) {
for (int i = 0; i < 4; i++) {
for (int j = 4; j > 2; j--) {
System.out.println(i + " " + j);
}
if (i == 1) {
i++;
}
}
}
}
class Output {
public static void main(String[] args) {
Output output = new Output();
output.go();
}
void go() {
int value = 7;
for (int i = 1; i < 8; i++) {
value++;
if (i > 4) {
System.out.print(++value + " ");
}
if (value > 14) {
System.out.println(" i = " + i);
break;
}
}
}
}
```

```java
% java TestArrays
island = Fiji
island = Cozumel
island = Bermuda
island = Azores
```

```java
% java Output
13 15 x = 6
% java MultiFor
0 4
0 3
1 4
1 3
3 4
3 3
```

```java
x = x + 3;
x = x + 6;
x = x + 2;
x++;
x--;
x = x + 0;
45 6
36 6
54 6
60 10
18 6
6 14
12 14
```