# Chapter 9: Chapter 9: Life and Death of an Object

pages 275-312

using. If you’re gonna write Java, you’re gonna create objects. Sooner or later, you’re gonna have to let some of them go, or risk running out of RAM. In this chapter we look at how objects are created, where they live while they’re alive, and how to keep or abandon them efficiently. That means we’ll talk about the heap, the stack, scope, constructors, superclass constructors, null references, and more. Warning: this chapter contains material about object death that

## The Stack and the Heap: where things live

```java
public class Duck {
int size;
}
```

```java
public void foo(int x) {
int i = x + 3;
boolean b = true;
}
```

```java
public void doStuff() {
boolean b = true;
go(4);
}
public void go(int x) {
int z = x + 24;
crazy();
// imagine more code here
}
public void crazy() {
char c = 'a';
}
```

## Methods are stacked

## What about local variables that are objects?

```java
public class StackRef {
public void foof() {
barf();
}
public void barf() {
Duck d = new Duck();
}
}
```

```java
private Antenna ant;
```

```java
private Antenna ant = new Antenna();
```

```java
public class CellPhone {
private Antenna ant;
}
public class CellPhone {
private Antenna ant = new Antenna();
}
```

## The miracle of object creation

```java
Duck myDuck = new Duck();
```

```java
Duck myDuck=new Duck();
Duck myDuck = new Duck();
```

```java
Duck myDuck = new Duck();
```

```java
public Duck() {
}
```

```java
public Duck() {
// constructor code goes here
}
```

## Construct a Duck

```java
public class UseADuck {
public static void main (String[] args) {
Duck d = new Duck();
}
}
public class Duck {
public Duck() {
System.out.println("Quack");
}
}
```

```java
Quack
```

## Initializing the state of a new Duck

```java
public Duck() {
size = 34;
}
```

```java
public class Duck {
int size;
public Duck() {
System.out.println("Quack");
}
public void setSize(int newSize) {
size = newSize;
}
}
public class UseADuck {
public static void main(String[] args) {
Duck d = new Duck();
d.setSize(42);
}
}
```

```java
public Duck() { }
public void Duck() { }
```

```java
public class Duck {
int size;
public Duck(int duckSize) {
System.out.println("Quack");
size = duckSize;
System.out.println("size is " + size);
}
}
public class UseADuck {
public static void main (String[] args) {
Duck d = new Duck(42);
}
}
```

```java
Quack
size is 42
```

## Make it easy to make a Duck

```java
public class Duck2 {
int size;
public Duck2() {
// supply default size
size = 27;
}
public Duck2(int duckSize) {
// use duckSize parameter
size = duckSize;
}
}
```

```java
Duck2 d = new Duck2(15);
```

```java
Duck2 d2 = new Duck2();
```

```java
public class Duck {
int size;
public Duck(int newSize) {
if (newSize == 0) {
size = 27;
} else {
size = newSize;
}
}
}
```

```java
public class Mushroom {
public Mushroom(int size) { }
public Mushroom( ) { }
public Mushroom(boolean isMagic) { }
public Mushroom(boolean isMagic, int size) { }
public Mushroom(int size, boolean isMagic) { }
}
```

```java
cannot resolve symbol
:constructor Color()
location: class java.awt.
Color
Color c = new Color();
^
1 error
public class TestDuck {
public static void main(String[] args) {
int weight = 8;
float density = 2.3F;
String name = "Donald";
long[] feathers = {1, 2, 3, 4, 5, 6};
boolean canFly = true;
int airspeed = 22;
Duck[] d = new Duck[7];
d[0] = new Duck();
d[1] = new Duck(density, weight);
d[2] = new Duck(name, feathers);
d[3] = new Duck(canFly);
d[4] = new Duck(3.3F, airspeed);
d[5] = new Duck(false);
d[6] = new Duck(airspeed, density);
}
}
class Duck {
private int kilos = 6;
private float floatability = 2.1F;
private String name = "Generic";
private long[] feathers = {1, 2, 3,
4, 5, 6, 7};
private boolean canFly = true;
private int maxSpeed = 25;
public Duck() {
System.out.println("type 1 duck");
}
public Duck(boolean fly) {
canFly = fly;
System.out.println("type 2 duck");
}
public Duck(String n, long[] f) {
name = n;
feathers = f;
System.out.println("type 3 duck");
}
public Duck(int w, float f) {
kilos = w;
floatability = f;
System.out.println("type 4 duck");
}
public Duck(float density, int max) {
floatability = density;
maxSpeed = max;
System.out.println("type 5 duck");
}
}
```

```java
Duck d = new Duck();
public Duck(int size) { }
public Duck() { }
public Duck() { }
public Duck(int size) { }
public Duck(String name) { }
public Duck(String name, int size) { }
```

Here’s where it gets fun. Remember in the previous chapter we looked at the Snowboard object wrapping around an inner core representing the Object portion of the Snowboard class? The Big Point there was that every object holds not just its own declared instance variables, but also everything from its superclasses (which, at a minimum, means class Object, since every class extends Object). So when an object is created (because somebody said new; there is no other way to create an object other than someone, somewhere saying new on the class type), the object gets space for all the instance variables, from all the way up the inheritance tree. Think about it for a moment... a superclass might have setter methods encapsulating a private variable. But that variable has to live somewhere. When an object is created, it’s almost as though multiple objects materialize—the object being new’d and one object per each superclass. Conceptually, though, it’s much better to think of it like the picture below, where the object being created has layers of itself representing each superclass.

```java
public class Animal {
public Animal() {
System.out.println("Making an Animal");
}
}
public class Hippo extends Animal {
public Hippo() {
System.out.println("Making a Hippo");
}
}
public class TestHippo {
public static void main(String[] args) {
System.out.println("Starting...");
Hippo h = new Hippo();
}
}
% java TestHippo
Starting...
Making an Animal
Making a Hippo
% java TestHippo
Starting...
Making a Hippo
Making an Animal
```

## How do you invoke a superclass constructor?

```java
public class Duck extends Animal {
int size;
public Duck(int newSize) {
Animal();
size = newSize;
}
}
```

```java
public class Duck extends Animal {
int size;
public Duck(int newSize) {
super();
size = newSize;
}
}
```

```java
public ClassName() {
super();
}
```

```java
super();
```

```java
public Boop() {
super();
}
public Boop(int i) {
super();
size = i;
}
```

```java
public Boop() {
}
public Boop(int i) {
size = i;
}
public Boop(int i) {
size = i;
super();
}
```

## Superclass constructors with arguments

super() call? Of course. If you couldn’t, you’d never be able to extend a class that didn’t have a no-arg constructor. Imagine this scenario: all animals have a name. There’s a getName() method in class Animal that returns the value of the name instance variable. The instance variable is marked private, but the subclass (in this case, Hippo) inherits the getName() method. So here’s the problem: Hippo has a getName() method (through inheritance) but does not have the name instance variable. Hippo has to depend on the Animal part of himself to keep the name instance variable, and return it when someone calls getName() on a Hippo object. But...how does the Animal part get the name? The only reference Hippo has to the Animal part of himself is through super(), so that’s the place where Hippo sends the Hippo’s name up to the Animal part of himself, so that the Animal part can store it in the private name instance variable.

```java
public abstract class Animal {
private String name;
public String getName() {
return name;
}
public Animal(String theName) {
name = theName;
}
}
```

```java
public class Hippo extends Animal {
public Hippo(String name) {
super(name);
}
}
public class MakeHippo {
public static void main(String[] args) {
Hippo h = new Hippo("Buffy");
System.out.println(h.getName());
}
}
```

```java
Buffy
```

```java
import java.awt.Color;
class Mini extends Car {
private Color color;
public Mini() {
this(Color.RED);
}
public Mini(Color c) {
super("Mini");
color = c;
// more initialization
}
public Mini(int size) {
this(Color.RED);
super(size);
}
}
```

```java
javac Mini.java
Mini.java:16: call to super must
be first statement in constructor
super();
^
```

```java
public class Boo {
public Boo(int i) { }
public Boo(String s) { }
public Boo(String s, int i) { }
}
class SonOfBoo extends Boo {
public SonOfBoo() {
super("boo");
}
public SonOfBoo(int i) {
super("Fred");
}
public SonOfBoo(String s) {
super(42);
}
public SonOfBoo(int i, String s) {
}
public SonOfBoo(String a, String b, String c) {
super(a, b);
}
public SonOfBoo(int i, int j) {
super("man", j);
}
public SonOfBoo(int i, int x, int y) {
super(i, "star");
}
}
```

```java
cannot resolve symbol
symbol:constructor Boo()
```

```java
cannot resolve symbol
symbol : constructor Boo
(java.lang.String,java.
lang.String)
```

```java
cannot resolve symbol
symbol : constructor Boo
(int,java.lang.String)
```

```java
public class TestLifeOne {
public void read() {
int s = 42;
sleep();
}
public void sleep() {
s = 7;
}
}
```

```java
public void read() {
int s = 42;
// ‘s’ can be used only
// within this method.
// When this method ends,
// ‘s’ disappears completely.
}
public class Life {
int size;
public void setSize(int s) {
size = s;
// ‘s’ disappears at the
// end of this method,
// but ‘size’ can be used
// anywhere in the class
}
}
```

```java
public void doStuff() {
boolean b = true;
go(4);
}
public void go(int x) {
int z = x + 24;
crazy();
// imagine more code here
}
public void crazy() {
char c = 'a';
}
```

## What about reference variables?

```java
void go() {
Life z = new Life();
}
Life z = new Life();
z = new Life();
Life z = new Life();
z = null;
```

```java
public class StackRef {
public void foof() {
barf();
}
public void barf() {
Duck d = new Duck();
}
}
```

```java
public class ReRef {
Duck d = new Duck();
public void go() {
d = new Duck();
}
}
```

```java
public class ReRef {
Duck d = new Duck();
public void go() {
d = null;
}
}
```

```java
public class GC {
public static GC doStuff() {
GC newGC = new GC();
doStuff2(newGC);
return newGC;
}
public static void main(String[] args) {
GC gc1;
GC gc2 = new GC();
GC gc3 = new GC();
GC gc4 = gc3;
gc1 = doStuff();
// call more methods
}
public static void doStuff2(GC copyGC) {
GC localGC = copyGC;
}
}
```

```java
copyGC = null;
gc2 = null;
newGC = gc3;
gc1 = null;
newGC = null;
gc4 = null;
gc3 = gc2;
gc1 = gc4;
gc3 = null;
```

```java
class Bees {
Honey[] beeHoney;
}
class Raccoon {
Kit rk;
Honey rh;
}
class Kit {
Honey honey;
}
class Bear {
Honey hunny;
}
public class Honey {
public static void main(String[] args) {
Honey honeyPot = new Honey();
Honey[] ha = {honeyPot, honeyPot, honeyPot, honeyPot};
Bees bees = new Bees();
bees.beeHoney = ha;
Bear[] bears = new Bear[5];
for (int i = 0; i < 5; i++) {
bears[i] = new Bear();
bears[i].hunny = honeyPot;
}
Kit kit = new Kit();
kit.honey = honeyPot;
Raccoon raccoon = new Raccoon();
raccoon.rh = honeyPot;
raccoon.rk = kit;
kit = null;
} // end of main
}
```

drifts out of nominal toward cold,” Sarah said, exasperated. “We installed the new temp-bots last week. The readings on the radiator bots, designed to cool the living quarters, seem to be within spec, so we’ve focused our analysis on the heat retention bots, the bots that help to warm the quar­ ters.” Tom sighed, at first it had seemed that nanotechnology was going to really put them ahead of schedule. Now, with only five weeks left until launch, some of the orbiter’s key life support systems were still not passing the simulation gauntlet.

Sarah continued. “Overall, the ratio of retention bots to radiator bots is supposed to run 4:3.” “How’s power consumption, Sarah?” Tom asked. Sarah paused, “Well, that’s another thing, power consumption is running higher than anticipated. We’ve got a team tracking that down too, but because the nanos are wireless, it’s been hard to isolate the power consumption of the radiators from the retention bots.” “Overall power consumption ratios,” Sarah continued, “are designed to run 3:2 with the radiators pulling more power from the wireless grid.”

```java
import java.util.ArrayList;
class V2Radiator {
V2Radiator(ArrayList<SimUnit> list) {
for (int x = 0; x < 5; x++) {
list.add(new SimUnit("V2Radiator"));
}
}
}
class V3Radiator extends V2Radiator {
V3Radiator(ArrayList<SimUnit> lglist) {
super(lglist);
for (int g = 0; g < 10; g++) {
lglist.add(new SimUnit("V3Radiator"));
}
}
}
class RetentionBot {
RetentionBot(ArrayList<SimUnit> rlist) {
rlist.add(new SimUnit("Retention"));
}
}
```

```java
import java.util.ArrayList;
public class TestLifeSupportSim {
public static void main(String[] args) {
ArrayList<SimUnit> aList = new ArrayList<SimUnit>();
V2Radiator v2 = new V2Radiator(aList);
V3Radiator v3 = new V3Radiator(aList);
for (int z = 0; z < 20; z++) {
RetentionBot ret = new RetentionBot(aList);
}
}
}
class SimUnit {
String botType;
SimUnit(String type) {
botType = type;
}
int powerUse() {
if ("Retention".equals(botType)) {
return 2;
} else {
return 4;
}
}
}
```

```java
public class Honey {
public static void main(String[] args) {
Honey honeyPot = new Honey();
Honey[] ha = {honeyPot, honeyPot,
honeyPot, honeyPot};
Bees bees = new Bees();
bees.beeHoney = ha;
Bear[] bears = new Bear[5];
for (int i = 0; i < 5; i++) {
bears[i] = new Bear();
bears[i].hunny = honeyPot;
}
Kit kit = new Kit();
kit.honey = honeyPot;
Raccoon raccoon = new Raccoon();
raccoon.rh = honeyPot;
raccoon.rk = kit;
kit = null;
} // end of main
}
```

found the problem, Sarah, and I bet I know by what percentage your power usage readings are off too!” What did Tom suspect? How could he guess the power readings errors, and what few lines of code could you add to help debug this program? Five-Minute Mystery continued... Answers on page 273. object lifecycle Honey Object ( ends up null ) Popular Objects (from page 269) It probably wasn’t too hard to figure out that the Honey object first referred to by the honeyPot variable is by far the most “popular” object in this class. But maybe it was a little trickier to see that all of the variables that point from the code to the Honey object refer to the same object! There are a total of 12 active references to this object right before the main( ) method completes. The kit.honeyPot variable is valid for a while, but kit gets nulled at the end. Since raccoon.rk still refers to the Kit object, raccoon.kit.honeyPot (although never explicitly declared) refers to the object!

```java
copyGC = null;
gc2 = null;
newGC = gc3;
gc1 = null;
newGC = null;
gc4 = null;
gc3 = gc2;
gc1 = gc4;
gc3 = null;
```