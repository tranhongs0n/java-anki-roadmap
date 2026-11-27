# Chapter 4: Chapter 4: How Objects Behave

pages 109-132

haven’t looked at how state and behavior are related. We already know that each instance of a class (each object of a particular type) can have its own unique values for its instance variables. Dog A can have a name “Fido” and a weight of 70 pounds. Dog B is “Killer” and weighs 9 pounds. And if the Dog class has a method makeNoise(), well, don’t you think a 70-pound dog barks a bit deeper than the little 9-pounder? (Assuming that annoying yippy sound can be considered

a bark.) Fortunately, that’s the whole point of an object—it has behavior that acts on its state. In other words, methods use instance variable values. Like, “if dog is less than 14 pounds, make yippy sound, else...” or “increase weight by 5.” Let’s go change some state. How Objects Behave objects have state and behavior A class is the blueprint for an object. When you write a class, you’re describing how the JVM should make an object of that type. You already know that every object of that type can have different instance variable values. But what about the methods?

```java
s1.play();
```

```java
s2.play();
```

```java
Song song1 = new Song();
song1.setArtist("Travis");
song1.setTitle("Sing");
Song song2 = new Song();
song2.setArtist("Sex Pistols");
song2.setTitle("My Way");
```

```java
void play() {
soundPlayer.playSound(title, artist);
}
```

```java
class Dog {
int size;
String name;
void bark() {
if (size > 60) {
System.out.println("Wooof! Wooof!");
} else if (size > 14) {
System.out.println("Ruff! Ruff!");
} else {
System.out.println("Yip! Yip!");
}
}
}
class DogTestDrive {
public static void main(String[] args) {
Dog one = new Dog();
one.size = 70;
Dog two = new Dog();
two.size = 8;
Dog three = new Dog();
three.size = 35;
one.bark();
two.bark();
three.bark();
}
}
```

## The size affects the bark <!--p111-->

```java
Wooof! Wooof!
Yip! Yip!
Ruff! Ruff!
```

## You can send things to a method <!--p112-->

```java
d.bark(3);
```

```java
void bark(int numOfBarks) {
while (numOfBarks > 0) {
System.out.println("ruff");
numOfBarks = numOfBarks - 1;
}
}
Dog d = new Dog();
```

```java
int giveSecret() {
return 42;
}
```

## You can get things back from a method <!--p113-->

```java
void go() {
}
```

```java
int giveSecret() {
return 42;
}
```

```java
void takeTwo(int x, int y) {
int z = x + y;
System.out.println("Total is " + z);
}
void go() {
TestStuff t = new TestStuff();
t.takeTwo(12, 34);
}
```

```java
void takeTwo(int x, int y) {
int z = x + y;
System.out.println("Total is " + z);
}
void go() {
int foo = 7;
int bar = 3;
t.takeTwo(foo, bar);
}
```

```java
int x = 7;
```

```java
foo.go(x);
void go(int z){ }
```

```java
void go(int z){
z = 0;
}
```

```java
class ElectricGuitar {
String brand;
int numOfPickups;
boolean rockStarUsesIt;
String getBrand() {
return brand;
}
void setBrand(String aBrand) {
brand = aBrand;
}
int getNumOfPickups() {
return numOfPickups;
}
void setNumOfPickups(int num) {
numOfPickups = num;
}
boolean getRockStarUsesIt() {
return rockStarUsesIt;
}
void setRockStarUsesIt(boolean yesOrNo) {
rockStarUsesIt = yesOrNo;
}
}
```

## Encapsulation <!--p118-->

```java
theCat.height = 27;
```

```java
theCat.height = 0;
```

```java
public void setHeight(int ht) {
if (ht > 9) {
height = ht;
}
}
```

Object: Is there any danger? Is there any danger? [starts laughing] Hey, did all you other instances hear that, “Is there any danger?” he asks? [falls on the floor laughing] HeadFirst: What’s funny about that? Seems like a reasonable question. Object: OK, I’ll explain it. It’s [bursts out laughing again, uncontrollably] HeadFirst: Can I get you anything? Water? Object: Whew! Oh boy. No I’m fine, really. I’ll be serious. Deep breath. OK, go on.

about their boundaries. Like, think of all the things that would break if negative numbers were allowed. Number of bathrooms in an office. Velocity of an airplane. Birthdays. Barbell weight. Phone numbers. Microwave oven power. HeadFirst: I see what you mean. So how does encapsulation let you set boundaries? Object: By forcing other code to go through setter methods. That way, the setter method can validate the parameter and decide if it’s doable. Maybe the method will reject it and do nothing, or maybe it’ll throw an Exception (like if it’s a null Social Security number for a credit card application), or maybe the method will round the parameter sent in to the nearest acceptable value. The point is, you can do whatever you want in the setter method, whereas you can’t do anything if your instance variables are public.

```java
class GoodDog {
private int size;
public int getSize() {
return size;
}
public void setSize(int s) {
size = s;
}
void bark() {
if (size > 60) {
System.out.println("Wooof! Wooof!");
} else if (size > 14) {
System.out.println("Ruff! Ruff!");
} else {
System.out.println("Yip! Yip!");
}
}
}
class GoodDogTestDrive {
public static void main(String[] args) {
GoodDog one = new GoodDog();
one.setSize(70);
GoodDog two = new GoodDog();
two.setSize(8);
System.out.println("Dog one: " + one.getSize());
System.out.println("Dog two: " + two.getSize());
one.bark();
two.bark();
}
}
```

```java
pets[0] = new Dog();
pets[1] = new Dog();
Dog[] pets;
pets = new Dog[7];
```

```java
pets[0].setSize(30);
int x = pets[0].getSize();
pets[1].setSize(8);
```

```java
int size;
String name;
```

```java
int size = 420;
String name = "Donny";
```

```java
class PoorDog {
private int size;
private String name;
public int getSize() {
return size;
}
public String getName() {
return name;
}
}
public class PoorDogTestDrive {
public static void main(String[] args) {
PoorDog one = new PoorDog();
System.out.println("Dog size is " + one.getSize());
System.out.println("Dog name is " + one.getName());
}
}
```

```java
Dog size is 0
Dog name is null
```

```java
class Horse {
private double height = 15.2;
private String breed;
// more code...
}
```

```java
class AddThing {
int a;
int b = 12;
public int add() {
int total = a + b;
return total;
}
}
```

```java
class Foo {
public void go() {
int x;
int z = x + 3;
}
}
```

```java
Foo.java:4: variable x might
not have been initialized
int z = x + 3;
1 error ^
```

we need to understand that the == operator is used only to compare the bits in two variables. What those bits represent doesn’t matter. The bits are either the same, or they’re not.

## Comparing variables (primitives or references) <!--p124-->

```java
int a = 3;
byte b = 3;
if (a == b) { // true }
```

if (a == b) {...} looks at the bits in a and b and returns true if the bit pattern is the same (although all the extra zeros on the left end don’t matter). To see if two references are the same (which means they refer to the same object on the heap) use the == operator Remember, the == operator cares only about the pattern of bits in the variable. The rules are the same whether the variable is a reference or primitive. So the == operator returns true if two reference variables refer to the same object! In that case, we don’t know what the bit pattern is (because it’s dependent on the JVM and hidden from us), but we do know that whatever it looks like, it will be the same for two references to a single object.

```java
Foo a =new Foo();
Foo b = new Foo();
Foo c = a;
if (a == b) { } // false
if (a == c) { } // true
if (b == c) { } // false
```

```java
int calcArea(int height, int width) {
return height * width;
}
int a = calcArea(7, 12);
short c = 7;
calcArea(c, 15);
int d = calcArea(57);
calcArea(2, 3);
long t = 42;
int f = calcArea(t, 17);
int g = calcArea();
calcArea();
byte h = calcArea(4, 20);
int j = calcArea(2, 3, 5);
private
```

```java
class XCopy {
public static void main(String[] args) {
int orig = 42;
XCopy x = new XCopy();
int y = x.go(orig);
System.out.println(orig + " " + y);
}
int go(int arg) {
arg = arg * 2;
return arg;
}
}
class Clock {
String time;
void setTime(String t) {
time = t;
}
void getTime() {
return time;
}
}
class ClockTestDrive {
public static void main(String[] args) {
Clock c = new Clock();
c.setTime("1245");
String tod = c.getTime();
System.out.println("time: "+tod);
}
}
```

```java
i < 9
index < 5
i < 20
index < 5
i < 7
index < 7
i < 19
index < 1
14 7
9 5
19 1
14 1
25 1
7 7
20 1
20 5
```

```java
public class Mix4 {
int counter = 0;
public static void main(String[] args) {
int count = 0;
Mix4[] mixes = new Mix4[20];
int i = 0;
while ( ) {
mixes[i] = new Mix4();
mixes[i].counter = mixes[i].counter + 1;
count = count + 1;
count = count + mixes[i].maybeNew(i);
i = i + 1;
}
System.out.println(count + " " +
mixes[1].counter);
}
public int maybeNew(int index) {
if ( ) {
Mix4 mix = new Mix4();
mix.counter = mix.counter + 1;
return 1;
}
return 0;
}
}
```

```java
public class Puzzle4 {
public static void main(String [] args) {
___________________________________
int number = 1;
int i = 0;
while (i < 6) {
___________________________
___________________________
number = number * 10;
_________________
}
int result = 0;
i = 6;
while (i > 0) {
_________________
result = result + ___________________
}
System.out.println("result " + result);
}
}
class ___________ {
int intValue;
________ ______ doStuff(int _________) {
if (intValue > 100) {
return _________________________
} else {
return _________________________
}
}
}
```

```java
%java Puzzle4
result 543345
```

When Buchanan roughly grabbed Jai’s arm from behind, Jai froze. Jai knew that Buchanan was as stupid as he was ugly and he didn’t want to spook the big guy. Buchanan ordered Jai into his boss’s office, but Jai’d done nothing wrong (lately), so he figured a little chat with Buchanan’s boss Leveler couldn’t be too bad. He’d been moving lots of neural-stimmers in the west side lately, and he figured Leveler would be pleased. Black market stimmers weren’t the best money pump around, but they were pretty harmless. Most of the stim-junkies he’d seen tapped out after a while and got back to life, maybe just a little less focused than before.

Leveler’s “office” was a skungy-looking skimmer, but once Buchanan shoved him in, Jai could see that it’d been modified to provide all the extra speed and armor that a local boss like Leveler could hope for. “Jai my boy,” hissed Leveler, “pleasure to see you again.” “Likewise I’m sure...,” said Jai, sensing the malice behind Leveler’s greeting, “We should be square Leveler, have I missed something?” “Ha! You’re making it look pretty good, Jai. Your volume is up, but I’ve been experiencing, shall we say, a little ‘breach’ lately,” said Leveler.

Jai winced involuntarily; he’d been a top drawer jack-hacker in his day. Anytime someone fig­ ured out how to break a street-jack’s security, unwanted attention turned toward Jai. “No way it’s me man,” said Jai, “not worth the downside. I’m retired from hacking, I just move my stuff and mind my own business.” “Yeah, yeah,” laughed Leveler, “I’m sure you’re clean on this one, but I’ll be losing big margins until this new jack-hacker is shut out!” “Well, best

bit, so what?” Jai responded, feeling a little queasy. “Neural edition’s how I let the stim- junkies know where the next drop will be,” explained Leveler. “Trouble is, some stim-junkie’s stayed straight long enough to figure out how to hack into my Warehousing database.” “I need a quick thinker like yourself, Jai, to take a look at my StimDrop Java NE class; methods, instance variables, the whole enchilada, and figure out how they’re getting in. It should...,” “HEY!” exclaimed Buchanan, “I don’t want no scum hacker like Jai nosin’ around my code!” “Easy big guy,” Jai saw his chance, “I’m sure you did a top rate job with your access modi...” “Don’t tell me, bit twiddler!” shouted Buchanan, “I left all of those junkie-level methods public so they could access the drop site data, but I marked all the critical WareHousing methods private. No­ body on the outside can access those methods, buddy, nobody!”

“I think I can spot your leak, Leveler. What say we drop Buchanan here off at the corner and take a cruise around the block?” suggested Jai. Buchanan clenched his fists and started toward Jai, but Leveler’s stunner was already on Buchanan’s neck, “Let it go, Buchanan,” sneered Lev­ eler, “Keep your hands where I can see them and step outside. I think Jai and I have some plans to make.” What did Jai suspect?

## Encapsulation <!--p118-->

```java
class Clock {
String time;
void setTime(String t) {
time = t;
}
return time;
}
}
class ClockTestDrive {
public static void main(String[] args) {
Clock c = new Clock();
c.setTime("1245");
String tod = c.getTime();
System.out.println("time: " + tod);
}
}
int a = calcArea(7, 12);
short c = 7;
calcArea(c, 15);
int d = calcArea(57);
calcArea(2, 3);
long t = 42;
int f = calcArea(t, 17);
int g = calcArea();
calcArea();
byte h = calcArea(4, 20);
int j = calcArea(2, 3, 5);
```

```java
public class Puzzle4 {
public static void main(String[] args) {
int number = 1;
int i = 0;
while (i < 6) {
number = number * 10;
}
int result = 0;
i = 6;
while (i > 0) {
}
System.out.println("result " + result);
}
}
```

```java
if (intValue > 100) {
} else {
}
}
}
```

```java
%java Puzzle4
result 543345
```

```java
i < 9
index < 5
i < 20
index < 5
i < 7
index < 7
i < 19
index < 1
14 7
9 5
19 1
14 1
25 1
7 7
20 1
20 5
```