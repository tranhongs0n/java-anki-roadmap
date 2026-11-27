# Chapter 7: Chapter 7: Better Living in Objectville

pages 205-236

Java code such that you could take more vacations, how much would it be worth to you? What if you could write code that someone else could extend, easily? And if you could write code that was flexible, for those pesky last-minute spec changes, would that be something you’d be interested in? Then this is your lucky day. For just three easy payments of 60 minutes time, you can have all this. When you get on the Polymorphism Plan, you’ll learn the 5 steps to bet­

ter class design, the 3 tricks to polymorphism, the 8 ways to make flexible code, and if you act now—a bonus lesson on the 4 tips for exploiting inheritance. Don’t delay, an offer this good will give you the design freedom and programming flexibility you deserve. It’s quick, it’s easy, and it’s available now. Start today, and we’ll throw in an extra level of abstraction! Better Living in Objectville

## Chair Wars Revisited... <!--p206-->

## Understanding Inheritance <!--p208-->

```java
public class Doctor {
boolean worksAtHospital;
void treatPatient() {
// perform a checkup
}
}
public class FamilyDoctor extends Doctor {
boolean makesHouseCalls;
void giveAdvice() {
// give homespun advice
}
}
public class Surgeon extends Doctor {
void treatPatient() {
// perform surgery
}
void makeIncision() {
// make incision (yikes!)
}
}
```

## Do all animals eat the same way? <!--p212-->

```java
Wolf w = new Wolf();
w.makeNoise();
w.roam();
w.eat();
w.sleep();
```

## Which method is called? <!--p215-->

## Using IS-A and HAS-A <!--p217-->

```java
public void roam() {
super.roam();
// my own roam stuff
}
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
Animal myDog = new Dog();
```

## polymorphism in action <!--p226-->

```java
Animal[] animals = new Animal[5];
animals[0] = new Dog();
animals[1] = new Cat();
animals[2] = new Wolf();
animals[3] = new Hippo();
animals[4] = new Lion();
for (Animal animal : animals) {
animal.eat();
animal.roam();
}
```

```java
class Vet {
public void giveShot(Animal a) {
// do horrible things to the Animal at
// the other end of the ‘a’ parameter
a.makeNoise();
}
}
class PetOwner {
public void start() {
Vet vet = new Vet();
Dog dog = new Dog();
Hippo hippo = new Hippo();
vet.giveShot(dog);
vet.giveShot(hippo);
}
}
```

```java
Appliance appliance = new Toaster();
```

## Keeping the contract: rules for overriding <!--p230-->

## Overloading a method <!--p231-->

```java
public class Overloads {
String uniqueID;
public int addNums(int a, int b) {
return a + b;
}
public double addNums(double a, double b) {
return a + b;
}
public void setUniqueID(String theID) {
// lots of validation code, and then:
uniqueID = theID;
}
public void setUniqueID(int ssNumber) {
String numString = "" + ssNumber;
setUniqueID(numString);
}
}
```

```java
class C extends B {
void m3() {
System.out.print("C's m3, " + (ivar + 6));
}
}
public class Mixed2 {
public static void main(String[] args) {
A a = new A();
B b = new B();
C c = new C();
A a2 = new C();
}
}
```

```java
class A {
int ivar = 7;
void m1() {
System.out.print("A's m1, ");
}
void m2() {
System.out.print("A's m2, ");
}
void m3() {
System.out.print("A's m3, ");
}
}
class B extends A {
void m1() {
System.out.print("B's m1, ");
}
}
```

```java
b.m1();
c.m2();
a.m3();
c.m1();
c.m2();
c.m3();
a.m1();
b.m2();
c.m3();
a2.m1();
a2.m2();
a2.m3();
A’s m1, A’s m2, C’s m3, 6
B’s m1, A’s m2, A’s m3,
A’s m1, B’s m2, A’s m3,
B’s m1, A’s m2, C’s m3, 13
B’s m1, C’s m2, A’s m3,
B’s m1, A’s m2, C’s m3, 6
A’s m1, A’s m2, C’s m3, 13
}
}
}
}
```

```java
public class MonsterTestDrive {
public static void main(String[] args) {
Monster[] monsters = new Monster[3];
monsters[0] = new Vampire();
monsters[1] = new Dragon();
monsters[2] = new Monster();
for (int i = 0; i < monsters.length; i++) {
monsters[i].frighten(i);
}
}
}
class Monster {
}
class Vampire extends Monster {
}
class Dragon extends Monster {
boolean frighten(int degree) {
System.out.println("breathe fire");
return true;
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
% java MonsterTestDrive
a bite?
breathe fire
arrrgh
boolean frighten(int d) {
System.out.println("arrrgh");
return true;
}
boolean frighten(int x) {
System.out.println("a bite?");
return false;
}
boolean frighten(int x) {
System.out.println("arrrgh");
return true;
}
int frighten(int f) {
System.out.println("a bite?");
return 1;
}
boolean frighten(int x) {
System.out.println("arrrgh");
return false;
}
boolean scare(int x) {
System.out.println("a bite?");
return true;
}
boolean frighten(int z) {
System.out.println("arrrgh");
return true;
}
boolean frighten(byte b) {
System.out.println("a bite?");
return true;
}
```

```java
public class Rowboat ________ ________ {
public ___________ rowTheBoat() {
System.out.print("stroke natasha");
}
}
public class ________ {
private int __________ ;
_______ void _________ ( ______ ) {
length = len;
}
public int getLength() {
________ _________ ;
}
public ___________ move() {
System.out.print("___________");
}
}
public class TestBoats {
______ ______ _______ main(String[] args){
_________ b1 = new Boat();
Sailboat b2 = new __________();
Rowboat ________ = new Rowboat();
b2.setLength(32);
b1.__________();
b3.__________();
_______.move();
}
}
public class __________ ________ Boat {
public _______ _________() {
System.out.print("___________");
}
}
```

```java
c.m1();
c.m2();
c.m3();
a.m1();
b.m2();
c.m3();
a2.m1();
a2.m2();
a2.m3();
A’s m1, A’s m2, C’s m3, 6
B’s m1, A’s m2, A’s m3,
A’s m1, B’s m2, A’s m3,
B’s m1, A’s m2, C’s m3, 13
B’s m1, C’s m2, A’s m3,
B’s m1, A’s m2, C’s m3, 6
A’s m1, A’s m2, C’s m3, 13
}
}
}
```

```java
arrrgh
breathe fire
arrrgh
```

```java
}
```