# Chapter 2: Chapter 2: A Trip to Objectville

pages 65-86

the main() method. That’s not exactly object-oriented. In fact, that’s not object-oriented at all. Well, we did use a few objects, like the String arrays for the Phrase-O-Matic, but we didn’t actually develop any of our own object types. So now we’ve got to leave that procedural world behind, get the heck out of main(), and start making some objects of our own. We’ll look at what makes object-oriented (OO) development in Java so much fun. We’ll look at the difference

between a class and an object. We’ll look at how objects can give you a better life (at least the programming part of your life. Not much we can do about your fashion sense). Warning: once you get to Objectville, you might never go back. Send us a postcard. A Trip to Objectville We’re going to Objectville! We’re leaving this dusty ol’ procedural town for good. I’ll send you a postcard. once upon a time in Objectville

```java
rotate(shapeNum) {
// make the shape rotate 360º
}
playSound(shapeNum) {
// use shapeNum to lookup which
// AIF sound to play, and play it
}
```

“OK, technically you were first, Laura,” said the Manager, “but we have to add just one tiny thing to the program. It’ll be no problem for crack programmers like you two.” “If I had a dime for every time I’ve heard that one,” thought Laura, knowing that spec-change-no- problem was a fantasy. “And yet Brad looks strangely serene. What’s up with that?” Still, Laura held tight to her core belief that the OO way, while cute, was just slow. And that if you wanted to change her mind, you’d have to pry it from her cold, dead, carpal-tunnelled hands.

```java
playSound(shapeNum) {
// if the shape is not an amoeba,
// use shapeNum to lookup which
// AIF sound to play, and play it
// else
// play amoeba .mp3 sound
}
```

(Hah! So much for that foofy OO nonsense.) But the smirk on Laura’s face melted when the Really Annoying Project Manager said (with that tone of disappointment), “Oh, no, that’s not how the amoeba is supposed to rotate...” Turns out, both programmers had written their rotate code like this: 1. determine the rectangle that surrounds the shape. 2. calculate the center of that rectangle, and rotate the shape around that point. But the amoeba shape was supposed to rotate around a point on one end, like a clock hand.

“I’m toast,” thought Laura, visualizing charred Wonderbread™. “Although, hmmmm. I could just add another if/else to the rotate procedure and then just hard-code the rotation point code for the amoeba. That probably won’t break anything.” But the little voice at the back of her head said, “Big Mistake. Do you honestly think the spec won’t change again?” Laura delivered just moments ahead of Brad Back at Laura’s desk

```java
rotate(shapeNum, xPt, yPt) {
// if the shape is not an amoeba,
// calculate the center point
// based on a rectangle,
// then rotate
// else
// use the xPt and yPt as
// the rotation point offset
// and then rotate
}
```

```java
class DogTestDrive {
public static void main(String[] args) {
Dog d = new Dog();
d.size = 40;
d.bark();
}
}
```

```java
class Dog {
int size;
String breed;
String name;
void bark() {
System.out.println("Ruff! Ruff!");
}
}
```

## Making your first object <!--p74-->

```java
class DogTestDrive {
public static void main(String[] args) {
// Dog test code goes here
}
}
```

```java
class Movie {
String title;
String genre;
int rating;
void playIt() {
System.out.println("Playing the movie");
}
}
public class MovieTestDrive {
public static void main(String[] args) {
Movie one = new Movie();
one.title = "Gone with the Stock";
one.genre = "Tragic";
one.rating = -2;
Movie two = new Movie();
two.title = "Lost in Cubicle Space";
two.genre = "Comedy";
two.rating = 5;
two.playIt();
Movie three = new Movie();
three.title = "Byte Club";
three.genre = "Tragic but ultimately uplifting";
three.rating = 127;
}
}
```

## Making and testing Movie objects <!--p75-->

## Quick! Get out of main! <!--p76-->

As long as you’re in main(), you’re not really in Objectville. It’s fine for a test program to run within the main method, but in a true OO application, you need objects talk­ ing to other objects, as opposed to a static main() method creating and testing objects. The two uses of main:  to test your real class  to launch/start your Java application A real Java application is nothing but objects talking to other objects. In this case, talking means objects calling methods on one another. On the previous page, and in Chapter 4, How Objects Behave, we look at using a main() method from a separate TestDrive class to create and test the methods and variables of another class. In Chapter 6, Using the Java Library, we look at using a class with a main() method to start the ball rolling on a real Java application (by making objects and then turning those objects loose to interact with other objects, etc.)

ing with a small toolkit, so you’ll find this program a little clunky and inefficient. You might want to think about what you could do to improve it, and in later chapters that’s exactly what we’ll do. Don’t worry if some of the code is confusing; the key point of this example is that objects talk to objects. The Guessing Game Summary: The Guessing Game involves a game object and three player objects. The game gen­ erates a random number between 0 and 9, and the three player objects try to guess it. (We didn’t say it was a really exciting game.)

```java
GuessGame.class Player.class GameLauncher.class
```

```java
public class GuessGame {
Player p1;
Player p2;
Player p3;
public void startGame() {
p1 = new Player();
p2 = new Player();
p3 = new Player();
int guessp1 = 0;
int guessp2 = 0;
int guessp3 = 0;
boolean p1isRight = false;
boolean p2isRight = false;
boolean p3isRight = false;
int targetNumber = (int) (Math.random() * 10);
System.out.println("I'm thinking of a number between 0 and 9...");
while (true) {
System.out.println("Number to guess is " + targetNumber);
p1.guess();
p2.guess();
p3.guess();
guessp1 = p1.number;
System.out.println("Player one guessed " + guessp1);
guessp2 = p2.number;
System.out.println("Player two guessed " + guessp2);
guessp3 = p3.number;
System.out.println("Player three guessed " + guessp3);
if (guessp1 == targetNumber) {
p1isRight = true;
}
if (guessp2 == targetNumber) {
p2isRight = true;
}
if (guessp3 == targetNumber) {
p3isRight = true;
}
if (p1isRight || p2isRight || p3isRight) {
System.out.println("We have a winner!");
System.out.println("Player one got it right? " + p1isRight);
System.out.println("Player two got it right? " + p2isRight);
System.out.println("Player three got it right? " + p3isRight);
System.out.println("Game is over.");
break; // game over, so break out of the loop
} else {
// we must keep going because nobody got it right!
System.out.println("Players will have to try again.");
} // end if/else
} // end loop
} // end method
} // end class
```

```java
I’m thinking of a number between 0 and 9...
Number to guess is 7
I’m guessing 1
I’m guessing 9
I’m guessing 9
Player one guessed 1
Player two guessed 9
Player three guessed 9
Players will have to try again.
Number to guess is 7
I’m guessing 3
I’m guessing 0
I’m guessing 9
Player one guessed 3
Player two guessed 0
Player three guessed 9
Players will have to try again.
Number to guess is 7
I’m guessing 7
I’m guessing 5
I’m guessing 0
Player one guessed 7
Player two guessed 5
Player three guessed 0
We have a winner!
Player one got it right? true
Player two got it right? false
Player three got it right? false
Game is over.
```

## Running the Guessing Game <!--p78-->

```java
class StreamingSong {
String title;
String artist;
int duration;
void play() {
System.out.println("Playing song");
}
void printDetails() {
System.out.println("This is " + title +
" by " + artist);
}
}
class StreamingSongTestDrive {
public static void main(String[] args) {
song.artist = "The Beatles";
song.title = "Come Together";
song.play();
song.printDetails();
}
}
class Episode {
int seriesNumber;
int episodeNumber;
void skipIntro() {
System.out.println("Skipping intro...");
}
void skipToNext() {
System.out.println("Loading next episode...");
}
}
class EpisodeTestDrive {
public static void main(String[] args) {
Episode episode = new Episode();
episode.seriesNumber = 4;
episode.play();
episode.skipIntro();
}
}
```

```java
boolean topHat = true;
boolean snare = true;
void playSnare() {
System.out.println("bang bang ba-bang");
}
if (d.snare == true) {
d.playSnare();
}
d.snare = false;
class DrumKitTestDrive {
d.playTopHat();
public static void main(String [] args) {
```

```java
% java DrumKitTestDrive
bang bang ba-bang
ding ding da-ding
void playTopHat () {
System.out.println("ding ding da-ding");
}
class DrumKit {
DrumKit d = new DrumKit();
d.playSnare();
```

```java
public class EchoTestDrive {
public static void main(String []
args) {
Echo e1 = new Echo();
_________________________
int x = 0;
while ( ___________ ) {
e1.hello();
__________________________
if ( ____________ ) {
e2.count = e2.count + 1;
}
if ( ____________ ) {
e2.count = e2.count + e1.count;
}
x = x + 1;
}
System.out.println(e2.count);
}
}
```

```java
helloooo...
helloooo...
helloooo...
helloooo...
```

```java
class ____________ {
int _________ = 0;
void ___________ {
System.out.println("helloooo... ");
}
}
```

```java
% java DrumKitTestDrive
bang bang ba-bang
ding ding da-ding
class DrumKit {
boolean topHat = true;
boolean snare = true;
void playTopHat() {
System.out.println("ding ding da-ding");
}
void playSnare() {
System.out.println("bang bang ba-bang");
}
}
class DrumKitTestDrive {
public static void main(String[] args) {
DrumKit d = new DrumKit();
d.playSnare();
d.snare = false;
d.playTopHat();
if (d.snare == true) {
d.playSnare();
}
}
}
class StreamingSong {
String title;
String artist;
int duration;
void play() {
System.out.println("Playing song");
}
void printDetails() {
System.out.println("This is " + title +
" by " + artist);
}
}
class StreamingSongTestDrive {
public static void main(String[] args) {
song.artist = "The Beatles";
song.title = "Come Together";
song.play();
song.printDetails();
}
}
class Episode {
int seriesNumber;
int episodeNumber;
```

```java
void skipIntro() {
System.out.println("Skipping intro...");
}
void skipToNext() {
System.out.println("Loading next episode...");
}
}
class EpisodeTestDrive {
public static void main(String[] args) {
Episode episode = new Episode();
episode.seriesNumber = 4;
episode.play();
episode.skipIntro();
}
}
```

```java
public class EchoTestDrive {
public static void main(String[]
args) {
Echo e1 = new Echo();
int x = 0;
e1.hello();
e2.count = e2.count + 1;
}
e2.count = e2.count + e1.count;
}
x = x + 1;
}
System.out.println(e2.count);
}
}
```

```java
System.out.println("helloooo... ");
}
}
```

```java
helloooo...
helloooo...
helloooo...
helloooo...
```