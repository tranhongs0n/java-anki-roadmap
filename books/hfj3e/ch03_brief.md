# Chapter 3: Chapter 3: Know Your Variables

pages 87-108

So far you’ve used variables in two places—as object state (instance variables) and as local variables (variables declared within a method). Later, we’ll use variables as arguments (values sent to a method by the calling code), and as return types (values sent back to the caller of the method). You’ve seen variables declared as simple primitive integer values (type int). You’ve seen variables declared as something more complex like a String or an array. But there’s gotta

be more to life than integers, Strings, and arrays. What if you have a PetOwner object with a Dog instance variable? Or a Car with an Engine? In this chapter we’ll unwrap the mysteries of Java types (like the difference between primited and references) and look at what you can declare as a variable, what you can put in a variable, and what you can do with a variable. And we’ll finally see what life is truly like on the garbage-collectible heap.

## Declaring a variable <!--p88-->

```java
Rabbit hopper = new Giraffe();
```

## “I’d like a double mocha, no, make it an int.” <!--p89-->

```java
int x;
x = 234;
byte b = 89;
boolean isFun = true;
double d = 3456.98;
char c = ‘f’;
int z = x;
boolean isPunkRock;
isPunkRock = false;
boolean powerOn;
powerOn = isFun;
long big = 3456789L;
float f = 32.5f;
```

## You really don’t want to spill that... <!--p90-->

```java
int x = 24;
byte b = x;
//won’t work!!
```

Why doesn’t this work, you ask? After all, the value of x is 24, and 24 is definitely small enough to fit into a byte. You know that, and we know that, but all the compiler cares about is that you’re trying to put a big thing into a small thing, and there’s the possibility of spilling. Don’t expect the compiler to know what the value of x is, even if you happen to be able to see it literally in your code.

```java
1. int x = 34.5;
2. boolean boo = x;
3. int g = 17;
4. int y = g;
5. y = y + 10;
6. short s;
7. s = y;
8. byte b = 3;
9. byte v = b;
10. short n = 12;
11. v = n;
12. byte k = 128;
```

## Back away from that keyword! <!--p91-->

```java
public static void
```

```java
boolean char byte short int long float double
```

Java’s keywords, reserved words, and special identifiers. If you use these for names, the compiler will probably be very, very upset. No matter what you hear, do not, I repeat, do not let me ingest another large furry dog. _ catch double float int private super true abstract char else for interface protected switch try assert class enum goto long public synchronized void boolean const extends if native return this volatile

## Controlling your Dog object <!--p92-->

```java
myDog.bark();
```

```java
Dog myDog = new Dog();
```

```java
Dog myDog = new Dog();
```

```java
Dog myDog = new Dog();
```

```java
Dog myDog=new Dog();
```

```java
byte x = 7;
```

```java
Dog myDog = new Dog();
```

some other Dog. As long as it’s a Dog, I can be redirected (like reprogramming your remote to a different TV) to it. Unless...no never mind. HeadFirst: No, tell me. What were you gonna say? Reference:I don’t think you want to get into this now, but I’ll just give you the short version—if I’m marked as final, then once I am assigned a Dog, I can never be repro­ grammed to anything else but that one and only Dog. In other words, no other object can be assigned to me.

final, then you can refer to one Dog and then refer to a different Dog later. Can you ever refer to nothing at all? Is it possible to not be programmed to anything? Reference: Yes, but it disturbs me to talk about it. HeadFirst: Why is that? Reference: Because it means I’m null, and that’s upsetting to me. HeadFirst: You mean, because then you have no value? Reference: Oh, nullis a value. I’m still a remote control, but it’s like you brought home a new universal remote control and you don’t have a TV. I’m not programmed to control anything. They can press my buttons all day long, but nothing good happens. I just feel so...useless. A waste of bits. Granted, not that many bits, but still. And that’s not the worst part. If I am the only reference to a particular object and then I’m set to null (deprogrammed), it means that now nobody can get to that object I had been referring to.

```java
Book b = new Book();
Book c = new Book();
Book d = c;
```

that object again, because now it’s eligible for [producer, cue tragic music] garbage collection. Sniff. But do you think programmers ever consider that? Snif. Why, why can’t I be a primi­ tive? I hate being a reference. The responsibility, all the broken attachments... This week’s interview: Object Reference Java Exposed primitives and references Book b Declare two Book reference variables. Create two new Book objects. Assign the Book objects to the reference variables.

```java
c = b;
```

## Life on the garbage-collectible heap <!--p95-->

```java
Book b = new Book();
Book c = new Book();
b = c;
```

```java
c = null;
```

```java
nums[0] = 6;
nums[1] = 19;
nums[2] = 44;
nums[3] = 42;
nums[4] = 10;
nums[5] = 20;
nums[6] = 1;
```

```java
int[] nums;
nums = new int[7];
```

## An array is like a tray of cups <!--p97-->

```java
pets[0] = new Dog();
pets[1] = new Dog();
```

You can have an array object that’s declared to hold primitive values. In other words, the array object can have elements that are primitives, but the array itself is never a primitive. Regardless of what the array holds, the array itself is always an object! Arrays are always objects, whether they’re declared to hold primitives or object references. Dog array object (Dog[]) Dog[] pets Declare a Dog array variable

```java
Dog[] pets;
pets = new Dog[7];
```

## Make an array of Dogs <!--p98-->

```java
Dog fido = new Dog();
fido.name = "Fido";
```

```java
fido.bark();
fido.chaseCat();
```

```java
Dog[] myDogs = new Dog[3];
myDogs[0] = new Dog();
myDogs[0].name = "Fido";
myDogs[0].bark();
```

```java
class Dog {
String name;
public static void main(String[] args) {
// make a Dog object and access it
Dog dog1 = new Dog();
dog1.bark();
dog1.name = "Bart";
// now make a Dog array
Dog[] myDogs = new Dog[3];
// and put some dogs in it
myDogs[0] = new Dog();
myDogs[1] = new Dog();
myDogs[2] = dog1;
// now access the Dogs using the array
// references
myDogs[0].name = "Fred";
myDogs[1].name = "Marge";
// Hmmmm... what is myDogs[2] name?
System.out.print("last dog’s name is ");
System.out.println(myDogs[2].name);
// now loop through the array
// and tell all dogs to bark
int x = 0;
while (x < myDogs.length) {
myDogs[x].bark();
x = x + 1;
}
}
public void bark() {
System.out.println(name + " says Ruff!");
}
public void eat() {
}
public void chaseCat() {
}
}
```

```java
null says Ruff!
last dog’s name is Bart
Fred says Ruff!
Marge says Ruff!
Bart says Ruff!
```

```java
class Books {
String title;
String author;
}
class BooksTestDrive {
public static void main(String[] args) {
Books[] myBooks = new Books[3];
int x = 0;
myBooks[0].title = "The Grapes of Java";
myBooks[1].title = "The Java Gatsby";
myBooks[2].title = "The Java Cookbook";
myBooks[0].author = "bob";
myBooks[1].author = "sue";
myBooks[2].author = "ian";
while (x < 3) {
System.out.print(myBooks[x].title);
System.out.print(" by ");
System.out.println(myBooks[x].author);
x = x + 1;
}
}
}
class Hobbits {
String name;
public static void main(String[] args) {
Hobbits[] h = new Hobbits[3];
int z = 0;
while (z < 4) {
z = z + 1;
h[z] = new Hobbits();
h[z].name = "bilbo";
if (z == 1) {
h[z].name = "frodo";
}
if (z == 2) {
h[z].name = "sam";
}
System.out.print(h[z].name + " is a ");
System.out.println("good Hobbit name");
}
}
}
```

```java
islands[0] = "Bermuda";
islands[1] = "Fiji";
islands[2] = "Azores";
islands[3] = "Cozumel";
class TestArrays {
public static void main(String [] args) {
int ref;
while (y < 4) {
String [] islands = new String[4];
System.out.print("island = ");
int [] index = new int[4];
System.out.println(islands[ref]);
```

```java
% java TestArrays
island = Fiji
island = Cozumel
island = Bermuda
island = Azores
index[0] = 1;
index[1] = 3;
index[2] = 0;
index[3] = 2;
y = y + 1;
int y = 0;
ref = index[y];
```

```java
class Triangle {
double area;
int height;
int length;
public static void main(String[] args) {
____________
_______________________
while ( __________ ) {
__________________________
________.height = (x + 1) * 2;
________.length = x + 4;
__________________________
System.out.print("triangle " + x + ", area");
System.out.println(" = " + _______.area);
________________
}
______________
x = 27;
Triangle t5 = ta[2];
ta[2].area = 343;
System.out.print("y = " + y);
System.out.println(", t5 area = " + t5.area);
}
void setArea() {
____________ = (height * length) / 2;
}
```

```java
triangle 0, area = 4.0
triangle 1, area = 10.0
triangle 2, area = 18.0
triangle 3, area = ____
y = ______________________
```

```java
class HeapQuiz {
int id = 0;
public static void main(String[] args) {
int x = 0;
HeapQuiz[] hq = new HeapQuiz[5];
while (x < 3) {
hq[x] = new HeapQuiz();
hq[x].id = x;
x = x + 1;
}
hq[3] = hq[1];
hq[4] = hq[1];
hq[3] = null;
hq[4] = hq[0];
hq[0] = hq[3];
hq[3] = hq[2];
hq[2] = hq[0];
// do stuff
}
}
```

It was a dark and stormy night. Tawny strolled into the programmers’ bullpen like she owned the place. She knew that all the programmers would still be hard at work, and she wanted help. She needed a new method added to the pivotal class that was to be loaded into the client’s new top-secret Java-enabled cell phone. Heap space in the cell phone’s memory was tight, and everyone knew it. The normally raucous buzz in the bullpen fell to silence as Tawny eased her way to the white board. She sketched a quick overview of the new method’s functionality and slowly scanned the room. “Well folks, it’s crunch time,” she purred. “Whoever creates the most memory efficient version of this method is coming with me to the client’s launch party on Maui tomorrow...to help me install the new software.”

```java
Contact [] contacts = new Contact[10];
while (x < 10 ) { // make 10 contact objects
contacts[x] = new Contact();
x = x + 1;
}
// do complicated Contact list updating with contacts
```

```java
Contact contactRef;
while ( x < 10 ) { // make 10 contact objects
contactRef = new Contact();
x = x + 1;
}
// do complicated Contact list updating with contactRef
```

individual contact information for all ten allowable contacts; this was the best scheme I could cook up,” said Bob. Kate was next, already imagining coconut cocktails at the party, “Bob,” she said, “your solution’s a bit kludgy, don’t you think?” Kate smirked, “Take a look at this baby”: “I saved a bunch of reference variables worth of memory, Bob-o-rino, so put away your sunscreen,” mocked Kate. “Not so fast Kate!” said Tawny, “you’ve saved a little memory, but Bob’s coming with me.”

```java
class Books {
String title;
String author;
}
class BooksTestDrive {
public static void main(String[] args) {
Books[] myBooks = new Books[3];
int x = 0;
myBooks[0].title = "The Grapes of Java";
myBooks[1].title = "The Java Gatsby";
myBooks[2].title = "The Java Cookbook";
myBooks[0].author = "bob";
myBooks[1].author = "sue";
myBooks[2].author = "ian";
while (x < 3) {
System.out.print(myBooks[x].title);
System.out.print(" by ");
System.out.println(myBooks[x].author);
x = x + 1;
}
}
}
class TestArrays {
public static void main(String[] args) {
int[] index = new int[4];
index[0] = 1;
index[1] = 3;
index[2] = 0;
index[3] = 2;
String[] islands = new String[4];
islands[0] = "Bermuda";
islands[1] = "Fiji";
islands[2] = "Azores";
islands[3] = "Cozumel";
int y = 0;
int ref;
while (y < 4) {
ref = index[y];
System.out.print("island = ");
System.out.println(islands[ref]);
y = y + 1;
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
class Hobbits {
String name;
public static void main(String[] args) {
Hobbits[] h = new Hobbits[3];
z = z + 1;
h[z] = new Hobbits();
h[z].name = "bilbo";
if (z == 1) {
h[z].name = "frodo";
}
if (z == 2) {
h[z].name = "sam";
}
System.out.print(h[z].name + " is a ");
System.out.println("good Hobbit name");
}
}
}
```

```java
1. int x = 34.5;
2. boolean boo = x;
3. int g = 17;
4. int y = g;
5. y = y + 10;
6. short s;
7. s = y;
8. byte b = 3;
9. byte v = b;
10. short n = 12;
11. v = n;
12. byte k = 128;
```

```java
class Triangle {
double area;
int height;
int length;
```

```java
void setArea() {
}
}
%java Triangle
triangle 0, area = 4.0
triangle 1, area = 10.0
triangle 2, area = 18.0
```