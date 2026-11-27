# Chapter 8: Chapter 8: Serious Polymorphism

pages 237-274

(and not the GUI kind). We need to go beyond simple inheritance to a level of flexibility and extensibility you can get only by designing and coding to interface specifications. Some of the coolest parts of Java wouldn’t even be possible without interfaces, so even if you don’t design with them yourself, you still have to use them. But you’ll want to design with them. You’ll need to design with them. You’llwonder how you ever lived without them. What’s an interface?

It’s a 100% abstract class. What’s an abstract class? It’s a class that can’t be instantiated. What’s that good for? You’ll see in just a few moments. But if you think about the end of the previous chapter, and how we used polymorphic arguments so that a single Vet method could take Animal subclasses of all types, well, that was just scratching the surface. Interfaces are the poly in polymorphism. Theab in abstract. The caffeine in Java.

```java
Wolf aWolf = new Wolf();
```

```java
Animal aHippo = new Hippo();
```

```java
Animal anim = new Animal();
```

```java
abstract class Canine extends Animal {
public void roam() { }
}
```

```java
abstract public class Canine extends Animal
{
public void roam() { }
}
public class MakeCanine {
public void go() {
Canine c;
c = new Dog();
c = new Canine();
c.roam();
}
}
```

```java
% javac MakeCanine.java
MakeCanine.java:5: Canine is abstract;
cannot be instantiated
c = new Canine();
^
1 error
```

## Abstract vs. Concrete <!--p242-->

## Abstract methods <!--p243-->

```java
public abstract void eat();
```

## You MUST implement all abstract methods <!--p244-->

## Polymorphism in action <!--p246-->

```java
public class MyDogList {
private Dog[] dogs = new Dog[5];
private int nextIndex = 0;
public void add(Dog d) {
if (nextIndex < dogs.length) {
dogs[nextIndex] = d;
System.out.println("Dog added at " + nextIndex);
nextIndex++;
}
}
}
```

```java
public class MyAnimalList {
private Animal[] animals = new Animal[5];
private int nextIndex = 0;
public void add(Animal a) {
if (nextIndex < animals.length) {
animals[nextIndex] = a;
System.out.println("Animal added at " + nextIndex);
nextIndex++;
}
}
}
```

## Uh-oh, now we need to keep Cats, too <!--p247-->

```java
public class AnimalTestDrive {
public static void main(String[] args) {
MyAnimalList list = new MyAnimalList();
Dog dog = new Dog();
Cat cat = new Cat();
list.add(dog);
list.add(cat);
}
}
```

```java
% java AnimalTestDrive
Animal added at 0
Animal added at 1
```

other kind of animal added as well). We like this option best, so let’s change our class to make it more generic, to take Animals instead of just Dogs. We’ve highlighted the key changes (the logic is the same, of course, but the type has changed from Dog to Animal everywhere in the code). File Edit Window Help Harm Don’t panic. We’re not making a new Animal object; we’re making a new array object, of type Animal.

```java
public class Dog extends Object { }
```

## So what’s in this ultra-super-megaclass Object? <!--p249-->

```java
Dog a = new Dog();
Cat c = new Cat();
if (a.equals(c)) {
System.out.println("true");
} else {
System.out.println("false");
}
```

```java
Cat c = new Cat();
System.out.println(c.getClass());
```

```java
% java TestObject
false
```

```java
% java TestObject
class Cat
Cat c = new Cat();
System.out.println(c.hashCode());
```

```java
% java TestObject
8202111
Cat c = new Cat();
System.out.println(c.toString());
```

```java
% java TestObject
Cat@7d277f
```

```java
Object o = new Ferrari();
o.goFast(); //Not legal!
```

Before you run off and start using type Object for all your ultra-flexible argument and return types, you need to consider a little issue of using type Object as a reference. And keep in mind that we’re not talking about making instances of type Object; we’re talking about making instances of some other type, but using a reference of type Object. When you put an object into an ArrayList<Dog>, it goes in as a Dog and comes out as a Dog:

```java
ArrayList<Dog> myDogArrayList = new ArrayList<Dog>();
Dog aDog = new Dog();
myDogArrayList.add(aDog);
Dog d = myDogArrayList.get(0);
```

```java
ArrayList<Object> myDogArrayList = new ArrayList<Object>();
Dog aDog = new Dog();
myDogArrayList.add(aDog);
```

```java
Dog d = myDogArrayList.get(0);
```

But what happens when you declare it as ArrayList<Object>? If you want to make an ArrayList that will literally take any kind of Object, you declare it like this: But what happens when you try to get the Dog object and assign it to a Dog reference? Everything comes out of an ArrayList<Object> as a reference of type Object, regardless of what the actual object is or what the reference type was when you added the object to the list.

## Using polymorphic references of type Object has a price... <!--p251-->

```java
public void go() {
Dog aDog = new Dog();
Object sameDog = getObject(aDog);
}
public Object getObject(Object o) {
return o;
}
public void go() {
Dog aDog = new Dog();
Dog sameDog = getObject(aDog);
}
public Object getObject(Object o) {
return o;
}
```

## When a Dog won’t act like a Dog <!--p252-->

```java
DogPolyTest.java:10: incompatible types
found : java.lang.Object
required: Dog
Dog sameDog = getObject(aDog);
1 error ^
```

## Objects don’t bark <!--p253-->

```java
Object o = al.get(index);
int i = o.hashCode();
o.bark();
```

## Get in touch with your inner Object <!--p254-->

```java
Snowboard s = new Snowboard();
Object o = s;
```

```java
Object o = al.get(index);
Dog d = (Dog) o;
d.roam();
```

## Interface to the rescue! <!--p264-->

```java
public interface Pet {...}
public class Dog extends Canine implements Pet {...}
```

```java
public interface Pet {
public abstract void beFriendly();
public abstract void play();
}
public class Dog extends Canine implements Pet {
public void beFriendly() {...}
public void play() {..}
public void roam() {...}
public void eat() {...}
}
```

```java
public class Dog extends Animal implements
Pet, Saveable, Paintable { ... }
```

```java
class BuzzwordsReport extends Report {
void runReport() {
super.runReport();
buzzwordCompliance();
printReport();
}
void buzzwordCompliance() {...}
}
```

## Invoking the superclass version of a method <!--p268-->

```java
super.runReport();
```

```java
abstract class Report {
void runReport() {
// set up report
}
void printReport() {
// generic printing
}
}
```

```java
public interface Foo { }
public class Bar implements Foo { }
public interface Vinn { }
public abstract class Vout implements Vinn { }
public abstract class Muffie implements Whuffie { }
public class Fluffie extends Muffie { }
public interface Whuffie { }
public class Zoop { }
public class Boop extends Zoop { }
public class Goop extends Boop { }
public class Gamma extends Delta implements Epsilon { }
public interface Epsilon { }
public interface Beta { }
public class Alpha extends Gamma implements Beta { }
public class Delta { }
```

```java
%java ______________
5 class Acts
7 class Clowns
________Of76
```

```java
____________ Nose {
________________________
}
abstract class Picasso implements ______{
_________________________
return 7;
}
}
class _________ ________ __________ { }
class _________ ________ __________ {
___________________________
return 5;
}
}
public ___________ ________ extends Clowns {
public static void main(String[] args) {
____________________________
i[0] = new __________
i[1] = new __________
i[2] = new __________
for (int x = 0; x < 3; x++) {
System.out.println(__________________
+ " " + _______.getClass());
}
}
}
```

```java
public static void main(String[] args) {
```

```java
for (int x = 0; x < 3; x++) {
```

```java
}
}
}
%java Of76
5 class Acts
7 class Clowns
7 class Of76
```

```java
return 5;
}
}
```