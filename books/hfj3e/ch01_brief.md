# Chapter 1: Chapter 1: Breaking the Surface

pages 39-64

version 1.02, Java seduced programmers with its friendly syntax, object-oriented features, memory management, and best of all­—the promise of portability. The lure of write-once/run-anywhere is just too strong. A devoted following exploded, as programmers fought against bugs, limita­ tions, and, oh yeah, the fact that it was dog slow. But that was ages ago. If you’re just starting in Java, you’re lucky. Some of us had to walk five miles in the snow, uphill both ways (barefoot), to

get even the most trivial application to work. But you, why, you get to ride the sleeker, faster, easier-to-read-and-write Java of today. B r ea k ng t h e S u r fa c e Come on, the water’s great! We’ll dive right in and write some code, then compile and run it. We’re talking syntax, looping and branching, and a look at what makes Java so cool. You’ll be coding in no time.

## The way Java works <!--p40-->

## What you’ll do in Java <!--p41-->

## A very brief history of Java <!--p42-->

Java was initially released (some would say “escaped”), on January 23, 1996. It’s over 25 years old! In the first 25 years, Java as a language evolved, and the Java API grew enormously. The best estimate we have is that over 17 gazillion lines of Java code have been written in the last 25 years. As you spend time programming in Java, you will most certainly come across Java code that’s quite old, and some that’s much newer. Java is famous for its backward compatibility, so old code can run quite happily on new JVMs.

In this book we’ll generally start off by using older coding styles (remember, you’re likely to encounter such code in the “real world”), and then we’ll introduce newer-style code. In a similar fashion, we will sometimes show you older classes in the Java API, and then show you newer alternatives. I’ve heard that Java isn’t very fast compared to compiled languages like C and Rust. Speed and memory usage

```java
int size = 27;
String name = "Fido";
Dog myDog = new Dog(name, size);
x = size - 5;
if (x < 15) myDog.bark(8);
while (x > 3) {
myDog.play();
}
int[] numList = {2, 4, 6, 8};
System.out.print("Hello");
System.out.print("Dog: " + name);
String num = "8";
int z = Integer.parseInt(num);
try {
readTheFile("myFile.txt");
}
catch (FileNotFoundException ex) {
System.out.print("File not found.");
}
```

```java
int size = 27;
String name = "Fido";
Dog myDog = new Dog(name, size);
x = size - 5;
if (x < 15) myDog.bark(8);
while (x > 3) {
myDog.play();
}
int[] numList = {2, 4, 6, 8};
System.out.print("Hello");
System.out.print("Dog: " + name);
String num = "8";
int z = Integer.parseInt(num);
try {
readTheFile("myFile.txt");
}
catch (FileNotFoundException ex) {
System.out.print("File not found.");
}
```

```java
public class Dog {
}
```

```java
public class Dog {
void bark() {
}
}
```

```java
public class Dog {
void bark() {
statement1;
statement2;
}
}
```

## Code structure in Java <!--p45-->

```java
public class MyFirstApp {
public static void main (String[] args) {
System.out.print("I Rule!");
```

## Anatomy of a class <!--p46-->

```java
public static void main (String[] args) {
// your code goes here
}
```

```java
}
```

## Writing a class with a main() <!--p47-->

```java
public class MyFirstApp {
public static void main (String[] args) {
System.out.println("I Rule!");
System.out.println("The World");
}
}
public class MyFirstApp {
public static void main (String[] args) {
System.out.print("I Rule!");
System.out.println("The World");
}
}
```

```java
Compiled from "MyFirstApp.java"
public class ch1.MyFirstApp {
public ch1.MyFirstApp();
Code:
0: aload_0
1: invokespecial #1
// Method java/lang/Object."<init>":()V
4: return
public static void main(java.lang.
String[]);
```

```java
%java MyFirstApp
I Rule!
The World
```

```java
javac MyFirstApp.java
```

```java
java MyFirstApp
```

```java
MyFirstApp.java
```

```java
int x = 3;
String name = "Dirk";
x = x * 17;
System.out.print("x is " + x);
double d = Math.random();
// this is a comment
```

```java
while (x > 12) {
x = x - 1;
}
for (int i = 0; i < 10; i = i + 1) {
System.out.print("i is now " + i);
}
```

```java
if (x == 10) {
System.out.print("x must be 10");
} else {
System.out.print("x isn't 10");
}
if ((x < 3) && (name.equals("Dirk"))) {
System.out.println("Gently");
}
System.out.print("this line runs no matter what");
```

```java
x = 22;
```

```java
x = 3 ;
```

```java
int weight;
```

```java
public void go() {
// amazing code here
}
```

## Looping and looping and... <!--p51-->

```java
int x = 4; // assign 4 to x
while (x > 3) {
// loop code will run because
// x is greater than 3
x = x - 1; // or we’d loop forever
}
int z = 27; //
while (z == 17) {
// loop code will not run because
// z is not equal to 17
}
```

```java
public class Loopy {
public static void main(String[] args) {
int x = 1;
System.out.println("Before the Loop");
while (x < 4) {
System.out.println("In the loop");
System.out.println("Value of x is " + x);
x = x + 1;
}
System.out.println("This is after the loop");
}
}
% java Loopy
Before the Loop
In the loop
Value of x is 1
In the loop
Value of x is 2
In the loop
Value of x is 3
This is after the loop
```

```java
int x = 1;
```

```java
boolean isHot = true;
while(isHot) { }
```

## Conditional branching <!--p53-->

```java
class IfTest {
public static void main (String[] args) {
int x = 3;
if (x == 3) {
System.out.println("x must be 3");
}
System.out.println("This runs no matter what");
}
}
% java IfTest
x must be 3
This runs no matter what
```

```java
class IfTest2 {
public static void main(String[] args) {
int x = 2;
if (x == 3) {
System.out.println("x must be 3");
} else {
System.out.println("x is NOT 3");
}
System.out.println("This runs no matter what");
}
}
% java IfTest2
x is NOT 3
This runs no matter what
```

```java
% java DooBee
DooBeeDooBeeDo
```

```java
public class DooBee {
public static void main(String[] args) {
int x = 1;
while (x < _____ ) {
System.out._________("Doo");
System.out._________("Bee");
x = x + 1;
}
if (x == ______ ) {
System.out.print("Do");
}
}
}
```

```java
public class BottleSong {
public static void main(String[] args) {
int bottlesNum = 10;
String word = "bottles";
while (bottlesNum > 0) {
if (bottlesNum == 1) {
word = "bottle"; // singular, as in ONE bottle.
}
System.out.println(bottlesNum + " green " + word + ", hanging on the wall");
System.out.println(bottlesNum + " green " + word + ", hanging on the wall");
System.out.println("And if one green bottle should accidentally fall,");
bottlesNum = bottlesNum - 1;
if (bottlesNum > 0) {
System.out.println("There'll be " + bottlesNum +
" green " + word + ", hanging on the wall");
} else {
System.out.println("There'll be no green bottles, hanging on the wall");
} // end else
} // end while loop
} // end main method
} // end class
```

```java
public class PhraseOMatic {
public static void main (String[] args) {
String[] wordListOne = {"agnostic", "opinionated",
"voice activated", "haptically driven", "extensible",
"reactive", "agent based", "functional", "AI enabled",
"strongly typed"};
String[] wordListTwo = {"loosely coupled", "six sigma",
"asynchronous", "event driven", "pub-sub", "IoT", "cloud
native", "service oriented", "containerized", "serverless",
"microservices", "distributed ledger"};
String[] wordListThree = {"framework", "library",
"DSL", "REST API", "repository", "pipeline", "service
mesh", "architecture", "perspective", "design",
"orientation"};
int oneLength = wordListOne.length;
int twoLength = wordListTwo.length;
int threeLength = wordListThree.length;
java.util.Random randomGenerator = new java.util.Random();
int rand1 = randomGenerator.nextInt(oneLength);
int rand2 = randomGenerator.nextInt(twoLength);
int rand3 = randomGenerator.nextInt(threeLength);
String phrase = wordListOne[rand1] + " " +
wordListTwo[rand2] + " " + wordListThree[rand3];
System.out.println("What we need is a " + phrase);
}
}
```

## Phrase-O-Matic <!--p57-->

In a nutshell, the program makes three lists of words, then randomly picks one word from each of the three lists, and prints out the result. Don’t worry if you don’t understand exactly what’s happening in each line. For goodness sake, you’ve got the whole book ahead of you, so relax. This is just a quick look from a 30,000-foot outside-the-box targeted leveraged paradigm. 1. The first step is to create three String arrays—the containers that will hold all the words. Declaring and creating an array is easy; here’s a small one:

2. For each of the three lists (arrays), the goal is to pick a random word, so we have to know how many words are in each list. If there are 14 words in a list, then we need a random num­ ber between 0 and 13 (Java arrays are zero-based, so the first word is at position 0, the second word position 1, and the last word is position 13 in a 14-element array). Quite handily, a Java array is more than happy to tell you its length. You just have to ask. In the pets array, we’d say:

random numbers, including java.util.Random (we will see later why this class name is prefixed with java.util). The nextInt() method returns a random number between 0 and some-num­ ber-we-give-it, not including the number that we give it. So we’ll give it the number of elements (the array length) in the list we’re using. Then we assign each result to a new variable. We could just as easily have asked for a random number between 0 and 5, not including 5:

```java
String s = pets[0]; // s is now the String "Fido"
s = s + " " + "is a dog"; // s is now "Fido is a dog"
```

which concatenates (we prefer the more technical smooshes) the String objects together. To get an element from an array, you give the array the index number (position) of the thing you want by using: what we need here is a... extensible microser­ vices pipeline opinionated loosely coupled REST API agent-based microservices library AI-enabled service oriented orientation agnostic pub-sub DSL functional IoT perspective

```java
if (x == 1) {
System.out.print("d");
x = x - 1;
}
if (x == 2) {
System.out.print("b c");
}
if (x > 2) {
System.out.print("a");
}
int x = 3;
x = x - 1;
System.out.print("-");
while (x > 0) {
class Shuff le1 {
public static void main(String [] args) {
% java Shuffle1
a-b c-d
```

```java
class Exercise1c {
int x = 5;
while (x > 1) {
x = x - 1;
if (x < 3) {
System.out.println("small x");
}
}
}
```

```java
class Exercise1a {
public static void main(String[] args) {
int x = 1;
while (x < 10) {
if (x > 3) {
System.out.println("big x");
}
}
}
}
```

```java
public static void main(String [] args) {
int x = 5;
while ( x > 1 ) {
x = x - 1;
if ( x < 3) {
System.out.println("small x");
}
}
}
```

```java
class Test {
public static void main(String [] args) {
int x = 0;
int y = 0;
while (x < 5) {
System.out.print(x + "" + y +" ");
x = x + 1;
}
}
}
y = x - y;
y = y + x;
y = y + 2;
if( y > 4 ) {
y = y - 1;
}
x = x + 1;
y = y + x;
if ( y < 5 ) {
x = x + 1;
if ( y < 3 ) {
x = x - 1;
}
}
y = y + 2;
22 46
11 34 59
02 14 26 38
02 14 36 48
00 11 21 32 42
11 21 32 42 53
00 11 23 36 410
02 14 25 36 47
```

```java
class PoolPuzzleOne {
public static void main(String [] args) {
int x = 0;
while ( __________ ) {
_____________________________
if ( x < 1 ) {
___________________________
}
_____________________________
if ( __________ ) {
____________________________
___________
}
if ( x == 1 ) {
____________________________
}
if ( ___________ ) {
____________________________
}
System.out.println();
____________
}
}
}
```

```java
a noise
annoys
an oyster
```

```java
% java Shuffle1
a-b c-d
class Shuffle1 {
public static void main(String[] args) {
int x = 3;
while (x > 0) {
if (x > 2) {
System.out.print("a");
}
x = x - 1;
System.out.print("-");
if (x == 2) {
System.out.print("b c");
}
if (x == 1) {
System.out.print("d");
x = x - 1;
}
}
}
}
class Exercise1a {
public static void main(String [] args) {
int x = 1;
while ( x < 10 ) {
```

```java
if ( x > 3) {
System.out.println("big x");
}
}
```

```java
public static void main(String [] args) {
int x = 5;
while ( x > 1 ) {
x = x - 1;
if ( x < 3) {
System.out.println("small x");
}
```

```java
class Exercise1c {
```

```java
int x = 5;
while ( x > 1 ) {
x = x - 1;
if ( x < 3) {
System.out.println("small x");
}
}
```

```java
}
```

```java
public class DooBee {
public static void main(String[] args) {
int x = 1;
while (x < 3) {
System.out.print("Doo");
System.out.print("Bee");
x = x + 1;
}
if (x == 3) {
System.out.print("Do");
}
}
}
```

```java
class PoolPuzzleOne {
public static void main(String [] args) {
int x = 0;
```

```java
}
}
}
```

```java
a noise
annoys
an oyster
class Test {
public static void main(String [] args) {
int x = 0;
int y = 0;
while ( x < 5 ) {
System.out.print(x + "" + y +" ");
x = x + 1;
}
}
}
y = x - y;
y = y + x;
y = y + 2;
if( y > 4 ) {
y = y - 1;
}
x = x + 1;
y = y + x;
if ( y < 5 ) {
x = x + 1;
if ( y < 3 ) {
x = x - 1;
}
}
y = y + 2;
22 46
11 34 59
02 14 26 38
02 14 36 48
00 11 21 32 42
11 21 32 42 53
00 11 23 36 410
02 14 25 36 47
```