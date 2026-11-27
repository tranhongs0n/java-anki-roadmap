# Chapter 10: Chapter 10: Numbers Matter

pages 313-346

arithmetic. You might want to get the absolute value of a number, or round a number, or find the larger of two numbers. You might want your numbers to print with exactly two decimal places, or you might want to put commas into your large numbers to make them easier to read. And what about parsing a String into a number? Or turning a number into a String? Someday you’re gonna want to put a bunch of numbers into a collection like ArrayList that takes only

objects. You’re in luck. Java and the Java API are full of handy number-tweaking capabilities and methods, ready and easy to use. But most of them are static, so we’ll start by learning what it means for a variable or method to be static, including constants in Java, also known as static final variables.

## Math methods

```java
TestMath.java:3: Math() has private
access in java.lang.Math
Math mathObject = new Math();
^
1 error
Math mathObject = new Math();
```

```java
long x = Math.round(42.2);
int y = Math.min(56, 12);
int z = Math.abs(-343);
```

```java
s2.play();
s3.play();
```

```java
public class Song {
String title;
public Song(String t) {
title = t;
}
public void play() {
SoundPlayer player = new SoundPlayer();
player.playSound(title);
}
}
public static int min(int a, int b) {
//returns the smallest of a and b
}
```

```java
Math.min(42,36);
```

```java
Math.min(88,86);
```

```java
Song t2 = new Song();
t2.play();
```

```java
public class Duck {
private int size;
public static void main(String[] args) {
System.out.println("Size of duck is " + size);
}
public void setSize(int s) {
size = s;
}
public int getSize() {
return size;
}
}
```

```java
% javac Duck.java
Duck.java:6: non-static variable
size cannot be referenced from a
static context
System.out.println("Size
of duck is " + size);
^
```

```java
public class Duck {
private int size;
public static void main(String[] args) {
System.out.println("Size is " + getSize());
}
public void setSize(int s) {
size = s;
}
public int getSize() {
return size;
}
}
```

```java
% javac Duck.java
Duck.java:5: error: non-static
method getSize() cannot be refer­
enced from a static context
System.out.println("Size is " +
getSize());
^
1 error
```

```java
Duck d = new Duck();
String[] s = {};
d.main(s);
```

```java
DateFormat.getDateTimeInstance();
DateFormat.getTimeInstance();
NumberFormat.getPercentInstance();
```

```java
class Duck {
int duckCount = 0;
public Duck() {
duckCount++;
}
}
```

```java
public class Duck {
private int size;
private static int duckCount = 0;
public Duck() {
duckCount++;
}
public void setSize(int s) {
size = s;
}
public int getSize() {
return size;
}
}
```

## Initializing a static variable

```java
class Player {
static int playerCount = 0;
private String name;
public Player(String n) {
name = n;
playerCount++;
}
}
public class PlayerTestDrive {
public static void main(String[] args) {
System.out.println(Player.playerCount);
Player one = new Player("Tiger Woods");
System.out.println(Player.playerCount);
}
}
```

```java
% java PlayerTestDrive
```

## static final variables are constants

```java
public static final double PI = 3.141592653589793;
```

```java
public class ConstantInit2 {
public static final int X_VALUE = 25;
}
```

```java
public class ConstantInit3 {
public static final double VAL;
static {
VAL = Math.random();
}
}
```

```java
class ConstantInit1 {
final static int X;
static {
X = 42;
}
}
```

```java
% javac ConstantInit3.java
ConstantInit3.java:2: error: vari­
able VAL not initialized in the
default constructor
public static final double VAL;
^
1 error
public class ConstantInit3 {
public static final double VAL;
}
```

```java
class Foof {
final int size = 3;
final int whuffie;
Foof() {
whuffie = 42;
}
void doStuff(final int x) {
// you can’t change x
}
void doMore() {
final int z = 7;
// you can’t change z
}
}
```

```java
class Poof {
final void calcWhuffie() {
// important things
// that must never be overridden
}
}
```

```java
final class MyMostPerfectClass {
// cannot be extended
}
```

```java
public class Foo {
static int x;
public void go() {
System.out.println(x);
}
}
public class Foo2 {
int x;
public static void go() {
System.out.println(x);
}
}
public class Foo3 {
final int x;
public void go() {
System.out.println(x);
}
}
public class Foo4 {
static final int x = 12;
public void go() {
System.out.println(x);
}
}
public class Foo5 {
static final int x = 12;
public void go(final int x) {
System.out.println(x);
}
}
public class Foo6 {
int x = 12;
public static void go(final int x) {
System.out.println(x);
}
}
```

## Math methods

```java
double r1 = Math.random();
int r2 = (int) (Math.random() * 5);
```

```java
int x = Math.abs(-240); // returns 240
double d = Math.abs(240.45); // returns 240.45
```

## Math methods

```java
int x = Math.round(-24.8f); // returns -25
int y = Math.round(24.45f); // returns 24
long z = Math.round(24.45); // returns 24L
```

```java
int x = Math.min(24,240); // returns 24
double y = Math.min(90876.5, 90876.49); // returns 90876.49
```

```java
int x = Math.max(24,240); // returns 240
double y = Math.max(90876.5, 90876.49); // returns 90876.5
```

```java
double x = Math.sqrt(9); //return 3
double y = Math.sqrt(42.0); // returns 6.48074069840786
```

## Wrapping a primitive

```java
int i = 288;
Integer iWrap = new Integer(i);
```

```java
int unWrapped = iWrap.intValue();
```

```java
ArrayList<???> list;
```

```java
public void autoboxing() {
int x = 32;
ArrayList<Integer> list = new ArrayList<Integer>();
list.add(x);
int num = list.get(0);
}
```

A: Because...you can’t. At least, not in the versions of Java this book covers (the language is constantly evolving and things may change!). Remember, the rule for generic types is that you can specify only class or interface types, not primitives. So ArrayList<int> will not com­ pile. But as you can see from the code above, it doesn’t really matter, since the compiler lets you put ints into the ArrayList<Integer>. In fact, there’s really no way to prevent you from putting primitives into an ArrayList where the type of the list is the type of that primitive’s wrapper, since autoboxing will happen automatically. So, you can put boolean primitives in an ArrayList<Boolean> and chars into an ArrayList<Character>.

## Java will Autobox primitives for you

```java
void takeNumber(Integer i) { }
```

```java
int giveNumber() {
return x;
}
```

```java
if (bool) {
System.out.println("true");
}
```

```java
true
```

```java
true
```

## Autoboxing works almost everywhere

```java
i++;
```

```java
Integer intVal = x;
```

```java
public class TestBox {
private Integer i;
private int j;
public static void main(String[] args) {
TestBox t = new TestBox();
t.go();
}
public void go() {
j = i;
System.out.println(j);
System.out.println(i);
}
}
```

```java
String s = "2";
int x = Integer.parseInt(s);
double d = Double.parseDouble("420.24");
boolean b = Boolean.parseBoolean("True");
```

```java
% java Wrappers
Exception in thread "main" java.lang.NumberFormatException:
For input string: "two"
at java.base/java.lang.NumberFormatException.forInputStri
ng(NumberFormatException.java:65)
at java.base/java.lang.Integer.parseInt(Integer.java:652)
at java.base/java.lang.Integer.parseInt(Integer.java:770)
at Snippets.badParse(Snippets.java:48)
at Snippets.main(Snippets.java:54)
String t = "two";
int y = Integer.parseInt(t);
```

```java
double d = 42.5;
String doubleString = "" + d;
double d = 42.5;
String doubleString = Double.toString(d);
double d = 42.5;
String doubleString = String.valueOf(d);
```

## Number formatting

In Java, formatting numbers and dates doesn’t have to be coupled with I/O. Think about it. One of the most typical ways to display numbers to a user is through a GUI. You put Strings into a scrolling text area, or maybe a table. If formatting was built only into print statements, you’d never be able to format a number into a nice String to display in a GUI. The Java API provides powerful and flexible formatting using the Formatter class in java.util. But often you don’t need to create and call methods on the Formatter class yourself, because the Java API has convenience methods in some of the I/O classes (including printf()) and the String class. So it can be a simple matter of calling a static String.format() method and passing it the thing you want formatted along with formatting instructions.

a little effort unless you’re familiar with the printf() function in C/C++. Fortunately, even if you don’t know printf(), you can simply follow recipes for the most basic things (that we’re showing in this chapter). But you will want to learn how to format if you want to mix and match to get anything you want. We’ll start here with a basic example and then look at how it works. (Note: we’ll revisit formatting again in Chapter 16, Saving Objects.)

```java
public class TestFormats {
public static void main(String[] args) {
long myBillion = 1_000_000_000;
String s = String.format("%,d", myBillion);
System.out.println(s);
}
}
```

```java
1,000,000,000
```

## number formatting

```java
long hardToRead = 1000000000;
long easierToRead = 1_000_000_000;
long legalButSilly = 10_0000_0000;
```

Before we get into formatting numbers, let’s take a small, useful detour. Sometimes you’ll want to declare variables with large initial values. Let’s look at three declarations that assign the same large value, a billion, to long primitives: When you’re assigning large values, properly located underscores will make your life easier! numbers and statics

## Formatting deconstructed...

```java
format("%,d", 1_000_000_000);
```

## The percent (%) says, “insert argument here”

```java
String.format("I have %.2f, bugs to fix.", 476578.09876);
```

```java
I have 476578.10 bugs to fix.
```

```java
String.format("I have %,.2f bugs to fix.", 476578.09876);
I have 476,578.10 bugs to fix.
```

```java
String.format("I have %.2f, bugs to fix.", 476578.09876);
```

## The format specifier

```java
%[argument number][flags][width][.precision]type
```

```java
%[argument number][flags][width][.precision]type
format("%,6.1f", 42.000);
```

## The only required specifier is for TYPE

```java
format("%d", 42);
```

```java
format("%.3f", 42.000000)
42.000
```

```java
format("%x", 42)
2a
```

```java
format("%c", 42)
*
```

## What happens if I have more than one argument?

after the format String (first argument), so that means your call to format() will have three arguments instead of two. And inside that first argument (the format String), you’ll have two different format specifiers (two things that start with “%”). The first format specifier will insert the second argument to the method, and the second format specifier will insert the third argument to the method. In other words, the variable insertions in the format String use the order in which the other arguments are passed into the format() method.

```java
int one = 20456654;
double two = 100567890.248907;
String s = String.format("The rank is %,d out of %,.2f", one, two);
```

```java
The rank is 20,456,654 out of 100,567,890.25
```

formatting specifiers to the same argument. That’s probably hard to imagine until you see how date formatting (as opposed to the number formatting we’ve been doing) works. Just know that in a minute, you’ll see how to be more specific about which format specifiers are applied to which arguments. We added commas to both variables and restricted the floating-point number (the second variable) to two decimal places.

pass? I mean, how many overloaded format() methods are IN the String class? So, what happens if I want to pass, say, ten different arguments to be formatted for a single output String? A: Good catch. Yes, there is something strange going on, and no there are not a bunch of overloaded format() methods to take a different number of possible arguments. In order to support this formatting (printf-like) API in Java, the language needed another feature—variable argument lists (called varargs for short). We’ll talk about varargs more in Appendix B.

## Just one more thing...static imports

```java
class NoStatic {
public static void main(String[] args) {
System.out.println("sqrt " + Math.sqrt(2.0));
System.out.println("tan " + Math.tan(60));
}
}
```

```java
import static java.lang.Math.*;
import static java.lang.System.out;
class WithStatic {
public static void main(String[] args) {
out.println("sqrt " + sqrt(2.0));
out.println("tan " + tan(60));
}
}
```

```java
class StaticSuper {
static {
System.out.println("super static block");
}
StaticSuper () {
System.out.println("super constructor");
}
}
public class StaticTests extends StaticSuper {
static int rand;
static {
rand = (int) (Math.random() * 6);
System.out.println("static block " + rand);
}
StaticTests() {
System.out.println("constructor");
}
public static void main(String[] args) {
System.out.println("in main");
StaticTests st = new StaticTests();
}
}
```

```java
static block 4
in main
super static block
super constructor
constructor
```

```java
super static block
static block 3
in main
super constructor
constructor
```

```java
System.out.println(
"super constructor");
}
```

```java
super static block
static block 3
in main
super constructor
constructor
```